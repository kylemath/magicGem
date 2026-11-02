import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import os

# A standard 4x4 magic square for reference
magic_square = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

def create_non_magic_arrangements():
    """Create a series of non-magic arrangements by modifying the magic square."""
    arrangements = []
    
    # 1. Arrangement with unequal row sums (swap two elements in a row)
    row_modified = magic_square.copy()
    row_modified[0, 0], row_modified[0, 1] = row_modified[0, 1], row_modified[0, 0]
    arrangements.append(("Row Modified", row_modified))
    
    # 2. Arrangement with unequal column sums (swap two elements in a column)
    col_modified = magic_square.copy()
    col_modified[0, 0], col_modified[1, 0] = col_modified[1, 0], col_modified[0, 0]
    arrangements.append(("Column Modified", col_modified))
    
    # 3. Arrangement with unequal diagonal sum (swap diagonal and non-diagonal elements)
    diag_modified = magic_square.copy()
    diag_modified[0, 0], diag_modified[0, 1] = diag_modified[0, 1], diag_modified[0, 0]
    arrangements.append(("Diagonal Modified", diag_modified))
    
    # 4. Arrangement with unequal anti-diagonal sum
    anti_diag_modified = magic_square.copy()
    anti_diag_modified[0, 3], anti_diag_modified[0, 2] = anti_diag_modified[0, 2], anti_diag_modified[0, 3]
    arrangements.append(("Anti-Diagonal Modified", anti_diag_modified))
    
    # 5. Random arrangement (but keeping the same set of numbers 1-16)
    numbers = np.arange(1, 17)
    np.random.shuffle(numbers)
    random_arrangement = numbers.reshape(4, 4)
    arrangements.append(("Random Arrangement", random_arrangement))
    
    # 6. Arrangement with some structure (transpose of magic square)
    arrangements.append(("Transpose", magic_square.T))
    
    return arrangements

def create_axial_points(square):
    """Create 3D points from a square arrangement using the axial representation."""
    n = square.shape[0]
    points = []
    
    for i in range(n):
        for j in range(n):
            point = np.array([
                i - (n-1)/2,  # x-coordinate (row-based)
                j - (n-1)/2,  # y-coordinate (column-based)
                square[i, j] - np.mean(square)  # z-coordinate (value-based)
            ])
            points.append(point)
    
    return np.array(points)

def compute_covariance_metrics(square):
    """Compute covariance metrics for an arrangement."""
    points = create_axial_points(square)
    
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    # Create diagonal projections
    main_diag_proj = (x + y) / np.sqrt(2)
    anti_diag_proj = (x - y) / np.sqrt(2)
    
    # Compute covariances
    cov_x_z = np.cov(x, z)[0, 1]
    cov_y_z = np.cov(y, z)[0, 1]
    cov_main_diag = np.cov(main_diag_proj, z)[0, 1]
    cov_anti_diag = np.cov(anti_diag_proj, z)[0, 1]
    
    # Compute correlations
    corr_x_z = np.corrcoef(x, z)[0, 1]
    corr_y_z = np.corrcoef(y, z)[0, 1]
    corr_main_diag = np.corrcoef(main_diag_proj, z)[0, 1]
    corr_anti_diag = np.corrcoef(anti_diag_proj, z)[0, 1]
    
    # Compute eigendecomposition
    cov_matrix = np.cov(points.T)
    eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
    
    # Compute extended covariance with diagonal projections
    extended_points = np.column_stack((x, y, z, main_diag_proj, anti_diag_proj))
    extended_cov = np.cov(extended_points.T)
    extended_eigenvals, _ = np.linalg.eigh(extended_cov)
    
    # Analyze row and column sums
    row_sums = np.sum(square, axis=1)
    col_sums = np.sum(square, axis=0)
    diag_sum = np.trace(square)
    anti_diag_sum = np.trace(np.fliplr(square))
    
    return {
        'points': points,
        'cov_x_z': cov_x_z,
        'cov_y_z': cov_y_z,
        'cov_main_diag': cov_main_diag,
        'cov_anti_diag': cov_anti_diag,
        'corr_x_z': corr_x_z,
        'corr_y_z': corr_y_z,
        'corr_main_diag': corr_main_diag,
        'corr_anti_diag': corr_anti_diag,
        'eigenvals': eigenvals,
        'eigenvecs': eigenvecs,
        'extended_eigenvals': extended_eigenvals,
        'row_sums': row_sums,
        'col_sums': col_sums,
        'diag_sum': diag_sum,
        'anti_diag_sum': anti_diag_sum
    }

def visualize_covariance_comparison(arrangements, metrics_list):
    """Visualize comparison of covariance properties between arrangements."""
    # Create output directory
    save_dir = 'figures_non_magic'
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Create bar plot comparing covariance values
    plt.figure(figsize=(15, 8))
    
    # Extract arrangement names and covariance values
    names = [name for name, _ in arrangements]
    cov_x_z_values = [metrics['cov_x_z'] for metrics in metrics_list]
    cov_y_z_values = [metrics['cov_y_z'] for metrics in metrics_list]
    cov_main_diag_values = [metrics['cov_main_diag'] for metrics in metrics_list]
    cov_anti_diag_values = [metrics['cov_anti_diag'] for metrics in metrics_list]
    
    # Create bar positions
    bar_width = 0.2
    r1 = np.arange(len(names))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
    
    # Create bars
    plt.bar(r1, cov_x_z_values, width=bar_width, label='Cov(x,z) (Rows)')
    plt.bar(r2, cov_y_z_values, width=bar_width, label='Cov(y,z) (Columns)')
    plt.bar(r3, cov_main_diag_values, width=bar_width, label='Cov(main_diag,z)')
    plt.bar(r4, cov_anti_diag_values, width=bar_width, label='Cov(anti_diag,z)')
    
    # Add reference line at y=0
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Customize plot
    plt.xlabel('Arrangement Type')
    plt.ylabel('Covariance Value')
    plt.title('Covariance Values for Different Arrangements')
    plt.xticks([r + 1.5 * bar_width for r in range(len(names))], names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{save_dir}/covariance_comparison.png', dpi=300, bbox_inches='tight')
    
    # 2. Create heatmap of correlation values
    plt.figure(figsize=(12, 8))
    
    # Create correlation matrix
    corr_data = np.zeros((len(names), 4))
    for i, metrics in enumerate(metrics_list):
        corr_data[i, 0] = metrics['corr_x_z']
        corr_data[i, 1] = metrics['corr_y_z']
        corr_data[i, 2] = metrics['corr_main_diag']
        corr_data[i, 3] = metrics['corr_anti_diag']
    
    # Create heatmap
    sns.heatmap(corr_data, annot=True, fmt='.4f', cmap='RdBu_r', center=0,
                xticklabels=['Rows', 'Columns', 'Main Diag', 'Anti-Diag'],
                yticklabels=names)
    plt.title('Correlation Values for Different Arrangements')
    plt.tight_layout()
    plt.savefig(f'{save_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    
    # 3. Create visualization of sum properties
    plt.figure(figsize=(14, 8))
    
    # Plot 1: Row sums
    plt.subplot(2, 2, 1)
    for i, metrics in enumerate(metrics_list):
        plt.plot(metrics['row_sums'], 'o-', label=names[i])
    plt.title('Row Sums')
    plt.xlabel('Row Index')
    plt.ylabel('Sum')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Column sums
    plt.subplot(2, 2, 2)
    for i, metrics in enumerate(metrics_list):
        plt.plot(metrics['col_sums'], 'o-', label=names[i])
    plt.title('Column Sums')
    plt.xlabel('Column Index')
    plt.ylabel('Sum')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Diagonal sums
    plt.subplot(2, 2, 3)
    diag_sums = [[metrics['diag_sum'], metrics['anti_diag_sum']] for metrics in metrics_list]
    x_pos = np.arange(2)
    width = 0.8 / len(names)
    for i, (name, sums) in enumerate(zip(names, diag_sums)):
        pos = x_pos + i * width - 0.4 + width/2
        plt.bar(pos, sums, width=width, label=name)
    plt.title('Diagonal Sums')
    plt.xticks([0, 1], ['Main Diagonal', 'Anti-Diagonal'])
    plt.ylabel('Sum')
    plt.grid(True, axis='y', alpha=0.3)
    
    # Plot 4: Legend
    plt.subplot(2, 2, 4)
    plt.axis('off')
    plt.legend(loc='center', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/sum_properties.png', dpi=300, bbox_inches='tight')
    
    # 4. Create visualization of eigenvalue properties
    plt.figure(figsize=(14, 8))
    
    # Plot 1: 3D eigenvalues
    plt.subplot(1, 2, 1)
    for i, metrics in enumerate(metrics_list):
        plt.plot(metrics['eigenvals'], 'o-', label=names[i])
    plt.title('Eigenvalues of 3D Covariance Matrix')
    plt.xlabel('Eigenvalue Index')
    plt.ylabel('Eigenvalue Magnitude')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: 5D extended eigenvalues
    plt.subplot(1, 2, 2)
    for i, metrics in enumerate(metrics_list):
        plt.plot(metrics['extended_eigenvals'], 'o-', label=names[i])
    plt.title('Eigenvalues of Extended 5D Covariance Matrix')
    plt.xlabel('Eigenvalue Index')
    plt.ylabel('Eigenvalue Magnitude')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/eigenvalue_properties.png', dpi=300, bbox_inches='tight')
    
    # 5. Create 3D visualizations of the points with eigenvectors
    for i, ((name, _), metrics) in enumerate(zip(arrangements, metrics_list)):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot points
        points = metrics['points']
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=points[:, 2], cmap='viridis', s=50)
        
        # Plot eigenvectors scaled by eigenvalues
        origin = np.zeros(3)
        colors = ['r', 'g', 'b']
        eigenvals = metrics['eigenvals']
        eigenvecs = metrics['eigenvecs']
        
        for j in range(3):
            vec = eigenvecs[:, j] * np.sqrt(eigenvals[j])
            ax.quiver(origin[0], origin[1], origin[2], 
                    vec[0], vec[1], vec[2], 
                    color=colors[j], arrow_length_ratio=0.1,
                    label=f"Eigenvector {j+1} (λ={eigenvals[j]:.2f})")
        
        ax.set_xlabel('X (row index)')
        ax.set_ylabel('Y (column index)')
        ax.set_zlabel('Z (value)')
        ax.set_title(f'3D Points and Eigenvectors for {name}')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(f'{save_dir}/3d_points_{i}_{name.replace(" ", "_").lower()}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

def print_summary_stats(arrangements, metrics_list):
    """Print summary statistics for all arrangements."""
    print("\nCovariance Properties Summary:")
    print("==========================")
    
    headers = ["Arrangement", "Cov(x,z)", "Cov(y,z)", "Cov(main_diag,z)", "Cov(anti_diag,z)"]
    print(f"{headers[0]:<20} {headers[1]:<12} {headers[2]:<12} {headers[3]:<16} {headers[4]:<16}")
    print("-" * 80)
    
    for (name, _), metrics in zip(arrangements, metrics_list):
        cov_x_z = metrics['cov_x_z']
        cov_y_z = metrics['cov_y_z']
        cov_main_diag = metrics['cov_main_diag']
        cov_anti_diag = metrics['cov_anti_diag']
        
        print(f"{name:<20} {cov_x_z:<12.6f} {cov_y_z:<12.6f} {cov_main_diag:<16.6f} {cov_anti_diag:<16.6f}")
    
    print("\nSum Properties Summary:")
    print("====================")
    
    print(f"{'Arrangement':<20} {'Row Sum Range':<20} {'Col Sum Range':<20} {'Diag Sum':<12} {'Anti-Diag Sum':<12}")
    print("-" * 90)
    
    for (name, _), metrics in zip(arrangements, metrics_list):
        row_min, row_max = np.min(metrics['row_sums']), np.max(metrics['row_sums'])
        col_min, col_max = np.min(metrics['col_sums']), np.max(metrics['col_sums'])
        diag_sum = metrics['diag_sum']
        anti_diag_sum = metrics['anti_diag_sum']
        
        row_range = f"{row_min}-{row_max}" if row_min != row_max else f"{row_min}"
        col_range = f"{col_min}-{col_max}" if col_min != col_max else f"{col_min}"
        
        print(f"{name:<20} {row_range:<20} {col_range:<20} {diag_sum:<12} {anti_diag_sum:<12}")
    
    print("\nEigenvalue Properties Summary:")
    print("===========================")
    
    headers = ["Arrangement", "Eigenvalues (3D)", "Alignment with Axes"]
    print(f"{headers[0]:<20} {headers[1]:<30} {headers[2]:<30}")
    print("-" * 80)
    
    for (name, _), metrics in zip(arrangements, metrics_list):
        eigenvals = metrics['eigenvals']
        eigenvecs = metrics['eigenvecs']
        
        # Check alignment with axes
        alignment = "Yes" if np.allclose(np.abs(eigenvecs), np.eye(3), atol=1e-10) else "No"
        
        print(f"{name:<20} [{eigenvals[0]:.2f}, {eigenvals[1]:.2f}, {eigenvals[2]:.2f}] {alignment:<30}")

def test_non_magic_arrangements():
    """Main function to test non-magic arrangements."""
    # Create arrangements
    arrangements = create_non_magic_arrangements()
    
    # Add the original magic square as reference
    arrangements.insert(0, ("Magic Square", magic_square))
    
    # Compute metrics for all arrangements
    metrics_list = []
    for _, square in arrangements:
        metrics = compute_covariance_metrics(square)
        metrics_list.append(metrics)
    
    # Visualize comparisons
    visualize_covariance_comparison(arrangements, metrics_list)
    
    # Print summary statistics
    print_summary_stats(arrangements, metrics_list)

if __name__ == '__main__':
    # Set random seed for reproducibility
    np.random.seed(42)
    
    test_non_magic_arrangements()
    print("Analysis complete. Visualizations saved in 'figures_non_magic' directory.") 