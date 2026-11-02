#!/usr/bin/env python3
"""
Investigating the covariance structure more carefully.

The user raises a key point: with 3 dimensions (X, Y, Z), why do we only 
have 2 independent covariance constraints?

Let's examine:
1. What covariances are possible?
2. Are the diagonal covariances truly linearly dependent?
3. What would make them independent?
"""

import numpy as np

def analyze_covariance_structure():
    """Analyze the linear algebra of the covariance constraints."""
    
    print("=" * 70)
    print("ANALYSIS OF COVARIANCE CONSTRAINT STRUCTURE")
    print("=" * 70)
    print()
    
    # Grid positions (0-indexed)
    positions = [(i, j) for i in range(4) for j in range(4)]
    x = np.array([p[0] for p in positions])  # row indices
    y = np.array([p[1] for p in positions])  # col indices
    
    # Center the positions
    x_c = x - x.mean()
    y_c = y - y.mean()
    
    print("PART 1: The Standard Covariance Formulation")
    print("-" * 50)
    print()
    print("Given an arrangement M, we embed as points (i, j, M[i,j]).")
    print("The covariances are computed as:")
    print()
    print("  c₁ = Cov(X, Z) = (1/16) Σᵢⱼ (i - μₓ)(M[i,j] - μ_z)")
    print("  c₂ = Cov(Y, Z) = (1/16) Σᵢⱼ (j - μᵧ)(M[i,j] - μ_z)")
    print()
    
    # The key observation
    print("For the 'diagonal' covariances:")
    print()
    print("  c₃ = Cov(X+Y, Z) = Cov(X,Z) + Cov(Y,Z) = c₁ + c₂")
    print("  c₄ = Cov(X-Y, Z) = Cov(X,Z) - Cov(Y,Z) = c₁ - c₂")
    print()
    print("This follows from BILINEARITY of covariance:")
    print("  Cov(aX + bY, Z) = a·Cov(X,Z) + b·Cov(Y,Z)")
    print()
    print("Therefore: {c₃=0, c₄=0} ⟺ {c₁=0, c₂=0}")
    print("The diagonal constraints add NO new information!")
    print()
    
    print("=" * 70)
    print("PART 2: Why the 'Four Conditions' Collapse to Two")
    print("-" * 50)
    print()
    
    print("The classical magic square constraints are:")
    print("  - 4 row sums = 34    (3 independent)")
    print("  - 4 column sums = 34 (3 independent)")
    print("  - Main diagonal = 34 (1 independent)")
    print("  - Anti-diagonal = 34 (1 independent)")
    print("  Total: ~8 independent constraints")
    print()
    print("But c₁ = c₂ = 0 gives only TWO linear constraints!")
    print()
    print("What does Cov(X, Z) = 0 actually constrain?")
    print()
    
    # Show what c1 = 0 means
    print("Let Rᵢ = sum of row i. Then:")
    print("  Cov(X, Z) = 0  ⟹  Σᵢ (i - 1.5) · Rᵢ = 0")
    print("  i.e., -1.5·R₀ - 0.5·R₁ + 0.5·R₂ + 1.5·R₃ = 0")
    print()
    print("This is ONE linear constraint on (R₀, R₁, R₂, R₃), not three!")
    print("It says the 'center of mass' of row sums is at the grid center.")
    print()
    print("Similarly, Cov(Y, Z) = 0 gives ONE constraint on column sums.")
    print()
    print("Two constraints cannot characterize an 8-constraint object!")
    print()
    
    print("=" * 70)
    print("PART 3: Could Different Diagonal Constraints Be Independent?")
    print("-" * 50)
    print()
    
    print("The issue is that Cov(X+Y, Z) is computed over ALL 16 cells,")
    print("but the diagonal sum constraint only involves 4 cells.")
    print()
    print("What if we defined RESTRICTED diagonal covariances?")
    print()
    
    # Main diagonal cells
    main_diag_indices = [0, 5, 10, 15]  # (0,0), (1,1), (2,2), (3,3)
    anti_diag_indices = [3, 6, 9, 12]   # (0,3), (1,2), (2,1), (3,0)
    
    print("Main diagonal cells: (0,0), (1,1), (2,2), (3,3)")
    print("Anti-diagonal cells: (0,3), (1,2), (2,1), (3,0)")
    print()
    
    # Position along main diagonal: d = i = j (since i=j on diagonal)
    main_diag_pos = np.array([0, 1, 2, 3])
    anti_diag_pos = np.array([0, 1, 2, 3])  # distance from top-right corner
    
    print("Define diagonal-specific constraints:")
    print()
    print("  c_main = Cov_restricted(d, M[d,d]) over d ∈ {0,1,2,3}")
    print("  c_anti = Cov_restricted(d, M[d,3-d]) over d ∈ {0,1,2,3}")
    print()
    print("These involve ONLY 4 cells each, not all 16!")
    print()
    print("Would these be independent of c₁ and c₂?")
    print()
    
    # Let's check with a specific example
    # Dürer's magic square
    durer = np.array([[16, 3, 2, 13],
                      [5, 10, 11, 8],
                      [9, 6, 7, 12],
                      [4, 15, 14, 1]])
    
    z = durer.flatten()
    z_c = z - z.mean()
    
    # Standard covariances
    c1 = np.mean(x_c * z_c)
    c2 = np.mean(y_c * z_c)
    
    # Main diagonal values
    main_vals = np.array([durer[i,i] for i in range(4)])
    main_pos_c = main_diag_pos - main_diag_pos.mean()
    main_vals_c = main_vals - main_vals.mean()
    c_main = np.mean(main_pos_c * main_vals_c)
    
    # Anti-diagonal values
    anti_vals = np.array([durer[i, 3-i] for i in range(4)])
    anti_pos_c = anti_diag_pos - anti_diag_pos.mean()
    anti_vals_c = anti_vals - anti_vals.mean()
    c_anti = np.mean(anti_pos_c * anti_vals_c)
    
    print("For Dürer's magic square:")
    print(f"  c₁ = Cov(X, Z) = {c1:.6f}")
    print(f"  c₂ = Cov(Y, Z) = {c2:.6f}")
    print(f"  c_main (restricted) = {c_main:.6f}")
    print(f"  c_anti (restricted) = {c_anti:.6f}")
    print()
    
    print("=" * 70)
    print("PART 4: Testing Restricted Diagonal Covariances on Counterexamples")
    print("-" * 50)
    print()
    
    # A counterexample from our earlier run
    counter = np.array([[ 7, 15, 13,  5],
                        [10,  3,  4,  6],
                        [ 8, 16, 12,  2],
                        [ 1,  9, 11, 14]])
    
    z_counter = counter.flatten()
    z_counter_c = z_counter - z_counter.mean()
    
    c1_counter = np.mean(x_c * z_counter_c)
    c2_counter = np.mean(y_c * z_counter_c)
    
    main_vals_counter = np.array([counter[i,i] for i in range(4)])
    main_vals_counter_c = main_vals_counter - main_vals_counter.mean()
    c_main_counter = np.mean(main_pos_c * main_vals_counter_c)
    
    anti_vals_counter = np.array([counter[i, 3-i] for i in range(4)])
    anti_vals_counter_c = anti_vals_counter - anti_vals_counter.mean()
    c_anti_counter = np.mean(anti_pos_c * anti_vals_counter_c)
    
    print("For counterexample (c₁=c₂=0 but NOT magic):")
    print(counter)
    print()
    print(f"  c₁ = Cov(X, Z) = {c1_counter:.6f}")
    print(f"  c₂ = Cov(Y, Z) = {c2_counter:.6f}")
    print(f"  c_main (restricted) = {c_main_counter:.6f}")
    print(f"  c_anti (restricted) = {c_anti_counter:.6f}")
    print()
    
    print("Row sums:", counter.sum(axis=1))
    print("Col sums:", counter.sum(axis=0))
    print("Main diag sum:", np.trace(counter))
    print("Anti diag sum:", np.trace(np.fliplr(counter)))
    print()
    
    if abs(c_main_counter) > 0.01 or abs(c_anti_counter) > 0.01:
        print("✓ The RESTRICTED diagonal covariances ARE non-zero!")
        print("  They could provide ADDITIONAL independent constraints!")
    else:
        print("✗ The restricted diagonal covariances are also zero.")
    
    print()
    print("=" * 70)
    print("CONCLUSION")
    print("-" * 50)
    print()
    print("The paper's formulation has a fundamental problem:")
    print()
    print("1. Cov(X+Y, Z) computed over all 16 cells is linearly dependent")
    print("   on Cov(X, Z) and Cov(Y, Z).")
    print()
    print("2. To get independent diagonal constraints, we might need to compute")
    print("   covariances RESTRICTED to the 4 diagonal cells only.")
    print()
    print("3. This would give a different theorem with potentially 4 independent")
    print("   constraints, but still only 4, not the ~8 needed for full magic.")
    print()
    print("The zero-covariance characterization, however formulated, may not be")
    print("SUFFICIENT for magic squares. But it remains an interesting NECESSARY")
    print("condition worth studying.")

if __name__ == "__main__":
    analyze_covariance_structure()

