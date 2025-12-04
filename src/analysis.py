"""
analysis.py
===========
Statistical analysis of Magic Gems and comparison with non-magic arrangements.

Key analyses:
1. Covariance structure of magic gem vectors
2. Distribution of properties across magic vs non-magic arrangements
3. Distance metrics between arrangements
4. Manifold structure exploration
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import stats
from scipy.spatial.distance import pdist, squareform
import json

from .magic_squares import (
    generate_all_3x3_magic_squares,
    generate_random_arrangement,
    is_magic_square,
    count_arrangements,
    canonical_form,
    siamese_method
)
from .magic_gems import (
    square_to_coordinates,
    compute_convex_hull,
    compute_moment_of_inertia,
    compute_principal_moments,
    square_to_magic_gem
)


def compute_covariance_matrix(coords: np.ndarray) -> np.ndarray:
    """
    Compute the covariance matrix of the coordinate vectors.
    
    For a magic square, we hypothesize this has special structure.
    
    Parameters
    ----------
    coords : np.ndarray
        n² × 3 array of coordinates
        
    Returns
    -------
    np.ndarray
        3×3 covariance matrix
    """
    return np.cov(coords.T)


def test_zero_covariance(coords: np.ndarray, tol: float = 1e-10) -> Dict:
    """
    Test if off-diagonal covariances are zero (balance property).
    
    Parameters
    ----------
    coords : np.ndarray
        Coordinate array
    tol : float
        Tolerance for zero comparison
        
    Returns
    -------
    Dict
        Test results including covariance matrix and boolean flags
    """
    cov = compute_covariance_matrix(coords)
    
    # Extract off-diagonal elements
    cov_xy = cov[0, 1]
    cov_xz = cov[0, 2]
    cov_yz = cov[1, 2]
    
    return {
        'covariance_matrix': cov.tolist(),
        'cov_xy': cov_xy,
        'cov_xz': cov_xz,
        'cov_yz': cov_yz,
        'xy_is_zero': abs(cov_xy) < tol,
        'xz_is_zero': abs(cov_xz) < tol,
        'yz_is_zero': abs(cov_yz) < tol,
        'all_offdiag_zero': all(abs(c) < tol for c in [cov_xy, cov_xz, cov_yz])
    }


def analyze_magic_vs_random(n: int, num_random: int = 10000, seed: int = 42) -> Dict:
    """
    Compare properties of magic squares vs random arrangements.
    
    Parameters
    ----------
    n : int
        Order of square (3, 4, or 5)
    num_random : int
        Number of random arrangements to generate
    seed : int
        Random seed for reproducibility
        
    Returns
    -------
    Dict
        Comparison statistics
    """
    np.random.seed(seed)
    
    # Get magic squares
    if n == 3:
        magic_squares = generate_all_3x3_magic_squares()
    elif n == 5:
        magic_squares = [siamese_method(5)]
    else:
        magic_squares = []
    
    # Analyze magic squares
    magic_data = {
        'hull_volumes': [],
        'hull_areas': [],
        'principal_moments': [],
        'covariances': [],
        'cov_xz': [],
        'cov_yz': []
    }
    
    for sq in magic_squares:
        gem = square_to_magic_gem(sq)
        if 'hull' in gem:
            magic_data['hull_volumes'].append(gem['hull']['volume'])
            magic_data['hull_areas'].append(gem['hull']['area'])
        magic_data['principal_moments'].append(gem['principal_moments'])
        
        coords = np.array(gem['coordinates'])
        cov_result = test_zero_covariance(coords)
        magic_data['covariances'].append(cov_result['covariance_matrix'])
        magic_data['cov_xz'].append(cov_result['cov_xz'])
        magic_data['cov_yz'].append(cov_result['cov_yz'])
    
    # Analyze random arrangements
    random_data = {
        'hull_volumes': [],
        'hull_areas': [],
        'principal_moments': [],
        'cov_xz': [],
        'cov_yz': [],
        'is_magic': []
    }
    
    magic_count = 0
    for _ in range(num_random):
        sq = generate_random_arrangement(n)
        is_magic = is_magic_square(sq)
        random_data['is_magic'].append(is_magic)
        if is_magic:
            magic_count += 1
        
        gem = square_to_magic_gem(sq)
        if 'hull' in gem:
            random_data['hull_volumes'].append(gem['hull']['volume'])
            random_data['hull_areas'].append(gem['hull']['area'])
        random_data['principal_moments'].append(gem['principal_moments'])
        
        coords = np.array(gem['coordinates'])
        cov_result = test_zero_covariance(coords)
        random_data['cov_xz'].append(cov_result['cov_xz'])
        random_data['cov_yz'].append(cov_result['cov_yz'])
    
    # Compute statistics
    results = {
        'n': n,
        'num_magic_squares': len(magic_squares),
        'num_random_samples': num_random,
        'magic_found_in_random': magic_count,
        'estimated_probability': magic_count / num_random if num_random > 0 else 0,
        'total_arrangements': count_arrangements(n),
        'magic': {
            'mean_hull_volume': np.mean(magic_data['hull_volumes']) if magic_data['hull_volumes'] else None,
            'mean_hull_area': np.mean(magic_data['hull_areas']) if magic_data['hull_areas'] else None,
            'mean_cov_xz': np.mean(magic_data['cov_xz']),
            'mean_cov_yz': np.mean(magic_data['cov_yz']),
        },
        'random': {
            'mean_hull_volume': np.mean(random_data['hull_volumes']) if random_data['hull_volumes'] else None,
            'std_hull_volume': np.std(random_data['hull_volumes']) if random_data['hull_volumes'] else None,
            'mean_hull_area': np.mean(random_data['hull_areas']) if random_data['hull_areas'] else None,
            'std_hull_area': np.std(random_data['hull_areas']) if random_data['hull_areas'] else None,
            'mean_cov_xz': np.mean(random_data['cov_xz']),
            'std_cov_xz': np.std(random_data['cov_xz']),
            'mean_cov_yz': np.mean(random_data['cov_yz']),
            'std_cov_yz': np.std(random_data['cov_yz']),
        }
    }
    
    return results


def arrangement_distance(sq1: np.ndarray, sq2: np.ndarray, metric: str = 'frobenius') -> float:
    """
    Compute distance between two arrangements.
    
    Parameters
    ----------
    sq1, sq2 : np.ndarray
        Two n×n arrangements
    metric : str
        'frobenius' - Frobenius norm of difference
        'hamming' - Number of differing positions
        'geometric' - Distance in Magic Gem space
        
    Returns
    -------
    float
        Distance value
    """
    if metric == 'frobenius':
        return np.linalg.norm(sq1 - sq2, 'fro')
    elif metric == 'hamming':
        return np.sum(sq1 != sq2)
    elif metric == 'geometric':
        coords1 = square_to_coordinates(sq1)
        coords2 = square_to_coordinates(sq2)
        # Use Hausdorff-like distance
        d1 = np.mean([np.min(np.linalg.norm(coords2 - c, axis=1)) for c in coords1])
        d2 = np.mean([np.min(np.linalg.norm(coords1 - c, axis=1)) for c in coords2])
        return max(d1, d2)
    else:
        raise ValueError(f"Unknown metric: {metric}")


def gem_signature(square: np.ndarray) -> np.ndarray:
    """
    Compute a rotation/reflection invariant signature for a Magic Gem.
    
    Uses sorted eigenvalues of inertia tensor and sorted edge lengths.
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
        
    Returns
    -------
    np.ndarray
        Signature vector
    """
    coords = square_to_coordinates(square)
    inertia = compute_moment_of_inertia(coords)
    eigenvalues, _ = compute_principal_moments(inertia)
    
    # Also include sorted z-values (rotation invariant in x-y plane)
    z_sorted = np.sort(coords[:, 2])
    
    return np.concatenate([eigenvalues, z_sorted])


def gem_distance(sq1: np.ndarray, sq2: np.ndarray) -> float:
    """
    Compute distance between two arrangements using gem signatures.
    
    This distance is invariant to D4 symmetry operations.
    
    Parameters
    ----------
    sq1, sq2 : np.ndarray
        Two n×n arrangements
        
    Returns
    -------
    float
        Distance between gem signatures
    """
    sig1 = gem_signature(sq1)
    sig2 = gem_signature(sq2)
    return np.linalg.norm(sig1 - sig2)


def analyze_manifold_structure(n: int, num_samples: int = 1000, seed: int = 42) -> Dict:
    """
    Explore the manifold structure of magic vs non-magic arrangements.
    
    Parameters
    ----------
    n : int
        Order of square
    num_samples : int
        Number of random samples
    seed : int
        Random seed
        
    Returns
    -------
    Dict
        Manifold analysis results
    """
    np.random.seed(seed)
    
    # Generate samples
    samples = []
    is_magic = []
    signatures = []
    
    for _ in range(num_samples):
        sq = generate_random_arrangement(n)
        samples.append(sq)
        is_magic.append(is_magic_square(sq))
        signatures.append(gem_signature(sq))
    
    # Add all magic squares
    if n == 3:
        for sq in generate_all_3x3_magic_squares():
            samples.append(sq)
            is_magic.append(True)
            signatures.append(gem_signature(sq))
    
    signatures = np.array(signatures)
    is_magic = np.array(is_magic)
    
    # Compute pairwise distances
    distances = squareform(pdist(signatures))
    
    # Analyze clustering
    magic_indices = np.where(is_magic)[0]
    nonmagic_indices = np.where(~is_magic)[0]
    
    if len(magic_indices) > 1 and len(nonmagic_indices) > 0:
        # Within-magic distances
        within_magic = distances[np.ix_(magic_indices, magic_indices)]
        within_magic_flat = within_magic[np.triu_indices(len(magic_indices), k=1)]
        
        # Between magic and non-magic
        between = distances[np.ix_(magic_indices, nonmagic_indices)].flatten()
        
        results = {
            'num_samples': len(samples),
            'num_magic': int(is_magic.sum()),
            'mean_within_magic_distance': float(np.mean(within_magic_flat)) if len(within_magic_flat) > 0 else None,
            'std_within_magic_distance': float(np.std(within_magic_flat)) if len(within_magic_flat) > 0 else None,
            'mean_magic_to_nonmagic_distance': float(np.mean(between)),
            'std_magic_to_nonmagic_distance': float(np.std(between)),
        }
    else:
        results = {
            'num_samples': len(samples),
            'num_magic': int(is_magic.sum()),
            'note': 'Insufficient magic squares found for clustering analysis'
        }
    
    return results


def perturbation_analysis(square: np.ndarray, epsilon: float = 0.1, num_trials: int = 100) -> Dict:
    """
    Analyze how covariance changes with small perturbations.
    
    This tests the hypothesis that magic squares are at covariance minima.
    
    Parameters
    ----------
    square : np.ndarray
        A magic square
    epsilon : float
        Perturbation magnitude
    num_trials : int
        Number of perturbation trials
        
    Returns
    -------
    Dict
        Perturbation analysis results
    """
    coords_original = square_to_coordinates(square)
    cov_original = test_zero_covariance(coords_original)
    
    original_offdiag_norm = np.sqrt(
        cov_original['cov_xz']**2 + cov_original['cov_yz']**2
    )
    
    perturbed_norms = []
    
    for _ in range(num_trials):
        # Perturb z-coordinates
        coords_perturbed = coords_original.copy()
        coords_perturbed[:, 2] += np.random.uniform(-epsilon, epsilon, size=len(coords_original))
        
        cov_perturbed = test_zero_covariance(coords_perturbed)
        perturbed_norm = np.sqrt(
            cov_perturbed['cov_xz']**2 + cov_perturbed['cov_yz']**2
        )
        perturbed_norms.append(perturbed_norm)
    
    return {
        'original_offdiag_norm': original_offdiag_norm,
        'mean_perturbed_norm': np.mean(perturbed_norms),
        'std_perturbed_norm': np.std(perturbed_norms),
        'min_perturbed_norm': np.min(perturbed_norms),
        'max_perturbed_norm': np.max(perturbed_norms),
        'proportion_larger': np.mean(np.array(perturbed_norms) > original_offdiag_norm),
        'epsilon': epsilon,
        'num_trials': num_trials
    }


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        return super().default(obj)


def save_analysis(results: Dict, filepath: str):
    """Save analysis results to JSON."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)


def load_analysis(filepath: str) -> Dict:
    """Load analysis results from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    from magic_squares import get_canonical_3x3
    
    # Test covariance analysis
    lo_shu = get_canonical_3x3()
    coords = square_to_coordinates(lo_shu)
    
    print("Lo Shu Covariance Analysis:")
    cov_result = test_zero_covariance(coords)
    print(f"  Cov(X,Z): {cov_result['cov_xz']:.6f}")
    print(f"  Cov(Y,Z): {cov_result['cov_yz']:.6f}")
    print(f"  All off-diagonal zero: {cov_result['all_offdiag_zero']}")
    
    # Perturbation test
    print("\nPerturbation Analysis:")
    pert = perturbation_analysis(lo_shu)
    print(f"  Original off-diag norm: {pert['original_offdiag_norm']:.6f}")
    print(f"  Mean perturbed norm: {pert['mean_perturbed_norm']:.6f}")
    print(f"  Proportion larger: {pert['proportion_larger']:.2%}")
    
    # Magic vs random comparison
    print("\nMagic vs Random Analysis (n=3):")
    comparison = analyze_magic_vs_random(3, num_random=1000)
    print(f"  Magic mean Cov(X,Z): {comparison['magic']['mean_cov_xz']:.6f}")
    print(f"  Random mean Cov(X,Z): {comparison['random']['mean_cov_xz']:.6f}")
    print(f"  Random std Cov(X,Z): {comparison['random']['std_cov_xz']:.6f}")

