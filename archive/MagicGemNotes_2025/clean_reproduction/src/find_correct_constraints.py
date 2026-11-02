#!/usr/bin/env python3
"""
Finding the CORRECT covariance formulation for magic squares.

Key insight from user: With 3D embedding (X, Y, Z), shouldn't we have 
more independent constraints?

Let's explore what constraints ACTUALLY characterize magic squares.
"""

import numpy as np
import json
from pathlib import Path

def load_magic_squares():
    """Load the 880 unique magic squares."""
    json_path = Path(__file__).parent.parent / "web" / "assets" / "data" / "unique_squares.json"
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                return [np.array(sq).reshape(4, 4) for sq in data]
    raise FileNotFoundError("Could not find magic squares data file")

def compute_all_covariances(M):
    """Compute various covariance measures for a 4x4 matrix."""
    M = np.array(M).reshape(4, 4)
    
    # Create coordinate arrays
    x = np.array([[i for j in range(4)] for i in range(4)]).flatten()
    y = np.array([[j for j in range(4)] for i in range(4)]).flatten()
    z = M.flatten()
    
    # Center everything
    x_c = x - x.mean()
    y_c = y - y.mean()
    z_c = z - z.mean()
    
    # Standard covariances (over all 16 cells)
    c1 = np.mean(x_c * z_c)  # Cov(X, Z)
    c2 = np.mean(y_c * z_c)  # Cov(Y, Z)
    c3 = c1 + c2  # Cov(X+Y, Z) - linearly dependent!
    c4 = c1 - c2  # Cov(X-Y, Z) - linearly dependent!
    
    # Restricted diagonal covariances (over 4 cells only)
    main_diag = np.array([M[i,i] for i in range(4)])
    anti_diag = np.array([M[i, 3-i] for i in range(4)])
    pos = np.array([0, 1, 2, 3])
    pos_c = pos - pos.mean()
    
    c_main_restricted = np.mean(pos_c * (main_diag - main_diag.mean()))
    c_anti_restricted = np.mean(pos_c * (anti_diag - anti_diag.mean()))
    
    # What about row-wise covariances?
    # For each row, Cov(column_position, value_in_row)
    row_covs = []
    for i in range(4):
        row_vals = M[i, :]
        col_pos = np.array([0, 1, 2, 3])
        row_cov = np.mean((col_pos - col_pos.mean()) * (row_vals - row_vals.mean()))
        row_covs.append(row_cov)
    
    # For each column, Cov(row_position, value_in_column)
    col_covs = []
    for j in range(4):
        col_vals = M[:, j]
        row_pos = np.array([0, 1, 2, 3])
        col_cov = np.mean((row_pos - row_pos.mean()) * (col_vals - col_vals.mean()))
        col_covs.append(col_cov)
    
    return {
        'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4,
        'c_main_restricted': c_main_restricted,
        'c_anti_restricted': c_anti_restricted,
        'row_covs': row_covs,
        'col_covs': col_covs,
        'main_diag_sum': np.trace(M),
        'anti_diag_sum': np.trace(np.fliplr(M)),
        'row_sums': M.sum(axis=1).tolist(),
        'col_sums': M.sum(axis=0).tolist()
    }

def is_magic(M):
    """Check if M is a valid 4x4 magic square."""
    M = np.array(M).reshape(4, 4)
    target = 34
    rows_ok = all(M[i, :].sum() == target for i in range(4))
    cols_ok = all(M[:, j].sum() == target for j in range(4))
    main_ok = np.trace(M) == target
    anti_ok = np.trace(np.fliplr(M)) == target
    return rows_ok and cols_ok and main_ok and anti_ok

def main():
    print("=" * 70)
    print("FINDING THE CORRECT CONSTRAINT FORMULATION")
    print("=" * 70)
    print()
    
    # Load magic squares
    magic_squares = load_magic_squares()
    print(f"Loaded {len(magic_squares)} magic squares")
    print()
    
    # Analyze all magic squares
    print("PART 1: What's CONSTANT across all magic squares?")
    print("-" * 50)
    
    all_covs = [compute_all_covariances(sq) for sq in magic_squares]
    
    # Check which quantities are constant
    quantities = ['c1', 'c2', 'c3', 'c4', 'c_main_restricted', 'c_anti_restricted',
                  'main_diag_sum', 'anti_diag_sum']
    
    for q in quantities:
        values = [c[q] for c in all_covs]
        print(f"{q:25s}: mean = {np.mean(values):10.4f}, std = {np.std(values):10.4f}")
    
    print()
    print("Row covariance statistics:")
    for i in range(4):
        row_i_covs = [c['row_covs'][i] for c in all_covs]
        print(f"  Row {i} Cov: mean = {np.mean(row_i_covs):10.4f}, std = {np.std(row_i_covs):10.4f}")
    
    print()
    print("Column covariance statistics:")
    for j in range(4):
        col_j_covs = [c['col_covs'][j] for c in all_covs]
        print(f"  Col {j} Cov: mean = {np.mean(col_j_covs):10.4f}, std = {np.std(col_j_covs):10.4f}")
    
    print()
    print("=" * 70)
    print("PART 2: Exploring the GLOBAL vs RESTRICTED covariances")
    print("-" * 50)
    print()
    
    # Dürer's square
    durer = np.array([[16, 3, 2, 13],
                      [5, 10, 11, 8],
                      [9, 6, 7, 12],
                      [4, 15, 14, 1]])
    
    durer_covs = compute_all_covariances(durer)
    print("Dürer's magic square:")
    print(durer)
    print()
    print(f"  c1 (global) = {durer_covs['c1']:.4f}")
    print(f"  c2 (global) = {durer_covs['c2']:.4f}")
    print(f"  c_main_restricted = {durer_covs['c_main_restricted']:.4f}")
    print(f"  c_anti_restricted = {durer_covs['c_anti_restricted']:.4f}")
    print(f"  Main diagonal: {[durer[i,i] for i in range(4)]} = {durer_covs['main_diag_sum']}")
    print(f"  Anti diagonal: {[durer[i,3-i] for i in range(4)]} = {durer_covs['anti_diag_sum']}")
    
    print()
    print("Key observation: c_main_restricted and c_anti_restricted are NOT zero")
    print("for magic squares! So they capture something different.")
    print()
    
    print("=" * 70)
    print("PART 3: What ARE the correct covariance constraints?")
    print("-" * 50)
    print()
    
    # The actual magic constraints as covariances
    print("Reframing classical constraints as covariances:")
    print()
    print("1. ALL rows sum to 34")
    print("   This is EQUIVALENT to: Cov(indicator(row=i), Z) = constant for all i")
    print("   Or more simply: the means of each row are equal")
    print()
    print("2. ALL columns sum to 34")
    print("   Similarly: the means of each column are equal")
    print()
    print("3. The GLOBAL covariances c1=c2=0 are WEAKER:")
    print("   They only say the WEIGHTED AVERAGE of row/column sums is balanced.")
    print()
    
    # Let's verify this
    print("=" * 70)
    print("PART 4: The dimension count problem")
    print("-" * 50)
    print()
    
    print("Classical magic constraints (for n=4):")
    print("  - 4 row sums = 34, but total sum is fixed, so 3 independent")
    print("  - 4 col sums = 34, but total sum is fixed, so 3 independent")  
    print("  - Main diagonal = 34 (1 constraint)")
    print("  - Anti diagonal = 34 (1 constraint)")
    print("  Total: 3 + 3 + 1 + 1 = 8 independent linear constraints")
    print()
    print("The permutation space has 15 degrees of freedom")
    print("  (16 values, but their assignment is fixed up to permutation)")
    print()
    print("With 8 constraints, we expect a ~7-dimensional solution space?")
    print("But we only have 880 solutions, so they must be isolated points.")
    print()
    
    print("Covariance constraints (paper's formulation):")
    print("  - c1 = 0: 1 constraint")
    print("  - c2 = 0: 1 constraint")
    print("  - c3 = c1 + c2 = 0: NOT independent")
    print("  - c4 = c1 - c2 = 0: NOT independent")
    print("  Total: 2 independent constraints")
    print()
    print("This cannot characterize an 8-constraint object!")
    print()
    
    print("=" * 70)
    print("PART 5: A potential fix - the FULL constraint set")
    print("-" * 50)
    print()
    
    print("To properly characterize magic squares via covariances, we need")
    print("covariances that are EQUIVALENT to the classical constraints.")
    print()
    print("Possible formulation:")
    print("  c1 = Cov(X, Z) = 0")
    print("  c2 = Cov(Y, Z) = 0")
    print("  c3' = Cov(X², Z) = 0  (captures variance of row sums)")
    print("  c4' = Cov(Y², Z) = 0  (captures variance of col sums)")
    print("  c5 = Diagonal-specific constraint")
    print("  c6 = Anti-diagonal constraint")
    print()
    
    # Check if Cov(X^2, Z) = 0 for magic squares
    print("Checking Cov(X², Z) for magic squares:")
    x = np.array([[i for j in range(4)] for i in range(4)]).flatten()
    x2 = x**2
    x2_c = x2 - x2.mean()
    
    cov_x2_values = []
    for sq in magic_squares[:20]:  # Sample
        z = sq.flatten()
        z_c = z - z.mean()
        cov_x2 = np.mean(x2_c * z_c)
        cov_x2_values.append(cov_x2)
    
    print(f"  Mean: {np.mean(cov_x2_values):.4f}")
    print(f"  Std:  {np.std(cov_x2_values):.4f}")
    print()
    
    if np.std(cov_x2_values) < 0.01:
        print("  Cov(X², Z) is approximately constant for magic squares!")
    else:
        print("  Cov(X², Z) varies across magic squares.")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("-" * 50)
    print()
    print("1. The paper's 'four covariance conditions' collapse to TWO.")
    print()
    print("2. These two conditions (c1=c2=0) are NECESSARY but not SUFFICIENT.")
    print()
    print("3. To fully characterize magic squares via covariances, we would need")
    print("   a richer set of constraints (higher moments, restricted covariances,")
    print("   or row/column-specific conditions).")
    print()
    print("4. The paper's theorem should be restated as a NECESSARY condition.")
    print()
    print("5. The geometric insight (magic squares have balanced 'center of mass')")
    print("   remains valid and interesting, just not a full characterization.")

if __name__ == "__main__":
    main()

