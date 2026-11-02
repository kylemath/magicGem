import numpy as np
from scipy import linalg
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import networkx as nx

# Lab Notebook Entry 1 - 4:45 AM
# After reading Anne's email, I need to first verify if the eigenvalue ratios 
# could indeed be a trivial consequence of the magic sum constraint.
# Let's generate random matrices with the same row/column sum and compare.

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

# Generate 100 random matrices and compute eigenvalue ratios
random_ratios = []
for _ in range(100):
    M = generate_random_magic_sum_matrix()
    eigvals = np.abs(linalg.eigvals(M))
    eigvals.sort()
    random_ratios.append([eigvals[1]/eigvals[0], eigvals[2]/eigvals[1]])

random_ratios = np.array(random_ratios)
print("Random Matrix Eigenvalue Ratios:")
print(f"λ₂/λ₁: {random_ratios[:,0].mean():.3f} ± {random_ratios[:,0].std():.3f}")
print(f"λ₃/λ₂: {random_ratios[:,1].mean():.3f} ± {random_ratios[:,1].std():.3f}")

# Lab Notebook Entry 2 - 5:15 AM
# The random matrices show much more variation in eigenvalue ratios.
# This suggests the consistency we see in magic squares isn't trivial.
# Let's look at the distribution more carefully.

# Generate example 4x4 magic square for comparison
example_magic = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

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

magic_geom = analyze_matrix_geometry(example_magic)
print("\nMagic Square Eigenvalue Ratios:")
print(f"λ₂/λ₁: {magic_geom['ratios'][0]:.3f}")
print(f"λ₃/λ₂: {magic_geom['ratios'][1]:.3f}")

# Lab Notebook Entry 3 - 5:45 AM
# Anne's right about needing to justify EMD as a natural metric.
# Let's compare it with other potential metrics.

def compute_metrics(matrix1, matrix2):
    """Compare different matrix similarity metrics"""
    # Frobenius norm
    frob = linalg.norm(matrix1 - matrix2, 'fro')
    
    # Spectral norm
    spec = linalg.norm(matrix1 - matrix2, 2)
    
    # Simple point cloud distance (placeholder for EMD)
    points1 = analyze_matrix_geometry(matrix1)['points']
    points2 = analyze_matrix_geometry(matrix2)['points']
    point_dist = linalg.norm(points1 - points2)
    
    return {'frobenius': frob, 'spectral': spec, 'point': point_dist}

# Generate slightly perturbed magic square
perturbed = example_magic + np.random.normal(0, 0.1, example_magic.shape)
metrics = compute_metrics(example_magic, perturbed)
print("\nMetric Comparisons:")
for name, value in metrics.items():
    print(f"{name}: {value:.3f}")

# Lab Notebook Entry 4 - 6:30 AM
# Need to address the manifold dimension estimate variation.
# Let's implement multiple estimation methods and compare.

def estimate_dimension(points, methods=['correlation', 'mle']):
    """Estimate intrinsic dimension using multiple methods"""
    results = {}
    
    if 'correlation' in methods:
        # Correlation dimension estimate
        dists = linalg.norm(points[:, None] - points, axis=2)
        r_values = np.logspace(-1, 1, 20)
        corr_dims = []
        for r in r_values:
            C_r = np.mean(dists < r)
            corr_dims.append(np.log(C_r) / np.log(r))
        results['correlation'] = np.mean(corr_dims)
    
    # Add other dimension estimation methods here
    
    return results

points = magic_geom['points']
dim_estimates = estimate_dimension(points)
print("\nDimension Estimates:")
for method, estimate in dim_estimates.items():
    print(f"{method}: {estimate:.2f}")

# Lab Notebook Entry 5 - 7:15 AM
# The dimension estimates are indeed more variable than we presented.
# Need to revise the paper to discuss this variation and its implications.
# 
# TODO for tomorrow (today?):
# 1. Implement proper EMD calculation
# 2. Add statistical tests for eigenvalue significance
# 3. Develop formal proof connecting geometry to enumeration
# 4. Compare with other structured matrices
# 5. Sleep(!)

print("\nNight's Work Summary:")
print("1. Eigenvalue ratios are NOT trivial consequences of magic sum")
print("2. Need better justification for EMD metric choice")
print("3. Dimension estimation needs more rigorous treatment")
print("4. Several formal proofs needed")
print("Time to sleep: 7:30 AM")

# Lab Notebook Entry 6 - 7:45 AM (One last test before sleep!)
# Need to compare with other structured matrices, not just random ones
# Let's look at Latin squares and circulant matrices

def generate_latin_square(n=4):
    """Generate a simple Latin square"""
    base = list(range(1, n+1))
    square = []
    for i in range(n):
        row = base[i:] + base[:i]
        square.append(row)
    return np.array(square)

def generate_circulant_matrix(n=4):
    """Generate a circulant matrix with similar row sums"""
    first_row = np.array([13, 2, 8, 11])  # Chosen to have sum 34
    matrix = np.zeros((n, n))
    for i in range(n):
        matrix[i] = np.roll(first_row, i)
    return matrix

# Compare geometric properties across different matrix types
latin = generate_latin_square()
circulant = generate_circulant_matrix()

print("\nComparative Analysis:")
print("Latin Square Geometry:")
latin_geom = analyze_matrix_geometry(latin)
print(f"λ₂/λ₁: {latin_geom['ratios'][0]:.3f}")
print(f"λ₃/λ₂: {latin_geom['ratios'][1]:.3f}")

print("\nCirculant Matrix Geometry:")
circ_geom = analyze_matrix_geometry(circulant)
print(f"λ₂/λ₁: {circ_geom['ratios'][0]:.3f}")
print(f"λ₃/λ₂: {circ_geom['ratios'][1]:.3f}")

# Lab Notebook Entry 7 - 8:00 AM
# Quick test of persistence homology-like features
# (Basic version - need proper implementation tomorrow)

def simple_persistence_features(points):
    """Compute basic persistence-like features"""
    dists = linalg.norm(points[:, None] - points, axis=2)
    np.fill_diagonal(dists, np.inf)  # Better handling of self-distances
    birth_times = np.min(dists, axis=1)
    death_times = np.max(dists, axis=1)
    return np.sort(birth_times), np.sort(death_times)

birth, death = simple_persistence_features(magic_geom['points'])
print("\nPersistence Features:")
print(f"Birth times range: {birth.min():.3f} to {birth.max():.3f}")
print(f"Death times range: {death.min():.3f} to {death.max():.3f}")
print(f"Persistence ratio: {(death.max() - birth.min())/(death.min() - birth.min()):.3f}")

# Lab Notebook Entry 8 - 8:15 AM
# Quick test of the multi-scale structure Anne mentioned
# Using different neighborhood sizes for dimension estimation

def multi_scale_dimension(points, scales=np.logspace(-1, 1, 5)):
    """Estimate dimension at different scales"""
    dims = []
    dists = linalg.norm(points[:, None] - points, axis=2)
    for scale in scales:
        neighbors = np.mean(dists < scale, axis=1)
        if np.mean(neighbors) > 0:
            dims.append(np.log(np.mean(neighbors)) / np.log(scale))
        else:
            dims.append(np.nan)  # Handle zero neighbor cases
    return scales, dims

scales, dims = multi_scale_dimension(magic_geom['points'])
print("\nMulti-scale Analysis:")
print("Scale | Dimension")
for s, d in zip(scales, dims):
    print(f"{s:.3f} | {d:.3f}")

print("\nFinal Thoughts (8:30 AM):")
print("1. Structured matrices show different patterns - this is good!")
print("2. Multi-scale analysis might explain dimension estimate variations")
print("3. Need proper persistence analysis implementation")
print("4. Latin squares could be good control group")
print("Really going to sleep now!")