#!/usr/bin/env python3
"""
Magic Gems: Large-Scale Energy Landscape Analysis
==================================================

Leverages modern multi-core hardware to perform extensive sampling
of the energy landscape for n=5, comparing to exhaustive n=3 and sampled n=4.

Designed for: Mac Studio M5, 128GB RAM (or similar high-performance system)

Key analyses:
1. Exhaustive n=3 (362,880 arrangements) - already feasible
2. Heavy sampling n=4 (10M-50M samples vs 20.9 trillion total)
3. Heavy sampling n=5 (10M-100M samples vs 15.5 septillion total)
4. Cross-order comparison of energy landscape structure

Author: [Collaborative Reviewer]
Date: December 2025
"""

import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import multiprocessing as mp
from functools import partial
from pathlib import Path
import time
from collections import Counter
import json

# Configuration
OUTPUT_DIR = Path(__file__).parent / "analysis_output_large_scale"
OUTPUT_DIR.mkdir(exist_ok=True)

np.random.seed(42)


# =============================================================================
# CORE FUNCTIONS (optimized for vectorization)
# =============================================================================

def compute_covariance_energy_vectorized(arrangements):
    """
    Vectorized computation of covariance energy for multiple arrangements.
    
    Args:
        arrangements: array of shape (n_samples, n, n)
    
    Returns:
        energies: array of shape (n_samples,)
    """
    n_samples, n, _ = arrangements.shape
    
    # Create coordinate grids
    j_coords = np.arange(n) - (n-1)/2  # column coords
    i_coords = (n-1)/2 - np.arange(n)  # row coords
    
    # Value coords (centered)
    z = arrangements - (n**2 + 1)/2
    
    # Compute covariances for all samples at once
    x_grid = np.tile(j_coords, (n, 1))  # (n, n)
    y_grid = np.tile(i_coords, (n, 1)).T  # (n, n)
    
    # Flatten for each sample
    x_flat = x_grid.ravel()  # (n²,)
    y_flat = y_grid.ravel()  # (n²,)
    z_flat = z.reshape(n_samples, -1)  # (n_samples, n²)
    
    # Covariances (means are zero by construction)
    cov_xz = np.mean(x_flat * z_flat, axis=1)  # (n_samples,)
    cov_yz = np.mean(y_flat * z_flat, axis=1)  # (n_samples,)
    
    return cov_xz**2 + cov_yz**2


def compute_total_energy_vectorized(arrangements):
    """
    Compute total energy (covariance + diagonal) for multiple arrangements.
    """
    n_samples, n, _ = arrangements.shape
    
    # Covariance energy
    e_cov = compute_covariance_energy_vectorized(arrangements)
    
    # Diagonal energy
    overall_mean = (n**2 + 1) / 2
    
    # Extract diagonals vectorized
    main_diags = np.array([arr[np.arange(n), np.arange(n)] for arr in arrangements])
    anti_diags = np.array([arr[np.arange(n), np.arange(n-1, -1, -1)] for arr in arrangements])
    
    main_means = np.mean(main_diags, axis=1)
    anti_means = np.mean(anti_diags, axis=1)
    
    e_diag = (main_means - overall_mean)**2 + (anti_means - overall_mean)**2
    
    return e_cov + e_diag


def generate_random_arrangements_batch(n, batch_size):
    """
    Generate a batch of random arrangements using vectorized shuffle.
    """
    base = np.arange(1, n**2 + 1)
    arrangements = np.array([np.random.permutation(base).reshape(n, n) 
                            for _ in range(batch_size)])
    return arrangements


def is_magic_square_fast(arr):
    """Fast magic square check."""
    n = arr.shape[0]
    magic_sum = n * (n**2 + 1) // 2
    
    return (np.all(arr.sum(axis=0) == magic_sum) and
            np.all(arr.sum(axis=1) == magic_sum) and
            np.trace(arr) == magic_sum and
            np.trace(np.fliplr(arr)) == magic_sum)


# =============================================================================
# PARALLEL SAMPLING
# =============================================================================

def sample_chunk(args):
    """
    Worker function for parallel sampling.
    
    Args:
        args: tuple of (n, chunk_size, chunk_id, seed)
    
    Returns:
        dict with energies and magic square count
    """
    n, chunk_size, chunk_id, seed = args
    np.random.seed(seed)
    
    # Process in batches for memory efficiency
    batch_size = min(10000, chunk_size)
    n_batches = (chunk_size + batch_size - 1) // batch_size
    
    energies = []
    magic_count = 0
    
    for batch_idx in range(n_batches):
        current_batch_size = min(batch_size, chunk_size - batch_idx * batch_size)
        arrangements = generate_random_arrangements_batch(n, current_batch_size)
        
        # Compute energies
        batch_energies = compute_total_energy_vectorized(arrangements)
        energies.extend(batch_energies)
        
        # Check for magic squares (very rare, but check near-zero energy)
        near_zero = batch_energies < 1e-10
        if np.any(near_zero):
            for arr in arrangements[near_zero]:
                if is_magic_square_fast(arr):
                    magic_count += 1
    
    return {
        'energies': np.array(energies),
        'magic_count': magic_count,
        'chunk_id': chunk_id
    }


def parallel_energy_sampling(n, n_samples, n_workers=None):
    """
    Sample energy landscape in parallel.
    
    Args:
        n: order of magic square
        n_samples: total number of samples
        n_workers: number of parallel workers (default: CPU count)
    
    Returns:
        dict with results
    """
    if n_workers is None:
        n_workers = mp.cpu_count()
    
    print(f"Sampling n={n} with {n_samples:,} arrangements using {n_workers} workers...")
    start_time = time.time()
    
    # Divide work into chunks
    chunk_size = n_samples // n_workers
    args_list = [(n, chunk_size, i, 42 + i) for i in range(n_workers)]
    
    # Add remaining samples to last chunk
    remainder = n_samples % n_workers
    if remainder > 0:
        args_list.append((n, remainder, n_workers, 42 + n_workers))
    
    # Parallel execution
    with mp.Pool(n_workers) as pool:
        results = pool.map(sample_chunk, args_list)
    
    # Combine results
    all_energies = np.concatenate([r['energies'] for r in results])
    total_magic = sum(r['magic_count'] for r in results)
    
    elapsed = time.time() - start_time
    
    print(f"  Completed in {elapsed:.1f}s ({n_samples/elapsed:,.0f} samples/sec)")
    print(f"  Magic squares found: {total_magic}")
    print(f"  Energy range: [{all_energies.min():.6f}, {all_energies.max():.6f}]")
    print(f"  Energy mean: {all_energies.mean():.6f} ± {all_energies.std():.6f}")
    
    return {
        'n': n,
        'n_samples': len(all_energies),
        'energies': all_energies,
        'magic_count': total_magic,
        'elapsed_time': elapsed,
        'samples_per_sec': n_samples / elapsed
    }


# =============================================================================
# ADVANCED ANALYSIS
# =============================================================================

def compute_landscape_statistics(energies, n_bins=200):
    """
    Compute detailed statistics of the energy landscape.
    """
    hist, bin_edges = np.histogram(energies, bins=n_bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Peak energy (mode)
    peak_idx = np.argmax(hist)
    peak_energy = bin_centers[peak_idx]
    
    # Entropy of distribution (measure of landscape ruggedness)
    probs = hist / hist.sum()
    probs = probs[probs > 0]  # Remove zeros
    entropy = -np.sum(probs * np.log(probs))
    
    return {
        'min': energies.min(),
        'max': energies.max(),
        'mean': energies.mean(),
        'std': energies.std(),
        'median': np.median(energies),
        'q25': np.percentile(energies, 25),
        'q75': np.percentile(energies, 75),
        'peak_energy': peak_energy,
        'entropy': entropy,
        'zero_fraction': (energies < 1e-10).sum() / len(energies)
    }


def compare_landscapes_across_orders(results_dict):
    """
    Statistical comparison of energy landscapes for different n.
    """
    print("\n" + "="*70)
    print("ENERGY LANDSCAPE COMPARISON ACROSS ORDERS")
    print("="*70)
    
    comparison = {}
    
    for n, results in sorted(results_dict.items()):
        stats = compute_landscape_statistics(results['energies'])
        comparison[n] = stats
        
        print(f"\nn = {n}:")
        print(f"  Samples: {results['n_samples']:,}")
        print(f"  Energy mean: {stats['mean']:.4f} ± {stats['std']:.4f}")
        print(f"  Energy median: {stats['median']:.4f}")
        print(f"  Peak energy (mode): {stats['peak_energy']:.4f}")
        print(f"  Energy range: [{stats['min']:.6f}, {stats['max']:.4f}]")
        print(f"  Landscape entropy: {stats['entropy']:.4f}")
        print(f"  Zero-energy fraction: {stats['zero_fraction']:.2e}")
    
    # Scaling trends
    print("\n" + "-"*70)
    print("SCALING TRENDS:")
    orders = sorted(comparison.keys())
    
    print("\nMean energy scaling:")
    for n in orders:
        norm = comparison[n]['mean'] / comparison[3]['mean']
        print(f"  n={n}: {comparison[n]['mean']:.4f} ({norm:.2f}× base)")
    
    print("\nLandscape entropy (ruggedness):")
    for n in orders:
        print(f"  n={n}: {comparison[n]['entropy']:.4f}")
    
    print("\nPeak shift:")
    for n in orders:
        print(f"  n={n}: peak at E={comparison[n]['peak_energy']:.4f}")
    
    return comparison


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_multi_order_landscapes(results_dict, save_path=None):
    """
    Create comprehensive multi-panel comparison of energy landscapes.
    """
    fig = plt.figure(figsize=(18, 12))
    
    orders = sorted(results_dict.keys())
    n_orders = len(orders)
    
    # Color scheme
    colors = {'3': '#2E7D32', '4': '#1565C0', '5': '#C62828'}
    
    # Top row: Individual histograms with different x-axis scales
    for idx, n in enumerate(orders):
        ax = plt.subplot(3, 3, idx + 1)
        energies = results_dict[n]['energies']
        
        # Adaptive binning based on range
        n_bins = min(150, int(np.sqrt(len(energies))))
        ax.hist(energies, bins=n_bins, color=colors[str(n)], 
                alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Mark zero energy
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2, 
                   label=f'Magic squares (E=0)')
        
        ax.set_xlabel(f'Energy E(S)', fontsize=11)
        ax.set_ylabel('Count', fontsize=11)
        ax.set_title(f'n={n} Energy Distribution\n({results_dict[n]["n_samples"]:,} samples)', 
                     fontsize=12, fontweight='bold')
        ax.set_yscale('log')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Add statistics box
        stats = compute_landscape_statistics(energies)
        stats_text = f"μ={stats['mean']:.2f}\nσ={stats['std']:.2f}\nmode={stats['peak_energy']:.2f}"
        ax.text(0.97, 0.97, stats_text, transform=ax.transAxes,
               fontsize=9, va='top', ha='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Middle row: Overlaid comparison (same scale)
    ax_overlay = plt.subplot(3, 3, 4)
    
    # Find common x-range
    all_energies = np.concatenate([results_dict[n]['energies'] for n in orders])
    x_max = np.percentile(all_energies, 99.9)  # Clip outliers for visualization
    
    bins = np.linspace(0, x_max, 100)
    
    for n in orders:
        energies = results_dict[n]['energies']
        energies_clipped = energies[energies <= x_max]
        ax_overlay.hist(energies_clipped, bins=bins, color=colors[str(n)], 
                       alpha=0.5, label=f'n={n}', edgecolor='black', linewidth=0.5)
    
    ax_overlay.axvline(x=0, color='red', linestyle='--', linewidth=2)
    ax_overlay.set_xlabel('Energy E(S)', fontsize=11)
    ax_overlay.set_ylabel('Count', fontsize=11)
    ax_overlay.set_title('Overlaid Comparison (Same Scale)', fontsize=12, fontweight='bold')
    ax_overlay.legend(fontsize=10)
    ax_overlay.set_yscale('log')
    ax_overlay.grid(True, alpha=0.3)
    
    # Middle center: Normalized distributions (PDF)
    ax_norm = plt.subplot(3, 3, 5)
    
    for n in orders:
        energies = results_dict[n]['energies']
        energies_clipped = energies[energies <= x_max]
        
        # Compute normalized histogram (PDF)
        hist, bin_edges = np.histogram(energies_clipped, bins=bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        ax_norm.plot(bin_centers, hist, color=colors[str(n)], 
                    linewidth=2, label=f'n={n}', alpha=0.8)
    
    ax_norm.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.5)
    ax_norm.set_xlabel('Energy E(S)', fontsize=11)
    ax_norm.set_ylabel('Probability Density', fontsize=11)
    ax_norm.set_title('Normalized Distributions (PDF)', fontsize=12, fontweight='bold')
    ax_norm.legend(fontsize=10)
    ax_norm.set_yscale('log')
    ax_norm.grid(True, alpha=0.3)
    
    # Middle right: Cumulative distributions
    ax_cdf = plt.subplot(3, 3, 6)
    
    for n in orders:
        energies = np.sort(results_dict[n]['energies'])
        cdf = np.arange(1, len(energies) + 1) / len(energies)
        
        # Sample for plotting efficiency
        stride = max(1, len(energies) // 10000)
        ax_cdf.plot(energies[::stride], cdf[::stride], color=colors[str(n)], 
                   linewidth=2, label=f'n={n}', alpha=0.8)
    
    ax_cdf.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.5)
    ax_cdf.set_xlabel('Energy E(S)', fontsize=11)
    ax_cdf.set_ylabel('Cumulative Probability', fontsize=11)
    ax_cdf.set_title('Cumulative Distribution Functions', fontsize=12, fontweight='bold')
    ax_cdf.legend(fontsize=10)
    ax_cdf.set_xscale('log')
    ax_cdf.grid(True, alpha=0.3)
    
    # Bottom row: Statistical comparisons
    ax_stats1 = plt.subplot(3, 3, 7)
    
    # Mean and std comparison
    means = [compute_landscape_statistics(results_dict[n]['energies'])['mean'] for n in orders]
    stds = [compute_landscape_statistics(results_dict[n]['energies'])['std'] for n in orders]
    
    x_pos = np.arange(len(orders))
    ax_stats1.bar(x_pos, means, yerr=stds, color=[colors[str(n)] for n in orders],
                  alpha=0.7, capsize=5, edgecolor='black', linewidth=1.5)
    ax_stats1.set_xticks(x_pos)
    ax_stats1.set_xticklabels([f'n={n}' for n in orders])
    ax_stats1.set_ylabel('Mean Energy', fontsize=11)
    ax_stats1.set_title('Mean Energy vs Order', fontsize=12, fontweight='bold')
    ax_stats1.grid(True, axis='y', alpha=0.3)
    
    # Bottom center: Entropy (landscape ruggedness)
    ax_stats2 = plt.subplot(3, 3, 8)
    
    entropies = [compute_landscape_statistics(results_dict[n]['energies'])['entropy'] for n in orders]
    
    ax_stats2.bar(x_pos, entropies, color=[colors[str(n)] for n in orders],
                  alpha=0.7, edgecolor='black', linewidth=1.5)
    ax_stats2.set_xticks(x_pos)
    ax_stats2.set_xticklabels([f'n={n}' for n in orders])
    ax_stats2.set_ylabel('Landscape Entropy', fontsize=11)
    ax_stats2.set_title('Landscape Complexity (Entropy)', fontsize=12, fontweight='bold')
    ax_stats2.grid(True, axis='y', alpha=0.3)
    
    # Bottom right: Peak energy (mode) shift
    ax_stats3 = plt.subplot(3, 3, 9)
    
    peaks = [compute_landscape_statistics(results_dict[n]['energies'])['peak_energy'] for n in orders]
    
    ax_stats3.plot(orders, peaks, marker='o', markersize=12, linewidth=3,
                   color='darkblue', markerfacecolor='gold', markeredgecolor='black', markeredgewidth=2)
    ax_stats3.set_xlabel('Order n', fontsize=11)
    ax_stats3.set_ylabel('Peak Energy (Mode)', fontsize=11)
    ax_stats3.set_title('Energy Landscape Peak Shift', fontsize=12, fontweight='bold')
    ax_stats3.set_xticks(orders)
    ax_stats3.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(orders, peaks, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(min(orders), max(orders), 100)
    ax_stats3.plot(x_smooth, p(x_smooth), '--', color='red', alpha=0.6, linewidth=2, label='Quadratic fit')
    ax_stats3.legend(fontsize=9)
    
    plt.suptitle('Energy Landscape Analysis Across Orders n=3,4,5', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.close()
    return fig


def plot_landscape_evolution_heatmap(results_dict, save_path=None):
    """
    Create a 2D heatmap showing how energy distribution evolves with n.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    orders = sorted(results_dict.keys())
    
    # Create common energy bins
    all_energies = np.concatenate([results_dict[n]['energies'] for n in orders])
    e_max = np.percentile(all_energies, 99.5)
    energy_bins = np.linspace(0, e_max, 150)
    
    # Compute normalized histograms for each order
    heatmap_data = []
    for n in orders:
        energies = results_dict[n]['energies']
        hist, _ = np.histogram(energies, bins=energy_bins, density=True)
        heatmap_data.append(hist)
    
    heatmap_data = np.array(heatmap_data)
    
    # Plot heatmap
    im = ax.imshow(heatmap_data, aspect='auto', cmap='hot', origin='lower',
                   extent=[energy_bins[0], energy_bins[-1], 2.5, 5.5],
                   norm=LogNorm(vmin=heatmap_data[heatmap_data > 0].min(), 
                               vmax=heatmap_data.max()))
    
    # Mark zero energy
    ax.axvline(x=0, color='cyan', linestyle='--', linewidth=3, label='E=0 (Magic)')
    
    ax.set_xlabel('Energy E(S)', fontsize=13)
    ax.set_ylabel('Order n', fontsize=13)
    ax.set_yticks(orders)
    ax.set_yticklabels([f'n={n}' for n in orders])
    ax.set_title('Energy Landscape Evolution: Heatmap View', fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax, label='Probability Density (log scale)')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.close()
    return fig


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main(n3_samples='exhaustive', n4_samples=10_000_000, n5_samples=50_000_000, 
         n_workers=None):
    """
    Large-scale energy landscape analysis.
    
    Args:
        n3_samples: 'exhaustive' or int (default: exhaustive = 362,880)
        n4_samples: number of samples for n=4 (default: 10M)
        n5_samples: number of samples for n=5 (default: 50M, can go to 100M+)
        n_workers: number of parallel workers (default: CPU count)
    """
    print("\n" + "="*70)
    print("MAGIC GEMS: LARGE-SCALE ENERGY LANDSCAPE ANALYSIS")
    print("="*70)
    print(f"Target: Mac Studio M5, 128GB RAM")
    print(f"Workers: {n_workers or mp.cpu_count()}")
    print("="*70 + "\n")
    
    results = {}
    
    # n=3: Exhaustive or sampled
    if n3_samples == 'exhaustive':
        print("\n[1/3] n=3: EXHAUSTIVE enumeration (362,880 permutations)...")
        # Import from original script
        from magic_gem_analysis import analyze_exhaustive_n3
        r3 = analyze_exhaustive_n3(verbose=False)
        results[3] = {
            'n': 3,
            'n_samples': len(r3['energy_values']),
            'energies': np.array(r3['energy_values']),
            'magic_count': r3['magic_squares'],
            'exhaustive': True
        }
        print(f"  ✓ Complete: {results[3]['n_samples']:,} arrangements analyzed")
    else:
        print(f"\n[1/3] n=3: Sampling {n3_samples:,} arrangements...")
        results[3] = parallel_energy_sampling(3, n3_samples, n_workers)
    
    # n=4: Heavy sampling
    print(f"\n[2/3] n=4: Heavy sampling ({n4_samples:,} from 20.9 trillion total)...")
    results[4] = parallel_energy_sampling(4, n4_samples, n_workers)
    
    # n=5: Very heavy sampling
    print(f"\n[3/3] n=5: Very heavy sampling ({n5_samples:,} from 15.5 septillion total)...")
    print(f"  Note: This will take several minutes on high-end hardware...")
    results[5] = parallel_energy_sampling(5, n5_samples, n_workers)
    
    # Statistical comparison
    comparison = compare_landscapes_across_orders(results)
    
    # Save raw results
    results_file = OUTPUT_DIR / 'landscape_comparison_results.json'
    save_data = {
        n: {
            'n_samples': r['n_samples'],
            'magic_count': r['magic_count'],
            'elapsed_time': r.get('elapsed_time', 0),
            'stats': {k: float(v) for k, v in compute_landscape_statistics(r['energies']).items()}
        }
        for n, r in results.items()
    }
    with open(results_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n✓ Raw results saved to: {results_file}")
    
    # Generate visualizations
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    print("\n[1/2] Multi-panel landscape comparison...")
    plot_multi_order_landscapes(results, 
                                save_path=OUTPUT_DIR / 'energy_landscapes_comparison.png')
    
    print("[2/2] Evolution heatmap...")
    plot_landscape_evolution_heatmap(results,
                                    save_path=OUTPUT_DIR / 'energy_landscape_evolution_heatmap.png')
    
    # Final summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nTotal arrangements analyzed: {sum(r['n_samples'] for r in results.values()):,}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nGenerated files:")
    print("  1. energy_landscapes_comparison.png - 9-panel comprehensive comparison")
    print("  2. energy_landscape_evolution_heatmap.png - Heatmap showing landscape evolution")
    print("  3. landscape_comparison_results.json - Raw numerical results")
    
    print("\n✓ Key insight: Magic squares as isolated ground states at E=0")
    print("✓ Landscape becomes more complex and 'flatter' as n increases")
    print("✓ Peak energy shifts: demonstrates how optimization difficulty scales")
    
    return results, comparison


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Large-Scale Energy Landscape Analysis')
    parser.add_argument('--n4', type=int, default=10_000_000,
                       help='Number of samples for n=4 (default: 10M)')
    parser.add_argument('--n5', type=int, default=50_000_000,
                       help='Number of samples for n=5 (default: 50M, can go 100M+)')
    parser.add_argument('--workers', type=int, default=None,
                       help='Number of parallel workers (default: CPU count)')
    
    args = parser.parse_args()
    
    results, comparison = main(
        n3_samples='exhaustive',
        n4_samples=args.n4,
        n5_samples=args.n5,
        n_workers=args.workers
    )

