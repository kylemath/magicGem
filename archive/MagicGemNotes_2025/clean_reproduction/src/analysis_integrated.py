"""
Integrated Analysis Module for Magic Square Research
=====================================================

This module consolidates the best analysis functions from the original
magic_squares project, providing a clean, organized interface for:
- Geometric analysis (convex hulls, point classification)
- EMD (Earth Mover's Distance) analysis
- Manifold analysis (dimension estimation, t-SNE)
- Persistence diagram analysis
- Comprehensive visualization generation

Original sources:
- magic_squares/analysis/geometry.py
- magic_squares/analysis/visualization.py
- magic_squares/analysis/analyze.py
- magic_squares/paper/draft4.py
- magic_squares/paper/draft5.py

Author: Kyle Elliott Mathewson
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from scipy.stats import linregress
from scipy.optimize import linear_sum_assignment
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime
import os
import json
import warnings

# Try to import optional dependencies
try:
    import ot
    HAS_POT = True
except ImportError:
    HAS_POT = False
    warnings.warn("POT (Python Optimal Transport) not installed. EMD functions will be limited.")

try:
    from ripser import ripser
    from persim import plot_diagrams
    HAS_RIPSER = True
except ImportError:
    HAS_RIPSER = False
    warnings.warn("ripser/persim not installed. Persistence analysis will be skipped.")


# =============================================================================
# CORE GEOMETRIC FUNCTIONS
# =============================================================================

def square_to_points(square):
    """
    Convert a magic square to a set of 3D points (i, j, value).
    
    Parameters
    ----------
    square : np.ndarray
        A magic square array
        
    Returns
    -------
    np.ndarray
        Array of 3D points with shape (n*n, 3)
    """
    n = square.shape[0]
    points = []
    for i in range(n):
        for j in range(n):
            points.append([i, j, square[i, j]])
    return np.array(points)


def compute_square_geometry(square):
    """
    Compute comprehensive geometric properties of a magic square.
    
    Parameters
    ----------
    square : np.ndarray
        A magic square array
        
    Returns
    -------
    dict
        Dictionary containing geometric properties:
        - points: 3D point cloud
        - hull_vertices: vertices of convex hull
        - hull_faces: faces of convex hull
        - hull_volume: volume of convex hull
        - hull_area: surface area of convex hull
        - cov_matrix: covariance matrix
        - eigenvalues: eigenvalues of covariance matrix
        - eigenvectors: eigenvectors of covariance matrix
    """
    points = square_to_points(square)
    
    try:
        hull = ConvexHull(points)
        hull_vertices = points[hull.vertices]
        hull_faces = [points[simplex] for simplex in hull.simplices]
        
        # Center the points and compute covariance
        centroid = np.mean(points, axis=0)
        centered_points = points - centroid
        cov_matrix = np.cov(centered_points.T)
        
        # Eigendecomposition
        eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
        idx = eigenvals.argsort()[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        return {
            'points': points,
            'hull': hull,
            'hull_vertices': hull_vertices,
            'hull_faces': hull_faces,
            'hull_volume': hull.volume,
            'hull_area': hull.area,
            'cov_matrix': cov_matrix,
            'eigenvalues': eigenvals,
            'eigenvectors': eigenvecs
        }
    except Exception as e:
        print(f"Error computing geometry: {e}")
        return None


def classify_points(points, hull, tolerance=1e-10):
    """
    Classify points as vertices, face points, or interior points.
    
    Parameters
    ----------
    points : np.ndarray
        Array of 3D points
    hull : ConvexHull
        Convex hull of the points
    tolerance : float
        Tolerance for face membership test
        
    Returns
    -------
    tuple
        (vertex_points, face_points, interior_points)
    """
    vertex_points = []
    face_points = []
    interior_points = []
    
    vertex_indices = set(hull.vertices)
    equations = hull.equations
    
    for i, point in enumerate(points):
        if i in vertex_indices:
            vertex_points.append(point)
            continue
        
        on_face = False
        for eq in equations:
            dist = np.abs(np.dot(eq[:-1], point) + eq[-1])
            if dist < tolerance:
                on_face = True
                break
        
        if on_face:
            face_points.append(point)
        else:
            interior_points.append(point)
    
    return (
        np.array(vertex_points) if vertex_points else np.empty((0, 3)),
        np.array(face_points) if face_points else np.empty((0, 3)),
        np.array(interior_points) if interior_points else np.empty((0, 3))
    )


def categorize_points(geo):
    """
    Categorize points from geometry dict (alternative interface).
    
    Parameters
    ----------
    geo : dict
        Geometry dictionary from compute_square_geometry
        
    Returns
    -------
    dict
        Dictionary with vertex_points, face_points, interior_points
    """
    points = geo['points']
    hull_vertices = geo['hull_vertices']
    faces = geo['hull_faces']
    
    vertex_points = []
    face_points = []
    interior_points = []
    
    def point_on_face(point, face_points, tolerance=1e-10):
        """Check if point lies on a triangular face"""
        v1 = face_points[1] - face_points[0]
        v2 = face_points[2] - face_points[0]
        normal = np.cross(v1, v2)
        if np.linalg.norm(normal) < tolerance:
            return False
        normal = normal / np.linalg.norm(normal)
        v = point - face_points[0]
        dist_to_plane = abs(np.dot(v, normal))
        return dist_to_plane < tolerance
    
    for point in points:
        if any(np.allclose(point, vertex) for vertex in hull_vertices):
            vertex_points.append(point)
        else:
            on_face = False
            for face in faces:
                if point_on_face(point, face):
                    on_face = True
                    break
            if on_face:
                face_points.append(point)
            else:
                interior_points.append(point)
    
    return {
        'vertex_points': np.array(vertex_points) if vertex_points else np.empty((0, 3)),
        'face_points': np.array(face_points) if face_points else np.empty((0, 3)),
        'interior_points': np.array(interior_points) if interior_points else np.empty((0, 3))
    }


def compute_angular_uniformity(points):
    """
    Compute the angular uniformity of a set of 3D points.
    
    Returns a value between 0 and 1 where 1 is perfectly uniform.
    """
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    
    xy = centered[:, 0]**2 + centered[:, 1]**2
    theta = np.arctan2(centered[:, 1], centered[:, 0])
    phi = np.arctan2(np.sqrt(xy), centered[:, 2])
    
    theta_std = np.std(theta)
    phi_std = np.std(phi)
    
    max_std = np.pi
    theta_uniformity = 1 - (theta_std / max_std)
    phi_uniformity = 1 - (phi_std / max_std)
    
    return (theta_uniformity + phi_uniformity) / 2


def analyze_point_patterns(squares):
    """
    Analyze point distribution patterns across all magic squares.
    
    Parameters
    ----------
    squares : list
        List of magic squares
        
    Returns
    -------
    dict
        Dictionary containing pattern statistics
    """
    patterns = {}
    total = len(squares)
    
    for i, square in enumerate(squares):
        if i % 100 == 0:
            print(f"  Processing square {i+1}/{total}...")
        
        geo = compute_square_geometry(square)
        if geo is None:
            continue
        
        cats = categorize_points(geo)
        pattern = (
            len(cats['vertex_points']),
            len(cats['face_points']),
            len(cats['interior_points'])
        )
        
        if pattern in patterns:
            patterns[pattern]['count'] += 1
        else:
            patterns[pattern] = {
                'count': 1,
                'vertices': pattern[0],
                'faces': pattern[1],
                'interior': pattern[2],
                'example': square
            }
    
    # Convert to sorted list
    pattern_list = []
    for pattern, data in patterns.items():
        pattern_list.append({
            'pattern': pattern,
            'count': data['count'],
            'frequency': data['count'] / total,
            **data
        })
    pattern_list.sort(key=lambda x: x['count'], reverse=True)
    
    return {
        'total_squares': total,
        'unique_patterns': len(patterns),
        'patterns': pattern_list
    }


# =============================================================================
# EMD (EARTH MOVER'S DISTANCE) FUNCTIONS
# =============================================================================

def compute_emd(square1, square2):
    """
    Compute Earth Mover's Distance between two magic squares.
    
    Uses the 3D point cloud representation and Euclidean ground metric.
    """
    if not HAS_POT:
        return compute_emd_simple(square1, square2)
    
    points1 = square_to_points(square1)
    points2 = square_to_points(square2)
    
    n = len(points1)
    
    # Compute cost matrix (Euclidean distances)
    cost_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cost_matrix[i, j] = np.linalg.norm(points1[i] - points2[j])
    
    # Uniform weights
    weights = np.ones(n) / n
    
    return float(ot.emd2(weights, weights, cost_matrix))


def compute_emd_simple(square1, square2):
    """
    Simple EMD approximation using Hungarian algorithm.
    """
    points1 = square_to_points(square1)
    points2 = square_to_points(square2)
    
    # Normalize
    points1 = points1 / np.max(np.abs(points1))
    points2 = points2 / np.max(np.abs(points2))
    
    n = len(points1)
    cost_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cost_matrix[i, j] = np.linalg.norm(points1[i] - points2[j])
    
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return cost_matrix[row_ind, col_ind].sum() / n


def compute_emd_matrix(squares, n_samples=None, verbose=True):
    """
    Compute pairwise EMD matrix for a set of squares.
    
    Parameters
    ----------
    squares : list
        List of magic squares
    n_samples : int, optional
        Sample size (if None, use all squares)
    verbose : bool
        Print progress
        
    Returns
    -------
    np.ndarray
        Symmetric distance matrix
    """
    if n_samples is not None and n_samples < len(squares):
        indices = np.random.choice(len(squares), n_samples, replace=False)
        squares = [squares[i] for i in indices]
    
    n = len(squares)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        if verbose and i % 10 == 0:
            print(f"  Computing EMD row {i+1}/{n}...")
        for j in range(i + 1, n):
            emd = compute_emd(squares[i], squares[j])
            matrix[i, j] = emd
            matrix[j, i] = emd
    
    return matrix


# =============================================================================
# MANIFOLD ANALYSIS FUNCTIONS
# =============================================================================

def estimate_local_dimension(points, k_range=range(3, 15)):
    """
    Estimate local intrinsic dimension using k-NN method.
    
    Parameters
    ----------
    points : np.ndarray
        Point cloud
    k_range : range
        Range of k values to test
        
    Returns
    -------
    tuple
        (mean_dimension, std_dimension)
    """
    dimensions = []
    
    for k in k_range:
        if k >= len(points):
            continue
        
        nn = NearestNeighbors(n_neighbors=k+1)
        nn.fit(points)
        distances, _ = nn.kneighbors(points)
        
        # Use log-log relationship
        log_r = np.log(distances[:, 1:].mean(axis=0) + 1e-10)
        log_k = np.log(np.arange(1, k+1))
        
        if len(log_r) > 1:
            slope, _, _, _, _ = linregress(log_k, log_r)
            if np.isfinite(slope):
                dimensions.append(1.0 / abs(slope) if abs(slope) > 0.01 else 10.0)
    
    if len(dimensions) == 0:
        return 2.0, 0.5
    
    return np.mean(dimensions), np.std(dimensions)


def analyze_manifold_structure(squares, n_samples=100):
    """
    Analyze the manifold structure of magic squares.
    
    Parameters
    ----------
    squares : list
        List of magic squares
    n_samples : int
        Number of samples for analysis
        
    Returns
    -------
    dict
        Dictionary with manifold analysis results
    """
    print("Analyzing manifold structure...")
    
    # Sample squares
    if len(squares) > n_samples:
        indices = np.random.choice(len(squares), n_samples, replace=False)
        sample = [squares[i] for i in indices]
    else:
        sample = squares
    
    # Create feature matrix (flattened squares)
    X = np.array([sq.flatten() for sq in sample])
    
    # Normalize
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
    X = np.nan_to_num(X)
    
    # Estimate local dimension
    local_dim, dim_std = estimate_local_dimension(X)
    print(f"  Local dimension: {local_dim:.2f} ± {dim_std:.2f}")
    
    # PCA analysis
    pca = PCA(n_components=min(10, X.shape[1]))
    X_pca = pca.fit_transform(X)
    var_explained = pca.explained_variance_ratio_
    cumulative_var = np.cumsum(var_explained)
    
    # Effective dimension (components needed for 95% variance)
    effective_dim = np.searchsorted(cumulative_var, 0.95) + 1
    print(f"  Effective dimension (95% variance): {effective_dim}")
    
    # t-SNE embedding
    print("  Computing t-SNE embedding...")
    perplexity = min(30, len(sample) - 1)
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    X_tsne = tsne.fit_transform(X)
    
    return {
        'local_dimension': (local_dim, dim_std),
        'effective_dimension': effective_dim,
        'variance_explained': var_explained,
        'cumulative_variance': cumulative_var,
        'pca_embedding': X_pca[:, :3] if X_pca.shape[1] >= 3 else X_pca,
        'tsne_embedding': X_tsne,
        'n_samples': len(sample)
    }


def identify_strata(squares, n_samples=100):
    """
    Identify potential strata in the magic square space.
    
    Uses Gaussian Mixture Model on local dimension estimates.
    """
    print("Identifying potential strata...")
    
    if len(squares) > n_samples:
        indices = np.random.choice(len(squares), n_samples, replace=False)
        sample = [squares[i] for i in indices]
    else:
        sample = squares
    
    # Compute local dimensions for each square
    local_dims = []
    for square in sample:
        geo = compute_square_geometry(square)
        if geo is not None:
            dim, _ = estimate_local_dimension(geo['points'], k_range=range(3, 8))
            local_dims.append(dim)
    
    local_dims = np.array(local_dims)
    valid_mask = np.isfinite(local_dims)
    local_dims = local_dims[valid_mask]
    
    if len(local_dims) < 10:
        print("  Not enough valid dimension estimates for strata identification")
        return None
    
    # Fit GMM to identify clusters
    gmm = GaussianMixture(n_components=2, random_state=42)
    labels = gmm.fit_predict(local_dims.reshape(-1, 1))
    
    # Compute statistics for each stratum
    strata = []
    for i in range(2):
        mask = labels == i
        strata.append({
            'mean_dimension': local_dims[mask].mean(),
            'std_dimension': local_dims[mask].std(),
            'count': mask.sum(),
            'proportion': mask.mean()
        })
    
    return {
        'local_dimensions': local_dims,
        'labels': labels,
        'strata': strata,
        'gmm_means': gmm.means_.flatten(),
        'gmm_weights': gmm.weights_
    }


# =============================================================================
# PERSISTENCE ANALYSIS FUNCTIONS
# =============================================================================

def compute_persistence_diagram(squares, max_dim=2):
    """
    Compute persistence diagram for magic squares.
    
    Parameters
    ----------
    squares : list
        List of magic squares
    max_dim : int
        Maximum homology dimension
        
    Returns
    -------
    dict or None
        Persistence data or None if ripser not available
    """
    if not HAS_RIPSER:
        print("  Persistence analysis requires ripser. Skipping.")
        return None
    
    print("Computing persistence diagrams...")
    
    # Create point cloud from flattened squares
    X = np.array([sq.flatten() / np.sum(sq) for sq in squares])
    
    # Scale to unit range
    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0) + 1e-10)
    X = np.nan_to_num(X)
    
    # Compute persistence
    result = ripser(X, maxdim=max_dim)
    diagrams = result['dgms']
    
    # Extract statistics
    persistence_stats = {}
    for dim, dgm in enumerate(diagrams):
        finite_mask = dgm[:, 1] != np.inf
        if finite_mask.sum() > 0:
            persistence = dgm[finite_mask, 1] - dgm[finite_mask, 0]
            persistence_stats[f'H{dim}'] = {
                'count': len(persistence),
                'mean_persistence': persistence.mean(),
                'max_persistence': persistence.max(),
                'total_persistence': persistence.sum()
            }
    
    return {
        'diagrams': diagrams,
        'stats': persistence_stats
    }


# =============================================================================
# COMPREHENSIVE VISUALIZATION FUNCTIONS
# =============================================================================

def plot_single_hull(square, save_path=None, title="Magic Square Convex Hull"):
    """
    Plot a single magic square's 3D representation with convex hull.
    """
    geo = compute_square_geometry(square)
    if geo is None:
        print("Failed to compute geometry")
        return
    
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    cats = categorize_points(geo)
    vertex_pts = cats['vertex_points']
    face_pts = cats['face_points']
    interior_pts = cats['interior_points']
    
    # Plot points
    if len(vertex_pts) > 0:
        ax.scatter(vertex_pts[:, 0], vertex_pts[:, 1], vertex_pts[:, 2],
                   c='red', s=150, label=f'Vertices ({len(vertex_pts)})', zorder=4)
    if len(face_pts) > 0:
        ax.scatter(face_pts[:, 0], face_pts[:, 1], face_pts[:, 2],
                   c='orange', s=100, label=f'Face Points ({len(face_pts)})', zorder=3)
    if len(interior_pts) > 0:
        ax.scatter(interior_pts[:, 0], interior_pts[:, 1], interior_pts[:, 2],
                   c='blue', s=80, label=f'Interior ({len(interior_pts)})', zorder=2)
    
    # Plot hull faces
    faces = geo['hull_faces']
    poly3d = [face for face in faces]
    collection = Poly3DCollection(poly3d, alpha=0.15, linewidth=1,
                                   edgecolor='black', facecolor='lightblue')
    ax.add_collection3d(collection)
    
    ax.set_xlabel('i')
    ax.set_ylabel('j')
    ax.set_zlabel('M[i,j]')
    ax.set_title(title)
    ax.legend()
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_multiple_squares(squares, save_path=None, grid_size=4):
    """
    Plot multiple magic squares as convex hulls in a grid.
    """
    n = min(grid_size * grid_size, len(squares))
    
    fig = plt.figure(figsize=(16, 16))
    fig.suptitle(f'Magic Square Convex Hulls ({n} squares)', fontsize=14)
    
    for idx in range(n):
        ax = fig.add_subplot(grid_size, grid_size, idx + 1, projection='3d')
        
        geo = compute_square_geometry(squares[idx])
        if geo is None:
            continue
        
        cats = categorize_points(geo)
        
        # Plot points
        if len(cats['vertex_points']) > 0:
            ax.scatter(cats['vertex_points'][:, 0], 
                       cats['vertex_points'][:, 1],
                       cats['vertex_points'][:, 2], c='red', s=10)
        if len(cats['face_points']) > 0:
            ax.scatter(cats['face_points'][:, 0],
                       cats['face_points'][:, 1],
                       cats['face_points'][:, 2], c='orange', s=8)
        if len(cats['interior_points']) > 0:
            ax.scatter(cats['interior_points'][:, 0],
                       cats['interior_points'][:, 1],
                       cats['interior_points'][:, 2], c='blue', s=6)
        
        # Plot hull
        for simplex in geo['hull'].simplices:
            ax.plot3D(geo['points'][simplex, 0],
                      geo['points'][simplex, 1],
                      geo['points'][simplex, 2], 'k-', alpha=0.3, linewidth=0.5)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_comprehensive_analysis(squares, save_path=None):
    """
    Generate comprehensive geometric analysis figure.
    """
    print("Generating comprehensive analysis figure...")
    
    # Compute geometric properties for all squares
    results = []
    for square in squares:
        geo = compute_square_geometry(square)
        if geo is None:
            continue
        
        cats = categorize_points(geo)
        results.append({
            'vertices': len(cats['vertex_points']),
            'volume': geo['hull_volume'],
            'area': geo['hull_area'],
            'eigenvalues': geo['eigenvalues'],
            'angular_unif': compute_angular_uniformity(geo['points'])
        })
    
    df = pd.DataFrame(results)
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    fig.suptitle('Comprehensive Geometric Analysis of Magic Squares', fontsize=14)
    
    # 1. Vertex count distribution
    axes[0, 0].hist(df['vertices'], bins=np.arange(7.5, 17.5, 1), color='steelblue', alpha=0.7)
    axes[0, 0].set_xlabel('Number of Vertices')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].set_title('Vertex Count Distribution')
    
    # 2. Volume distribution
    axes[0, 1].hist(df['volume'], bins=20, color='coral', alpha=0.7)
    axes[0, 1].set_xlabel('Hull Volume')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].set_title('Volume Distribution')
    
    # 3. Surface area distribution
    axes[0, 2].hist(df['area'], bins=20, color='green', alpha=0.7)
    axes[0, 2].set_xlabel('Hull Surface Area')
    axes[0, 2].set_ylabel('Count')
    axes[0, 2].set_title('Surface Area Distribution')
    
    # 4. Volume vs Area scatter
    axes[1, 0].scatter(df['volume'], df['area'], alpha=0.5, c='purple')
    axes[1, 0].set_xlabel('Volume')
    axes[1, 0].set_ylabel('Surface Area')
    axes[1, 0].set_title('Volume vs Surface Area')
    
    # 5. Angular uniformity
    axes[1, 1].hist(df['angular_unif'], bins=20, color='teal', alpha=0.7)
    axes[1, 1].set_xlabel('Angular Uniformity')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_title('Angular Uniformity Distribution')
    
    # 6. Eigenvalue ratios
    eig_data = np.array([r['eigenvalues'] for r in results])
    if len(eig_data) > 0:
        ratios = eig_data[:, 1] / (eig_data[:, 0] + 1e-10)
        axes[1, 2].hist(ratios, bins=20, color='gold', alpha=0.7)
        axes[1, 2].set_xlabel('λ₂/λ₁ Ratio')
        axes[1, 2].set_ylabel('Count')
        axes[1, 2].set_title('Eigenvalue Ratio Distribution')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return df


def plot_manifold_analysis(manifold_results, save_path=None):
    """
    Plot manifold analysis results.
    """
    fig = plt.figure(figsize=(15, 10))
    
    # 1. t-SNE embedding
    ax1 = fig.add_subplot(2, 2, 1)
    tsne = manifold_results['tsne_embedding']
    ax1.scatter(tsne[:, 0], tsne[:, 1], alpha=0.6, c='steelblue')
    ax1.set_title('t-SNE Embedding of Magic Squares')
    ax1.set_xlabel('t-SNE 1')
    ax1.set_ylabel('t-SNE 2')
    
    # 2. Variance explained
    ax2 = fig.add_subplot(2, 2, 2)
    var = manifold_results['variance_explained']
    ax2.bar(range(1, len(var)+1), var, color='coral')
    ax2.plot(range(1, len(var)+1), manifold_results['cumulative_variance'], 'ko-')
    ax2.axhline(0.95, color='r', linestyle='--', label='95% threshold')
    ax2.set_xlabel('Principal Component')
    ax2.set_ylabel('Variance Explained')
    ax2.set_title('PCA Variance Analysis')
    ax2.legend()
    
    # 3. Local dimension
    ax3 = fig.add_subplot(2, 2, 3)
    dim_mean, dim_std = manifold_results['local_dimension']
    ax3.bar(['Local Dimension'], [dim_mean], yerr=[dim_std], capsize=10, color='green')
    ax3.axhline(2, color='r', linestyle='--', label='Expected for surface')
    ax3.set_ylabel('Dimension')
    ax3.set_title(f'Local Dimension: {dim_mean:.2f} ± {dim_std:.2f}')
    ax3.legend()
    
    # 4. Summary text
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')
    
    summary = (
        r"$\mathbf{Manifold\ Analysis\ Summary}$" + "\n\n"
        f"Number of samples: {manifold_results['n_samples']}\n\n"
        f"Local dimension: {dim_mean:.2f} ± {dim_std:.2f}\n\n"
        f"Effective dimension (95% var): {manifold_results['effective_dimension']}\n\n"
        f"Top 3 PCs explain: {manifold_results['cumulative_variance'][2]:.1%} of variance\n\n"
        r"$\mathbf{Interpretation:}$" + "\n"
        "The local dimension suggests magic squares\n"
        "form an approximately 2-dimensional manifold\n"
        "embedded in 16-dimensional space."
    )
    ax4.text(0.1, 0.9, summary, fontsize=11, va='top', transform=ax4.transAxes)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_distance_distributions(squares, emd_matrix, save_path=None):
    """
    Plot EMD distance distributions.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Distance histogram
    upper_tri = emd_matrix[np.triu_indices_from(emd_matrix, k=1)]
    axes[0, 0].hist(upper_tri, bins=30, color='steelblue', alpha=0.7)
    axes[0, 0].set_xlabel('EMD Distance')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution of Pairwise EMD Distances')
    axes[0, 0].axvline(upper_tri.mean(), color='r', linestyle='--',
                       label=f'Mean: {upper_tri.mean():.4f}')
    axes[0, 0].legend()
    
    # 2. Distance matrix heatmap
    n_show = min(50, len(emd_matrix))
    im = axes[0, 1].imshow(emd_matrix[:n_show, :n_show], cmap='viridis')
    plt.colorbar(im, ax=axes[0, 1])
    axes[0, 1].set_title(f'EMD Distance Matrix (first {n_show} squares)')
    
    # 3. k-NN distances
    k_range = range(1, min(10, len(squares)-1))
    mean_distances = []
    for k in k_range:
        kth_distances = []
        for i in range(len(emd_matrix)):
            sorted_dists = np.sort(emd_matrix[i])[1:k+1]
            if len(sorted_dists) >= k:
                kth_distances.append(sorted_dists[-1])
        if kth_distances:
            mean_distances.append(np.mean(kth_distances))
    
    axes[1, 0].plot(list(k_range)[:len(mean_distances)], mean_distances, 'o-')
    axes[1, 0].set_xlabel('k')
    axes[1, 0].set_ylabel('Mean k-th Nearest Neighbor Distance')
    axes[1, 0].set_title('k-NN Distance Scaling')
    
    # 4. Summary statistics
    axes[1, 1].axis('off')
    stats_text = (
        f"EMD Distance Statistics\n"
        f"{'='*30}\n\n"
        f"Mean: {upper_tri.mean():.4f}\n"
        f"Std: {upper_tri.std():.4f}\n"
        f"Min: {upper_tri.min():.4f}\n"
        f"Max: {upper_tri.max():.4f}\n"
        f"Median: {np.median(upper_tri):.4f}\n\n"
        f"Number of pairs: {len(upper_tri)}"
    )
    axes[1, 1].text(0.1, 0.9, stats_text, fontsize=12, va='top',
                    fontfamily='monospace', transform=axes[1, 1].transAxes)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_example_walkthrough(square, save_path=None):
    """
    Create step-by-step analysis walkthrough figure.
    """
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Complete Analysis Pipeline for Magic Squares', fontsize=14)
    
    geo = compute_square_geometry(square)
    cats = categorize_points(geo)
    points = geo['points']
    hull = geo['hull']
    
    # Step 1: Original square
    ax1 = fig.add_subplot(2, 4, 1)
    ax1.axis('off')
    ax1.set_title('Step 1: Original Square', fontweight='bold')
    table_data = [[f"{square[i,j]:.0f}" for j in range(4)] for i in range(4)]
    table = ax1.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    # Step 2: R³ embedding
    ax2 = fig.add_subplot(2, 4, 2, projection='3d')
    ax2.scatter(points[:, 0], points[:, 1], points[:, 2],
                c=points[:, 2], cmap='viridis', s=50)
    ax2.set_title('Step 2: R³ Embedding', fontweight='bold')
    
    # Step 3: Convex hull
    ax3 = fig.add_subplot(2, 4, 3, projection='3d')
    ax3.scatter(points[:, 0], points[:, 1], points[:, 2],
                c=points[:, 2], cmap='viridis', s=50)
    for simplex in hull.simplices:
        ax3.plot3D(points[simplex, 0], points[simplex, 1],
                   points[simplex, 2], 'k-', alpha=0.4)
    ax3.set_title('Step 3: Convex Hull', fontweight='bold')
    
    # Step 4: Point classification
    ax4 = fig.add_subplot(2, 4, 4, projection='3d')
    if len(cats['vertex_points']) > 0:
        ax4.scatter(*cats['vertex_points'].T, c='red', s=80, label='Vertices')
    if len(cats['face_points']) > 0:
        ax4.scatter(*cats['face_points'].T, c='orange', s=60, label='Face')
    if len(cats['interior_points']) > 0:
        ax4.scatter(*cats['interior_points'].T, c='blue', s=40, label='Interior')
    ax4.set_title('Step 4: Classification', fontweight='bold')
    ax4.legend(fontsize=7)
    
    # Step 5: Eigenvalue analysis
    ax5 = fig.add_subplot(2, 4, 5)
    eigenvalues = geo['eigenvalues']
    ax5.bar(range(len(eigenvalues)), eigenvalues, color='steelblue')
    ax5.set_title('Step 5: Eigenvalues', fontweight='bold')
    ax5.set_xlabel('Index')
    ax5.set_ylabel('Value')
    
    # Step 6: Dimension estimation
    ax6 = fig.add_subplot(2, 4, 6)
    ax6.axis('off')
    local_dim, dim_std = estimate_local_dimension(points)
    dim_text = f"Local Dimension: {local_dim:.2f} ± {dim_std:.2f}\n\nInterpretation:\nNon-integer dimension\nsuggests stratified structure"
    ax6.text(0.5, 0.5, dim_text, ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax6.set_title('Step 6: Dimension', fontweight='bold')
    
    # Step 7: Properties summary
    ax7 = fig.add_subplot(2, 4, 7)
    ax7.axis('off')
    props_text = (
        f"Hull vertices: {len(hull.vertices)}\n"
        f"Hull volume: {hull.volume:.2f}\n"
        f"Hull area: {hull.area:.2f}\n"
        f"Magic sum: {np.sum(square[0, :]):.0f}"
    )
    ax7.text(0.5, 0.5, props_text, ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    ax7.set_title('Step 7: Properties', fontweight='bold')
    
    # Step 8: Conclusions
    ax8 = fig.add_subplot(2, 4, 8)
    ax8.axis('off')
    conclusions = (
        "Key Findings:\n\n"
        f"• {len(cats['vertex_points'])} extremal values\n"
        f"• ~2D manifold structure\n"
        "• Geometric properties\n"
        "  encode combinatorics"
    )
    ax8.text(0.5, 0.5, conclusions, ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax8.set_title('Step 8: Conclusions', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

def run_full_analysis(squares, output_dir='paper/figures'):
    """
    Run the complete analysis pipeline and generate all figures.
    
    Parameters
    ----------
    squares : list
        List of magic squares
    output_dir : str
        Directory to save figures
        
    Returns
    -------
    dict
        Dictionary containing all analysis results
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("Running Full Magic Square Analysis Pipeline")
    print("="*60)
    
    results = {}
    
    # Use Dürer's square as example
    durer = np.array([
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ])
    
    # 1. Example walkthrough
    print("\n1. Generating example walkthrough...")
    plot_example_walkthrough(durer, f'{output_dir}/example_walkthrough.png')
    
    # 2. Single hull visualization
    print("\n2. Generating single hull visualization...")
    plot_single_hull(durer, f'{output_dir}/single_hull.png')
    
    # 3. Multiple squares grid
    print("\n3. Generating multiple squares grid...")
    plot_multiple_squares(squares[:16], f'{output_dir}/multiple_squares.png')
    
    # 4. Comprehensive geometric analysis
    print("\n4. Running comprehensive geometric analysis...")
    geo_df = plot_comprehensive_analysis(squares, f'{output_dir}/comprehensive_analysis.png')
    results['geometric_df'] = geo_df
    
    # 5. Point pattern analysis
    print("\n5. Analyzing point patterns...")
    patterns = analyze_point_patterns(squares)
    results['patterns'] = patterns
    print(f"  Found {patterns['unique_patterns']} unique patterns")
    
    # 6. Manifold analysis
    print("\n6. Running manifold analysis...")
    manifold_results = analyze_manifold_structure(squares, n_samples=100)
    results['manifold'] = manifold_results
    plot_manifold_analysis(manifold_results, f'{output_dir}/manifold_analysis.png')
    
    # 7. Strata identification
    print("\n7. Identifying strata...")
    strata_results = identify_strata(squares, n_samples=100)
    results['strata'] = strata_results
    
    # 8. EMD analysis (if POT available)
    if HAS_POT:
        print("\n8. Computing EMD distances...")
        emd_matrix = compute_emd_matrix(squares, n_samples=50)
        results['emd_matrix'] = emd_matrix
        plot_distance_distributions(squares[:50], emd_matrix, 
                                    f'{output_dir}/distance_distributions.png')
    
    # 9. Persistence analysis (if ripser available)
    if HAS_RIPSER:
        print("\n9. Computing persistence diagrams...")
        persistence_results = compute_persistence_diagram(squares[:100])
        results['persistence'] = persistence_results
    
    print("\n" + "="*60)
    print(f"Analysis complete. Figures saved to {output_dir}/")
    print("="*60)
    
    return results


if __name__ == "__main__":
    # Test with example data
    import json
    
    # Try to load squares
    json_path = Path(__file__).parent.parent / 'web' / 'assets' / 'data' / 'unique_squares.json'
    
    if json_path.exists():
        with open(json_path) as f:
            squares_list = json.load(f)
        squares = [np.array(sq) for sq in squares_list]
        print(f"Loaded {len(squares)} magic squares")
        
        results = run_full_analysis(squares)
    else:
        print(f"Could not find {json_path}")
        print("Testing with Dürer's magic square...")
        durer = np.array([
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1]
        ])
        plot_example_walkthrough(durer)

