#!/usr/bin/env python3
"""
Testing whether extended covariance constraints characterize magic squares.

We found that Cov(X², Z) = 0 is also constant for magic squares.
Can we find a complete set of covariance constraints?
"""

import numpy as np
import json
from pathlib import Path
import random

def load_magic_squares():
    """Load the 880 unique magic squares."""
    json_path = Path(__file__).parent.parent / "web" / "assets" / "data" / "unique_squares.json"
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            return [np.array(sq).reshape(4, 4) for sq in data]
    raise FileNotFoundError("Could not find magic squares data file")

def compute_extended_covariances(M):
    """Compute an extended set of covariances."""
    M = np.array(M).reshape(4, 4)
    z = M.flatten()
    
    # Position coordinates
    x = np.array([[i for j in range(4)] for i in range(4)]).flatten()
    y = np.array([[j for j in range(4)] for i in range(4)]).flatten()
    
    # Center everything
    x_c = x - x.mean()
    y_c = y - y.mean()
    z_c = z - z.mean()
    
    # First-order covariances
    c1 = np.mean(x_c * z_c)  # Cov(X, Z)
    c2 = np.mean(y_c * z_c)  # Cov(Y, Z)
    
    # Second-order covariances  
    x2_c = (x**2) - np.mean(x**2)
    y2_c = (y**2) - np.mean(y**2)
    xy_c = (x*y) - np.mean(x*y)
    
    c_x2 = np.mean(x2_c * z_c)   # Cov(X², Z)
    c_y2 = np.mean(y2_c * z_c)   # Cov(Y², Z)
    c_xy = np.mean(xy_c * z_c)   # Cov(XY, Z)
    
    # Diagonal indicators
    main_diag_indicator = (x == y).astype(float)
    anti_diag_indicator = (x + y == 3).astype(float)
    
    main_diag_c = main_diag_indicator - main_diag_indicator.mean()
    anti_diag_c = anti_diag_indicator - anti_diag_indicator.mean()
    
    c_main_ind = np.mean(main_diag_c * z_c)  # Cov(1_{main diagonal}, Z)
    c_anti_ind = np.mean(anti_diag_c * z_c)  # Cov(1_{anti diagonal}, Z)
    
    return {
        'c1': c1, 
        'c2': c2, 
        'c_x2': c_x2, 
        'c_y2': c_y2, 
        'c_xy': c_xy,
        'c_main_ind': c_main_ind,
        'c_anti_ind': c_anti_ind
    }

def is_magic(M):
    """Check if M is a valid 4x4 magic square."""
    M = np.array(M).reshape(4, 4)
    target = 34
    return (all(M[i, :].sum() == target for i in range(4)) and
            all(M[:, j].sum() == target for j in range(4)) and
            np.trace(M) == target and
            np.trace(np.fliplr(M)) == target)

def main():
    print("=" * 70)
    print("EXTENDED COVARIANCE CONSTRAINTS")
    print("=" * 70)
    print()
    
    # Load magic squares
    magic_squares = load_magic_squares()
    print(f"Loaded {len(magic_squares)} magic squares")
    print()
    
    # Check what's constant across magic squares
    print("PART 1: Which extended covariances are CONSTANT for magic squares?")
    print("-" * 50)
    
    all_covs = [compute_extended_covariances(sq) for sq in magic_squares]
    
    for key in ['c1', 'c2', 'c_x2', 'c_y2', 'c_xy', 'c_main_ind', 'c_anti_ind']:
        values = [c[key] for c in all_covs]
        print(f"{key:15s}: mean = {np.mean(values):10.6f}, std = {np.std(values):10.6f}")
    
    print()
    print("Constraints that are CONSTANT (std ≈ 0) for magic squares:")
    constant_constraints = []
    for key in ['c1', 'c2', 'c_x2', 'c_y2', 'c_xy', 'c_main_ind', 'c_anti_ind']:
        values = [c[key] for c in all_covs]
        if np.std(values) < 0.001:
            constant_constraints.append((key, np.mean(values)))
            print(f"  {key} = {np.mean(values):.6f}")
    
    print()
    print(f"Found {len(constant_constraints)} constant covariance constraints!")
    print()
    
    # Now test if these constraints are SUFFICIENT
    print("=" * 70)
    print("PART 2: Are these constraints SUFFICIENT?")
    print("-" * 50)
    print()
    
    # Generate random permutations and check how many satisfy all constant constraints
    N_SAMPLES = 100000
    TOLERANCE = 0.001
    
    print(f"Testing {N_SAMPLES} random permutations...")
    print(f"Checking if they satisfy all {len(constant_constraints)} constraints (tol={TOLERANCE})")
    print()
    
    satisfies_all = []
    
    for i in range(N_SAMPLES):
        if i > 0 and i % 20000 == 0:
            print(f"  Checked {i} permutations, found {len(satisfies_all)} satisfying all constraints")
        
        # Generate random permutation
        perm = list(range(1, 17))
        random.shuffle(perm)
        M = np.array(perm).reshape(4, 4)
        
        covs = compute_extended_covariances(M)
        
        # Check if all constant constraints are satisfied
        all_satisfied = True
        for key, target_value in constant_constraints:
            if abs(covs[key] - target_value) > TOLERANCE:
                all_satisfied = False
                break
        
        if all_satisfied:
            magic = is_magic(M)
            satisfies_all.append((M.copy(), magic))
    
    print()
    print(f"Results: {len(satisfies_all)} permutations satisfy all constraints")
    
    if len(satisfies_all) > 0:
        n_magic = sum(1 for _, m in satisfies_all if m)
        n_non_magic = len(satisfies_all) - n_magic
        
        print(f"  Magic squares: {n_magic}")
        print(f"  Non-magic: {n_non_magic}")
        
        if n_non_magic > 0:
            print()
            print("COUNTEREXAMPLES (satisfy all constraints but not magic):")
            for M, magic in satisfies_all[:5]:
                if not magic:
                    covs = compute_extended_covariances(M)
                    print()
                    print(M)
                    print(f"Row sums: {M.sum(axis=1)}")
                    print(f"Col sums: {M.sum(axis=0)}")
                    print(f"Diag sums: {np.trace(M)}, {np.trace(np.fliplr(M))}")
                    for key, target in constant_constraints:
                        print(f"  {key} = {covs[key]:.6f} (target: {target:.6f})")
        else:
            print()
            print("NO COUNTEREXAMPLES FOUND!")
            print("The extended covariance constraints MAY be sufficient!")
    else:
        print("No permutations satisfied all constraints - that's suspicious.")
    
    print()
    print("=" * 70)
    print("PART 3: Understanding the constraint algebra")
    print("-" * 50)
    print()
    
    print("The covariances can be expressed in terms of sums:")
    print()
    print("Let Rᵢ = sum of row i, Cⱼ = sum of column j")
    print()
    print("c1 = Cov(X, Z) = 0")
    print("  → Σᵢ (i - μₓ) · Rᵢ = 0")
    print("  → This constrains the 'center of mass' of row sums")
    print()
    print("c_x2 = Cov(X², Z) = 0")  
    print("  → Σᵢ (i² - μ_{x²}) · Rᵢ = 0")
    print("  → This constrains the 'moment of inertia' of row sums")
    print()
    print("Together, c1=0 and c_x2=0 give 2 constraints on 4 row sums (R₀, R₁, R₂, R₃).")
    print("Combined with Σ Rᵢ = 136, we have 3 constraints on 4 variables.")
    print("But to force R₀ = R₁ = R₂ = R₃ = 34, we need 3 independent constraints.")
    print()
    print("So c1=0 + c_x2=0 + total_sum MAY be equivalent to equal row sums!")
    
    print()
    print("=" * 70)
    print("PART 4: Verify the algebra explicitly")
    print("-" * 50)
    print()
    
    # For 4x4 with row positions 0,1,2,3
    # c1 = 0 means: (-1.5)R₀ + (-0.5)R₁ + (0.5)R₂ + (1.5)R₃ = 0
    # c_x2 = 0 means: ...
    
    print("Row positions: 0, 1, 2, 3")
    print("Mean position μ = 1.5")
    print("Mean of squares μ_{x²} = (0 + 1 + 4 + 9)/4 = 3.5")
    print()
    print("c1 = 0 gives:")
    coeffs_c1 = np.array([-1.5, -0.5, 0.5, 1.5])
    print(f"  {coeffs_c1[0]:.1f}·R₀ + {coeffs_c1[1]:.1f}·R₁ + {coeffs_c1[2]:.1f}·R₂ + {coeffs_c1[3]:.1f}·R₃ = 0")
    
    print()
    print("c_x2 = 0 gives:")
    x_vals = np.array([0, 1, 2, 3])
    x2_vals = x_vals ** 2
    mu_x2 = x2_vals.mean()
    coeffs_cx2 = x2_vals - mu_x2  # (i² - μ_{x²}) for each row
    print(f"  {coeffs_cx2[0]:.1f}·R₀ + {coeffs_cx2[1]:.1f}·R₁ + {coeffs_cx2[2]:.1f}·R₂ + {coeffs_cx2[3]:.1f}·R₃ = 0")
    
    print()
    print("Total sum constraint:")
    print("  1·R₀ + 1·R₁ + 1·R₂ + 1·R₃ = 136")
    
    print()
    print("Constraint matrix A (rows are constraints, cols are R₀,R₁,R₂,R₃):")
    A = np.array([
        coeffs_c1,
        coeffs_cx2,
        [1, 1, 1, 1]
    ])
    print(A)
    print(f"Rank of A: {np.linalg.matrix_rank(A)}")
    
    print()
    print("If rank = 3, then we can solve for row sums uniquely!")

if __name__ == "__main__":
    main()

