#!/usr/bin/env python3
"""
Orbital Visualization of Magic Squares

Visualizes magic squares as particles orbiting a central nucleus,
where each particle's position determines its "shell" and its value
determines its "weight" or "spin magnitude".

This captures the physical intuition of balance and symmetry.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

# Dürer's magic square
DURER = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

def create_orbital_view_2d(square, title="Magic Square as Orbital System", save_path=None):
    """
    Create a 2D orbital view where:
    - Position from center shows the grid location
    - Circle size shows the value (weight/spin magnitude)
    - Color intensity also indicates value
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    n = square.shape[0]
    center = (n - 1) / 2  # 1.5 for 4x4
    
    # Left: Traditional grid view with orbital overlay
    ax1 = axes[0]
    ax1.set_xlim(-0.5, n - 0.5)
    ax1.set_ylim(-0.5, n - 0.5)
    ax1.set_aspect('equal')
    ax1.set_title("Grid View with Orbital Rings", fontsize=12)
    
    # Draw concentric orbital rings (based on distance from center)
    for r in [0.5, 1.0, 1.5, 2.0, 2.5]:
        circle = Circle((center, center), r, fill=False, color='lightgray', 
                        linestyle='--', linewidth=0.5, alpha=0.5)
        ax1.add_patch(circle)
    
    # Plot each cell as a weighted particle
    cmap = cm.viridis
    norm = plt.Normalize(1, 16)
    
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            # Size proportional to value
            size = 100 + val * 30
            color = cmap(norm(val))
            ax1.scatter(j, n - 1 - i, s=size, c=[color], edgecolors='black', 
                       linewidths=1, zorder=5)
            ax1.text(j, n - 1 - i, str(int(val)), ha='center', va='center', 
                    fontsize=8, fontweight='bold', color='white' if val > 8 else 'black')
    
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel("Column (y)")
    ax1.set_ylabel("Row (x)")
    
    # Right: Polar/orbital view - particles arranged by distance from center
    ax2 = axes[1]
    ax2.set_title("Orbital Balance View", fontsize=12)
    
    # Group cells by their distance from center
    particles = []
    for i in range(n):
        for j in range(n):
            dist = np.sqrt((i - center)**2 + (j - center)**2)
            angle = np.arctan2(i - center, j - center)
            val = square[i, j]
            particles.append((dist, angle, val, i, j))
    
    # Sort by distance to see orbital shells
    particles.sort(key=lambda x: x[0])
    
    # Plot in polar-like view
    for dist, angle, val, i, j in particles:
        # Use distance as radius, angle as position
        x = dist * np.cos(angle)
        y = dist * np.sin(angle)
        size = 100 + val * 30
        color = cmap(norm(val))
        ax2.scatter(x, y, s=size, c=[color], edgecolors='black', linewidths=1, zorder=5)
        ax2.text(x, y, str(int(val)), ha='center', va='center', 
                fontsize=8, fontweight='bold', color='white' if val > 8 else 'black')
    
    # Draw orbital shells
    max_dist = np.sqrt(2) * center
    for r in np.unique([np.sqrt((i - center)**2 + (j - center)**2) 
                        for i in range(n) for j in range(n)]):
        circle = Circle((0, 0), r, fill=False, color='lightgray', 
                        linestyle='--', linewidth=0.5, alpha=0.5)
        ax2.add_patch(circle)
    
    ax2.set_xlim(-max_dist - 0.5, max_dist + 0.5)
    ax2.set_ylim(-max_dist - 0.5, max_dist + 0.5)
    ax2.set_aspect('equal')
    ax2.axhline(0, color='gray', linewidth=0.5, alpha=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5, alpha=0.5)
    ax2.set_xlabel("Distance × cos(θ)")
    ax2.set_ylabel("Distance × sin(θ)")
    
    # Add center marker (nucleus)
    ax2.scatter(0, 0, s=200, c='red', marker='*', zorder=10, label='Nucleus')
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_spinning_vectors_view(square, save_path=None):
    """
    Visualize each cell as a vector from the center, where:
    - Direction is determined by position (i, j)
    - Length is determined by value (weight)
    
    Shows how the vectors must balance (sum to zero in various projections).
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    n = square.shape[0]
    center = (n - 1) / 2
    mean_val = np.mean(square)
    
    cmap = cm.coolwarm
    norm = plt.Normalize(-7.5, 7.5)  # Centered on mean of 8.5
    
    # Left: Vectors colored by value
    ax1 = axes[0]
    ax1.set_title("Position Vectors (colored by value)", fontsize=11)
    
    for i in range(n):
        for j in range(n):
            dx = j - center
            dy = center - i  # Flip y for display
            val = square[i, j]
            
            # Arrow from center to position, colored by value
            color = cmap(norm(val - mean_val))
            ax1.arrow(0, 0, dx * 0.9, dy * 0.9, head_width=0.1, head_length=0.05,
                     fc=color, ec='black', linewidth=0.5, alpha=0.8)
            
            ax1.text(dx, dy, str(int(val)), ha='center', va='center', 
                    fontsize=9, fontweight='bold')
    
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_aspect('equal')
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.scatter(0, 0, s=100, c='red', marker='o', zorder=10)
    
    # Middle: Weighted vectors (length = value - mean)
    ax2 = axes[1]
    ax2.set_title("Weighted Vectors (length ∝ value - 8.5)", fontsize=11)
    
    for i in range(n):
        for j in range(n):
            dx = j - center
            dy = center - i
            val = square[i, j]
            weight = (val - mean_val) / 7.5  # Normalize to [-1, 1]
            
            # Direction from center, scaled by weight
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                ux, uy = dx / length, dy / length
                # Draw vector with length proportional to weight
                scaled_len = weight * 1.5
                color = cmap(norm(val - mean_val))
                ax2.arrow(0, 0, ux * scaled_len * 0.9, uy * scaled_len * 0.9, 
                         head_width=0.08, head_length=0.04,
                         fc=color, ec='black', linewidth=0.5, alpha=0.8)
    
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.scatter(0, 0, s=100, c='red', marker='o', zorder=10)
    
    # Right: Show balance - torques in each direction
    ax3 = axes[2]
    ax3.set_title("Torque Balance Check", fontsize=11)
    
    # Compute torques (covariances)
    c1 = sum((i - center) * (square[i, j] - mean_val) for i in range(n) for j in range(n)) / 16
    c2 = sum((j - center) * (square[i, j] - mean_val) for i in range(n) for j in range(n)) / 16
    c3 = sum((i**2 - 3.5) * (square[i, j] - mean_val) for i in range(n) for j in range(n)) / 16
    c4 = sum((j**2 - 3.5) * (square[i, j] - mean_val) for i in range(n) for j in range(n)) / 16
    
    labels = ['c₁\n(Row)', 'c₂\n(Col)', 'c₃\n(Row²)', 'c₄\n(Col²)']
    values = [c1, c2, c3, c4]
    colors = ['green' if abs(v) < 0.01 else 'red' for v in values]
    
    bars = ax3.bar(labels, values, color=colors, edgecolor='black')
    ax3.axhline(0, color='black', linewidth=1)
    ax3.set_ylabel('Covariance Value')
    ax3.set_ylim(-0.5, 0.5)
    
    for bar, val in zip(bars, values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.4f}', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle("Magic Square as Spinning Particle System", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_3d_orbital_view(square, save_path=None):
    """
    3D view showing particles orbiting with:
    - x, y from grid position
    - z (height) from value
    - Size from value
    """
    fig = plt.figure(figsize=(12, 5))
    
    n = square.shape[0]
    center = (n - 1) / 2
    mean_val = np.mean(square)
    
    cmap = cm.viridis
    norm = plt.Normalize(1, 16)
    
    # Left: 3D scatter
    ax1 = fig.add_subplot(121, projection='3d')
    
    xs, ys, zs, sizes, colors = [], [], [], [], []
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            xs.append(j - center)
            ys.append(i - center)
            zs.append(val - mean_val)
            sizes.append(50 + val * 20)
            colors.append(cmap(norm(val)))
    
    ax1.scatter(xs, ys, zs, s=sizes, c=colors, edgecolors='black', linewidths=0.5)
    
    # Add labels
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            ax1.text(j - center, i - center, val - mean_val, str(int(val)),
                    fontsize=8, ha='center', va='center')
    
    # Draw grid plane at z=0
    xx, yy = np.meshgrid(np.linspace(-2, 2, 2), np.linspace(-2, 2, 2))
    ax1.plot_surface(xx, yy, np.zeros_like(xx), alpha=0.1, color='gray')
    
    ax1.set_xlabel('Column (y - 1.5)')
    ax1.set_ylabel('Row (x - 1.5)')
    ax1.set_zlabel('Value - 8.5')
    ax1.set_title('3D Orbital View\n(height = value deviation)', fontsize=11)
    
    # Right: Top-down view with value as "weight"
    ax2 = fig.add_subplot(122)
    
    for i in range(n):
        for j in range(n):
            val = square[i, j]
            x = j - center
            y = center - i
            size = 100 + val * 30
            color = cmap(norm(val))
            ax2.scatter(x, y, s=size, c=[color], edgecolors='black', linewidths=1)
            ax2.text(x, y, str(int(val)), ha='center', va='center', 
                    fontsize=9, fontweight='bold', color='white' if val > 10 else 'black')
    
    # Show center of mass (should be at origin for magic square)
    com_x = sum((j - center) * square[i, j] for i in range(n) for j in range(n)) / sum(square.flatten())
    com_y = sum((center - i) * square[i, j] for i in range(n) for j in range(n)) / sum(square.flatten())
    ax2.scatter(com_x, com_y, s=300, marker='+', c='red', linewidths=3, zorder=10,
               label=f'Center of Mass\n({com_x:.3f}, {com_y:.3f})')
    ax2.scatter(0, 0, s=100, marker='x', c='blue', linewidths=2, zorder=10,
               label='Grid Center')
    
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_aspect('equal')
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlabel('Column offset from center')
    ax2.set_ylabel('Row offset from center')
    ax2.set_title('Top-Down View with Center of Mass', fontsize=11)
    
    plt.suptitle("Magic Square as 3D Orbital System (Dürer)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_electron_shell_analogy(square, save_path=None):
    """
    Draw magic square explicitly as electron shells:
    - Concentric rings for each "distance level"
    - Values as electrons on the rings
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    n = square.shape[0]
    center = (n - 1) / 2
    
    # Group cells by distance from center
    distance_groups = {}
    for i in range(n):
        for j in range(n):
            dist = round(np.sqrt((i - center)**2 + (j - center)**2), 2)
            if dist not in distance_groups:
                distance_groups[dist] = []
            distance_groups[dist].append((i, j, square[i, j]))
    
    # Sort distances
    distances = sorted(distance_groups.keys())
    
    # Color map for values
    cmap = cm.plasma
    norm = plt.Normalize(1, 16)
    
    # Draw shells and place electrons
    shell_radii = {d: 1 + 1.5 * idx for idx, d in enumerate(distances)}
    
    for dist in distances:
        shell_r = shell_radii[dist]
        
        # Draw shell
        theta = np.linspace(0, 2 * np.pi, 100)
        ax.plot(shell_r * np.cos(theta), shell_r * np.sin(theta), 
               'gray', linestyle='--', linewidth=0.5, alpha=0.5)
        
        # Place electrons on shell
        cells = distance_groups[dist]
        n_cells = len(cells)
        
        for idx, (i, j, val) in enumerate(cells):
            # Distribute evenly around shell
            angle = np.arctan2(i - center, j - center)
            x = shell_r * np.cos(angle)
            y = shell_r * np.sin(angle)
            
            size = 300 + val * 40
            color = cmap(norm(val))
            ax.scatter(x, y, s=size, c=[color], edgecolors='black', linewidths=2, zorder=5)
            ax.text(x, y, str(int(val)), ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='white')
    
    # Draw nucleus
    ax.scatter(0, 0, s=500, c='red', marker='*', zorder=10)
    ax.text(0, -0.4, 'Nucleus', ha='center', va='top', fontsize=10, color='red')
    
    # Add shell labels
    for dist, r in shell_radii.items():
        ax.text(r + 0.2, 0.2, f'd={dist:.2f}', fontsize=9, color='gray')
    
    # Title and formatting
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add legend for values
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.6, label='Cell Value')
    
    ax.set_title("Magic Square as Electron Orbital Configuration\n" + 
                "(Values distributed across shells by grid distance)",
                fontsize=14, fontweight='bold')
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved to {save_path}")
    
    return fig


def main():
    """Generate all orbital visualizations."""
    import os
    
    output_dir = "paper/figures"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating orbital visualizations of magic squares...")
    print("=" * 60)
    
    # Use Dürer's magic square
    square = DURER
    print(f"Using Dürer's magic square:\n{square}\n")
    
    # Generate visualizations
    print("1. Creating orbital view (2D)...")
    create_orbital_view_2d(square, save_path=f"{output_dir}/orbital_view_2d.png")
    
    print("2. Creating spinning vectors view...")
    create_spinning_vectors_view(square, save_path=f"{output_dir}/spinning_vectors.png")
    
    print("3. Creating 3D orbital view...")
    create_3d_orbital_view(square, save_path=f"{output_dir}/orbital_view_3d.png")
    
    print("4. Creating electron shell analogy...")
    create_electron_shell_analogy(square, save_path=f"{output_dir}/electron_shells.png")
    
    print("\nAll visualizations complete!")
    print(f"Output saved to {output_dir}/")


if __name__ == "__main__":
    main()

