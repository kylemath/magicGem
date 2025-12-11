"""
Investigation of the Trimodal Structure in n=4 Magic Squares

The paper observes that 880 n=4 magic squares cluster into 3 distinct
bands of perturbation resistance. This script investigates what
geometric or algebraic properties distinguish these classes.
"""

import numpy as np
from scipy.spatial import ConvexHull
from itertools import permutations
import json
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

def square_to_coordinates(square: np.ndarray) -> np.ndarray:
    """Convert magic square to centered 3D coordinates."""
    n = square.shape[0]
    offset = (n - 1) / 2
    z_center = (n**2 + 1) / 2
    coords = []
    for i in range(n):
        for j in range(n):
            x, y, z = j - offset, offset - i, square[i, j] - z_center
            coords.append([x, y, z])
    return np.array(coords)

def compute_total_magic_energy(square: np.ndarray) -> float:
    """Compute total magic energy E(S)."""
    coords = square_to_coordinates(square)
    n = square.shape[0]
    
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    
    cov_xz = np.mean(x * z)
    cov_yz = np.mean(y * z)
    
    n_sq = n * n
    z_flat = square.flatten() - (n_sq + 1) / 2
    
    D_main = np.zeros(n_sq)
    D_anti = np.zeros(n_sq)
    for i in range(n):
        D_main[i * n + i] = 1
        D_anti[i * n + (n - 1 - i)] = 1
    
    cov_main = np.mean(D_main * z_flat)
    cov_anti = np.mean(D_anti * z_flat)
    
    return cov_xz**2 + cov_yz**2 + cov_main**2 + cov_anti**2

def is_magic_square(square: np.ndarray) -> bool:
    """Check if arrangement is a magic square."""
    n = square.shape[0]
    M = n * (n*n + 1) // 2
    
    if not all(np.sum(square, axis=1) == M):
        return False
    if not all(np.sum(square, axis=0) == M):
        return False
    if np.trace(square) != M:
        return False
    if np.trace(np.fliplr(square)) != M:
        return False
    return True

def generate_magic_4x4_squares(max_count=1000) -> List[np.ndarray]:
    """
    Generate n=4 magic squares by testing arrangements.
    This is a brute-force approach that generates many squares.
    """
    print("Generating n=4 magic squares...")
    squares = []
    
    # We'll use a smarter approach: start from known magic squares
    # and apply transformations
    
    # Frénicle's canonical 4x4 magic square
    base_squares = [
        np.array([[1, 15, 14, 4],
                  [12, 6, 7, 9],
                  [8, 10, 11, 5],
                  [13, 3, 2, 16]]),
        np.array([[1, 14, 15, 4],
                  [8, 11, 10, 5],
                  [12, 7, 6, 9],
                  [13, 2, 3, 16]]),
        np.array([[2, 16, 13, 3],
                  [11, 5, 8, 10],
                  [7, 9, 12, 6],
                  [14, 4, 1, 15]]),
    ]
    
    # Generate D4 variants of each base
    all_squares = []
    seen = set()
    
    for base in base_squares:
        current = base.copy()
        for _ in range(4):
            # Add rotation
            key = tuple(current.flatten())
            if key not in seen:
                seen.add(key)
                all_squares.append(current.copy())
            # Add reflection
            reflected = np.fliplr(current)
            key = tuple(reflected.flatten())
            if key not in seen:
                seen.add(key)
                all_squares.append(reflected.copy())
            current = np.rot90(current)
    
    # Also try row/column permutations that preserve magic property
    # This is complex - skip for now
    
    print(f"Generated {len(all_squares)} unique squares from base set")
    
    # Verify all are magic
    for sq in all_squares:
        assert is_magic_square(sq), "Generated non-magic square!"
    
    return all_squares

def compute_min_perturbation_gap(square: np.ndarray) -> Dict:
    """Compute minimum perturbation gap for a square."""
    n = square.shape[0]
    base_energy = compute_total_magic_energy(square)
    
    min_gap = float('inf')
    min_positions = None
    gaps = []
    
    for i1 in range(n):
        for j1 in range(n):
            for i2 in range(n):
                for j2 in range(n):
                    if (i1, j1) < (i2, j2):
                        perturbed = square.copy()
                        perturbed[i1, j1], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i1, j1]
                        gap = compute_total_magic_energy(perturbed) - base_energy
                        gaps.append(gap)
                        
                        if gap < min_gap:
                            min_gap = gap
                            min_positions = ((i1, j1), (i2, j2))
    
    return {
        'min_gap': float(min_gap),
        'mean_gap': float(np.mean(gaps)),
        'positions': min_positions
    }

def compute_geometric_properties(square: np.ndarray) -> Dict:
    """Compute geometric properties of the Magic Gem."""
    coords = square_to_coordinates(square)
    
    try:
        hull = ConvexHull(coords)
        return {
            'hull_volume': hull.volume,
            'hull_area': hull.area,
            'n_hull_vertices': len(hull.vertices),
            'interior_points': len(coords) - len(hull.vertices)
        }
    except:
        return {'error': 'Hull computation failed'}

def compute_spectral_properties(square: np.ndarray) -> Dict:
    """Compute spectral properties of the magic square matrix."""
    eigenvalues = np.linalg.eigvals(square)
    det = np.linalg.det(square)
    
    return {
        'determinant': float(det),
        'trace': float(np.trace(square)),
        'eigenvalues': sorted([float(np.real(e)) for e in eigenvalues])[::-1]
    }

def analyze_trimodal_structure():
    """Main analysis function."""
    print("="*70)
    print("TRIMODAL STRUCTURE INVESTIGATION FOR n=4 MAGIC SQUARES")
    print("="*70)
    
    squares = generate_magic_4x4_squares()
    
    print(f"\nAnalyzing {len(squares)} magic squares...")
    
    results = []
    
    for i, sq in enumerate(squares):
        gap_info = compute_min_perturbation_gap(sq)
        geom_info = compute_geometric_properties(sq)
        spec_info = compute_spectral_properties(sq)
        
        results.append({
            'index': i,
            'square': sq.tolist(),
            'min_gap': gap_info['min_gap'],
            'mean_gap': gap_info['mean_gap'],
            'geometry': geom_info,
            'spectral': spec_info
        })
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i+1}/{len(squares)}")
    
    # Analyze gap distribution
    gaps = [r['min_gap'] for r in results]
    gaps = np.array(gaps)
    
    print("\n" + "="*70)
    print("GAP DISTRIBUTION ANALYSIS")
    print("="*70)
    print(f"Min gap: {gaps.min():.6f}")
    print(f"Max gap: {gaps.max():.6f}")
    print(f"Mean gap: {gaps.mean():.6f}")
    print(f"Std gap: {gaps.std():.6f}")
    
    # Look for clusters
    unique_gaps = sorted(set([round(g, 6) for g in gaps]))
    print(f"\nUnique gap values: {len(unique_gaps)}")
    print(f"Gap values: {unique_gaps[:10]}")
    
    # Correlate with geometric properties
    print("\n" + "="*70)
    print("CORRELATION WITH GEOMETRIC PROPERTIES")
    print("="*70)
    
    hull_vertices = [r['geometry'].get('n_hull_vertices', 0) for r in results]
    hull_volumes = [r['geometry'].get('hull_volume', 0) for r in results]
    determinants = [r['spectral']['determinant'] for r in results]
    
    print(f"\nHull vertices: {set(hull_vertices)}")
    
    # Group by min_gap and analyze
    gap_groups = {}
    for r in results:
        gap_key = round(r['min_gap'], 4)
        if gap_key not in gap_groups:
            gap_groups[gap_key] = []
        gap_groups[gap_key].append(r)
    
    print(f"\nGap groups: {len(gap_groups)}")
    for gap_key in sorted(gap_groups.keys())[:5]:
        group = gap_groups[gap_key]
        print(f"\n  Gap = {gap_key}:")
        print(f"    Count: {len(group)}")
        vols = [g['geometry'].get('hull_volume', 0) for g in group]
        dets = [g['spectral']['determinant'] for g in group]
        print(f"    Hull volumes: {min(vols):.2f} to {max(vols):.2f}")
        print(f"    Determinants: {set([round(d, 2) for d in dets])}")
    
    # Save detailed results
    with open('n4_trimodal_results.json', 'w') as f:
        json.dump({
            'n_squares': len(squares),
            'gaps': gaps.tolist(),
            'gap_groups': {str(k): len(v) for k, v in gap_groups.items()},
            'unique_gaps': unique_gaps
        }, f, indent=2)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    analyze_trimodal_structure()
