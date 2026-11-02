# Magic Square Manifold Analysis

This directory contains visualizations of the magic square manifold, based on the covariance constraint analysis.

## Overview

These visualizations demonstrate that magic squares can be understood as points on a well-defined manifold in the space of all possible numerical arrangements. The manifold is characterized by four covariance constraints:

1. Cov(x,z) = 0 (row sum constraint)
2. Cov(y,z) = 0 (column sum constraint)
3. Cov((x+y)/√2,z) = 0 (main diagonal constraint)
4. Cov((x-y)/√2,z) = 0 (anti-diagonal constraint)

## Figures

### 1. Constraint Space Visualization (constraint_space_3d.png)

This 3D visualization places each arrangement in a space where:

- X-axis represents row sum covariance (Cov(x,z))
- Y-axis represents column sum covariance (Cov(y,z))
- Z-axis represents main diagonal covariance (Cov(main_diag,z))

Magic squares (blue) form a tight cluster at the origin (0,0,0), while non-magic arrangements (colored by perturbation level) spread outward.

### 2. Distance to Manifold Distribution (distance_distribution.png)

This histogram shows the distribution of distances to the magic square manifold:

- Magic squares (blue) have distances very close to zero
- Non-magic arrangements (red) have a broader distribution with larger distances

The distance is calculated as the Euclidean norm of the four covariance values:

```python
d(S, M) = √(Cov(x,z)² + Cov(y,z)² + Cov(main_diag,z)² + Cov(anti_diag,z)²)
```

### 3. Perturbation vs. Distance (perturbation_vs_distance.png)

This visualization shows how the distance from the manifold increases with perturbation level:

- Level 0 (magic squares) have near-zero distance
- Each subsequent level of perturbation (random swaps) increases the average distance
- Error bars show the standard deviation within each level

### 4. t-SNE Visualization (tsne_visualization.png)

This 2D mapping of the high-dimensional space uses t-SNE dimensionality reduction to visualize:

- Magic squares (blue) as a distinct, tight cluster
- Non-magic arrangements spread out by perturbation level
- The topology of the magic square manifold

### 5. Constraint Violation Analysis (constraint_violation.png)

This bar chart breaks down which constraints are violated by different types of arrangements:

- Magic squares (blue) show near-zero violation across all constraints
- As perturbation level increases, constraint violations grow systematically
- Different constraints show different sensitivity to perturbations

## Implications

These visualizations confirm that:

1. Magic squares form a well-defined geometric manifold in the space of all possible arrangements
2. The distance to this manifold provides a continuous measure of how "magical" any arrangement is
3. Different types of perturbations violate different constraints in predictable ways
4. The manifold has a specific dimensionality and topology that can be explored with dimensionality reduction techniques

## Code Details

These visualizations were generated using:

- `visualize_magic_manifold.py` - Main script for generating all visualizations
- Distances calculated with `compute_distance_to_manifold()` function
- Perturbation levels 1-5 created by random swaps of elements
- t-SNE parameters: perplexity=30, random_state=42
- Random seed 42 for reproducibility

## References

For more information, see:

- `magic_square_theorem.md` - Formal mathematical proof of the manifold properties
- `analysisSummaryAxial.md` - Integration with other axial analysis approaches
- `mathematical_proof.md` - Detailed derivation of constraint properties
