"""
figures.py
==========
Generate publication-quality figures for the Magic Gems paper.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import os
from typing import Optional, List

from .magic_squares import get_canonical_3x3, get_canonical_4x4, generate_all_3x3_magic_squares, siamese_method, is_magic_square
from .magic_gems import square_to_coordinates, compute_convex_hull
from .analysis import (
    test_zero_covariance, 
    analyze_magic_vs_random, 
    perturbation_analysis,
    compute_total_magic_energy,
    analyze_exhaustive_n3,
    analyze_perturbation_isolation,
    analyze_scaling
)


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


def fig_magic_square_grid(square: np.ndarray, title: str = "Magic Square", 
                          filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot a magic square as a colored grid.
    
    Parameters
    ----------
    square : np.ndarray
        n×n magic square
    title : str
        Figure title
    filepath : str, optional
        If provided, save figure to this path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    n = square.shape[0]
    
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # Create colored grid
    im = ax.imshow(square, cmap='viridis', aspect='equal')
    
    # Add text annotations
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            color = 'white' if val < (n**2 + 1) / 2 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=16, fontweight='bold', color=color)
    
    # Styling
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=2)
    ax.tick_params(which='both', length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    plt.colorbar(im, ax=ax, label='Value', shrink=0.8)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_magic_gem_3d(square: np.ndarray, title: str = "Magic Gem",
                     filepath: Optional[str] = None, show_hull: bool = True) -> plt.Figure:
    """
    Plot a Magic Gem in 3D.
    
    Parameters
    ----------
    square : np.ndarray
        n×n magic square
    title : str
        Figure title
    filepath : str, optional
        Save path
    show_hull : bool
        Whether to show convex hull
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    coords = square_to_coordinates(square, center_z=True)
    n = square.shape[0]
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot points
    scatter = ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                        c=coords[:, 2], cmap='viridis', s=100, 
                        edgecolors='black', linewidth=1)
    
    # Add labels
    for i, (x, y, z) in enumerate(coords):
        ax.text(x, y, z + 0.3, str(square.flatten()[i]), fontsize=8, ha='center')
    
    # Show convex hull
    if show_hull:
        try:
            hull = ConvexHull(coords)
            for simplex in hull.simplices:
                pts = coords[simplex]
                tri = Poly3DCollection([pts], alpha=0.2, facecolor='cyan', 
                                       edgecolor='darkblue', linewidth=0.5)
                ax.add_collection3d(tri)
        except Exception:
            pass
    
    # Draw axes through origin
    max_range = max(1, np.abs(coords).max()) * 1.2
    ax.plot([-max_range, max_range], [0, 0], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
    ax.plot([0, 0], [-max_range, max_range], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-max_range, max_range], 'k--', alpha=0.3, linewidth=0.5)
    
    # Mark origin
    ax.scatter([0], [0], [0], c='red', s=50, marker='x', linewidth=2)
    
    ax.set_xlabel('X (Column)')
    ax.set_ylabel('Y (Row)')
    ax.set_zlabel('Z (Value - centered)')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    plt.colorbar(scatter, ax=ax, label='Z-value', shrink=0.6, pad=0.1)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_vectors_from_origin(square: np.ndarray, title: str = "Vector Representation",
                            filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot vectors from origin to each magic gem point.
    
    Parameters
    ----------
    square : np.ndarray
        n×n magic square
    title : str
        Figure title
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    coords = square_to_coordinates(square, center_z=True)
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw vectors
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.1, linewidth=1.5)
    
    # Plot endpoints
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
              c=coords[:, 2], cmap='viridis', s=80, edgecolors='black')
    
    # Origin
    ax.scatter([0], [0], [0], c='red', s=100, marker='o', label='Origin')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_covariance_comparison(filepath: Optional[str] = None) -> plt.Figure:
    """
    Compare covariance structure of magic vs random arrangements.
    
    Parameters
    ----------
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    np.random.seed(42)
    
    # Generate data
    n_random = 5000
    random_cov_xz = []
    random_cov_yz = []
    
    for _ in range(n_random):
        arr = np.arange(1, 10)
        np.random.shuffle(arr)
        sq = arr.reshape(3, 3)
        coords = square_to_coordinates(sq)
        cov = test_zero_covariance(coords)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    # Magic square covariances
    magic_squares = generate_all_3x3_magic_squares()
    magic_cov_xz = []
    magic_cov_yz = []
    for sq in magic_squares:
        coords = square_to_coordinates(sq)
        cov = test_zero_covariance(coords)
        magic_cov_xz.append(cov['cov_xz'])
        magic_cov_yz.append(cov['cov_yz'])
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Cov(X,Z) histogram
    axes[0].hist(random_cov_xz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random', density=True)
    axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic (all = 0)')
    axes[0].set_xlabel('Cov(X, Z)')
    axes[0].set_ylabel('Density')
    axes[0].set_title('Covariance X-Z: Magic vs Random')
    axes[0].legend()
    
    # Cov(Y,Z) histogram
    axes[1].hist(random_cov_yz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random', density=True)
    axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic (all = 0)')
    axes[1].set_xlabel('Cov(Y, Z)')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Covariance Y-Z: Magic vs Random')
    axes[1].legend()
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_all_symmetries(filepath: Optional[str] = None) -> plt.Figure:
    """
    Show all 8 symmetries of the 3×3 magic square.
    
    Parameters
    ----------
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    magic_squares = generate_all_3x3_magic_squares()
    
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.flatten()
    
    for idx, sq in enumerate(magic_squares):
        ax = axes[idx]
        im = ax.imshow(sq, cmap='viridis', aspect='equal')
        
        # Add numbers
        for i in range(3):
            for j in range(3):
                val = sq[i, j]
                color = 'white' if val < 5 else 'black'
                ax.text(j, i, str(val), ha='center', va='center', 
                       fontsize=12, fontweight='bold', color=color)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Variant {idx + 1}', fontsize=10)
    
    fig.suptitle('All 8 D₄ Symmetries of the 3×3 Magic Square', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_hull_volume_distribution(n: int = 3, num_samples: int = 5000,
                                  filepath: Optional[str] = None) -> plt.Figure:
    """
    Show distribution of convex hull volumes for random arrangements.
    
    Parameters
    ----------
    n : int
        Order of square
    num_samples : int
        Number of random samples
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    np.random.seed(42)
    
    volumes = []
    magic_volumes = []
    
    for _ in range(num_samples):
        arr = np.arange(1, n**2 + 1)
        np.random.shuffle(arr)
        sq = arr.reshape(n, n)
        coords = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords)
            volumes.append(hull.volume)
        except:
            pass
    
    # Magic square volumes
    if n == 3:
        for sq in generate_all_3x3_magic_squares():
            coords = square_to_coordinates(sq)
            try:
                hull = ConvexHull(coords)
                magic_volumes.append(hull.volume)
            except:
                pass
    elif n == 5:
        sq = siamese_method(5)
        coords = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords)
            magic_volumes.append(hull.volume)
        except:
            pass
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.hist(volumes, bins=50, alpha=0.7, color='steelblue', label='Random', density=True)
    if magic_volumes:
        ax.axvline(x=magic_volumes[0], color='red', linestyle='--', linewidth=2, 
                  label=f'Magic ({magic_volumes[0]:.2f})')
    
    ax.set_xlabel('Convex Hull Volume')
    ax.set_ylabel('Density')
    ax.set_title(f'{n}×{n} Arrangements: Convex Hull Volume Distribution')
    ax.legend()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_construction_process(filepath: Optional[str] = None) -> plt.Figure:
    """
    Illustrate the construction process from magic square to magic gem.
    
    Parameters
    ----------
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    lo_shu = get_canonical_3x3()
    
    fig = plt.figure(figsize=(14, 4))
    
    # Step 1: Magic Square
    ax1 = fig.add_subplot(141)
    im = ax1.imshow(lo_shu, cmap='viridis', aspect='equal')
    for i in range(3):
        for j in range(3):
            val = lo_shu[i, j]
            color = 'white' if val < 5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=14, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('Step 1: Magic Square\n(Lo Shu)', fontsize=11, fontweight='bold')
    
    # Step 2: Centered Grid
    ax2 = fig.add_subplot(142)
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
    ax2.set_title('Step 2: Centered Grid\n(Origin at center)', fontsize=11, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Step 3: Add Z dimension
    ax3 = fig.add_subplot(143, projection='3d')
    coords_uncentered = square_to_coordinates(lo_shu, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=80, edgecolors='black')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z (value)')
    ax3.set_title('Step 3: Add Z\n(Square values)', fontsize=11, fontweight='bold')
    
    # Step 4: Center Z and form gem
    ax4 = fig.add_subplot(144, projection='3d')
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
    ax4.set_title('Step 4: Magic Gem\n(Centered, with hull)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_magic_square_grid_5x5(square: np.ndarray, title: str = "5×5 Magic Square",
                               filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot a 5×5 magic square as a colored grid.
    """
    n = square.shape[0]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    im = ax.imshow(square, cmap='viridis', aspect='equal')
    
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            color = 'white' if val < (n**2 + 1) / 2 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=11, fontweight='bold', color=color)
    
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=2)
    ax.tick_params(which='both', length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    plt.colorbar(im, ax=ax, label='Value', shrink=0.8)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_construction_process_5x5(filepath: Optional[str] = None) -> plt.Figure:
    """
    Illustrate the construction process for 5×5 magic square to magic gem.
    """
    siamese_5 = siamese_method(5)
    
    fig = plt.figure(figsize=(16, 4))
    
    # Step 1: Magic Square
    ax1 = fig.add_subplot(141)
    im = ax1.imshow(siamese_5, cmap='viridis', aspect='equal')
    for i in range(5):
        for j in range(5):
            val = siamese_5[i, j]
            color = 'white' if val < 13 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=9, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('Step 1: 5×5 Magic Square\n(Siamese Method)', fontsize=10, fontweight='bold')
    
    # Step 2: Centered Grid
    ax2 = fig.add_subplot(142)
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.5, 2.5)
    for i in range(5):
        for j in range(5):
            x, y = j - 2, 2 - i
            ax2.scatter(x, y, s=100, c='steelblue', edgecolors='black')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Step 2: Centered 5×5 Grid\n(25 positions)', fontsize=10, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Step 3: Add Z dimension (uncentered)
    ax3 = fig.add_subplot(143, projection='3d')
    coords_uncentered = square_to_coordinates(siamese_5, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=40, edgecolors='black')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('Step 3: Add Z\n(25 values 1-25)', fontsize=10, fontweight='bold')
    
    # Step 4: Center Z and form gem
    ax4 = fig.add_subplot(144, projection='3d')
    coords = square_to_coordinates(siamese_5, center_z=True)
    ax4.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=40, edgecolors='black')
    ax4.scatter([0], [0], [0], c='red', s=50, marker='x')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.1, facecolor='cyan', edgecolor='darkblue', linewidth=0.3)
            ax4.add_collection3d(tri)
    except:
        pass
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z')
    ax4.set_title('Step 4: 5×5 Magic Gem\n(Centered, with hull)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_covariance_comparison_5x5(filepath: Optional[str] = None) -> plt.Figure:
    """
    Compare covariance structure of 5×5 magic vs random arrangements.
    """
    np.random.seed(42)
    
    n_random = 3000
    random_cov_xz = []
    random_cov_yz = []
    
    for _ in range(n_random):
        arr = np.arange(1, 26)
        np.random.shuffle(arr)
        sq = arr.reshape(5, 5)
        coords = square_to_coordinates(sq)
        cov = test_zero_covariance(coords)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    # Magic square covariance
    siamese_5 = siamese_method(5)
    coords_magic = square_to_coordinates(siamese_5)
    cov_magic = test_zero_covariance(coords_magic)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].hist(random_cov_xz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random 5×5', density=True)
    axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, 
                   label=f'Magic (Cov={cov_magic["cov_xz"]:.1f})')
    axes[0].set_xlabel('Cov(X, Z)')
    axes[0].set_ylabel('Density')
    axes[0].set_title('5×5 Covariance X-Z: Magic vs Random')
    axes[0].legend()
    
    axes[1].hist(random_cov_yz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random 5×5', density=True)
    axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2, 
                   label=f'Magic (Cov={cov_magic["cov_yz"]:.1f})')
    axes[1].set_xlabel('Cov(Y, Z)')
    axes[1].set_ylabel('Density')
    axes[1].set_title('5×5 Covariance Y-Z: Magic vs Random')
    axes[1].legend()
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_vectors_5x5(filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot vectors from origin for 5×5 Magic Gem.
    """
    siamese_5 = siamese_method(5)
    coords = square_to_coordinates(siamese_5, center_z=True)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw vectors
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.05, linewidth=1)
    
    # Plot endpoints
    scatter = ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                        c=coords[:, 2], cmap='viridis', s=60, edgecolors='black')
    
    # Origin
    ax.scatter([0], [0], [0], c='red', s=100, marker='o', label='Origin (Centroid)')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('5×5 Magic Gem: 25 Vectors from Centroid', fontsize=14, fontweight='bold', pad=20)
    ax.legend()
    
    plt.colorbar(scatter, ax=ax, label='Z-value', shrink=0.6, pad=0.1)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_hull_volume_distribution_5x5(num_samples: int = 3000,
                                      filepath: Optional[str] = None) -> plt.Figure:
    """
    Show distribution of convex hull volumes for random 5×5 arrangements.
    """
    np.random.seed(42)
    
    volumes = []
    
    for _ in range(num_samples):
        arr = np.arange(1, 26)
        np.random.shuffle(arr)
        sq = arr.reshape(5, 5)
        coords = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords)
            volumes.append(hull.volume)
        except:
            pass
    
    # Magic square volume
    siamese_5 = siamese_method(5)
    coords_magic = square_to_coordinates(siamese_5)
    hull_magic = ConvexHull(coords_magic)
    magic_vol = hull_magic.volume
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.hist(volumes, bins=50, alpha=0.7, color='steelblue', label='Random 5×5', density=True)
    ax.axvline(x=magic_vol, color='red', linestyle='--', linewidth=2, 
              label=f'Magic ({magic_vol:.1f})')
    
    ax.set_xlabel('Convex Hull Volume')
    ax.set_ylabel('Density')
    ax.set_title('5×5 Arrangements: Convex Hull Volume Distribution')
    ax.legend()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_magic_square_grid_4x4(square: np.ndarray, title: str = "4×4 Magic Square",
                               filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot a 4×4 magic square as a colored grid.
    """
    n = square.shape[0]
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    im = ax.imshow(square, cmap='viridis', aspect='equal')
    
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            color = 'white' if val < (n**2 + 1) / 2 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=12, fontweight='bold', color=color)
    
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=2)
    ax.tick_params(which='both', length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    plt.colorbar(im, ax=ax, label='Value', shrink=0.8)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_construction_process_4x4(filepath: Optional[str] = None) -> plt.Figure:
    """
    Illustrate the construction process for 4×4 magic square to magic gem.
    """
    magic_4 = get_canonical_4x4()
    
    fig = plt.figure(figsize=(16, 4))
    
    # Step 1: Magic Square
    ax1 = fig.add_subplot(141)
    im = ax1.imshow(magic_4, cmap='viridis', aspect='equal')
    for i in range(4):
        for j in range(4):
            val = magic_4[i, j]
            color = 'white' if val < 8.5 else 'black'
            ax1.text(j, i, str(val), ha='center', va='center', 
                    fontsize=10, fontweight='bold', color=color)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('Step 1: 4×4 Magic Square\n(Doubly-Even Method)', fontsize=10, fontweight='bold')
    
    # Step 2: Centered Grid
    ax2 = fig.add_subplot(142)
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    for i in range(4):
        for j in range(4):
            x, y = j - 1.5, 1.5 - i
            ax2.scatter(x, y, s=120, c='steelblue', edgecolors='black')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Step 2: Centered 4×4 Grid\n(16 positions)', fontsize=10, fontweight='bold')
    ax2.set_aspect('equal')
    
    # Step 3: Add Z dimension (uncentered)
    ax3 = fig.add_subplot(143, projection='3d')
    coords_uncentered = square_to_coordinates(magic_4, center_z=False)
    ax3.scatter(coords_uncentered[:, 0], coords_uncentered[:, 1], coords_uncentered[:, 2], 
               c=coords_uncentered[:, 2], cmap='viridis', s=50, edgecolors='black')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('Step 3: Add Z\n(16 values 1-16)', fontsize=10, fontweight='bold')
    
    # Step 4: Center Z and form gem
    ax4 = fig.add_subplot(144, projection='3d')
    coords = square_to_coordinates(magic_4, center_z=True)
    ax4.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
               c=coords[:, 2], cmap='viridis', s=50, edgecolors='black')
    ax4.scatter([0], [0], [0], c='red', s=50, marker='x')
    try:
        hull = ConvexHull(coords)
        for simplex in hull.simplices:
            pts = coords[simplex]
            tri = Poly3DCollection([pts], alpha=0.12, facecolor='cyan', edgecolor='darkblue', linewidth=0.4)
            ax4.add_collection3d(tri)
    except:
        pass
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z')
    ax4.set_title('Step 4: 4×4 Magic Gem\n(Centered, with hull)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_covariance_comparison_4x4(filepath: Optional[str] = None) -> plt.Figure:
    """
    Compare covariance structure of 4×4 magic vs random arrangements.
    """
    np.random.seed(42)
    
    n_random = 3000
    random_cov_xz = []
    random_cov_yz = []
    
    for _ in range(n_random):
        arr = np.arange(1, 17)
        np.random.shuffle(arr)
        sq = arr.reshape(4, 4)
        coords = square_to_coordinates(sq)
        cov = test_zero_covariance(coords)
        random_cov_xz.append(cov['cov_xz'])
        random_cov_yz.append(cov['cov_yz'])
    
    # Magic square covariance
    magic_4 = get_canonical_4x4()
    coords_magic = square_to_coordinates(magic_4)
    cov_magic = test_zero_covariance(coords_magic)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].hist(random_cov_xz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random 4×4', density=True)
    axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, 
                   label=f'Magic (Cov={cov_magic["cov_xz"]:.1f})')
    axes[0].set_xlabel('Cov(X, Z)')
    axes[0].set_ylabel('Density')
    axes[0].set_title('4×4 Covariance X-Z: Magic vs Random')
    axes[0].legend()
    
    axes[1].hist(random_cov_yz, bins=50, alpha=0.7, color='steelblue', 
                 label='Random 4×4', density=True)
    axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2, 
                   label=f'Magic (Cov={cov_magic["cov_yz"]:.1f})')
    axes[1].set_xlabel('Cov(Y, Z)')
    axes[1].set_ylabel('Density')
    axes[1].set_title('4×4 Covariance Y-Z: Magic vs Random')
    axes[1].legend()
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_vectors_4x4(filepath: Optional[str] = None) -> plt.Figure:
    """
    Plot vectors from origin for 4×4 Magic Gem.
    """
    magic_4 = get_canonical_4x4()
    coords = square_to_coordinates(magic_4, center_z=True)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw vectors
    colors = plt.cm.viridis(np.linspace(0, 1, len(coords)))
    for i, (x, y, z) in enumerate(coords):
        ax.quiver(0, 0, 0, x, y, z, color=colors[i], arrow_length_ratio=0.06, linewidth=1.2)
    
    # Plot endpoints
    scatter = ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                        c=coords[:, 2], cmap='viridis', s=70, edgecolors='black')
    
    # Origin
    ax.scatter([0], [0], [0], c='red', s=100, marker='o', label='Origin (Centroid)')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('4×4 Magic Gem: 16 Vectors from Centroid', fontsize=14, fontweight='bold', pad=20)
    ax.legend()
    
    plt.colorbar(scatter, ax=ax, label='Z-value', shrink=0.6, pad=0.1)
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_hull_volume_distribution_4x4(num_samples: int = 3000,
                                      filepath: Optional[str] = None) -> plt.Figure:
    """
    Show distribution of convex hull volumes for random 4×4 arrangements.
    """
    np.random.seed(42)
    
    volumes = []
    
    for _ in range(num_samples):
        arr = np.arange(1, 17)
        np.random.shuffle(arr)
        sq = arr.reshape(4, 4)
        coords = square_to_coordinates(sq)
        try:
            hull = ConvexHull(coords)
            volumes.append(hull.volume)
        except:
            pass
    
    # Magic square volume
    magic_4 = get_canonical_4x4()
    coords_magic = square_to_coordinates(magic_4)
    hull_magic = ConvexHull(coords_magic)
    magic_vol = hull_magic.volume
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.hist(volumes, bins=50, alpha=0.7, color='steelblue', label='Random 4×4', density=True)
    ax.axvline(x=magic_vol, color='red', linestyle='--', linewidth=2, 
              label=f'Magic ({magic_vol:.1f})')
    
    ax.set_xlabel('Convex Hull Volume')
    ax.set_ylabel('Density')
    ax.set_title('4×4 Arrangements: Convex Hull Volume Distribution')
    ax.legend()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_all_orders_comparison(filepath: Optional[str] = None) -> plt.Figure:
    """
    Side-by-side comparison of 3×3, 4×4, and 5×5 Magic Gems.
    """
    lo_shu = get_canonical_3x3()
    magic_4 = get_canonical_4x4()
    siamese_5 = siamese_method(5)
    
    fig = plt.figure(figsize=(16, 5))
    
    squares = [lo_shu, magic_4, siamese_5]
    titles = ['3×3 Magic Gem\n(Odd order)', '4×4 Magic Gem\n(Even order)', '5×5 Magic Gem\n(Odd order)']
    
    for idx, (sq, title) in enumerate(zip(squares, titles)):
        ax = fig.add_subplot(1, 3, idx + 1, projection='3d')
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
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_3x3_vs_5x5_comparison(filepath: Optional[str] = None) -> plt.Figure:
    """
    Side-by-side comparison of 3×3 and 5×5 Magic Gems.
    """
    lo_shu = get_canonical_3x3()
    siamese_5 = siamese_method(5)
    
    fig = plt.figure(figsize=(14, 6))
    
    # 3×3 Magic Gem
    ax1 = fig.add_subplot(121, projection='3d')
    coords_3 = square_to_coordinates(lo_shu, center_z=True)
    scatter1 = ax1.scatter(coords_3[:, 0], coords_3[:, 1], coords_3[:, 2], 
                          c=coords_3[:, 2], cmap='viridis', s=100, edgecolors='black')
    try:
        hull = ConvexHull(coords_3)
        for simplex in hull.simplices:
            pts = coords_3[simplex]
            tri = Poly3DCollection([pts], alpha=0.15, facecolor='cyan', edgecolor='darkblue')
            ax1.add_collection3d(tri)
    except:
        pass
    ax1.scatter([0], [0], [0], c='red', s=50, marker='x')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3×3 Magic Gem\n(9 vertices, 8 on hull)', fontsize=12, fontweight='bold')
    
    # 5×5 Magic Gem
    ax2 = fig.add_subplot(122, projection='3d')
    coords_5 = square_to_coordinates(siamese_5, center_z=True)
    scatter2 = ax2.scatter(coords_5[:, 0], coords_5[:, 1], coords_5[:, 2], 
                          c=coords_5[:, 2], cmap='viridis', s=60, edgecolors='black')
    try:
        hull = ConvexHull(coords_5)
        for simplex in hull.simplices:
            pts = coords_5[simplex]
            tri = Poly3DCollection([pts], alpha=0.1, facecolor='cyan', edgecolor='darkblue', linewidth=0.3)
            ax2.add_collection3d(tri)
    except:
        pass
    ax2.scatter([0], [0], [0], c='red', s=50, marker='x')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title(f'5×5 Magic Gem\n(25 vertices, {len(hull.vertices)} on hull)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    return fig


def fig_energy_landscape_n3(energy_data: dict = None, filepath: Optional[str] = None) -> plt.Figure:
    """
    Visualize the energy landscape for n=3.
    
    Shows the distribution of total energy across all 362,880 permutations,
    with magic squares marked at E=0. This illustrates how magic squares
    occupy unique zero-energy positions in the landscape.
    
    Parameters
    ----------
    energy_data : dict
        Pre-computed energy data from analyze_exhaustive_n3()
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    if energy_data is None:
        energy_data = analyze_exhaustive_n3(verbose=False)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    energies = energy_data['energy_values']
    
    # Left panel: Full distribution (log scale)
    ax1 = axes[0]
    ax1.hist(energies, bins=100, color='steelblue', alpha=0.7, edgecolor='black', linewidth=0.3)
    ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic squares (E=0)')
    ax1.set_xlabel('Total Energy E(S)', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Energy Distribution: All 362,880 Permutations', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.set_yscale('log')
    
    # Add annotation
    ax1.annotate(f'8 magic squares\nat E = 0', 
                xy=(0, 1), xytext=(5, 10000),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, color='red')
    
    # Right panel: Zoomed view near zero
    ax2 = axes[1]
    low_energy = [e for e in energies if e < 10]
    ax2.hist(low_energy, bins=50, color='steelblue', alpha=0.7, edgecolor='black', linewidth=0.3)
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Magic squares')
    ax2.set_xlabel('Total Energy E(S)', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('Low-Energy Region (E < 10)', fontsize=12, fontweight='bold')
    ax2.legend()
    
    # Add text box with statistics
    textstr = f"Total arrangements: {energy_data['total_permutations']:,}\n"
    textstr += f"Zero-energy (magic): {energy_data['zero_energy_count']}\n"
    textstr += f"Theorem verified: {energy_data['theorem_verified']}"
    ax2.text(0.95, 0.95, textstr, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    plt.close()
    return fig


def fig_perturbation_gaps(pert_data: dict = None, filepath: Optional[str] = None) -> plt.Figure:
    """
    Visualize the distribution of minimum energy gaps after single-swap perturbation.
    
    This demonstrates that magic squares are isolated local minima: every single
    swap increases the energy, with a positive gap.
    
    Parameters
    ----------
    pert_data : dict
        Pre-computed perturbation data
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    if pert_data is None:
        magic_squares = generate_all_3x3_magic_squares()
        pert_data = analyze_perturbation_isolation(magic_squares, verbose=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    gaps = pert_data['min_energy_gaps']
    
    ax.hist(gaps, bins=30, color='darkorange', alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
    ax.set_xlabel('Minimum Energy Gap After Single Swap', fontsize=12)
    ax.set_ylabel('Number of Magic Squares', fontsize=12)
    ax.set_title('Perturbation Analysis: Magic Squares as Isolated Minima', fontsize=12, fontweight='bold')
    
    # Add annotation
    min_gap = min(gaps)
    ax.annotate(f'Min gap: {min_gap:.4f}', 
                xy=(min_gap, 0), xytext=(min_gap + 0.05, ax.get_ylim()[1] * 0.7),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=10)
    
    # Add text box
    textstr = f"Squares tested: {pert_data['n_squares_tested']}\n"
    textstr += f"All isolated: {pert_data['all_isolated']}\n"
    textstr += f"Mean min gap: {pert_data['overall_mean_min_gap']:.4f}"
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    plt.close()
    return fig


def fig_scaling_analysis(scaling_data: dict = None, filepath: Optional[str] = None) -> plt.Figure:
    """
    Compare scaling properties across n = 3, 4, 5.
    
    Shows how hull volume, vertex fraction, perturbation gap, and magic constant
    scale with magic square order.
    
    Parameters
    ----------
    scaling_data : dict
        Pre-computed scaling data
    filepath : str, optional
        Save path
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    if scaling_data is None:
        scaling_data = analyze_scaling(verbose=False)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    ns = [3, 4, 5]
    
    # Panel 1: Hull Volume
    ax1 = axes[0, 0]
    volumes = [scaling_data[n]['hull_volume'] for n in ns]
    bars = ax1.bar(ns, volumes, color='teal', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Order n', fontsize=11)
    ax1.set_ylabel('Hull Volume', fontsize=11)
    ax1.set_title('Convex Hull Volume vs Order', fontsize=12, fontweight='bold')
    ax1.set_xticks(ns)
    for bar, vol in zip(bars, volumes):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{vol:.1f}', ha='center', fontsize=9)
    
    # Panel 2: Vertex Fraction
    ax2 = axes[0, 1]
    vertex_fracs = [scaling_data[n]['vertex_fraction'] for n in ns]
    bars = ax2.bar(ns, vertex_fracs, color='coral', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Order n', fontsize=11)
    ax2.set_ylabel('Fraction on Hull', fontsize=11)
    ax2.set_title('Hull Vertex Fraction vs Order', fontsize=12, fontweight='bold')
    ax2.set_xticks(ns)
    ax2.set_ylim(0, 1)
    for bar, frac in zip(bars, vertex_fracs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{frac:.2f}', ha='center', fontsize=9)
    
    # Panel 3: Perturbation Gap
    ax3 = axes[1, 0]
    gaps = [scaling_data[n]['min_perturbation_gap'] for n in ns]
    bars = ax3.bar(ns, gaps, color='mediumpurple', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Order n', fontsize=11)
    ax3.set_ylabel('Min Perturbation Gap', fontsize=11)
    ax3.set_title('Energy Gap After Single Swap', fontsize=12, fontweight='bold')
    ax3.set_xticks(ns)
    for bar, gap in zip(bars, gaps):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002, 
                f'{gap:.3f}', ha='center', fontsize=9)
    
    # Panel 4: Magic Constant
    ax4 = axes[1, 1]
    constants = [scaling_data[n]['magic_constant'] for n in ns]
    bars = ax4.bar(ns, constants, color='forestgreen', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Order n', fontsize=11)
    ax4.set_ylabel('Magic Constant M(n)', fontsize=11)
    ax4.set_title('Magic Constant vs Order', fontsize=12, fontweight='bold')
    ax4.set_xticks(ns)
    for bar, const in zip(bars, constants):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{const}', ha='center', fontsize=9)
    
    plt.tight_layout()
    
    if filepath:
        fig.savefig(filepath)
        print(f"Saved: {filepath}")
    
    plt.close()
    return fig


def generate_all_figures(output_dir: str = 'figures'):
    """
    Generate all figures for the paper.
    
    Parameters
    ----------
    output_dir : str
        Directory to save figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    lo_shu = get_canonical_3x3()
    magic_4 = get_canonical_4x4()
    siamese_5 = siamese_method(5)
    
    print("Generating figures...")
    
    # === 3×3 Figures ===
    print("\n--- 3×3 Figures ---")
    
    fig_magic_square_grid(lo_shu, "The Lo Shu Magic Square (3×3)", 
                          os.path.join(output_dir, 'fig01_lo_shu.pdf'))
    plt.close()
    
    fig_construction_process(os.path.join(output_dir, 'fig02_construction_3x3.pdf'))
    plt.close()
    
    fig_magic_gem_3d(lo_shu, "3×3 Magic Gem",
                     os.path.join(output_dir, 'fig03_magic_gem_3x3.pdf'))
    plt.close()
    
    fig_vectors_from_origin(lo_shu, "3×3 Vector Representation",
                            os.path.join(output_dir, 'fig04_vectors_3x3.pdf'))
    plt.close()
    
    fig_all_symmetries(os.path.join(output_dir, 'fig05_symmetries.pdf'))
    plt.close()
    
    fig_covariance_comparison(os.path.join(output_dir, 'fig06_covariance_3x3.pdf'))
    plt.close()
    
    fig_hull_volume_distribution(3, 5000, os.path.join(output_dir, 'fig07_hull_volume_3x3.pdf'))
    plt.close()
    
    # === 4×4 Figures ===
    print("\n--- 4×4 Figures ---")
    
    fig_magic_square_grid_4x4(magic_4, "4×4 Magic Square (Doubly-Even Method)",
                              os.path.join(output_dir, 'fig08_magic_square_4x4.pdf'))
    plt.close()
    
    fig_construction_process_4x4(os.path.join(output_dir, 'fig09_construction_4x4.pdf'))
    plt.close()
    
    fig_magic_gem_3d(magic_4, "4×4 Magic Gem",
                     os.path.join(output_dir, 'fig10_magic_gem_4x4.pdf'))
    plt.close()
    
    fig_vectors_4x4(os.path.join(output_dir, 'fig11_vectors_4x4.pdf'))
    plt.close()
    
    fig_covariance_comparison_4x4(os.path.join(output_dir, 'fig12_covariance_4x4.pdf'))
    plt.close()
    
    fig_hull_volume_distribution_4x4(3000, os.path.join(output_dir, 'fig13_hull_volume_4x4.pdf'))
    plt.close()
    
    # === 5×5 Figures ===
    print("\n--- 5×5 Figures ---")
    
    fig_magic_square_grid_5x5(siamese_5, "5×5 Magic Square (Siamese Method)",
                              os.path.join(output_dir, 'fig14_magic_square_5x5.pdf'))
    plt.close()
    
    fig_construction_process_5x5(os.path.join(output_dir, 'fig15_construction_5x5.pdf'))
    plt.close()
    
    fig_magic_gem_3d(siamese_5, "5×5 Magic Gem",
                     os.path.join(output_dir, 'fig16_magic_gem_5x5.pdf'))
    plt.close()
    
    fig_vectors_5x5(os.path.join(output_dir, 'fig17_vectors_5x5.pdf'))
    plt.close()
    
    fig_covariance_comparison_5x5(os.path.join(output_dir, 'fig18_covariance_5x5.pdf'))
    plt.close()
    
    fig_hull_volume_distribution_5x5(3000, os.path.join(output_dir, 'fig19_hull_volume_5x5.pdf'))
    plt.close()
    
    # === Comparison Figures ===
    print("\n--- Comparison Figures ---")
    
    fig_all_orders_comparison(os.path.join(output_dir, 'fig20_comparison_all_orders.pdf'))
    plt.close()
    
    # === Energy Landscape Figures ===
    print("\n--- Energy Landscape Figures ---")
    
    # Run exhaustive analysis for n=3
    print("  Running exhaustive n=3 analysis (this takes ~30 seconds)...")
    exhaustive_data = analyze_exhaustive_n3(verbose=False)
    
    fig_energy_landscape_n3(exhaustive_data, 
                            os.path.join(output_dir, 'fig21_energy_landscape_n3.pdf'))
    plt.close()
    
    # Perturbation analysis
    print("  Running perturbation isolation analysis...")
    magic_3x3 = generate_all_3x3_magic_squares()
    pert_data = analyze_perturbation_isolation(magic_3x3, verbose=False)
    
    fig_perturbation_gaps(pert_data,
                          os.path.join(output_dir, 'fig22_perturbation_gaps.pdf'))
    plt.close()
    
    # Scaling analysis
    print("  Running scaling analysis...")
    scaling_data = analyze_scaling(verbose=False)
    
    fig_scaling_analysis(scaling_data,
                         os.path.join(output_dir, 'fig23_scaling_analysis.pdf'))
    plt.close()
    
    print(f"\nAll figures saved to {output_dir}/")


if __name__ == "__main__":
    generate_all_figures()

