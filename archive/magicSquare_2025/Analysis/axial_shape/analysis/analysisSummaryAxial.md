# Axial Analysis of Magic Squares

## Overview

This document summarizes the axial analysis approach used to study magic squares through their geometric representation in 3D space and subsequent spherical harmonic analysis. The analysis includes a special focus on geometric classification of magic squares based on their vertex, face point, and interior point counts.

## 1. Axial Representation

### Basic Transformation

The magic square is transformed into a set of points in 3D space using the following mapping:

- For each cell (i,j) with value v in the magic square:
  - x = i - (n-1)/2 (centered row index)
  - y = j - (n-1)/2 (centered column index)
  - z = v - mean(square) (centered value)

This creates a centered point cloud where:

- The x-y plane represents the grid structure of the square
- The z-axis represents the values in the square
- The origin (0,0,0) represents the center of the square with mean value

### Geometric Classification

Magic squares can be classified based on their geometric properties in 3D space:

1. **Vertices**: Points at the extremes of the convex hull
2. **Face Points**: Points on the faces of the convex hull
3. **Interior Points**: Points inside the convex hull

Common configurations include:

- 8v_4f_4i: 8 vertices, 4 face points, 4 interior points (most balanced)
- 16v_0f_0i: 16 vertices, 0 face points, 0 interior points (most extreme)

## 2. Spherical Harmonic Analysis

### Process

1. **Point Cloud to Spherical Coordinates**

   - Convert (x,y,z) points to spherical coordinates (r,θ,φ)
   - r = radial distance from origin
   - θ = azimuthal angle in x-y plane
   - φ = polar angle from z-axis

2. **Harmonic Decomposition**

   - Compute spherical harmonic coefficients up to order 6 (l_max = 6)
   - For each degree l and order m:
     - Compute Y_l^m(θ,φ) (spherical harmonic functions)
     - Calculate coefficients as sum of Y_l^m over all points
   - Filter significant coefficients (> 5% of maximum coefficient)

3. **Surface Reconstruction**
   - Create a continuous surface by combining significant harmonics
   - r(θ,φ) = Σ c_l^m |Y_l^m(θ,φ)|
   - Scale reconstruction to match original point cloud scale
   - Convert back to Cartesian coordinates for visualization

## 3. Visualization (axialOnionGif.py)

### Features

- **Continuous Surface**: Shows a smooth interpolation between discrete points
- **Original Points**: Displayed as red dots for reference
- **Color Mapping**: Uses viridis colormap to show radial distance
- **Transparency**: Surface alpha=0.6 to show internal structure
- **Rotation**: Animates the shape rotating around z-axis for 3D understanding
- **Resolution**: Uses 100x100 grid for smooth surface rendering
- **Auto-scaling**: Adjusts view limits based on data range

### Technical Details

- Surface opacity: 0.6 for better visibility of original points
- Grid lines: Added for better spatial reference
- View limits: Auto-adjusted based on data range
- Elevation angle: Fixed at 20° for optimal viewing
- Legend: Shows original points and surface mapping

## 4. Mathematical Significance

### Properties Captured

1. **Geometric Structure**

   - Global symmetries of the magic square
   - Spatial relationships between values
   - Distribution of values in 3D space
   - Vertex/face/interior point classification

2. **Harmonic Content**

   - Dominant modes indicate major patterns
   - Higher-order harmonics (up to l=6) capture fine details
   - Coefficient magnitudes reveal symmetry strength
   - Zero coefficients indicate specific symmetries

3. **Topological Features**
   - Surface connectivity represents value relationships
   - Bulges and depressions show value clusters
   - Overall shape reflects geometric classification

## 5. Implementation Details

### Key Functions

1. `square_to_axial(square)`:

   - Input: n×n magic square
   - Output: Array of 3D points and vectors
   - Centers and scales the representation

2. `compute_spherical_harmonics(points, lmax=6)`:

   - Input: 3D points, maximum degree
   - Output: Dictionary of harmonic coefficients
   - Computes spherical harmonic decomposition

3. `create_harmonic_reconstruction(points, max_l=6)`:
   - Input: 3D points, maximum degree
   - Output: Surface coordinates (x,y,z) and radial values
   - Creates continuous surface representation
   - Scales output to match input point cloud

## 6. Visualization Parameters

### Display Settings

- Figure size: 10×10 inches
- DPI: 300 for high resolution
- Grid stride: 2 for balance of detail and performance
- Edge colors: White for surface grid lines
- Background grid: Alpha 0.3 for subtle reference
- Point size: 50 for original points
- Surface transparency: 0.6

## 7. Analysis Results

### Geometric Classifications

1. **Balanced Configuration (8v_4f_4i)**

```python
[[1, 6, 11, 16],
 [14, 12, 5, 3],
 [15, 9, 8, 2],
 [4, 7, 10, 13]]
```

- Even distribution of points
- Dominant l0m0 (spherical) term
- Significant l2m2 and l3m3 components

2. **Extreme Configuration (16v_0f_0i)**

```python
[[1, 4, 13, 16],
 [8, 15, 2, 9],
 [14, 5, 12, 3],
 [11, 10, 7, 6]]
```

- All points are vertices
- More complex harmonic content
- Larger range of radial values

## 8. Usage

### Basic Analysis

```python
from axialSquareStorm import square_to_axial, compute_spherical_harmonics

# Convert square to points
points, vectors = square_to_axial(square)

# Create visualization with debug info
create_visualization(square_key="8v_4f_4i")  # or any other geometric class
```

### Animation Generation

```python
# Create rotating animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)
ani.save(f'figures/axial_harmonic_rotation_{square_key}.gif', writer='pillow', fps=30)
```

## 9. The Magic Square Manifold

### Covariance Constraint Analysis

Building on the axial representation, we've discovered that magic squares can be characterized through their covariance properties in the following way:

1. **Four Key Constraints**: A 4×4 arrangement is a magic square if and only if:

   - Cov(x,z) = 0 (row sum constraint)
   - Cov(y,z) = 0 (column sum constraint)
   - Cov((x+y)/√2,z) = 0 (main diagonal constraint)
   - Cov((x-y)/√2,z) = 0 (anti-diagonal constraint)

2. **Manifold Interpretation**: These four constraints define a manifold within the space of all possible 4×4 numerical arrangements.

   <Figure constraint_space_3d.png>

   The visualization shows magic squares (blue) clustered at the origin (0,0,0) in constraint space, with non-magic arrangements (colored by perturbation level) spreading outward.

3. **Distance Metric**: The Euclidean distance in constraint space provides a measure of how "magical" any arrangement is:

   ```python
   def compute_distance_to_manifold(square):
       covs = compute_covariance_constraints(square)
       return np.linalg.norm(covs)
   ```

   <Figure distance_distribution.png>

   The histogram shows a clear separation between magic squares (blue) and non-magic arrangements (red) based on their distance to the manifold.

### Relationship to Geometric Classification

The manifold perspective complements our geometric classification approach:

1. **Unified Framework**: While geometric classification (8v_4f_4i, 16v_0f_0i, etc.) describes the shape characteristics of magic squares, the manifold perspective explains why all magic squares, regardless of their geometric class, share fundamental statistical properties.

2. **Constraint Preservation**: Different geometric classes of magic squares occupy different regions of the manifold, but all satisfy the four covariance constraints exactly.

3. **Perturbation Effects**: When perturbing a magic square, its distance from the manifold increases systematically:

   <Figure perturbation_vs_distance.png>

   This figure shows how each level of perturbation (number of random swaps) increases the average distance to the magic square manifold.

### Manifold Structure Analysis

Advanced techniques allow us to explore the structure of the magic square manifold:

1. **t-SNE Visualization**: Using t-SNE dimensionality reduction, we can visualize the high-dimensional structure of the manifold in 2D:

   <Figure tsne_visualization.png>

   Magic squares (blue) form a distinct cluster, while non-magic arrangements spread outward with increasing perturbation levels.

2. **Constraint Violation Patterns**: Different types of perturbations violate different constraints:

   <Figure constraint_violation.png>

   The figure shows how different perturbation levels affect each of the four constraints.

## 10. Integration of Approaches

### Combining Axial, Harmonic, and Manifold Analyses

The three approaches provide complementary insights into magic squares:

1. **Axial Representation**: Provides the foundation by mapping magic squares to 3D points.
2. **Spherical Harmonic Analysis**: Captures the detailed shape structure and symmetries.
3. **Manifold Analysis**: Reveals the underlying geometric constraints that define magic squares.

### Implementation for Combined Analysis

```python
# Combined analysis workflow
def comprehensive_magic_analysis(square):
    # 1. Axial representation
    points, vectors = square_to_axial(square)

    # 2. Geometric classification
    vertices, face_points, interior_points = classify_geometry(points)

    # 3. Harmonic analysis
    harmonics = compute_spherical_harmonics(points)

    # 4. Manifold analysis
    constraints = compute_covariance_constraints(square)
    distance = compute_distance_to_manifold(square)

    return {
        'geometric_class': f"{len(vertices)}v_{len(face_points)}f_{len(interior_points)}i",
        'harmonic_coefficients': harmonics,
        'covariance_constraints': constraints,
        'manifold_distance': distance
    }
```

## 11. Future Extensions

1. Higher-order harmonic analysis (beyond l=6)
2. Comparative analysis between geometric classes
3. Automated geometric classification
4. Integration with other magic square properties
5. Machine learning for pattern recognition
6. Statistical analysis of harmonic coefficients
7. Investigation of symmetry relationships
8. Analysis of the manifold structure of higher-order magic squares
9. Development of perturbation measures that preserve specific constraints
10. Exploration of the relationship between manifold distance and human perception of "magicalness"

## References

- Spherical harmonics: `scipy.special.sph_harm_y`
- Animation: `matplotlib.animation.FuncAnimation`
- 3D plotting: `mpl_toolkits.mplot3d`
- Geometric classification: Convex hull analysis
- Dimensionality reduction: `sklearn.manifold.TSNE`
- Covariance analysis: "The Axial Covariance Theorem for Magic Squares"
