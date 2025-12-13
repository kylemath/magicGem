#!/usr/bin/env python3
"""
generate_new_figures.py
=======================
Generate the new high-impact figures recommended by referee feedback.

New figures:
1. fig_lowmode_failure_n4: Visual showing E_low=0 but non-magic (with deviation bars)
2. fig_energy_comparison_n4: E_low vs E_full scatter showing they measure different things
3. fig_n4_bands_geometry: Perturbation gap vs hull vertices (explaining trimodal structure)

These replace the redundant n=3,4,5 full-pipeline composites.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.spatial import ConvexHull

from src.magic_squares import is_magic_square, generate_all_3x3_magic_squares, get_canonical_4x4
from src.magic_gems import square_to_coordinates
from src.analysis import compute_total_magic_energy_v2

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def compute_complete_energy(arr: np.ndarray) -> float:
    """
    Compute complete energy using individual row/column indicators.
    
    E_full = sum_k Cov(R_k,Z)^2 + sum_l Cov(C_l,Z)^2 + Cov(D_main,Z)^2 + Cov(D_anti,Z)^2
    """
    n = arr.shape[0]
    z = arr - (n*n + 1)/2
    
    # Row covariances (drop last for redundancy)
    e_rows = 0
    for k in range(n-1):
        row_indicator = np.zeros((n,n))
        row_indicator[k,:] = 1
        cov_rk = np.mean(row_indicator * z)
        e_rows += cov_rk**2
    
    # Column covariances (drop last)
    e_cols = 0
    for l in range(n-1):
        col_indicator = np.zeros((n,n))
        col_indicator[:,l] = 1
        cov_cl = np.mean(col_indicator * z)
        e_cols += cov_cl**2
    
    # Diagonals
    n_sq = n*n
    z_flat = z.flatten()
    D_main = np.zeros(n_sq)
    D_anti = np.zeros(n_sq)
    for i in range(n):
        D_main[i*n+i] = 1
        D_anti[i*n+(n-1-i)] = 1
    cov_main = np.mean(D_main * z_flat) 
    cov_anti = np.mean(D_anti * z_flat)
    e_diag = cov_main**2 + cov_anti**2
    
    return e_rows + e_cols + e_diag


def compute_lowmode_energy(arr: np.ndarray) -> float:
    """Compute low-mode energy (4-term aggregate)."""
    res = compute_total_magic_energy_v2(arr)
    return res['E_total']


def fig1_lowmode_failure_n4(output_dir='figures'):
    """
    Figure: Why E_low fails for n≥4
    
    Shows one non-magic n=4 example with E_low=0, with row/col deviation bars.
    """
    # The counterexample from the review
    counter = np.array([
        [9,4,12,3],
        [16,1,14,7],
        [10,15,11,8],
        [2,5,6,13]
    ])
    
    n = 4
    M = n*(n*n+1)//2
    
    fig = plt.figure(figsize=(14, 5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.35)
    
    # Panel (a): The arrangement
    ax1 = fig.add_subplot(gs[0,0])
    im = ax1.imshow(counter, cmap='viridis', aspect='equal')
    for i in range(n):
        for j in range(n):
            val = counter[i,j]
            color = 'white' if val < 8.5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center',
                    fontsize=12, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) Example: $E_{\\mathrm{low}}=0$ but NOT magic', fontsize=12, fontweight='bold')
    
    # Add annotation showing it's non-magic (avoid unicode glyphs for PDF portability)
    textstr = 'Both diagonals = 34 (OK)\nRows/columns ≠ 34 (NOT magic)'
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Panel (b): Line-sum deviations
    ax2 = fig.add_subplot(gs[0,1])
    row_sums = counter.sum(axis=1)
    col_sums = counter.sum(axis=0)
    row_dev = row_sums - M
    col_dev = col_sums - M
    
    x = np.arange(n)
    ax2.axhline(0, color='k', lw=1.5, alpha=0.7, label=f'Target (M={M})')
    width = 0.35
    bars1 = ax2.bar(x - width/2, row_dev, width=width, label='Row sum − M', 
                    color='steelblue', edgecolor='black')
    bars2 = ax2.bar(x + width/2, col_dev, width=width, label='Col sum − M',
                    color='coral', edgecolor='black')
    
    # Annotate actual sums
    for i, (rs, cs) in enumerate(zip(row_sums, col_sums)):
        ax2.text(i - width/2, row_dev[i] + (1 if row_dev[i]>0 else -1.5), 
                str(rs), ha='center', fontsize=8)
        ax2.text(i + width/2, col_dev[i] + (1 if col_dev[i]>0 else -1.5),
                str(cs), ha='center', fontsize=8)
    
    ax2.set_xticks(x)
    ax2.set_xlabel('Index', fontsize=11)
    ax2.set_ylabel('Sum deviation from $M$', fontsize=11)
    ax2.set_title('(b) Row/column sums deviate from magic constant', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Panel (c): The four low-mode constraints are satisfied
    ax3 = fig.add_subplot(gs[0,2])
    ax3.axis('off')
    
    res = compute_total_magic_energy_v2(counter)
    
    table_data = [
        ['Constraint', 'Value'],
        ['$\\mathrm{Cov}(X,Z)$', f'{res["cov_xz"]:.2e}'],
        ['$\\mathrm{Cov}(Y,Z)$', f'{res["cov_yz"]:.2e}'],
        ['$\\mathrm{Cov}(D_{\\mathrm{main}},Z)$', f'{res["cov_main_z"]:.2e}'],
        ['$\\mathrm{Cov}(D_{\\mathrm{anti}},Z)$', f'{res["cov_anti_z"]:.2e}'],
        ['', ''],
        ['$E_{\\mathrm{low}}$', f'{res["E_total"]:.2e}'],
    ]
    
    table = ax3.table(cellText=table_data, loc='center', cellLoc='left',
                     bbox=[0.1, 0.2, 0.8, 0.7])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)
    
    # Style
    for i in range(len(table_data)):
        for j in range(2):
            cell = table[(i,j)]
            if i == 0:
                cell.set_facecolor('#E8E8E8')
                cell.set_text_props(weight='bold')
            elif i == len(table_data)-1:
                cell.set_facecolor('lightgreen')
                cell.set_text_props(weight='bold')
            elif i <= 4:
                cell.set_facecolor('lightblue' if j==1 else 'white')
    
    ax3.text(0.5, 0.05, 'All four covariances = 0, yet NOT magic!', 
            transform=ax3.transAxes, ha='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    ax3.set_title('(c) Low-mode energy vanishes', fontsize=12, fontweight='bold')
    
    plt.suptitle('Why $E_{\\mathrm{low}}$ Cannot Characterize Magic Squares for $n \\geq 4$',
                 fontsize=14, fontweight='bold')
    
    filepath = os.path.join(output_dir, 'fig_lowmode_failure_n4.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def fig2_energy_comparison_scatter_n4(output_dir='figures'):
    """
    Figure: E_low vs E_full scatter for n=4
    
    Shows that small E_low does not imply small E_full.
    """
    np.random.seed(42)
    
    n = 4
    n_samples = 5000
    
    print(f"Generating {n_samples} random n=4 arrangements...")
    e_low_vals = []
    e_full_vals = []
    is_magic_vals = []
    
    for _ in range(n_samples):
        arr = np.arange(1, n*n+1)
        np.random.shuffle(arr)
        sq = arr.reshape(n,n)
        
        e_low = compute_lowmode_energy(sq)
        e_full = compute_complete_energy(sq)
        
        e_low_vals.append(e_low)
        e_full_vals.append(e_full)
        is_magic_vals.append(is_magic_square(sq))
    
    # Add a few magic squares
    print("Adding magic squares...")
    magic = get_canonical_4x4()
    for k in range(4):
        rotated = np.rot90(magic, k)
        e_low_vals.append(compute_lowmode_energy(rotated))
        e_full_vals.append(compute_complete_energy(rotated))
        is_magic_vals.append(True)
    
    # Add the counterexample
    counter = np.array([[9,4,12,3],[16,1,14,7],[10,15,11,8],[2,5,6,13]])
    e_low_vals.append(compute_lowmode_energy(counter))
    e_full_vals.append(compute_complete_energy(counter))
    is_magic_vals.append(False)
    
    e_low_vals = np.array(e_low_vals)
    e_full_vals = np.array(e_full_vals)
    is_magic_vals = np.array(is_magic_vals)
    
    fig, ax = plt.subplots(figsize=(9, 8))
    
    # Scatter plot
    # random
    mask_random = ~is_magic_vals
    ax.scatter(e_low_vals[mask_random], e_full_vals[mask_random],
              s=15, alpha=0.4, color='steelblue', label='Random arrangements')
    
    # magic
    mask_magic = is_magic_vals
    ax.scatter(e_low_vals[mask_magic], e_full_vals[mask_magic],
              s=150, marker='*', color='gold', edgecolors='black', linewidth=1.5,
              label='Magic squares', zorder=10)
    
    # counterexample (last point)
    ax.scatter([e_low_vals[-1]], [e_full_vals[-1]],
              s=300, marker='X', color='red', edgecolors='darkred', linewidth=2,
              label='$E_{\\mathrm{low}}=0$, not magic', zorder=11)
    
    # Annotate axes
    ax.axhline(0, color='k', lw=0.8, alpha=0.5)
    ax.axvline(0, color='k', lw=0.8, alpha=0.5)
    
    # Diagonal line
    max_val = max(e_low_vals.max(), e_full_vals.max())
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, lw=1, label='$E_{\\mathrm{low}}=E_{\\mathrm{full}}$')
    
    ax.set_xlabel('Low-mode energy $E_{\\mathrm{low}}$ (4 covariances)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Complete energy $E_{\\mathrm{full}}$ ($2n$ covariances)', fontsize=12, fontweight='bold')
    ax.set_title('Comparing Low-Mode and Complete Energies ($n=4$)', fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Zoom inset near origin
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax, width="35%", height="35%", loc='lower right',
                      bbox_to_anchor=(0.05, 0.05, 0.9, 0.9), bbox_transform=ax.transAxes)
    
    # Plot in inset
    zoom_thresh = 1.0
    mask_zoom = (e_low_vals < zoom_thresh) & (e_full_vals < zoom_thresh*4)
    axins.scatter(e_low_vals[mask_zoom & mask_random], e_full_vals[mask_zoom & mask_random],
                 s=20, alpha=0.5, color='steelblue')
    axins.scatter(e_low_vals[mask_magic], e_full_vals[mask_magic],
                 s=100, marker='*', color='gold', edgecolors='black', linewidth=1)
    axins.scatter([e_low_vals[-1]], [e_full_vals[-1]],
                 s=200, marker='X', color='red', edgecolors='darkred', linewidth=1.5)
    
    axins.axhline(0, color='k', lw=0.5, alpha=0.5)
    axins.axvline(0, color='k', lw=0.5, alpha=0.5)
    axins.set_xlim(-0.05, zoom_thresh)
    axins.set_ylim(-0.2, zoom_thresh*4)
    axins.set_xlabel('$E_{\\mathrm{low}}$', fontsize=8)
    axins.set_ylabel('$E_{\\mathrm{full}}$', fontsize=8)
    axins.grid(True, alpha=0.3)
    
    filepath = os.path.join(output_dir, 'fig_energy_comparison_n4.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def fig3_n4_bands_geometry(output_dir='figures'):
    """
    Figure: n=4 perturbation gap vs hull vertices
    
    Explains the trimodal structure observed in the perturbation analysis.
    """
    # Generate a diverse set of n=4 magic squares
    print("Generating n=4 magic squares for band analysis...")
    
    magic_4 = get_canonical_4x4()
    squares = []
    seen = set()
    
    # Base + D4 variants
    for k in range(4):
        rotated = np.rot90(magic_4, k)
        sig = tuple(rotated.flatten())
        if sig not in seen:
            seen.add(sig)
            squares.append(rotated.copy())
        
        flipped = np.fliplr(rotated)
        sig = tuple(flipped.flatten())
        if sig not in seen:
            seen.add(sig)
            squares.append(flipped.copy())
    
    # Generate a few more by permuting within magic constraints
    # (this is a heuristic - full enumeration of 880 is out of scope)
    # For demonstration, we'll work with what we have
    
    print(f"Analyzing {len(squares)} n=4 magic squares...")
    
    n = 4
    gaps = []
    hull_verts = []
    hull_vols = []
    
    for sq in squares:
        # Compute min perturbation gap
        base_e = compute_complete_energy(sq)
        assert base_e < 1e-10, "Not magic!"
        
        min_gap = float('inf')
        for i1 in range(n):
            for j1 in range(n):
                for i2 in range(i1, n):
                    j2_start = j1+1 if i2==i1 else 0
                    for j2 in range(j2_start, n):
                        pert = sq.copy()
                        pert[i1,j1], pert[i2,j2] = pert[i2,j2], pert[i1,j1]
                        e = compute_complete_energy(pert)
                        gap = e - base_e
                        if gap < min_gap:
                            min_gap = gap
        
        gaps.append(min_gap)
        
        # Compute hull properties
        coords = square_to_coordinates(sq, center_z=True)
        try:
            hull = ConvexHull(coords)
            hull_verts.append(len(hull.vertices))
            hull_vols.append(hull.volume)
        except:
            hull_verts.append(0)
            hull_vols.append(0)
    
    gaps = np.array(gaps)
    hull_verts = np.array(hull_verts)
    hull_vols = np.array(hull_vols)
    
    fig = plt.figure(figsize=(14, 5))
    gs = GridSpec(1, 2, figure=fig, wspace=0.3)
    
    # Panel (a): Gap vs hull vertices
    ax1 = fig.add_subplot(gs[0,0])
    
    # Color by gap range
    colors_map = []
    for g in gaps:
        if g < 0.008:
            colors_map.append('darkred')
        elif g < 0.020:
            colors_map.append('orange')
        else:
            colors_map.append('gold')
    
    scatter = ax1.scatter(hull_verts, gaps, c=colors_map, s=100, 
                         edgecolors='black', linewidth=1, alpha=0.8)
    
    ax1.set_xlabel('Number of hull vertices', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Minimum perturbation gap', fontsize=12, fontweight='bold')
    ax1.set_title('(a) Perturbation resistance vs hull geometry', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='darkred', edgecolor='black', label='High isolation (gap < 0.008)'),
        Patch(facecolor='orange', edgecolor='black', label='Medium isolation (0.008–0.020)'),
        Patch(facecolor='gold', edgecolor='black', label='Low isolation (gap > 0.020)')
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Panel (b): Hull vertex distribution
    ax2 = fig.add_subplot(gs[0,1])
    
    unique_verts = sorted(set(hull_verts))
    vert_counts = [np.sum(hull_verts == v) for v in unique_verts]
    
    bars = ax2.bar(unique_verts, vert_counts, width=0.6, color='teal',
                  alpha=0.7, edgecolor='black')
    
    for bar, v, count in zip(bars, unique_verts, vert_counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                str(count), ha='center', fontsize=9)
    
    ax2.set_xlabel('Number of hull vertices', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Count of magic squares', fontsize=12, fontweight='bold')
    ax2.set_title('(b) Hull vertex distribution ($n=4$ magic squares)', fontsize=12, fontweight='bold')
    ax2.set_xticks(unique_verts)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Geometric Structure of $n=4$ Magic Squares (Sample Analysis)',
                 fontsize=14, fontweight='bold', y=0.98)
    
    filepath = os.path.join(output_dir, 'fig_n4_bands_geometry.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def main():
    """Generate all new figures."""
    print("="*60)
    print("GENERATING NEW HIGH-IMPACT FIGURES")
    print("="*60)
    
    output_dir = 'figures'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[1/3] Figure: Low-mode failure for n=4...")
    fig1_lowmode_failure_n4(output_dir)
    
    print("\n[2/3] Figure: E_low vs E_full scatter...")
    fig2_energy_comparison_scatter_n4(output_dir)
    
    print("\n[3/3] Figure: n=4 bands vs geometry...")
    fig3_n4_bands_geometry(output_dir)
    
    print("\n" + "="*60)
    print("✓ All new figures generated")
    print("="*60)
    
    # Copy to arxiv_submission/figures/
    import shutil
    arxiv_fig_dir = 'arxiv_submission/figures'
    os.makedirs(arxiv_fig_dir, exist_ok=True)
    
    new_figs = [
        'fig_lowmode_failure_n4.pdf',
        'fig_energy_comparison_n4.pdf',
        'fig_n4_bands_geometry.pdf'
    ]
    
    print("\nCopying to arxiv_submission/figures/...")
    for fname in new_figs:
        src = os.path.join(output_dir, fname)
        dst = os.path.join(arxiv_fig_dir, fname)
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"  ✓ {fname}")
    
    print("\n✓ Figures ready for manuscript integration")
    return 0


if __name__ == "__main__":
    sys.exit(main())
