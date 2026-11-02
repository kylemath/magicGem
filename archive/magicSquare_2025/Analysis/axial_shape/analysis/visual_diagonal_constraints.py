import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import os

# A standard 4x4 magic square for demonstration
magic_square = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

def create_axial_points(square):
    """Create 3D points from a magic square using the axial representation."""
    n = square.shape[0]
    points = []
    indices = []
    
    for i in range(n):
        for j in range(n):
            point = np.array([
                i - (n-1)/2,  # x-coordinate (row-based)
                j - (n-1)/2,  # y-coordinate (column-based)
                square[i, j] - np.mean(square)  # z-coordinate (value-based)
            ])
            points.append(point)
            indices.append((i, j))
    
    return np.array(points), indices

def identify_diagonals(indices, n):
    """Identify points on the main and anti-diagonals."""
    main_diag = []
    anti_diag = []
    
    for idx, (i, j) in enumerate(indices):
        if i == j:
            main_diag.append(idx)
        if i + j == n - 1:
            anti_diag.append(idx)
    
    return main_diag, anti_diag

def visualize_diagonal_constraints():
    """Create visualizations highlighting diagonal constraints."""
    # Create output directory
    os.makedirs('figures_diagonals', exist_ok=True)
    
    # Get axial points
    points, indices = create_axial_points(magic_square)
    n = magic_square.shape[0]
    
    # Identify diagonal points
    main_diag_indices, anti_diag_indices = identify_diagonals(indices, n)
    
    # Extract coordinates
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    # Define diagonal projections
    main_diag_proj = (x + y) / np.sqrt(2)
    anti_diag_proj = (x - y) / np.sqrt(2)
    
    # Create custom colormap for different point types
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # regular, main diag, anti diag, both
    node_colors = np.zeros(len(points), dtype=int)
    node_colors[main_diag_indices] = 1
    node_colors[anti_diag_indices] = 2
    for idx in set(main_diag_indices) & set(anti_diag_indices):
        node_colors[idx] = 3
    
    # 1. Create 3D visualization of points with diagonals highlighted
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot regular points
    for color_idx in range(4):
        mask = node_colors == color_idx
        ax.scatter(x[mask], y[mask], z[mask], c=[colors[color_idx]], s=100, label=['Regular', 'Main Diagonal', 'Anti-Diagonal', 'Both'][color_idx])
    
    # Connect diagonal points with lines
    ax.plot(x[main_diag_indices], y[main_diag_indices], z[main_diag_indices], 'o-', color=colors[1], linewidth=2, alpha=0.7)
    ax.plot(x[anti_diag_indices], y[anti_diag_indices], z[anti_diag_indices], 'o-', color=colors[2], linewidth=2, alpha=0.7)
    
    # Add projection vectors from origin
    origin = np.zeros(3)
    # Draw X, Y axes for reference
    ax.quiver(origin[0], origin[1], origin[2], 2, 0, 0, color='gray', arrow_length_ratio=0.1, alpha=0.5)
    ax.quiver(origin[0], origin[1], origin[2], 0, 2, 0, color='gray', arrow_length_ratio=0.1, alpha=0.5)
    # Draw diagonal projection vectors
    ax.quiver(origin[0], origin[1], origin[2], 1/np.sqrt(2), 1/np.sqrt(2), 0, color=colors[1], arrow_length_ratio=0.1, label='Main Diagonal Direction')
    ax.quiver(origin[0], origin[1], origin[2], 1/np.sqrt(2), -1/np.sqrt(2), 0, color=colors[2], arrow_length_ratio=0.1, label='Anti-Diagonal Direction')
    
    ax.set_xlabel('X (row index)')
    ax.set_ylabel('Y (column index)')
    ax.set_zlabel('Z (value)')
    ax.set_title('Magic Square Axial Representation with Diagonals Highlighted')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('figures_diagonals/3d_diagonal_visualization.png', dpi=300, bbox_inches='tight')
    
    # 2. Create visualization showing that sum of Z values along diagonals is zero
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Main diagonal Z values
    main_diag_z = z[main_diag_indices]
    x_pos = np.arange(len(main_diag_z))
    ax1.bar(x_pos, main_diag_z, color=colors[1])
    ax1.axhline(y=0, color='red', linestyle='--')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f"({indices[i][0]},{indices[i][1]})" for i in main_diag_indices])
    ax1.set_ylabel('Z Value (centered)')
    ax1.set_title('Main Diagonal Z Values\nSum = {:.4f}'.format(np.sum(main_diag_z)))
    
    # Anti-diagonal Z values
    anti_diag_z = z[anti_diag_indices]
    x_pos = np.arange(len(anti_diag_z))
    ax2.bar(x_pos, anti_diag_z, color=colors[2])
    ax2.axhline(y=0, color='red', linestyle='--')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f"({indices[i][0]},{indices[i][1]})" for i in anti_diag_indices])
    ax2.set_ylabel('Z Value (centered)')
    ax2.set_title('Anti-Diagonal Z Values\nSum = {:.4f}'.format(np.sum(anti_diag_z)))
    
    plt.tight_layout()
    plt.savefig('figures_diagonals/diagonal_z_values.png', dpi=300, bbox_inches='tight')
    
    # 3. Create visualization showing covariance calculation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Main diagonal projection vs Z
    ax1.scatter(main_diag_proj, z, color=colors[0], alpha=0.7)
    ax1.scatter(main_diag_proj[main_diag_indices], z[main_diag_indices], color=colors[1], s=100)
    
    # Add linear regression line
    coef = np.polyfit(main_diag_proj, z, 1)
    poly1d_fn = np.poly1d(coef)
    ax1.plot(sorted(main_diag_proj), poly1d_fn(sorted(main_diag_proj)), 'k--', alpha=0.5)
    
    # Add covariance information
    cov = np.cov(main_diag_proj, z)[0, 1]
    corr = np.corrcoef(main_diag_proj, z)[0, 1]
    ax1.set_title(f'Main Diagonal Projection vs Z\nCovariance = {cov:.8f}, Correlation = {corr:.8f}')
    ax1.set_xlabel('Main Diagonal Projection ((x+y)/√2)')
    ax1.set_ylabel('Z Value')
    
    # Anti-diagonal projection vs Z
    ax2.scatter(anti_diag_proj, z, color=colors[0], alpha=0.7)
    ax2.scatter(anti_diag_proj[anti_diag_indices], z[anti_diag_indices], color=colors[2], s=100)
    
    # Add linear regression line
    coef = np.polyfit(anti_diag_proj, z, 1)
    poly1d_fn = np.poly1d(coef)
    ax2.plot(sorted(anti_diag_proj), poly1d_fn(sorted(anti_diag_proj)), 'k--', alpha=0.5)
    
    # Add covariance information
    cov = np.cov(anti_diag_proj, z)[0, 1]
    corr = np.corrcoef(anti_diag_proj, z)[0, 1]
    ax2.set_title(f'Anti-Diagonal Projection vs Z\nCovariance = {cov:.8f}, Correlation = {corr:.8f}')
    ax2.set_xlabel('Anti-Diagonal Projection ((x-y)/√2)')
    ax2.set_ylabel('Z Value')
    
    plt.tight_layout()
    plt.savefig('figures_diagonals/diagonal_covariance_visualization.png', dpi=300, bbox_inches='tight')
    
    # 4. Visualize the magic square itself
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(magic_square, cmap='viridis')
    
    # Add the values inside each cell
    for i in range(n):
        for j in range(n):
            text_color = 'white' if magic_square[i, j] > 8 else 'black'
            ax.text(j, i, str(magic_square[i, j]), ha='center', va='center', color=text_color, fontsize=16)
    
    # Highlight diagonals with alpha
    diagonal_mask = np.zeros_like(magic_square, dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:  # Main diagonal
                diagonal_mask[i, j] += 0.5
            if i + j == n - 1:  # Anti-diagonal
                diagonal_mask[i, j] += 0.5
    
    # Create a white semi-transparent overlay
    rgba_data = np.zeros((n, n, 4))
    for i in range(n):
        for j in range(n):
            rgba_data[i, j, 0] = 1.0  # R
            rgba_data[i, j, 1] = 1.0  # G
            rgba_data[i, j, 2] = 1.0  # B
            rgba_data[i, j, 3] = diagonal_mask[i, j]  # Alpha
    
    ax.imshow(rgba_data, alpha=0.3)
    
    # Add row and column sums
    row_sums = np.sum(magic_square, axis=1)
    col_sums = np.sum(magic_square, axis=0)
    diag_sum = np.trace(magic_square)
    anti_diag_sum = np.trace(np.fliplr(magic_square))
    
    for i in range(n):
        ax.text(n, i, str(row_sums[i]), ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(i, n, str(col_sums[i]), ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.text(-0.5, -0.5, f"Main Diag Sum: {diag_sum}", ha='left', va='center', fontsize=12)
    ax.text(-0.5, n, f"Anti-Diag Sum: {anti_diag_sum}", ha='left', va='center', fontsize=12)
    
    ax.set_title('Magic Square with Diagonals Highlighted')
    plt.tight_layout()
    plt.savefig('figures_diagonals/magic_square_highlighted.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    visualize_diagonal_constraints()
    print("Visualizations created in 'figures_diagonals' directory.") 