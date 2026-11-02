#!/usr/bin/env python3
"""
Verify Near-Zero Energy Configurations
=======================================

This script investigates the configurations found with E ≈ 0 in the large-scale
sampling to verify whether they are:
1. True magic squares (validates conjecture)
2. Floating-point artifacts (E actually > 10^-10)
3. Semi-magic squares (E_cov = 0 but E_diag > 0)
4. Counterexamples (E = 0 but not magic) - would require investigation!

Author: [Collaborative Reviewer]
Date: December 2025
"""

import numpy as np
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "verification_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def is_magic_square(arr):
    """Rigorous magic square verification."""
    n = arr.shape[0]
    magic_sum = n * (n**2 + 1) // 2
    
    # Check all rows
    row_sums = arr.sum(axis=1)
    if not np.all(row_sums == magic_sum):
        return False, "Row sums not equal"
    
    # Check all columns
    col_sums = arr.sum(axis=0)
    if not np.all(col_sums == magic_sum):
        return False, "Column sums not equal"
    
    # Check main diagonal
    if np.trace(arr) != magic_sum:
        return False, "Main diagonal sum incorrect"
    
    # Check anti-diagonal
    if np.trace(np.fliplr(arr)) != magic_sum:
        return False, "Anti-diagonal sum incorrect"
    
    return True, "Valid magic square"


def compute_precise_energy(arr):
    """
    Compute energy with high precision (using float64).
    Returns (E_total, E_cov, E_diag, details)
    """
    n = arr.shape[0]
    
    # Centered coordinates
    j_coords = np.arange(n, dtype=np.float64) - (n-1)/2
    i_coords = (n-1)/2 - np.arange(n, dtype=np.float64)
    z = arr.astype(np.float64) - (n**2 + 1)/2
    
    # Build grids
    x_grid = np.tile(j_coords, (n, 1))
    y_grid = np.tile(i_coords, (n, 1)).T
    
    # Covariances (means are zero by construction)
    cov_xz = np.mean(x_grid * z)
    cov_yz = np.mean(y_grid * z)
    e_cov = cov_xz**2 + cov_yz**2
    
    # Diagonal energy
    overall_mean = (n**2 + 1) / 2
    main_diag = np.array([arr[i, i] for i in range(n)])
    anti_diag = np.array([arr[i, n-1-i] for i in range(n)])
    
    main_mean = np.mean(main_diag)
    anti_mean = np.mean(anti_diag)
    
    e_diag = (main_mean - overall_mean)**2 + (anti_mean - overall_mean)**2
    e_total = e_cov + e_diag
    
    details = {
        'cov_xz': float(cov_xz),
        'cov_yz': float(cov_yz),
        'e_cov': float(e_cov),
        'main_mean': float(main_mean),
        'anti_mean': float(anti_mean),
        'e_diag': float(e_diag),
        'e_total': float(e_total)
    }
    
    return e_total, e_cov, e_diag, details


def analyze_configuration(arr, config_id, n):
    """
    Complete analysis of a single configuration.
    """
    result = {
        'config_id': config_id,
        'n': n,
        'arrangement': arr.tolist()
    }
    
    # Check if magic
    is_magic, msg = is_magic_square(arr)
    result['is_magic'] = is_magic
    result['magic_check_msg'] = msg
    
    # Compute precise energy
    e_total, e_cov, e_diag, details = compute_precise_energy(arr)
    result['energy'] = details
    
    # Compute row/column/diagonal sums
    result['row_sums'] = arr.sum(axis=1).tolist()
    result['col_sums'] = arr.sum(axis=0).tolist()
    result['main_diag_sum'] = int(np.trace(arr))
    result['anti_diag_sum'] = int(np.trace(np.fliplr(arr)))
    
    # Classification
    magic_sum = n * (n**2 + 1) // 2
    equal_rows = np.all(arr.sum(axis=1) == magic_sum)
    equal_cols = np.all(arr.sum(axis=0) == magic_sum)
    equal_diags = (np.trace(arr) == magic_sum and np.trace(np.fliplr(arr)) == magic_sum)
    
    if is_magic:
        result['classification'] = "MAGIC SQUARE"
    elif equal_rows and equal_cols and not equal_diags:
        result['classification'] = "SEMI-MAGIC (no diagonals)"
    elif e_total < 1e-14:
        result['classification'] = "FLOATING-POINT ZERO (E < 10^-14)"
    elif e_total < 1e-10:
        result['classification'] = "NEAR-ZERO (E < 10^-10)"
    else:
        result['classification'] = "FALSE POSITIVE (E too large)"
    
    return result


def main():
    """
    Main verification routine.
    
    Since we don't have the actual near-zero configurations saved from the 
    large-scale run, this script demonstrates how to verify them when available.
    """
    print("="*70)
    print("NEAR-ZERO CONFIGURATION VERIFICATION")
    print("="*70)
    
    # Load the results summary
    results_file = Path(__file__).parent / "analysis_output_large_scale" / "landscape_comparison_results.json"
    
    if not results_file.exists():
        print(f"\nResults file not found: {results_file}")
        print("This script requires the output from magic_gem_large_scale_analysis.py")
        return
    
    with open(results_file) as f:
        results = json.load(f)
    
    print("\nSummary of Large-Scale Run:")
    for n_str, data in sorted(results.items()):
        n = int(n_str)
        print(f"\nn = {n}:")
        print(f"  Samples tested: {data['n_samples']:,}")
        print(f"  Magic squares found: {data['magic_count']}")
        print(f"  Zero-energy fraction: {data['stats']['zero_fraction']:.2e}")
        
        # Calculate expected near-zero count
        near_zero_count = int(data['n_samples'] * data['stats']['zero_fraction'])
        print(f"  Estimated near-zero configs: ~{near_zero_count}")
    
    print("\n" + "-"*70)
    print("DEMONSTRATION: Verifying Known Magic Squares")
    print("-"*70)
    
    # Test with known magic squares
    lo_shu = np.array([
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ])
    
    durer = np.array([
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ])
    
    test_configs = [
        (lo_shu, "Lo Shu", 3),
        (durer, "Dürer", 4)
    ]
    
    results_list = []
    
    for arr, name, n in test_configs:
        print(f"\nAnalyzing {name} square (n={n})...")
        result = analyze_configuration(arr, name, n)
        results_list.append(result)
        
        print(f"  Is magic: {result['is_magic']}")
        print(f"  E_total: {result['energy']['e_total']:.2e}")
        print(f"  E_cov: {result['energy']['e_cov']:.2e}")
        print(f"  E_diag: {result['energy']['e_diag']:.2e}")
        print(f"  Classification: {result['classification']}")
    
    # Test with a non-magic configuration
    print("\n" + "-"*70)
    print("DEMONSTRATION: Non-Magic Configuration")
    print("-"*70)
    
    non_magic = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ])
    
    result = analyze_configuration(non_magic, "Sequential", 4)
    results_list.append(result)
    
    print(f"\nAnalyzing sequential arrangement (clearly not magic)...")
    print(f"  Is magic: {result['is_magic']}")
    print(f"  E_total: {result['energy']['e_total']:.6f}")
    print(f"  E_cov: {result['energy']['e_cov']:.6f}")
    print(f"  E_diag: {result['energy']['e_diag']:.6f}")
    print(f"  Classification: {result['classification']}")
    print(f"  Row sums: {result['row_sums']}")
    print(f"  Col sums: {result['col_sums']}")
    
    # Save results
    output_file = OUTPUT_DIR / "verification_results.json"
    with open(output_file, 'w') as f:
        json.dump(results_list, f, indent=2)
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {output_file}")
    
    print("\n" + "="*70)
    print("INSTRUCTIONS FOR FULL VERIFICATION")
    print("="*70)
    print("""
To verify the near-zero configurations from your large-scale run:

1. Modify magic_gem_large_scale_analysis.py to save configurations with E < 10^-6
2. Add this code to the sampling function:
   
   if e_total < 1e-6:
       near_zero_configs.append({
           'arrangement': arr.copy(),
           'energy': e_total
       })

3. After sampling completes, save these configurations:
   
   with open('near_zero_configs_n{n}.json', 'w') as f:
       json.dump(near_zero_configs, f)

4. Run this verification script on the saved configurations
5. Report findings in the paper

Expected outcome: All near-zero configs should be either:
- True magic squares (E < 10^-14), OR
- Floating-point artifacts

Finding a non-magic configuration with E = 0 would be a COUNTEREXAMPLE
to Conjecture A.1 and would require immediate investigation!
    """)


if __name__ == '__main__':
    main()

