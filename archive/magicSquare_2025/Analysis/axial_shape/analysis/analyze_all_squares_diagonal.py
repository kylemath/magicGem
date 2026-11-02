import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from tqdm import tqdm
import os
from axialDay2 import AxialAnalyzer

def load_squares():
    """Load the magic squares."""
    squares_path = '../../magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, squares_path)
    
    if not os.path.exists(full_path):
        # Try the root directory
        root_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 
                                'magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy')
        if os.path.exists(root_path):
            return np.load(root_path)
        raise FileNotFoundError(f"Could not find magic squares file at {full_path} or {root_path}")
    
    return np.load(full_path)

def create_axial_points(square):
    """Create 3D points from a magic square using the axial representation."""
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

def analyze_diagonal_constraints(points):
    """Analyze diagonal constraints in axial representation."""
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    # Create projections along diagonal directions
    main_diag_proj = (x + y) / np.sqrt(2)
    anti_diag_proj = (x - y) / np.sqrt(2)
    
    # Compute covariances
    cov_main_diag = np.cov(main_diag_proj, z)[0, 1]
    cov_anti_diag = np.cov(anti_diag_proj, z)[0, 1]
    
    # Also compute the normalized covariance (correlation coefficient)
    corr_main_diag = np.corrcoef(main_diag_proj, z)[0, 1]
    corr_anti_diag = np.corrcoef(anti_diag_proj, z)[0, 1]
    
    return {
        'cov_main_diagonal': cov_main_diag,
        'cov_anti_diagonal': cov_anti_diag,
        'corr_main_diagonal': corr_main_diag,
        'corr_anti_diagonal': corr_anti_diag
    }

def analyze_diagonal_eigendecomposition(points):
    """Analyze if diagonal constraints can be represented as eigenvalues."""
    # Form a 5D vector for each point: [x, y, z, d1, d2]
    # where d1 = (x+y)/√2 and d2 = (x-y)/√2 are diagonal projections
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    d1 = (x + y) / np.sqrt(2)  # Main diagonal projection
    d2 = (x - y) / np.sqrt(2)  # Anti-diagonal projection
    
    # Create the extended vectors
    extended_points = np.column_stack((x, y, z, d1, d2))
    
    # Compute covariance matrix of extended points
    cov_matrix = np.cov(extended_points.T)
    
    # Perform eigendecomposition
    eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
    
    return {
        'extended_cov': cov_matrix,
        'extended_eigenvals': eigenvals,
        'extended_eigenvecs': eigenvecs
    }

def analyze_squares(squares):
    """Analyze all squares and collect metrics."""
    results = []
    diagonal_eigvals = []
    
    for i, square in enumerate(tqdm(squares, desc="Analyzing squares")):
        # Create axial points
        points = create_axial_points(square)
        
        # Compute standard metrics with AxialAnalyzer
        analyzer = AxialAnalyzer(square)
        metrics = analyzer.compute_balance_metrics()
        
        # Analyze diagonal constraints
        diag_metrics = analyze_diagonal_constraints(points)
        
        # Analyze diagonal eigendecomposition
        diag_eigen = analyze_diagonal_eigendecomposition(points)
        diagonal_eigvals.append(diag_eigen['extended_eigenvals'])
        
        # Combine metrics
        result = {
            'square_id': i,
            'balance_measure': metrics['balance_measure'],
            'rms_distance': metrics['rms_distance'],
            'condition_number': metrics['condition_number'],
            'skewness_magnitude': metrics['skewness_magnitude'],
            'eigenvalue_1': metrics['eigenvalues'][0],
            'eigenvalue_2': metrics['eigenvalues'][1],
            'eigenvalue_3': metrics['eigenvalues'][2],
            'cov_main_diagonal': diag_metrics['cov_main_diagonal'],
            'cov_anti_diagonal': diag_metrics['cov_anti_diagonal'],
            'corr_main_diagonal': diag_metrics['corr_main_diagonal'],
            'corr_anti_diagonal': diag_metrics['corr_anti_diagonal']
        }
        results.append(result)
    
    return pd.DataFrame(results), np.array(diagonal_eigvals)

def visualize_diagonal_metrics(df, diagonal_eigvals, save_dir):
    """Visualize the diagonal covariance metrics."""
    # Set the visual style
    sns.set(style="whitegrid")
    
    # Create figure directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Diagonal covariance distribution
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['cov_main_diagonal'], kde=True, color='blue')
    plt.title('Main Diagonal Covariance Distribution')
    plt.xlabel('Covariance Value')
    plt.axvline(x=0, color='red', linestyle='--')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['cov_anti_diagonal'], kde=True, color='green')
    plt.title('Anti-Diagonal Covariance Distribution')
    plt.xlabel('Covariance Value')
    plt.axvline(x=0, color='red', linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/diagonal_covariance_distribution.png', dpi=300)
    
    # 2. Diagonal correlation distribution
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['corr_main_diagonal'], kde=True, color='blue')
    plt.title('Main Diagonal Correlation Distribution')
    plt.xlabel('Correlation Coefficient')
    plt.axvline(x=0, color='red', linestyle='--')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['corr_anti_diagonal'], kde=True, color='green')
    plt.title('Anti-Diagonal Correlation Distribution')
    plt.xlabel('Correlation Coefficient')
    plt.axvline(x=0, color='red', linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/diagonal_correlation_distribution.png', dpi=300)
    
    # 3. Scatterplot of main vs anti-diagonal covariance
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='cov_main_diagonal', y='cov_anti_diagonal', data=df)
    plt.title('Main Diagonal vs Anti-Diagonal Covariance')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'{save_dir}/diagonal_covariance_scatter.png', dpi=300)
    
    # 4. Extended eigenvalue distribution
    mean_eigenvals = np.mean(diagonal_eigvals, axis=0)
    std_eigenvals = np.std(diagonal_eigvals, axis=0)
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, 6), mean_eigenvals, yerr=std_eigenvals, capsize=5)
    plt.title('Extended Eigenvalues (Including Diagonal Projections)')
    plt.xlabel('Eigenvalue Index')
    plt.ylabel('Eigenvalue Magnitude')
    plt.yscale('log')
    plt.xticks(range(1, 6))
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{save_dir}/extended_eigenvalues.png', dpi=300)
    
    # 5. Create a heatmap of the average extended covariance matrix
    # Compute average extended covariance matrix for first 10 squares
    squares = load_squares()[:10]
    avg_cov = np.zeros((5, 5))
    
    for square in squares:
        points = create_axial_points(square)
        diag_eigen = analyze_diagonal_eigendecomposition(points)
        avg_cov += diag_eigen['extended_cov']
    
    avg_cov /= len(squares)
    
    plt.figure(figsize=(10, 8))
    labels = ['x', 'y', 'z', 'Main Diag', 'Anti Diag']
    sns.heatmap(avg_cov, annot=True, fmt='.4f', cmap='viridis', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Average Extended Covariance Matrix')
    plt.tight_layout()
    plt.savefig(f'{save_dir}/extended_covariance_heatmap.png', dpi=300)

def analyze_and_save():
    """Main function to run analysis and save results."""
    # Create output directory
    save_dir = 'figures_diagonals'
    os.makedirs(save_dir, exist_ok=True)
    
    # Load squares
    print("Loading magic squares...")
    squares = load_squares()
    print(f"Loaded {len(squares)} squares")
    
    # Analyze squares
    print("Analyzing squares...")
    results_df, diagonal_eigvals = analyze_squares(squares)
    
    # Save results
    results_df.to_csv(f'{save_dir}/diagonal_metrics.csv', index=False)
    np.save(f'{save_dir}/diagonal_eigvals.npy', diagonal_eigvals)
    
    # Compute summary statistics
    summary = results_df.describe()
    summary.to_csv(f'{save_dir}/diagonal_metrics_summary.csv')
    
    # Create visualizations
    print("Creating visualizations...")
    visualize_diagonal_metrics(results_df, diagonal_eigvals, save_dir)
    
    # Print key findings
    print("\nAnalysis Complete!")
    print("\nDiagonal Constraint Statistics:")
    print("===========================")
    print(f"Average main diagonal covariance: {results_df['cov_main_diagonal'].mean():.8f}")
    print(f"Average anti-diagonal covariance: {results_df['cov_anti_diagonal'].mean():.8f}")
    print(f"Standard deviation of main diagonal covariance: {results_df['cov_main_diagonal'].std():.8f}")
    print(f"Standard deviation of anti-diagonal covariance: {results_df['cov_anti_diagonal'].std():.8f}")
    
    # Check if all values are near zero (within numerical precision)
    tol = 1e-10
    all_main_diag_zero = np.all(np.abs(results_df['cov_main_diagonal']) < tol)
    all_anti_diag_zero = np.all(np.abs(results_df['cov_anti_diagonal']) < tol)
    
    print("\nConstraint Verification:")
    print("=====================")
    print(f"All main diagonal covariances ≈ 0: {all_main_diag_zero}")
    print(f"All anti-diagonal covariances ≈ 0: {all_anti_diag_zero}")
    
    # Analyze extended eigenvalues
    mean_extended_eigenvals = np.mean(diagonal_eigvals, axis=0)
    print("\nExtended Eigenvalue Analysis:")
    print("=========================")
    for i, val in enumerate(mean_extended_eigenvals):
        print(f"Extended eigenvalue {i+1}: {val:.6f}")

if __name__ == '__main__':
    analyze_and_save() 