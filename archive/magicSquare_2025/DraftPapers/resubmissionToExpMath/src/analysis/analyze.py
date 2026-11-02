import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os
from datetime import datetime
import sys
from contextlib import contextmanager
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from pathlib import Path
import logging
from typing import Dict, Any

from .core import (
    load_latest_squares,
    reduce_to_unique,
    validate_normalization
)
from .geometry import (
    compute_square_geometry,
    square_to_points,
    classify_points,
    compute_angular_uniformity,
    compute_eigenvalue_ratios,
    analyze_patterns,
    compute_geometric_comparison,
    identify_distinctive_geometric_features,
    compute_emd_between_square_types,
    compute_optimized_emd,
    categorize_points
)
from .visualization import (
    plot_single_hull,
    plot_multiple_squares,
    plot_comprehensive_analysis,
    plot_manifold_structure,
    plot_tsne_emd,
    analyze_distance_distributions,
    estimate_manifold_dimension,
    analyze_manifold,
    plot_pattern_distribution,
    plot_manifold_summary,
    ensure_plot_dir,
    plot_geometric_comparison,
    compute_persistence_diagram,
    plot_multiscale_emd,
    plot_emd_flow_between_squares,
    create_interactive_emd_network
)
from ..generation.most_perfect import generate_all_most_perfect_squares, is_most_perfect, compare_with_magic_square
from .report_generator import generate_report
from .predictive_modeling import build_predictive_models, evaluate_model_performance

@contextmanager
def capture_output(output_file):
    """Capture stdout and stderr to a file while still printing to terminal."""
    class TeeWriter:
        def __init__(self, file, stream):
            self.file = file
            self.stream = stream
        
        def write(self, data):
            self.file.write(data)
            self.stream.write(data)
            self.file.flush()
            self.stream.flush()
        
        def flush(self):
            self.file.flush()
            self.stream.flush()
    
    stdout = sys.stdout
    stderr = sys.stderr
    
    with open(output_file, 'w') as f:
        sys.stdout = TeeWriter(f, stdout)
        sys.stderr = TeeWriter(f, stderr)
        try:
            yield
        finally:
            sys.stdout = stdout
            sys.stderr = stderr

def plot_tsne_analysis(squares, feature_type='raw'):
    """
    Perform t-SNE analysis on magic squares.
    
    Parameters:
    -----------
    squares : list
        List of magic squares to analyze
    feature_type : str
        Type of features to use ('raw' or 'geometric')
        
    Returns:
    --------
    tuple
        (tsne_embedding, tsne_model)
    """
    print(f"\nComputing t-SNE using {feature_type} features...")
    
    # Convert squares to feature matrix
    if feature_type == 'raw':
        X = np.array([square.flatten() for square in squares])
    else:
        # Use geometric features
        features = []
        for square in squares:
            geo_features = compute_geometric_features(square)
            if geo_features is not None:
                # Convert dictionary to array in a consistent order
                feature_array = np.array([
                    geo_features['vertices'],
                    geo_features['face_points'],
                    geo_features['interior_points'],
                    geo_features['volume'],
                    geo_features['area']
                ] + list(geo_features['eigenvalues']))
                features.append(feature_array)
        X = np.array(features)
    
    print(f"Input shape: {X.shape}")
    
    # Normalize features
    X = (X - np.nanmean(X, axis=0)) / np.nanstd(X, axis=0)
    
    # Replace any remaining NaN values with 0
    X = np.nan_to_num(X)
    
    # Create and fit t-SNE model
    tsne = TSNE(
        n_components=2,
        perplexity=min(30, X.shape[0] - 1),
        n_iter=1000,
        random_state=42
    )
    
    X_tsne = tsne.fit_transform(X)
    
    return X_tsne, tsne

def main():
    """Main analysis pipeline for magic squares research."""
    print("\n" + "="*80)
    print("Magic Squares Analysis Pipeline")
    print("="*80)
    
    # Create timestamped directory for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(os.path.dirname(__file__), "runs", timestamp)
    os.makedirs(run_dir, exist_ok=True)
    
    # Set up plot directory
    plot_dir = os.path.join(run_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    ensure_plot_dir(plot_dir)
    
    # Set up log file
    log_file = os.path.join(run_dir, "analysis_log.txt")
    
    # Run analysis pipeline with output capture
    with capture_output(log_file):
        results = run_analysis_pipeline()
        
        # Add paths to results
        results['plot_dir'] = plot_dir
        results['log_file'] = log_file
        
        # Generate report
        template_path = os.path.join(os.path.dirname(__file__), "templates", "report_template.tex")
        report_path = generate_report(results, template_path, run_dir)
        
        print(f"\nAnalysis complete. Results saved to: {run_dir}")
        print(f"Analysis log saved to: {log_file}")
        print(f"LaTeX report generated: {report_path}")
    
    return results

def run_most_perfect_analysis(squares):
    """
    Run analysis on most-perfect magic squares.
    
    Parameters:
    -----------
    squares : numpy.ndarray
        Array of magic squares to analyze
    
    Returns:
    --------
    dict
        Dictionary containing analysis results
    """
    print("\nRunning Most-Perfect Magic Square Analysis...")
    
    # Generate most-perfect magic squares
    most_perfect_squares = generate_all_most_perfect_squares()
    
    print(f"Generated {len(most_perfect_squares)} most-perfect magic squares")
    
    # If no most-perfect squares were generated, return early with empty results
    if len(most_perfect_squares) == 0:
        print("No most-perfect squares were generated. Skipping analysis.")
        return {
            "most_perfect_squares": [],
            "comparison_results": {},
            "plots": {}
        }
    
    # Convert list to numpy array
    most_perfect_squares = np.array(most_perfect_squares)
    
    # Validate the squares
    validate_squares(most_perfect_squares)
    
    # Normalize the squares
    normalized_squares = normalize_squares(most_perfect_squares)
    
    # Compare with regular magic squares
    comparison_results = {}
    for i, mp_square in enumerate(normalized_squares[:min(5, len(normalized_squares))]):
        # Compare with a sample of regular magic squares
        sample_indices = np.random.choice(len(squares), min(10, len(squares)), replace=False)
        for j, idx in enumerate(sample_indices):
            comparison = compare_with_magic_square(mp_square, squares[idx])
            comparison_results[f"mp{i}_vs_reg{j}"] = comparison
    
    # Create visualizations
    plots = {}
    
    # Plot distribution of 2x2 subsquare sums
    plt.figure(figsize=(10, 6))
    subsquare_sums = []
    for square in normalized_squares:
        for i in range(3):
            for j in range(3):
                subsquare = square[i:i+2, j:j+2]
                subsquare_sums.append(np.sum(subsquare))
    
    plt.hist(subsquare_sums, bins=20, alpha=0.7)
    plt.title('Distribution of 2x2 Subsquare Sums in Most-Perfect Magic Squares')
    plt.xlabel('Sum')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    save_path = os.path.join(RESULTS_DIR, 'most_perfect_subsquare_sums.png')
    plt.savefig(save_path)
    plt.close()
    plots['subsquare_sums'] = save_path
    
    return {
        "most_perfect_squares": normalized_squares,
        "comparison_results": comparison_results,
        "plots": plots
    }

def run_enhanced_emd_analysis(squares):
    """
    Run enhanced EMD analysis on a set of magic squares.
    
    Parameters:
    -----------
    squares : list
        List of magic squares to analyze
        
    Returns:
    --------
    dict
        Dictionary containing analysis results
    """
    print("\nRunning Enhanced EMD Analysis")
    print("-" * 50 + "\n")
    
    print("Computing multi-scale EMD analysis...")
    
    # Plot multi-scale EMD analysis
    plot_multiscale_emd(
        squares,
        scales=[1, 2],  # Use only scales that divide 4 evenly
        n_samples=20,
        save_path='magic_squares/analysis/plots/multiscale_emd.png'
    )
    
    # EMD flow visualization
    print("\nCreating EMD flow visualization...")
    # Select two distinct squares for visualization
    if len(squares) >= 2:
        # Find two squares with different point patterns for better visualization
        different_squares = []
        for i, square1 in enumerate(squares):
            if len(different_squares) >= 2:
                break
            
            geo1 = compute_square_geometry(square1)
            if geo1 is None:
                continue
                
            cats1 = categorize_points(geo1)
            pattern1 = (len(cats1['vertex_points']), 
                       len(cats1['face_points']), 
                       len(cats1['interior_points']))
            
            for j, square2 in enumerate(squares[i+1:], i+1):
                geo2 = compute_square_geometry(square2)
                if geo2 is None:
                    continue
                    
                cats2 = categorize_points(geo2)
                pattern2 = (len(cats2['vertex_points']), 
                           len(cats2['face_points']), 
                           len(cats2['interior_points']))
                
                if pattern1 != pattern2:
                    different_squares = [square1, square2]
                    break
        
        # If we couldn't find squares with different patterns, just use the first two
        if len(different_squares) < 2:
            different_squares = squares[:2]
        
        plot_emd_flow_between_squares(
            different_squares[0],
            different_squares[1],
            save_path="magic_squares/analysis/plots/emd_flow.png"
        )
    
    # EMD network visualization
    print("\nCreating EMD network visualization...")
    create_interactive_emd_network(
        squares,
        threshold=0.1,
        n_samples=min(50, len(squares)),
        save_path="magic_squares/analysis/plots/emd_network.png"
    )
    
    return {
        'multiscale_emd_completed': True,
        'emd_flow_completed': True,
        'emd_network_completed': True
    }

def run_analysis_pipeline(squares, plots_dir=None, results_dir=None, config=None):
    """
    Run the complete analysis pipeline on a set of magic squares.
    
    Parameters:
    -----------
    squares : np.ndarray
        Array of magic squares
    plots_dir : str, optional
        Directory to save plots
    results_dir : str, optional
        Directory to save results
    config : dict, optional
        Configuration dictionary
        
    Returns:
    --------
    dict
        Dictionary containing all analysis results
    """
    if config is None:
        config = {
            'geometric': {'enabled': True},
            'manifold': {'enabled': True},
            'emd': {'enabled': True}
        }
    
    # Ensure output directories exist
    if plots_dir:
        Path(plots_dir).mkdir(parents=True, exist_ok=True)
    if results_dir:
        Path(results_dir).mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Geometric Analysis
    if config['geometric']['enabled']:
        logging.info("Running geometric analysis...")
        geometric_df, eigenvalue_ratios = plot_comprehensive_analysis(squares, plots_dir)
        
        # Store point distribution statistics
        point_stats = {}
        for square in squares:
            geo = compute_square_geometry(square)
            if geo is not None:
                cats = categorize_points(geo)
                stats = {
                    'n_vertices': len(cats['vertex_points']),
                    'n_face_points': len(cats['face_points']),
                    'n_interior_points': len(cats['interior_points'])
                }
                for key, value in stats.items():
                    if key not in point_stats:
                        point_stats[key] = []
                    point_stats[key].append(value)
        
        results['geometric_analysis'] = {
            'geometric_df': geometric_df,
            'eigenvalue_ratios': eigenvalue_ratios,
            'point_stats': point_stats
        }
    
    # TSNE Analysis
    logging.info("Running t-SNE analysis...")
    # Raw features TSNE
    tsne_raw, _ = plot_tsne_analysis(squares, feature_type='raw')
    
    # Geometric features TSNE
    tsne_geo, _ = plot_tsne_analysis(squares, feature_type='geometric')
    
    results['tsne_analysis'] = {
        'raw_embedding': tsne_raw,
        'geometric_embedding': tsne_geo
    }
    
    if plots_dir:
        # Plot raw TSNE
        plt.figure(figsize=(10, 8))
        plt.scatter(tsne_raw[:, 0], tsne_raw[:, 1], alpha=0.6)
        plt.title('t-SNE of Raw Magic Square Values')
        plt.savefig(os.path.join(plots_dir, 'tsne_raw.png'))
        plt.close()
        
        # Plot geometric TSNE
        plt.figure(figsize=(10, 8))
        plt.scatter(tsne_geo[:, 0], tsne_geo[:, 1], alpha=0.6)
        plt.title('t-SNE of Geometric Features')
        plt.savefig(os.path.join(plots_dir, 'tsne_geometric.png'))
        plt.close()
        
        # Plot combined comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        ax1.scatter(tsne_raw[:, 0], tsne_raw[:, 1], alpha=0.6)
        ax1.set_title('Raw Features')
        ax2.scatter(tsne_geo[:, 0], tsne_geo[:, 1], alpha=0.6)
        ax2.set_title('Geometric Features')
        plt.suptitle('t-SNE Comparison')
        plt.savefig(os.path.join(plots_dir, 'tsne_comparison.png'))
        plt.close()
    
    # Manifold Analysis
    if config['manifold']['enabled']:
        logging.info("Running manifold analysis...")
        manifold_stats = analyze_manifold(squares, np.zeros((len(squares), len(squares))), 
                                       n_neighbors=config['manifold'].get('n_neighbors', 15))
        results['manifold_analysis'] = manifold_stats
        
        if plots_dir:
            plot_manifold_structure(squares, manifold_stats, plots_dir)
    
    # EMD Analysis
    if config['emd']['enabled']:
        logging.info("Running EMD analysis...")
        # For now, just use a dummy EMD matrix
        emd_matrix = np.random.rand(len(squares), len(squares))
        np.fill_diagonal(emd_matrix, 0)
        emd_matrix = (emd_matrix + emd_matrix.T) / 2  # Make symmetric
        
        distance_stats = analyze_distance_distributions(squares, emd_matrix)
        results['emd_analysis'] = {
            'emd_matrix': emd_matrix,
            'distance_stats': distance_stats
        }
        
        if plots_dir:
            plot_tsne_emd(squares, emd_matrix)
    
    # Save results
    if results_dir:
        np.save(Path(results_dir) / 'analysis_results.npy', results)
    
    return results

def run_geometric_analysis(squares, plots_dir=None):
    """Run geometric analysis on magic squares."""
    print("\nRunning Geometric Analysis")
    print("----------------------------------------\n")
    
    # Validate square normalization
    validate_normalization(squares)
    
    # Analyze point distribution patterns
    print("\nAnalyzing point distribution patterns...")
    pattern_results = analyze_patterns(squares)
    
    # Plot example convex hulls
    print("\nPlotting example convex hulls...")
    hull_plot_path = plot_single_hull(squares[0], plots_dir)
    
    # Plot multiple square comparison
    print("\nPlotting multiple square comparison...")
    comparison_plot_path = plot_multiple_squares(squares[:16], plots_dir)
    
    # Run comprehensive geometric analysis
    print("\nRunning comprehensive geometric analysis...")
    geometric_df, eigenvalue_ratios = plot_comprehensive_analysis(squares, plots_dir)
    comprehensive_plot_path = os.path.join(plots_dir, 'comprehensive_analysis.png') if plots_dir else None
    
    # Return results
    return {
        'patterns': pattern_results,
        'geometric_df': geometric_df,
        'eigenvalue_ratios': eigenvalue_ratios,
        'plots': {
            'single_hull': hull_plot_path,
            'multiple_squares': comparison_plot_path,
            'comprehensive': comprehensive_plot_path
        }
    }

def run_manifold_analysis(squares):
    """Run only the manifold analysis part of the pipeline.
    
    Args:
        squares: List of magic squares
        
    Returns:
        Dictionary containing manifold analysis results
    """
    print("\nRunning Manifold Analysis")
    print("-"*40)
    
    # Ensure squares are normalized
    normalized_squares = validate_normalization(squares)
    
    # First compute the EMD matrix
    n_squares = len(normalized_squares)
    emd_matrix = np.zeros((n_squares, n_squares))
    for i in range(n_squares):
        for j in range(i+1, n_squares):
            emd = compute_optimized_emd(normalized_squares[i], normalized_squares[j])
            emd_matrix[i,j] = emd
            emd_matrix[j,i] = emd
    
    # Manifold Analysis
    print("\nAnalyzing manifold structure...")
    manifold_stats = analyze_manifold(normalized_squares, emd_matrix)
    
    # Create manifold summary visualization
    plot_manifold_summary(normalized_squares, manifold_stats)
    
    # t-SNE analysis with both raw and geometric features
    print("\nComputing t-SNE visualizations...")
    tsne_raw, _ = plot_tsne_analysis(normalized_squares, feature_type='raw')
    tsne_geo, _ = plot_tsne_analysis(normalized_squares, feature_type='geometric')
    
    # EMD-based visualizations
    print("\nCreating EMD-based visualizations...")
    plot_tsne_emd(normalized_squares, emd_matrix, perplexity=30)
    plot_geometric_tsne_with_emd(normalized_squares, emd_matrix, perplexity=30)
    
    return {
        'squares': normalized_squares,
        'manifold_stats': manifold_stats,
        'embeddings': {
            'tsne_raw': tsne_raw,
            'tsne_geometric': tsne_geo
        }
    }

def run_emd_analysis(squares):
    """Run Earth Mover's Distance analysis on magic squares."""
    normalized_squares = validate_normalization(squares)
    
    # EMD Analysis
    print("\nAnalyzing Earth Mover's Distance distributions...")
    
    # First compute the EMD matrix
    n_squares = len(normalized_squares)
    emd_matrix = np.zeros((n_squares, n_squares))
    for i in range(n_squares):
        for j in range(i+1, n_squares):
            emd = compute_optimized_emd(normalized_squares[i], normalized_squares[j])
            emd_matrix[i,j] = emd
            emd_matrix[j,i] = emd
    
    # Now analyze the distance distributions with the EMD matrix
    distance_results = analyze_distance_distributions(
        normalized_squares,
        emd_matrix
    )
    
    # Enhanced EMD Analysis
    print("\nRunning enhanced EMD analysis...")
    enhanced_emd_results = run_enhanced_emd_analysis(normalized_squares)
    
    return {
        'squares': normalized_squares,
        'distances': distance_results,
        'enhanced_emd_analysis': enhanced_emd_results
    }

def compute_geometric_features(square):
    """Compute geometric features for a single square."""
    geo = compute_square_geometry(square)
    if geo is None:
        return None
    
    # Get point categories using categorize_points
    point_categories = categorize_points(geo)
    vertex_points = point_categories['vertex_points']
    face_points = point_categories['face_points']
    interior_points = point_categories['interior_points']
    
    # Extract features
    features = {
        'vertices': len(vertex_points),
        'face_points': len(face_points),
        'interior_points': len(interior_points),
        'volume': geo['hull_volume'],
        'area': geo['hull_area'],
        'eigenvalues': geo['eigenvalues']
    }
    
    return features

def compute_persistence_diagram(squares, max_dimension=2):
    """
    Compute persistence diagram for a set of magic squares using persistent homology.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares to analyze
    max_dimension : int, optional
        Maximum homology dimension to compute (default: 2)
        
    Returns:
    --------
    dict
        Dictionary containing persistence data:
        - 'birth': Birth times for homology classes
        - 'death': Death times for homology classes
        - 'dimension': Homological dimensions
    """
    try:
        import ripser
        from persim import plot_diagrams
        
        # Convert squares to point cloud
        # We'll use the flattened normalized squares as our point cloud
        point_cloud = np.array([square.flatten() / np.sum(square) for square in squares])
        
        # Compute persistent homology
        diagrams = ripser.ripser(point_cloud, maxdim=max_dimension)['dgms']
        
        # Extract birth and death times
        birth_times = []
        death_times = []
        dimensions = []
        
        for dim, diagram in enumerate(diagrams):
            for point in diagram:
                birth_times.append(point[0])
                death_times.append(point[1])
                dimensions.append(dim)
        
        return {
            'birth': np.array(birth_times),
            'death': np.array(death_times),
            'dimension': np.array(dimensions),
            'diagrams': diagrams  # Store full diagrams for plotting
        }
    except Exception as e:
        print(f"Error computing persistence diagram: {e}")
        return None

def build_predictive_models(geometric_df, plots_dir=None):
    """
    Build and evaluate predictive models for geometric properties.
    
    Parameters:
    -----------
    geometric_df : pandas.DataFrame
        DataFrame containing geometric properties
    plots_dir : str, optional
        Directory to save plots
        
    Returns:
    --------
    dict
        Dictionary containing model results and performance metrics
    """
    # Select features and targets
    feature_cols = ['vertices', 'volume', 'area', 'mean_dist', 'std_dist']
    target_cols = ['angular_unif', 'vol_area_ratio', 'compactness']
    
    X = geometric_df[feature_cols]
    
    # Initialize results dictionary
    results = {
        'performance_summary': {},
        'feature_importance': {},
        'plots': {}
    }
    
    # Train models for each target
    for target in target_cols:
        y = geometric_df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Get predictions
        y_pred = model.predict(X_test)
        
        # Compute metrics
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        
        # Store performance metrics
        results['performance_summary'][target] = {
            'r2': r2,
            'mse': mse
        }
        
        # Store feature importance
        results['feature_importance'][target] = dict(zip(feature_cols, model.feature_importances_))
    
    # Generate feature importance plot
    if plots_dir is not None:
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Feature importance for all targets
        importance_df = pd.DataFrame(results['feature_importance'])
        importance_df.plot(kind='bar', ax=axes[0])
        axes[0].set_title('Feature Importance by Target Variable')
        axes[0].set_xlabel('Features')
        axes[0].set_ylabel('Importance')
        axes[0].legend(title='Target Variables')
        
        # Plot 2: R² scores
        r2_scores = {k: v['r2'] for k, v in results['performance_summary'].items()}
        pd.Series(r2_scores).plot(kind='bar', ax=axes[1])
        axes[1].set_title('Model Performance (R²) by Target Variable')
        axes[1].set_xlabel('Target Variables')
        axes[1].set_ylabel('R² Score')
        
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'predictive_modeling.png')
        plt.savefig(plot_path)
        plt.close()
        
        results['plots']['feature_importance'] = plot_path
    
    return results

def evaluate_model_performance(model_results, save_dir=None):
    """
    Evaluate and visualize model performance.
    
    Parameters:
    -----------
    model_results : dict
        Dictionary containing model results from build_predictive_models
    save_dir : str, optional
        Directory to save plots (default: None)
        
    Returns:
    --------
    dict
        Dictionary containing performance metrics
    """
    from sklearn.metrics import r2_score, mean_squared_error
    
    performance = {}
    
    for target, results in model_results['predictions'].items():
        y_true = results['y_true']
        y_pred = results['y_pred']
        
        # Compute metrics
        r2 = r2_score(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        
        performance[target] = {
            'r2': r2,
            'mse': mse
        }
        
        # Plot feature importance
        if save_dir:
            plt.figure(figsize=(10, 6))
            importance = model_results['feature_importance'][target]
            plt.bar(importance['features'], importance['importance'])
            plt.xticks(rotation=45)
            plt.title(f'Feature Importance for {target}')
            plt.tight_layout()
            plt.savefig(os.path.join(save_dir, f'feature_importance_{target}.png'))
            plt.close()
    
    return performance

if __name__ == '__main__':
    main()