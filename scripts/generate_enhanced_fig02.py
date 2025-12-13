"""
Generate enhanced Figure 2 with 3D Magic Gem visualizations for each D4 symmetry.

This script creates a comprehensive figure showing:
1. The construction process (as before)
2. 3D Magic Gem views for each of the 8 D4 symmetries
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
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def create_enhanced_fig02(filepath=None):
    """
    Create enhanced Figure 2 with construction process and 3D gems for all symmetries.
    """
    lo_shu = get_canonical_3x3()
    all_symmetries = generate_all_3x3_magic_squares()
    
    # Create figure
    fig = plt.figure(figsize=(16, 16))
    
    # Use GridSpec for better control
    gs = gridspec.GridSpec(5, 4, figure=fig, hspace=0.4, wspace=0.3)
    
    # ========================================
    # TOP ROW: Construction Process (4 panels)
    # ========================================
    
    # Panel (a): Magic Square
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(lo_shu, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = int(lo_shu[i, j])
            color = 'white' if val < 5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=11, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) Magic Square\n(Lo Shu)', fontsize=10, fontweight='bold')
    
    # Panel (b): Centered Grid
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    for i in range(3):
        for j in range(3):
            x, y = j - 1, 1 - i
            ax2.scatter(x, y, s=200, c='steelblue', edgecolors='black', linewidth=1.5)
            ax2.text(x, y - 0.35, f'({x},{y})', ha='center', fontsize=7)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('X', fontsize=8)
    ax2.set_ylabel('Y', fontsize=8)
    ax2.set_title('(b) Centered Grid\n(Origin at center)', fontsize=10, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Panel (c): Add Z dimension
    ax3 = fig.add_subplot(gs[0, 2], projection='3d')
    coords_uncentered = square_to_coordinates(lo_shu, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=60, edgecolors='black', linewidth=1)
    ax3.set_xlabel('X', fontsize=8)
    ax3.set_ylabel('Y', fontsize=8)
    ax3.set_zlabel('Z', fontsize=8)
    ax3.set_title('(c) Add Z\n(Square values)', fontsize=10, fontweight='bold')
    ax3.tick_params(labelsize=7)
    
    # Panel (d): Magic Gem with hull
    ax4 = fig.add_subplot(gs[0, 3], projection='3d')
    coords = square_to_coordinates(lo_shu, center_z=True)
    ax4.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=60, edgecolors='black', linewidth=1)
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.2, facecolor='cyan', 
                                   edgecolor='darkblue', linewidth=0.5)
            ax4.add_collection3d(tri)
    except:
        pass
    ax4.scatter([0], [0], [0], c='red', s=30, marker='x', linewidth=1.5)
    ax4.set_xlabel('X', fontsize=8)
    ax4.set_ylabel('Y', fontsize=8)
    ax4.set_zlabel('Z', fontsize=8)
    ax4.set_title('(d) Magic Gem\n(Centered, with hull)', fontsize=10, fontweight='bold')
    ax4.view_init(elev=20, azim=45)
    ax4.tick_params(labelsize=7)
    
    # ========================================
    # ROWS 2-5: D4 Symmetries with 3D Gems
    # Two variants per row: 2D square + 3D gem
    # ========================================
    
    # Different viewing angles for visual variety
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
    
    labels = ['e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    
    for idx, (square, angles, label) in enumerate(zip(all_symmetries, viewing_angles, labels)):
        row = 1 + idx // 2
        col = (idx % 2) * 2
        
        # 2D magic square
        ax_2d = fig.add_subplot(gs[row, col])
        im = ax_2d.imshow(square, cmap='viridis', aspect='equal')
        for i in range(3):
            for j in range(3):
                val = int(square[i, j])
                color = 'white' if val < 5 else 'black'
                ax_2d.text(j, i, str(val), ha='center', va='center', 
                          fontsize=10, fontweight='bold', color=color)
        ax_2d.set_xticks([])
        ax_2d.set_yticks([])
        ax_2d.set_title(f'({label}) D₄ variant {idx + 1}', fontsize=9, fontweight='bold')
        
        # 3D Magic Gem
        ax_3d = fig.add_subplot(gs[row, col + 1], projection='3d')
        coords = square_to_coordinates(square, center_z=True)
        ax_3d.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                     c=coords[:, 2], cmap='viridis', s=60, edgecolors='black', linewidth=1)
        
        # Show hull
        try:
            hull = ConvexHull(coords)
            for simplex in hull.simplices:
                pts = coords[simplex]
                tri = Poly3DCollection([pts], alpha=0.2, facecolor='cyan', 
                                       edgecolor='darkblue', linewidth=0.5)
                ax_3d.add_collection3d(tri)
        except:
            pass
        
        ax_3d.scatter([0], [0], [0], c='red', s=20, marker='x', linewidth=1)
        
        elev, azim = angles
        ax_3d.view_init(elev=elev, azim=azim)
        ax_3d.set_xlim(-1.5, 1.5)
        ax_3d.set_ylim(-1.5, 1.5)
        ax_3d.set_zlim(-5, 5)
        ax_3d.set_xlabel('X', fontsize=7)
        ax_3d.set_ylabel('Y', fontsize=7)
        ax_3d.set_zlabel('Z', fontsize=7)
        ax_3d.set_title(f'3D Magic Gem (az={azim}°)', fontsize=8)
        ax_3d.tick_params(labelsize=6)
    
    # Add main title
    fig.suptitle('Construction process and symmetry structure\n' + 
                 'Top row: Construction from magic square to Magic Gem. ' +
                 'Bottom rows: All 8 D₄ symmetries shown as both 2D squares and 3D Magic Gems.',
                 fontsize=12, fontweight='bold', y=0.995)
    
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
    
    print("Generating enhanced Figure 2 with 3D Magic Gem views...")
    create_enhanced_fig02(output_path)
    
    # Also save to main figures directory
    output_path2 = os.path.join(os.path.dirname(__file__), 
                                '..', 'figures', 
                                'fig02_combined_construction_symmetries.pdf')
    create_enhanced_fig02(output_path2)
    
    print("\nDone! Enhanced Figure 2 shows:")
    print("  - Construction process (4 steps)")
    print("  - All 8 D4 symmetries as 2D squares")
    print("  - All 8 D4 symmetries as 3D Magic Gems from different viewing angles")
    print("  This demonstrates that all symmetries yield the SAME 3D Magic Gem!")
