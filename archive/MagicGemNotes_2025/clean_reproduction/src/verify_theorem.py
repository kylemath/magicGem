#!/usr/bin/env python3
"""
Verification script for the Zero-Covariance Theorem.

This script tests whether the theorem as stated is actually TRUE:
- Does c1=c2=0 characterize magic squares among all permutations of {1,...,16}?

Key questions:
1. Do all 880 magic squares have c1=c2=0? (Forward direction)
2. Is there ANY non-magic permutation with c1=c2=0? (Reverse direction - critical!)

If we find a non-magic permutation with c1=c2=0, the theorem is FALSE.
If we can show no such permutation exists, the theorem is TRUE for n=4.
"""

import numpy as np
import json
import random
from pathlib import Path
import time

def compute_covariances(M):
    """
    Compute the four covariances for a 4x4 arrangement.
    
    Returns c1, c2, c3, c4 where:
    - c1 = Cov(X, Z) (row position vs value)
    - c2 = Cov(Y, Z) (column position vs value)
    - c3 = Cov(X+Y, Z) = c1 + c2
    - c4 = Cov(X-Y, Z) = c1 - c2
    
    Note: c3 and c4 are linearly dependent on c1 and c2!
    """
    M = np.array(M).reshape(4, 4)
    
    # Create coordinate arrays
    x = np.array([[i for j in range(4)] for i in range(4)]).flatten()  # row indices
    y = np.array([[j for j in range(4)] for i in range(4)]).flatten()  # col indices
    z = M.flatten()  # values
    
    # Center everything
    x_c = x - x.mean()
    y_c = y - y.mean()
    z_c = z - z.mean()
    
    # Compute covariances (using definition: E[XZ] - E[X]E[Z], with centered vars this is E[X_c * Z_c])
    c1 = np.mean(x_c * z_c)  # Cov(X, Z)
    c2 = np.mean(y_c * z_c)  # Cov(Y, Z)
    c3 = c1 + c2              # Cov(X+Y, Z) by linearity
    c4 = c1 - c2              # Cov(X-Y, Z) by linearity
    
    return c1, c2, c3, c4

def is_magic(M):
    """Check if M is a valid 4x4 magic square."""
    M = np.array(M).reshape(4, 4)
    target = 34  # Magic constant for 4x4
    
    # Check rows
    for i in range(4):
        if M[i, :].sum() != target:
            return False
    
    # Check columns
    for j in range(4):
        if M[:, j].sum() != target:
            return False
    
    # Check main diagonal
    if np.trace(M) != target:
        return False
    
    # Check anti-diagonal
    if np.trace(np.fliplr(M)) != target:
        return False
    
    return True

def load_magic_squares():
    """Load the 880 unique magic squares."""
    # Try to load from JSON first
    json_path = Path(__file__).parent.parent / "web" / "assets" / "data" / "unique_squares.json"
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                return [np.array(sq).reshape(4, 4) for sq in data]
    
    # Otherwise try CSV
    csv_path = Path(__file__).parent.parent / "data" / "all7040CategoriesData.csv"
    if csv_path.exists():
        import pandas as pd
        df = pd.read_csv(csv_path)
        squares = []
        # Get unique squares (columns 0-15 are the values, column 16 is category)
        value_cols = [f'v{i}' if f'v{i}' in df.columns else df.columns[i] for i in range(16)]
        seen = set()
        for _, row in df.iterrows():
            sq = tuple(int(row[c]) for c in value_cols)
            if sq not in seen:
                seen.add(sq)
                squares.append(np.array(sq).reshape(4, 4))
        return squares[:880]  # First 880 unique
    
    raise FileNotFoundError("Could not find magic squares data file")

def generate_random_permutation():
    """Generate a random permutation of {1,...,16}."""
    perm = list(range(1, 17))
    random.shuffle(perm)
    return np.array(perm).reshape(4, 4)

def main():
    print("=" * 60)
    print("ZERO-COVARIANCE THEOREM VERIFICATION")
    print("=" * 60)
    print()
    
    # Step 1: Verify forward direction for all magic squares
    print("STEP 1: Verify all magic squares have c1=c2=0")
    print("-" * 40)
    
    try:
        magic_squares = load_magic_squares()
        print(f"Loaded {len(magic_squares)} magic squares")
    except Exception as e:
        print(f"Could not load magic squares: {e}")
        print("Using a sample magic square for demonstration...")
        # Dürer's magic square
        magic_squares = [np.array([[16, 3, 2, 13],
                                   [5, 10, 11, 8],
                                   [9, 6, 7, 12],
                                   [4, 15, 14, 1]])]
    
    max_c1, max_c2 = 0, 0
    for i, sq in enumerate(magic_squares):
        c1, c2, c3, c4 = compute_covariances(sq)
        max_c1 = max(max_c1, abs(c1))
        max_c2 = max(max_c2, abs(c2))
        
        # Verify it's actually magic
        if not is_magic(sq):
            print(f"ERROR: Square {i} is not magic!")
        
        # Check c1, c2 are zero (within floating point tolerance)
        if abs(c1) > 1e-10 or abs(c2) > 1e-10:
            print(f"ERROR: Magic square {i} has non-zero covariance!")
            print(f"  c1 = {c1}, c2 = {c2}")
    
    print(f"Maximum |c1| across all magic squares: {max_c1:.2e}")
    print(f"Maximum |c2| across all magic squares: {max_c2:.2e}")
    
    if max_c1 < 1e-10 and max_c2 < 1e-10:
        print("✓ FORWARD DIRECTION VERIFIED: All magic squares have c1=c2=0")
    else:
        print("✗ FORWARD DIRECTION FAILED!")
    print()
    
    # Step 2: Search for non-magic permutations with c1=c2=0
    print("STEP 2: Search for counterexamples (non-magic with c1=c2≈0)")
    print("-" * 40)
    
    TOLERANCE = 0.01  # How close to zero counts as "approximately zero"
    N_SAMPLES = 1000000  # Number of random permutations to check
    
    print(f"Testing {N_SAMPLES:,} random permutations...")
    print(f"Tolerance: |c1|, |c2| < {TOLERANCE}")
    
    counterexamples = []
    near_misses = []  # Track how close we get
    
    min_norm = float('inf')
    start_time = time.time()
    
    for i in range(N_SAMPLES):
        if i > 0 and i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked {i:,} permutations ({elapsed:.1f}s), min ||(c1,c2)|| = {min_norm:.6f}")
        
        perm = generate_random_permutation()
        c1, c2, _, _ = compute_covariances(perm)
        
        norm = np.sqrt(c1**2 + c2**2)
        if norm < min_norm:
            min_norm = norm
            if norm < 1.0:  # Track near misses
                near_misses.append((norm, c1, c2, perm.copy()))
        
        if abs(c1) < TOLERANCE and abs(c2) < TOLERANCE:
            if not is_magic(perm):
                counterexamples.append((c1, c2, perm.copy()))
                print(f"\n!!! COUNTEREXAMPLE FOUND !!!")
                print(f"c1 = {c1:.6f}, c2 = {c2:.6f}")
                print(f"Matrix:\n{perm}")
    
    elapsed = time.time() - start_time
    print(f"\nCompleted {N_SAMPLES:,} samples in {elapsed:.1f}s")
    print()
    
    if counterexamples:
        print(f"✗ FOUND {len(counterexamples)} COUNTEREXAMPLES!")
        print("THE THEOREM IS FALSE (for this tolerance)")
        for c1, c2, perm in counterexamples[:5]:
            print(f"\n  c1={c1:.6f}, c2={c2:.6f}")
            print(f"  Row sums: {perm.sum(axis=1)}")
            print(f"  Col sums: {perm.sum(axis=0)}")
    else:
        print(f"✓ No counterexamples found among {N_SAMPLES:,} random samples")
        print(f"  Minimum covariance norm achieved: {min_norm:.6f}")
        print()
        print("  Note: This is EMPIRICAL evidence, not a proof.")
        print("  To prove the theorem rigorously, we would need to check all 16!/8 ≈ 2.6×10^12 permutations")
    
    print()
    print("CONCLUSION:")
    print("-" * 40)
    print()
    print("The diagonal covariances (c3, c4) are LINEAR COMBINATIONS of (c1, c2):")
    print("  c3 = Cov(X+Y, Z) = Cov(X,Z) + Cov(Y,Z) = c1 + c2")
    print("  c4 = Cov(X-Y, Z) = Cov(X,Z) - Cov(Y,Z) = c1 - c2")
    print()
    print("Therefore, the 'four independent conditions' are actually ONLY TWO:")
    print("  c1 = 0 and c2 = 0")
    print()
    print("The theorem should be RESTATED to reflect this!")
    
    # Show near misses for insight
    if near_misses:
        print()
        print("NEAR MISSES (smallest covariance norms found):")
        near_misses.sort(key=lambda x: x[0])
        for norm, c1, c2, perm in near_misses[:3]:
            print(f"\n  ||(c1,c2)|| = {norm:.6f}")
            print(f"  c1 = {c1:.6f}, c2 = {c2:.6f}")
            print(f"  Row sums: {perm.sum(axis=1)}")
            print(f"  Col sums: {perm.sum(axis=0)}")
            print(f"  Is magic: {is_magic(perm)}")

if __name__ == "__main__":
    main()

