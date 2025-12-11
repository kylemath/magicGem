"""
New Theorems and Conjectures Exploration
=========================================

Based on the deep exploration results, this script investigates
specific potential new theorems and deeper mathematical connections.

KEY FINDINGS FROM INITIAL EXPLORATION:
1. Magic constant M is always the largest eigenvalue (verified for n=3,4,5)
2. Covariance matrix has degenerate eigenvalues (two equal smaller eigenvalues)
3. Magic squares remain "magic" under modular arithmetic mod 2,3,5
4. Hull volume scaling appears to approach V ~ n⁴/2 as n increases
5. The rigidity analysis shows Magic Gems are NOT infinitesimally rigid
6. Perturbation gap Δ scales differently than expected - needs more investigation

This script explores:
- Detailed spectral structure theorems
- Cohomological connections
- Higher-order moment invariants
- Connection to representation theory
- Potential for new enumeration formulas
"""

import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy import linalg
from itertools import permutations, combinations
from collections import Counter, defaultdict
import json
import math
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# MAGIC SQUARE UTILITIES
# ============================================================================

def lo_shu():
    return np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])

def siamese_method(n: int) -> np.ndarray:
    if n % 2 == 0:
        raise ValueError("Siamese method only works for odd n")
    square = np.zeros((n, n), dtype=int)
    i, j = 0, n // 2
    for num in range(1, n*n + 1):
        square[i, j] = num
        i_new, j_new = (i - 1) % n, (j + 1) % n
        if square[i_new, j_new] != 0:
            i_new, j_new = (i + 1) % n, j
        i, j = i_new, j_new
    return square

def doubly_even_method(n: int) -> np.ndarray:
    if n % 4 != 0:
        raise ValueError("Doubly-even method requires n divisible by 4")
    square = np.arange(1, n*n + 1).reshape(n, n)
    for i in range(n):
        for j in range(n):
            if ((i % 4 == j % 4) or ((i % 4) + (j % 4) == 3)):
                square[i, j] = n*n + 1 - square[i, j]
    return square

def generate_all_3x3_magic_squares() -> List[np.ndarray]:
    base = lo_shu()
    squares = []
    current = base.copy()
    for _ in range(4):
        squares.append(current.copy())
        squares.append(np.fliplr(current).copy())
        current = np.rot90(current)
    return squares

def square_to_coordinates(square: np.ndarray) -> np.ndarray:
    n = square.shape[0]
    offset = (n - 1) / 2
    z_center = (n**2 + 1) / 2
    coords = []
    for i in range(n):
        for j in range(n):
            x, y, z = j - offset, offset - i, square[i, j] - z_center
            coords.append([x, y, z])
    return np.array(coords)

# ============================================================================
# THEOREM 1: SPECTRAL DECOMPOSITION THEOREM
# ============================================================================

def analyze_spectral_decomposition(square: np.ndarray) -> Dict:
    """
    CONJECTURE: The eigenvalue spectrum of an n×n magic square has the form:
    - λ₁ = M(n) (the magic constant)
    - Remaining eigenvalues come in ± pairs (or are zero)
    
    This suggests a deep connection to the representation theory of the
    symmetry group acting on magic squares.
    """
    n = square.shape[0]
    M = n * (n*n + 1) // 2
    
    eigenvalues = np.linalg.eigvals(square)
    eigenvalues_real = np.sort(np.real(eigenvalues))[::-1]
    
    # Check if M is the largest eigenvalue
    max_eig = eigenvalues_real[0]
    m_is_max = abs(max_eig - M) < 0.01
    
    # Check for ± pair structure
    nonzero_eigs = eigenvalues[np.abs(eigenvalues) > 0.01]
    pairs = []
    unpaired = []
    
    for eig in nonzero_eigs:
        if abs(eig - M) < 0.01:  # Skip M
            continue
        # Look for -eig
        found_pair = False
        for eig2 in nonzero_eigs:
            if abs(eig + eig2) < 0.01 and abs(eig - eig2) > 0.01:
                pairs.append((float(np.real(eig)), float(np.real(eig2))))
                found_pair = True
                break
        if not found_pair and eig not in [p[0] for p in pairs] and eig not in [p[1] for p in pairs]:
            unpaired.append(float(np.real(eig)))
    
    # Compute the characteristic polynomial coefficients
    char_poly = np.poly(square)
    
    return {
        'n': n,
        'magic_constant': M,
        'max_eigenvalue': float(max_eig),
        'M_is_max_eigenvalue': m_is_max,
        'all_eigenvalues': [float(np.real(e)) for e in eigenvalues_real],
        'eigenvalue_pairs': pairs[:5],  # First 5 pairs
        'unpaired_eigenvalues': unpaired[:5],
        'characteristic_poly_coeffs': char_poly[:6].tolist(),
        'trace': float(np.trace(square)),
        'determinant': float(np.linalg.det(square))
    }

# ============================================================================
# THEOREM 2: COVARIANCE EIGENVALUE THEOREM
# ============================================================================

def analyze_covariance_eigenvalue_theorem(square: np.ndarray) -> Dict:
    """
    CONJECTURE: For an n×n magic square, the covariance matrix of the 
    Magic Gem coordinates has eigenvalues with specific structure:
    
    λ_z = Var(Z) = (n⁴ - 1) / 12
    λ_x = λ_y = (n² - 1) / 12
    
    This follows from:
    - The z-values are a permutation of {1-μ, 2-μ, ..., n²-μ}
    - The x,y values are symmetric around 0
    - Var(Z) = Σ(k-μ)² / n² = (n⁴-1)/12
    """
    n = square.shape[0]
    coords = square_to_coordinates(square)
    
    # Empirical variances
    var_x = np.var(coords[:, 0])
    var_y = np.var(coords[:, 1])
    var_z = np.var(coords[:, 2])
    
    # Theoretical predictions
    # For centered values 1,2,...,n², variance = (n⁴-1)/12
    theoretical_var_z = (n**4 - 1) / 12
    
    # For x,y on grid {-(n-1)/2, ..., (n-1)/2}, variance = (n²-1)/12
    theoretical_var_xy = (n**2 - 1) / 12
    
    # Covariance matrix and eigenvalues
    cov = np.cov(coords.T)
    eigenvalues = np.linalg.eigvals(cov)
    
    return {
        'n': n,
        'empirical_var_x': float(var_x),
        'empirical_var_y': float(var_y),
        'empirical_var_z': float(var_z),
        'theoretical_var_z': float(theoretical_var_z),
        'theoretical_var_xy': float(theoretical_var_xy),
        'var_z_matches_theory': abs(var_z - theoretical_var_z) < 0.01,
        'var_xy_matches_theory': abs(var_x - theoretical_var_xy) < 0.01,
        'cov_eigenvalues': [float(e) for e in sorted(np.real(eigenvalues))[::-1]],
        'cov_matrix': cov.tolist()
    }

# ============================================================================
# THEOREM 3: MOMENT INVARIANTS
# ============================================================================

def analyze_higher_moments(square: np.ndarray) -> Dict:
    """
    CONJECTURE: Higher-order moments of Magic Gem coordinates have special structure.
    
    For magic squares, we know:
    - E[X] = E[Y] = E[Z] = 0 (first moment)
    - Cov(X,Z) = Cov(Y,Z) = 0 (second moment cross-terms)
    
    What about:
    - Third moments (skewness)
    - Fourth moments (kurtosis)
    - Cross-moments E[X²Z], E[Y²Z], E[XYZ], etc.
    """
    coords = square_to_coordinates(square)
    n = square.shape[0]
    
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    
    # Second moments
    E_X2 = np.mean(x**2)
    E_Y2 = np.mean(y**2)
    E_Z2 = np.mean(z**2)
    E_XZ = np.mean(x * z)
    E_YZ = np.mean(y * z)
    E_XY = np.mean(x * y)
    
    # Third moments
    E_X3 = np.mean(x**3)
    E_Y3 = np.mean(y**3)
    E_Z3 = np.mean(z**3)
    E_X2Z = np.mean(x**2 * z)
    E_Y2Z = np.mean(y**2 * z)
    E_XYZ = np.mean(x * y * z)
    E_XZ2 = np.mean(x * z**2)
    E_YZ2 = np.mean(y * z**2)
    
    # Fourth moments
    E_X4 = np.mean(x**4)
    E_Y4 = np.mean(y**4)
    E_Z4 = np.mean(z**4)
    E_X2Y2 = np.mean(x**2 * y**2)
    E_X2Z2 = np.mean(x**2 * z**2)
    E_Y2Z2 = np.mean(y**2 * z**2)
    
    # Kurtosis
    kurtosis_z = E_Z4 / E_Z2**2 - 3  # Excess kurtosis
    
    return {
        'n': n,
        'second_moments': {
            'E_X2': float(E_X2), 'E_Y2': float(E_Y2), 'E_Z2': float(E_Z2),
            'E_XZ': float(E_XZ), 'E_YZ': float(E_YZ), 'E_XY': float(E_XY)
        },
        'third_moments': {
            'E_X3': float(E_X3), 'E_Y3': float(E_Y3), 'E_Z3': float(E_Z3),
            'E_X2Z': float(E_X2Z), 'E_Y2Z': float(E_Y2Z), 'E_XYZ': float(E_XYZ),
            'E_XZ2': float(E_XZ2), 'E_YZ2': float(E_YZ2)
        },
        'fourth_moments': {
            'E_X4': float(E_X4), 'E_Y4': float(E_Y4), 'E_Z4': float(E_Z4),
            'E_X2Y2': float(E_X2Y2), 'E_X2Z2': float(E_X2Z2), 'E_Y2Z2': float(E_Y2Z2)
        },
        'kurtosis_z': float(kurtosis_z),
        # Key prediction: For magic squares, certain cross-moments should vanish
        'E_X2Z_is_zero': abs(E_X2Z) < 1e-10,
        'E_Y2Z_is_zero': abs(E_Y2Z) < 1e-10,
        'E_XYZ_is_zero': abs(E_XYZ) < 1e-10
    }

# ============================================================================
# THEOREM 4: REPRESENTATION THEORY CONNECTION
# ============================================================================

def analyze_D4_representation(square: np.ndarray) -> Dict:
    """
    EXPLORATION: Connection to representation theory of D₄.
    
    The dihedral group D₄ acts on magic squares. This action induces
    a representation on the space of magic square coordinates.
    
    Key question: How do the eigenspaces of the magic square matrix
    transform under D₄?
    """
    n = square.shape[0]
    
    # Generate D4 transformations
    def apply_d4_transform(sq, k, flip):
        result = sq.copy()
        for _ in range(k):
            result = np.rot90(result)
        if flip:
            result = np.fliplr(result)
        return result
    
    # Compute eigenvalues for all D4 transforms
    eigenvalue_sets = []
    for k in range(4):
        for flip in [False, True]:
            transformed = apply_d4_transform(square, k, flip)
            eigs = np.sort(np.real(np.linalg.eigvals(transformed)))[::-1]
            eigenvalue_sets.append(eigs.tolist())
    
    # Check if eigenvalues are invariant under D4
    first_eigs = np.array(eigenvalue_sets[0])
    all_same = True
    for eigs in eigenvalue_sets[1:]:
        if not np.allclose(first_eigs, np.array(eigs)):
            all_same = False
            break
    
    return {
        'n': n,
        'eigenvalues_D4_invariant': all_same,
        'eigenvalue_sets': eigenvalue_sets[:4]  # First 4 transforms
    }

# ============================================================================
# THEOREM 5: PERTURBATION GAP STRUCTURE
# ============================================================================

def analyze_perturbation_gap_structure(square: np.ndarray) -> Dict:
    """
    REFINED ANALYSIS: Structure of perturbation gaps.
    
    The paper observed scaling Δ ∝ 1/n². But there may be finer structure.
    
    Key questions:
    1. Which swaps produce the minimum gap?
    2. Is there a pattern to which positions are most "sensitive"?
    3. Can we predict the gap from geometric properties?
    """
    n = square.shape[0]
    coords = square_to_coordinates(square)
    
    # Compute energy for base square (should be 0)
    def compute_energy(sq):
        c = square_to_coordinates(sq)
        x, y, z = c[:, 0], c[:, 1], c[:, 2]
        cov_xz = np.mean(x * z)
        cov_yz = np.mean(y * z)
        
        # Diagonal covariances
        n_sq = n * n
        z_flat = sq.flatten() - (n_sq + 1) / 2
        D_main = np.zeros(n_sq)
        D_anti = np.zeros(n_sq)
        for i in range(n):
            D_main[i * n + i] = 1
            D_anti[i * n + (n - 1 - i)] = 1
        cov_main = np.mean(D_main * z_flat)
        cov_anti = np.mean(D_anti * z_flat)
        
        return cov_xz**2 + cov_yz**2 + cov_main**2 + cov_anti**2
    
    base_energy = compute_energy(square)
    
    # Analyze all swaps
    gaps = []
    min_gap = float('inf')
    min_gap_positions = None
    
    # Categorize by swap type
    same_row_swaps = []
    same_col_swaps = []
    diagonal_swaps = []
    other_swaps = []
    
    for i1 in range(n):
        for j1 in range(n):
            for i2 in range(n):
                for j2 in range(n):
                    if (i1, j1) < (i2, j2):
                        perturbed = square.copy()
                        perturbed[i1, j1], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i1, j1]
                        gap = compute_energy(perturbed) - base_energy
                        gaps.append(gap)
                        
                        if gap < min_gap:
                            min_gap = gap
                            min_gap_positions = ((i1, j1), (i2, j2))
                        
                        # Categorize
                        if i1 == i2:
                            same_row_swaps.append(gap)
                        elif j1 == j2:
                            same_col_swaps.append(gap)
                        elif i1 == j1 and i2 == j2:  # Main diagonal
                            diagonal_swaps.append(gap)
                        elif i1 + j1 == n-1 and i2 + j2 == n-1:  # Anti-diagonal
                            diagonal_swaps.append(gap)
                        else:
                            other_swaps.append(gap)
    
    return {
        'n': n,
        'min_gap': float(min_gap),
        'min_gap_positions': min_gap_positions,
        'mean_gap': float(np.mean(gaps)),
        'std_gap': float(np.std(gaps)),
        'n_swaps': len(gaps),
        'same_row_mean': float(np.mean(same_row_swaps)) if same_row_swaps else None,
        'same_col_mean': float(np.mean(same_col_swaps)) if same_col_swaps else None,
        'diagonal_mean': float(np.mean(diagonal_swaps)) if diagonal_swaps else None,
        'other_mean': float(np.mean(other_swaps)) if other_swaps else None,
        'min_gap_times_n2': float(min_gap * n**2),
        'min_gap_times_n4': float(min_gap * n**4)
    }

# ============================================================================
# THEOREM 6: HULL VERTEX FORMULA
# ============================================================================

def analyze_hull_vertex_pattern() -> Dict:
    """
    CONJECTURE: The number of hull vertices follows a pattern.
    
    Observations:
    - n=3: 8 hull vertices, 1 interior
    - n=4: 12 hull vertices, 4 interior  
    - n=5: 12 hull vertices, 13 interior
    
    Is there a formula relating n to the number of hull vertices?
    """
    results = {}
    
    for n in [3, 5, 7, 9]:
        sq = siamese_method(n)
        coords = square_to_coordinates(sq)
        
        try:
            hull = ConvexHull(coords)
            n_hull = len(hull.vertices)
            n_interior = n*n - n_hull
            
            results[n] = {
                'n_points': n * n,
                'hull_vertices': n_hull,
                'interior_points': n_interior,
                'hull_fraction': n_hull / (n*n),
                'volume': hull.volume,
                'area': hull.area
            }
        except Exception as e:
            results[n] = {'error': str(e)}
    
    return results

# ============================================================================
# THEOREM 7: MODULAR MAGIC PRESERVATION
# ============================================================================

def analyze_modular_magic_preservation() -> Dict:
    """
    THEOREM (to prove): Magic squares preserve their magic property 
    under reduction modulo p for primes p.
    
    Specifically, if S is magic with constant M, then S mod p is
    "magic mod p" with constant M mod p.
    """
    results = {}
    
    for n in [3, 5, 7]:
        sq = siamese_method(n)
        M = n * (n*n + 1) // 2
        
        for p in [2, 3, 5, 7, 11, 13]:
            sq_mod = sq % p
            M_mod = M % p
            
            # Check if magic mod p
            row_sums = np.sum(sq_mod, axis=1) % p
            col_sums = np.sum(sq_mod, axis=0) % p
            main_diag = np.trace(sq_mod) % p
            anti_diag = np.trace(np.fliplr(sq_mod)) % p
            
            is_magic_mod_p = (
                len(set(row_sums)) == 1 and
                len(set(col_sums)) == 1 and
                row_sums[0] == col_sums[0] and
                main_diag == row_sums[0] and
                anti_diag == row_sums[0]
            )
            
            magic_sum_mod_p = int(row_sums[0]) if is_magic_mod_p else None
            
            key = f'n{n}_p{p}'
            results[key] = {
                'n': n,
                'p': p,
                'M_mod_p': int(M_mod),
                'is_magic_mod_p': is_magic_mod_p,
                'actual_magic_sum': magic_sum_mod_p,
                'sum_matches_M_mod_p': magic_sum_mod_p == M_mod if is_magic_mod_p else False
            }
    
    return results

# ============================================================================
# THEOREM 8: ENERGY LANDSCAPE TOPOLOGY
# ============================================================================

def analyze_energy_landscape_topology() -> Dict:
    """
    EXPLORATION: Topological structure of the energy landscape.
    
    Key questions:
    1. How many local minima are there (besides magic squares)?
    2. What's the connectivity structure?
    3. Are there saddle points with interesting structure?
    """
    n = 3
    
    # For n=3, we can do exhaustive analysis
    all_arrangements = list(permutations(range(1, n*n + 1)))
    
    def compute_energy(arr):
        sq = np.array(arr).reshape(n, n)
        coords = square_to_coordinates(sq)
        x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
        cov_xz = np.mean(x * z)
        cov_yz = np.mean(y * z)
        
        n_sq = n * n
        z_flat = sq.flatten() - (n_sq + 1) / 2
        D_main = np.zeros(n_sq)
        D_anti = np.zeros(n_sq)
        for i in range(n):
            D_main[i * n + i] = 1
            D_anti[i * n + (n - 1 - i)] = 1
        cov_main = np.mean(D_main * z_flat)
        cov_anti = np.mean(D_anti * z_flat)
        
        return cov_xz**2 + cov_yz**2 + cov_main**2 + cov_anti**2
    
    # Compute energies
    energies = [compute_energy(arr) for arr in all_arrangements]
    
    # Find local minima
    # An arrangement is a local minimum if all single swaps increase energy
    local_minima = []
    
    for idx, arr in enumerate(all_arrangements):
        e = energies[idx]
        is_local_min = True
        
        sq = np.array(arr).reshape(n, n)
        for i1 in range(n):
            for j1 in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if (i1, j1) < (i2, j2):
                            perturbed = sq.copy()
                            perturbed[i1, j1], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i1, j1]
                            perturbed_e = compute_energy(perturbed.flatten())
                            if perturbed_e < e - 1e-12:
                                is_local_min = False
                                break
                    if not is_local_min:
                        break
                if not is_local_min:
                    break
            if not is_local_min:
                break
        
        if is_local_min:
            local_minima.append({'index': idx, 'energy': e, 'arrangement': arr})
    
    # Count magic squares
    magic_count = sum(1 for e in energies if e < 1e-12)
    
    # Energy statistics
    energies = np.array(energies)
    
    return {
        'n': n,
        'total_arrangements': len(all_arrangements),
        'magic_squares': magic_count,
        'local_minima_count': len(local_minima),
        'all_local_minima_are_magic': all(lm['energy'] < 1e-12 for lm in local_minima),
        'energy_mean': float(np.mean(energies)),
        'energy_std': float(np.std(energies)),
        'energy_min': float(np.min(energies)),
        'energy_max': float(np.max(energies)),
        'energy_median': float(np.median(energies)),
        'fraction_near_zero': float((energies < 0.01).sum() / len(energies))
    }

# ============================================================================
# POTENTIAL NEW FORMULA EXPLORATION
# ============================================================================

def explore_characteristic_polynomial_pattern() -> Dict:
    """
    EXPLORATION: Pattern in characteristic polynomials of magic squares.
    
    The characteristic polynomial det(M - λI) encodes eigenvalue information.
    Are there patterns in the coefficients?
    """
    results = {}
    
    for n in [3, 5, 7]:
        if n == 3:
            sq = lo_shu()
        else:
            sq = siamese_method(n)
        
        # Characteristic polynomial
        char_poly = np.poly(sq)
        
        # Compute some invariants
        M = n * (n*n + 1) // 2
        trace = np.trace(sq)
        det = np.linalg.det(sq)
        
        # For magic squares, trace should equal sum of diagonal
        # which should equal M for the magic diagonal
        
        results[n] = {
            'magic_constant': M,
            'trace': float(trace),
            'determinant': float(det),
            'char_poly_coeffs': char_poly.tolist(),
            'leading_coeff': float(char_poly[0]),
            'constant_term': float(char_poly[-1]),  # (-1)^n * det
            'trace_equals_diagonal': abs(trace - np.trace(sq)) < 0.01
        }
    
    return results

# ============================================================================
# MAIN EXPLORATION
# ============================================================================

def run_new_theorems_exploration():
    """Run all new theorem explorations."""
    
    print("="*70)
    print("NEW THEOREMS AND CONJECTURES EXPLORATION")
    print("="*70)
    
    results = {}
    
    # Test squares
    lo_shu_sq = lo_shu()
    sq_4 = doubly_even_method(4)
    sq_5 = siamese_method(5)
    sq_7 = siamese_method(7)
    
    print("\n" + "="*70)
    print("THEOREM 1: SPECTRAL DECOMPOSITION")
    print("="*70)
    for n, sq in [(3, lo_shu_sq), (4, sq_4), (5, sq_5), (7, sq_7)]:
        spec = analyze_spectral_decomposition(sq)
        print(f"\nn={n}:")
        print(f"  M = {spec['magic_constant']}, max λ = {spec['max_eigenvalue']:.2f}")
        print(f"  M is max eigenvalue: {spec['M_is_max_eigenvalue']}")
        print(f"  Eigenvalues: {spec['all_eigenvalues'][:5]}")
        print(f"  Determinant: {spec['determinant']:.2f}")
        results[f'spectral_n{n}'] = spec
    
    print("\n" + "="*70)
    print("THEOREM 2: COVARIANCE EIGENVALUE STRUCTURE")
    print("="*70)
    for n, sq in [(3, lo_shu_sq), (5, sq_5), (7, sq_7)]:
        cov_th = analyze_covariance_eigenvalue_theorem(sq)
        print(f"\nn={n}:")
        print(f"  Var(Z) empirical: {cov_th['empirical_var_z']:.4f}")
        print(f"  Var(Z) theoretical: {cov_th['theoretical_var_z']:.4f}")
        print(f"  Match: {cov_th['var_z_matches_theory']}")
        print(f"  Var(X,Y) empirical: {cov_th['empirical_var_x']:.4f}")
        print(f"  Var(X,Y) theoretical: {cov_th['theoretical_var_xy']:.4f}")
        results[f'cov_theorem_n{n}'] = cov_th
    
    print("\n" + "="*70)
    print("THEOREM 3: HIGHER MOMENT STRUCTURE")
    print("="*70)
    for n, sq in [(3, lo_shu_sq), (5, sq_5)]:
        moments = analyze_higher_moments(sq)
        print(f"\nn={n}:")
        print(f"  E[X²Z] = {moments['third_moments']['E_X2Z']:.6f} (zero: {moments['E_X2Z_is_zero']})")
        print(f"  E[Y²Z] = {moments['third_moments']['E_Y2Z']:.6f} (zero: {moments['E_Y2Z_is_zero']})")
        print(f"  E[XYZ] = {moments['third_moments']['E_XYZ']:.6f} (zero: {moments['E_XYZ_is_zero']})")
        print(f"  Kurtosis(Z) = {moments['kurtosis_z']:.4f}")
        results[f'moments_n{n}'] = moments
    
    print("\n" + "="*70)
    print("THEOREM 4: D₄ REPRESENTATION")
    print("="*70)
    for n, sq in [(3, lo_shu_sq), (5, sq_5)]:
        d4_rep = analyze_D4_representation(sq)
        print(f"\nn={n}:")
        print(f"  Eigenvalues D₄-invariant: {d4_rep['eigenvalues_D4_invariant']}")
        results[f'd4_rep_n{n}'] = d4_rep
    
    print("\n" + "="*70)
    print("THEOREM 5: PERTURBATION GAP STRUCTURE")
    print("="*70)
    for n, sq in [(3, lo_shu_sq), (4, sq_4), (5, sq_5)]:
        gap_struct = analyze_perturbation_gap_structure(sq)
        print(f"\nn={n}:")
        print(f"  Min gap: {gap_struct['min_gap']:.6f}")
        print(f"  Min gap × n²: {gap_struct['min_gap_times_n2']:.4f}")
        print(f"  Min gap × n⁴: {gap_struct['min_gap_times_n4']:.4f}")
        print(f"  Same-row mean: {gap_struct['same_row_mean']:.4f}" if gap_struct['same_row_mean'] else "  Same-row: N/A")
        print(f"  Diagonal mean: {gap_struct['diagonal_mean']:.4f}" if gap_struct['diagonal_mean'] else "  Diagonal: N/A")
        results[f'gap_structure_n{n}'] = gap_struct
    
    print("\n" + "="*70)
    print("THEOREM 6: HULL VERTEX PATTERN")
    print("="*70)
    hull_pattern = analyze_hull_vertex_pattern()
    for n in sorted([k for k in hull_pattern.keys() if isinstance(k, int)]):
        data = hull_pattern[n]
        if 'error' not in data:
            print(f"n={n}: {data['hull_vertices']} hull, {data['interior_points']} interior, "
                  f"frac={data['hull_fraction']:.3f}")
    results['hull_pattern'] = hull_pattern
    
    print("\n" + "="*70)
    print("THEOREM 7: MODULAR MAGIC PRESERVATION")
    print("="*70)
    mod_magic = analyze_modular_magic_preservation()
    print("Magic mod p preserved for all tested (n, p) pairs:")
    all_preserved = all(v['is_magic_mod_p'] for v in mod_magic.values())
    print(f"  All preserved: {all_preserved}")
    # Show some examples
    for key in ['n3_p2', 'n3_p3', 'n5_p5', 'n7_p7']:
        if key in mod_magic:
            v = mod_magic[key]
            print(f"  {key}: magic mod p = {v['is_magic_mod_p']}, sum = {v['actual_magic_sum']}")
    results['modular_magic'] = mod_magic
    
    print("\n" + "="*70)
    print("THEOREM 8: ENERGY LANDSCAPE TOPOLOGY (n=3)")
    print("="*70)
    topo = analyze_energy_landscape_topology()
    print(f"Total arrangements: {topo['total_arrangements']}")
    print(f"Magic squares: {topo['magic_squares']}")
    print(f"Local minima: {topo['local_minima_count']}")
    print(f"All local minima are magic: {topo['all_local_minima_are_magic']}")
    print(f"Energy range: [{topo['energy_min']:.4f}, {topo['energy_max']:.4f}]")
    results['landscape_topology'] = topo
    
    print("\n" + "="*70)
    print("CHARACTERISTIC POLYNOMIAL PATTERNS")
    print("="*70)
    char_patterns = explore_characteristic_polynomial_pattern()
    for n in sorted(char_patterns.keys()):
        data = char_patterns[n]
        print(f"n={n}: det={data['determinant']:.2f}, trace={data['trace']:.0f}, M={data['magic_constant']}")
    results['char_poly'] = char_patterns
    
    # Save results
    print("\n\nSaving results to new_theorems_results.json...")
    
    def convert_to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, dict):
            return {str(k): convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(v) for v in obj]
        elif isinstance(obj, tuple):
            return [convert_to_serializable(v) for v in obj]
        elif isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag}
        return obj
    
    serializable_results = convert_to_serializable(results)
    
    with open('new_theorems_results.json', 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print("\n" + "="*70)
    print("EXPLORATION COMPLETE")
    print("="*70)
    
    return results

if __name__ == "__main__":
    results = run_new_theorems_exploration()
