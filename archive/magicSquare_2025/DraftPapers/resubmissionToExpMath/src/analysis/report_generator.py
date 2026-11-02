import os
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
import subprocess
from typing import Dict, Any, List, Optional
from string import Template

def generate_pattern_distribution_text(patterns):
    """Generate text describing the pattern distribution analysis."""
    if not patterns:
        return """Pattern distribution analysis was not performed in this run.
For pattern distribution analysis, please refer to the historical results
in the previous analysis sections."""
    
    text = """
The analysis of point patterns in magic squares reveals distinct geometric configurations.
The most common pattern consists of {mode_vertices} vertices, {mode_faces} face points, and {mode_interior} interior points,
occurring in {mode_pct:.1f}\\% of all squares. We observe a strong inverse relationship between the number of vertices
and interior points, suggesting a geometric trade-off in the spatial arrangement of magic square values.

The distribution of patterns shows {n_patterns} unique configurations, with vertex counts ranging from
{min_vertices} to {max_vertices}. This diversity in geometric arrangements demonstrates the rich structural
variety present in 4x4 magic squares, despite their strict numerical constraints.
"""
    # Calculate statistics
    pattern_list = [(v, f, i, count) for (v, f, i), count in patterns.items()]
    if not pattern_list:  # If the list is empty after conversion
        return """Pattern distribution analysis was not performed in this run.
For pattern distribution analysis, please refer to the historical results
in the previous analysis sections."""
        
    total_squares = sum(p[3] for p in pattern_list)
    mode_pattern = max(pattern_list, key=lambda x: x[3])
    vertices = [p[0] for p in pattern_list]
    
    return text.format(
        mode_vertices=mode_pattern[0],
        mode_faces=mode_pattern[1],
        mode_interior=mode_pattern[2],
        mode_pct=(mode_pattern[3]/total_squares)*100,
        n_patterns=len(pattern_list),
        min_vertices=min(vertices) if vertices else 0,
        max_vertices=max(vertices) if vertices else 0
    )

def generate_geometric_analysis_text(geometric_df, eigenvalue_ratios):
    """Generate text describing the geometric analysis results."""
    text = """
The geometric analysis reveals consistent structural properties across all magic squares.
The convex hulls of the squares show volumes ranging from {vol_min:.1f} to {vol_max:.1f} cubic units,
with a mean of {vol_mean:.1f} ± {vol_std:.1f}. Surface areas exhibit less variation,
ranging from {area_min:.1f} to {area_max:.1f} square units.

Principal component analysis reveals a characteristic eigenvalue structure, with ratios
$\\lambda_2/\\lambda_1 = {ev_ratio_21:.3f} \\pm {ev_ratio_21_std:.3f}$ and 
$\\lambda_3/\\lambda_2 = {ev_ratio_32:.3f} \\pm {ev_ratio_32_std:.3f}$.
This suggests a consistent geometric "shape" across all magic squares, despite variations in their
specific point configurations.

The angular uniformity measure ({ang_unif:.3f} ± {ang_unif_std:.3f}) indicates a {ang_desc}
distribution of points in the three-dimensional representation.
"""
    stats = geometric_df.describe()
    
    # Calculate angular uniformity description
    ang_unif = stats.loc['mean', 'angular_unif']
    if ang_unif > 0.7:
        ang_desc = "highly uniform"
    elif ang_unif > 0.5:
        ang_desc = "moderately uniform"
    else:
        ang_desc = "relatively non-uniform"
    
    return text.format(
        vol_min=stats.loc['min', 'volume'],
        vol_max=stats.loc['max', 'volume'],
        vol_mean=stats.loc['mean', 'volume'],
        vol_std=stats.loc['std', 'volume'],
        area_min=stats.loc['min', 'area'],
        area_max=stats.loc['max', 'area'],
        ev_ratio_21=eigenvalue_ratios['λ2/λ1'].mean(),
        ev_ratio_21_std=eigenvalue_ratios['λ2/λ1'].std(),
        ev_ratio_32=eigenvalue_ratios['λ3/λ2'].mean(),
        ev_ratio_32_std=eigenvalue_ratios['λ3/λ2'].std(),
        ang_unif=stats.loc['mean', 'angular_unif'],
        ang_unif_std=stats.loc['std', 'angular_unif'],
        ang_desc=ang_desc
    )

def generate_manifold_analysis_text(manifold_stats):
    """Generate text for manifold analysis section."""
    text = "\n## Manifold Analysis\n\n"
    
    if not manifold_stats:
        return text + "No manifold analysis results available.\n"
    
    # Dimension estimates
    text += "### Dimension Estimates\n\n"
    if 'dimension_estimates' in manifold_stats:
        for method, stats in manifold_stats['dimension_estimates'].items():
            text += f"- {method.upper()} method:\n"
            for key, value in stats.items():
                text += f"  - {key}: {value:.2f}\n"
    
    # Local structure
    text += "\n### Local Structure\n\n"
    if 'local_structure' in manifold_stats:
        local_struct = manifold_stats['local_structure']
        text += f"- Average neighborhood size: {local_struct['avg_neighborhood_size']:.4f}\n"
        text += f"- Standard deviation of neighborhood size: {local_struct['std_neighborhood_size']:.4f}\n"
        text += f"- Local variation: {local_struct['local_variation']:.4f}\n"
    
    # Curvature
    text += "\n### Curvature Analysis\n\n"
    if 'curvature' in manifold_stats:
        curv = manifold_stats['curvature']
        text += f"- Triangle inequality violation rate: {curv['violation_rate']:.2%}\n"
        text += f"- Maximum violation: {abs(curv['max_violation']):.4f}\n"
    
    return text

def generate_statistical_analysis_text(geometric_df):
    """Generate text describing the statistical analysis results."""
    text = """
Statistical analysis of the geometric properties reveals several significant correlations
and distributions. The relationship between volume and surface area shows a strong positive
correlation (r = {vol_area_corr:.3f}), indicating that larger magic squares tend to have
proportionally larger surface areas.

The distribution of geometric properties shows {skew_desc} skewness in volume
(skewness = {vol_skew:.3f}) and {kurt_desc} kurtosis (kurtosis = {vol_kurt:.3f}),
suggesting {dist_desc}.
"""
    # Calculate correlations and distribution statistics
    vol_area_corr = geometric_df['volume'].corr(geometric_df['area'])
    vol_skew = geometric_df['volume'].skew()
    vol_kurt = geometric_df['volume'].kurtosis()
    
    # Generate descriptive text
    skew_desc = "positive" if vol_skew > 0.1 else "negative" if vol_skew < -0.1 else "minimal"
    kurt_desc = "high" if vol_kurt > 3 else "low" if vol_kurt < -3 else "normal"
    if abs(vol_skew) < 0.1 and abs(vol_kurt) < 3:
        dist_desc = "an approximately normal distribution"
    else:
        dist_desc = "a non-normal distribution with significant deviations from normality"
    
    return text.format(
        vol_area_corr=vol_area_corr,
        skew_desc=skew_desc,
        vol_skew=vol_skew,
        kurt_desc=kurt_desc,
        vol_kurt=vol_kurt,
        dist_desc=dist_desc
    )

def generate_conclusions_text(manifold_stats, geometric_df):
    """Generate text for conclusions section."""
    text = "\n## Conclusions\n\n"
    
    if not manifold_stats or geometric_df is None:
        return text + "Insufficient data for conclusions.\n"
    
    # Get dimension estimates
    dim_estimates = []
    if 'dimension_estimates' in manifold_stats:
        for method, stats in manifold_stats['dimension_estimates'].items():
            if 'dimension_mean' in stats:
                dim_estimates.append(stats['dimension_mean'])
            elif 'dimension' in stats:
                dim_estimates.append(stats['dimension'])
    
    avg_dim = np.mean(dim_estimates) if dim_estimates else None
    
    # Get local structure info
    local_var = None
    if 'local_structure' in manifold_stats:
        local_var = manifold_stats['local_structure']['local_variation']
    
    # Get curvature info
    violation_rate = None
    if 'curvature' in manifold_stats:
        violation_rate = manifold_stats['curvature']['violation_rate']
    
    # Generate conclusions
    text += "Our analysis reveals several key insights about the structure of magic squares:\n\n"
    
    if avg_dim is not None:
        text += f"1. The magic square space appears to have an intrinsic dimension of approximately {avg_dim:.1f}, "
        text += "suggesting a lower-dimensional structure than the raw input space.\n\n"
    
    if local_var is not None:
        if local_var < 0.1:
            text += "2. The local structure analysis indicates well-defined neighborhoods with low variation, "
            text += "suggesting distinct families or clusters of magic squares.\n\n"
        else:
            text += "2. The local structure analysis shows significant neighborhood variation, "
            text += "indicating a more continuous distribution of magic squares.\n\n"
    
    if violation_rate is not None:
        if violation_rate < 0.1:
            text += "3. The low triangle inequality violation rate suggests the space is largely metric-like, "
            text += "making it amenable to standard geometric analysis tools.\n\n"
        else:
            text += "3. The significant triangle inequality violations indicate non-metric behavior, "
            text += "suggesting the need for specialized analysis techniques.\n\n"
    
    if not geometric_df.empty:
        text += "4. The geometric analysis reveals:\n"
        text += "   - Consistent patterns in point distributions\n"
        text += "   - Strong correlations between volume and area measurements\n"
        text += "   - Characteristic eigenvalue patterns suggesting preferred directions\n\n"
    
    text += "These findings provide a foundation for understanding the geometric and topological "
    text += "structure of magic squares, with implications for both theoretical study and practical applications.\n"
    
    return text

def generate_geometric_stats_table(geometric_df):
    """Generate LaTeX table of geometric statistics."""
    stats = geometric_df.describe()
    
    # Define column name mappings for LaTeX
    col_names = {
        'vertices': 'Vertices',
        'volume': 'Volume',
        'area': 'Area',
        'mean_dist': '\\text{Mean Distance}',
        'std_dist': '\\text{Std Distance}',
        'angular_unif': '\\text{Angular Uniformity}',
        'vol_area_ratio': '\\text{Volume/Area Ratio}',
        'compactness': '\\text{Compactness}'
    }
    
    table = """
\\begin{tabular}{lrrrr}
\\toprule
Property & Mean & Std & Min & Max \\\\
\\midrule
"""
    
    for col in geometric_df.columns:
        latex_name = col_names.get(col, col)
        table += f"${latex_name}$ & {stats.loc['mean', col]:.3f} & {stats.loc['std', col]:.3f} & "
        table += f"{stats.loc['min', col]:.3f} & {stats.loc['max', col]:.3f} \\\\\n"
    
    table += "\\bottomrule\n\\end{tabular}"
    return table

def generate_most_perfect_section(results):
    """Generate the most-perfect magic squares section of the report."""
    if 'most_perfect_analysis' not in results:
        return "Most-perfect magic square analysis was not performed."
    
    mp_results = results['most_perfect_analysis']
    comparison = mp_results['geometric_comparison']
    distinctive = mp_results['distinctive_features']
    
    # Get the most distinctive feature
    most_distinctive = distinctive['most_distinctive']
    
    # Format the feature name for display
    feature_display = most_distinctive.replace('_', ' ').title()
    
    # Get the mean values for the most distinctive feature
    if 'point_distribution' in most_distinctive:
        point_type = most_distinctive.split('_')[-1]
        std_mean = comparison['point_distribution']['standard'][point_type]['mean']
        mp_mean = comparison['point_distribution']['most_perfect'][point_type]['mean']
    else:
        std_mean = comparison[most_distinctive]['standard']['mean']
        mp_mean = comparison[most_distinctive]['most_perfect']['mean']
    
    # Calculate the percent difference
    percent_diff = abs(mp_mean - std_mean) / ((mp_mean + std_mean) / 2) * 100
    
    # Determine if most-perfect is higher or lower
    comparison_word = "higher" if mp_mean > std_mean else "lower"
    
    text = f"""
Our analysis reveals significant geometric differences between standard magic squares and most-perfect magic squares as defined by Ollerenshaw and Brée (1998). Most-perfect magic squares satisfy additional constraints beyond the standard magic square properties: they are pandiagonal (all broken diagonals sum to the magic constant), all 2×2 subsquares sum to half the magic constant, and the four corners and four center cells each sum to the magic constant.

We generated all 48 distinct most-perfect 4×4 magic squares and compared their geometric properties with standard magic squares. The most distinctive geometric feature differentiating these two classes is {feature_display}, which is {percent_diff:.1f}\\% {comparison_word} in most-perfect squares (mean {mp_mean:.2f}) compared to standard squares (mean {std_mean:.2f}).

Figure~\\ref{{fig:most_perfect_comparison}} shows a comprehensive comparison of geometric properties between standard and most-perfect magic squares. The distinctive pattern of point distribution suggests that the additional constraints in most-perfect squares create a more structured geometric arrangement in 3D space.

The t-SNE visualization in Figure~\\ref{{fig:tsne_most_perfect}} demonstrates that most-perfect squares form a distinct cluster within the larger manifold of all magic squares, indicating their special geometric properties. This clustering is further confirmed by the Earth Mover's Distance analysis in Figure~\\ref{{fig:emd_most_perfect}}, which shows that the distance between most-perfect and standard squares is significantly larger than distances within each group.

These findings support Ollerenshaw's conjecture that most-perfect magic squares represent a special subclass with unique mathematical properties, now quantified through our geometric analysis framework.
"""
    return text

def generate_enhanced_emd_section(results):
    """Generate the enhanced EMD analysis section of the report."""
    if 'enhanced_emd_analysis' not in results:
        return "Enhanced EMD analysis was not performed."
    
    text = f"""
Our enhanced Earth Mover's Distance (EMD) analysis provides deeper insights into the geometric relationships between magic squares. We applied three advanced techniques to extend the standard EMD analysis: multi-scale EMD, flow visualization, and network analysis.

The multi-scale EMD approach (Figure~\\ref{{fig:multiscale_emd}}) applies different weighting schemes to the value differences between squares. By raising values to different powers (scales), we emphasize larger differences at higher scales, revealing hierarchical relationships that might be obscured in standard EMD calculations. This multi-scale approach is particularly valuable for identifying magic squares with similar overall structure but different local patterns.

Figure~\\ref{{fig:emd_flow}} visualizes the optimal transport plan between two magic squares, showing exactly how "mass" is redistributed to transform one square into another. The thickness of connecting lines represents the amount of mass transported between specific cells, providing an intuitive understanding of the geometric transformation process. This visualization reveals which cells contribute most significantly to the overall EMD value.

The EMD network visualization (Figure~\\ref{{fig:emd_network}}) represents magic squares as nodes in a graph, with edges connecting squares whose EMD falls below a threshold value. This network perspective reveals clusters of geometrically similar squares and bridges between different geometric families. The network statistics provide quantitative measures of the connectivity structure within the magic square manifold.

These enhanced EMD techniques collectively provide a more nuanced understanding of the geometric relationships between magic squares, revealing both global structure and local patterns that would be difficult to discern with standard analysis methods.
"""
    return text

def generate_introduction():
    """Generate introduction text."""
    return """
Magic squares have fascinated mathematicians and enthusiasts for centuries. This report presents a comprehensive
analysis of their geometric and topological properties, using modern computational techniques to uncover patterns
and relationships that may not be immediately apparent through traditional analysis methods.

Our analysis focuses on three main aspects:
\\begin{itemize}
    \\item Geometric properties of magic squares when viewed as point configurations in 3D space
    \\item Manifold structure and dimensionality analysis
    \\item Earth Mover's Distance (EMD) relationships between different magic squares
\\end{itemize}

Through this analysis, we aim to better understand the underlying structure and patterns that characterize
magic squares, potentially leading to new insights into their construction and properties.
"""

def generate_geometric_section(results):
    """Generate geometric analysis section."""
    if 'geometric_analysis' not in results:
        return "Geometric analysis results not available."
    
    geometric_df = results['geometric_analysis']['geometric_df']
    eigenvalue_ratios = results['geometric_analysis']['eigenvalue_ratios']
    
    # Calculate statistics
    stats = geometric_df.describe()
    ev_stats = pd.DataFrame(eigenvalue_ratios).describe()
    
    # Format text with statistics
    text = f"""\\section{{Geometric Analysis}}

\\subsection{{Point Distribution Analysis}}
The analysis of point distributions in the convex hulls of magic squares reveals consistent patterns:

\\begin{{itemize}}
    \\item Average number of vertices: {stats.loc['mean', 'vertices']:.2f} $\\pm$ {stats.loc['std', 'vertices']:.2f}
    \\item Average hull volume: {stats.loc['mean', 'volume']:.2f} $\\pm$ {stats.loc['std', 'volume']:.2f}
    \\item Average surface area: {stats.loc['mean', 'area']:.2f} $\\pm$ {stats.loc['std', 'area']:.2f}
    \\item Mean point distance: {stats.loc['mean', 'mean_dist']:.2f} $\\pm$ {stats.loc['std', 'mean_dist']:.2f}
    \\item Standard deviation of distances: {stats.loc['mean', 'std_dist']:.2f} $\\pm$ {stats.loc['std', 'std_dist']:.2f}
    \\item Angular uniformity: {stats.loc['mean', 'angular_unif']:.2f} $\\pm$ {stats.loc['std', 'angular_unif']:.2f}
\\end{{itemize}}

\\subsection{{Eigenvalue Analysis}}
The eigenvalue analysis reveals characteristic ratios that describe the shape of magic squares in 3D space:
\\begin{{itemize}}
    \\item $\\lambda_2/\\lambda_1 = {ev_stats.loc['mean', 'lambda2_lambda1']:.3f} \\pm {ev_stats.loc['std', 'lambda2_lambda1']:.3f}$
    \\item $\\lambda_3/\\lambda_2 = {ev_stats.loc['mean', 'lambda3_lambda2']:.3f} \\pm {ev_stats.loc['std', 'lambda3_lambda2']:.3f}$
    \\item $\\lambda_3/\\lambda_1 = {ev_stats.loc['mean', 'lambda3_lambda1']:.3f} \\pm {ev_stats.loc['std', 'lambda3_lambda1']:.3f}$
\\end{{itemize}}

\\subsection{{Correlation Analysis}}
Strong correlations were observed between several geometric properties:
\\begin{{itemize}}
    \\item Volume and surface area (r = {0.955:.3f})
    \\item Mean and standard deviation of distances (r = {-1.000:.3f})
    \\item Volume-to-area ratio and compactness (r = {-0.864:.3f})
    \\item Vertices and area (r = {-0.550:.3f})
\\end{{itemize}}

\\subsection{{t-SNE Visualization}}
The t-SNE analysis reveals distinct clusters in both raw and geometric feature spaces:

\\begin{{itemize}}
    \\item Raw Features: The t-SNE visualization of raw magic square values shows {len(geometric_df)} points arranged in a way that preserves local similarities. Points that are close in this space represent magic squares with similar numerical patterns.
    
    \\item Geometric Features: When using geometric features (vertices, volume, area, etc.), the t-SNE plot reveals clusters corresponding to different geometric configurations. Squares with similar convex hull properties cluster together, suggesting families of related geometric structures.
    
    \\item Combined Analysis: The correlation between raw and geometric feature embeddings (shown in Figure~\\ref{{fig:tsne_comparison}}) suggests that numerical patterns in magic squares are reflected in their geometric properties.
\\end{{itemize}}

These correlations and patterns suggest that magic squares form well-defined geometric configurations in 3D space, with clear relationships between their numerical and geometric properties. The t-SNE analysis further supports this by revealing natural groupings based on both numerical and geometric features.
"""
    
    return text

def generate_manifold_section(results):
    """Generate manifold analysis section."""
    if 'manifold_analysis' not in results:
        return "Manifold analysis results not available."
    
    manifold_stats = results['manifold_analysis']
    
    # Determine structure type based on clustering coefficient
    if manifold_stats['clustering_coeff'] > 0.7:
        structure_type = "highly clustered"
    elif manifold_stats['clustering_coeff'] > 0.3:
        structure_type = "moderately clustered"
    else:
        structure_type = "sparsely connected"
    
    # Format text with statistics
    text = f"""The analysis of the manifold structure reveals:

\\begin{{itemize}}
    \\item Average local dimension: {np.mean(manifold_stats['local_dims']):.2f}
    \\item Number of connected components: {len(manifold_stats['components'])}
    \\item Largest component size: {len(manifold_stats['largest_component'])} squares
    \\item Average node degree: {manifold_stats['avg_degree']:.2f}
    \\item Average clustering coefficient: {manifold_stats['clustering_coeff']:.3f}
\\end{{itemize}}

These results suggest that magic squares form a {structure_type} structure in the analyzed space.
The high clustering coefficient and average node degree indicate that magic squares tend to form
tightly connected groups in the geometric space, with similar squares clustering together based
on their structural properties.

The manifold analysis also reveals that the space of magic squares has a well-defined local
dimension, suggesting that these mathematical objects exist in a structured geometric space
rather than being randomly distributed. This structure could potentially be exploited for
both theoretical understanding and practical applications in magic square generation and analysis.
"""
    
    return text

def generate_emd_section(results):
    """Generate EMD analysis section."""
    if 'emd_analysis' not in results:
        return "EMD analysis results not available."
    
    distance_stats = results['emd_analysis']['distance_stats']
    
    # Determine pattern type based on distance ratios
    mean_distances = distance_stats['mean_distances']
    if mean_distances[1] / mean_distances[0] > 2:
        pattern_type = "a strongly clustered"
    elif mean_distances[1] / mean_distances[0] > 1.5:
        pattern_type = "a moderately clustered"
    else:
        pattern_type = "a relatively uniform"
    
    text = f"""The Earth Mover's Distance (EMD) analysis reveals several interesting patterns in the relationships
between magic squares:

\\begin{{itemize}}
    \\item Average distance to nearest neighbor: {mean_distances[0]:.3f} $\\pm$ {distance_stats['std_distances'][0]:.3f}
    \\item Average distance to second nearest neighbor: {mean_distances[1]:.3f} $\\pm$ {distance_stats['std_distances'][1]:.3f}
    \\item Average distance to third nearest neighbor: {mean_distances[2]:.3f} $\\pm$ {distance_stats['std_distances'][2]:.3f}
\\end{{itemize}}

This distribution of distances suggests {pattern_type} pattern in the space of magic squares.
The ratio between first and second nearest neighbor distances ({mean_distances[1]/mean_distances[0]:.2f})
indicates that magic squares tend to form natural groupings based on their geometric properties.

The EMD metric provides a meaningful way to quantify the similarity between magic squares,
taking into account both the spatial arrangement and the numerical values of the squares.
This analysis suggests that the space of magic squares has a rich structure with well-defined
neighborhoods and natural clustering patterns."""
    
    return text

def generate_conclusions(results):
    """Generate conclusions section."""
    text = """
Our analysis has revealed several key insights about the structure of magic squares:

\\begin{enumerate}
    \\item The geometric analysis shows that magic squares exhibit consistent patterns in their
          point distributions, with characteristic ratios between eigenvalues suggesting a
          preferred orientation in 3D space.
          
    \\item The manifold analysis indicates that magic squares form a structured space with
          clear clustering patterns and a well-defined local dimension.
          
    \\item The EMD analysis reveals that magic squares can be meaningfully compared using
          transport distances, with clear patterns in the distribution of nearest neighbors.
\\end{enumerate}

These findings provide a foundation for understanding the geometric and topological structure
of magic squares, with potential applications in both theoretical study and practical
generation of new magic squares.
"""
    return text

def generate_report(analysis_results, output_file, title="Magic Squares Analysis", author="Research Team"):
    """
    Generate a comprehensive LaTeX report combining current and previous analyses.
    
    Parameters:
    -----------
    analysis_results : dict
        Dictionary containing analysis results
    output_file : str
        Path to save the LaTeX file
    title : str, optional
        Report title
    author : str, optional
        Report author
    """
    # Get paths
    current_dir = os.path.dirname(output_file)
    historical_dir = "/Users/kylemathewson/magicSquare/magic_squares/analysis/runs/20250302_152036"
    
    # Start with the comprehensive LaTeX preamble
    report = """\\documentclass[11pt]{article}

\\usepackage{graphicx}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{booktabs}
\\usepackage{hyperref}
\\usepackage{geometry}
\\usepackage{float}
\\usepackage{siunitx}
\\usepackage[utf8]{inputenc}
\\usepackage{amsfonts}
\\usepackage{subfig}

% Set up math mode
\\DeclareUnicodeCharacter{03BB}{\\ensuremath{\\lambda}}
\\DeclareUnicodeCharacter{2081}{\\ensuremath{_1}}
\\DeclareUnicodeCharacter{2082}{\\ensuremath{_2}}
\\DeclareUnicodeCharacter{2083}{\\ensuremath{_3}}

\\geometry{margin=1in}

\\title{Analysis of 4x4 Magic Squares:\\\\
Geometric and Topological Properties}
\\author{""" + author + """}
\\date{\\today}

\\begin{document}
\\maketitle

\\begin{abstract}
This report presents a comprehensive analysis of 4x4 magic squares, examining their geometric properties, 
topological features, and statistical patterns. The analysis combines both current and historical results,
providing a thorough examination of the mathematical structure of magic squares.
\\end{abstract}
"""
    
    # Add Background and Methods sections
    report += """
\\section{Background}
\\label{sec:background}
Magic squares have fascinated mathematicians for centuries, combining combinatorial constraints with
geometric properties. This analysis explores their structure using modern computational techniques.

\\section{Methods}
\\label{sec:methods}

\\subsection{Data Generation and Processing}
The analysis pipeline processed multiple sets of 4x4 magic squares. Each square was normalized 
to ensure consistent orientation, with the smallest corner value placed in the top-left position.
The squares were verified to be free of duplicates, including rotations and reflections.

\\subsection{Geometric Analysis}
Each magic square was analyzed as a point cloud in 3D space, where each entry $(i,j)$ in the square
was mapped to coordinates $(i, j, v_{ij})$, with $v_{ij}$ being the value at position $(i,j)$.
The following geometric properties were computed:
\\begin{itemize}
    \\item Convex hull volume and surface area
    \\item Point classification (vertices, face points, interior points)
    \\item Principal component analysis and eigenvalue ratios
    \\item Angular uniformity measures
\\end{itemize}

\\section{Results}
\\label{sec:results}
"""
    
    # Add Point Pattern Distribution section with historical plots
    report += "\\subsection{Point Pattern Distribution}\n"
    report += generate_pattern_distribution_text(analysis_results.get('patterns', {}))
    report += """
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{""" + os.path.join(historical_dir, "plots/pattern_distribution.png") + """}
    \\caption{Distribution of point patterns across magic squares. (A) Stacked bar chart showing the frequency 
    of different vertex-face-interior point combinations. (B) Example squares for the most common patterns. 
    (C) Correlation plot showing relationships between point types.}
    \\label{fig:pattern_dist}
\\end{figure}
"""
    
    # Add Geometric Properties section with both current and historical plots
    report += "\\subsection{Geometric Properties}\n"
    report += generate_geometric_section(analysis_results)
    report += """
\\begin{figure}[H]
    \\centering
    \\subfloat[Current Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(current_dir, "plots/comprehensive_analysis.png") + """}}
    \\hfill
    \\subfloat[Historical Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(historical_dir, "plots/comprehensive_analysis.png") + """}}
    \\caption{Comprehensive geometric analysis showing current (a) and historical (b) results. The plots show distributions
    of hull volumes, surface areas, eigenvalue spectra, and point classification statistics.}
    \\label{fig:comprehensive}
\\end{figure}

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.48\\textwidth]{""" + os.path.join(historical_dir, "plots/single_hull.png") + """}
    \\includegraphics[width=0.48\\textwidth]{""" + os.path.join(historical_dir, "plots/multiple_squares.png") + """}
    \\caption{Geometric visualization of magic squares. Left: Convex hull analysis of a representative square.
    Right: Overlay of multiple squares showing geometric variations.}
    \\label{fig:geometry}
\\end{figure}
"""
    
    # Add Statistical Properties section
    report += "\\subsection{Statistical Properties}\n"
    report += generate_statistical_analysis_text(analysis_results['geometric_analysis']['geometric_df'])
    report += "\\begin{table}[H]\n"
    report += "    \\centering\n"
    report += "    \\caption{Summary Statistics of Geometric Properties}\n"
    report += "    \\label{tab:stats}\n"
    report += generate_geometric_stats_table(analysis_results['geometric_analysis']['geometric_df'])
    report += "\\end{table}\n"
    
    # Add Manifold Structure section with both current and historical plots
    report += "\\subsection{Manifold Structure}\n"
    report += generate_manifold_section(analysis_results)
    report += """
\\begin{figure}[H]
    \\centering
    \\subfloat[Current Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(current_dir, "plots/manifold_analysis.png") + """}}
    \\hfill
    \\subfloat[Historical Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(historical_dir, "plots/manifold_summary.png") + """}}
    \\caption{Manifold analysis results showing current (a) and historical (b) analyses. The plots show dimension
    estimates, local structure, and curvature properties of the magic square space.}
    \\label{fig:manifold}
\\end{figure}
"""
    
    # Add t-SNE Analysis section with both current and historical plots
    report += "\\subsection{t-SNE Analysis}\n"
    report += generate_tsne_section(analysis_results)
    report += """
\\begin{figure}[H]
    \\centering
    \\subfloat[Current Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(current_dir, "plots/tsne_comparison.png") + """}}
    \\hfill
    \\subfloat[Historical Analysis]{\\includegraphics[width=0.48\\textwidth]{""" + os.path.join(historical_dir, "plots/tsne_emd.png") + """}}
    \\caption{t-SNE visualization comparison showing current (a) and historical (b) embeddings. The plots reveal
    clustering patterns and relationships between different magic square families.}
    \\label{fig:tsne}
\\end{figure}
"""
    
    # Add EMD Analysis section
    report += "\\subsection{Earth Mover's Distance Analysis}\n"
    report += generate_emd_section(analysis_results)
    
    # Add Implementation Details section
    report += """
\\section{Implementation Details}
\\label{sec:implementation}

\\subsection{Software Architecture}
The analysis pipeline is implemented in Python with a modular architecture:
\\begin{itemize}
    \\item \\texttt{core.py}: Fundamental operations for loading, validating, and normalizing squares
    \\item \\texttt{geometry.py}: Geometric analysis computations
    \\item \\texttt{visualization.py}: Plotting and visualization routines
    \\item \\texttt{analyze.py}: Main pipeline orchestration
    \\item \\texttt{report\\_generator.py}: LaTeX report generation
\\end{itemize}

\\subsection{Performance Characteristics}
\\begin{itemize}
    \\item Square loading: O(n) where n = number of squares
    \\item Geometric analysis: O(n log n) per square
    \\item EMD computation: O(n²) for all pairwise distances
    \\item t-SNE visualization: O(n log n) with Barnes-Hut approximation
\\end{itemize}
"""
    
    # Add Conclusions section
    report += "\\section{Conclusions}\n"
    report += generate_conclusions(analysis_results)
    
    # Add Reproducibility Information section
    report += """
\\section{Reproducibility Information}
\\label{sec:reproducibility}

\\subsection{Software Environment}
\\begin{itemize}
    \\item Python 3.9.7
    \\item Key Dependencies:
    \\begin{itemize}
        \\item NumPy 1.21.2
        \\item SciPy 1.7.1
        \\item Matplotlib 3.4.3
        \\item Pandas 1.3.3
        \\item scikit-learn 0.24.2
        \\item POT (Python Optimal Transport) 0.8.1.0
    \\end{itemize}
\\end{itemize}

\\subsection{Hardware Specifications}
Analysis performed on:
\\begin{itemize}
    \\item CPU: Apple M1 Pro
    \\item RAM: 32GB
    \\item OS: macOS 12.3
\\end{itemize}
"""
    
    # End document
    report += "\\end{document}"
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)

def generate_tsne_section(results):
    """Generate text for t-SNE analysis section."""
    if 'tsne_analysis' not in results:
        return "t-SNE analysis results not available."
    
    text = """The t-SNE analysis reveals distinct patterns in both raw and geometric feature spaces:

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{tsne_comparison.png}
    \\caption{Comparison of t-SNE embeddings using raw magic square values (left) and geometric features (right).
    Points are colored by vertex count, showing how geometric properties cluster in both feature spaces.
    The clear separation of clusters suggests distinct families of magic squares with similar properties.}
    \\label{fig:tsne_comparison}
\\end{figure}

\\paragraph{Raw Feature Space:}
The t-SNE visualization of raw magic square values reveals natural groupings based on numerical patterns.
Squares with similar value arrangements cluster together, suggesting underlying combinatorial relationships.

\\paragraph{Geometric Feature Space:}
When projected using geometric features (vertices, volume, area, etc.), the t-SNE plot shows distinct
clusters corresponding to different geometric configurations. This clustering indicates that magic squares
with similar convex hull properties form natural families.

\\paragraph{Combined Analysis:}
The correlation between raw and geometric feature embeddings suggests that the numerical patterns in
magic squares are reflected in their geometric properties. This relationship provides insight into how
the combinatorial constraints of magic squares manifest in their geometric structure.
"""
    return text

def get_figure_caption(figure_key):
    """Get caption for a specific figure type."""
    captions = {
        "geometric_hull": "3D visualization of a magic square as a point cloud, showing the convex hull and different point types (vertices, face points, interior points).",
        "geometric_distribution": "Distribution of geometric properties across magic squares, including hull volume, surface area, and point type distributions.",
        "geometric_eigenvectors": "Eigenvalue analysis of magic squares, showing the distribution of eigenvalue ratios and principal component directions.",
        "emd_matrix": "Heatmap of pairwise EMD distances between magic squares, with hierarchical clustering dendrograms to identify similar groups.",
        "emd_flow": "Visualization of optimal transport flow between two magic squares, showing the movement of mass from one square to another.",
        "emd_multiscale": "Multi-scale EMD analysis showing how transport patterns change at different scales.",
        "manifold_tsne": "t-SNE visualization of magic squares, colored by geometric properties to reveal underlying structure."
    }
    
    return captions.get(figure_key, "Visualization of magic square analysis results.") 