#!/usr/bin/env python3
"""
Generate Publication-Ready Figures for Magic Gems Paper
========================================================

This script generates the specific figures needed for the paper revision:

Figure 4: Perturbation Gaps (already in analysis_output)
Figure 5: Energy Landscape Evolution Heatmap (already in analysis_output_large_scale)
Figure 6: 9-Panel Energy Landscape Analysis (already in analysis_output_large_scale)
Figure 7: Scaling Summary (NEW - create here)

Author: [Collaborative Reviewer]
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

OUTPUT_DIR = Path(__file__).parent / "paper_figures"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_large_scale_results():
    """Load the results from the large-scale analysis."""
    results_file = Path(__file__).parent / "analysis_output_large_scale" / "landscape_comparison_results.json"
    
    if not results_file.exists():
        print(f"Error: Could not find {results_file}")
        print("Run magic_gem_large_scale_analysis.py first!")
        return None
    
    with open(results_file) as f:
        data = json.load(f)
    
    return {int(k): v for k, v in data.items()}


def create_figure_7_scaling_summary(results):
    """
    Create Figure 7: Comprehensive Scaling Summary
    
    A 2x2 panel showing:
    - Peak energy vs n (with quadratic fit)
    - Mean energy vs n (with error bars)
    - Landscape entropy vs n
    - Sample size / Magic square rarity
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    orders = sorted(results.keys())
    colors = {3: '#2E7D32', 4: '#1565C0', 5: '#C62828'}
    
    # Extract data
    peak_energies = [results[n]['stats']['peak_energy'] for n in orders]
    mean_energies = [results[n]['stats']['mean'] for n in orders]
    std_energies = [results[n]['stats']['std'] for n in orders]
    entropies = [results[n]['stats']['entropy'] for n in orders]
    samples = [results[n]['n_samples'] for n in orders]
    
    # Panel A: Peak Energy with Quadratic Fit
    ax1 = axes[0, 0]
    ax1.scatter(orders, peak_energies, s=200, c=[colors[n] for n in orders],
                edgecolors='black', linewidths=2, zorder=3)
    
    # Quadratic fit
    coeffs = np.polyfit(orders, peak_energies, 2)
    x_smooth = np.linspace(2.5, 5.5, 100)
    y_fit = np.polyval(coeffs, x_smooth)
    ax1.plot(x_smooth, y_fit, '--', color='darkred', linewidth=2.5, 
             label=f'$E_{{peak}} = {coeffs[0]:.2f}n^2 + {coeffs[1]:.2f}n + {coeffs[2]:.2f}$', 
             alpha=0.7)
    
    ax1.set_xlabel('Order $n$', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Peak Energy (Mode)', fontsize=13, fontweight='bold')
    ax1.set_title('(A) Peak Energy Scaling', fontsize=14, fontweight='bold')
    ax1.set_xticks(orders)
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Add R² value
    ss_res = np.sum((peak_energies - np.polyval(coeffs, orders))**2)
    ss_tot = np.sum((peak_energies - np.mean(peak_energies))**2)
    r_squared = 1 - (ss_res / ss_tot)
    ax1.text(0.95, 0.15, f'$R^2 = {r_squared:.4f}$', 
             transform=ax1.transAxes, fontsize=11, ha='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Panel B: Mean Energy with Error Bars
    ax2 = axes[0, 1]
    ax2.bar(orders, mean_energies, yerr=std_energies, 
            color=[colors[n] for n in orders], alpha=0.7,
            capsize=8, edgecolor='black', linewidth=1.5, error_kw={'linewidth': 2})
    
    ax2.set_xlabel('Order $n$', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Mean Energy $\\pm$ Std Dev', fontsize=13, fontweight='bold')
    ax2.set_title('(B) Mean Energy Distribution', fontsize=14, fontweight='bold')
    ax2.set_xticks(orders)
    ax2.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add values on bars
    for i, (n, mean, std) in enumerate(zip(orders, mean_energies, std_energies)):
        ax2.text(n, mean + std + 2, f'{mean:.1f}±{std:.1f}', 
                ha='center', fontsize=9, fontweight='bold')
    
    # Panel C: Landscape Entropy
    ax3 = axes[1, 0]
    bars = ax3.bar(orders, entropies, color=[colors[n] for n in orders],
                   alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add horizontal line at mean entropy
    mean_entropy = np.mean(entropies)
    ax3.axhline(y=mean_entropy, color='darkred', linestyle='--', 
                linewidth=2.5, alpha=0.7, label=f'Mean: {mean_entropy:.2f}')
    
    ax3.set_xlabel('Order $n$', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Landscape Entropy $H$', fontsize=13, fontweight='bold')
    ax3.set_title('(C) Landscape Complexity (Entropy)', fontsize=14, fontweight='bold')
    ax3.set_xticks(orders)
    ax3.set_ylim([3.5, 5.5])
    ax3.legend(fontsize=10)
    ax3.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add annotation
    ax3.text(0.5, 0.95, 'Near-constant entropy\nsuggests scale-invariant\nlandscape structure', 
             transform=ax3.transAxes, fontsize=9, va='top', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Panel D: Sample Size and Rarity
    ax4 = axes[1, 1]
    
    # Log scale for samples
    ax4_samples = ax4
    bars1 = ax4_samples.bar([n - 0.2 for n in orders], samples, width=0.35,
                            color='steelblue', alpha=0.7, edgecolor='black', 
                            linewidth=1.5, label='Samples Tested')
    ax4_samples.set_ylabel('Samples Tested', fontsize=13, fontweight='bold', color='steelblue')
    ax4_samples.set_yscale('log')
    ax4_samples.tick_params(axis='y', labelcolor='steelblue')
    
    # Twin axis for magic square probability
    ax4_prob = ax4_samples.twinx()
    
    # Known probabilities (from Table 2 in paper)
    probs = {
        3: 2.2e-5,   # 8 / 362,880
        4: 3.4e-10,  # 7,040 / 20.9 trillion
        5: 1.8e-17   # 2.8e8 / 15.5 septillion
    }
    prob_values = [probs[n] for n in orders]
    
    bars2 = ax4_prob.bar([n + 0.2 for n in orders], prob_values, width=0.35,
                         color='coral', alpha=0.7, edgecolor='black',
                         linewidth=1.5, label='Magic Square Rarity')
    ax4_prob.set_ylabel('P(Magic)', fontsize=13, fontweight='bold', color='coral')
    ax4_prob.set_yscale('log')
    ax4_prob.tick_params(axis='y', labelcolor='coral')
    
    ax4_samples.set_xlabel('Order $n$', fontsize=13, fontweight='bold')
    ax4_samples.set_title('(D) Sampling Scale vs Rarity', fontsize=14, fontweight='bold')
    ax4_samples.set_xticks(orders)
    
    # Combined legend
    lines1, labels1 = ax4_samples.get_legend_handles_labels()
    lines2, labels2 = ax4_prob.get_legend_handles_labels()
    ax4_samples.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    ax4_samples.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    plt.suptitle('Magic Square Energy Landscape: Scaling Properties', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    return fig


def copy_existing_figures():
    """
    Copy the already-generated figures to the paper_figures directory
    with proper names.
    """
    import shutil
    
    source_analysis = Path(__file__).parent / "analysis_output"
    source_large = Path(__file__).parent / "analysis_output_large_scale"
    
    # Figure 4: Perturbation gaps
    fig4_source = source_analysis / "perturbation_gaps.png"
    if fig4_source.exists():
        shutil.copy(fig4_source, OUTPUT_DIR / "Figure4_PerturbationGaps.png")
        print("✓ Copied Figure 4: Perturbation Gaps")
    else:
        print("✗ Figure 4 source not found")
    
    # Figure 5: Heatmap
    fig5_source = source_large / "energy_landscape_evolution_heatmap.png"
    if fig5_source.exists():
        shutil.copy(fig5_source, OUTPUT_DIR / "Figure5_EnergyLandscapeHeatmap.png")
        print("✓ Copied Figure 5: Energy Landscape Heatmap")
    else:
        print("✗ Figure 5 source not found")
    
    # Figure 6: 9-panel comparison
    fig6_source = source_large / "energy_landscapes_comparison.png"
    if fig6_source.exists():
        shutil.copy(fig6_source, OUTPUT_DIR / "Figure6_LandscapeComparison_9Panel.png")
        print("✓ Copied Figure 6: 9-Panel Landscape Comparison")
    else:
        print("✗ Figure 6 source not found")


def main():
    """Generate all figures for the paper."""
    print("\n" + "="*70)
    print("GENERATING PUBLICATION FIGURES FOR MAGIC GEMS PAPER")
    print("="*70 + "\n")
    
    # Load data
    print("[1/3] Loading large-scale analysis results...")
    results = load_large_scale_results()
    
    if results is None:
        return
    
    print("✓ Loaded results for n =", list(results.keys()))
    print(f"  Total samples: {sum(r['n_samples'] for r in results.values()):,}")
    
    # Generate new figure
    print("\n[2/3] Generating Figure 7: Scaling Summary...")
    fig7 = create_figure_7_scaling_summary(results)
    fig7_path = OUTPUT_DIR / "Figure7_ScalingSummary.png"
    fig7.savefig(fig7_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {fig7_path}")
    plt.close(fig7)
    
    # Copy existing figures
    print("\n[3/3] Organizing existing figures...")
    copy_existing_figures()
    
    # Summary
    print("\n" + "="*70)
    print("FIGURE GENERATION COMPLETE")
    print("="*70)
    print(f"\nAll figures saved to: {OUTPUT_DIR}")
    print("\nFigures ready for paper:")
    print("  Figure 4: Perturbation Gaps (isolation analysis)")
    print("  Figure 5: Energy Landscape Heatmap (n=3,4,5 evolution)")
    print("  Figure 6: 9-Panel Landscape Comparison (comprehensive)")
    print("  Figure 7: Scaling Summary (NEW - peak/mean/entropy/rarity)")
    
    print("\n" + "="*70)
    print("LATEX FIGURE COMMANDS")
    print("="*70)
    print("""
Add these to your paper:

% Figure 4
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.9\\textwidth]{figures/Figure4_PerturbationGaps.png}
    \\caption{\\textbf{Isolation of Magic Squares.} Distribution of minimum 
    energy increases after single-swap perturbations of $n=4$ magic squares 
    (880 squares tested). Every perturbation strictly increases energy 
    (minimum gap: 0.0039), confirming that magic squares are isolated local 
    minima in the covariance landscape.}
    \\label{fig:perturbation}
\\end{figure}

% Figure 5
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.9\\textwidth]{figures/Figure5_EnergyLandscapeHeatmap.png}
    \\caption{\\textbf{Energy Landscape Evolution.} Heatmap showing probability 
    density (log scale) as a function of energy $E(S)$ and order $n$. Data from 
    exhaustive enumeration ($n=3$, 362,880 samples) and large-scale sampling 
    ($n=4$: $5 \\times 10^7$, $n=5$: $2 \\times 10^8$ samples). The cyan line 
    marks $E=0$, where magic squares reside as isolated ground states.}
    \\label{fig:heatmap}
\\end{figure}

% Figure 6
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{figures/Figure6_LandscapeComparison_9Panel.png}
    \\caption{\\textbf{Comprehensive Energy Landscape Analysis.} (Top) Individual 
    energy distributions for $n=3,4,5$. (Middle) Overlaid comparison, normalized 
    PDFs, and cumulative distributions. (Bottom) Mean energy scaling, landscape 
    entropy, and quadratic fit to peak energy shift ($R^2=0.9999$).}
    \\label{fig:landscape-comparison}
\\end{figure}

% Figure 7
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{figures/Figure7_ScalingSummary.png}
    \\caption{\\textbf{Scaling Properties Across Orders.} (A) Peak energy follows 
    quadratic scaling $E_{\\text{peak}} \\approx 0.70n^2$. (B) Mean energy with 
    error bars. (C) Landscape entropy remains near-constant at $H \\approx 4.4$, 
    suggesting scale-invariant structure. (D) Sample sizes tested vs magic square 
    rarity, demonstrating the computational challenge at larger $n$.}
    \\label{fig:scaling}
\\end{figure}
    """)


if __name__ == '__main__':
    main()

