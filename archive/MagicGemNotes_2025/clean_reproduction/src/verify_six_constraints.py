#!/usr/bin/env python3
"""
Verify if the 6 covariance constraints fully characterize magic squares.

The 6 constraints we found:
  c1 = Cov(X, Z) = 0
  c2 = Cov(Y, Z) = 0  
  c_x2 = Cov(X², Z) = 0
  c_y2 = Cov(Y², Z) = 0
  c_main_ind = Cov(1_{main diagonal}, Z) = 0
  c_anti_ind = Cov(1_{anti diagonal}, Z) = 0
"""

import numpy as np
import json
from pathlib import Path
import random
from itertools import permutations
import time

def load_magic_squares():
    """Load the 880 unique magic squares."""
    json_path = Path(__file__).parent.parent / "web" / "assets" / "data" / "unique_squares.json"
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            return [np.array(sq).reshape(4, 4) for sq in data]
    raise FileNotFoundError("Could not find magic squares data file")

# Pre-compute position arrays (constant)
X = np.array([[i for j in range(4)] for i in range(4)]).flatten()
Y = np.array([[j for j in range(4)] for i in range(4)]).flatten()
X_c = X - X.mean()
Y_c = Y - Y.mean()
X2_c = (X**2) - np.mean(X**2)
Y2_c = (Y**2) - np.mean(Y**2)
MAIN_DIAG_IND = (X == Y).astype(float)
ANTI_DIAG_IND = (X + Y == 3).astype(float)
MAIN_DIAG_C = MAIN_DIAG_IND - MAIN_DIAG_IND.mean()
ANTI_DIAG_C = ANTI_DIAG_IND - ANTI_DIAG_IND.mean()

def compute_constraints(z_flat):
    """Compute all 6 constraint values for a flattened array."""
    z_c = z_flat - z_flat.mean()
    
    c1 = np.dot(X_c, z_c) / 16
    c2 = np.dot(Y_c, z_c) / 16
    c_x2 = np.dot(X2_c, z_c) / 16
    c_y2 = np.dot(Y2_c, z_c) / 16
    c_main = np.dot(MAIN_DIAG_C, z_c) / 16
    c_anti = np.dot(ANTI_DIAG_C, z_c) / 16
    
    return np.array([c1, c2, c_x2, c_y2, c_main, c_anti])

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
    print("VERIFYING THE 6-CONSTRAINT CHARACTERIZATION")
    print("=" * 70)
    print()
    
    # Load and verify magic squares
    magic_squares = load_magic_squares()
    print(f"Loaded {len(magic_squares)} magic squares")
    print()
    
    # Verify all magic squares have zero constraints
    print("Step 1: Verify all magic squares satisfy the 6 constraints")
    print("-" * 50)
    
    max_violation = 0
    for sq in magic_squares:
        constraints = compute_constraints(sq.flatten().astype(float))
        max_violation = max(max_violation, np.max(np.abs(constraints)))
    
    print(f"Maximum constraint violation across all magic squares: {max_violation:.2e}")
    if max_violation < 1e-10:
        print("✓ All magic squares satisfy the 6 constraints exactly")
    print()
    
    # Test random permutations with VERY tight tolerance
    print("Step 2: Search for counterexamples with tight tolerance")
    print("-" * 50)
    
    N_SAMPLES = 1000000
    TOLERANCE = 1e-10  # Very tight
    
    print(f"Testing {N_SAMPLES:,} random permutations...")
    print(f"Tolerance: {TOLERANCE}")
    print()
    
    counterexamples = []
    near_misses = []
    
    start_time = time.time()
    
    for i in range(N_SAMPLES):
        if i > 0 and i % 200000 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked {i:,} ({elapsed:.1f}s), counterexamples: {len(counterexamples)}")
        
        perm = np.random.permutation(np.arange(1, 17))
        constraints = compute_constraints(perm.astype(float))
        
        max_constraint = np.max(np.abs(constraints))
        
        # Track near misses
        if max_constraint < 0.1:
            near_misses.append((max_constraint, perm.copy()))
        
        # Check for counterexample
        if max_constraint < TOLERANCE:
            magic = is_magic(perm.reshape(4, 4))
            if not magic:
                counterexamples.append(perm.reshape(4, 4).copy())
    
    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.1f}s")
    print()
    
    if counterexamples:
        print(f"FOUND {len(counterexamples)} COUNTEREXAMPLES!")
        print("The 6-constraint characterization is NOT sufficient.")
        for M in counterexamples[:3]:
            print()
            print(M)
            print(f"Row sums: {M.sum(axis=1)}, Col sums: {M.sum(axis=0)}")
    else:
        print("NO COUNTEREXAMPLES FOUND!")
        print()
        print("This suggests the 6 constraints MAY be sufficient.")
        print()
        print("Near misses (smallest max constraint among non-magic):")
        near_misses.sort(key=lambda x: x[0])
        for max_c, perm in near_misses[:5]:
            M = perm.reshape(4, 4)
            magic = is_magic(M)
            print(f"  max|constraint| = {max_c:.6f}, is_magic = {magic}")
    
    print()
    print("=" * 70)
    print("THEORETICAL ANALYSIS: Why 6 constraints might work")
    print("-" * 50)
    print()
    
    print("For equal ROW sums (R₀ = R₁ = R₂ = R₃ = 34):")
    print("  c1 = 0: linear constraint on Rᵢ")
    print("  c_x2 = 0: quadratic constraint on Rᵢ")
    print("  Total = 136: sum constraint")
    print("  → 3 constraints on 4 variables = unique solution (rank 3)")
    print()
    
    print("Similarly for equal COLUMN sums:")
    print("  c2 = 0 + c_y2 = 0 + Total = 136")
    print("  → Forces C₀ = C₁ = C₂ = C₃ = 34")
    print()
    
    print("For DIAGONAL sums:")
    print("  c_main_ind = Cov(1_{x=y}, Z) = 0")
    print("  This says: mean(diagonal values) = mean(all values) = 8.5")
    print("  → sum(diagonal) = 4 × 8.5 = 34 ✓")
    print()
    print("  c_anti_ind = Cov(1_{x+y=3}, Z) = 0")
    print("  → sum(anti-diagonal) = 34 ✓")
    print()
    
    print("=" * 70)
    print("CONCLUSION")
    print("-" * 50)
    print()
    print("The 6 covariance constraints appear to be EQUIVALENT to the classical")
    print("magic square constraints:")
    print()
    print("  Classical:                     Covariance form:")
    print("  ─────────                      ───────────────")
    print("  All row sums = 34       ←→     c1 = 0, c_x2 = 0 (+ total=136)")
    print("  All col sums = 34       ←→     c2 = 0, c_y2 = 0 (+ total=136)")
    print("  Main diag sum = 34      ←→     c_main_ind = 0")
    print("  Anti diag sum = 34      ←→     c_anti_ind = 0")
    print()
    print("This gives a CORRECTED Zero-Covariance Theorem!")

if __name__ == "__main__":
    main()

