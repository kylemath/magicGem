import numpy as np
from axialDay2 import AxialAnalyzer
import os
from tqdm import tqdm

def load_squares():
    """Load squares using a different method than the original script for verification."""
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

def verify_magic_square_properties(square):
    """Verify basic properties of a magic square."""
    n = len(square)
    target_sum = n * (n * n + 1) // 2 // 1  # Magic constant for 4x4 square
    
    # Check rows, columns, and diagonals
    row_sums = np.sum(square, axis=1)
    col_sums = np.sum(square, axis=0)
    diag1_sum = np.trace(square)
    diag2_sum = np.trace(np.fliplr(square))
    
    return {
        'is_magic': (
            np.all(row_sums == target_sum) and
            np.all(col_sums == target_sum) and
            diag1_sum == target_sum and
            diag2_sum == target_sum
        ),
        'row_sums': row_sums,
        'col_sums': col_sums,
        'diag_sums': [diag1_sum, diag2_sum],
        'target_sum': target_sum
    }

def compute_covariance_directly(points):
    """Compute covariance matrix directly without using library functions."""
    mean = np.mean(points, axis=0)
    centered = points - mean
    n = len(points)
    cov = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            cov[i,j] = np.sum(centered[:,i] * centered[:,j]) / (n-1)
    return cov, mean

def verify_eigenvectors(square, verbose=False):
    """Perform multiple independent checks on eigenvector computation."""
    analyzer = AxialAnalyzer(square)
    metrics = analyzer.compute_balance_metrics()
    
    # Get the points directly from the analyzer
    points = analyzer.points
    
    # Check 1: Compute covariance matrix directly
    cov_direct, mean_direct = compute_covariance_directly(points)
    eigenvals_direct, eigenvecs_direct = np.linalg.eigh(cov_direct)
    
    # Check 2: Use numpy's built-in covariance
    cov_numpy = np.cov(points.T)
    eigenvals_numpy, eigenvecs_numpy = np.linalg.eigh(cov_numpy)
    
    # Check 3: Compare with stored metrics
    stored_eigenvecs = metrics['eigenvectors']
    stored_eigenvals = metrics['eigenvalues']
    
    # Normalize and sort all eigenvectors consistently
    def normalize_and_sort(evals, evecs):
        idx = np.argsort(evals)
        evals = evals[idx]
        evecs = evecs[:, idx]
        # Ensure consistent sign (make largest component positive)
        for i in range(evecs.shape[1]):
            max_idx = np.argmax(np.abs(evecs[:, i]))
            if evecs[max_idx, i] < 0:
                evecs[:, i] *= -1
        return evals, evecs
    
    eigenvals_direct, eigenvecs_direct = normalize_and_sort(eigenvals_direct, eigenvecs_direct)
    eigenvals_numpy, eigenvecs_numpy = normalize_and_sort(eigenvals_numpy, eigenvecs_numpy)
    stored_eigenvals, stored_eigenvecs = normalize_and_sort(stored_eigenvals, stored_eigenvecs)
    
    # Compare results
    tol = 1e-10  # Numerical tolerance
    eigenvecs_match = (
        np.allclose(eigenvecs_direct, eigenvecs_numpy, atol=tol) and
        np.allclose(eigenvecs_direct, stored_eigenvecs, atol=tol)
    )
    eigenvals_match = (
        np.allclose(eigenvals_direct, eigenvals_numpy, atol=tol) and
        np.allclose(eigenvals_direct, stored_eigenvals, atol=tol)
    )
    
    if verbose:
        print("\nDirect computation eigenvalues:", eigenvals_direct)
        print("Numpy covariance eigenvalues:", eigenvals_numpy)
        print("Stored eigenvalues:", stored_eigenvals)
        print("\nDirect computation eigenvectors:\n", eigenvecs_direct)
        print("Numpy covariance eigenvectors:\n", eigenvecs_numpy)
        print("Stored eigenvectors:\n", stored_eigenvecs)
    
    return {
        'eigenvecs_match': eigenvecs_match,
        'eigenvals_match': eigenvals_match,
        'direct_eigenvecs': eigenvecs_direct,
        'direct_eigenvals': eigenvals_direct,
        'mean_vector': mean_direct
    }

def main():
    print("Loading squares...")
    squares = load_squares()
    n_squares = len(squares)
    print(f"Loaded {n_squares} squares")
    
    # Verify magic square properties
    print("\nVerifying magic square properties...")
    invalid_squares = []
    for i, square in enumerate(tqdm(squares)):
        props = verify_magic_square_properties(square)
        if not props['is_magic']:
            invalid_squares.append({
                'id': i,
                'properties': props
            })
    
    if invalid_squares:
        print(f"\nWARNING: Found {len(invalid_squares)} invalid magic squares!")
        for inv in invalid_squares[:5]:  # Show first 5
            print(f"\nSquare {inv['id']}:")
            print(f"Row sums: {inv['properties']['row_sums']}")
            print(f"Column sums: {inv['properties']['col_sums']}")
            print(f"Diagonal sums: {inv['properties']['diag_sums']}")
            print(f"Target sum: {inv['properties']['target_sum']}")
    else:
        print("All squares verified as valid magic squares.")
    
    # Verify eigenvector computation
    print("\nVerifying eigenvector computation...")
    mismatches = []
    all_eigenvecs = []
    all_eigenvals = []
    all_means = []
    
    for i, square in enumerate(tqdm(squares)):
        results = verify_eigenvectors(square)
        all_eigenvecs.append(results['direct_eigenvecs'])
        all_eigenvals.append(results['direct_eigenvals'])
        all_means.append(results['mean_vector'])
        
        if not (results['eigenvecs_match'] and results['eigenvals_match']):
            mismatches.append(i)
    
    if mismatches:
        print(f"\nWARNING: Found {len(mismatches)} squares with mismatched eigenvectors/values!")
        print("First few mismatches:", mismatches[:5])
    else:
        print("All eigenvector computations verified as consistent.")
    
    # Analyze variations
    all_eigenvecs = np.array(all_eigenvecs)
    all_eigenvals = np.array(all_eigenvals)
    all_means = np.array(all_means)
    
    print("\nEigenvector Statistics:")
    print("=====================")
    for i in range(3):
        print(f"\nEigenvector {i+1}:")
        evec = all_eigenvecs[:,:,i]
        print(f"Mean: {np.mean(evec, axis=0)}")
        print(f"Std: {np.std(evec, axis=0)}")
        print(f"Min: {np.min(evec, axis=0)}")
        print(f"Max: {np.max(evec, axis=0)}")
    
    print("\nEigenvalue Statistics:")
    print("====================")
    for i in range(3):
        print(f"\nEigenvalue {i+1}:")
        eval_i = all_eigenvals[:,i]
        print(f"Mean: {np.mean(eval_i)}")
        print(f"Std: {np.std(eval_i)}")
        print(f"Min: {np.min(eval_i)}")
        print(f"Max: {np.max(eval_i)}")
    
    print("\nMean Vector Statistics:")
    print("=====================")
    print(f"Mean: {np.mean(all_means, axis=0)}")
    print(f"Std: {np.std(all_means, axis=0)}")
    print(f"Min: {np.min(all_means, axis=0)}")
    print(f"Max: {np.max(all_means, axis=0)}")
    
    # Detailed analysis of first square
    print("\nDetailed analysis of first square:")
    print("================================")
    _ = verify_eigenvectors(squares[0], verbose=True)

if __name__ == '__main__':
    main() 