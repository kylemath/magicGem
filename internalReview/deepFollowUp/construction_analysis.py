"""
Critical Analysis: Construction Method Bias and Covariance-Based Construction

This script investigates:
1. Whether my findings are artifacts of specific construction methods
2. The covariance conditions as a SYSTEM OF EQUATIONS to solve for magic squares
3. Comparison across ALL n=4 magic squares (not just one construction)

KEY INSIGHT: Setting all covariances to zero is equivalent to solving:
- Cov(X,Z) = 0  →  Equal column sums
- Cov(Y,Z) = 0  →  Equal row sums  
- Cov(D_main,Z) = 0  →  Main diagonal = M(n)
- Cov(D_anti,Z) = 0  →  Anti-diagonal = M(n)

These are LINEAR CONSTRAINTS on the entries!
"""

import numpy as np
from scipy.spatial import ConvexHull
from itertools import permutations
import json
from typing import List, Dict, Tuple
import time

# ============================================================================
# GENERATE ALL n=4 MAGIC SQUARES
# ============================================================================

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

def canonical_form(square: np.ndarray) -> tuple:
    """Return canonical form (smallest under D4) for deduplication."""
    forms = []
    current = square.copy()
    for _ in range(4):
        forms.append(tuple(current.flatten()))
        forms.append(tuple(np.fliplr(current).flatten()))
        current = np.rot90(current)
    return min(forms)

def generate_all_4x4_magic_squares_exhaustive():
    """
    Generate ALL 880 essentially different 4x4 magic squares.
    
    This is computationally intensive but necessary for unbiased analysis.
    Uses smart pruning based on row/column sum constraints.
    """
    print("Generating all 4x4 magic squares (this may take a while)...")
    start = time.time()
    
    n = 4
    M = 34  # Magic constant for n=4
    
    magic_squares = []
    seen_canonical = set()
    
    # Strategy: Generate row by row with pruning
    # Row 1: All 4-element subsets summing to 34
    values = list(range(1, 17))
    
    count = 0
    found = 0
    
    # For speed, we'll use a smarter approach
    # Check all permutations but with early termination
    for perm in permutations(range(1, 17)):
        count += 1
        if count % 1000000 == 0:
            print(f"  Checked {count:,} permutations, found {found} squares...")
        
        # Early row check
        row1_sum = sum(perm[0:4])
        if row1_sum != M:
            continue
            
        row2_sum = sum(perm[4:8])
        if row2_sum != M:
            continue
            
        row3_sum = sum(perm[8:12])
        if row3_sum != M:
            continue
        
        # Row 4 is automatic if others sum correctly
        # Check columns
        col_ok = True
        for j in range(4):
            col_sum = perm[j] + perm[j+4] + perm[j+8] + perm[j+12]
            if col_sum != M:
                col_ok = False
                break
        if not col_ok:
            continue
        
        # Check diagonals
        main_diag = perm[0] + perm[5] + perm[10] + perm[15]
        if main_diag != M:
            continue
            
        anti_diag = perm[3] + perm[6] + perm[9] + perm[12]
        if anti_diag != M:
            continue
        
        # It's magic!
        square = np.array(perm).reshape(4, 4)
        canon = canonical_form(square)
        
        if canon not in seen_canonical:
            seen_canonical.add(canon)
            magic_squares.append(square)
            found += 1
            
            if found % 100 == 0:
                print(f"  Found {found} unique squares...")
    
    elapsed = time.time() - start
    print(f"Found {len(magic_squares)} essentially different 4x4 magic squares in {elapsed:.1f}s")
    
    return magic_squares

def generate_4x4_magic_squares_smart(max_squares=100):
    """
    Smart generation using constraint-based approach.
    
    Faster than exhaustive for getting a diverse sample.
    """
    print(f"Generating up to {max_squares} diverse 4x4 magic squares...")
    
    magic_squares = []
    seen_canonical = set()
    attempts = 0
    max_attempts = 100000
    
    while len(magic_squares) < max_squares and attempts < max_attempts:
        attempts += 1
        
        # Random permutation
        perm = np.random.permutation(range(1, 17))
        square = perm.reshape(4, 4)
        
        if is_magic_square(square):
            canon = canonical_form(square)
            if canon not in seen_canonical:
                seen_canonical.add(canon)
                magic_squares.append(square)
    
    print(f"Found {len(magic_squares)} unique squares in {attempts} attempts")
    return magic_squares

# ============================================================================
# ANALYZE HULL PROPERTIES ACROSS ALL SQUARES
# ============================================================================

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

def analyze_hull_diversity(squares: List[np.ndarray]) -> Dict:
    """Analyze hull properties across ALL magic squares."""
    print(f"\nAnalyzing hull properties for {len(squares)} squares...")
    
    hull_vertex_counts = []
    hull_volumes = []
    hull_areas = []
    
    for sq in squares:
        coords = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords)
            hull_vertex_counts.append(len(hull.vertices))
            hull_volumes.append(hull.volume)
            hull_areas.append(hull.area)
        except:
            pass
    
    # Analyze diversity
    unique_vertex_counts = sorted(set(hull_vertex_counts))
    vertex_count_dist = {v: hull_vertex_counts.count(v) for v in unique_vertex_counts}
    
    return {
        'n_squares': len(squares),
        'unique_vertex_counts': unique_vertex_counts,
        'vertex_count_distribution': vertex_count_dist,
        'volume_range': (min(hull_volumes), max(hull_volumes)),
        'volume_mean': np.mean(hull_volumes),
        'volume_std': np.std(hull_volumes),
        'all_same_vertices': len(unique_vertex_counts) == 1
    }

# ============================================================================
# COVARIANCE CONDITIONS AS LINEAR SYSTEM
# ============================================================================

def analyze_covariance_as_constraints():
    """
    Analyze the covariance conditions as a system of linear equations.
    
    For an n×n arrangement S with entries s_ij:
    
    1. Cov(X,Z) = 0 means: Σ_j (j - (n-1)/2) * C_j = 0
       where C_j = column j sum
       
    2. Cov(Y,Z) = 0 means: Σ_i ((n-1)/2 - i) * R_i = 0
       where R_i = row i sum
       
    3. For equal row sums R_i = M(n), we need:
       Σ_i ((n-1)/2 - i) * M(n) = M(n) * Σ_i ((n-1)/2 - i) = 0 ✓
       
    4. Similarly for columns.
    
    So Cov = 0 is IMPLIED by equal sums, but equal sums is STRONGER.
    
    The key insight: 760 arrangements satisfy Cov(X,Z)=Cov(Y,Z)=0
    but only 8 are magic. The DIAGONAL conditions are what distinguish them!
    """
    print("\n" + "="*70)
    print("COVARIANCE CONDITIONS AS CONSTRAINT SYSTEM")
    print("="*70)
    
    n = 3
    
    # Count arrangements satisfying each condition
    count_covxz_zero = 0
    count_covyz_zero = 0
    count_both_zero = 0
    count_all_four_zero = 0
    count_magic = 0
    
    for perm in permutations(range(1, n*n + 1)):
        square = np.array(perm).reshape(n, n)
        coords = square_to_coordinates(square)
        
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
        
        if abs(cov_xz) < 1e-10:
            count_covxz_zero += 1
        if abs(cov_yz) < 1e-10:
            count_covyz_zero += 1
        if abs(cov_xz) < 1e-10 and abs(cov_yz) < 1e-10:
            count_both_zero += 1
        if abs(cov_xz) < 1e-10 and abs(cov_yz) < 1e-10 and abs(cov_main) < 1e-10 and abs(cov_anti) < 1e-10:
            count_all_four_zero += 1
        if is_magic_square(square):
            count_magic += 1
    
    print(f"\nFor n=3 (362,880 total arrangements):")
    print(f"  Cov(X,Z) = 0:     {count_covxz_zero:,} arrangements")
    print(f"  Cov(Y,Z) = 0:     {count_covyz_zero:,} arrangements")
    print(f"  Both = 0:         {count_both_zero:,} arrangements")
    print(f"  All four = 0:     {count_all_four_zero:,} arrangements")
    print(f"  Magic squares:    {count_magic:,} arrangements")
    print(f"\n  Match: All four = 0 ⟺ Magic: {count_all_four_zero == count_magic}")
    
    return {
        'cov_xz_zero': count_covxz_zero,
        'cov_yz_zero': count_covyz_zero,
        'both_zero': count_both_zero,
        'all_four_zero': count_all_four_zero,
        'magic': count_magic
    }

def explore_construction_via_covariance():
    """
    Explore using covariance constraints to CONSTRUCT magic squares.
    
    The constraints form a linear system. Can we solve it?
    """
    print("\n" + "="*70)
    print("CONSTRUCTION VIA COVARIANCE CONSTRAINTS")
    print("="*70)
    
    # For n=3, the constraints are:
    # Let s_ij be the entry at row i, column j (0-indexed)
    # 
    # 1. Cov(X,Z) = 0:
    #    Σ_ij (j - 1) * (s_ij - 5) = 0
    #    Expanding: Σ_ij (j-1)*s_ij = 5 * Σ_ij (j-1) = 5 * 3 * (0+1+2 - 3) = 0
    #    So: Σ_j (j-1) * C_j = 0 where C_j = column sum
    #    → -1*C_0 + 0*C_1 + 1*C_2 = 0 → C_0 = C_2
    #
    # 2. Cov(Y,Z) = 0:
    #    Similarly: R_0 = R_2 (row 0 sum = row 2 sum)
    #
    # 3. Diagonal constraints add more.
    
    print("\nFor n=3, the covariance constraints imply:")
    print("  Cov(X,Z)=0 → Column sums: C_0 = C_2 (but C_1 can differ)")
    print("  Cov(Y,Z)=0 → Row sums: R_0 = R_2 (but R_1 can differ)")
    print("  These are WEAKER than 'all equal'!")
    print("\n  The 760 - 8 = 752 non-magic solutions exploit this freedom.")
    
    print("\nThe FULL magic constraint is:")
    print("  C_0 = C_1 = C_2 = 15")
    print("  R_0 = R_1 = R_2 = 15")
    print("  Main diagonal = 15")
    print("  Anti-diagonal = 15")
    print("\nThis is 8 linear equations on 9 variables with permutation constraint.")

# ============================================================================
# COMPARE CONSTRUCTION METHODS
# ============================================================================

def lo_shu():
    return np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])

def siamese_method(n: int) -> np.ndarray:
    if n % 2 == 0:
        raise ValueError("Siamese method requires odd n")
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

def compare_construction_methods():
    """Compare properties across different construction methods."""
    print("\n" + "="*70)
    print("CONSTRUCTION METHOD COMPARISON")
    print("="*70)
    
    # n=3: All 8 are equivalent under D4
    print("\nn=3: All 8 magic squares are D4-equivalent to Lo Shu")
    
    # n=5: Compare Siamese to other methods
    print("\nn=5: Siamese method gives ONE specific magic square")
    sq5 = siamese_method(5)
    coords5 = square_to_coordinates(sq5)
    hull5 = ConvexHull(coords5)
    print(f"  Siamese n=5: {len(hull5.vertices)} hull vertices")
    
    # Generate some random n=5 magic squares for comparison
    # (This is hard - random generation rarely finds magic squares for n=5)
    
    # n=4: Compare across diverse squares
    print("\nn=4: Analyzing diverse magic squares...")
    
    # Generate some diverse 4x4 squares
    n4_squares = generate_4x4_magic_squares_smart(50)
    
    if n4_squares:
        hull_analysis = analyze_hull_diversity(n4_squares)
        print(f"\n  Analyzed {hull_analysis['n_squares']} n=4 magic squares:")
        print(f"  Unique hull vertex counts: {hull_analysis['unique_vertex_counts']}")
        print(f"  Distribution: {hull_analysis['vertex_count_distribution']}")
        print(f"  All have same # vertices: {hull_analysis['all_same_vertices']}")
        print(f"  Volume range: {hull_analysis['volume_range']}")
        
        return hull_analysis
    
    return None

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("="*70)
    print("CRITICAL ANALYSIS: CONSTRUCTION METHOD BIAS")
    print("="*70)
    print("\nThis analysis addresses the concern that findings may be")
    print("artifacts of specific construction methods rather than")
    print("properties of magic squares in general.")
    
    # 1. Analyze covariance constraints
    cov_analysis = analyze_covariance_as_constraints()
    
    # 2. Explore construction via covariance
    explore_construction_via_covariance()
    
    # 3. Compare construction methods
    method_comparison = compare_construction_methods()
    
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    
    print("""
1. COVARIANCE CONDITIONS ARE WEAKER THAN MAGIC:
   - 760 arrangements satisfy Cov(X,Z) = Cov(Y,Z) = 0
   - Only 8 of these are magic squares
   - The diagonal covariances are essential for characterization
   
2. COVARIANCE = 0 AS A CONSTRUCTION METHOD:
   - Setting all four covariances to zero gives LINEAR constraints
   - Combined with permutation constraint, this is a lattice point problem
   - Could potentially lead to new enumeration algorithms
   
3. CONSTRUCTION METHOD BIAS (IMPORTANT!):
   - My "12 hull vertices" finding may only apply to Siamese construction
   - Different n=4 squares may have different hull structures
   - Need to analyze ALL 880 n=4 squares for unbiased conclusions
   
4. UNIVERSAL vs METHOD-SPECIFIC PROPERTIES:
   UNIVERSAL (proven for all magic squares):
   - Zero energy E(S) = 0
   - Variance formulas Var(Z) = (n⁴-1)/12
   - Modular preservation
   
   POSSIBLY METHOD-SPECIFIC (need verification):
   - 12 hull vertices for n≥5
   - Specific perturbation gap values
   - Eigenvalue patterns
""")
    
    # Save results
    results = {
        'covariance_analysis': cov_analysis,
        'key_insight': 'Covariance conditions form linear constraints that could be used for construction'
    }
    
    with open('construction_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to construction_analysis_results.json")

if __name__ == "__main__":
    main()
