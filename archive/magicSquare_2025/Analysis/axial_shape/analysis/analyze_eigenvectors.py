import numpy as np

# Load eigenvectors
try:
    eigenvectors = np.load('figures_all_squares/eigenvectors.npy')
    print(f"Loaded {len(eigenvectors)} eigenvector sets")
except FileNotFoundError:
    print("Error: eigenvectors.npy not found")
    exit(1)

# Reshape to separate the three eigenvectors
n_squares = len(eigenvectors)
eigenvectors = eigenvectors.reshape(n_squares, 3, 3)  # (n_squares, 3 eigenvectors, 3 components)

# Analyze each eigenvector separately
for i in range(3):
    print(f"\nEigenvector {i+1} analysis:")
    evec = eigenvectors[:, i, :]
    mean_vec = np.mean(evec, axis=0)
    std_vec = np.std(evec, axis=0)
    
    print(f"Mean vector: [{mean_vec[0]:.3f}, {mean_vec[1]:.3f}, {mean_vec[2]:.3f}]")
    print(f"Standard deviation: [{std_vec[0]:.3f}, {std_vec[1]:.3f}, {std_vec[2]:.3f}]")
    
    # Check alignment with coordinate axes
    abs_mean = np.abs(mean_vec)
    max_component = np.argmax(abs_mean)
    if abs_mean[max_component] > 0.9:  # Strong alignment threshold
        axis_names = ['X', 'Y', 'Z']
        print(f"Strongly aligned with {axis_names[max_component]} axis")

# Check orthogonality
print("\nOrthogonality check:")
dot_products = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        # Average dot product across all squares
        dots = np.sum(eigenvectors[:, i, :] * eigenvectors[:, j, :], axis=1)
        dot_products[i, j] = np.mean(dots)

print("Average dot products between eigenvectors:")
print(dot_products)

# Check consistency of handedness
print("\nHandedness check:")
for i in range(n_squares):
    cross = np.cross(eigenvectors[i, 0], eigenvectors[i, 1])
    alignment = np.dot(cross, eigenvectors[i, 2])
    if alignment < 0:
        print(f"Square {i} has negative handedness (alignment = {alignment:.3f})")
        break
else:
    print("All squares have consistent handedness") 