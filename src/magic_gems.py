"""
magic_gems.py
=============
Functions for constructing Magic Gems - polyhedral representations of magic squares.

A Magic Gem is constructed by:
1. Placing a magic square on a centered coordinate grid
2. Using square values as z-coordinates (centered around 0)
3. Treating each point as a vector from origin
4. Connecting points to form a polyhedron
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from scipy.spatial import ConvexHull, Delaunay
import json


def square_to_coordinates(square: np.ndarray, center_z: bool = True) -> np.ndarray:
    """
    Convert a magic square to 3D coordinates.
    
    Parameters
    ----------
    square : np.ndarray
        n×n magic square
    center_z : bool
        If True, center z-values around 0
        
    Returns
    -------
    np.ndarray
        Array of shape (n², 3) with (x, y, z) coordinates
    """
    n = square.shape[0]
    
    # Create centered x, y grid
    # For n=3: positions are -1, 0, 1
    # For n=4: positions are -1.5, -0.5, 0.5, 1.5
    offset = (n - 1) / 2
    
    coords = []
    for i in range(n):
        for j in range(n):
            x = j - offset  # Column -> x
            y = offset - i  # Row -> y (inverted so top is positive)
            z = square[i, j]
            coords.append([x, y, z])
    
    coords = np.array(coords)
    
    if center_z:
        # Center z around 0 by subtracting mean (which equals (n²+1)/2 for 1..n²)
        z_center = (n**2 + 1) / 2
        coords[:, 2] -= z_center
    
    return coords


def coords_to_vectors(coords: np.ndarray) -> np.ndarray:
    """
    Treat coordinates as vectors from origin.
    (This is essentially an identity function but clarifies intent.)
    
    Parameters
    ----------
    coords : np.ndarray
        Array of (x, y, z) coordinates
        
    Returns
    -------
    np.ndarray
        Same array, interpreted as vectors from origin
    """
    return coords.copy()


def compute_convex_hull(coords: np.ndarray) -> Optional[ConvexHull]:
    """
    Compute the convex hull of the Magic Gem points.
    
    Parameters
    ----------
    coords : np.ndarray
        3D coordinates
        
    Returns
    -------
    ConvexHull or None
        The convex hull object, or None if degenerate
    """
    try:
        hull = ConvexHull(coords)
        return hull
    except Exception:
        return None


def compute_delaunay(coords: np.ndarray) -> Optional[Delaunay]:
    """
    Compute Delaunay triangulation of the Magic Gem points.
    
    Parameters
    ----------
    coords : np.ndarray
        3D coordinates
        
    Returns
    -------
    Delaunay or None
        The triangulation, or None if degenerate
    """
    try:
        tri = Delaunay(coords)
        return tri
    except Exception:
        return None


def compute_gem_properties(coords: np.ndarray) -> Dict:
    """
    Compute geometric properties of a Magic Gem.
    
    Parameters
    ----------
    coords : np.ndarray
        3D coordinates of the gem vertices
        
    Returns
    -------
    Dict
        Dictionary of geometric properties
    """
    hull = compute_convex_hull(coords)
    
    props = {
        'num_points': len(coords),
        'centroid': coords.mean(axis=0).tolist(),
        'bounding_box': {
            'min': coords.min(axis=0).tolist(),
            'max': coords.max(axis=0).tolist()
        }
    }
    
    if hull is not None:
        props['hull_volume'] = hull.volume
        props['hull_area'] = hull.area
        props['num_hull_vertices'] = len(hull.vertices)
        props['num_hull_faces'] = len(hull.simplices)
    
    return props


def compute_moment_of_inertia(coords: np.ndarray, masses: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Compute the moment of inertia tensor for the Magic Gem.
    
    Assumes unit mass at each vertex unless masses provided.
    
    Parameters
    ----------
    coords : np.ndarray
        3D coordinates
    masses : np.ndarray, optional
        Mass at each vertex
        
    Returns
    -------
    np.ndarray
        3×3 inertia tensor
    """
    if masses is None:
        masses = np.ones(len(coords))
    
    I = np.zeros((3, 3))
    
    for m, (x, y, z) in zip(masses, coords):
        I[0, 0] += m * (y**2 + z**2)
        I[1, 1] += m * (x**2 + z**2)
        I[2, 2] += m * (x**2 + y**2)
        I[0, 1] -= m * x * y
        I[0, 2] -= m * x * z
        I[1, 2] -= m * y * z
    
    # Symmetric
    I[1, 0] = I[0, 1]
    I[2, 0] = I[0, 2]
    I[2, 1] = I[1, 2]
    
    return I


def compute_principal_moments(inertia_tensor: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute principal moments of inertia and principal axes.
    
    Parameters
    ----------
    inertia_tensor : np.ndarray
        3×3 inertia tensor
        
    Returns
    -------
    eigenvalues : np.ndarray
        Principal moments (sorted)
    eigenvectors : np.ndarray
        Principal axes (columns)
    """
    eigenvalues, eigenvectors = np.linalg.eigh(inertia_tensor)
    # Sort by eigenvalue
    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenvectors[:, idx]


def gems_are_equivalent(coords1: np.ndarray, coords2: np.ndarray, tol: float = 1e-10) -> bool:
    """
    Check if two Magic Gems are geometrically equivalent.
    
    Two gems are equivalent if one can be transformed to the other
    via rotation/reflection (the D4 symmetry group acts on the xy-plane).
    
    Parameters
    ----------
    coords1, coords2 : np.ndarray
        3D coordinates of two gems
    tol : float
        Numerical tolerance
        
    Returns
    -------
    bool
        True if gems are equivalent
    """
    # Compare sorted coordinate sets (simple but effective for small n)
    def sorted_coords(c):
        return tuple(sorted([tuple(np.round(p, 10)) for p in c]))
    
    # Generate all D4 transformations of coords1
    transforms = []
    
    # Rotation matrices around z-axis (0, 90, 180, 270 degrees)
    for k in range(4):
        theta = k * np.pi / 2
        R = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
        transforms.append(R)
        
        # Add reflection (flip x)
        Rf = R @ np.diag([-1, 1, 1])
        transforms.append(Rf)
    
    sorted2 = sorted_coords(coords2)
    
    for T in transforms:
        transformed = coords1 @ T.T
        if sorted_coords(transformed) == sorted2:
            return True
    
    return False


def compute_edge_lengths(coords: np.ndarray, hull: ConvexHull) -> np.ndarray:
    """
    Compute all edge lengths of the convex hull.
    
    Parameters
    ----------
    coords : np.ndarray
        Vertex coordinates
    hull : ConvexHull
        The convex hull
        
    Returns
    -------
    np.ndarray
        Array of edge lengths
    """
    edges = set()
    for simplex in hull.simplices:
        for i in range(len(simplex)):
            for j in range(i + 1, len(simplex)):
                edge = tuple(sorted([simplex[i], simplex[j]]))
                edges.add(edge)
    
    lengths = []
    for i, j in edges:
        length = np.linalg.norm(coords[i] - coords[j])
        lengths.append(length)
    
    return np.array(lengths)


def square_to_magic_gem(square: np.ndarray) -> Dict:
    """
    Full conversion of magic square to Magic Gem representation.
    
    Parameters
    ----------
    square : np.ndarray
        n×n magic square
        
    Returns
    -------
    Dict
        Complete Magic Gem data structure
    """
    coords = square_to_coordinates(square, center_z=True)
    vectors = coords_to_vectors(coords)
    hull = compute_convex_hull(coords)
    inertia = compute_moment_of_inertia(coords)
    principal_moments, principal_axes = compute_principal_moments(inertia)
    
    gem = {
        'square': square.tolist(),
        'coordinates': coords.tolist(),
        'vectors': vectors.tolist(),
        'properties': compute_gem_properties(coords),
        'inertia_tensor': inertia.tolist(),
        'principal_moments': principal_moments.tolist(),
        'principal_axes': principal_axes.tolist()
    }
    
    if hull is not None:
        gem['hull'] = {
            'vertices': hull.vertices.tolist(),
            'simplices': hull.simplices.tolist(),
            'volume': hull.volume,
            'area': hull.area
        }
        gem['edge_lengths'] = compute_edge_lengths(coords, hull).tolist()
    
    return gem


def save_gem(gem: Dict, filepath: str):
    """Save Magic Gem to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(gem, f, indent=2)


def load_gem(filepath: str) -> Dict:
    """Load Magic Gem from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    from magic_squares import get_canonical_3x3, siamese_method
    
    # Test with Lo Shu square
    lo_shu = get_canonical_3x3()
    print("Lo Shu Square:")
    print(lo_shu)
    
    coords = square_to_coordinates(lo_shu)
    print("\n3D Coordinates (centered):")
    print(coords)
    
    gem = square_to_magic_gem(lo_shu)
    print("\nMagic Gem Properties:")
    print(f"  Hull Volume: {gem['properties'].get('hull_volume', 'N/A'):.4f}")
    print(f"  Hull Area: {gem['properties'].get('hull_area', 'N/A'):.4f}")
    print(f"  Centroid: {gem['properties']['centroid']}")
    print(f"  Principal Moments: {gem['principal_moments']}")
    
    # Test 5×5
    siamese_5 = siamese_method(5)
    gem_5 = square_to_magic_gem(siamese_5)
    print(f"\n5×5 Magic Gem Hull Volume: {gem_5['properties'].get('hull_volume', 'N/A'):.4f}")

