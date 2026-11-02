import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# A 4x4 magic square for demonstration
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
    
    # Same transformation as in AxialAnalyzer
    for i in range(n):
        for j in range(n):
            point = np.array([
                i - (n-1)/2,  # x-coordinate (row-based)
                j - (n-1)/2,  # y-coordinate (column-based)
                square[i, j] - np.mean(square)  # z-coordinate (value-based)
            ])
            points.append(point)
    
    return np.array(points)

def prove_covariance_structure(points):
    """Demonstrate why the covariance matrix has a diagonal structure."""
    
    # 1. Compute the full covariance matrix
    cov_matrix = np.cov(points.T)
    print("Full covariance matrix:")
    print(cov_matrix)
    print()
    
    # 2. Analyze the off-diagonal terms
    print("Off-diagonal terms (should be close to zero):")
    print(f"Cov(x, y) = {cov_matrix[0, 1]}")
    print(f"Cov(x, z) = {cov_matrix[0, 2]}")
    print(f"Cov(y, z) = {cov_matrix[1, 2]}")
    print()
    
    # 3. Compute eigendecomposition
    eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
    print("Eigenvalues:")
    print(eigenvals)
    print("\nEigenvectors (should be aligned with coordinate axes):")
    print(eigenvecs)
    print()
    
    # 4. Demonstrate why Cov(x, z) is zero
    n = int(np.sqrt(len(points)))
    x_coords = points[:, 0]
    z_coords = points[:, 2]
    
    print("Demonstrating why Cov(x, z) = 0:")
    for i in range(n):
        # Get z values for each row i
        row_indices = range(i*n, (i+1)*n)
        row_x = x_coords[row_indices]
        row_z = z_coords[row_indices]
        print(f"Row {i}:")
        print(f"  x value: {row_x[0]}")  # same value for entire row
        print(f"  z values: {row_z}")
        print(f"  Sum of z values: {np.sum(row_z)}")  # Should be close to 0
    
    return cov_matrix, eigenvals, eigenvecs

def visualize_points_and_eigenvectors(points, eigenvectors, eigenvalues):
    """Visualize the points in 3D along with eigenvectors."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
               c=magic_square.flatten(), cmap='viridis', s=100, alpha=0.8)
    
    # Plot the eigenvectors from the origin
    origin = np.zeros(3)
    colors = ['r', 'g', 'b']
    
    for i in range(3):
        # Scale by square root of eigenvalue for visualization
        vec = eigenvectors[:, i] * np.sqrt(eigenvalues[i])
        ax.quiver(origin[0], origin[1], origin[2], 
                  vec[0], vec[1], vec[2], 
                  color=colors[i], label=f"Eigenvector {i+1}", 
                  arrow_length_ratio=0.1, linewidth=2)
    
    # Add coordinate axes for reference
    ax_length = max(np.ptp(points[:, 0]), np.ptp(points[:, 1]), np.ptp(points[:, 2])) / 2
    ax.quiver(origin[0], origin[1], origin[2], ax_length, 0, 0, color='k', alpha=0.3, arrow_length_ratio=0.1)
    ax.quiver(origin[0], origin[1], origin[2], 0, ax_length, 0, color='k', alpha=0.3, arrow_length_ratio=0.1)
    ax.quiver(origin[0], origin[1], origin[2], 0, 0, ax_length, color='k', alpha=0.3, arrow_length_ratio=0.1)
    
    ax.set_xlabel('X (row index)')
    ax.set_ylabel('Y (column index)')
    ax.set_zlabel('Z (square value)')
    ax.set_title('Magic Square Axial Representation with Eigenvectors')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('figures_day2/direct_proof.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    # Create output directory if it doesn't exist
    import os
    os.makedirs('figures_day2', exist_ok=True)
    
    # Create points from magic square
    points = create_axial_points(magic_square)
    
    # Print the magic square
    print("Original Magic Square:")
    print(magic_square)
    print("\nMagic constant:", np.sum(magic_square[0, :]))
    print()
    
    # Prove the covariance structure
    cov_matrix, eigenvals, eigenvecs = prove_covariance_structure(points)
    
    # Visualize the points and eigenvectors
    visualize_points_and_eigenvectors(points, eigenvecs, eigenvals)
    
    print("\nConclusion:")
    print("The eigenvectors of the covariance matrix are aligned with the coordinate axes")
    print("because the covariance matrix is diagonal due to the structure of the axial representation.")

if __name__ == "__main__":
    main() 