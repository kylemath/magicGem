#!/usr/bin/env python3
"""
run_analysis.py
===============
Run all analyses and generate data files for the Magic Gems paper.

This script:
1. Generates all magic squares for n=3,4,5
2. Computes Magic Gem properties
3. Runs covariance analysis
4. Performs perturbation analysis
5. Analyzes manifold structure
6. Saves all results to JSON files in data/

Usage:
    python scripts/run_analysis.py
"""

import sys
import os
import json
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.magic_squares import (
    generate_all_3x3_magic_squares,
    get_canonical_3x3,
    siamese_method,
    count_arrangements,
    save_magic_squares,
    is_magic_square,
    generate_4x4_magic_squares
)
from src.magic_gems import (
    square_to_magic_gem,
    square_to_coordinates,
    save_gem
)
from src.analysis import (
    test_zero_covariance,
    analyze_magic_vs_random,
    perturbation_analysis,
    analyze_manifold_structure,
    save_analysis,
    analyze_exhaustive_n3,
    analyze_perturbation_isolation,
    analyze_scaling,
    analyze_large_scale_landscape,
    compute_landscape_statistics
)
from src.figures import generate_all_figures


def ensure_dirs():
    """Create output directories if they don't exist."""
    dirs = ['data', 'figures', 'output']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print("✓ Output directories created")


def analyze_3x3():
    """Complete analysis of 3×3 magic squares."""
    print("\n" + "="*50)
    print("Analyzing 3×3 Magic Squares")
    print("="*50)
    
    # Generate all magic squares
    magic_squares = generate_all_3x3_magic_squares()
    print(f"✓ Generated {len(magic_squares)} magic squares")
    
    # Save magic squares
    save_magic_squares(magic_squares, 'data/magic_squares_3x3.json')
    print("✓ Saved magic squares to data/magic_squares_3x3.json")
    
    # Compute Magic Gems
    gems = []
    for i, sq in enumerate(magic_squares):
        gem = square_to_magic_gem(sq)
        gems.append(gem)
        if i == 0:  # Save first one as example
            save_gem(gem, 'data/magic_gem_3x3_example.json')
    
    print("✓ Computed Magic Gems for all variants")
    
    # Covariance analysis
    print("\nCovariance Analysis:")
    lo_shu = get_canonical_3x3()
    coords = square_to_coordinates(lo_shu)
    cov_result = test_zero_covariance(coords)
    print(f"  Cov(X,Z) = {cov_result['cov_xz']:.10f}")
    print(f"  Cov(Y,Z) = {cov_result['cov_yz']:.10f}")
    print(f"  All off-diagonal zero: {cov_result['all_offdiag_zero']}")
    
    save_analysis(cov_result, 'data/covariance_3x3.json')
    
    # Magic vs random comparison
    print("\nMagic vs Random Comparison:")
    comparison = analyze_magic_vs_random(3, num_random=10000, seed=42)
    print(f"  Total arrangements: {comparison['total_arrangements']:,}")
    print(f"  Magic found in random sample: {comparison['magic_found_in_random']}")
    print(f"  Random mean Cov(X,Z): {comparison['random']['mean_cov_xz']:.6f}")
    print(f"  Random std Cov(X,Z): {comparison['random']['std_cov_xz']:.6f}")
    
    save_analysis(comparison, 'data/magic_vs_random_3x3.json')
    
    # Perturbation analysis
    print("\nPerturbation Analysis:")
    pert = perturbation_analysis(lo_shu, epsilon=0.1, num_trials=1000)
    print(f"  Original off-diag norm: {pert['original_offdiag_norm']:.10f}")
    print(f"  Mean perturbed norm: {pert['mean_perturbed_norm']:.6f}")
    print(f"  Proportion larger: {pert['proportion_larger']:.2%}")
    
    save_analysis(pert, 'data/perturbation_3x3.json')
    
    # Manifold structure
    print("\nManifold Structure Analysis:")
    manifold = analyze_manifold_structure(3, num_samples=5000, seed=42)
    print(f"  Samples analyzed: {manifold['num_samples']}")
    print(f"  Magic squares found: {manifold['num_magic']}")
    
    save_analysis(manifold, 'data/manifold_3x3.json')
    
    # Summary statistics
    summary = {
        'n': 3,
        'num_magic_squares': len(magic_squares),
        'total_arrangements': count_arrangements(3),
        'magic_constant': 15,
        'hull_volume': gems[0]['properties'].get('hull_volume'),
        'hull_area': gems[0]['properties'].get('hull_area'),
        'cov_xz': cov_result['cov_xz'],
        'cov_yz': cov_result['cov_yz'],
        'perturbation_proportion_larger': pert['proportion_larger'],
        'random_cov_xz_mean': comparison['random']['mean_cov_xz'],
        'random_cov_xz_std': comparison['random']['std_cov_xz'],
    }
    save_analysis(summary, 'data/summary_3x3.json')
    
    return summary


def analyze_5x5():
    """Analysis of 5×5 magic squares."""
    print("\n" + "="*50)
    print("Analyzing 5×5 Magic Squares")
    print("="*50)
    
    # Generate using Siamese method
    siamese_5 = siamese_method(5)
    print("✓ Generated 5×5 magic square (Siamese method)")
    print(f"  Is magic: {is_magic_square(siamese_5)}")
    
    # Save
    save_magic_squares([siamese_5], 'data/magic_squares_5x5.json')
    
    # Compute Magic Gem
    gem = square_to_magic_gem(siamese_5)
    save_gem(gem, 'data/magic_gem_5x5.json')
    print("✓ Computed Magic Gem")
    
    # Covariance analysis
    coords = square_to_coordinates(siamese_5)
    cov_result = test_zero_covariance(coords)
    print(f"\nCovariance Analysis:")
    print(f"  Cov(X,Z) = {cov_result['cov_xz']:.10f}")
    print(f"  Cov(Y,Z) = {cov_result['cov_yz']:.10f}")
    
    save_analysis(cov_result, 'data/covariance_5x5.json')
    
    # Summary
    summary = {
        'n': 5,
        'magic_constant': 65,
        'hull_volume': gem['properties'].get('hull_volume'),
        'hull_area': gem['properties'].get('hull_area'),
        'cov_xz': cov_result['cov_xz'],
        'cov_yz': cov_result['cov_yz'],
    }
    save_analysis(summary, 'data/summary_5x5.json')
    
    return summary


def analyze_4x4():
    """Analysis of 4×4 magic squares."""
    print("\n" + "="*50)
    print("Analyzing 4×4 Magic Squares")
    print("="*50)
    
    # Generate some 4×4 magic squares
    magic_squares = generate_4x4_magic_squares(limit=8)
    print(f"✓ Generated {len(magic_squares)} 4×4 magic squares")
    
    if magic_squares:
        save_magic_squares(magic_squares, 'data/magic_squares_4x4.json')
        
        # Analyze first one
        sq = magic_squares[0]
        gem = square_to_magic_gem(sq)
        save_gem(gem, 'data/magic_gem_4x4.json')
        
        coords = square_to_coordinates(sq)
        cov_result = test_zero_covariance(coords)
        print(f"\nCovariance Analysis (first square):")
        print(f"  Cov(X,Z) = {cov_result['cov_xz']:.10f}")
        print(f"  Cov(Y,Z) = {cov_result['cov_yz']:.10f}")
        
        save_analysis(cov_result, 'data/covariance_4x4.json')
        
        summary = {
            'n': 4,
            'num_generated': len(magic_squares),
            'essentially_different': 880,  # Known value
            'magic_constant': 34,
            'hull_volume': gem['properties'].get('hull_volume'),
            'hull_area': gem['properties'].get('hull_area'),
            'cov_xz': cov_result['cov_xz'],
            'cov_yz': cov_result['cov_yz'],
        }
        save_analysis(summary, 'data/summary_4x4.json')
        return summary
    
    return None


def analyze_energy_landscape():
    """
    Comprehensive energy landscape analysis.
    
    This includes:
    1. Exhaustive verification for n=3
    2. Perturbation isolation analysis
    3. Scaling analysis across n=3,4,5
    """
    print("\n" + "="*50)
    print("Energy Landscape Analysis")
    print("="*50)
    
    # 1. Exhaustive verification for n=3
    print("\nExhaustive Verification (n=3):")
    print("  Testing all 362,880 permutations...")
    exhaustive = analyze_exhaustive_n3(verbose=True)
    save_analysis(exhaustive, 'data/exhaustive_n3.json')
    print(f"  ✓ Saved to data/exhaustive_n3.json")
    
    # 2. Perturbation isolation
    print("\nPerturbation Isolation Analysis:")
    magic_squares = generate_all_3x3_magic_squares()
    perturbation = analyze_perturbation_isolation(magic_squares, verbose=True)
    save_analysis(perturbation, 'data/perturbation_isolation.json')
    print(f"  ✓ Saved to data/perturbation_isolation.json")
    
    # 3. Scaling analysis
    print("\nScaling Analysis (n=3,4,5):")
    scaling = analyze_scaling(verbose=True)
    save_analysis(scaling, 'data/scaling_analysis.json')
    print(f"  ✓ Saved to data/scaling_analysis.json")
    
    return {
        'exhaustive': exhaustive,
        'perturbation': perturbation,
        'scaling': scaling
    }


def analyze_large_scale(n4_samples=100000, n5_samples=100000):
    """
    Large-scale energy landscape analysis across orders n=3,4,5.
    
    This analysis provides comprehensive sampling of the energy landscape,
    enabling characterization of how the distribution evolves with order.
    For full-scale analysis (millions of samples), increase sample counts.
    
    Parameters
    ----------
    n4_samples : int
        Number of samples for n=4 (default: 100,000)
    n5_samples : int
        Number of samples for n=5 (default: 100,000)
    """
    print("\n" + "="*50)
    print("Large-Scale Energy Landscape Analysis")
    print("="*50)
    print(f"  n=3: Exhaustive (362,880)")
    print(f"  n=4: {n4_samples:,} samples")
    print(f"  n=5: {n5_samples:,} samples")
    print("="*50)
    
    results = analyze_large_scale_landscape(
        n3_exhaustive=True,
        n4_samples=n4_samples,
        n5_samples=n5_samples,
        verbose=True
    )
    
    # Save results (without full energy arrays for size)
    results_summary = {}
    for n in [3, 4, 5]:
        r = results[n]
        results_summary[str(n)] = {
            'n_samples': r['n_samples'],
            'magic_count': r['magic_count'],
            'exhaustive': r.get('exhaustive', False),
            'stats': r['stats']
        }
    
    save_analysis(results_summary, 'data/large_scale_landscape.json')
    print(f"\n✓ Saved to data/large_scale_landscape.json")
    
    # Print summary comparison
    print("\n" + "="*50)
    print("SCALING COMPARISON")
    print("="*50)
    print(f"\n{'Statistic':<25} {'n=3':<15} {'n=4':<15} {'n=5':<15}")
    print("-"*70)
    
    for stat in ['mean', 'std', 'peak_energy', 'entropy', 'zero_fraction']:
        row = f"{stat:<25}"
        for n in [3, 4, 5]:
            val = results[n]['stats'][stat]
            if stat == 'zero_fraction':
                row += f"{val:<15.2e}"
            else:
                row += f"{val:<15.4f}"
        print(row)
    
    return results


def main():
    """Run all analyses."""
    print("="*60)
    print("MAGIC GEMS: Full Analysis Pipeline")
    print("="*60)
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    print(f"Working directory: {os.getcwd()}")
    
    # Create directories
    ensure_dirs()
    
    # Run analyses
    summary_3 = analyze_3x3()
    summary_5 = analyze_5x5()
    summary_4 = analyze_4x4()
    
    # Energy landscape analysis
    energy_results = analyze_energy_landscape()
    
    # Large-scale landscape analysis (reduced samples for quick runs)
    # For full analysis, use n4_samples=10_000_000, n5_samples=50_000_000
    large_scale_results = analyze_large_scale(n4_samples=100000, n5_samples=100000)
    
    # Generate figures
    print("\n" + "="*50)
    print("Generating Figures")
    print("="*50)
    generate_all_figures('figures')
    
    # Create master summary
    master_summary = {
        '3x3': summary_3,
        '5x5': summary_5,
        '4x4': summary_4,
        'energy_landscape': {
            'theorem_verified': energy_results['exhaustive']['theorem_verified'],
            'all_magic_isolated': energy_results['perturbation']['all_isolated'],
            'min_perturbation_gap': energy_results['perturbation']['overall_min_gap']
        },
        'large_scale': {
            'n3_samples': large_scale_results[3]['n_samples'],
            'n4_samples': large_scale_results[4]['n_samples'],
            'n5_samples': large_scale_results[5]['n_samples'],
            'n3_peak_energy': large_scale_results[3]['stats']['peak_energy'],
            'n4_peak_energy': large_scale_results[4]['stats']['peak_energy'],
            'n5_peak_energy': large_scale_results[5]['stats']['peak_energy'],
        }
    }
    save_analysis(master_summary, 'data/master_summary.json')
    
    print("\n" + "="*60)
    print("✓ Analysis Complete!")
    print("="*60)
    print("\nOutput files:")
    print("  - data/*.json (analysis results)")
    print("  - figures/*.pdf (publication figures)")
    print("\nKey findings:")
    print(f"  - Zero-covariance theorem verified for n=3: {energy_results['exhaustive']['theorem_verified']}")
    print(f"  - Magic squares are isolated minima: {energy_results['perturbation']['all_isolated']}")
    print(f"  - Minimum energy gap: {energy_results['perturbation']['overall_min_gap']:.6f}")
    print("\nLarge-scale landscape analysis:")
    print(f"  - n=3 peak energy: {large_scale_results[3]['stats']['peak_energy']:.2f}")
    print(f"  - n=4 peak energy: {large_scale_results[4]['stats']['peak_energy']:.2f}")
    print(f"  - n=5 peak energy: {large_scale_results[5]['stats']['peak_energy']:.2f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

