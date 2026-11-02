#!/usr/bin/env python3
"""
Magic Square as a Balanced Mobile / Weight-on-String System

Each cell is a weight hanging from the center on a string.
- String direction = position vector (i-1.5, j-1.5)  
- String length = distance from center (fixed by grid)
- Weight = cell value

For balance: the weighted sum of all position vectors = 0
This is exactly what the covariance conditions enforce!
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.cm as cm

# Dürer's magic square
DURER = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

def create_mobile_view_2d(square, title="Magic Square as Balanced Mobile", save_path=None):
    """
    2D view of the mobile: weights on strings radiating from center.
    String direction = position, weight shown as circle size.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    n = square.shape[0]
    center = (n - 1) / 2  # 1.5
    mean_val = np.mean(square)  # 8.5
    
    # Color by value
    cmap = cm.RdYlBu_r  # Red = heavy, Blue = light
    norm = plt.Normalize(1, 16)
    
    # Left: The mobile view
    ax1 = axes[0]
    ax1.set_title("Weights on Strings from Central Pivot", fontsize=12)
    
    # Draw central pivot
    ax1.scatter(0, 0, s=300, c='black', marker='o', zorder=10, label='Pivot')
    
    # Draw each weight on its string
    for i in range(n):
        for j in range(n):
            # Position vector (string direction)
            dx = j - center
            dy = center - i  # Flip for display
            
            # String length (fixed by grid position)
            string_len = np.sqrt(dx**2 + dy**2)
            
            # Weight (cell value)
            weight = square[i, j]
            
            # Normalize direction
            if string_len > 0:
                ux, uy = dx / string_len, dy / string_len
            else:
                ux, uy = 0, 0
            
            # Draw string
            ax1.plot([0, dx], [0, dy], 'k-', linewidth=1, alpha=0.6)
            
            # Draw weight (size proportional to value)
            size = 100 + weight * 40
            color = cmap(norm(weight))
            ax1.scatter(dx, dy, s=size, c=[color], edgecolors='black', 
                       linewidths=2, zorder=5)
            ax1.text(dx, dy, str(int(weight)), ha='center', va='center',
                    fontsize=9, fontweight='bold', 
                    color='white' if weight > 10 else 'black')
    
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_aspect('equal')
    ax1.axhline(0, color='gray', linewidth=0.3, alpha=0.5)
    ax1.axvline(0, color='gray', linewidth=0.3, alpha=0.5)
    ax1.set_xlabel('← West | East →')
    ax1.set_ylabel('← South | North →')
    
    # Right: Show the torque balance
    ax2 = axes[1]
    ax2.set_title("Torque Analysis: Why It Balances", fontsize=12)
    
    # Calculate weighted position vectors (torques)
    torque_x = 0  # Sum of weight * x-position
    torque_y = 0  # Sum of weight * y-position
    
    # Draw contribution from each weight
    for i in range(n):
        for j in range(n):
            dx = j - center
            dy = center - i
            weight = square[i, j] - mean_val  # Deviation from mean
            
            # Torque contribution = weight_deviation * position
            tx = weight * dx
            ty = weight * dy
            torque_x += tx
            torque_y += ty
            
            # Draw torque vector from origin
            color = 'red' if weight > 0 else 'blue'
            alpha = min(1.0, abs(weight) / 8)
            if abs(tx) > 0.01 or abs(ty) > 0.01:
                ax2.arrow(0, 0, tx * 0.15, ty * 0.15, 
                         head_width=0.1, head_length=0.05,
                         fc=color, ec=color, alpha=alpha)
    
    # Show net torque (should be zero)
    ax2.scatter(torque_x / 16, torque_y / 16, s=200, c='green', marker='*', 
               zorder=10, label=f'Net Torque: ({torque_x/16:.4f}, {torque_y/16:.4f})')
    ax2.scatter(0, 0, s=100, c='black', marker='o', zorder=10)
    
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.legend(loc='upper right')
    ax2.set_xlabel('Torque-X')
    ax2.set_ylabel('Torque-Y')
    
    # Add explanation text
    ax2.text(0, -1.8, 'Red arrows: Heavy weights (>8.5) pull outward\n'
                      'Blue arrows: Light weights (<8.5) pull inward\n'
                      'Perfect cancellation → Net torque = 0',
            ha='center', fontsize=9, style='italic')
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_hanging_mobile_3d(square, save_path=None):
    """
    3D view: A hanging mobile where weights hang DOWN from central pivot.
    - Horizontal position = grid position
    - Vertical drop = proportional to weight (heavy = hangs lower)
    """
    fig = plt.figure(figsize=(14, 6))
    
    n = square.shape[0]
    center = (n - 1) / 2
    mean_val = np.mean(square)
    
    cmap = cm.RdYlBu_r
    norm = plt.Normalize(1, 16)
    
    # Left: Side view of hanging mobile
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_title("Hanging Mobile (Heavy = Lower)", fontsize=11)
    
    # Central pivot point (at top)
    pivot = np.array([0, 0, 2])
    ax1.scatter(*pivot, s=200, c='black', marker='o')
    
    # Draw each weight hanging from pivot
    for i in range(n):
        for j in range(n):
            # Horizontal position
            x = j - center
            y = i - center
            
            # Vertical position: heavier weights hang lower
            weight = square[i, j]
            z = 2 - (weight / 16) * 3  # Scale so heaviest at bottom
            
            # Draw string from pivot
            ax1.plot([0, x], [0, y], [2, z], 'k-', linewidth=0.8, alpha=0.5)
            
            # Draw weight
            size = 50 + weight * 15
            color = cmap(norm(weight))
            ax1.scatter(x, y, z, s=size, c=[color], edgecolors='black', linewidths=1)
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Height')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_zlim(-2, 2.5)
    
    # Right: Top-down view showing balance
    ax2 = fig.add_subplot(122)
    ax2.set_title("Top-Down View: Balance Check", fontsize=11)
    
    # Compute center of mass
    total_weight = np.sum(square)
    com_x = sum((j - center) * square[i, j] for i in range(n) for j in range(n)) / total_weight
    com_y = sum((i - center) * square[i, j] for i in range(n) for j in range(n)) / total_weight
    
    # Draw weights
    for i in range(n):
        for j in range(n):
            x = j - center
            y = center - i
            weight = square[i, j]
            size = 100 + weight * 30
            color = cmap(norm(weight))
            ax2.scatter(x, y, s=size, c=[color], edgecolors='black', linewidths=1.5)
            ax2.text(x, y, str(int(weight)), ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='white' if weight > 10 else 'black')
    
    # Draw center of mass
    ax2.scatter(com_x, -com_y, s=400, marker='+', c='green', linewidths=4, 
               zorder=10, label=f'Center of Mass\n({com_x:.4f}, {-com_y:.4f})')
    ax2.scatter(0, 0, s=200, marker='x', c='red', linewidths=3,
               zorder=10, label='Pivot Point')
    
    # Draw balance verification lines
    ax2.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax2.axvline(0, color='gray', linewidth=0.5, linestyle='--')
    
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_aspect('equal')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlabel('East-West')
    ax2.set_ylabel('North-South')
    
    plt.suptitle("Magic Square as Hanging Mobile", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_radial_weight_diagram(square, save_path=None):
    """
    Each weight shown at its radial distance from center.
    Like a balance wheel where weights must sum to zero torque at each angle.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    n = square.shape[0]
    center = (n - 1) / 2
    mean_val = np.mean(square)
    
    cmap = cm.RdYlBu_r
    norm = plt.Normalize(1, 16)
    
    # Left: Radial view - angle shows position, radius shows weight
    ax1 = axes[0]
    ax1.set_title("Radial Balance Wheel\n(Angle = Position, Radius = Weight)", fontsize=11)
    
    # Draw each weight
    for i in range(n):
        for j in range(n):
            # Angle from position
            dx = j - center
            dy = center - i
            angle = np.arctan2(dy, dx)
            
            # Radius from weight (scaled)
            weight = square[i, j]
            radius = 0.5 + weight * 0.15
            
            # Position on wheel
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Draw spoke from center
            ax1.plot([0, x], [0, y], 'k-', linewidth=0.5, alpha=0.3)
            
            # Draw weight
            size = 100 + weight * 30
            color = cmap(norm(weight))
            ax1.scatter(x, y, s=size, c=[color], edgecolors='black', linewidths=1.5)
            ax1.text(x, y, str(int(weight)), ha='center', va='center',
                    fontsize=8, fontweight='bold',
                    color='white' if weight > 10 else 'black')
    
    # Draw concentric circles for reference
    for r in [1, 2, 3]:
        circle = plt.Circle((0, 0), r * 0.15 + 0.5, fill=False, 
                            color='gray', linestyle=':', linewidth=0.5)
        ax1.add_patch(circle)
    
    ax1.scatter(0, 0, s=150, c='black', marker='o', zorder=10)
    ax1.set_xlim(-3.5, 3.5)
    ax1.set_ylim(-3.5, 3.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Right: The balance equation visualization
    ax2 = axes[1]
    ax2.set_title("The Balance Equation", fontsize=11)
    
    # Show how weights at opposite positions cancel
    # Group by approximate angle
    angle_groups = {}
    for i in range(n):
        for j in range(n):
            dx = j - center
            dy = i - center
            angle = np.arctan2(dy, dx)
            # Round angle to nearest 45 degrees
            angle_key = round(angle / (np.pi/4)) * (np.pi/4)
            if angle_key not in angle_groups:
                angle_groups[angle_key] = []
            angle_groups[angle_key].append((dx, dy, square[i, j], i, j))
    
    # For each direction, show the weighted sum
    y_pos = 0.9
    ax2.text(0.5, 0.95, "Weighted Sum of Positions = 0", ha='center', 
            fontsize=12, fontweight='bold', transform=ax2.transAxes)
    
    # Calculate and display the sums
    sum_x = sum((j - center) * (square[i, j] - mean_val) 
                for i in range(n) for j in range(n))
    sum_y = sum((i - center) * (square[i, j] - mean_val) 
                for i in range(n) for j in range(n))
    
    ax2.text(0.5, 0.8, f"Σ (x_i - 1.5)(v_i - 8.5) = {sum_x:.6f}", 
            ha='center', fontsize=11, transform=ax2.transAxes, family='monospace')
    ax2.text(0.5, 0.7, f"Σ (y_i - 1.5)(v_i - 8.5) = {sum_y:.6f}", 
            ha='center', fontsize=11, transform=ax2.transAxes, family='monospace')
    
    # Show a specific cancellation example
    ax2.text(0.5, 0.55, "Example: Corners cancel", ha='center', 
            fontsize=10, fontweight='bold', transform=ax2.transAxes)
    
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    corner_vals = [square[i, j] for i, j in corners]
    corner_text = " + ".join([f"{v}" for v in corner_vals]) + f" = {sum(corner_vals)}"
    ax2.text(0.5, 0.45, f"Corner values: {corner_text}", 
            ha='center', fontsize=10, transform=ax2.transAxes)
    ax2.text(0.5, 0.35, f"Each corner at distance √2×1.5 ≈ 2.12 from center",
            ha='center', fontsize=9, transform=ax2.transAxes, style='italic')
    
    # Physical interpretation
    ax2.text(0.5, 0.15, 
            "Like a mobile: if you hang weights from strings,\n"
            "the system balances when center of mass = pivot point.\n"
            "Magic squares are PERFECTLY balanced mobiles!",
            ha='center', fontsize=10, transform=ax2.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax2.axis('off')
    
    plt.suptitle("Magic Square: A Perfectly Balanced Weight System", 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    return fig


def create_string_tension_view(square, save_path=None):
    """
    Show the strings with tension proportional to weight.
    Thicker strings = heavier weights = more tension.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    n = square.shape[0]
    center = (n - 1) / 2
    mean_val = np.mean(square)
    
    cmap = cm.RdYlBu_r
    norm = plt.Normalize(1, 16)
    
    ax.set_title("String Tension View\n(Thicker string = Heavier weight = More tension)", 
                fontsize=12)
    
    # Draw central pivot
    pivot = plt.Circle((0, 0), 0.15, color='black', zorder=10)
    ax.add_patch(pivot)
    
    # Draw each string and weight
    for i in range(n):
        for j in range(n):
            # Position
            dx = j - center
            dy = center - i
            
            weight = square[i, j]
            
            # String thickness proportional to weight
            thickness = 0.5 + weight * 0.3
            
            # Draw string (thicker for heavier weights)
            ax.plot([0, dx], [0, dy], 'k-', linewidth=thickness, alpha=0.7, 
                   solid_capstyle='round')
            
            # Draw weight
            size = 150 + weight * 40
            color = cmap(norm(weight))
            ax.scatter(dx, dy, s=size, c=[color], edgecolors='black', 
                      linewidths=2, zorder=5)
            ax.text(dx, dy, str(int(weight)), ha='center', va='center',
                   fontsize=10, fontweight='bold',
                   color='white' if weight > 10 else 'black')
    
    # Add legend for string thickness
    ax.plot([], [], 'k-', linewidth=0.5 + 1*0.3, label='Light (1)')
    ax.plot([], [], 'k-', linewidth=0.5 + 8*0.3, label='Medium (8)')
    ax.plot([], [], 'k-', linewidth=0.5 + 16*0.3, label='Heavy (16)')
    ax.legend(loc='upper left', title='String Tension', fontsize=9)
    
    # Compute and show balance
    com_x = sum((j - center) * square[i, j] for i in range(n) for j in range(n)) / np.sum(square)
    com_y = sum((center - i) * square[i, j] for i in range(n) for j in range(n)) / np.sum(square)
    
    # Show that COM is at origin
    ax.annotate(f'Center of Mass at ({com_x:.4f}, {com_y:.4f})\n= Pivot Point ✓',
               xy=(0, 0), xytext=(1.5, -2),
               fontsize=10, ha='center',
               arrowprops=dict(arrowstyle='->', color='green'),
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.8, 2.8)
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linewidth=0.3, alpha=0.3)
    ax.axvline(0, color='gray', linewidth=0.3, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved to {save_path}")
    
    return fig


def main():
    """Generate all mobile/weight visualizations."""
    import os
    
    output_dir = "paper/figures"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating mobile/weight-on-string visualizations...")
    print("=" * 60)
    
    square = DURER
    print(f"Using Dürer's magic square:\n{square}\n")
    
    print("1. Creating mobile view (2D)...")
    create_mobile_view_2d(square, save_path=f"{output_dir}/mobile_view_2d.png")
    
    print("2. Creating hanging mobile (3D)...")
    create_hanging_mobile_3d(square, save_path=f"{output_dir}/hanging_mobile_3d.png")
    
    print("3. Creating radial weight diagram...")
    create_radial_weight_diagram(square, save_path=f"{output_dir}/radial_weight.png")
    
    print("4. Creating string tension view...")
    create_string_tension_view(square, save_path=f"{output_dir}/string_tension.png")
    
    print("\nAll visualizations complete!")


if __name__ == "__main__":
    main()

