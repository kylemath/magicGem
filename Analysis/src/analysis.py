"""
analysis.py
===========
Statistical analysis of Magic Gems and comparison with non-magic arrangements.

Key analyses:
1. Covariance structure of magic gem vectors
2. Distribution of properties across magic vs non-magic arrangements
3. Distance metrics between arrangements
4. Manifold structure exploration
5. Energy landscape analysis (covariance energy functional)
6. Exhaustive verification for small orders
7. Perturbation isolation analysis
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import ConvexHull
from itertools import permutations
import json

from .magic_squares import (
    generate_all_3x3_magic_squares,
    generate_random_arrangement,
    is_magic_square,
    count_arrangements,
    canonical_form,
    siamese_method,
    get_canonical_3x3,
    get_canonical_4x4
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


def compute_diagonal_covariances(square: np.ndarray, tol: float = 1e-10) -> Dict:
    """
    Compute covariances with diagonal indicator variables.
    
    Following the framework where diagonal conditions are expressed as:
    - Cov(D_main, Z) = 0 iff main diagonal sum equals M(n)
    - Cov(D_anti, Z) = 0 iff anti-diagonal sum equals M(n)
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
    tol : float
        Tolerance for zero comparison
        
    Returns
    -------
    Dict
        Diagonal covariance analysis results
    """
    n = square.shape[0]
    n_sq = n * n
    M_n = n * (n_sq + 1) // 2
    
    # Centered z-values
    z_center = (n_sq + 1) / 2
    z_vals = square.flatten() - z_center
    
    # Main diagonal indicator: D_main(i,j) = 1 if i==j
    D_main = np.zeros(n_sq)
    for i in range(n):
        D_main[i * n + i] = 1
    
    # Anti-diagonal indicator: D_anti(i,j) = 1 if i+j == n-1
    D_anti = np.zeros(n_sq)
    for i in range(n):
        j = n - 1 - i
        D_anti[i * n + j] = 1
    
    # Means
    D_main_mean = n / n_sq  # = 1/n
    D_anti_mean = n / n_sq
    z_mean = 0  # by construction
    
    # Covariances (using E[XY] - E[X]E[Y], but E[Z]=0)
    cov_main_z = np.mean(D_main * z_vals) - D_main_mean * z_mean
    cov_anti_z = np.mean(D_anti * z_vals) - D_anti_mean * z_mean
    
    # Actual diagonal sums
    main_diag_sum = np.trace(square)
    anti_diag_sum = np.trace(np.fliplr(square))
    
    return {
        'cov_main_z': cov_main_z,
        'cov_anti_z': cov_anti_z,
        'main_is_zero': abs(cov_main_z) < tol,
        'anti_is_zero': abs(cov_anti_z) < tol,
        'main_diag_sum': int(main_diag_sum),
        'anti_diag_sum': int(anti_diag_sum),
        'magic_constant': M_n,
        'main_equals_M': main_diag_sum == M_n,
        'anti_equals_M': anti_diag_sum == M_n
    }


def compute_total_magic_energy_v2(square: np.ndarray) -> Dict:
    """
    Compute the 4-term "low-mode" energy as sum of four squared covariances.
    
    E(S) = Cov(X,Z)² + Cov(Y,Z)² + Cov(D_main,Z)² + Cov(D_anti,Z)²
    
    WARNING: This 4-term energy does NOT characterize magic squares for n >= 4.
    It defines a broader "low-mode balanced" class. Use compute_full_magic_energy()
    for a true characterization. See the discussion in Section 2.5 of the paper.
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
        
    Returns
    -------
    Dict
        Energy breakdown with all four components
    """
    coords = square_to_coordinates(square, center_z=True)
    n = square.shape[0]
    
    # Row/column covariances
    x_vals = coords[:, 0]
    y_vals = coords[:, 1]
    z_vals = coords[:, 2]
    
    cov_xz = np.mean(x_vals * z_vals)  # E[XZ] since E[X]=E[Z]=0
    cov_yz = np.mean(y_vals * z_vals)
    
    # Diagonal covariances
    diag_cov = compute_diagonal_covariances(square)
    cov_main_z = diag_cov['cov_main_z']
    cov_anti_z = diag_cov['cov_anti_z']
    
    # Energy components
    E_cov = cov_xz**2 + cov_yz**2
    E_diag = cov_main_z**2 + cov_anti_z**2
    E_total = E_cov + E_diag
    
    return {
        'cov_xz': cov_xz,
        'cov_yz': cov_yz,
        'cov_main_z': cov_main_z,
        'cov_anti_z': cov_anti_z,
        'E_cov': E_cov,
        'E_diag': E_diag,
        'E_total': E_total,
        'is_zero_energy': E_total < 1e-20
    }


def compute_full_magic_energy(square: np.ndarray) -> Dict:
    """
    Compute the COMPLETE magic energy using individual row/column indicators.
    
    E_full(S) = Σ_{k=0}^{n-2} Cov(R_k,Z)² + Σ_{ℓ=0}^{n-2} Cov(C_ℓ,Z)² 
                + Cov(D_main,Z)² + Cov(D_anti,Z)²
    
    where R_k(i,j) = 1{i=k} and C_ℓ(i,j) = 1{j=ℓ} are row/column indicators.
    
    THEOREM: For all n >= 3, E_full(S) = 0 if and only if S is a magic square.
    
    This is the corrected characterization that works for all orders, unlike
    the 4-term "low-mode" energy which only characterizes magic squares for n=3.
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
        
    Returns
    -------
    Dict
        Complete energy breakdown with all 2n terms
    """
    n = square.shape[0]
    n_sq = n * n
    M_n = n * (n_sq + 1) // 2
    
    # Centered z-values (mean-zero)
    z_center = (n_sq + 1) / 2
    z_flat = square.flatten() - z_center
    
    # Row indicator covariances: R_k(i,j) = 1{i=k}
    # Cov(R_k, Z) = E[R_k * Z] - E[R_k] * E[Z] = E[R_k * Z] (since E[Z]=0)
    # E[R_k * Z] = (1/n²) * Σ_j z_{kj} = (1/n²) * (row_k_sum - n*z_center)
    row_cov = []
    for k in range(n - 1):  # Only need n-1 (last is redundant due to constraint)
        # R_k has mean 1/n
        R_k_mean = 1.0 / n
        # E[R_k * Z] = (1/n²) * sum of z values in row k
        row_k_z_sum = z_flat[k*n:(k+1)*n].sum()
        E_RkZ = row_k_z_sum / n_sq
        cov_Rk_Z = E_RkZ  # Since E[Z] = 0
        row_cov.append(cov_Rk_Z)
    
    # Column indicator covariances: C_ℓ(i,j) = 1{j=ℓ}
    col_cov = []
    for ell in range(n - 1):  # Only need n-1
        # E[C_ℓ * Z] = (1/n²) * sum of z values in column ℓ
        col_ell_z_sum = sum(z_flat[i*n + ell] for i in range(n))
        E_CellZ = col_ell_z_sum / n_sq
        cov_Cell_Z = E_CellZ  # Since E[Z] = 0
        col_cov.append(cov_Cell_Z)
    
    # Diagonal covariances (same as before)
    diag_cov = compute_diagonal_covariances(square)
    cov_main_z = diag_cov['cov_main_z']
    cov_anti_z = diag_cov['cov_anti_z']
    
    # Energy components
    E_row = sum(c**2 for c in row_cov)
    E_col = sum(c**2 for c in col_cov)
    E_diag = cov_main_z**2 + cov_anti_z**2
    E_full = E_row + E_col + E_diag
    
    # Also compute actual row/column sums for verification
    row_sums = [int(square[k, :].sum()) for k in range(n)]
    col_sums = [int(square[:, ell].sum()) for ell in range(n)]
    
    return {
        'row_covariances': row_cov,
        'col_covariances': col_cov,
        'cov_main_z': cov_main_z,
        'cov_anti_z': cov_anti_z,
        'E_row': E_row,
        'E_col': E_col,
        'E_diag': E_diag,
        'E_full': E_full,
        'is_zero_energy': E_full < 1e-20,
        'row_sums': row_sums,
        'col_sums': col_sums,
        'magic_constant': M_n,
        'n_terms': 2 * (n - 1) + 2  # = 2n terms total
    }


def compute_variance_formulas(n: int) -> Dict:
    """
    Compute theoretical and actual variance formulas for Magic Gem coordinates.
    
    THEOREM: For any n×n magic square:
        Var(Z) = (n⁴ - 1) / 12
        Var(X) = Var(Y) = (n² - 1) / 12
    
    These follow from the fact that z-values are a permutation of centered 
    integers {1-μ, ..., n²-μ} where μ = (n²+1)/2, and x,y are symmetric grids.
    
    Parameters
    ----------
    n : int
        Order of the magic square
        
    Returns
    -------
    Dict
        Theoretical and actual variance values
    """
    # Theoretical predictions
    var_z_theory = (n**4 - 1) / 12
    var_xy_theory = (n**2 - 1) / 12
    
    # Actual computation
    # Z values: 1..n² centered by μ = (n²+1)/2
    z_values = np.arange(1, n**2 + 1) - (n**2 + 1) / 2
    var_z_actual = np.var(z_values, ddof=0)
    
    # X values: column positions centered
    x_values = np.tile(np.arange(n) - (n-1)/2, n)
    var_x_actual = np.var(x_values, ddof=0)
    
    # Y values: row positions centered
    y_values = np.repeat((n-1)/2 - np.arange(n), n)
    var_y_actual = np.var(y_values, ddof=0)
    
    return {
        'n': n,
        'var_z_theory': var_z_theory,
        'var_z_actual': var_z_actual,
        'var_z_match': np.isclose(var_z_theory, var_z_actual),
        'var_xy_theory': var_xy_theory,
        'var_x_actual': var_x_actual,
        'var_y_actual': var_y_actual,
        'var_xy_match': np.isclose(var_xy_theory, var_x_actual) and np.isclose(var_xy_theory, var_y_actual)
    }


def compute_higher_moments(square: np.ndarray) -> Dict:
    """
    Compute higher-order cross-moments for a magic square.
    
    THEOREM: For any n×n magic square, E[X^k Z] = E[Y^k Z] = 0 for all k ≥ 1.
    
    Proof: Since X depends only on column j, we have
        E[X^k Z] = (1/n²) Σⱼ Xⱼᵏ · (column_j_sum - n·μ) = 0
    because all column sums equal M(n) = n·μ for magic squares.
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
        
    Returns
    -------
    Dict
        Higher-order moments and verification of vanishing
    """
    n = square.shape[0]
    mu = (n**2 + 1) / 2
    
    # Build coordinate arrays
    x_vals, y_vals, z_vals = [], [], []
    for i in range(n):
        for j in range(n):
            x_vals.append(j - (n-1)/2)
            y_vals.append((n-1)/2 - i)
            z_vals.append(square[i, j] - mu)
    
    x = np.array(x_vals)
    y = np.array(y_vals)
    z = np.array(z_vals)
    
    results = {
        'n': n,
        # First moments (k=1) - standard covariances
        'E_XZ': float(np.mean(x * z)),
        'E_YZ': float(np.mean(y * z)),
        # Second moments (k=2)
        'E_X2Z': float(np.mean(x**2 * z)),
        'E_Y2Z': float(np.mean(y**2 * z)),
        'E_XYZ': float(np.mean(x * y * z)),
        # Third moments (k=3)
        'E_X3Z': float(np.mean(x**3 * z)),
        'E_Y3Z': float(np.mean(y**3 * z)),
        # Mixed moments
        'E_XZ2': float(np.mean(x * z**2)),
        'E_YZ2': float(np.mean(y * z**2)),
    }
    
    # Verify vanishing (within numerical tolerance)
    tol = 1e-10
    results['all_XkZ_vanish'] = all(abs(results[k]) < tol for k in ['E_XZ', 'E_X2Z', 'E_X3Z'])
    results['all_YkZ_vanish'] = all(abs(results[k]) < tol for k in ['E_YZ', 'E_Y2Z', 'E_Y3Z'])
    
    return results


def count_local_minima(n: int, energy_type: str = 'full', verbose: bool = False) -> Dict:
    """
    Count local minima in the energy landscape for order n.
    
    A local minimum is an arrangement where no single swap decreases energy.
    Magic squares are global minima (E=0); this counts non-global local minima too.
    
    Parameters
    ----------
    n : int
        Order of the square (only n=3 is feasible for exhaustive enumeration)
    energy_type : str
        'full' for E_full (complete energy), 'low' for E_low (4-term energy)
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Counts of global and local minima
    """
    from itertools import combinations
    
    if n > 3:
        return {'error': 'Exhaustive enumeration only feasible for n=3'}
    
    def get_energy(arr):
        if energy_type == 'full':
            return compute_full_magic_energy(arr)['E_full']
        else:
            return compute_total_magic_energy_v2(arr)['E_total']
    
    def get_swaps(arr):
        flat = arr.flatten()
        neighbors = []
        for i, j in combinations(range(n*n), 2):
            new_flat = flat.copy()
            new_flat[i], new_flat[j] = new_flat[j], new_flat[i]
            neighbors.append(new_flat.reshape(n, n))
        return neighbors
    
    local_minima = []
    global_minima = []
    total = 0
    
    for perm in permutations(range(1, n*n + 1)):
        arr = np.array(perm).reshape(n, n)
        total += 1
        
        e = get_energy(arr)
        
        # Check if local minimum
        is_local_min = True
        for neighbor in get_swaps(arr):
            if get_energy(neighbor) < e - 1e-12:
                is_local_min = False
                break
        
        if is_local_min:
            local_minima.append((arr.copy(), e))
            if e < 1e-12:
                global_minima.append(arr.copy())
        
        if verbose and total % 100000 == 0:
            print(f'  Processed {total:,}...')
    
    energies = [e for _, e in local_minima]
    
    return {
        'n': n,
        'energy_type': energy_type,
        'total_arrangements': total,
        'total_local_minima': len(local_minima),
        'global_minima': len(global_minima),
        'non_global_local_minima': len(local_minima) - len(global_minima),
        'min_energy': float(min(energies)) if energies else None,
        'max_local_min_energy': float(max(energies)) if energies else None,
        'mean_local_min_energy': float(np.mean(energies)) if energies else None,
    }


def compute_position_weighted_vectors(square: np.ndarray) -> Dict:
    """
    Compute position-weighted vector sums that reveal zero-covariance geometrically.
    
    W_x = sum_ij x_ij * v_ij  (z-component = n² * Cov(X,Z))
    W_y = sum_ij y_ij * v_ij  (z-component = n² * Cov(Y,Z))
    
    For magic squares, W_x and W_y have zero z-components.
    
    Parameters
    ----------
    square : np.ndarray
        n×n arrangement
        
    Returns
    -------
    Dict
        Position-weighted vector sums and their properties
    """
    coords = square_to_coordinates(square, center_z=True)
    n = square.shape[0]
    n_sq = n * n
    
    x_vals = coords[:, 0]
    y_vals = coords[:, 1]
    
    # Weighted vector sums
    W_x = np.sum(x_vals[:, np.newaxis] * coords, axis=0)
    W_y = np.sum(y_vals[:, np.newaxis] * coords, axis=0)
    
    # The z-components relate to covariance
    W_x_z = W_x[2]  # = n² * Cov(X,Z)
    W_y_z = W_y[2]  # = n² * Cov(Y,Z)
    
    return {
        'W_x': W_x.tolist(),
        'W_y': W_y.tolist(),
        'W_x_z_component': W_x_z,
        'W_y_z_component': W_y_z,
        'Cov_XZ_from_W': W_x_z / n_sq,
        'Cov_YZ_from_W': W_y_z / n_sq,
        'x_balanced': abs(W_x_z) < 1e-10,
        'y_balanced': abs(W_y_z) < 1e-10
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


# =============================================================================
# ENERGY LANDSCAPE ANALYSIS
# =============================================================================

def compute_covariance_energy(arr: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute the covariance energy E(S) = Cov(X,Z)² + Cov(Y,Z)².
    
    This is the key energy functional whose zeros characterize semi-magic squares.
    Magic squares are the arrangements where this "imbalance energy" vanishes.
    
    Parameters
    ----------
    arr : np.ndarray
        n×n arrangement of integers
        
    Returns
    -------
    Tuple[float, float, float]
        (energy, cov_xz, cov_yz)
    """
    coords = square_to_coordinates(arr, center_z=True)
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    
    # Covariances (means are all zero by construction)
    cov_xz = np.mean(x * z)
    cov_yz = np.mean(y * z)
    
    return cov_xz**2 + cov_yz**2, cov_xz, cov_yz


def compute_diagonal_energy(arr: np.ndarray) -> float:
    """
    Compute the diagonal energy measuring deviation of diagonal means from overall mean.
    
    E_diag = (mean_main_diag - overall_mean)² + (mean_anti_diag - overall_mean)²
    
    Parameters
    ----------
    arr : np.ndarray
        n×n arrangement
        
    Returns
    -------
    float
        Diagonal energy value
    """
    n = arr.shape[0]
    overall_mean = (n**2 + 1) / 2
    
    main_diag_mean = np.mean([arr[i, i] for i in range(n)])
    anti_diag_mean = np.mean([arr[i, n-1-i] for i in range(n)])
    
    e_main = (main_diag_mean - overall_mean)**2
    e_anti = (anti_diag_mean - overall_mean)**2
    
    return e_main + e_anti


def compute_total_magic_energy(arr: np.ndarray) -> float:
    """
    Total energy functional: E_total = E_cov + E_diag.
    
    Magic squares are exactly the zeros of this functional among permutations.
    This provides an energy landscape interpretation where magic squares
    correspond to ground states---configurations of perfect equilibrium.
    
    Parameters
    ----------
    arr : np.ndarray
        n×n arrangement
        
    Returns
    -------
    float
        Total magic energy
    """
    e_cov, _, _ = compute_covariance_energy(arr)
    e_diag = compute_diagonal_energy(arr)
    return e_cov + e_diag


def single_swap_perturbations(arr: np.ndarray):
    """
    Generate all single-swap perturbations of an arrangement.
    
    A single swap exchanges two elements at positions (i1,j1) and (i2,j2).
    
    Parameters
    ----------
    arr : np.ndarray
        n×n arrangement
        
    Yields
    ------
    Tuple[np.ndarray, Tuple]
        (perturbed_arr, ((i1,j1), (i2,j2))) for each swap
    """
    n = arr.shape[0]
    positions = [(i, j) for i in range(n) for j in range(n)]
    
    for idx1 in range(len(positions)):
        for idx2 in range(idx1 + 1, len(positions)):
            pos1, pos2 = positions[idx1], positions[idx2]
            perturbed = arr.copy()
            perturbed[pos1], perturbed[pos2] = perturbed[pos2], perturbed[pos1]
            yield perturbed, (pos1, pos2)


def analyze_exhaustive_n3(verbose: bool = False) -> Dict:
    """
    Exhaustive analysis for n=3: verify zero-covariance characterization.
    
    Tests ALL 9! = 362,880 permutations to verify that magic squares
    are exactly the configurations with zero total energy.
    
    Parameters
    ----------
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Exhaustive verification results including energy distribution
    """
    if verbose:
        print("Running exhaustive analysis for n=3 (362,880 permutations)...")
    
    n = 3
    
    results = {
        'total_permutations': 0,
        'zero_energy_count': 0,
        'magic_squares_count': 0,
        'false_positives': 0,
        'false_negatives': 0,
        'energy_values': [],
        'magic_energy_values': [],
        'theorem_verified': False
    }
    
    # Iterate over all permutations of 1..9
    for perm in permutations(range(1, n*n + 1)):
        arr = np.array(perm).reshape(n, n)
        results['total_permutations'] += 1
        
        e_total = compute_total_magic_energy(arr)
        results['energy_values'].append(e_total)
        
        is_magic = is_magic_square(arr)
        is_zero_energy = e_total < 1e-12
        
        if is_zero_energy:
            results['zero_energy_count'] += 1
        
        if is_magic:
            results['magic_squares_count'] += 1
            results['magic_energy_values'].append(e_total)
            if not is_zero_energy:
                results['false_negatives'] += 1
        
        if is_zero_energy and not is_magic:
            results['false_positives'] += 1
    
    # Verify theorem
    results['theorem_verified'] = (
        results['magic_squares_count'] == results['zero_energy_count'] and
        results['false_positives'] == 0 and
        results['false_negatives'] == 0
    )
    
    # Compute energy distribution statistics
    energies = np.array(results['energy_values'])
    results['energy_min'] = float(np.min(energies))
    results['energy_max'] = float(np.max(energies))
    results['energy_mean'] = float(np.mean(energies))
    results['energy_std'] = float(np.std(energies))
    results['energy_median'] = float(np.median(energies))
    
    if verbose:
        print(f"  Total permutations: {results['total_permutations']:,}")
        print(f"  Magic squares found: {results['magic_squares_count']}")
        print(f"  Zero-energy configurations: {results['zero_energy_count']}")
        print(f"  Theorem verified: {results['theorem_verified']}")
    
    return results


def analyze_perturbation_isolation(magic_squares: List[np.ndarray], verbose: bool = False) -> Dict:
    """
    Perturbation analysis: verify that magic squares are isolated energy minima.
    
    For each magic square, compute energy after every possible single swap
    and verify that all swaps increase energy. This establishes magic squares
    as strict local minima in the energy landscape.
    
    Parameters
    ----------
    magic_squares : List[np.ndarray]
        List of magic squares to analyze
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Perturbation analysis results including energy gaps
    """
    if verbose:
        print(f"Analyzing perturbation isolation for {len(magic_squares)} magic squares...")
    
    results = {
        'n_squares_tested': 0,
        'all_isolated': True,
        'min_energy_gaps': [],
        'mean_energy_gaps': [],
        'non_isolated_count': 0
    }
    
    for sq in magic_squares:
        results['n_squares_tested'] += 1
        base_energy = compute_total_magic_energy(sq)
        
        gaps = []
        is_isolated = True
        
        for perturbed, _ in single_swap_perturbations(sq):
            pert_energy = compute_total_magic_energy(perturbed)
            gap = pert_energy - base_energy
            gaps.append(gap)
            
            if gap <= 1e-12:
                is_isolated = False
        
        min_gap = min(gaps)
        mean_gap = np.mean(gaps)
        
        results['min_energy_gaps'].append(min_gap)
        results['mean_energy_gaps'].append(mean_gap)
        
        if not is_isolated:
            results['all_isolated'] = False
            results['non_isolated_count'] += 1
    
    # Summary statistics
    results['overall_min_gap'] = float(min(results['min_energy_gaps']))
    results['overall_mean_min_gap'] = float(np.mean(results['min_energy_gaps']))
    results['overall_std_min_gap'] = float(np.std(results['min_energy_gaps']))
    
    if verbose:
        print(f"  All isolated: {results['all_isolated']}")
        print(f"  Minimum energy gap: {results['overall_min_gap']:.6f}")
    
    return results


def analyze_scaling(verbose: bool = False) -> Dict:
    """
    Scaling analysis: compare properties across n = 3, 4, 5.
    
    Examines how geometric and energy properties scale with magic square order,
    providing insight into the structure of the energy landscape at different scales.
    
    Parameters
    ----------
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Scaling analysis results for each order
    """
    if verbose:
        print("Running scaling analysis for n = 3, 4, 5...")
    
    results = {}
    
    squares_by_n = {
        3: get_canonical_3x3(),
        4: get_canonical_4x4(),
        5: siamese_method(5)
    }
    
    for n, magic_square in squares_by_n.items():
        coords = square_to_coordinates(magic_square, center_z=True)
        e_cov, cov_xz, cov_yz = compute_covariance_energy(magic_square)
        e_diag = compute_diagonal_energy(magic_square)
        
        try:
            hull = ConvexHull(coords)
            hull_volume = hull.volume
            hull_area = hull.area
            n_vertices = len(hull.vertices)
        except Exception:
            hull_volume = hull_area = n_vertices = 0
        
        # Compute perturbation gap
        min_gap = float('inf')
        gap_count = 0
        for perturbed, _ in single_swap_perturbations(magic_square):
            gap = compute_total_magic_energy(perturbed)
            if gap < min_gap:
                min_gap = gap
            gap_count += 1
        
        results[n] = {
            'n': n,
            'n_points': n**2,
            'magic_constant': n * (n**2 + 1) // 2,
            'cov_energy': float(e_cov),
            'diag_energy': float(e_diag),
            'total_energy': float(e_cov + e_diag),
            'cov_xz': float(cov_xz),
            'cov_yz': float(cov_yz),
            'hull_volume': float(hull_volume),
            'hull_area': float(hull_area),
            'n_hull_vertices': int(n_vertices),
            'n_interior_points': n**2 - int(n_vertices),
            'vertex_fraction': float(n_vertices / n**2),
            'min_perturbation_gap': float(min_gap),
            'num_possible_swaps': gap_count
        }
        
        if verbose:
            print(f"  n={n}: energy={e_cov + e_diag:.2e}, gap={min_gap:.4f}, hull_verts={n_vertices}")
    
    return results


# =============================================================================
# LARGE-SCALE ENERGY LANDSCAPE ANALYSIS
# =============================================================================

def compute_covariance_energy_vectorized(arrangements: np.ndarray) -> np.ndarray:
    """
    Vectorized computation of covariance energy for multiple arrangements.
    
    Optimized for batch processing on modern multi-core hardware.
    
    Parameters
    ----------
    arrangements : np.ndarray
        Array of shape (n_samples, n, n) containing arrangements
        
    Returns
    -------
    np.ndarray
        Array of shape (n_samples,) containing energies
    """
    n_samples, n, _ = arrangements.shape
    
    # Create coordinate grids
    j_coords = np.arange(n) - (n-1)/2  # column coords
    i_coords = (n-1)/2 - np.arange(n)  # row coords
    
    # Value coords (centered)
    z = arrangements - (n**2 + 1)/2
    
    # Compute covariances for all samples at once
    x_grid = np.tile(j_coords, (n, 1))  # (n, n)
    y_grid = np.tile(i_coords, (n, 1)).T  # (n, n)
    
    # Flatten for each sample
    x_flat = x_grid.ravel()  # (n²,)
    y_flat = y_grid.ravel()  # (n²,)
    z_flat = z.reshape(n_samples, -1)  # (n_samples, n²)
    
    # Covariances (means are zero by construction)
    cov_xz = np.mean(x_flat * z_flat, axis=1)  # (n_samples,)
    cov_yz = np.mean(y_flat * z_flat, axis=1)  # (n_samples,)
    
    return cov_xz**2 + cov_yz**2


def compute_total_energy_vectorized(arrangements: np.ndarray) -> np.ndarray:
    """
    Compute total energy (covariance + diagonal) for multiple arrangements.
    
    Parameters
    ----------
    arrangements : np.ndarray
        Array of shape (n_samples, n, n)
        
    Returns
    -------
    np.ndarray
        Array of shape (n_samples,) containing total energies
    """
    n_samples, n, _ = arrangements.shape
    
    # Covariance energy
    e_cov = compute_covariance_energy_vectorized(arrangements)
    
    # Diagonal energy
    overall_mean = (n**2 + 1) / 2
    
    # Extract diagonals vectorized
    main_diags = np.array([arr[np.arange(n), np.arange(n)] for arr in arrangements])
    anti_diags = np.array([arr[np.arange(n), np.arange(n-1, -1, -1)] for arr in arrangements])
    
    main_means = np.mean(main_diags, axis=1)
    anti_means = np.mean(anti_diags, axis=1)
    
    e_diag = (main_means - overall_mean)**2 + (anti_means - overall_mean)**2
    
    return e_cov + e_diag


def generate_random_arrangements_batch(n: int, batch_size: int) -> np.ndarray:
    """
    Generate a batch of random arrangements using vectorized shuffle.
    
    Parameters
    ----------
    n : int
        Order of the square
    batch_size : int
        Number of arrangements to generate
        
    Returns
    -------
    np.ndarray
        Array of shape (batch_size, n, n)
    """
    base = np.arange(1, n**2 + 1)
    arrangements = np.array([np.random.permutation(base).reshape(n, n) 
                            for _ in range(batch_size)])
    return arrangements


def compute_landscape_statistics(energies: np.ndarray, n_bins: int = 200) -> Dict:
    """
    Compute detailed statistics of the energy landscape.
    
    Parameters
    ----------
    energies : np.ndarray
        Array of energy values
    n_bins : int
        Number of histogram bins
        
    Returns
    -------
    Dict
        Dictionary containing landscape statistics
    """
    hist, bin_edges = np.histogram(energies, bins=n_bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Peak energy (mode)
    peak_idx = np.argmax(hist)
    peak_energy = bin_centers[peak_idx]
    
    # Entropy of distribution (measure of landscape ruggedness)
    probs = hist / hist.sum()
    probs = probs[probs > 0]  # Remove zeros
    entropy = -np.sum(probs * np.log(probs))
    
    return {
        'min': float(energies.min()),
        'max': float(energies.max()),
        'mean': float(energies.mean()),
        'std': float(energies.std()),
        'median': float(np.median(energies)),
        'q25': float(np.percentile(energies, 25)),
        'q75': float(np.percentile(energies, 75)),
        'peak_energy': float(peak_energy),
        'entropy': float(entropy),
        'zero_fraction': float((energies < 1e-10).sum() / len(energies))
    }


def sample_energy_landscape(n: int, n_samples: int, batch_size: int = 10000, 
                           seed: int = 42, verbose: bool = False) -> Dict:
    """
    Sample the energy landscape for order n.
    
    For large-scale analysis of how energy distributions evolve with order.
    
    Parameters
    ----------
    n : int
        Order of the magic square
    n_samples : int
        Number of samples to generate
    batch_size : int
        Batch size for memory efficiency
    seed : int
        Random seed for reproducibility
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Dictionary containing sampled energies and statistics
    """
    import time
    
    np.random.seed(seed)
    
    if verbose:
        print(f"Sampling n={n} energy landscape ({n_samples:,} samples)...")
    
    start_time = time.time()
    
    n_batches = (n_samples + batch_size - 1) // batch_size
    
    all_energies = []
    magic_count = 0
    
    for batch_idx in range(n_batches):
        current_batch_size = min(batch_size, n_samples - batch_idx * batch_size)
        arrangements = generate_random_arrangements_batch(n, current_batch_size)
        
        # Compute energies
        batch_energies = compute_total_energy_vectorized(arrangements)
        all_energies.extend(batch_energies)
        
        # Check for magic squares (very rare, but check near-zero energy)
        near_zero = batch_energies < 1e-10
        if np.any(near_zero):
            for arr in arrangements[near_zero]:
                if is_magic_square(arr):
                    magic_count += 1
        
        if verbose and (batch_idx + 1) % 100 == 0:
            pct = 100 * (batch_idx + 1) / n_batches
            print(f"  Progress: {pct:.1f}%")
    
    elapsed = time.time() - start_time
    energies = np.array(all_energies)
    
    if verbose:
        print(f"  Completed in {elapsed:.1f}s ({n_samples/elapsed:,.0f} samples/sec)")
        print(f"  Magic squares found: {magic_count}")
    
    # Compute statistics
    stats = compute_landscape_statistics(energies)
    
    return {
        'n': n,
        'n_samples': len(energies),
        'energies': energies.tolist(),  # Convert for JSON serialization
        'magic_count': magic_count,
        'elapsed_time': elapsed,
        'samples_per_sec': n_samples / elapsed,
        'stats': stats
    }


def analyze_large_scale_landscape(n3_exhaustive: bool = True,
                                  n4_samples: int = 100000,
                                  n5_samples: int = 100000,
                                  verbose: bool = True) -> Dict:
    """
    Comprehensive large-scale energy landscape analysis across orders.
    
    This function performs the analysis described in Section 5.5 of the paper,
    sampling millions of arrangements to characterize the energy landscape.
    
    Parameters
    ----------
    n3_exhaustive : bool
        Whether to use exhaustive enumeration for n=3
    n4_samples : int
        Number of samples for n=4
    n5_samples : int
        Number of samples for n=5
    verbose : bool
        Whether to print progress
        
    Returns
    -------
    Dict
        Dictionary containing results for all orders
    """
    results = {}
    
    # n=3: exhaustive or sampled
    if n3_exhaustive:
        if verbose:
            print("\n[1/3] n=3: Exhaustive enumeration...")
        r3 = analyze_exhaustive_n3(verbose=verbose)
        results[3] = {
            'n': 3,
            'n_samples': len(r3['energy_values']),
            'energies': r3['energy_values'],
            'magic_count': r3['magic_squares_count'],
            'exhaustive': True,
            'stats': compute_landscape_statistics(np.array(r3['energy_values']))
        }
    else:
        results[3] = sample_energy_landscape(3, n4_samples, verbose=verbose)
    
    # n=4: sampling
    if verbose:
        print(f"\n[2/3] n=4: Sampling {n4_samples:,} arrangements...")
    results[4] = sample_energy_landscape(4, n4_samples, verbose=verbose)
    
    # n=5: sampling
    if verbose:
        print(f"\n[3/3] n=5: Sampling {n5_samples:,} arrangements...")
    results[5] = sample_energy_landscape(5, n5_samples, verbose=verbose)
    
    # Compare landscapes
    if verbose:
        print("\n" + "="*60)
        print("ENERGY LANDSCAPE COMPARISON")
        print("="*60)
        
        for n in [3, 4, 5]:
            stats = results[n]['stats']
            print(f"\nn={n}:")
            print(f"  Samples: {results[n]['n_samples']:,}")
            print(f"  Mean energy: {stats['mean']:.4f} ± {stats['std']:.4f}")
            print(f"  Peak energy (mode): {stats['peak_energy']:.4f}")
            print(f"  Landscape entropy: {stats['entropy']:.4f}")
            print(f"  Zero-energy fraction: {stats['zero_fraction']:.2e}")
    
    return results


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

