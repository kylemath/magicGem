"""
Magic Squares Analysis Package

This package contains tools for analyzing magic squares, including:
- Geometric analysis
- Pattern detection
- Visualization tools
- Advanced statistical analysis
"""

from .analyze import (
    run_analysis_pipeline,
    run_geometric_analysis,
    run_manifold_analysis,
    run_emd_analysis,
    run_most_perfect_analysis
)

from .visualization import (
    plot_single_hull,
    plot_multiple_squares,
    plot_comprehensive_analysis,
    plot_tsne_emd,
    plot_geometric_tsne_with_emd,
    analyze_manifold,
    plot_pattern_distribution,
    plot_manifold_summary,
    ensure_plot_dir
)

from .geometry import (
    compute_square_geometry,
    square_to_points,
    classify_points,
    compute_angular_uniformity,
    compute_eigenvalue_ratios,
    analyze_patterns
)

__all__ = [
    'run_analysis_pipeline',
    'run_geometric_analysis',
    'run_manifold_analysis',
    'run_emd_analysis',
    'run_most_perfect_analysis',
    'plot_single_hull',
    'plot_multiple_squares',
    'plot_comprehensive_analysis',
    'plot_tsne_emd',
    'plot_geometric_tsne_with_emd',
    'analyze_manifold',
    'plot_pattern_distribution',
    'plot_manifold_summary',
    'ensure_plot_dir',
    'compute_square_geometry',
    'square_to_points',
    'classify_points',
    'compute_angular_uniformity',
    'compute_eigenvalue_ratios',
    'analyze_patterns'
]
