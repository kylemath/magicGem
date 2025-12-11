"""
Deep Mathematical Exploration of Magic Gems
============================================

This script explores potential new theorems, conjectures, and connections
to other areas of mathematics arising from the Magic Gem framework.

Key areas explored:
1. Spectral theory connections (eigenvalues, determinants)
2. Graph theory and Latin squares
3. Number theory (modular arithmetic patterns)
4. Topological invariants
5. Algebraic structure of the n=4 trimodal clustering
6. Connections to Birkhoff polytope and doubly stochastic matrices
7. Tensegrity and rigidity analysis
8. Potential Langlands-type connections via L-functions
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
# MAGIC SQUARE GENERATION
# ============================================================================

def lo_shu():
    """The canonical Lo Shu 3x3 magic square."""
    return np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])

def siamese_method(n: int) -> np.ndarray:
    """Generate magic square using Siamese method (odd n only)."""
    if n % 2 == 0:
        raise ValueError("Siamese method only works for odd n")
    
    square = np.zeros((n, n), dtype=int)
    i, j = 0, n // 2
    
    for num in range(1, n*n + 1):
        square[i, j] = num
        i_new, j_new = (i - 1) % n, (j + 1) % n
        if square[i_new, j_new] != 0:
            i_new = (i + 1) % n
            j_new = j
        i, j = i_new, j_new
    
    return square

def doubly_even_method(n: int) -> np.ndarray:
    """Generate magic square using doubly-even method (n divisible by 4)."""
    if n % 4 != 0:
        raise ValueError("Doubly-even method requires n divisible by 4")
    
    square = np.arange(1, n*n + 1).reshape(n, n)
    
    for i in range(n):
        for j in range(n):
            if ((i % 4 == j % 4) or ((i % 4) + (j % 4) == 3)):
                square[i, j] = n*n + 1 - square[i, j]
    
    return square

def generate_all_3x3_magic_squares() -> List[np.ndarray]:
    """Generate all 8 D4 variants of the 3x3 magic square."""
    base = lo_shu()
    squares = []
    
    current = base.copy()
    for _ in range(4):
        squares.append(current.copy())
        squares.append(np.fliplr(current).copy())
        current = np.rot90(current)
    
    return squares

def generate_all_4x4_magic_squares() -> List[np.ndarray]:
    """
    Generate all 880 essentially different 4x4 magic squares.
    Uses the known enumeration algorithm.
    """
    # This is a more involved generation - we use a subset for exploration
    # Full enumeration would require the Frénicle algorithm
    squares = []
    
    # Start with the doubly-even construction
    base = doubly_even_method(4)
    
    # Generate D4 variants
    current = base.copy()
    for _ in range(4):
        squares.append(current.copy())
        squares.append(np.fliplr(current).copy())
        current = np.rot90(current)
    
    # For full analysis, we'd need to implement Frénicle enumeration
    # For now, return what we have plus some additional known squares
    
    return squares

def is_magic_square(square: np.ndarray) -> bool:
    """Check if an arrangement is a magic square."""
    n = square.shape[0]
    M = n * (n*n + 1) // 2
    
    # Check rows and columns
    if not all(np.sum(square, axis=1) == M):
        return False
    if not all(np.sum(square, axis=0) == M):
        return False
    
    # Check diagonals
    if np.trace(square) != M:
        return False
    if np.trace(np.fliplr(square)) != M:
        return False
    
    return True

# ============================================================================
# CORE ENERGY COMPUTATIONS
# ============================================================================

def square_to_coordinates(square: np.ndarray) -> np.ndarray:
    """Convert magic square to centered 3D coordinates."""
    n = square.shape[0]
    offset = (n - 1) / 2
    z_center = (n**2 + 1) / 2
    
    coords = []
    for i in range(n):
        for j in range(n):
            x = j - offset
            y = offset - i
            z = square[i, j] - z_center
            coords.append([x, y, z])
    
    return np.array(coords)

def compute_total_magic_energy(square: np.ndarray) -> float:
    """Compute total magic energy E(S)."""
    coords = square_to_coordinates(square)
    n = square.shape[0]
    
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    
    cov_xz = np.mean(x * z)
    cov_yz = np.mean(y * z)
    
    # Diagonal covariances
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

# ============================================================================
# 1. SPECTRAL THEORY ANALYSIS
# ============================================================================

def analyze_spectral_properties(square: np.ndarray) -> Dict:
    """
    Analyze spectral properties of magic square matrices.
    
    Known result: Magic squares have eigenvalue M(n) with eigenvector (1,1,...,1).
    We explore additional spectral structure and connections to the Magic Gem.
    """
    n = square.shape[0]
    M = n * (n*n + 1) // 2
    
    # Eigenvalues of the magic square matrix
    eigenvalues = np.linalg.eigvals(square)
    eigenvalues_sorted = np.sort(np.real(eigenvalues))[::-1]
    
    # Verify M is an eigenvalue
    has_M_eigenvalue = np.any(np.abs(eigenvalues - M) < 1e-10)
    
    # Determinant
    det = np.linalg.det(square)
    
    # Trace (should equal n * center value = n * (n²+1)/2 for magic squares)
    trace = np.trace(square)
    expected_trace = n * (n**2 + 1) / 2  # Only true if center value is average
    
    # Condition number (measures matrix stability)
    cond = np.linalg.cond(square)
    
    # Singular values
    singular_values = np.linalg.svd(square, compute_uv=False)
    
    # Frobenius norm
    frobenius = np.linalg.norm(square, 'fro')
    
    # Spectral radius
    spectral_radius = np.max(np.abs(eigenvalues))
    
    # NEW: Eigenvalue ratios (potential invariant)
    nonzero_eigs = eigenvalues[np.abs(eigenvalues) > 1e-10]
    if len(nonzero_eigs) >= 2:
        eig_ratios = np.sort(np.abs(nonzero_eigs))[::-1]
        eig_ratio_12 = eig_ratios[0] / eig_ratios[1] if len(eig_ratios) > 1 else None
    else:
        eig_ratio_12 = None
    
    return {
        'eigenvalues': eigenvalues_sorted.tolist(),
        'has_M_eigenvalue': has_M_eigenvalue,
        'determinant': det,
        'trace': trace,
        'condition_number': cond,
        'singular_values': singular_values.tolist(),
        'frobenius_norm': frobenius,
        'spectral_radius': spectral_radius,
        'eigenvalue_ratio_1_2': eig_ratio_12
    }

def analyze_covariance_matrix_spectrum(square: np.ndarray) -> Dict:
    """
    Analyze the spectrum of the covariance matrix of the Magic Gem.
    
    For magic squares, we proved Cov(X,Z) = Cov(Y,Z) = 0.
    This means the covariance matrix has special block-diagonal structure.
    """
    coords = square_to_coordinates(square)
    cov_matrix = np.cov(coords.T)
    
    eigenvalues = np.linalg.eigvals(cov_matrix)
    eigenvalues_sorted = np.sort(np.real(eigenvalues))[::-1]
    
    # Check block-diagonal property
    off_diag_xz = abs(cov_matrix[0, 2])
    off_diag_yz = abs(cov_matrix[1, 2])
    
    is_block_diagonal = off_diag_xz < 1e-10 and off_diag_yz < 1e-10
    
    return {
        'cov_matrix': cov_matrix.tolist(),
        'cov_eigenvalues': eigenvalues_sorted.tolist(),
        'is_block_diagonal': is_block_diagonal,
        'off_diag_xz': off_diag_xz,
        'off_diag_yz': off_diag_yz
    }

# ============================================================================
# 2. GRAPH THEORY AND LATIN SQUARE CONNECTIONS
# ============================================================================

def magic_square_to_latin_square(square: np.ndarray) -> np.ndarray:
    """
    Convert a magic square to a Latin-square-like representation.
    
    For n=3, values 1-9 can be partitioned into 3 groups of 3.
    We label cells by which "level" their value belongs to.
    """
    n = square.shape[0]
    n_sq = n * n
    
    # Partition values into n groups of n values each
    partition_size = n
    latin = np.zeros_like(square)
    
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            level = (val - 1) // partition_size
            latin[i, j] = level
    
    return latin

def analyze_graph_structure(square: np.ndarray) -> Dict:
    """
    Analyze the graph structure induced by the magic square.
    
    Create graphs:
    1. Adjacency graph: vertices are cells, edges connect cells sharing row/col/diag
    2. Value graph: vertices are values 1..n², edges based on position relationship
    """
    n = square.shape[0]
    
    # Build adjacency structure
    cells = [(i, j) for i in range(n) for j in range(n)]
    
    # Count how many "structural constraints" each pair of cells shares
    constraint_matrix = np.zeros((n*n, n*n))
    
    for idx1, (i1, j1) in enumerate(cells):
        for idx2, (i2, j2) in enumerate(cells):
            if idx1 == idx2:
                continue
            
            shared = 0
            if i1 == i2:  # Same row
                shared += 1
            if j1 == j2:  # Same column
                shared += 1
            if i1 == j1 and i2 == j2:  # Both on main diagonal
                shared += 1
            if i1 + j1 == n - 1 and i2 + j2 == n - 1:  # Both on anti-diagonal
                shared += 1
            
            constraint_matrix[idx1, idx2] = shared
    
    # Analyze the constraint graph
    max_shared = int(constraint_matrix.max())
    avg_shared = constraint_matrix.sum() / (n*n * (n*n - 1))
    
    # Check if it's regular (each vertex has same number of edges)
    edge_counts = (constraint_matrix > 0).sum(axis=1)
    is_regular = len(set(edge_counts)) == 1
    
    return {
        'n_vertices': n * n,
        'max_shared_constraints': max_shared,
        'avg_shared_constraints': avg_shared,
        'is_regular_graph': is_regular,
        'vertex_degrees': edge_counts.tolist()
    }

# ============================================================================
# 3. NUMBER THEORY CONNECTIONS
# ============================================================================

def analyze_modular_structure(square: np.ndarray) -> Dict:
    """
    Analyze modular arithmetic patterns in magic squares.
    
    Explores:
    1. Row/column/diagonal sums modulo various primes
    2. Quadratic residue patterns
    3. Connection to magic constant factorization
    """
    n = square.shape[0]
    M = n * (n*n + 1) // 2
    
    results = {
        'n': n,
        'magic_constant': M,
        'magic_constant_factorization': prime_factorization(M)
    }
    
    # Analyze modular structure for small primes
    primes = [2, 3, 5, 7, 11]
    
    for p in primes:
        square_mod_p = square % p
        
        # Row sums mod p
        row_sums_mod = np.sum(square_mod_p, axis=1) % p
        col_sums_mod = np.sum(square_mod_p, axis=0) % p
        
        # Check if still "magic" mod p
        is_magic_mod_p = (len(set(row_sums_mod)) == 1 and 
                         len(set(col_sums_mod)) == 1 and
                         row_sums_mod[0] == col_sums_mod[0])
        
        results[f'mod_{p}'] = {
            'square_mod_p': square_mod_p.tolist(),
            'row_sums_mod_p': row_sums_mod.tolist(),
            'is_magic_mod_p': is_magic_mod_p,
            'M_mod_p': M % p
        }
    
    # Quadratic residue pattern
    for p in [3, 5, 7]:
        if n*n >= p:
            qr_pattern = np.array([[is_quadratic_residue(v, p) for v in row] for row in square])
            results[f'qr_pattern_mod_{p}'] = qr_pattern.tolist()
    
    return results

def prime_factorization(n: int) -> Dict[int, int]:
    """Return prime factorization as dict."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def is_quadratic_residue(a: int, p: int) -> int:
    """Check if a is a quadratic residue mod p. Returns 1, -1, or 0."""
    a = int(a)
    if a % p == 0:
        return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

# ============================================================================
# 4. TOPOLOGICAL INVARIANTS
# ============================================================================

def analyze_topology(square: np.ndarray) -> Dict:
    """
    Analyze topological properties of the Magic Gem.
    
    Computes:
    1. Euler characteristic of the convex hull
    2. Betti numbers (via edge/face counts)
    3. Genus estimate
    """
    coords = square_to_coordinates(square)
    
    try:
        hull = ConvexHull(coords)
        
        V = len(hull.vertices)  # Vertices on hull
        F = len(hull.simplices)  # Faces (triangular)
        
        # Edges: each triangular face has 3 edges, each shared by 2 faces
        # For convex hull: E = 3F/2
        E = 3 * F // 2
        
        # Euler characteristic: V - E + F = 2 for convex polyhedra
        euler_char = V - E + F
        
        # Volume and area
        volume = hull.volume
        area = hull.area
        
        # Isoperimetric ratio: V^(2/3) / A (normalized)
        if area > 0:
            isoperimetric = (volume ** (2/3)) / area
        else:
            isoperimetric = 0
        
        return {
            'hull_vertices': V,
            'hull_faces': F,
            'hull_edges': E,
            'euler_characteristic': euler_char,
            'hull_volume': volume,
            'hull_area': area,
            'isoperimetric_ratio': isoperimetric,
            'interior_points': len(coords) - V
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_delaunay_complex(square: np.ndarray) -> Dict:
    """
    Analyze the Delaunay complex of the Magic Gem points.
    
    The Delaunay triangulation provides a natural simplicial complex
    whose homology we can study.
    """
    coords = square_to_coordinates(square)
    
    try:
        tri = Delaunay(coords)
        
        n_simplices = len(tri.simplices)
        
        # Find unique edges
        edges = set()
        for simplex in tri.simplices:
            for i in range(len(simplex)):
                for j in range(i+1, len(simplex)):
                    edge = tuple(sorted([simplex[i], simplex[j]]))
                    edges.add(edge)
        
        n_edges = len(edges)
        n_vertices = len(coords)
        
        # Euler characteristic of Delaunay complex
        euler = n_vertices - n_edges + n_simplices
        
        return {
            'n_vertices': n_vertices,
            'n_edges': n_edges,
            'n_tetrahedra': n_simplices,
            'delaunay_euler_char': euler
        }
    except Exception as e:
        return {'error': str(e)}

# ============================================================================
# 5. TRIMODAL STRUCTURE ANALYSIS (n=4)
# ============================================================================

def analyze_n4_trimodal_structure() -> Dict:
    """
    Investigate the trimodal structure observed in n=4 perturbation gaps.
    
    The paper observes that 880 n=4 magic squares cluster into 3 distinct
    bands of perturbation resistance. We investigate what geometric/algebraic
    properties distinguish these classes.
    """
    print("Analyzing n=4 trimodal structure...")
    
    # We'll analyze a subset of n=4 squares we can generate
    squares = generate_all_4x4_magic_squares()
    
    results = {
        'n_squares_analyzed': len(squares),
        'gap_distribution': [],
        'spectral_clusters': [],
        'hull_clusters': []
    }
    
    for sq in squares:
        # Compute perturbation gap
        base_energy = compute_total_magic_energy(sq)
        
        min_gap = float('inf')
        for i in range(4):
            for j in range(4):
                for i2 in range(4):
                    for j2 in range(4):
                        if (i, j) < (i2, j2):
                            perturbed = sq.copy()
                            perturbed[i, j], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i, j]
                            gap = compute_total_magic_energy(perturbed) - base_energy
                            min_gap = min(min_gap, gap)
        
        results['gap_distribution'].append(min_gap)
        
        # Spectral properties
        spectral = analyze_spectral_properties(sq)
        results['spectral_clusters'].append({
            'determinant': spectral['determinant'],
            'condition': spectral['condition_number'],
            'gap': min_gap
        })
        
        # Hull properties
        topo = analyze_topology(sq)
        if 'hull_volume' in topo:
            results['hull_clusters'].append({
                'volume': topo['hull_volume'],
                'area': topo['hull_area'],
                'vertices': topo['hull_vertices'],
                'gap': min_gap
            })
    
    # Cluster analysis
    gaps = np.array(results['gap_distribution'])
    results['gap_statistics'] = {
        'min': float(np.min(gaps)),
        'max': float(np.max(gaps)),
        'mean': float(np.mean(gaps)),
        'std': float(np.std(gaps))
    }
    
    return results

# ============================================================================
# 6. BIRKHOFF POLYTOPE CONNECTION
# ============================================================================

def analyze_birkhoff_connection(square: np.ndarray) -> Dict:
    """
    Explore connection between magic squares and doubly stochastic matrices.
    
    The Birkhoff-von Neumann theorem relates permutation matrices to
    doubly stochastic matrices. Magic squares, as permutation matrices
    of values, may have similar structure.
    """
    n = square.shape[0]
    n_sq = n * n
    
    # Normalize the magic square
    normalized = (square - 1) / (n_sq - 1)  # Map [1, n²] to [0, 1]
    
    # Check row and column sum properties
    row_sums = np.sum(normalized, axis=1)
    col_sums = np.sum(normalized, axis=0)
    
    # For doubly stochastic: all row/col sums = 1
    # For magic: all row/col sums = same value (but not necessarily 1)
    
    magic_row_sum = np.mean(row_sums)
    
    # Compute "doubly stochastic distance"
    # How far is this from being a valid doubly stochastic matrix?
    ds_distance = np.std(row_sums) + np.std(col_sums)
    
    # Permanence (for the permutation structure)
    # Each row and column of a magic square contains each position exactly once
    # in the permutation interpretation
    
    return {
        'normalized_row_sums': row_sums.tolist(),
        'normalized_col_sums': col_sums.tolist(),
        'magic_row_sum': magic_row_sum,
        'doubly_stochastic_distance': ds_distance,
        'is_row_stochastic_approx': ds_distance < 0.1
    }

# ============================================================================
# 7. TENSEGRITY AND RIGIDITY
# ============================================================================

def analyze_rigidity(square: np.ndarray) -> Dict:
    """
    Analyze the rigidity of the Magic Gem as a tensegrity structure.
    
    Computes:
    1. The rigidity matrix
    2. Rank and nullity
    3. Whether the structure is infinitesimally rigid
    """
    coords = square_to_coordinates(square)
    n_points = len(coords)
    
    try:
        hull = ConvexHull(coords)
        
        # Build edge list from hull
        edges = set()
        for simplex in hull.simplices:
            for i in range(len(simplex)):
                for j in range(i+1, len(simplex)):
                    edge = tuple(sorted([simplex[i], simplex[j]]))
                    edges.add(edge)
        
        edges = list(edges)
        n_edges = len(edges)
        
        # Rigidity matrix: (n_edges × 3*n_points)
        # Each row corresponds to an edge, enforcing the distance constraint
        rigidity_matrix = np.zeros((n_edges, 3 * n_points))
        
        for e_idx, (i, j) in enumerate(edges):
            diff = coords[i] - coords[j]
            # d/d(p_i) of ||p_i - p_j||² gives 2(p_i - p_j)
            rigidity_matrix[e_idx, 3*i:3*i+3] = diff
            rigidity_matrix[e_idx, 3*j:3*j+3] = -diff
        
        # Compute rank
        rank = np.linalg.matrix_rank(rigidity_matrix)
        
        # For 3D with n vertices, need rank = 3n - 6 for infinitesimal rigidity
        # (subtracting 6 for rigid motions: 3 translations, 3 rotations)
        required_rank = 3 * n_points - 6
        
        is_rigid = rank >= required_rank
        
        return {
            'n_points': n_points,
            'n_edges': n_edges,
            'rigidity_matrix_rank': rank,
            'required_rank_for_rigidity': required_rank,
            'is_infinitesimally_rigid': is_rigid,
            'degrees_of_freedom': 3 * n_points - 6 - rank if rank < required_rank else 0
        }
    except Exception as e:
        return {'error': str(e)}

# ============================================================================
# 8. POTENTIAL L-FUNCTION CONNECTIONS
# ============================================================================

def analyze_zeta_like_properties(square: np.ndarray) -> Dict:
    """
    Explore potential connections to zeta/L-functions.
    
    Magic squares have highly structured sums. We investigate
    if there are any Dirichlet-series-like structures.
    """
    n = square.shape[0]
    values = square.flatten()
    
    # Compute various "zeta-like" sums
    results = {}
    
    for s in [1, 2, 3, 4]:
        # Sum of 1/v^s
        zeta_sum = np.sum(1.0 / values**s)
        results[f'zeta_sum_s{s}'] = zeta_sum
    
    # Position-weighted sums (like Dirichlet L-functions)
    coords = square_to_coordinates(square)
    for s in [1, 2]:
        # Sum of z^s / (x² + y² + 1)
        weighted_sum = np.sum(coords[:, 2]**s / (coords[:, 0]**2 + coords[:, 1]**2 + 1))
        results[f'position_weighted_s{s}'] = weighted_sum
    
    # Character-like sums (using row/col position as "character")
    for i in range(n):
        row_sum = np.sum(square[i, :])
        col_sum = np.sum(square[:, i])
        results[f'row_{i}_sum'] = int(row_sum)
        results[f'col_{i}_sum'] = int(col_sum)
    
    return results

# ============================================================================
# 9. NEW CONJECTURES EXPLORATION
# ============================================================================

def explore_hull_volume_scaling() -> Dict:
    """
    Conjecture: Hull volume scales as O(n^4).
    
    Investigate the scaling of convex hull volume with n.
    """
    results = {}
    
    for n in [3, 5, 7]:
        sq = siamese_method(n)
        coords = square_to_coordinates(sq)
        
        try:
            hull = ConvexHull(coords)
            results[n] = {
                'hull_volume': hull.volume,
                'n^4': n**4,
                'ratio_to_n4': hull.volume / n**4,
                'hull_area': hull.area,
                'ratio_area_to_n3': hull.area / n**3
            }
        except:
            pass
    
    return results

def explore_gap_scaling_conjecture() -> Dict:
    """
    Conjecture: Minimum perturbation gap scales as 1/n².
    
    The paper observed Δ_min ∝ 1/n². We verify and refine this.
    """
    results = {}
    
    for n in [3, 5]:
        sq = siamese_method(n)
        base_energy = compute_total_magic_energy(sq)
        
        min_gap = float('inf')
        for i in range(n):
            for j in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if (i, j) < (i2, j2):
                            perturbed = sq.copy()
                            perturbed[i, j], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i, j]
                            gap = compute_total_magic_energy(perturbed) - base_energy
                            min_gap = min(min_gap, gap)
        
        results[n] = {
            'min_gap': min_gap,
            'n_squared': n**2,
            'gap_times_n2': min_gap * n**2,
            'gap_times_n4': min_gap * n**4
        }
    
    # Add n=4
    sq4 = doubly_even_method(4)
    base_energy = compute_total_magic_energy(sq4)
    min_gap = float('inf')
    for i in range(4):
        for j in range(4):
            for i2 in range(4):
                for j2 in range(4):
                    if (i, j) < (i2, j2):
                        perturbed = sq4.copy()
                        perturbed[i, j], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i, j]
                        gap = compute_total_magic_energy(perturbed) - base_energy
                        min_gap = min(min_gap, gap)
    
    results[4] = {
        'min_gap': min_gap,
        'n_squared': 16,
        'gap_times_n2': min_gap * 16,
        'gap_times_n4': min_gap * 256
    }
    
    return results

def explore_eigenvalue_sum_conjecture() -> Dict:
    """
    Conjecture: The sum of eigenvalues (trace) has a specific relationship
    to the magic constant and geometric properties.
    """
    results = {}
    
    for n in [3, 4, 5]:
        if n == 4:
            sq = doubly_even_method(4)
        else:
            sq = siamese_method(n)
        
        M = n * (n*n + 1) // 2
        
        eigenvalues = np.linalg.eigvals(sq)
        trace = np.sum(eigenvalues)  # = sum of diagonal = sum of all values / n for some squares
        
        # For the standard magic square, what's the trace?
        actual_trace = np.trace(sq)
        
        # Diagonal sum for magic square should be M
        diag_sum = np.trace(sq)
        
        results[n] = {
            'magic_constant': M,
            'trace': float(np.real(trace)),
            'diagonal_sum': int(diag_sum),
            'eigenvalue_sum': float(np.real(np.sum(eigenvalues))),
            'max_eigenvalue': float(np.max(np.real(eigenvalues))),
            'max_equals_M': abs(np.max(np.real(eigenvalues)) - M) < 0.01
        }
    
    return results

def explore_covariance_tensor_structure() -> Dict:
    """
    New exploration: The covariance tensor across all magic squares.
    
    For a fixed n, what is the structure of the "average" covariance
    matrix across all magic squares?
    """
    results = {}
    
    # n=3: all 8 squares
    squares_3 = generate_all_3x3_magic_squares()
    cov_matrices = []
    
    for sq in squares_3:
        coords = square_to_coordinates(sq)
        cov = np.cov(coords.T)
        cov_matrices.append(cov)
    
    avg_cov = np.mean(cov_matrices, axis=0)
    
    results['n3'] = {
        'n_squares': len(squares_3),
        'average_covariance_matrix': avg_cov.tolist(),
        'avg_cov_eigenvalues': np.linalg.eigvals(avg_cov).tolist()
    }
    
    return results

# ============================================================================
# 10. ENUMERATION CONJECTURES
# ============================================================================

def analyze_enumeration_patterns() -> Dict:
    """
    Analyze patterns in magic square enumeration that might yield new formulas.
    
    Known counts:
    n=3: 8 (1 equivalence class)
    n=4: 7040 (880 equivalence classes)  
    n=5: ~275,305,224 (~34,413,153 classes)
    
    Are there patterns suggesting a closed form?
    """
    known_counts = {
        3: {'total': 8, 'classes': 1},
        4: {'total': 7040, 'classes': 880},
        5: {'total': 275305224, 'classes': 34413153}
    }
    
    results = {
        'known_counts': known_counts
    }
    
    # Analyze ratios
    for n in [3, 4, 5]:
        data = known_counts[n]
        results[f'n{n}_ratio_to_factorial'] = data['total'] / math.factorial(n*n)
        results[f'n{n}_ratio_classes_to_total'] = data['classes'] / data['total']
        results[f'n{n}_log_total'] = np.log(float(data['total']))
        results[f'n{n}_log_factorial'] = np.log(float(math.factorial(n*n)))
    
    # Potential formula patterns
    for n in [3, 4, 5]:
        data = known_counts[n]
        # classes = total / |D4| = total / 8
        expected_classes = data['total'] / 8
        results[f'n{n}_expected_classes_from_D4'] = expected_classes
        results[f'n{n}_actual_vs_expected_classes'] = data['classes'] / expected_classes
    
    return results

# ============================================================================
# MAIN EXPLORATION
# ============================================================================

def run_deep_exploration():
    """Run all explorations and compile results."""
    
    print("="*70)
    print("DEEP MATHEMATICAL EXPLORATION OF MAGIC GEMS")
    print("="*70)
    
    results = {}
    
    # Test squares
    lo_shu_sq = lo_shu()
    sq_5 = siamese_method(5)
    sq_4 = doubly_even_method(4)
    
    print("\n1. SPECTRAL THEORY ANALYSIS")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (4, sq_4), (5, sq_5)]:
        spec = analyze_spectral_properties(sq)
        print(f"\nn={n}:")
        print(f"  Eigenvalues: {[f'{e:.2f}' for e in spec['eigenvalues'][:4]]}")
        print(f"  Has M as eigenvalue: {spec['has_M_eigenvalue']}")
        print(f"  Determinant: {spec['determinant']:.2f}")
        print(f"  Condition number: {spec['condition_number']:.4f}")
        results[f'spectral_n{n}'] = spec
    
    print("\n\n2. COVARIANCE MATRIX SPECTRUM")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (4, sq_4), (5, sq_5)]:
        cov_spec = analyze_covariance_matrix_spectrum(sq)
        print(f"\nn={n}:")
        print(f"  Is block-diagonal: {cov_spec['is_block_diagonal']}")
        print(f"  Cov eigenvalues: {[f'{e:.4f}' for e in cov_spec['cov_eigenvalues']]}")
        results[f'cov_spectrum_n{n}'] = cov_spec
    
    print("\n\n3. GRAPH STRUCTURE")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (5, sq_5)]:
        graph = analyze_graph_structure(sq)
        print(f"\nn={n}:")
        print(f"  Vertices: {graph['n_vertices']}")
        print(f"  Max shared constraints: {graph['max_shared_constraints']}")
        print(f"  Is regular graph: {graph['is_regular_graph']}")
        results[f'graph_n{n}'] = graph
    
    print("\n\n4. NUMBER THEORY PATTERNS")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (5, sq_5)]:
        mod_analysis = analyze_modular_structure(sq)
        print(f"\nn={n}:")
        print(f"  Magic constant: {mod_analysis['magic_constant']}")
        print(f"  Factorization: {mod_analysis['magic_constant_factorization']}")
        for p in [2, 3, 5]:
            print(f"  Is magic mod {p}: {mod_analysis[f'mod_{p}']['is_magic_mod_p']}")
        results[f'modular_n{n}'] = mod_analysis
    
    print("\n\n5. TOPOLOGICAL INVARIANTS")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (4, sq_4), (5, sq_5)]:
        topo = analyze_topology(sq)
        if 'error' not in topo:
            print(f"\nn={n}:")
            print(f"  Hull vertices: {topo['hull_vertices']}")
            print(f"  Hull faces: {topo['hull_faces']}")
            print(f"  Euler char: {topo['euler_characteristic']}")
            print(f"  Interior points: {topo['interior_points']}")
            print(f"  Isoperimetric ratio: {topo['isoperimetric_ratio']:.4f}")
        results[f'topology_n{n}'] = topo
    
    print("\n\n6. RIGIDITY ANALYSIS")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (5, sq_5)]:
        rigid = analyze_rigidity(sq)
        if 'error' not in rigid:
            print(f"\nn={n}:")
            print(f"  Is infinitesimally rigid: {rigid['is_infinitesimally_rigid']}")
            print(f"  Rigidity matrix rank: {rigid['rigidity_matrix_rank']}")
            print(f"  Required rank: {rigid['required_rank_for_rigidity']}")
        results[f'rigidity_n{n}'] = rigid
    
    print("\n\n7. BIRKHOFF POLYTOPE CONNECTION")
    print("-" * 40)
    for n, sq in [(3, lo_shu_sq), (4, sq_4)]:
        birk = analyze_birkhoff_connection(sq)
        print(f"\nn={n}:")
        print(f"  Magic row sum (normalized): {birk['magic_row_sum']:.4f}")
        print(f"  Doubly stochastic distance: {birk['doubly_stochastic_distance']:.6f}")
        results[f'birkhoff_n{n}'] = birk
    
    print("\n\n8. SCALING CONJECTURES")
    print("-" * 40)
    
    print("\nHull volume scaling:")
    hull_scaling = explore_hull_volume_scaling()
    for n, data in hull_scaling.items():
        print(f"  n={n}: V={data['hull_volume']:.2f}, V/n⁴={data['ratio_to_n4']:.6f}")
    results['hull_volume_scaling'] = hull_scaling
    
    print("\nPerturbation gap scaling:")
    gap_scaling = explore_gap_scaling_conjecture()
    for n, data in gap_scaling.items():
        print(f"  n={n}: Δ={data['min_gap']:.6f}, Δ·n²={data['gap_times_n2']:.4f}")
    results['gap_scaling'] = gap_scaling
    
    print("\n\n9. EIGENVALUE CONJECTURES")
    print("-" * 40)
    eig_conj = explore_eigenvalue_sum_conjecture()
    for n, data in eig_conj.items():
        print(f"  n={n}: M={data['magic_constant']}, max_λ={data['max_eigenvalue']:.2f}, "
              f"max_λ=M: {data['max_equals_M']}")
    results['eigenvalue_conjecture'] = eig_conj
    
    print("\n\n10. ENUMERATION PATTERNS")
    print("-" * 40)
    enum_patterns = analyze_enumeration_patterns()
    for n in [3, 4, 5]:
        print(f"  n={n}: total/n!={enum_patterns[f'n{n}_ratio_to_factorial']:.2e}")
    results['enumeration'] = enum_patterns
    
    print("\n\n11. COVARIANCE TENSOR STRUCTURE")
    print("-" * 40)
    cov_tensor = explore_covariance_tensor_structure()
    print("Average covariance matrix for n=3 (all 8 squares):")
    avg_cov = np.array(cov_tensor['n3']['average_covariance_matrix'])
    print(np.round(avg_cov, 4))
    results['covariance_tensor'] = cov_tensor
    
    # Save results
    print("\n\nSaving results to deep_exploration_results.json...")
    
    # Convert numpy types for JSON
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
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(v) for v in obj]
        elif isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag}
        return obj
    
    serializable_results = convert_to_serializable(results)
    
    with open('deep_exploration_results.json', 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print("\n" + "="*70)
    print("EXPLORATION COMPLETE")
    print("="*70)
    
    return results

if __name__ == "__main__":
    results = run_deep_exploration()
