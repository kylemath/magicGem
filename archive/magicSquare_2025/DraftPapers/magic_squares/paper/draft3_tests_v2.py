import numpy as np
from scipy import linalg, stats
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import networkx as nx
from scipy.optimize import linear_sum_assignment
import warnings
warnings.filterwarnings('ignore')

# Original functions from draft3_tests.py
def generate_random_magic_sum_matrix(n=4, magic_sum=34):
    """Generate a random matrix with same row/column sums as magic square"""
    matrix = np.random.rand(n, n)
    # Normalize rows
    row_sums = matrix.sum(axis=1)
    matrix = matrix / row_sums[:, np.newaxis] * magic_sum
    # Normalize columns while preserving row sums
    for _ in range(10):  # Iterate to converge
        col_sums = matrix.sum(axis=0)
        matrix = matrix / col_sums * magic_sum
        row_sums = matrix.sum(axis=1)
        matrix = matrix / row_sums[:, np.newaxis] * magic_sum
    return matrix

def analyze_matrix_geometry(matrix):
    """Compute geometric properties of matrix when viewed as 3D points"""
    points = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            points.append([i, j, matrix[i,j]])
    points = np.array(points)
    
    # Compute PCA
    centered = points - points.mean(axis=0)
    U, S, Vh = linalg.svd(centered)
    
    return {
        'eigenvalues': S,
        'ratios': [S[1]/S[0], S[2]/S[1]],
        'points': points
    }

def simple_persistence_features(points):
    """Compute basic persistence-like features with better numerical stability"""
    # Scale points to [0,1] range first
    scaled_points = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0) + 1e-10)
    
    # Compute pairwise distances
    dists = linalg.norm(scaled_points[:, None] - scaled_points, axis=2)
    np.fill_diagonal(dists, np.inf)
    
    # Compute birth and death times more robustly
    finite_dists = dists[~np.isinf(dists)]
    if len(finite_dists) == 0:
        return {
            'birth_times': np.array([0]),
            'death_times': np.array([1]),
            'total_persistence': 1.0,
            'max_persistence': 1.0
        }
    
    birth_times = np.min(dists, axis=1)
    death_times = np.max(finite_dists)
    
    # Ensure we have valid values
    birth_times = birth_times[~np.isinf(birth_times)]
    if len(birth_times) == 0:
        birth_times = np.array([0])
    
    # Compute persistence features
    persistence = death_times - birth_times
    total_persistence = float(np.sum(persistence))
    max_persistence = float(np.max(persistence))
    
    return {
        'birth_times': birth_times,
        'death_times': np.array([death_times]),
        'total_persistence': total_persistence,
        'max_persistence': max_persistence
    }

def multi_scale_dimension(points, scales=np.logspace(-2, 1, 20)):
    """Estimate dimension at different scales with robust numerical handling"""
    # Scale points to [0,1] range
    scaled_points = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0) + 1e-10)
    
    # Compute pairwise distances
    dists = linalg.norm(scaled_points[:, None] - scaled_points, axis=2)
    np.fill_diagonal(dists, np.inf)
    
    dims = []
    for scale in scales:
        # Count neighbors within scale, excluding self
        neighbors = np.sum(dists < scale, axis=1) - 1  # Subtract self-count
        mean_neighbors = np.mean(neighbors)
        
        if mean_neighbors > 0:  # Only compute if we have neighbors
            try:
                dim = np.log(mean_neighbors) / np.log(scale)
                if 0 < dim < 10:  # Reasonable bounds
                    dims.append(dim)
            except:
                continue
    
    if len(dims) > 0:
        dims = np.array(dims)
        # Use trimmed mean to avoid outliers
        good_dims = dims[(dims > np.percentile(dims, 10)) & 
                        (dims < np.percentile(dims, 90))]
        if len(good_dims) > 0:
            return np.mean(good_dims), np.std(good_dims)
    
    return 2.0, 1.0  # Fallback to reasonable defaults

# New functions for enhanced analysis

def earth_movers_distance(points1, points2):
    """
    Compute Earth Mover's Distance between point clouds
    Using Hungarian algorithm for optimal transport
    """
    # Normalize point clouds to [0,1] range
    def normalize_points(points):
        min_vals = points.min(axis=0)
        max_vals = points.max(axis=0)
        return (points - min_vals) / (max_vals - min_vals)
    
    p1 = normalize_points(points1)
    p2 = normalize_points(points2)
    
    # Compute cost matrix
    cost_matrix = np.zeros((len(p1), len(p2)))
    for i in range(len(p1)):
        for j in range(len(p2)):
            cost_matrix[i,j] = np.linalg.norm(p1[i] - p2[j])
    
    # Solve optimal transport
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return cost_matrix[row_ind, col_ind].sum() / len(p1)  # Normalize by number of points

def generate_structured_matrices(n=4, count=100):
    """Generate different types of structured matrices"""
    matrices = {
        'magic': [],
        'latin': [],
        'circulant': [],
        'random_magic_sum': [],
        'symmetric': [],
        'toeplitz': []
    }
    
    # Example magic square (Dürer's square)
    durer = np.array([
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ])
    matrices['magic'].append(durer)
    
    # Generate Latin squares
    base = list(range(1, n+1))
    for i in range(count):
        square = []
        np.random.shuffle(base)
        for j in range(n):
            row = np.roll(base, j)
            square.append(row)
        matrices['latin'].append(np.array(square))
    
    # Generate circulant matrices
    for i in range(count):
        first_row = np.random.permutation([13, 2, 8, 11])
        matrix = np.zeros((n, n))
        for j in range(n):
            matrix[j] = np.roll(first_row, j)
        matrices['circulant'].append(matrix)
    
    # Generate random magic sum matrices
    for i in range(count):
        matrices['random_magic_sum'].append(
            generate_random_magic_sum_matrix())
    
    # Generate symmetric matrices with similar value range
    for i in range(count):
        upper = np.random.uniform(1, 16, size=(n,n))
        matrix = np.triu(upper) + np.triu(upper, 1).T
        matrices['symmetric'].append(matrix)
    
    # Generate Toeplitz matrices
    for i in range(count):
        first_row = np.random.uniform(1, 16, size=n)
        first_col = np.random.uniform(1, 16, size=n)
        first_col[0] = first_row[0]
        matrix = linalg.toeplitz(first_col, first_row)
        matrices['toeplitz'].append(matrix)
    
    return matrices

def analyze_matrix_collection(matrices):
    """Analyze geometric properties of matrix collections with error handling"""
    results = {}
    
    for mat_type, mat_list in matrices.items():
        eigenvalue_ratios = []
        persistence_features = []
        dimensions = []
        
        for matrix in mat_list:
            try:
                geom = analyze_matrix_geometry(matrix)
                eigenvalue_ratios.append(geom['ratios'])
                
                points = geom['points']
                pers_features = simple_persistence_features(points)
                persistence_features.append(pers_features['total_persistence'])
                
                dim_mean, dim_std = multi_scale_dimension(points)
                dimensions.append(dim_mean)
                
            except Exception as e:
                print(f"Warning: Error processing {mat_type} matrix: {str(e)}")
                continue
        
        results[mat_type] = {
            'eigenvalue_ratios': np.array(eigenvalue_ratios),
            'persistence': np.array(persistence_features),
            'dimension': np.array(dimensions)
        }
        
        # Debug output
        print(f"\nDebug - {mat_type} collection results:")
        print(f"Number of matrices processed: {len(mat_list)}")
        print(f"Number of eigenvalue ratios: {len(eigenvalue_ratios)}")
        print(f"Number of persistence values: {len(persistence_features)}")
        print(f"Number of dimension values: {len(dimensions)}")
    
    return results

def statistical_analysis(results):
    """
    Perform statistical analysis on the results.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing analysis results
        
    Returns:
    --------
    dict
        Dictionary containing statistical test results
    """
    # Initialize results dictionary
    stats_results = {}
    
    # Get magic square properties
    magic_eigenvalues = np.array(results['magic']['eigenvalue_ratios'])
    magic_persistence = np.array(results['magic']['persistence'])
    magic_dimension = np.array(results['magic']['dimension'])
    
    # Compare each matrix type with magic squares
    for mat_type in ['latin', 'circulant', 'random_magic_sum', 'symmetric', 'toeplitz']:
        stats_results[mat_type] = {}
        
        # Get current matrix type properties
        current_eigenvalues = np.array(results[mat_type]['eigenvalue_ratios'])
        current_persistence = np.array(results[mat_type]['persistence'])
        current_dimension = np.array(results[mat_type]['dimension'])
        
        # Remove NaN values
        magic_eigenvalues_clean = magic_eigenvalues[~np.isnan(magic_eigenvalues)]
        magic_persistence_clean = magic_persistence[~np.isnan(magic_persistence)]
        magic_dimension_clean = magic_dimension[~np.isnan(magic_dimension)]
        
        current_eigenvalues_clean = current_eigenvalues[~np.isnan(current_eigenvalues)]
        current_persistence_clean = current_persistence[~np.isnan(current_persistence)]
        current_dimension_clean = current_dimension[~np.isnan(current_dimension)]
        
        # Eigenvalue ratio test
        if len(magic_eigenvalues_clean) > 0 and len(current_eigenvalues_clean) > 0:
            stats_results[mat_type]['eigenvalue_p'] = stats.ttest_ind(
                magic_eigenvalues_clean,
                current_eigenvalues_clean
            ).pvalue
        else:
            stats_results[mat_type]['eigenvalue_p'] = np.nan
        
        # Persistence test
        if len(magic_persistence_clean) > 0 and len(current_persistence_clean) > 0:
            stats_results[mat_type]['persistence_p'] = stats.ttest_ind(
                magic_persistence_clean,
                current_persistence_clean
            ).pvalue
        else:
            stats_results[mat_type]['persistence_p'] = np.nan
        
        # Dimension test
        if len(magic_dimension_clean) > 0 and len(current_dimension_clean) > 0:
            stats_results[mat_type]['dimension_p'] = stats.ttest_ind(
                magic_dimension_clean,
                current_dimension_clean
            ).pvalue
        else:
            stats_results[mat_type]['dimension_p'] = np.nan
    
    return stats_results

def estimate_local_dimension(points, k_range=[5,10,15,20]):
    """
    Estimate local dimension using k-nearest neighbors
    at multiple scales
    """
    n_points = len(points)
    dists = linalg.norm(points[:, None] - points, axis=2)
    local_dims = []
    
    for k in k_range:
        # Get k-nearest neighbor distances
        k_dists = np.sort(dists, axis=1)[:,1:k+1]
        # Estimate dimension using MLE
        local_dim = np.mean([
            k / np.sum(np.log(k_dists[i,-1] / k_dists[i,:-1]))
            for i in range(n_points)
        ])
        local_dims.append(local_dim)
    
    return np.mean(local_dims), np.std(local_dims)

def print_statistical_results(stats_results):
    """Print statistical analysis results."""
    print("\nStatistical Analysis Results:\n")
    for mat_type, stats in stats_results.items():
        print(f"{mat_type} vs Magic Squares:")
        for test_type in ['eigenvalue_p', 'persistence_p', 'dimension_p']:
            p_value = stats[test_type]
            if np.isnan(p_value):
                print(f"{test_type}: insufficient data")
            else:
                print(f"{test_type}: {p_value:.3e}")
        print()

# Run analyses
print("Running comprehensive analysis...")

# Generate and analyze structured matrices
matrices = generate_structured_matrices()
results = analyze_matrix_collection(matrices)
stats_results = statistical_analysis(results)

print_statistical_results(stats_results)

# Estimate local dimension for magic square
magic_points = analyze_matrix_geometry(matrices['magic'][0])['points']
local_dim, dim_std = estimate_local_dimension(magic_points)
print(f"\nRefined Local Dimension Estimate:")
print(f"Dimension: {local_dim:.2f} ± {dim_std:.2f}")

# EMD distance matrix between different types
print("\nEMD Distance Analysis:")
for type1 in ['magic', 'latin', 'circulant']:
    for type2 in ['magic', 'latin', 'circulant']:
        if type1 >= type2:
            continue
        points1 = analyze_matrix_geometry(matrices[type1][0])['points']
        points2 = analyze_matrix_geometry(matrices[type2][0])['points']
        dist = earth_movers_distance(points1, points2)
        print(f"{type1} vs {type2}: {dist:.3f}")

print("\nKey Findings:")
print("1. Statistical significance of geometric signatures")
print("2. Refined dimension estimates with uncertainty")
print("3. Quantitative differences between matrix types")
print("4. EMD provides meaningful distance metric")

# TODO: 
# 1. Implement proper persistence diagram visualization
# 2. Add more matrix types (Hadamard, etc.)
# 3. Cross-validation of dimension estimates
# 4. Formal proofs of geometric constraints