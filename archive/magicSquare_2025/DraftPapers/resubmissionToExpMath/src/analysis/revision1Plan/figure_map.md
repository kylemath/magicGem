# Figure Mapping for Magic Squares Analysis

## Introduction Section

### Figure I1: Historical Context
- Type: Composite figure
- Content:
  * Example of a Lo Shu 3×3 magic square
  * Dürer's magic square from Melencolia I
  * Timeline of major developments in magic square research
- Purpose: Provide visual context for the historical significance

### Figure I2: Research Framework
- Type: Schematic diagram
- Content: Visual representation of our analysis pipeline
  * Geometric analysis branch
  * EMD analysis branch
  * Manifold learning branch
- Purpose: Orient readers to our methodology

## Geometric Analysis Section

### Figure G1: Point Cloud Representation
- Type: 3D visualization
- Content:
  * 3D scatter plot of magic square as point cloud
  * Color-coded points (vertices, face points, interior points)
  * Multiple viewing angles
- Implementation: Using `plot_single_hull()` in visualization.py

### Figure G2: Geometric Properties Distribution
- Type: Multi-panel statistical plot
- Content:
  * Histogram of hull volumes
  * Histogram of surface areas
  * Scatter plot of volume vs. surface area
  * Box plots of point type distributions
- Implementation: Using `plot_comprehensive_analysis()` in visualization.py

### Figure G3: Eigenvalue Analysis
- Type: Technical plot
- Content:
  * Eigenvalue ratio distributions
  * Principal component visualization
  * Angular uniformity measures
- Implementation: Using `plot_eigenvectors()` in visualization.py

## EMD Analysis Section

### Figure E1: EMD Distance Matrix
- Type: Heatmap
- Content:
  * Pairwise EMD distances between magic squares
  * Hierarchical clustering dendrograms
- Implementation: Using `plot_emd_comparison()` in visualization.py

### Figure E2: EMD Flow Visualization
- Type: Flow diagram
- Content:
  * Visualization of optimal transport between two magic squares
  * Multiple examples showing different transport patterns
- Implementation: Using `plot_emd_flow_between_squares()` in visualization.py

### Figure E3: Multi-scale EMD Analysis
- Type: Multi-panel comparison
- Content:
  * EMD patterns at different scales
  * Scale-dependent features
- Implementation: Using `plot_multiscale_emd()` in visualization.py

## Manifold Analysis Section

### Figure M1: t-SNE Visualization
- Type: Dimensionality reduction plot
- Content:
  * 2D t-SNE embedding of magic squares
  * Color-coded by geometric properties
  * Interactive version for web supplement
- Implementation: Using `plot_tsne_squares()` in visualization.py

### Figure M2: Manifold Structure
- Type: Technical analysis
- Content:
  * Intrinsic dimension estimates
  * Local neighborhood structure
  * Persistence diagrams
- Implementation: Using `plot_manifold_summary()` in visualization.py

## Predictive Modeling Section

### Figure P1: Feature Importance
- Type: Bar plots
- Content:
  * Feature importance for each target variable
  * Comparison across different models
- Implementation: Using new `evaluate_model_performance()` in predictive_modeling.py

### Figure P2: Prediction Performance
- Type: Scatter plots
- Content:
  * Actual vs. predicted values
  * Error distribution analysis
  * Cross-validation results
- Implementation: Using new `plot_prediction_comparison()` in predictive_modeling.py

## Implementation Status

- [x] Basic geometric visualizations (G1, G2)
- [x] EMD analysis plots (E1, E2)
- [x] t-SNE visualization (M1)
- [ ] Historical context figure (I1)
- [ ] Research framework diagram (I2)
- [ ] Complete manifold analysis plots (M2)
- [ ] Predictive modeling plots (P1, P2)
- [ ] Interactive visualizations for web supplement

## Next Steps

1. Implement missing visualizations
2. Standardize plot styles and color schemes
3. Create high-resolution versions for publication
4. Develop interactive versions for web supplement
5. Write detailed figure captions
6. Cross-reference figures in main text 