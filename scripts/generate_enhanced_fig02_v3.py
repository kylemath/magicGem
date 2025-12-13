"""
Generate enhanced Figure 2 V3 - Clean web app style presentation.

Layout:
- Top row: Construction process (4 steps)
- Bottom 2 rows: 8 D4 symmetries with small number grids above large prominent gems
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.magic_squares import get_canonical_3x3, generate_all_3x3_magic_squares
from src.magic_gems import square_to_coordinates

# Style settings
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'axes.labelsize': 7,
    'axes.titlesize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def plot_magic_square_tiny(ax, square, title):
    """Plot a compact magic square."""
    im = ax.imshow(square, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = int(square[i, j])
            color = 'white' if val < 5 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=7, fontweight='bold', color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=7, fontweight='bold', pad=2)


def plot_3d_gem_large(ax, square, title, elev=20, azim=45, show_hull=True):
    """Plot a large, prominent Magic Gem with minimal axes."""
    coords = square_to_coordinates(square, center_z=True)
    
    # Plot points - larger and more prominent
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
              c=coords[:, 2], cmap='viridis', s=120, 
              edgecolors='black', linewidth=1.2, alpha=1.0, zorder=10)
    
    # Show hull with more opacity
    if show_hull:
        try:
            hull = ConvexHull(coords)
            for simplex in hull.simplices:
                pts = coords[simplex]
                tri = Poly3DCollection([pts], alpha=0.25, facecolor='cyan', 
                                       edgecolor='darkblue', linewidth=0.6)
                ax.add_collection3d(tri)
        except:
            pass
    
    # Small origin marker
    ax.scatter([0], [0], [0], c='red', s=25, marker='x', linewidth=1.5, alpha=0.6, zorder=5)
    
    # Very light axes through origin - barely visible
    lim = 1.2
    ax.plot([-lim, lim], [0, 0], [0, 0], 'k--', alpha=0.08, linewidth=0.5)
    ax.plot([0, 0], [-lim, lim], [0, 0], 'k--', alpha=0.08, linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-lim, lim], 'k--', alpha=0.08, linewidth=0.5)
    
    # Minimal axis labels with light color
    ax.set_xlabel('X', fontsize=6, color='gray', alpha=0.5)
    ax.set_ylabel('Y', fontsize=6, color='gray', alpha=0.5)
    ax.set_zlabel('Z', fontsize=6, color='gray', alpha=0.5)
    ax.set_title(title, fontsize=8, fontweight='bold', pad=4)
    
    # Set view
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-5, 5)
    
    # Very light tick labels
    ax.tick_params(labelsize=5, colors='gray', labelcolor='lightgray')
    ax.set_box_aspect([1, 1, 1.5])
    
    # Make panes almost transparent
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('gray')
    ax.yaxis.pane.set_edgecolor('gray')
    ax.zaxis.pane.set_edgecolor('gray')
    ax.xaxis.pane.set_alpha(0.1)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)
    
    # Lighten grid
    ax.grid(True, alpha=0.1)


def create_enhanced_fig02_v3(filepath=None):
    """
    Create enhanced Figure 2 V3 - web app style with prominent gems.
    """
    lo_shu = get_canonical_3x3()
    all_symmetries = generate_all_3x3_magic_squares()
    
    # Create figure with clean layout
    fig = plt.figure(figsize=(16, 11))
    gs = gridspec.GridSpec(5, 8, figure=fig, hspace=0.6, wspace=0.4,
                          height_ratios=[1.2, 0.15, 0.6, 1.4, 1.4])
    
    # ========================================
    # SECTION 1: Construction Process (Row 0)
    # ========================================
    
    # Panel (a): Magic Square
    ax1 = fig.add_subplot(gs[0, 0:2])
    im = ax1.imshow(lo_shu, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = int(lo_shu[i, j])
            color = 'white' if val < 5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=13, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) Lo Shu Magic Square', fontsize=10, fontweight='bold')
    
    # Panel (b): Centered Grid
    ax2 = fig.add_subplot(gs[0, 2:4])
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    for i in range(3):
        for j in range(3):
            x, y = j - 1, 1 - i
            ax2.scatter(x, y, s=220, c='steelblue', edgecolors='black', linewidth=1.5)
            ax2.text(x, y - 0.35, f'({x},{y})', ha='center', fontsize=7)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    ax2.set_xlabel('X', fontsize=8)
    ax2.set_ylabel('Y', fontsize=8)
    ax2.set_title('(b) Centered Grid', fontsize=10, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Panel (c): Add Z
    ax3 = fig.add_subplot(gs[0, 4:6], projection='3d')
    coords_uncentered = square_to_coordinates(lo_shu, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=80, edgecolors='black', linewidth=1)
    ax3.set_xlabel('X', fontsize=7, color='gray')
    ax3.set_ylabel('Y', fontsize=7, color='gray')
    ax3.set_zlabel('Z', fontsize=7, color='gray')
    ax3.set_title('(c) Add Z (values)', fontsize=10, fontweight='bold')
    ax3.tick_params(labelsize=6, colors='gray')
    ax3.xaxis.pane.set_alpha(0.1)
    ax3.yaxis.pane.set_alpha(0.1)
    ax3.zaxis.pane.set_alpha(0.1)
    
    # Panel (d): Magic Gem
    ax4 = fig.add_subplot(gs[0, 6:8], projection='3d')
    plot_3d_gem_large(ax4, lo_shu, '(d) Magic Gem', elev=20, azim=45, show_hull=True)
    
    # ========================================
    # SECTION 2: D4 Symmetries Title (Row 1)
    # ========================================
    ax_title = fig.add_subplot(gs[1, :])
    ax_title.text(0.5, 0.5, 'D₄ Symmetry Group: Eight Magic Squares → One 3D Magic Gem', 
                 ha='center', va='center', fontsize=11, fontweight='bold',
                 style='italic', color='darkblue')
    ax_title.axis('off')
    
    # ========================================
    # SECTION 3: 8 D4 Symmetries (Rows 2-4)
    # Small 2D squares (row 2) + Large 3D gems (rows 3-4)
    # ========================================
    
    # Different viewing angles to show it's the same object
    viewing_angles = [
        (20, 45),   # variant 1
        (20, 135),  # variant 2
        (20, 225),  # variant 3
        (20, 315),  # variant 4
        (20, 90),   # variant 5
        (20, 180),  # variant 6
        (20, 270),  # variant 7
        (20, 0),    # variant 8
    ]
    
    labels = ['(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)']
    symmetry_names = ['R0°', 'R90°', 'R180°', 'R270°', 
                     'H-flip', 'V-flip', 'D1-flip', 'D2-flip']
    
    for idx in range(8):
        col = idx % 4
        row_offset = 0 if idx < 4 else 1
        
        square = all_symmetries[idx]
        elev, azim = viewing_angles[idx]
        label = labels[idx]
        sym_name = symmetry_names[idx]
        
        # Small 2D square on top (row 2)
        ax_sq = fig.add_subplot(gs[2, col*2:col*2+2])
        plot_magic_square_tiny(ax_sq, square, f'{label} {sym_name}')
        
        # Large 3D gem below (rows 3-4)
        ax_3d = fig.add_subplot(gs[3+row_offset, col*2:col*2+2], projection='3d')
        plot_3d_gem_large(ax_3d, square, f'3D view (az={azim}°)', 
                         elev=elev, azim=azim, show_hull=True)
    
    # Main title
    title_text = ('Construction and D₄ Symmetry Structure\n'
                  'Top: Construction process. Bottom: All eight D₄ symmetries produce the same 3D Magic Gem.')
    fig.suptitle(title_text, fontsize=11, fontweight='bold', y=0.995)
    
    if filepath:
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Saved: {filepath}")
        plt.close(fig)
    
    return fig


if __name__ == "__main__":
    # Generate for arxiv_submission
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'arxiv_submission', 'figures', 
                               'fig02_combined_construction_symmetries.pdf')
    
    print("Generating enhanced Figure 2 V3 (web app style)...")
    print("  - Clean, minimal axes")
    print("  - Large, prominent 3D Magic Gems")
    print("  - Compact number grids")
    print("  - Focus on 8 D4 symmetries")
    
    create_enhanced_fig02_v3(output_path)
    
    # Also save to main figures directory
    output_path2 = os.path.join(os.path.dirname(__file__), 
                                '..', 'figures', 
                                'fig02_combined_construction_symmetries.pdf')
    create_enhanced_fig02_v3(output_path2)
    
    print("\nDone! Clean web-app-style presentation:")
    print("  ✓ Gems are large and prominent")
    print("  ✓ Axes are lightened and minimal")
    print("  ✓ Number grids are compact")
    print("  ✓ Focus on the 8 D4 symmetries")
