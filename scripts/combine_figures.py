"""
combine_figures.py
==================
Combine multiple figures into multi-panel layouts for journal submission.
Reduces the total number of figures while preserving all content.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from PIL import Image
import matplotlib.image as mpimg

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.magic_squares import get_canonical_3x3, get_canonical_4x4, generate_all_3x3_magic_squares, siamese_method
from src.magic_gems import square_to_coordinates
from src.analysis import test_zero_covariance

# Style settings
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


def create_combined_figure_2(output_dir='figures'):
    """
    Figure 2: Construction and Symmetries (6-panel layout)
    Combines fig02_construction_3x3.pdf + fig05_symmetries.pdf
    
    Top row: 4-panel construction process
    Bottom row: 8 D4 symmetry variants (4x2 subgrid)
    """
    lo_shu = get_canonical_3x3()
    magic_squares = generate_all_3x3_magic_squares()
    
    fig = plt.figure(figsize=(16, 10))
    
    # Create gridspec for layout
    gs = GridSpec(2, 4, figure=fig, height_ratios=[1, 0.8], hspace=0.3)
    
    # --- TOP ROW: Construction Process ---
    # Step 1: Magic Square
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(lo_shu, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = lo_shu[i, j]
            color = 'white' if val < 5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=14, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) Magic Square\n(Lo Shu)', fontsize=11, fontweight='bold')
    
    # Step 2: Centered Grid
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    for i in range(3):
        for j in range(3):
            x, y = j - 1, 1 - i
            ax2.scatter(x, y, s=200, c='steelblue', edgecolors='black')
            ax2.text(x, y - 0.3, f'({x},{y})', ha='center', fontsize=8)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('(b) Centered Grid\n(Origin at center)', fontsize=11, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Step 3: Add Z dimension
    ax3 = fig.add_subplot(gs[0, 2], projection='3d')
    coords_uncentered = square_to_coordinates(lo_shu, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=80, edgecolors='black')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z (value)')
    ax3.set_title('(c) Add Z\n(Square values)', fontsize=11, fontweight='bold')
    
    # Step 4: Center Z and form gem
    ax4 = fig.add_subplot(gs[0, 3], projection='3d')
    coords = square_to_coordinates(lo_shu, center_z=True)
    ax4.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=80, edgecolors='black')
    ax4.scatter([0], [0], [0], c='red', s=50, marker='x')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.15, facecolor='cyan', edgecolor='darkblue')
            ax4.add_collection3d(tri)
    except:
        pass
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z (centered)')
    ax4.set_title('(d) Magic Gem\n(Centered, with hull)', fontsize=11, fontweight='bold')
    
    # --- BOTTOM ROW: D4 Symmetries (2x4 grid) ---
    gs_bottom = GridSpec(2, 4, figure=fig, top=0.42, bottom=0.02, hspace=0.15, wspace=0.15)
    
    for idx, sq in enumerate(magic_squares):
        row = idx // 4
        col = idx % 4
        ax = fig.add_subplot(gs_bottom[row, col])
        im = ax.imshow(sq, cmap='viridis', aspect='equal')
        
        for i in range(3):
            for j in range(3):
                val = sq[i, j]
                color = 'white' if val < 5 else 'black'
                ax.text(j, i, str(val), ha='center', va='center', 
                       fontsize=10, fontweight='bold', color=color)
        
        ax.set_xticks([])
        ax.set_yticks([])
        label = chr(ord('e') + idx)  # e, f, g, h, i, j, k, l
        ax.set_title(f'({label}) D₄ variant {idx + 1}', fontsize=9)
    
    filepath = os.path.join(output_dir, 'fig02_combined_construction_symmetries.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def create_combined_figure_3(output_dir='figures'):
    """
    Figure 3: 3×3 Geometric Analysis (4-panel layout)
    Combines: Magic Gem, Vectors, Covariance, Hull Volume
    """
    lo_shu = get_canonical_3x3()
    np.random.seed(42)
    
    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.25, wspace=0.25)
    
    # --- Panel (a): Magic Gem 3D ---
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    coords = square_to_coordinates(lo_shu, center_z=True)
    scatter = ax1.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                         c=coords[:, 2], cmap='viridis', s=100, edgecolors='black', linewidth=1)
    for i, (x, y, z) in enumerate(coords):
        ax1.text(x, y, z + 0.3, str(lo_shu.flatten()[i]), fontsize=8, ha='center')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.2, facecolor='cyan', 
                                   edgecolor='darkblue', linewidth=0.5)
            ax1.add_collection3d(tri)
    except:
        pass
    # Draw subtle axis lines
    ax1.plot([-1.2, 1.2], [0, 0], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
    ax1.plot([0, 0], [-1.2, 1.2], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
    ax1.plot([0, 0], [0, 0], [-4.5, 4.5], 'k--', alpha=0.3, linewidth=0.5)
    ax1.scatter([0], [0], [0], c='red', s=50, marker='x', linewidth=2)
    # Set axis limits to match data range closely
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_zlim(-5, 5)
    ax1.set_xlabel('X (Column)')
    ax1.set_ylabel('Y (Row)')
    ax1.set_zlabel('Z (Value)')
    ax1.set_title('(a) 3×3 Magic Gem', fontsize=12, fontweight='bold')
    
    # --- Panel (b): Vector Representation ---
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax2.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.1, linewidth=1.5)
    ax2.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=80, edgecolors='black')
    ax2.scatter([0], [0], [0], c='red', s=100, marker='o', label='Origin')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('(b) Vector Representation', fontsize=12, fontweight='bold')
    
    # --- Panel (c): Covariance Distributions ---
    ax3 = fig.add_subplot(gs[1, 0])
    n_random = 5000
    random_cov_xz = []
    random_cov_yz = []
    for _ in range(n_random):
        arr = np.arange(1, 10)
        np.random.shuffle(arr)
        sq = arr.reshape(3, 3)
        coords_rand = square_to_coordinates(sq)
        cov = test_zero_covariance(coords_rand)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    ax3.hist(random_cov_xz, bins=50, alpha=0.5, color='steelblue', 
             label='Cov(X,Z) Random', density=True)
    ax3.hist(random_cov_yz, bins=50, alpha=0.5, color='coral', 
             label='Cov(Y,Z) Random', density=True)
    ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic (all = 0)')
    ax3.set_xlabel('Covariance')
    ax3.set_ylabel('Density')
    ax3.set_title('(c) Covariance: Magic vs 5000 Random', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper right', fontsize=9)
    
    # --- Panel (d): Hull Volume Distribution ---
    ax4 = fig.add_subplot(gs[1, 1])
    volumes = []
    for _ in range(5000):
        arr = np.arange(1, 10)
        np.random.shuffle(arr)
        sq = arr.reshape(3, 3)
        coords_rand = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords_rand)
            volumes.append(hull.volume)
        except:
            pass
    
    # Magic volume
    coords_magic = square_to_coordinates(lo_shu)
    hull_magic = ConvexHull(coords_magic)
    magic_vol = hull_magic.volume
    
    ax4.hist(volumes, bins=50, alpha=0.7, color='steelblue', label='Random', density=True)
    ax4.axvline(x=magic_vol, color='red', linestyle='--', linewidth=2, 
               label=f'Magic ({magic_vol:.2f})')
    ax4.set_xlabel('Convex Hull Volume')
    ax4.set_ylabel('Density')
    ax4.set_title('(d) Hull Volume Distribution', fontsize=12, fontweight='bold')
    ax4.legend()
    
    filepath = os.path.join(output_dir, 'fig03_combined_3x3_analysis.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def create_combined_figure_4(output_dir='figures'):
    """
    Figure 4: 4×4 Complete Analysis (6-panel layout)
    Combines: Magic Square, Construction, Magic Gem, Vectors, Covariance, Hull Volume
    """
    magic_4 = get_canonical_4x4()
    np.random.seed(42)
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # --- Panel (a): Magic Square ---
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(magic_4, cmap='viridis', aspect='equal')
    for i in range(4):
        for j in range(4):
            val = magic_4[i, j]
            color = 'white' if val < 8.5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=11, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) 4×4 Magic Square\nM(4) = 34', fontsize=11, fontweight='bold')
    
    # --- Panel (b): Magic Gem 3D ---
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    coords = square_to_coordinates(magic_4, center_z=True)
    scatter = ax2.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                         c=coords[:, 2], cmap='viridis', s=80, edgecolors='black')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.15, facecolor='cyan', 
                                   edgecolor='darkblue', linewidth=0.4)
            ax2.add_collection3d(tri)
    except:
        pass
    ax2.scatter([0], [0], [0], c='red', s=50, marker='x')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('(b) 4×4 Magic Gem', fontsize=11, fontweight='bold')
    
    # --- Panel (c): Vector Representation ---
    ax3 = fig.add_subplot(gs[0, 2], projection='3d')
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax3.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.06, linewidth=1.2)
    ax3.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=70, edgecolors='black')
    ax3.scatter([0], [0], [0], c='red', s=100, marker='o')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('(c) 16 Vectors from Centroid', fontsize=11, fontweight='bold')
    
    # --- Panel (d): Construction Process (simplified 2x2 subset) ---
    ax4 = fig.add_subplot(gs[1, 0])
    # Show centered grid positions
    ax4.set_xlim(-2.2, 2.2)
    ax4.set_ylim(-2.2, 2.2)
    for i in range(4):
        for j in range(4):
            x, y = j - 1.5, 1.5 - i
            ax4.scatter(x, y, s=150, c='steelblue', edgecolors='black')
            ax4.text(x, y + 0.25, f'{magic_4[i,j]}', ha='center', fontsize=8)
    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('X (Column)')
    ax4.set_ylabel('Y (Row)')
    ax4.set_title('(d) Centered Grid with Values', fontsize=11, fontweight='bold')
    ax4.set_aspect('equal')
    
    # --- Panel (e): Covariance Distribution ---
    ax5 = fig.add_subplot(gs[1, 1])
    n_random = 3000
    random_cov_xz = []
    random_cov_yz = []
    for _ in range(n_random):
        arr = np.arange(1, 17)
        np.random.shuffle(arr)
        sq = arr.reshape(4, 4)
        coords_rand = square_to_coordinates(sq)
        cov = test_zero_covariance(coords_rand)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    ax5.hist(random_cov_xz, bins=50, alpha=0.5, color='steelblue', 
             label='Cov(X,Z)', density=True)
    ax5.hist(random_cov_yz, bins=50, alpha=0.5, color='coral', 
             label='Cov(Y,Z)', density=True)
    ax5.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic = 0')
    ax5.set_xlabel('Covariance')
    ax5.set_ylabel('Density')
    ax5.set_title('(e) Covariance: Magic vs Random', fontsize=11, fontweight='bold')
    ax5.legend(fontsize=9)
    
    # --- Panel (f): Hull Volume ---
    ax6 = fig.add_subplot(gs[1, 2])
    volumes = []
    for _ in range(3000):
        arr = np.arange(1, 17)
        np.random.shuffle(arr)
        sq = arr.reshape(4, 4)
        coords_rand = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords_rand)
            volumes.append(hull.volume)
        except:
            pass
    
    coords_magic = square_to_coordinates(magic_4)
    hull_magic = ConvexHull(coords_magic)
    magic_vol = hull_magic.volume
    
    ax6.hist(volumes, bins=50, alpha=0.7, color='steelblue', density=True)
    ax6.axvline(x=magic_vol, color='red', linestyle='--', linewidth=2, 
               label=f'Magic ({magic_vol:.1f})')
    ax6.set_xlabel('Convex Hull Volume')
    ax6.set_ylabel('Density')
    ax6.set_title('(f) Hull Volume Distribution', fontsize=11, fontweight='bold')
    ax6.legend()
    
    filepath = os.path.join(output_dir, 'fig04_combined_4x4_analysis.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def create_combined_figure_5(output_dir='figures'):
    """
    Figure 5: 5×5 Complete Analysis (6-panel layout)
    Same structure as 4×4 analysis
    """
    siamese_5 = siamese_method(5)
    np.random.seed(42)
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # --- Panel (a): Magic Square ---
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(siamese_5, cmap='viridis', aspect='equal')
    for i in range(5):
        for j in range(5):
            val = siamese_5[i, j]
            color = 'white' if val < 13 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=9, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) 5×5 Magic Square\nM(5) = 65', fontsize=11, fontweight='bold')
    
    # --- Panel (b): Magic Gem 3D ---
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    coords = square_to_coordinates(siamese_5, center_z=True)
    scatter = ax2.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                         c=coords[:, 2], cmap='viridis', s=60, edgecolors='black')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.1, facecolor='cyan', 
                                   edgecolor='darkblue', linewidth=0.3)
            ax2.add_collection3d(tri)
    except:
        pass
    ax2.scatter([0], [0], [0], c='red', s=50, marker='x')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('(b) 5×5 Magic Gem', fontsize=11, fontweight='bold')
    
    # --- Panel (c): Vector Representation ---
    ax3 = fig.add_subplot(gs[0, 2], projection='3d')
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax3.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.05, linewidth=1)
    ax3.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=60, edgecolors='black')
    ax3.scatter([0], [0], [0], c='red', s=100, marker='o')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('(c) 25 Vectors from Centroid', fontsize=11, fontweight='bold')
    
    # --- Panel (d): Construction Grid ---
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_xlim(-2.8, 2.8)
    ax4.set_ylim(-2.8, 2.8)
    for i in range(5):
        for j in range(5):
            x, y = j - 2, 2 - i
            ax4.scatter(x, y, s=100, c='steelblue', edgecolors='black')
            ax4.text(x, y + 0.28, f'{siamese_5[i,j]}', ha='center', fontsize=7)
    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('X (Column)')
    ax4.set_ylabel('Y (Row)')
    ax4.set_title('(d) Centered Grid with Values', fontsize=11, fontweight='bold')
    ax4.set_aspect('equal')
    
    # --- Panel (e): Covariance Distribution ---
    ax5 = fig.add_subplot(gs[1, 1])
    n_random = 3000
    random_cov_xz = []
    random_cov_yz = []
    for _ in range(n_random):
        arr = np.arange(1, 26)
        np.random.shuffle(arr)
        sq = arr.reshape(5, 5)
        coords_rand = square_to_coordinates(sq)
        cov = test_zero_covariance(coords_rand)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    ax5.hist(random_cov_xz, bins=50, alpha=0.5, color='steelblue', 
             label='Cov(X,Z)', density=True)
    ax5.hist(random_cov_yz, bins=50, alpha=0.5, color='coral', 
             label='Cov(Y,Z)', density=True)
    ax5.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic = 0')
    ax5.set_xlabel('Covariance')
    ax5.set_ylabel('Density')
    ax5.set_title('(e) Covariance: Magic vs Random', fontsize=11, fontweight='bold')
    ax5.legend(fontsize=9)
    
    # --- Panel (f): Hull Volume ---
    ax6 = fig.add_subplot(gs[1, 2])
    volumes = []
    for _ in range(3000):
        arr = np.arange(1, 26)
        np.random.shuffle(arr)
        sq = arr.reshape(5, 5)
        coords_rand = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords_rand)
            volumes.append(hull.volume)
        except:
            pass
    
    coords_magic = square_to_coordinates(siamese_5)
    hull_magic = ConvexHull(coords_magic)
    magic_vol = hull_magic.volume
    
    ax6.hist(volumes, bins=50, alpha=0.7, color='steelblue', density=True)
    ax6.axvline(x=magic_vol, color='red', linestyle='--', linewidth=2, 
               label=f'Magic ({magic_vol:.1f})')
    ax6.set_xlabel('Convex Hull Volume')
    ax6.set_ylabel('Density')
    ax6.set_title('(f) Hull Volume Distribution', fontsize=11, fontweight='bold')
    ax6.legend()
    
    filepath = os.path.join(output_dir, 'fig05_combined_5x5_analysis.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def create_combined_figure_6(output_dir='figures'):
    """
    Figure 6: Cross-Order Comparison and Scaling (5-panel layout)
    Combines: Comparison of 3x3, 4x4, 5x5 Magic Gems + Scaling properties
    """
    lo_shu = get_canonical_3x3()
    magic_4 = get_canonical_4x4()
    siamese_5 = siamese_method(5)
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # --- Top Row: Three Magic Gems side by side ---
    squares = [lo_shu, magic_4, siamese_5]
    titles = ['(a) 3×3 Magic Gem\n(Odd order)', '(b) 4×4 Magic Gem\n(Even order)', '(c) 5×5 Magic Gem\n(Odd order)']
    
    for idx, (sq, title) in enumerate(zip(squares, titles)):
        ax = fig.add_subplot(gs[0, idx], projection='3d')
        coords = square_to_coordinates(sq, center_z=True)
        
        scatter = ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                            c=coords[:, 2], cmap='viridis', s=80 - idx*15, edgecolors='black')
        try:
            hull = ConvexHull(coords)
            for simplex in hull.simplices:
                pts = coords[simplex]
                tri = Poly3DCollection([pts], alpha=0.12, facecolor='cyan', 
                                       edgecolor='darkblue', linewidth=0.3)
                ax.add_collection3d(tri)
        except:
            pass
        ax.scatter([0], [0], [0], c='red', s=40, marker='x')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title, fontsize=11, fontweight='bold')
    
    # --- Bottom Row: Scaling Properties ---
    ns = [3, 4, 5]
    
    # Compute properties
    hull_volumes = []
    vertex_fracs = []
    magic_constants = []
    
    for n, sq in zip(ns, squares):
        coords = square_to_coordinates(sq, center_z=True)
        hull = ConvexHull(coords)
        hull_volumes.append(hull.volume)
        vertex_fracs.append(len(hull.vertices) / n**2)
        magic_constants.append(n * (n**2 + 1) // 2)
    
    # Panel (d): Hull Volume vs Order
    ax4 = fig.add_subplot(gs[1, 0])
    bars = ax4.bar(ns, hull_volumes, color='teal', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Order n', fontsize=11)
    ax4.set_ylabel('Hull Volume', fontsize=11)
    ax4.set_title('(d) Convex Hull Volume', fontsize=12, fontweight='bold')
    ax4.set_xticks(ns)
    for bar, vol in zip(bars, hull_volumes):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{vol:.1f}', ha='center', fontsize=9)
    
    # Panel (e): Vertex Fraction
    ax5 = fig.add_subplot(gs[1, 1])
    bars = ax5.bar(ns, vertex_fracs, color='coral', alpha=0.7, edgecolor='black')
    ax5.set_xlabel('Order n', fontsize=11)
    ax5.set_ylabel('Fraction on Hull', fontsize=11)
    ax5.set_title('(e) Hull Vertex Fraction', fontsize=12, fontweight='bold')
    ax5.set_xticks(ns)
    ax5.set_ylim(0, 1)
    for bar, frac in zip(bars, vertex_fracs):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{frac:.2f}', ha='center', fontsize=9)
    
    # Panel (f): Magic Constant
    ax6 = fig.add_subplot(gs[1, 2])
    bars = ax6.bar(ns, magic_constants, color='forestgreen', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('Order n', fontsize=11)
    ax6.set_ylabel('Magic Constant M(n)', fontsize=11)
    ax6.set_title('(f) Magic Constant', fontsize=12, fontweight='bold')
    ax6.set_xticks(ns)
    for bar, const in zip(bars, magic_constants):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{const}', ha='center', fontsize=9)
    
    filepath = os.path.join(output_dir, 'fig06_combined_comparison_scaling.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def create_combined_figure_7(output_dir='figures'):
    """
    Figure 7: Energy Landscape for n=3 (2-panel layout)
    Shows exhaustive analysis for n=3 only - larger scale analysis shown in separate figure.
    """
    from src.analysis import analyze_exhaustive_n3
    
    # Run analysis for n=3
    print("  Running exhaustive n=3 analysis...")
    energy_data = analyze_exhaustive_n3(verbose=False)
    
    fig = plt.figure(figsize=(14, 5))
    gs = GridSpec(1, 2, figure=fig, wspace=0.25)
    
    energies = energy_data['energy_values']
    
    # --- Panel (a): Full distribution (log scale) ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(energies, bins=100, color='steelblue', alpha=0.7, edgecolor='black', linewidth=0.3)
    ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic squares (E=0)')
    ax1.set_xlabel('Total Energy E(S)', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('(a) Energy Distribution: All 362,880 Permutations', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.set_yscale('log')
    ax1.annotate(f'8 magic squares\nat E = 0', 
                xy=(0, 1), xytext=(5, 10000),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, color='red')
    
    # --- Panel (b): Zoomed view near zero ---
    ax2 = fig.add_subplot(gs[0, 1])
    low_energy = [e for e in energies if e < 10]
    ax2.hist(low_energy, bins=50, color='steelblue', alpha=0.7, edgecolor='black', linewidth=0.3)
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic squares')
    ax2.set_xlabel('Total Energy E(S)', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('(b) Low-Energy Region (E < 10)', fontsize=12, fontweight='bold')
    ax2.legend()
    textstr = f"Total arrangements: {energy_data['total_permutations']:,}\n"
    textstr += f"Zero-energy (magic): {energy_data['zero_energy_count']}\n"
    textstr += f"Theorem verified: {energy_data['theorem_verified']}"
    ax2.text(0.95, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    filepath = os.path.join(output_dir, 'fig07_combined_energy_landscape.pdf')
    fig.savefig(filepath)
    print(f"Saved: {filepath}")
    plt.close()
    return filepath


def generate_all_combined_figures(output_dir='figures'):
    """Generate all combined figures for the reduced figure set."""
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Generating Combined Figures for Journal Submission")
    print("=" * 60)
    
    # Figure 1: Lo Shu (keep as is)
    print("\nFigure 1: Lo Shu (keeping existing fig01_lo_shu.pdf)")
    
    # Figure 2: Construction + Symmetries
    print("\nFigure 2: Construction + Symmetries")
    create_combined_figure_2(output_dir)
    
    # Figure 3: 3x3 Analysis
    print("\nFigure 3: 3×3 Geometric Analysis")
    create_combined_figure_3(output_dir)
    
    # Figure 4: 4x4 Analysis
    print("\nFigure 4: 4×4 Complete Analysis")
    create_combined_figure_4(output_dir)
    
    # Figure 5: 5x5 Analysis
    print("\nFigure 5: 5×5 Complete Analysis")
    create_combined_figure_5(output_dir)
    
    # Figure 6: Comparison + Scaling
    print("\nFigure 6: Cross-Order Comparison + Scaling")
    create_combined_figure_6(output_dir)
    
    # Figure 7: Energy Landscape
    print("\nFigure 7: Energy Landscape Combined")
    create_combined_figure_7(output_dir)
    
    # Figures 8-10: Keep existing comprehensive figures
    print("\n" + "=" * 60)
    print("Summary: Reduced Figure Set")
    print("=" * 60)
    print("""
New Combined Figure Structure:
  Figure 1:  Lo Shu (fig01_lo_shu.pdf) - KEEP
  Figure 2:  Construction + Symmetries (fig02_combined_construction_symmetries.pdf) - NEW
  Figure 3:  3×3 Geometric Analysis (fig03_combined_3x3_analysis.pdf) - NEW  
  Figure 4:  4×4 Complete Analysis (fig04_combined_4x4_analysis.pdf) - NEW
  Figure 5:  5×5 Complete Analysis (fig05_combined_5x5_analysis.pdf) - NEW
  Figure 6:  Comparison + Scaling (fig06_combined_comparison_scaling.pdf) - NEW
  Figure 7:  Energy Landscape (fig07_combined_energy_landscape.pdf) - NEW
  Figure 8:  Perturbation Analysis (Complete_Perturbation_Analysis_n345.png) - KEEP
  Figure 9:  Energy Comparison (energy_landscapes_comparison.png) - KEEP
  Figure 10: Scaling Summary (Figure7_ScalingSummary.png) - KEEP

Total: ~10 figures (reduced from ~24)
""")
    
    print(f"\nCombined figures saved to {output_dir}/")


if __name__ == "__main__":
    generate_all_combined_figures()

