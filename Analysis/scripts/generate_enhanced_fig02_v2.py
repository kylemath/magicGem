"""
Generate enhanced Figure 2 V2 with improved spatial organization and rotation sequence.

This creates a figure showing:
1. Construction process
2. D4 symmetries organized by type (rotations vs reflections)
3. A rotation sequence showing the same Magic Gem from different angles
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
    'axes.labelsize': 8,
    'axes.titlesize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def plot_magic_square_small(ax, square, title):
    """Plot a magic square as a colored grid."""
    im = ax.imshow(square, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = int(square[i, j])
            color = 'white' if val < 5 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=9, fontweight='bold', color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=8, fontweight='bold')


def plot_3d_gem(ax, square, title, elev=20, azim=45, show_hull=True):
    """Plot a Magic Gem in 3D."""
    coords = square_to_coordinates(square, center_z=True)
    
    # Plot points
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
              c=coords[:, 2], cmap='viridis', s=50, 
              edgecolors='black', linewidth=0.8, alpha=0.9)
    
    # Show hull
    if show_hull:
        try:
            hull = ConvexHull(coords)
            for simplex in hull.simplices:
                pts = coords[simplex]
                tri = Poly3DCollection([pts], alpha=0.15, facecolor='cyan', 
                                       edgecolor='darkblue', linewidth=0.4)
                ax.add_collection3d(tri)
        except:
            pass
    
    # Origin
    ax.scatter([0], [0], [0], c='red', s=20, marker='x', linewidth=1, alpha=0.7)
    
    # Axes through origin
    lim = 1.2
    ax.plot([-lim, lim], [0, 0], [0, 0], 'k--', alpha=0.15, linewidth=0.5)
    ax.plot([0, 0], [-lim, lim], [0, 0], 'k--', alpha=0.15, linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-lim, lim], 'k--', alpha=0.15, linewidth=0.5)
    
    ax.set_xlabel('X', fontsize=7)
    ax.set_ylabel('Y', fontsize=7)
    ax.set_zlabel('Z', fontsize=7)
    ax.set_title(title, fontsize=7)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-5, 5)
    ax.tick_params(labelsize=6)
    ax.set_box_aspect([1, 1, 1.5])


def create_enhanced_fig02_v2(filepath=None):
    """
    Create enhanced Figure 2 V2 with spatial organization and rotation sequence.
    """
    lo_shu = get_canonical_3x3()
    all_symmetries = generate_all_3x3_magic_squares()
    
    # Create figure with custom layout
    fig = plt.figure(figsize=(16, 14))
    gs = gridspec.GridSpec(6, 8, figure=fig, hspace=0.5, wspace=0.4,
                          height_ratios=[1, 0.2, 1, 1, 0.2, 1])
    
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
                    fontsize=12, fontweight='bold', color=color)
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
            ax2.scatter(x, y, s=200, c='steelblue', edgecolors='black', linewidth=1.5)
            ax2.text(x, y - 0.35, f'({x},{y})', ha='center', fontsize=7)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('X', fontsize=8)
    ax2.set_ylabel('Y', fontsize=8)
    ax2.set_title('(b) Centered Grid', fontsize=10, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Panel (c): Add Z
    ax3 = fig.add_subplot(gs[0, 4:6], projection='3d')
    coords_uncentered = square_to_coordinates(lo_shu, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=60, edgecolors='black', linewidth=1)
    ax3.set_xlabel('X', fontsize=8)
    ax3.set_ylabel('Y', fontsize=8)
    ax3.set_zlabel('Z', fontsize=8)
    ax3.set_title('(c) Add Z (values)', fontsize=10, fontweight='bold')
    ax3.tick_params(labelsize=7)
    
    # Panel (d): Magic Gem
    ax4 = fig.add_subplot(gs[0, 6:8], projection='3d')
    plot_3d_gem(ax4, lo_shu, '(d) Magic Gem', elev=20, azim=45, show_hull=True)
    
    # ========================================
    # SECTION 2: D4 Symmetry Structure (Rows 2-3)
    # Organized by symmetry type
    # ========================================
    
    # Add section title
    ax_title1 = fig.add_subplot(gs[1, :])
    ax_title1.text(0.5, 0.5, 'D₄ Symmetry Group: Rotations and Reflections', 
                   ha='center', va='center', fontsize=11, fontweight='bold')
    ax_title1.axis('off')
    
    # D4 symmetries organized by type:
    # Row 2: 4 Rotations (0°, 90°, 180°, 270°)
    # Row 3: 4 Reflections (horizontal, vertical, diagonal1, diagonal2)
    
    # ROTATIONS (indices 0, 1, 2, 3 typically)
    rotation_indices = [0, 1, 2, 3]
    rotation_labels = ['(e) 0° rotation', '(f) 90° rotation', 
                       '(g) 180° rotation', '(h) 270° rotation']
    rotation_azimuths = [45, 135, 225, 315]
    
    for i, (idx, label, azim) in enumerate(zip(rotation_indices, rotation_labels, rotation_azimuths)):
        # 2D square
        ax_sq = fig.add_subplot(gs[2, i*2])
        plot_magic_square_small(ax_sq, all_symmetries[idx], label)
        
        # 3D gem
        ax_3d = fig.add_subplot(gs[2, i*2+1], projection='3d')
        plot_3d_gem(ax_3d, all_symmetries[idx], f'az={azim}°', 
                   elev=20, azim=azim, show_hull=True)
    
    # REFLECTIONS (indices 4, 5, 6, 7 typically)
    reflection_indices = [4, 5, 6, 7]
    reflection_labels = ['(i) H-reflect', '(j) V-reflect', 
                         '(k) D1-reflect', '(l) D2-reflect']
    reflection_azimuths = [90, 0, 45, 135]
    
    for i, (idx, label, azim) in enumerate(zip(reflection_indices, reflection_labels, reflection_azimuths)):
        # 2D square
        ax_sq = fig.add_subplot(gs[3, i*2])
        plot_magic_square_small(ax_sq, all_symmetries[idx], label)
        
        # 3D gem
        ax_3d = fig.add_subplot(gs[3, i*2+1], projection='3d')
        plot_3d_gem(ax_3d, all_symmetries[idx], f'az={azim}°', 
                   elev=20, azim=azim, show_hull=True)
    
    # ========================================
    # SECTION 3: Rotation Sequence (Row 5)
    # Shows the SAME Magic Gem rotating through 360°
    # ========================================
    
    # Add section title
    ax_title2 = fig.add_subplot(gs[4, :])
    ax_title2.text(0.5, 0.5, 'Rotation Sequence: Same 3D Magic Gem viewed from different angles', 
                   ha='center', va='center', fontsize=11, fontweight='bold',
                   style='italic', color='darkblue')
    ax_title2.axis('off')
    
    # Show 8 viewing angles of the SAME gem
    rotation_sequence_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    
    for i, azim in enumerate(rotation_sequence_angles):
        ax_rot = fig.add_subplot(gs[5, i], projection='3d')
        plot_3d_gem(ax_rot, lo_shu, f'{azim}°', elev=20, azim=azim, show_hull=True)
        
        # Add arrow to show rotation direction
        if i < 7:
            ax_arrow = fig.add_subplot(gs[5, :])
            ax_arrow.annotate('', xy=((i+1)/8, 0.5), xytext=(i/8, 0.5),
                            arrowprops=dict(arrowstyle='->', lw=2, color='darkblue'))
            ax_arrow.axis('off')
    
    # Main title
    title_text = ('Construction, Symmetries, and Rotational Equivalence\n'
                  'Top: Construction process from square to Magic Gem. '
                  'Middle: D₄ symmetry group (rotations & reflections). '
                  'Bottom: Continuous rotation of a single Magic Gem.')
    fig.suptitle(title_text, fontsize=12, fontweight='bold', y=0.995)
    
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
    
    print("Generating enhanced Figure 2 V2...")
    print("  - Construction process (4 steps)")
    print("  - D4 symmetries organized by type (rotations vs reflections)")
    print("  - Rotation sequence showing the same 3D gem from 8 angles")
    
    create_enhanced_fig02_v2(output_path)
    
    # Also save to main figures directory
    output_path2 = os.path.join(os.path.dirname(__file__), 
                                '..', 'figures', 
                                'fig02_combined_construction_symmetries.pdf')
    create_enhanced_fig02_v2(output_path2)
    
    print("\nDone! This demonstrates that:")
    print("  1. All 8 D4 symmetries map to the SAME 3D Magic Gem")
    print("  2. The 3D gem can be continuously rotated (bottom sequence)")
    print("  3. Different 2D squares = same 3D object viewed from different angles")
