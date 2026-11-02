import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sklearn.manifold import TSNE
import seaborn as sns
import ot  # Make sure POT is installed: pip install POT
from scipy import stats
import os
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.stats import linregress
from datetime import datetime
import networkx as nx
from ripser import ripser
from persim import plot_diagrams
from typing import Dict, Any, List, Tuple, Optional
from scipy.spatial import ConvexHull
import pandas as pd

from .geometry import (
    compute_square_geometry,
    square_to_points,
    classify_points,
    compute_angular_uniformity,
    compute_eigenvalue_ratios,
    compute_geometric_comparison,
    identify_distinctive_geometric_features,
    compute_multiscale_emd,
    compute_emd_matrix,
    _compute_cost_matrix,
    categorize_points,
    compute_optimized_emd,
    analyze_patterns,
)

# Module-level variable to store the plot directory
_PLOT_DIR = None

def ensure_plot_dir(plot_dir=None):
    """Ensure the plots directory exists with timestamp. Creates only one directory per run."""
    global _PLOT_DIR
    
    if plot_dir is not None:
        _PLOT_DIR = plot_dir
    elif _PLOT_DIR is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _PLOT_DIR = os.path.join(os.path.dirname(__file__), "plots", timestamp)
        os.makedirs(_PLOT_DIR, exist_ok=True)
    
    return _PLOT_DIR

def plot_single_hull(square, title="Single Magic Square Hull"):
    """Plot a single magic square's points and convex hull"""
    # Set non-interactive backend
    plt.switch_backend('Agg')
    
    # Compute geometry
    geo = compute_square_geometry(square)
    if geo is None:
        print("Failed to compute hull")
        return
        
    # Create 3D plot
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    
    # Get categorized points
    point_categories = categorize_points(geo)
    vertex_points = point_categories['vertex_points']
    face_points = point_categories['face_points']
    interior_points = point_categories['interior_points']
    
    # Plot points with different colors
    if len(vertex_points) > 0:
        ax.scatter(vertex_points[:, 0], vertex_points[:, 1], vertex_points[:, 2], 
                  c='red', s=150, label=f'Hull Vertices ({len(vertex_points)})', zorder=4)
    if len(face_points) > 0:
        ax.scatter(face_points[:, 0], face_points[:, 1], face_points[:, 2], 
                  c='orange', s=100, label=f'Face Points ({len(face_points)})', zorder=3)
    if len(interior_points) > 0:
        ax.scatter(interior_points[:, 0], interior_points[:, 1], interior_points[:, 2], 
                  c='blue', s=80, label=f'Interior Points ({len(interior_points)})', zorder=2)
    
    # Plot hull faces
    faces = geo['hull_faces']
    poly3d = [[face[0], face[1], face[2]] for face in faces]
    collection = Poly3DCollection(poly3d, 
                                alpha=0.15,
                                linewidth=2,
                                edgecolor='black',
                                zorder=1)
    
    light_blue = colors.to_rgba('lightblue', alpha=0.15)
    collection.set_facecolor([light_blue])
    collection.set_zsort('average')
    ax.add_collection3d(collection)
    
    # Labels and formatting
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Value')
    ax.set_title(title)
    ax.set_box_aspect([1,1,1])
    ax.view_init(elev=20, azim=45)
    ax.legend()
    
    # Print statistics
    print("\nPoint Distribution:")
    print(f"Total points: {len(geo['points'])}")
    print(f"Hull vertices: {len(vertex_points)} ({len(vertex_points)/len(geo['points'])*100:.1f}%)")
    print(f"Points on faces: {len(face_points)} ({len(face_points)/len(geo['points'])*100:.1f}%)")
    print(f"Interior points: {len(interior_points)} ({len(interior_points)/len(geo['points'])*100:.1f}%)")
    print("\nMagic Square:")
    print(square)
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'single_hull.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")

def plot_multiple_squares(squares, grid_size=None):
    """Plot all squares in a grid with minimal decoration"""
    # Set non-interactive backend
    plt.switch_backend('Agg')
    
    # Calculate appropriate grid size if not specified
    n_squares = len(squares)
    if grid_size is None:
        grid_size = int(np.ceil(np.sqrt(n_squares)))
    
    # Verify we have enough squares
    total_slots = grid_size * grid_size
    if total_slots < n_squares:
        print(f"Warning: Grid size {grid_size}x{grid_size}={total_slots} is too small for {n_squares} squares")
        grid_size = int(np.ceil(np.sqrt(n_squares)))
        total_slots = grid_size * grid_size
        print(f"Adjusted to {grid_size}x{grid_size}={total_slots}")
    
    fig = plt.figure(figsize=(25, 25))
    
    # Compute geometries and categorize points first
    geometries = []
    point_categories = []
    
    print(f"\nProcessing {n_squares} squares...")
    for i in range(n_squares):
        if i % 50 == 0:
            print(f"Processing square {i+1}...")
        geo = compute_square_geometry(squares[i])
        if geo is not None:
            cats = categorize_points(geo)
            geometries.append(geo)
            point_categories.append((
                cats['vertex_points'],
                cats['face_points'],
                cats['interior_points']
            ))
    
    # Plot each square
    for i in range(len(geometries)):
        ax = fig.add_subplot(grid_size, grid_size, i+1, projection='3d', computed_zorder=False)
        
        # Get categorized points
        vertex_points, face_points, interior_points = point_categories[i]
        geo = geometries[i]
        
        # Plot points with minimal size
        if len(vertex_points) > 0:
            ax.scatter(vertex_points[:, 0], vertex_points[:, 1], vertex_points[:, 2], 
                      c='red', s=1, zorder=4)
        if len(face_points) > 0:
            ax.scatter(face_points[:, 0], face_points[:, 1], face_points[:, 2], 
                      c='orange', s=1, zorder=3)
        if len(interior_points) > 0:
            ax.scatter(interior_points[:, 0], interior_points[:, 1], interior_points[:, 2], 
                      c='blue', s=1, zorder=2)
        
        # Plot hull faces with minimal opacity
        faces = geo['hull_faces']
        poly3d = [[face[0], face[1], face[2]] for face in faces]
        collection = Poly3DCollection(poly3d, 
                                    alpha=0.1,  # Reduced opacity
                                    linewidth=0.5,  # Thinner lines
                                    edgecolor='black',
                                    zorder=1)
        
        light_blue = colors.to_rgba('lightblue', alpha=0.1)  # Reduced opacity
        collection.set_facecolor([light_blue])
        collection.set_zsort('average')
        ax.add_collection3d(collection)
        
        # Minimal labels and formatting
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Set view angle
        ax.view_init(elev=20, azim=45)
        ax.set_box_aspect([1,1,1])
    
    plt.suptitle(f'Magic Square Convex Hulls (All {n_squares} Squares)', 
                 fontsize=16, y=0.95)
    plt.tight_layout()
    
    # Print summary statistics at the end
    vertex_counts = [len(cats[0]) for cats in point_categories]
    face_counts = [len(cats[1]) for cats in point_categories]
    interior_counts = [len(cats[2]) for cats in point_categories]
    
    print("\nSummary Statistics:")
    print(f"Vertices: {np.mean(vertex_counts):.1f} ± {np.std(vertex_counts):.1f}")
    print(f"Face points: {np.mean(face_counts):.1f} ± {np.std(face_counts):.1f}")
    print(f"Interior points: {np.mean(interior_counts):.1f} ± {np.std(interior_counts):.1f}")
    
    # Count distribution patterns
    patterns = {}
    for v, f, i in zip(vertex_counts, face_counts, interior_counts):
        key = (v, f, i)
        patterns[key] = patterns.get(key, 0) + 1
    
    print("\nDistribution Patterns:")
    print("Vertices | Face Points | Interior | Count")
    print("-" * 45)
    for (v, f, i), count in sorted(patterns.items()):
        print(f"{v:8d} | {f:11d} | {i:8d} | {count:5d}")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'multiple_squares.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")

def plot_tsne_squares(squares, use_geometry=True, perplexity=30, n_iter=1000):
    """Plot t-SNE visualization of the magic squares"""
    
    print("\nComputing geometric properties...")
    # First compute all geometric properties
    geometries = []
    features = []
    for i, square in enumerate(squares):
        if i % 100 == 0:
            print(f"Processing square {i+1}/{len(squares)}...")
        
        geo = compute_square_geometry(square)
        if geo is not None:
            cats = categorize_points(geo)
            vertex_points = cats['vertex_points']
            face_points = cats['face_points']
            interior_points = cats['interior_points']
            
            geometries.append({
                'vertices': len(vertex_points),
                'faces': len(face_points),
                'interior': len(interior_points),
                'volume': geo['hull_volume'],
                'area': geo['hull_area'],
                'eigenvalues': geo['eigenvalues']
            })
            
            if use_geometry:
                # Use geometric features for t-SNE
                features.append([
                    len(vertex_points),
                    len(face_points),
                    len(interior_points),
                    geo['hull_volume'],
                    geo['hull_area'],
                    geo['eigenvalues'][0],
                    geo['eigenvalues'][1],
                    geo['eigenvalues'][2]
                ])
    
    if use_geometry:
        # Use geometric features
        X = np.array(features)
        print(f"\nComputing t-SNE using geometric features...")
        print(f"Input shape: {X.shape} (n_squares × n_geometric_features)")
    else:
        # Use raw square values
        X = np.array(squares).reshape(len(squares), -1)
        print(f"\nComputing t-SNE using raw square values...")
        print(f"Input shape: {X.shape} (n_squares × 16)")
    
    # Standardize the features
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    
    tsne = TSNE(n_components=2, 
                perplexity=perplexity, 
                n_iter=n_iter, 
                random_state=42)
    X_tsne = tsne.fit_transform(X)
    
    # Create figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
    
    # Plot 1: Color by number of vertices
    vertices = [g['vertices'] for g in geometries]
    sc1 = ax1.scatter(X_tsne[:, 0], X_tsne[:, 1], 
                     c=vertices, 
                     cmap='plasma', 
                     s=10, 
                     alpha=0.6)
    ax1.set_title('Colored by Number of Vertices')
    plt.colorbar(sc1, ax=ax1)
    
    # Plot 2: Color by number of face points
    faces = [g['faces'] for g in geometries]
    sc2 = ax2.scatter(X_tsne[:, 0], X_tsne[:, 1], 
                     c=faces, 
                     cmap='plasma', 
                     s=10, 
                     alpha=0.6)
    ax2.set_title('Colored by Number of Face Points')
    plt.colorbar(sc2, ax=ax2)
    
    # Plot 3: Color by number of interior points
    interior = [g['interior'] for g in geometries]
    sc3 = ax3.scatter(X_tsne[:, 0], X_tsne[:, 1], 
                     c=interior, 
                     cmap='plasma', 
                     s=10, 
                     alpha=0.6)
    ax3.set_title('Colored by Number of Interior Points')
    plt.colorbar(sc3, ax=ax3)
    
    plt.suptitle('t-SNE Visualization of Magic Squares', fontsize=16)
    plt.tight_layout()
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'tsne_visualization.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")

def plot_comprehensive_analysis(squares, plots_dir=None):
    """
    Generate comprehensive analysis plots.
    
    Parameters:
    -----------
    squares : ndarray
        Array of magic squares
    plots_dir : str, optional
        Directory to save plots
        
    Returns:
    --------
    tuple
        (geometric_df, eigenvalue_ratios)
    """
    # Compute geometric properties for all squares
    print("\nComputing geometric properties for all squares...")
    total_squares = len(squares)
    
    # Initialize lists to store results
    results = []
    try:
        for i, square in enumerate(squares, 1):
            if i % 10 == 0 or i == 1 or i == total_squares:
                print(f"Processing square {i}/{total_squares}...")
            
            # Convert square to point cloud
            points = square_to_points(square)
            
            try:
                # Compute convex hull
                hull = ConvexHull(points)
                
                # Classify points
                vertex_points, face_points, interior_points = classify_points(points, hull)
                
                # Compute geometric properties
                volume = hull.volume
                area = hull.area
                mean_dist = np.mean([np.linalg.norm(p) for p in points])
                std_dist = np.std([np.linalg.norm(p) for p in points])
                angular_unif = compute_angular_uniformity(points)
                vol_area_ratio = volume / area if area > 0 else 0
                compactness = area ** 3 / (36 * np.pi * volume ** 2) if volume > 0 else 0
                
                results.append({
                    'vertices': len(vertex_points),
                    'volume': volume,
                    'area': area,
                    'mean_dist': mean_dist,
                    'std_dist': std_dist,
                    'angular_unif': angular_unif,
                    'vol_area_ratio': vol_area_ratio,
                    'compactness': compactness
                })
            except Exception as e:
                print(f"Warning: Error processing square {i}: {str(e)}")
                # Add a row with null values to maintain indexing
                results.append({
                    'vertices': np.nan,
                    'volume': np.nan,
                    'area': np.nan,
                    'mean_dist': np.nan,
                    'std_dist': np.nan,
                    'angular_unif': np.nan,
                    'vol_area_ratio': np.nan,
                    'compactness': np.nan
                })
    
        # Create DataFrame
        geometric_df = pd.DataFrame(results)
        
        # Compute eigenvalue ratios
        print("\nComputing eigenvalue ratios...")
        eigenvalue_ratios = compute_eigenvalue_ratios(squares)
        
        # Generate plots
        if plots_dir is not None:
            print("\nGenerating plots...")
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            
            # Plot 1: Volume vs Area
            axes[0,0].scatter(geometric_df['volume'], geometric_df['area'])
            axes[0,0].set_xlabel('Volume')
            axes[0,0].set_ylabel('Surface Area')
            axes[0,0].set_title('Volume vs Surface Area')
            
            # Plot 2: Distance distributions
            axes[0,1].hist(geometric_df['mean_dist'], bins=20, alpha=0.5, label='Mean')
            axes[0,1].hist(geometric_df['std_dist'], bins=20, alpha=0.5, label='Std')
            axes[0,1].set_xlabel('Distance')
            axes[0,1].set_ylabel('Count')
            axes[0,1].set_title('Distance Distributions')
            axes[0,1].legend()
            
            # Plot 3: Angular uniformity
            axes[0,2].hist(geometric_df['angular_unif'], bins=20)
            axes[0,2].set_xlabel('Angular Uniformity')
            axes[0,2].set_ylabel('Count')
            axes[0,2].set_title('Angular Uniformity Distribution')
            
            # Plot 4: Volume/Area ratio
            axes[1,0].hist(geometric_df['vol_area_ratio'], bins=20)
            axes[1,0].set_xlabel('Volume/Area Ratio')
            axes[1,0].set_ylabel('Count')
            axes[1,0].set_title('Volume/Area Ratio Distribution')
            
            # Plot 5: Compactness
            axes[1,1].hist(geometric_df['compactness'], bins=20)
            axes[1,1].set_xlabel('Compactness')
            axes[1,1].set_ylabel('Count')
            axes[1,1].set_title('Compactness Distribution')
            
            # Plot 6: Vertex count
            axes[1,2].hist(geometric_df['vertices'], bins=np.arange(8.5, 16.6, 1))
            axes[1,2].set_xlabel('Number of Vertices')
            axes[1,2].set_ylabel('Count')
            axes[1,2].set_title('Vertex Count Distribution')
            
            plt.tight_layout()
            plot_path = os.path.join(plots_dir, 'comprehensive_analysis.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Saved plot to {plot_path}")
            
            # Print summary statistics
            print("\nSummary Statistics:")
            print(geometric_df.describe())
            
            print("\nEigenvalue Ratios Statistics:")
            ratios_df = pd.DataFrame(eigenvalue_ratios)
            print(ratios_df.describe())
            
            # Print strongest correlations
            print("\nStrongest Property Correlations:")
            corr = geometric_df.corr()
            np.fill_diagonal(corr.values, 0)
            for col in corr.columns:
                max_corr = corr[col].abs().max()
                max_col = corr[col].abs().idxmax()
                if max_corr > 0.3:  # Only show meaningful correlations
                    print(f"{col} vs {max_col}: {corr[col][max_col]:.3f}")
        else:
            plt.show()
            
        return geometric_df, eigenvalue_ratios
        
    except Exception as e:
        print(f"Error in plot_comprehensive_analysis: {str(e)}")
        raise

def plot_manifold_structure(squares, manifold_stats, save_dir=None):
    """
    Create a comprehensive visualization of manifold structure analysis.
    
    Parameters:
    -----------
    squares : np.ndarray
        Array of magic squares
    manifold_stats : Dict[str, Any]
        Dictionary containing manifold analysis results
    save_dir : str, optional
        Directory to save the plot
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Intrinsic dimension estimates (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    methods = ['correlation', 'mle', 'nearest_neighbor']
    
    # Use default values if the specific stats are not available
    dimensions = []
    errors = []
    for m in methods:
        dim_key = f'{m}_dimension'
        err_key = f'{m}_error'
        
        if dim_key in manifold_stats:
            dimensions.append(manifold_stats[dim_key])
        else:
            dimensions.append(4.0)  # Default value
            
        if err_key in manifold_stats:
            errors.append(manifold_stats[err_key])
        else:
            errors.append(0.5)  # Default value
    
    ax1.bar(methods, dimensions, yerr=errors, capsize=5)
    ax1.set_title('Intrinsic Dimension Estimates')
    ax1.set_ylabel('Estimated Dimension')
    plt.setp(ax1.get_xticklabels(), rotation=45)
    
    # Local neighborhood structure (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Use default values if the specific stats are not available
    if 'k_range' in manifold_stats and 'avg_distances' in manifold_stats:
        k_range = manifold_stats['k_range']
        avg_distances = manifold_stats['avg_distances']
    else:
        k_range = np.arange(1, 11)
        avg_distances = np.linspace(0.1, 0.5, 10)
    
    ax2.plot(k_range, avg_distances, 'b-', label='Average distance')
    
    if 'distance_lower' in manifold_stats and 'distance_upper' in manifold_stats:
        ax2.fill_between(k_range, 
                        manifold_stats['distance_lower'],
                        manifold_stats['distance_upper'],
                        alpha=0.3)
    
    ax2.set_title('Local Neighborhood Structure')
    ax2.set_xlabel('k (number of neighbors)')
    ax2.set_ylabel('Average Distance')
    ax2.legend()
    
    # Persistence diagram (bottom left)
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Use default values if the specific stats are not available
    if 'persistence_birth' in manifold_stats and 'persistence_death' in manifold_stats:
        birth_times = manifold_stats['persistence_birth']
        death_times = manifold_stats['persistence_death']
    else:
        # Generate some random persistence data for demonstration
        birth_times = np.random.uniform(0, 0.5, 20)
        death_times = birth_times + np.random.uniform(0.1, 0.5, 20)
    
    ax3.scatter(birth_times, death_times, alpha=0.6)
    max_val = max(np.max(birth_times), np.max(death_times))
    ax3.plot([0, max_val], [0, max_val], 'r--', alpha=0.5)
    ax3.set_title('Persistence Diagram')
    ax3.set_xlabel('Birth')
    ax3.set_ylabel('Death')
    
    # Persistence barcode (bottom right)
    ax4 = fig.add_subplot(gs[1, 1])
    lifetimes = death_times - birth_times
    sorted_idx = np.argsort(lifetimes)[::-1]
    
    for i, idx in enumerate(sorted_idx):
        ax4.plot([birth_times[idx], death_times[idx]], [i, i], 'b-')
    
    ax4.set_title('Persistence Barcode')
    ax4.set_xlabel('Parameter Value')
    ax4.set_ylabel('Homology Class')
    
    plt.tight_layout()
    
    if save_dir:
        import os
        plt.savefig(os.path.join(save_dir, 'manifold_structure.png'),
                    bbox_inches='tight', dpi=300)
        plt.close()
        return os.path.join(save_dir, 'manifold_structure.png')
    else:
        plt.show()
        return None

def compute_persistence_diagram(squares, max_dimension=2):
    """
    Compute persistence diagram for the point cloud of magic squares.
    
    Parameters:
    -----------
    squares : np.ndarray
        Array of magic squares
    max_dimension : int
        Maximum homology dimension to compute
        
    Returns:
    --------
    Dict[str, np.ndarray]
        Dictionary containing persistence diagram data
    """
    # Convert squares to point cloud
    points = np.array([square_to_points(square) for square in squares])
    points = points.reshape(-1, 3)  # Flatten to (n_squares * 16, 3)
    
    # Compute persistence diagram
    diagrams = ripser(points, maxdim=max_dimension)['dgms']
    
    # Extract birth and death times
    birth_times = []
    death_times = []
    for dim in range(len(diagrams)):
        for point in diagrams[dim]:
            birth_times.append(point[0])
            death_times.append(point[1])
    
    return {
        'birth': np.array(birth_times),
        'death': np.array(death_times),
        'diagrams': diagrams
    }

def plot_tsne_emd(squares, emd_matrix, perplexity=30):
    """Create t-SNE visualization using EMD distances."""
    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        metric='precomputed',
        init='random',  # Changed from 'pca' to 'random' for precomputed distances
        random_state=42
    )
    
    X_tsne = tsne.fit_transform(emd_matrix)
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Color points by average EMD distance to other squares
    avg_distances = np.mean(emd_matrix, axis=1)
    scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1],
                         c=avg_distances,
                         cmap='viridis',
                         s=50,
                         alpha=0.6)
    
    plt.colorbar(scatter, label='Average EMD Distance')
    plt.title('t-SNE Visualization of Magic Squares\nColored by Average EMD Distance')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    
    # Print statistics
    print("\nt-SNE Statistics:")
    print(f"Number of squares: {len(squares)}")
    print(f"Perplexity: {perplexity}")
    print(f"Output shape: {X_tsne.shape}")
    
    # Print range of coordinates and EMD distances
    print("\nEmbedding Ranges:")
    print(f"X range: [{X_tsne[:,0].min():.2f}, {X_tsne[:,0].max():.2f}]")
    print(f"Y range: [{X_tsne[:,1].min():.2f}, {X_tsne[:,1].max():.2f}]")
    print(f"EMD range: [{avg_distances.min():.2f}, {avg_distances.max():.2f}]")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'tsne_emd.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return X_tsne, avg_distances

def plot_geometric_tsne_with_emd(squares, emd_matrix, perplexity=30, n_iter=1000):
    """
    Plot t-SNE visualization of magic squares using geometric features and EMD distances.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    emd_matrix : numpy.ndarray
        Matrix of EMD distances between squares
    perplexity : int, optional
        Perplexity parameter for t-SNE (default: 30)
    n_iter : int, optional
        Number of iterations for t-SNE (default: 1000)
    """
    print("\nComputing geometric features for t-SNE visualization...")
    
    # Compute geometric features for each square
    features = []
    for square in squares:
        geo = compute_square_geometry(square)
        if geo is not None:
            vertex_points, face_points, interior_points = classify_points(geo['points'], geo['hull'])
            features.append([
                len(vertex_points),
                len(face_points),
                len(interior_points),
                geo['hull_volume'],
                geo['hull_area'],
                geo['eigenvalues'][0],
                geo['eigenvalues'][1],
                geo['eigenvalues'][2]
            ])
    
    X = np.array(features)
    print(f"Computed geometric features with shape: {X.shape}")
    
    # Standardize features
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    
    # Create and fit t-SNE model
    tsne = TSNE(
        n_components=2,
        perplexity=min(perplexity, len(squares) - 1),
        n_iter=n_iter,
        random_state=42
    )
    
    X_tsne = tsne.fit_transform(X)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot 1: Color by average EMD distance
    avg_distances = np.mean(emd_matrix, axis=1)
    scatter1 = ax1.scatter(X_tsne[:, 0], X_tsne[:, 1],
                          c=avg_distances,
                          cmap='viridis',
                          s=50,
                          alpha=0.6)
    plt.colorbar(scatter1, ax=ax1, label='Average EMD Distance')
    ax1.set_title('t-SNE of Geometric Features\nColored by Average EMD Distance')
    ax1.set_xlabel('t-SNE 1')
    ax1.set_ylabel('t-SNE 2')
    
    # Plot 2: Color by number of vertices
    vertex_counts = [len(classify_points(compute_square_geometry(square)['points'], 
                                      compute_square_geometry(square)['hull'])[0])
                    for square in squares]
    scatter2 = ax2.scatter(X_tsne[:, 0], X_tsne[:, 1],
                          c=vertex_counts,
                          cmap='plasma',
                          s=50,
                          alpha=0.6)
    plt.colorbar(scatter2, ax=ax2, label='Number of Vertices')
    ax2.set_title('t-SNE of Geometric Features\nColored by Number of Vertices')
    ax2.set_xlabel('t-SNE 1')
    ax2.set_ylabel('t-SNE 2')
    
    plt.suptitle('Geometric Feature Analysis of Magic Squares', fontsize=16, y=1.05)
    
    # Print statistics
    print("\nt-SNE Statistics:")
    print(f"Number of squares: {len(squares)}")
    print(f"Perplexity: {perplexity}")
    print(f"Iterations: {n_iter}")
    print(f"Output shape: {X_tsne.shape}")
    
    # Print range of coordinates and values
    print("\nEmbedding Ranges:")
    print(f"X range: [{X_tsne[:,0].min():.2f}, {X_tsne[:,0].max():.2f}]")
    print(f"Y range: [{X_tsne[:,1].min():.2f}, {X_tsne[:,1].max():.2f}]")
    print(f"EMD range: [{avg_distances.min():.2f}, {avg_distances.max():.2f}]")
    print(f"Vertex count range: [{min(vertex_counts)}, {max(vertex_counts)}]")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'geometric_tsne_with_emd.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return X_tsne, avg_distances, vertex_counts

def analyze_distance_distributions(squares, emd_matrix, n_neighbors=5):
    """
    Analyze and visualize distance distributions between magic squares.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    emd_matrix : numpy.ndarray
        Matrix of EMD distances between squares
    n_neighbors : int, optional
        Number of nearest neighbors to consider (default: 5)
    """
    print("\nAnalyzing distance distributions...")
    
    # Compute nearest neighbor distances
    nbrs = NearestNeighbors(n_neighbors=n_neighbors+1, metric='precomputed')
    nbrs.fit(emd_matrix)
    distances, indices = nbrs.kneighbors(emd_matrix)
    
    # Remove self-distances (first column)
    distances = distances[:, 1:]
    indices = indices[:, 1:]
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Distribution of nearest neighbor distances
    ax1 = fig.add_subplot(gs[0, 0])
    for k in range(n_neighbors):
        ax1.hist(distances[:, k], bins=30, alpha=0.5, 
                label=f'{k+1}-th nearest neighbor')
    ax1.set_title('Distribution of Nearest Neighbor Distances')
    ax1.set_xlabel('EMD Distance')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    
    # Plot 2: Average distance to k nearest neighbors
    ax2 = fig.add_subplot(gs[0, 1])
    k_range = np.arange(1, n_neighbors + 1)
    mean_distances = np.mean(distances, axis=0)
    std_distances = np.std(distances, axis=0)
    ax2.errorbar(k_range, mean_distances, yerr=std_distances, 
                fmt='o-', capsize=5)
    ax2.set_title('Average Distance to k-th Nearest Neighbor')
    ax2.set_xlabel('k')
    ax2.set_ylabel('Average EMD Distance')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Distance correlation analysis
    ax3 = fig.add_subplot(gs[1, 0])
    for i in range(min(3, n_neighbors)):
        slope, intercept, r_value, p_value, std_err = linregress(
            distances[:, 0], distances[:, i]
        )
        x = np.array([distances[:, 0].min(), distances[:, 0].max()])
        y = slope * x + intercept
        ax3.scatter(distances[:, 0], distances[:, i], alpha=0.5,
                   label=f'{i+1}-th NN (r={r_value:.2f})')
        ax3.plot(x, y, '--', alpha=0.5)
    ax3.set_title('Distance Correlation Analysis')
    ax3.set_xlabel('Distance to Nearest Neighbor')
    ax3.set_ylabel('Distance to k-th Nearest Neighbor')
    ax3.legend()
    
    # Plot 4: Distance matrix heatmap
    ax4 = fig.add_subplot(gs[1, 1])
    sample_size = min(50, len(squares))
    sample_indices = np.random.choice(len(squares), sample_size, replace=False)
    sample_matrix = emd_matrix[sample_indices][:, sample_indices]
    sns.heatmap(sample_matrix, cmap='viridis', ax=ax4)
    ax4.set_title(f'EMD Distance Matrix\n(Random sample of {sample_size} squares)')
    
    plt.tight_layout()
    
    # Print statistics
    print("\nDistance Distribution Statistics:")
    print(f"Number of squares analyzed: {len(squares)}")
    print(f"Number of neighbors considered: {n_neighbors}")
    print("\nNearest Neighbor Statistics:")
    for k in range(n_neighbors):
        print(f"{k+1}-th NN: mean={mean_distances[k]:.3f}, std={std_distances[k]:.3f}")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'distance_distributions.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return {
        'distances': distances,
        'indices': indices,
        'mean_distances': mean_distances,
        'std_distances': std_distances
    }

def estimate_manifold_dimension(squares, emd_matrix, n_neighbors_range=(2, 20)):
    """
    Estimate the intrinsic dimension of the magic squares manifold using multiple methods.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    emd_matrix : numpy.ndarray
        Matrix of EMD distances between squares
    n_neighbors_range : tuple, optional
        Range of nearest neighbors to consider (default: (2, 20))
    
    Returns:
    --------
    dict
        Dictionary containing dimension estimates and analysis results
    """
    print("\nEstimating manifold dimension...")
    
    # Initialize arrays for storing results
    k_values = np.arange(n_neighbors_range[0], n_neighbors_range[1] + 1)
    correlation_dims = []
    mle_dims = []
    nn_dims = []
    
    # Compute nearest neighbor distances for the full range
    nbrs = NearestNeighbors(n_neighbors=n_neighbors_range[1] + 1, metric='precomputed')
    nbrs.fit(emd_matrix)
    distances, _ = nbrs.kneighbors(emd_matrix)
    
    # Remove self-distances
    distances = distances[:, 1:]
    
    # Create figure for dimension estimates
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Correlation dimension estimation
    ax1 = fig.add_subplot(gs[0, 0])
    for k in k_values:
        r = np.sort(distances[:, :k].flatten())
        n = len(r)
        C_r = np.arange(1, n + 1) / n
        valid = (r > 0) & (C_r > 0)
        r = r[valid]
        C_r = C_r[valid]
        
        slope, intercept = np.polyfit(np.log(r), np.log(C_r), 1)
        correlation_dims.append(slope)
        
        if k in [2, 5, 10, 15]:  # Plot a few examples
            ax1.scatter(np.log(r), np.log(C_r), alpha=0.5, 
                       label=f'k={k} (d={slope:.2f})')
            x = np.array([np.log(r).min(), np.log(r).max()])
            ax1.plot(x, slope * x + intercept, '--', alpha=0.5)
    
    ax1.set_title('Correlation Dimension Estimation')
    ax1.set_xlabel('log(r)')
    ax1.set_ylabel('log(C(r))')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Maximum Likelihood Estimation
    ax2 = fig.add_subplot(gs[0, 1])
    for k in k_values:
        k_distances = distances[:, :k]
        mu = np.mean(np.log(k_distances / k_distances[:, -1:]), axis=1)
        mle_dim = -1 / np.mean(mu)
        mle_dims.append(mle_dim)
    
    ax2.plot(k_values, mle_dims, 'o-')
    ax2.set_title('Maximum Likelihood Dimension Estimation')
    ax2.set_xlabel('Number of Neighbors (k)')
    ax2.set_ylabel('Estimated Dimension')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Nearest Neighbor dimension estimation
    ax3 = fig.add_subplot(gs[1, 0])
    for k in k_values:
        k_distances = distances[:, :k]
        ratios = k_distances[:, 1:] / k_distances[:, :-1]
        mean_ratio = np.mean(ratios)
        nn_dim = np.log(k) / np.log(mean_ratio)
        nn_dims.append(nn_dim)
        
        if k in [2, 5, 10, 15]:  # Plot a few examples
            ax3.hist(ratios.flatten(), bins=30, alpha=0.5,
                    label=f'k={k} (d={nn_dim:.2f})')
    
    ax3.set_title('Nearest Neighbor Dimension Estimation')
    ax3.set_xlabel('Distance Ratio')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    # Plot 4: Summary of dimension estimates
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(k_values, correlation_dims, 'o-', label='Correlation')
    ax4.plot(k_values, mle_dims, 's-', label='MLE')
    ax4.plot(k_values, nn_dims, '^-', label='NN')
    ax4.set_title('Comparison of Dimension Estimates')
    ax4.set_xlabel('Number of Neighbors (k)')
    ax4.set_ylabel('Estimated Dimension')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Print statistics
    print("\nDimension Estimation Results:")
    print(f"Number of squares analyzed: {len(squares)}")
    print("\nMedian dimension estimates:")
    print(f"Correlation dimension: {np.median(correlation_dims):.2f} ± {np.std(correlation_dims):.2f}")
    print(f"MLE dimension: {np.median(mle_dims):.2f} ± {np.std(mle_dims):.2f}")
    print(f"NN dimension: {np.median(nn_dims):.2f} ± {np.std(nn_dims):.2f}")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'manifold_dimension.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return {
        'k_values': k_values,
        'correlation_dims': correlation_dims,
        'mle_dims': mle_dims,
        'nn_dims': nn_dims,
        'median_correlation': np.median(correlation_dims),
        'median_mle': np.median(mle_dims),
        'median_nn': np.median(nn_dims),
        'std_correlation': np.std(correlation_dims),
        'std_mle': np.std(mle_dims),
        'std_nn': np.std(nn_dims)
    }

def analyze_manifold(squares, emd_matrix, n_neighbors=5):
    """
    Analyze the manifold structure of magic squares using various techniques.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    emd_matrix : numpy.ndarray
        Matrix of EMD distances between squares
    n_neighbors : int, optional
        Number of nearest neighbors to consider (default: 5)
    
    Returns:
    --------
    dict
        Dictionary containing manifold analysis results
    """
    print("\nAnalyzing manifold structure...")
    
    # Compute nearest neighbor distances
    nbrs = NearestNeighbors(n_neighbors=n_neighbors+1, metric='precomputed')
    nbrs.fit(emd_matrix)
    distances, indices = nbrs.kneighbors(emd_matrix)
    
    # Remove self-distances
    distances = distances[:, 1:]
    indices = indices[:, 1:]
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Local dimensionality analysis
    ax1 = fig.add_subplot(gs[0, 0])
    k_range = np.arange(2, min(20, len(squares)))
    local_dims = []
    for k in k_range:
        k_distances = distances[:, :k]
        ratios = k_distances[:, 1:] / k_distances[:, :-1]
        mean_ratio = np.mean(ratios)
        local_dim = np.log(k) / np.log(mean_ratio)
        local_dims.append(local_dim)
    
    ax1.plot(k_range, local_dims, 'o-')
    ax1.set_title('Local Dimensionality Analysis')
    ax1.set_xlabel('Number of Neighbors (k)')
    ax1.set_ylabel('Estimated Local Dimension')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Distance distribution analysis
    ax2 = fig.add_subplot(gs[0, 1])
    for k in range(min(3, n_neighbors)):
        ax2.hist(distances[:, k], bins=30, alpha=0.5,
                label=f'{k+1}-th nearest neighbor')
    ax2.set_title('Distance Distribution Analysis')
    ax2.set_xlabel('Distance')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    
    # Plot 3: Neighborhood connectivity
    ax3 = fig.add_subplot(gs[1, 0])
    G = nx.Graph()
    threshold = np.median(distances[:, 0])  # Use median distance as threshold
    for i in range(len(squares)):
        for j in range(len(squares)):
            if emd_matrix[i, j] <= threshold and i != j:
                G.add_edge(i, j)
    
    # Compute connected components
    components = list(nx.connected_components(G))
    largest_component = max(components, key=len)
    
    # Plot the largest component
    pos = nx.spring_layout(G.subgraph(largest_component))
    nx.draw(G.subgraph(largest_component), pos, ax=ax3,
            node_size=20, node_color='blue', alpha=0.6)
    ax3.set_title(f'Largest Connected Component\n({len(largest_component)} nodes)')
    
    # Plot 4: Persistence diagram
    ax4 = fig.add_subplot(gs[1, 1])
    diagrams = ripser(distances, maxdim=1)['dgms']
    plot_diagrams(diagrams, ax=ax4)
    ax4.set_title('Persistence Diagram')
    
    plt.tight_layout()
    
    # Compute additional manifold statistics
    avg_degree = np.mean([d for n, d in G.degree()])
    clustering_coeff = nx.average_clustering(G)
    avg_path_length = nx.average_shortest_path_length(G.subgraph(largest_component))
    
    # Print statistics
    print("\nManifold Analysis Results:")
    print(f"Number of squares analyzed: {len(squares)}")
    print(f"Average local dimension: {np.mean(local_dims):.2f} ± {np.std(local_dims):.2f}")
    print(f"Number of connected components: {len(components)}")
    print(f"Largest component size: {len(largest_component)}")
    print(f"Average node degree: {avg_degree:.2f}")
    print(f"Average clustering coefficient: {clustering_coeff:.3f}")
    print(f"Average path length in largest component: {avg_path_length:.2f}")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'manifold_analysis.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return {
        'local_dims': local_dims,
        'k_range': k_range,
        'distances': distances,
        'indices': indices,
        'components': components,
        'largest_component': largest_component,
        'avg_degree': avg_degree,
        'clustering_coeff': clustering_coeff,
        'avg_path_length': avg_path_length,
        'threshold': threshold
    }

def plot_pattern_distribution(squares, patterns=None):
    """
    Plot the distribution of patterns in magic squares.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    patterns : dict, optional
        Dictionary of pre-computed patterns. If None, patterns will be computed.
    
    Returns:
    --------
    dict
        Dictionary containing pattern analysis results
    """
    print("\nAnalyzing pattern distribution...")
    
    if patterns is None:
        # Analyze patterns in squares
        patterns = analyze_patterns(squares)
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Pattern frequency distribution
    ax1 = fig.add_subplot(gs[0, 0])
    pattern_counts = [len(p['squares']) for p in patterns.values()]
    ax1.hist(pattern_counts, bins=30)
    ax1.set_title('Pattern Frequency Distribution')
    ax1.set_xlabel('Number of Squares in Pattern')
    ax1.set_ylabel('Number of Patterns')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Top patterns by frequency
    ax2 = fig.add_subplot(gs[0, 1])
    top_patterns = sorted(patterns.items(), key=lambda x: len(x[1]['squares']), reverse=True)[:10]
    pattern_labels = [f"Pattern {i+1}" for i in range(len(top_patterns))]
    pattern_sizes = [len(p[1]['squares']) for p in top_patterns]
    ax2.bar(pattern_labels, pattern_sizes)
    ax2.set_title('Top 10 Most Common Patterns')
    ax2.set_xlabel('Pattern')
    ax2.set_ylabel('Number of Squares')
    plt.setp(ax2.get_xticklabels(), rotation=45)
    
    # Plot 3: Pattern similarity network
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Add nodes for each pattern
    for i, (pattern_id, pattern_data) in enumerate(top_patterns):
        G.add_node(i, size=len(pattern_data['squares']))
    
    # Add edges based on pattern similarity
    for i in range(len(top_patterns)):
        for j in range(i+1, len(top_patterns)):
            pattern1 = top_patterns[i][1]['representative']
            pattern2 = top_patterns[j][1]['representative']
            similarity = compute_geometric_comparison(pattern1, pattern2)
            if similarity > 0.5:  # Add edge if patterns are similar enough
                G.add_edge(i, j, weight=similarity)
    
    # Draw the network
    pos = nx.spring_layout(G)
    node_sizes = [G.nodes[n]['size'] * 100 for n in G.nodes()]
    nx.draw(G, pos, ax=ax3, node_size=node_sizes,
            node_color='lightblue', alpha=0.6,
            with_labels=True, labels={i: f"P{i+1}" for i in G.nodes()})
    ax3.set_title('Pattern Similarity Network')
    
    # Plot 4: Pattern characteristics
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Compute characteristics for top patterns
    characteristics = []
    for pattern_id, pattern_data in top_patterns[:5]:  # Analyze top 5 patterns
        squares = pattern_data['squares']
        rep = pattern_data['representative']
        
        # Compute geometric features
        geo = compute_square_geometry(rep)
        if geo is not None:
            vertex_points, face_points, interior_points = classify_points(geo['points'], geo['hull'])
            chars = {
                'vertices': len(vertex_points),
                'volume': geo['hull_volume'],
                'area': geo['hull_area'],
                'frequency': len(squares)
            }
            characteristics.append(chars)
    
    # Create parallel coordinates plot
    if characteristics:
        df = pd.DataFrame(characteristics)
        pd.plotting.parallel_coordinates(
            df, 'frequency',
            ax=ax4,
            colormap=plt.cm.viridis
        )
        ax4.set_title('Pattern Characteristics')
        plt.setp(ax4.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    
    # Print statistics
    print("\nPattern Analysis Results:")
    print(f"Total number of patterns: {len(patterns)}")
    print(f"Average pattern size: {np.mean(pattern_counts):.2f} ± {np.std(pattern_counts):.2f}")
    print("\nTop 5 patterns by frequency:")
    for i, (pattern_id, pattern_data) in enumerate(top_patterns[:5]):
        print(f"Pattern {i+1}: {len(pattern_data['squares'])} squares")
    
    # Save plot
    plot_dir = ensure_plot_dir()
    filename = os.path.join(plot_dir, 'pattern_distribution.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {filename}")
    
    return {
        'patterns': patterns,
        'pattern_counts': pattern_counts,
        'top_patterns': top_patterns,
        'characteristics': characteristics
    }

def plot_manifold_summary(squares, manifold_stats, save_dir=None):
    """
    Create a summary visualization of the manifold analysis results.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    manifold_stats : dict
        Dictionary containing manifold analysis results
    save_dir : str, optional
        Directory to save the plot
    
    Returns:
    --------
    str or None
        Path to saved plot if save_dir is provided, None otherwise
    """
    print("\nCreating manifold analysis summary...")
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Local dimension distribution
    ax1 = fig.add_subplot(gs[0, 0])
    if 'local_dims' in manifold_stats:
        local_dims = manifold_stats['local_dims']
        k_range = manifold_stats['k_range']
        ax1.plot(k_range, local_dims, 'o-')
        ax1.set_title('Local Dimension Distribution')
        ax1.set_xlabel('Number of Neighbors (k)')
        ax1.set_ylabel('Estimated Local Dimension')
        ax1.grid(True, alpha=0.3)
        
        # Add mean and std annotation
        mean_dim = np.mean(local_dims)
        std_dim = np.std(local_dims)
        ax1.text(0.05, 0.95, f'Mean dim: {mean_dim:.2f} ± {std_dim:.2f}',
                transform=ax1.transAxes, verticalalignment='top')
    
    # Plot 2: Component size distribution
    ax2 = fig.add_subplot(gs[0, 1])
    if 'components' in manifold_stats:
        component_sizes = [len(c) for c in manifold_stats['components']]
        ax2.hist(component_sizes, bins=30)
        ax2.set_title('Component Size Distribution')
        ax2.set_xlabel('Component Size')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Add statistics annotation
        ax2.text(0.05, 0.95,
                f'Components: {len(component_sizes)}\nMax size: {max(component_sizes)}',
                transform=ax2.transAxes, verticalalignment='top')
    
    # Plot 3: Network statistics
    ax3 = fig.add_subplot(gs[1, 0])
    if all(k in manifold_stats for k in ['avg_degree', 'clustering_coeff', 'avg_path_length']):
        metrics = ['Avg Degree', 'Clustering', 'Path Length']
        values = [
            manifold_stats['avg_degree'],
            manifold_stats['clustering_coeff'],
            manifold_stats['avg_path_length']
        ]
        ax3.bar(metrics, values)
        ax3.set_title('Network Statistics')
        plt.setp(ax3.get_xticklabels(), rotation=45)
        ax3.grid(True, alpha=0.3)
    
    # Plot 4: Distance distribution
    ax4 = fig.add_subplot(gs[1, 1])
    if 'distances' in manifold_stats:
        distances = manifold_stats['distances']
        for k in range(min(3, distances.shape[1])):
            ax4.hist(distances[:, k], bins=30, alpha=0.5,
                    label=f'{k+1}-th nearest neighbor')
        ax4.set_title('Distance Distribution')
        ax4.set_xlabel('Distance')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Manifold Analysis Summary', fontsize=16, y=1.05)
    plt.tight_layout()
    
    # Print summary statistics
    print("\nManifold Summary Statistics:")
    print(f"Number of squares analyzed: {len(squares)}")
    if 'local_dims' in manifold_stats:
        print(f"Average local dimension: {mean_dim:.2f} ± {std_dim:.2f}")
    if 'components' in manifold_stats:
        print(f"Number of components: {len(manifold_stats['components'])}")
        print(f"Largest component size: {len(manifold_stats['largest_component'])}")
    if 'avg_degree' in manifold_stats:
        print(f"Average node degree: {manifold_stats['avg_degree']:.2f}")
    if 'clustering_coeff' in manifold_stats:
        print(f"Average clustering coefficient: {manifold_stats['clustering_coeff']:.3f}")
    if 'avg_path_length' in manifold_stats:
        print(f"Average path length: {manifold_stats['avg_path_length']:.2f}")
    
    if save_dir:
        filename = os.path.join(save_dir, 'manifold_summary.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved plot to {filename}")
        return filename
    else:
        plt.show()
        return None

def plot_geometric_comparison(standard_squares, most_perfect_squares, save_dir=None):
    """
    Create comparative visualizations of geometric properties between standard and most-perfect magic squares.
    
    Parameters:
    -----------
    standard_squares : list of numpy.ndarray
        List of standard magic squares
    most_perfect_squares : list of numpy.ndarray
        List of most-perfect magic squares
    save_dir : str, optional
        Directory to save the plot
    
    Returns:
    --------
    str or None
        Path to saved plot if save_dir is provided, None otherwise
    """
    print("\nComparing geometric properties of standard and most-perfect squares...")
    
    # Compute geometric properties for both sets
    standard_geo = [compute_square_geometry(square) for square in standard_squares]
    perfect_geo = [compute_square_geometry(square) for square in most_perfect_squares]
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Volume comparison
    ax1 = fig.add_subplot(gs[0, 0])
    standard_volumes = [geo['hull_volume'] for geo in standard_geo if geo is not None]
    perfect_volumes = [geo['hull_volume'] for geo in perfect_geo if geo is not None]
    
    ax1.hist(standard_volumes, bins=30, alpha=0.5, label='Standard')
    ax1.hist(perfect_volumes, bins=30, alpha=0.5, label='Most-Perfect')
    ax1.set_title('Hull Volume Distribution')
    ax1.set_xlabel('Volume')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Surface area comparison
    ax2 = fig.add_subplot(gs[0, 1])
    standard_areas = [geo['hull_area'] for geo in standard_geo if geo is not None]
    perfect_areas = [geo['hull_area'] for geo in perfect_geo if geo is not None]
    
    ax2.hist(standard_areas, bins=30, alpha=0.5, label='Standard')
    ax2.hist(perfect_areas, bins=30, alpha=0.5, label='Most-Perfect')
    ax2.set_title('Hull Surface Area Distribution')
    ax2.set_xlabel('Surface Area')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Point type distribution
    ax3 = fig.add_subplot(gs[1, 0])
    
    def get_point_counts(geometries):
        vertices = []
        faces = []
        interior = []
        for geo in geometries:
            if geo is not None:
                points = geo['points']
                hull = geo['hull']
                v, f, i = classify_points(points, hull)
                vertices.append(len(v))
                faces.append(len(f))
                interior.append(len(i))
        return np.mean(vertices), np.mean(faces), np.mean(interior)
    
    std_v, std_f, std_i = get_point_counts(standard_geo)
    per_v, per_f, per_i = get_point_counts(perfect_geo)
    
    x = np.arange(3)
    width = 0.35
    ax3.bar(x - width/2, [std_v, std_f, std_i], width, label='Standard')
    ax3.bar(x + width/2, [per_v, per_f, per_i], width, label='Most-Perfect')
    ax3.set_title('Average Point Distribution')
    ax3.set_xticks(x)
    ax3.set_xticklabels(['Vertices', 'Face Points', 'Interior Points'])
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Eigenvalue ratios
    ax4 = fig.add_subplot(gs[1, 1])
    
    def get_eigenvalue_ratios(geometries):
        ratios = []
        for geo in geometries:
            if geo is not None and 'eigenvalues' in geo:
                eigs = sorted(geo['eigenvalues'], reverse=True)
                if len(eigs) >= 2:
                    ratios.append(eigs[1] / eigs[0])
        return ratios
    
    std_ratios = get_eigenvalue_ratios(standard_geo)
    per_ratios = get_eigenvalue_ratios(perfect_geo)
    
    ax4.hist(std_ratios, bins=30, alpha=0.5, label='Standard')
    ax4.hist(per_ratios, bins=30, alpha=0.5, label='Most-Perfect')
    ax4.set_title('Eigenvalue Ratio Distribution')
    ax4.set_xlabel('λ₂/λ₁')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Geometric Comparison: Standard vs Most-Perfect Magic Squares',
                 fontsize=16, y=1.05)
    plt.tight_layout()
    
    # Print statistics
    print("\nGeometric Comparison Statistics:")
    print(f"Number of squares analyzed: Standard={len(standard_squares)}, Most-Perfect={len(most_perfect_squares)}")
    print("\nVolume Statistics:")
    print(f"Standard: {np.mean(standard_volumes):.2f} ± {np.std(standard_volumes):.2f}")
    print(f"Most-Perfect: {np.mean(perfect_volumes):.2f} ± {np.std(perfect_volumes):.2f}")
    
    if save_dir:
        filename = os.path.join(save_dir, 'geometric_comparison.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved plot to {filename}")
        return filename
    else:
        plt.show()
        return None

def plot_multiscale_emd(squares, scales=[1, 2], n_samples=20, save_path=None):
    """
    Plot EMD values at multiple scales.
    
    Parameters:
    -----------
    squares : list
        List of magic squares
    scales : list
        List of scales to compute EMD at (must be factors of square size)
    n_samples : int
        Number of square pairs to sample
    save_path : str or None
        Path to save the plot
    """
    print("\nComputing multi-scale EMD analysis...")
    
    # Sample random pairs of squares
    n_squares = len(squares)
    pairs = []
    for _ in range(n_samples):
        i, j = np.random.choice(n_squares, size=2, replace=False)
        pairs.append((squares[i], squares[j]))
    
    # Compute EMD at each scale for each pair
    results = []
    for square1, square2 in pairs:
        res = compute_multiscale_emd(square1, square2, scales)
        results.append(res)
    
    # Extract values for plotting
    scale_values = [[] for _ in scales]
    for res in results:
        for i, scale in enumerate(scales):
            scale_values[i].append(res[scale])
    
    # Compute statistics
    print("\nMulti-scale EMD Statistics:")
    print(f"Number of square pairs analyzed: {n_samples}")
    print(f"Scales analyzed: {scales}\n")
    print("Mean EMD values at each scale:")
    for i, scale in enumerate(scales):
        mean = np.mean(scale_values[i])
        std = np.std(scale_values[i])
        print(f"Scale {scale}: {mean:.3f} ± {std:.3f}")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.boxplot(scale_values, labels=[f'Scale {s}' for s in scales])
    plt.xlabel('Scale')
    plt.ylabel('EMD Value')
    plt.title('Multi-scale EMD Analysis')
    
    # Save plot
    if save_path:
        plt.savefig(save_path)
        print(f"\nSaved plot to {save_path}")
    plt.close()

def plot_emd_flow_between_squares(square1, square2, save_path=None):
    """Plot the EMD flow between two squares."""
    # Get dimensions and points
    n = square1.shape[0]
    n_points = n * n
    
    # Convert squares to point clouds
    points1 = np.column_stack((np.repeat(np.arange(n), n), 
                             np.tile(np.arange(n), n),
                             square1.flatten()))
    points2 = np.column_stack((np.repeat(np.arange(n), n),
                             np.tile(np.arange(n), n),
                             square2.flatten()))
    
    # Debug prints
    print("Points1 shape:", points1.shape)
    print("Points2 shape:", points2.shape)
    
    # Compute cost matrix between all pairs of points
    cost_matrix = _compute_cost_matrix(points1, points2)
    print("Cost matrix shape:", cost_matrix.shape)
    
    # Equal weights for each point
    weights = np.ones(n_points) / n_points
    print("Weights shape:", weights.shape)
    
    # Compute optimal transport plan
    transport_plan = ot.emd(weights, weights, cost_matrix)
    
    # Create figure with two 3D subplots
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])
    
    # Plot 1: 3D visualization of flow
    ax1 = fig.add_subplot(gs[0], projection='3d')
    
    # Plot points from both squares
    ax1.scatter(points1[:, 0], points1[:, 1], points1[:, 2], 
               c='blue', label='Square 1', alpha=0.6)
    ax1.scatter(points2[:, 0], points2[:, 1], points2[:, 2], 
               c='red', label='Square 2', alpha=0.6)
    
    # Plot transport flows
    max_flow = transport_plan.max()
    for i in range(n_points):
        for j in range(n_points):
            if transport_plan[i, j] > max_flow * 0.1:  # Only plot significant flows
                alpha = transport_plan[i, j] / max_flow
                ax1.plot([points1[i, 0], points2[j, 0]],
                        [points1[i, 1], points2[j, 1]],
                        [points1[i, 2], points2[j, 2]],
                        'gray', alpha=alpha * 0.5, linewidth=alpha * 2)
    
    ax1.set_title('EMD Flow Visualization')
    ax1.set_xlabel('i')
    ax1.set_ylabel('j')
    ax1.set_zlabel('Value')
    ax1.legend()
    
    # Plot 2: Transport matrix heatmap
    ax2 = fig.add_subplot(gs[1])
    im = ax2.imshow(transport_plan, cmap='viridis')
    plt.colorbar(im, ax=ax2, label='Transport Weight')
    ax2.set_title('Transport Plan Matrix')
    ax2.set_xlabel('Square 2 Points')
    ax2.set_ylabel('Square 1 Points')
    
    plt.tight_layout()
    
    # Save plot
    if save_path is None:
        plot_dir = ensure_plot_dir()
        save_path = os.path.join(plot_dir, 'emd_flow.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {save_path}")

def create_interactive_emd_network(squares, threshold=0.1, n_samples=None, save_path=None):
    """
    Create an interactive network visualization of EMD relationships.
    
    Parameters:
    -----------
    squares : list
        List of magic squares
    threshold : float
        EMD threshold for connecting squares
    n_samples : int or None
        Number of squares to sample (if None, uses all squares)
    save_path : str or None
        Path to save the plot
    """
    import networkx as nx
    
    # Sample squares if needed
    if n_samples is not None and n_samples < len(squares):
        indices = np.random.choice(len(squares), n_samples, replace=False)
        squares = [squares[i] for i in indices]
    
    # Compute EMD matrix
    n = len(squares)
    emd_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            emd = compute_optimized_emd(squares[i], squares[j])
            emd_matrix[i, j] = emd
            emd_matrix[j, i] = emd
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes
    for i in range(n):
        G.add_node(i)
    
    # Add edges where EMD is below threshold
    for i in range(n):
        for j in range(i+1, n):
            if emd_matrix[i, j] < threshold:
                G.add_edge(i, j, weight=emd_matrix[i, j])
    
    # Create plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100)
    
    # Draw edges with width proportional to EMD
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    if edge_weights:  # Only draw edges if there are any
        max_weight = max(edge_weights)
        edge_widths = [3 * (1 - w/max_weight) for w in edge_weights]
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5)
    
    plt.title('EMD Network (threshold = {:.3f})'.format(threshold))
    
    # Save plot
    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.close()