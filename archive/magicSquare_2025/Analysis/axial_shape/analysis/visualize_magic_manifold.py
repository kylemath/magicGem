import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import umap  # Add UMAP import
import json
from tqdm import tqdm  # Add progress bar
import warnings
import plotly.utils
from manifoldAllFeatures import compute_all_features  # Changed to absolute import

# A standard 4x4 magic square for reference
BASE_MAGIC_SQUARE = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

def visualize_magic_square_manifold(method='umap', sample_size=None, dimensions=4):
    """Visualize the manifold of magic squares.
    
    Args:
        method (str): Dimensionality reduction method to use ('umap' or 'tsne')
        sample_size (int, optional): Number of magic squares to sample. If None, uses all squares.
        dimensions (int): Number of dimensions for the visualization (3 or 4)
    """
    # Create output directory
    save_dir = 'figures_manifold'
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate samples
    n_magic = 7040 if sample_size is None else min(sample_size, 7040)  # Increased from 70 to 500
    n_perturbed = 0  # Increased from 70 to 100
    n_random = 0  # Increased from 70 to 100
    
    print(f"Generating {n_magic} magic squares and {n_perturbed} perturbed arrangements plus {n_random} random arrangements...")
    magic_squares, numbers, groups, versions = generate_magic_squares(n_magic)
    
    # Initialize empty arrays for non-magic and random squares if not requested
    non_magic_arrangements = []
    if n_perturbed > 0 or n_random > 0:
        non_magic_arrangements = generate_non_magic_squares(n_perturbed, perturbation_levels=20, n_random=n_random)
    
    # Extract levels and squares from non-magic list, separating random squares
    levels = []
    non_magic_squares = []
    random_squares = []
    
    if non_magic_arrangements:  # Only process if we have non-magic arrangements
        for level, square in non_magic_arrangements:
            if level == 21:  # perturbation_levels + 1
                random_squares.append(square)
            else:
                levels.append(level)
                non_magic_squares.append(square)
    
    levels = np.array(levels) if levels else np.array([])
    non_magic_squares = np.array(non_magic_squares) if non_magic_squares else np.array([]).reshape(0, 4, 4)
    random_squares = np.array(random_squares) if random_squares else np.array([]).reshape(0, 4, 4)
    
    # Calculate extended features for all types of squares
    magic_extended_features = []
    non_magic_extended_features = []
    random_extended_features = []
    magic_squares_str = []
    non_magic_squares_str = []
    random_squares_str = []
    
    print("\nCalculating features for magic squares...")
    for square in tqdm(magic_squares, desc="Processing magic squares"):
        # Get all features from manifoldAllFeatures
        all_features = compute_all_features(square)
        
        # Print features for the first square only
        if len(magic_extended_features) == 0:
            print("\nFeatures for first magic square:")
            print("--------------------------------")
            print("Geometric Features:")
            print(f"  Hull Volume: {all_features['hull_volume']:.6f}")
            print(f"  Hull Area: {all_features['hull_area']:.6f}")
            print(f"  Hull Density: {all_features['hull_density']:.6f}")
            print(f"  Area/Volume Ratio: {all_features['area_volume_ratio']:.6f}")
            print(f"  Number of Vertices: {all_features['n_vertices']}")
            print(f"  Number of Face Points: {all_features['n_face_points']}")
            print(f"  Number of Interior Points: {all_features['n_interior_points']}")
            print(f"  Vertex Ratio: {all_features['vertex_ratio']:.6f}")
            print(f"  Face Ratio: {all_features['face_ratio']:.6f}")
            print(f"  Interior Ratio: {all_features['interior_ratio']:.6f}")
            print(f"  Angular Uniformity: {all_features['angular_uniformity']:.6f}")
            print("\nEigenvalue Features:")
            print(f"  Eigenvalue 1: {all_features['eigenvalue_1']:.6f}")
            print(f"  Eigenvalue 2: {all_features['eigenvalue_2']:.6f}")
            print(f"  Eigenvalue 3: {all_features['eigenvalue_3']:.6f}")
            print(f"  Eigenvalue Ratio 2:1: {all_features['eigenvalue_ratio_21']:.6f}")
            print(f"  Eigenvalue Ratio 3:2: {all_features['eigenvalue_ratio_32']:.6f}")
            print(f"  Eigenvalue Ratio 3:1: {all_features['eigenvalue_ratio_31']:.6f}")
            print(f"  Aspect Ratio 2:1: {all_features['aspect_ratio_21']:.6f}")
            print(f"  Aspect Ratio 3:1: {all_features['aspect_ratio_31']:.6f}")
            print("\nSpatial Distribution Features:")
            print(f"  Mean Distance to Centroid: {all_features['mean_dist_to_centroid']:.6f}")
            print(f"  Std Distance to Centroid: {all_features['std_dist_to_centroid']:.6f}")
            print(f"  Max Distance to Centroid: {all_features['max_dist_to_centroid']:.6f}")
            print("\nFace Analysis Features:")
            print(f"  Number of Faces: {all_features['n_faces']}")
            print(f"  Mean Face Area: {all_features['mean_face_area']:.6f}")
            print(f"  Std Face Area: {all_features['std_face_area']:.6f}")
            print(f"  Face Area Ratio: {all_features['face_area_ratio']:.6f}")
            print(f"  Sphericity: {all_features['sphericity']:.6f}")
            print("\nSubsquare Analysis Features:")
            print(f"  Subsquare Sum Mean: {all_features['subsquare_sum_mean']:.6f}")
            print(f"  Subsquare Sum Std: {all_features['subsquare_sum_std']:.6f}")
            print(f"  Subsquare Sum Range: {all_features['subsquare_sum_range']:.6f}")
            print("\nLocal Gradient Features:")
            print(f"  Mean Local Gradient: {all_features['mean_local_gradient']:.6f}")
            print(f"  Std Local Gradient: {all_features['std_local_gradient']:.6f}")
            print("\nRaw Square Values:")
            print(square)
            print("--------------------------------\n")
        
        # Extract features in a consistent order
        feature_list = [
            # Geometric features
            all_features['hull_volume'],
            all_features['hull_area'], 
            all_features['hull_density'],
            all_features['area_volume_ratio'],
            all_features['n_vertices'],
            all_features['n_face_points'],
            all_features['n_interior_points'],
            all_features['vertex_ratio'],
            all_features['face_ratio'],
            all_features['interior_ratio'],
            all_features['angular_uniformity'],
            all_features['eigenvalue_1'],
            all_features['eigenvalue_2'],
            all_features['eigenvalue_3'],
            all_features['eigenvalue_ratio_21'],
            all_features['eigenvalue_ratio_32'],
            all_features['eigenvalue_ratio_31'],
            all_features['aspect_ratio_21'],
            all_features['aspect_ratio_31'],
            all_features['mean_dist_to_centroid'],
            all_features['std_dist_to_centroid'],
            all_features['max_dist_to_centroid'],
            all_features['n_faces'],
            all_features['mean_face_area'],
            all_features['std_face_area'],
            all_features['face_area_ratio'],
            all_features['sphericity'],
            all_features['subsquare_sum_mean'],
            all_features['subsquare_sum_std'],
            all_features['subsquare_sum_range'],
            all_features['mean_local_gradient'],
            all_features['std_local_gradient'],
            # Raw square values
            *square.flatten()  # 16 raw values
        ]
        magic_extended_features.append(feature_list)
        magic_squares_str.append(str(square.tolist()))
    
    if len(non_magic_squares) > 0:
        print("\nCalculating features for non-magic squares...")
        for square in non_magic_squares:
            # Get all features from manifoldAllFeatures
            all_features = compute_all_features(square)
            
            # Extract features in same order as magic squares
            feature_list = [
                # Geometric features
                all_features['hull_volume'],
                all_features['hull_area'], 
                all_features['hull_density'],
                all_features['area_volume_ratio'],
                all_features['n_vertices'],
                all_features['n_face_points'],
                all_features['n_interior_points'],
                all_features['vertex_ratio'],
                all_features['face_ratio'],
                all_features['interior_ratio'],
                all_features['angular_uniformity'],
                all_features['eigenvalue_1'],
                all_features['eigenvalue_2'],
                all_features['eigenvalue_3'],
                all_features['eigenvalue_ratio_21'],
                all_features['eigenvalue_ratio_32'],
                all_features['eigenvalue_ratio_31'],
                all_features['aspect_ratio_21'],
                all_features['aspect_ratio_31'],
                all_features['mean_dist_to_centroid'],
                all_features['std_dist_to_centroid'],
                all_features['max_dist_to_centroid'],
                all_features['n_faces'],
                all_features['mean_face_area'],
                all_features['std_face_area'],
                all_features['face_area_ratio'],
                all_features['sphericity'],
                all_features['subsquare_sum_mean'],
                all_features['subsquare_sum_std'],
                all_features['subsquare_sum_range'],
                all_features['mean_local_gradient'],
                all_features['std_local_gradient'],
                # Raw square values
                *square.flatten()  # 16 raw values
            ]
            non_magic_extended_features.append(feature_list)
            non_magic_squares_str.append(str(square.tolist()))
    
    if len(random_squares) > 0:
        print("\nCalculating features for random squares...")
        for square in random_squares:
            # Get all features from manifoldAllFeatures
            all_features = compute_all_features(square)
            
            # Extract features in same order as magic squares
            feature_list = [
                # Geometric features
                all_features['hull_volume'],
                all_features['hull_area'], 
                all_features['hull_density'],
                all_features['area_volume_ratio'],
                all_features['n_vertices'],
                all_features['n_face_points'],
                all_features['n_interior_points'],
                all_features['vertex_ratio'],
                all_features['face_ratio'],
                all_features['interior_ratio'],
                all_features['angular_uniformity'],
                all_features['eigenvalue_1'],
                all_features['eigenvalue_2'],
                all_features['eigenvalue_3'],
                all_features['eigenvalue_ratio_21'],
                all_features['eigenvalue_ratio_32'],
                all_features['eigenvalue_ratio_31'],
                all_features['aspect_ratio_21'],
                all_features['aspect_ratio_31'],
                all_features['mean_dist_to_centroid'],
                all_features['std_dist_to_centroid'],
                all_features['max_dist_to_centroid'],
                all_features['n_faces'],
                all_features['mean_face_area'],
                all_features['std_face_area'],
                all_features['face_area_ratio'],
                all_features['sphericity'],
                all_features['subsquare_sum_mean'],
                all_features['subsquare_sum_std'],
                all_features['subsquare_sum_range'],
                all_features['mean_local_gradient'],
                all_features['std_local_gradient'],
                # Raw square values
                *square.flatten()  # 16 raw values
            ]
            random_extended_features.append(feature_list)
            random_squares_str.append(str(square.tolist()))
        
    magic_extended_features = np.array(magic_extended_features)
    non_magic_extended_features = np.array(non_magic_extended_features) if non_magic_extended_features else np.array([]).reshape(0, magic_extended_features.shape[1])
    random_extended_features = np.array(random_extended_features) if random_extended_features else np.array([]).reshape(0, magic_extended_features.shape[1])
    
    # Combine all features for dimensionality reduction
    extended_features = []
    if len(magic_extended_features) > 0:
        extended_features.append(magic_extended_features)
    if len(non_magic_extended_features) > 0:
        extended_features.append(non_magic_extended_features)
    if len(random_extended_features) > 0:
        extended_features.append(random_extended_features)
    
    extended_features = np.vstack(extended_features) if extended_features else np.array([])
    
    # Print the feature array that will be used for t-SNE
    print("\nFeature array shape:", extended_features.shape)
    print("First row of features (first square):")
    print(extended_features[0])
    
    # Apply dimensionality reduction with optimized parameters
    if method == 'umap':
        print(f"\nApplying UMAP dimensionality reduction to {dimensions}D...")
        reducer = umap.UMAP(
            n_components=dimensions,
            n_neighbors=min(30, len(extended_features)-1) if len(extended_features) > 0 else 2,
            min_dist=0.1,
            metric='euclidean',
            random_state=42,
            verbose=True
        )
    else:  # t-SNE
        print(f"\nApplying t-SNE dimensionality reduction to {dimensions}D...")
        reducer = TSNE(
            n_components=dimensions,
            random_state=42,
            perplexity=min(30, len(extended_features)-1) if len(extended_features) > 0 else 2,
            early_exaggeration=4,  # Reduced from 12
            max_iter=1000,  # Reduced from 2000
            method='exact',
            n_iter_without_progress=25,  # Add early stopping
            verbose=1  # Add verbosity
        )
    
    if len(extended_features) > 0:
        print(f"\nRunning {method.upper()} on {len(extended_features)} data points...")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        reduced_results = reducer.fit_transform(extended_features)
        print(f"{method.upper()} completed successfully!")
    else:
        print("Error: No data points available for dimensionality reduction")
        return
    
    # Split results by type
    n_magic_squares = len(magic_squares)
    n_non_magic_squares = len(non_magic_squares)
    
    magic_reduced = reduced_results[:n_magic_squares]
    non_magic_reduced = reduced_results[n_magic_squares:n_magic_squares + n_non_magic_squares] if n_non_magic_squares > 0 else np.array([]).reshape(0, dimensions)
    random_reduced = reduced_results[n_magic_squares + n_non_magic_squares:] if len(random_squares) > 0 else np.array([]).reshape(0, dimensions)
    
    # Create DataFrames for each type
    df_magic = pd.DataFrame({
        'dim_1': magic_reduced[:, 0],
        'dim_2': magic_reduced[:, 1],
        'dim_3': magic_reduced[:, 2],
        'type': ['Magic Square'] * n_magic_squares,
        'level': [0] * n_magic_squares,
        'number': numbers,
        'group': groups,
        'version': versions,
        'square': magic_squares_str,
        'row_var': magic_extended_features[:, 4],
        'col_var': magic_extended_features[:, 5],
        'diag_var': magic_extended_features[:, 6]
    })
    
    if dimensions == 4:
        df_magic['dim_4'] = magic_reduced[:, 3]
    
    if len(non_magic_squares) > 0:
        df_non_magic = pd.DataFrame({
            'dim_1': non_magic_reduced[:, 0],
            'dim_2': non_magic_reduced[:, 1],
            'dim_3': non_magic_reduced[:, 2],
            'type': ['Perturbed'] * n_non_magic_squares,
            'level': levels,
            'square': non_magic_squares_str,
            'row_var': non_magic_extended_features[:, 4],
            'col_var': non_magic_extended_features[:, 5],
            'diag_var': non_magic_extended_features[:, 6]
        })
        
        if dimensions == 4:
            df_non_magic['dim_4'] = non_magic_reduced[:, 3]
    else:
        df_non_magic = pd.DataFrame(columns=['dim_1', 'dim_2', 'dim_3', 'type', 'level', 'square', 'row_var', 'col_var', 'diag_var'])
        if dimensions == 4:
            df_non_magic['dim_4'] = []
    
    if len(random_squares) > 0:
        df_random = pd.DataFrame({
            'dim_1': random_reduced[:, 0],
            'dim_2': random_reduced[:, 1],
            'dim_3': random_reduced[:, 2],
            'type': ['Random'] * len(random_squares),
            'level': [-1] * len(random_squares),  # Use -1 to distinguish random squares
            'square': random_squares_str,
            'row_var': random_extended_features[:, 4],
            'col_var': random_extended_features[:, 5],
            'diag_var': random_extended_features[:, 6]
        })
        
        if dimensions == 4:
            df_random['dim_4'] = random_reduced[:, 3]
    else:
        df_random = pd.DataFrame(columns=['dim_1', 'dim_2', 'dim_3', 'type', 'level', 'square', 'row_var', 'col_var', 'diag_var'])
        if dimensions == 4:
            df_random['dim_4'] = []
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add magic squares with color options
    if dimensions == 4:
        fig.add_trace(go.Scatter3d(
            x=df_magic['dim_1'].tolist(),
            y=df_magic['dim_2'].tolist(),
            z=df_magic['dim_3'].tolist(),
            mode='markers',
            marker=dict(
                size=6,
                color=df_magic['dim_4'].tolist(),  # Use 4th dimension for color
                colorscale='Viridis',
                line=dict(width=0.5, color='darkblue'),
                opacity=0.8,
                showscale=True,
                colorbar=dict(
                    title='4D Value',
                    x=1.1
                )
            ),
            name='Magic Square',
            hovertemplate=(
                '<b>Type:</b> %{customdata[0]}<br>' +
                '<b>Number:</b> %{customdata[7]}<br>' +
                '<b>Group:</b> %{customdata[5]}<br>' +
                '<b>Version:</b> %{customdata[6]}<br>' +
                '<b>Square:</b><br>%{customdata[1]}<br>' +
                '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                '<b>4D Value:</b> %{marker.color:.3f}<br>' +
                '<extra></extra>'
            ),
            customdata=np.column_stack((
                df_magic['type'],
                df_magic['square'],
                df_magic['row_var'],
                df_magic['col_var'],
                df_magic['diag_var'],
                df_magic['group'],
                df_magic['version'],
                df_magic['number']
            )).tolist()
        ))
    else:
        fig.add_trace(go.Scatter3d(
            x=df_magic['dim_1'].tolist(),
            y=df_magic['dim_2'].tolist(),
            z=df_magic['dim_3'].tolist(),
            mode='markers',
            marker=dict(
                size=6,
                color=df_magic['version'].tolist(),  # Color by version
                colorscale=[
                    [0, '#1f77b4'],     # Version 1
                    [0.143, '#ff7f0e'], # Version 2
                    [0.286, '#2ca02c'], # Version 3
                    [0.429, '#d62728'], # Version 4
                    [0.572, '#9467bd'], # Version 5
                    [0.715, '#8c564b'], # Version 6
                    [0.858, '#e377c2'], # Version 7
                    [1, '#7f7f7f']      # Version 8
                ],
                line=dict(width=0.5, color='darkblue'),
                opacity=0.8,
                showscale=True,
                colorbar=dict(
                    title='Version',
                    tickmode='array',
                    tickvals=[1, 2, 3, 4, 5, 6, 7, 8],
                    ticktext=['Version 1', 'Version 2', 'Version 3', 'Version 4',
                             'Version 5', 'Version 6', 'Version 7', 'Version 8'],
                    len=400,
                    lenmode='pixels',
                    x=1.1
                )
            ),
            name='Magic Square',
            hovertemplate=(
                '<b>Type:</b> %{customdata[0]}<br>' +
                '<b>Number:</b> %{customdata[7]}<br>' +
                '<b>Group:</b> %{customdata[5]}<br>' +
                '<b>Version:</b> %{customdata[6]}<br>' +
                '<b>Square:</b><br>%{customdata[1]}<br>' +
                '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                '<extra></extra>'
            ),
            customdata=np.column_stack((
                df_magic['type'],
                df_magic['square'],
                df_magic['row_var'],
                df_magic['col_var'],
                df_magic['diag_var'],
                df_magic['group'],
                df_magic['version'],
                df_magic['number']
            )).tolist()
        ))
    
    # Add perturbed squares if they exist
    if len(non_magic_squares) > 0:
        if dimensions == 4:
            fig.add_trace(go.Scatter3d(
                x=df_non_magic['dim_1'].tolist(),
                y=df_non_magic['dim_2'].tolist(),
                z=df_non_magic['dim_3'].tolist(),
                mode='markers',
                marker=dict(
                    size=4,
                    color=df_non_magic['dim_4'].tolist(),
                    colorscale='Viridis',
                    line=dict(width=0.2, color='gray'),
                    opacity=0.6,
                    showscale=True,
                    colorbar=dict(
                        title='4D Value',
                        x=1.2
                    )
                ),
                name='Perturbed',
                hovertemplate=(
                    '<b>Type:</b> %{customdata[0]}<br>' +
                    '<b>Level:</b> %{customdata[5]}<br>' +
                    '<b>Square:</b><br>%{customdata[1]}<br>' +
                    '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                    '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                    '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                    '<b>4D Value:</b> %{marker.color:.3f}<br>' +
                    '<extra></extra>'
                ),
                customdata=np.column_stack((
                    df_non_magic['type'],
                    df_non_magic['square'],
                    df_non_magic['row_var'],
                    df_non_magic['col_var'],
                    df_non_magic['diag_var'],
                    df_non_magic['level']
                )).tolist()
            ))
        else:
            fig.add_trace(go.Scatter3d(
                x=df_non_magic['dim_1'].tolist(),
                y=df_non_magic['dim_2'].tolist(),
                z=df_non_magic['dim_3'].tolist(),
                mode='markers',
                marker=dict(
                    size=4,
                    color=df_non_magic['level'].tolist(),
                    colorscale='Plasma',
                    line=dict(width=0.2, color='gray'),
                    opacity=0.6,
                    showscale=True,
                    colorbar=dict(
                        title='Perturbation Level',
                        x=1.2
                    )
                ),
                name='Perturbed',
                hovertemplate=(
                    '<b>Type:</b> %{customdata[0]}<br>' +
                    '<b>Level:</b> %{customdata[5]}<br>' +
                    '<b>Square:</b><br>%{customdata[1]}<br>' +
                    '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                    '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                    '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                    '<extra></extra>'
                ),
                customdata=np.column_stack((
                    df_non_magic['type'],
                    df_non_magic['square'],
                    df_non_magic['row_var'],
                    df_non_magic['col_var'],
                    df_non_magic['diag_var'],
                    df_non_magic['level']
                )).tolist()
            ))
    
    # Add random squares if they exist
    if len(random_squares) > 0:
        if dimensions == 4:
            fig.add_trace(go.Scatter3d(
                x=df_random['dim_1'].tolist(),
                y=df_random['dim_2'].tolist(),
                z=df_random['dim_3'].tolist(),
                mode='markers',
                marker=dict(
                    size=5,
                    color=df_random['dim_4'].tolist(),
                    colorscale='Viridis',
                    symbol='diamond',
                    line=dict(width=0.2, color='black'),
                    opacity=0.7,
                    showscale=True,
                    colorbar=dict(
                        title='4D Value',
                        x=1.3
                    )
                ),
                name='Random',
                hovertemplate=(
                    '<b>Type:</b> Random Square<br>' +
                    '<b>Square:</b><br>%{customdata[1]}<br>' +
                    '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                    '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                    '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                    '<b>4D Value:</b> %{marker.color:.3f}<br>' +
                    '<extra></extra>'
                ),
                customdata=np.column_stack((
                    df_random['type'],
                    df_random['square'],
                    df_random['row_var'],
                    df_random['col_var'],
                    df_random['diag_var']
                )).tolist()
            ))
        else:
            fig.add_trace(go.Scatter3d(
                x=df_random['dim_1'].tolist(),
                y=df_random['dim_2'].tolist(),
                z=df_random['dim_3'].tolist(),
                mode='markers',
                marker=dict(
                    size=5,
                    color=df_random['level'].tolist(),
                    colorscale='Viridis',
                    symbol='diamond',
                    line=dict(width=0.2, color='black'),
                    opacity=0.7,
                    showscale=True,
                    colorbar=dict(
                        title='Random',
                        x=1.3
                    )
                ),
                name='Random',
                hovertemplate=(
                    '<b>Type:</b> Random Square<br>' +
                    '<b>Square:</b><br>%{customdata[1]}<br>' +
                    '<b>Row Variance:</b> %{customdata[2]:.6f}<br>' +
                    '<b>Column Variance:</b> %{customdata[3]:.6f}<br>' +
                    '<b>Diagonal Variance:</b> %{customdata[4]:.6f}<br>' +
                    '<extra></extra>'
                ),
                customdata=np.column_stack((
                    df_random['type'],
                    df_random['square'],
                    df_random['row_var'],
                    df_random['col_var'],
                    df_random['diag_var']
                )).tolist()
            ))
    
    # Update layout with more space for colorbars
    fig.update_layout(
        scene=dict(
            xaxis=dict(title=f'{method.upper()} Component 1'),
            yaxis=dict(title=f'{method.upper()} Component 2'),
            zaxis=dict(title=f'{method.upper()} Component 3'),
            aspectmode='cube'
        ),
        width=1400,  # Increased width to accommodate colorbars
        height=800,
        title=f'4D {method.upper()} Visualization of Magic Square Manifold',
        showlegend=True,
        margin=dict(r=150)  # Add right margin for colorbars
    )

    # Generate HTML with simpler template
    fig_json = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)  # Use Plotly's JSON encoder
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>4D Magic Square Manifold Visualization</title>
        <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
            }}
            #graph {{
                width: 100%;
                height: calc(100vh - 50px);
                min-height: 750px;
            }}
            #controls {{
                position: fixed;
                top: 10px;
                right: 20px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            #colorControls {{
                display: flex;
                flex-direction: column;
                gap: 5px;
            }}
            .colorOption {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .colorOption label {{
                font-size: 14px;
            }}
            button {{
                padding: 8px 16px;
                font-size: 14px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #45a049;
            }}
            button.active {{
                background-color: #2196F3;
            }}
        </style>
    </head>
    <body>
        <div id="controls">
            <button id="rotationMode">3D Rotation Mode</button>
            <div id="colorControls">
                <div class="colorOption">
                    <input type="radio" id="color4d" name="colorScheme" value="4d" checked>
                    <label for="color4d">Color by 4D Value</label>
                </div>
                <div class="colorOption">
                    <input type="radio" id="colorNumber" name="colorScheme" value="number">
                    <label for="colorNumber">Color by Number</label>
                </div>
                <div class="colorOption">
                    <input type="radio" id="colorGroup" name="colorScheme" value="group">
                    <label for="colorGroup">Color by Group</label>
                </div>
                <div class="colorOption">
                    <input type="radio" id="colorVersion" name="colorScheme" value="version">
                    <label for="colorVersion">Color by Version</label>
                </div>
            </div>
        </div>
        <div id="graph"></div>
        <script>
            const plotData = {fig_json};
            
            function updatePlot(colorScheme = '4d') {{
                const update = {{
                    x: [],
                    y: [],
                    z: [],
                    'marker.color': [],
                    'marker.colorscale': []
                }};
                
                plotData.data.forEach(function(trace, i) {{
                    if (i === 0) {{  // Magic squares
                        let colors;
                        switch(colorScheme) {{
                            case 'number':
                                colors = currentPoints[i].map(function(p) {{ return parseInt(p.customdata[7]); }});  // Number
                                break;
                            case 'group':
                                colors = currentPoints[i].map(function(p) {{ return parseInt(p.customdata[5]); }});  // Group
                                break;
                            case 'version':
                                colors = currentPoints[i].map(function(p) {{ return parseInt(p.customdata[6]); }});  // Version
                                break;
                            default:  // '4d'
                                colors = currentPoints[i].map(function(p) {{ return p.coords[3]; }});
                                break;
                        }}
                        
                        update.x.push(currentPoints[i].map(function(p) {{ return p.coords[0]; }}));
                        update.y.push(currentPoints[i].map(function(p) {{ return p.coords[1]; }}));
                        update.z.push(currentPoints[i].map(function(p) {{ return p.coords[2]; }}));
                        update['marker.color'].push(colors);
                        update['marker.colorscale'].push(
                            colorScheme === '4d' ? 'Viridis' : 
                            colorScheme === 'version' ? [
                                [0, '#1f77b4'],     // Version 1
                                [0.143, '#ff7f0e'], // Version 2
                                [0.286, '#2ca02c'], // Version 3
                                [0.429, '#d62728'], // Version 4
                                [0.572, '#9467bd'], // Version 5
                                [0.715, '#8c564b'], // Version 6
                                [0.858, '#e377c2'], // Version 7
                                [1, '#7f7f7f']      // Version 8
                            ] : 'Turbo'  // Use Turbo for Number and Group
                        );
                    }} else {{  // Non-magic and random squares
                        update.x.push(currentPoints[i].map(function(p) {{ return p.coords[0]; }}));
                        update.y.push(currentPoints[i].map(function(p) {{ return p.coords[1]; }}));
                        update.z.push(currentPoints[i].map(function(p) {{ return p.coords[2]; }}));
                        update['marker.color'].push(currentPoints[i].map(function(p) {{ return p.coords[3]; }}));
                        update['marker.colorscale'].push(trace.marker.colorscale);
                    }}
                }});
                
                Plotly.update('graph', update);
            }}
            
            let is4DMode = false;
            let plotDiv;
            let rotationSpeed = 0.1;
            
            // Store original 4D coordinates and metadata
            let originalPoints = [];
            plotData.data.forEach(trace => {{
                const points = [];
                for (let i = 0; i < trace.x.length; i++) {{
                    points.push({{
                        coords: [
                            trace.x[i],
                            trace.y[i],
                            trace.z[i],
                            trace.marker.color[i]
                        ],
                        customdata: trace.customdata ? trace.customdata[i] : null
                    }});
                }}
                originalPoints.push(points);
            }});

            // Current state of rotated points
            let currentPoints = JSON.parse(JSON.stringify(originalPoints));

            // 4D rotation matrices
            function rotateXW(points, angle) {{
                return points.map(p => {{
                    const x = p.coords[0] * Math.cos(angle) - p.coords[3] * Math.sin(angle);
                    const w = p.coords[0] * Math.sin(angle) + p.coords[3] * Math.cos(angle);
                    return {{
                        ...p,
                        coords: [x, p.coords[1], p.coords[2], w]
                    }};
                }});
            }}

            function rotateYW(points, angle) {{
                return points.map(p => {{
                    const y = p.coords[1] * Math.cos(angle) - p.coords[3] * Math.sin(angle);
                    const w = p.coords[1] * Math.sin(angle) + p.coords[3] * Math.cos(angle);
                    return {{
                        ...p,
                        coords: [p.coords[0], y, p.coords[2], w]
                    }};
                }});
            }}

            function rotateZW(points, angle) {{
                return points.map(p => {{
                    const z = p.coords[2] * Math.cos(angle) - p.coords[3] * Math.sin(angle);
                    const w = p.coords[2] * Math.sin(angle) + p.coords[3] * Math.cos(angle);
                    return {{
                        ...p,
                        coords: [p.coords[0], p.coords[1], z, w]
                    }};
                }});
            }}

            function init() {{
                plotDiv = document.getElementById('graph');
                Plotly.newPlot('graph', plotData.data, plotData.layout, {{
                    responsive: true,
                    displayModeBar: true
                }}).then(() => {{
                    console.log("Plot initialized successfully");
                    window.dispatchEvent(new Event('resize'));
                    setupEventListeners();
                }}).catch(err => {{
                    console.error("Error initializing plot:", err);
                }});
            }}

            function setupEventListeners() {{
                const rotationButton = document.getElementById('rotationMode');
                const colorControls = document.querySelectorAll('input[name="colorScheme"]');
                
                rotationButton.addEventListener('click', () => {{
                    is4DMode = !is4DMode;
                    rotationButton.textContent = is4DMode ? '4D Rotation Mode' : '3D Rotation Mode';
                    rotationButton.style.backgroundColor = is4DMode ? '#2196F3' : '#4CAF50';
                    
                    // Reset to original positions when switching modes
                    if (is4DMode) {{
                        currentPoints = JSON.parse(JSON.stringify(originalPoints));
                        updatePlot(document.querySelector('input[name="colorScheme"]:checked').value);
                    }}
                }});

                // Color scheme radio buttons
                colorControls.forEach(radio => {{
                    radio.addEventListener('change', (e) => {{
                        updatePlot(e.target.value);
                    }});
                }});

                // Handle keyboard events for 4D rotation
                document.addEventListener('keydown', function(e) {{
                    if (!is4DMode) return;  // Only handle keys in 4D mode
                    
                    let updated = false;
                    
                    switch(e.key.toLowerCase()) {{
                        case 'a':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateXW(tracePoints, -rotationSpeed));
                            updated = true;
                            break;
                        case 'd':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateXW(tracePoints, rotationSpeed));
                            updated = true;
                            break;
                        case 'w':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateYW(tracePoints, -rotationSpeed));
                            updated = true;
                            break;
                        case 's':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateYW(tracePoints, rotationSpeed));
                            updated = true;
                            break;
                        case 'q':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateZW(tracePoints, -rotationSpeed));
                            updated = true;
                            break;
                        case 'e':
                            currentPoints = currentPoints.map(tracePoints => 
                                rotateZW(tracePoints, rotationSpeed));
                            updated = true;
                            break;
                    }}
                    
                    if (updated) {{
                        updatePlot(document.querySelector('input[name="colorScheme"]:checked').value);
                    }}
                }});
            }}

            window.addEventListener('resize', () => {{
                Plotly.Plots.resize('graph');
            }});

            init();
        </script>
    </body>
    </html>
    '''
    
    with open(f'{save_dir}/interactive_{method}_4d.html', 'w') as f:
        f.write(html_content)
    
    print(f"Interactive 4D visualization saved as '{save_dir}/interactive_{method}_4d.html'")
    
    # 5. Constraint violation visualization
    print("Creating constraint violation visualization...")
    plt.figure(figsize=(12, 8))
    
    # Calculate mean and std of constraint violations for each group
    constraints = ['Row Sum', 'Column Sum', 'Main Diagonal', 'Anti-Diagonal']
    x_pos = np.arange(len(constraints))
    width = 0.15
    
    # Magic squares - take only the first 4 features (covariance constraints)
    magic_mean = np.mean(np.abs(magic_extended_features[:, :4]), axis=0)
    magic_std = np.std(np.abs(magic_extended_features[:, :4]), axis=0)
    
    # Group non-magic squares by level
    unique_levels = sorted(set(levels))
    level_means = []
    level_stds = []
    
    for level in unique_levels:
        level_mask = levels == level
        level_constraints = non_magic_extended_features[level_mask, :4]  # Take only covariance constraints
        level_means.append(np.mean(np.abs(level_constraints), axis=0))
        level_stds.append(np.std(np.abs(level_constraints), axis=0))
    
    level_means = np.array(level_means)
    level_stds = np.array(level_stds)
    
    # Plot bars
    plt.bar(x_pos - (len(unique_levels)/2 + 0.5)*width, magic_mean, width, 
            yerr=magic_std, label='Magic Squares', color='blue', alpha=0.7, capsize=5)
    
    colors = plt.cm.plasma(np.linspace(0, 1, len(unique_levels)))
    for i, level in enumerate(unique_levels):
        plt.bar(x_pos - ((len(unique_levels)/2 - i - 0.5)*width), level_means[i], width,
                yerr=level_stds[i], label=f'Level {level}', color=colors[i], alpha=0.7, capsize=5)
    
    plt.xlabel('Constraint Type')
    plt.ylabel('Absolute Covariance Value')
    plt.title('Constraint Violations by Square Type')
    plt.xticks(x_pos, constraints, rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/constraint_violation.png', dpi=300, bbox_inches='tight')
    
    print(f"Visualizations saved in '{save_dir}' directory.")


def generate_magic_squares(n=100):
    """Load magic squares from the CSV file.
    
    Args:
        n (int): Number of magic squares to return
    
    Returns:
        tuple: (numpy.ndarray of squares, numbers, groups, versions)
    """
    # Load the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all7040CategoriesData.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Could not find magic squares CSV file at {csv_path}")
    
    print(f"\nLoading magic squares from: {csv_path}")
    print("First few rows of the CSV file:")
    
    # Read the CSV file
    data = pd.read_csv(csv_path, sep='\t', header=0)
    print(data.head())
    print("\nColumns in the CSV file:")
    print(data.columns.tolist())
    
    # Convert the data into magic squares
    squares = []
    numbers = []
    groups = []
    versions = []
    
    print("\nExtracting data from first 20 rows:")
    for idx, row in data.iterrows():
        # if idx >= 20:  # Only print first 20 rows for debugging
        #     break
            
        # Extract identification information
        number = row['Nr.']
        group = row['Gr.']
        version = row['Vs.']
        
        print(f"\nRow {idx + 1}:")
        print(f"Number: {number}")
        print(f"Group: {group}")
        print(f"Version: {version}")
        
        # Extract the 16 numbers (skip the first 3 columns which are Nr., Gr., and Vs.)
        square_values = row.iloc[3:19].values
        # Reshape into 4x4 array
        square = square_values.reshape(4, 4)
        
        print("Square values:")
        print(square)
        
        squares.append(square)
        numbers.append(number)
        groups.append(group)
        versions.append(version)
    
    # Print summary statistics
    print("\nSummary of extracted data:")
    print(f"Total number of squares: {len(squares)}")
    print(f"Unique numbers: {np.unique(numbers)}")
    print(f"Unique groups: {np.unique(groups)}")
    print(f"Unique versions: {np.unique(versions)}")
    
    # Print some example combinations
    print("\nExample combinations (first 20):")
    for i in range(min(20, len(squares))):
        print(f"Square {i+1}: Number={numbers[i]}, Group={groups[i]}, Version={versions[i]}")
    
    squares = np.array(squares)
    numbers = np.array(numbers)
    groups = np.array(groups)
    versions = np.array(versions)
    
    # Return requested number of squares, or all if n > len(squares)
    n = min(n, len(squares))
    return squares[:n], numbers[:n], groups[:n], versions[:n]

def generate_non_magic_squares(n=100, perturbation_levels=20, n_random=50):
    """Generate non-magic squares at varying distances from the magic manifold.
    
    Args:
        n (int): Number of perturbed squares to generate
        perturbation_levels (int): Number of perturbation levels
        n_random (int): Number of completely random squares to generate
    """
    non_magic_squares = []
    unique_squares = set()  # Track all unique squares
    
    # Load all available magic squares first
    all_magic_squares, _, _, _ = generate_magic_squares(7040)
    
    # Define multipliers for each level (10x for level 1, 8x for level 2, etc.)
    level_multipliers = {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1
    }
    
    # Calculate base squares per level (without multipliers)
    total_multiplier = sum(level_multipliers.get(i, 1) for i in range(1, perturbation_levels + 1))
    base_squares_per_level = n // total_multiplier
    
    # For each perturbation level
    for level in range(1, perturbation_levels + 1):
        squares_at_level = []
        
        # Apply multiplier for this level
        squares_per_level = base_squares_per_level * level_multipliers.get(level, 1)
        
        print(f"Generating {squares_per_level} squares for level {level}")
        
        attempts = 0
        max_attempts = squares_per_level * 10  # Allow multiple attempts per desired square
        
        while len(squares_at_level) < squares_per_level and attempts < max_attempts:
            # Use a randomly chosen magic square as the base
            base = all_magic_squares[np.random.randint(0, len(all_magic_squares))].copy()
            base_tuple = tuple(base.flatten())
            
            # Track unique starting squares
            if base_tuple not in unique_squares:
                unique_squares.add(base_tuple)
            
            # Create a non-magic square by swapping some elements
            new_square = base.copy()
            swaps_made = 0
            swap_attempts = 0
            max_swap_attempts = 100  # Prevent infinite loops
            swaps_history = []  # Track the swaps we've made
            
            while swaps_made < level and swap_attempts < max_swap_attempts:
                # Pick two different random positions
                pos1 = (np.random.randint(0, 4), np.random.randint(0, 4))
                pos2 = (np.random.randint(0, 4), np.random.randint(0, 4))
                
                # Only swap if:
                # 1. Positions are different
                # 2. Values are different
                # 3. This swap hasn't been made before (or its reverse)
                # 4. The swap won't undo a previous swap
                swap_valid = (
                    pos1 != pos2 and
                    new_square[pos1] != new_square[pos2] and
                    (pos1, pos2) not in swaps_history and
                    (pos2, pos1) not in swaps_history
                )
                
                if swap_valid:
                    # Store the values before swapping
                    val1, val2 = new_square[pos1], new_square[pos2]
                    
                    # Check if this swap would undo a previous swap
                    would_undo_previous = False
                    temp_square = new_square.copy()
                    temp_square[pos1], temp_square[pos2] = temp_square[pos2].copy(), temp_square[pos1].copy()
                    temp_tuple = tuple(temp_square.flatten())
                    
                    if temp_tuple in unique_squares:
                        would_undo_previous = True
                    
                    if not would_undo_previous:
                        # Perform the swap
                        new_square[pos1], new_square[pos2] = new_square[pos2].copy(), new_square[pos1].copy()
                        swaps_made += 1
                        swaps_history.append((pos1, pos2))
                        print(f"Level {level} - Swap {swaps_made}: {pos1}{val1} ↔ {pos2}{val2}")
                
                swap_attempts += 1
            
            if swaps_made == level:  # Only add if we made all required swaps
                new_square_tuple = tuple(new_square.flatten())
                if new_square_tuple not in unique_squares:  # Check for uniqueness
                    squares_at_level.append((level, new_square))
                    unique_squares.add(new_square_tuple)
            
            attempts += 1
        
        if len(squares_at_level) < squares_per_level:
            print(f"Warning: Could only generate {len(squares_at_level)} unique squares at level {level}")
        
        non_magic_squares.extend(squares_at_level)
    
    # Generate completely random arrangements
    print(f"\nGenerating {n_random} completely random arrangements...")
    random_attempts = 0
    max_random_attempts = n_random * 10
    random_squares = []
    accidental_magic_count = 0
    
    while len(random_squares) < n_random and random_attempts < max_random_attempts:
        numbers = np.arange(1, 17)
        np.random.shuffle(numbers)
        square = numbers.reshape(4, 4)
        square_tuple = tuple(square.flatten())
        
        # Only add if it's unique and not a magic square
        if square_tuple not in unique_squares and not is_magic_square(square):
            random_squares.append((perturbation_levels + 1, square))
            unique_squares.add(square_tuple)
        elif is_magic_square(square):
            print("\nFound accidental magic square in random arrangement:")
            print(square)
            print("\nRow sums:", np.sum(square, axis=1))
            print("Column sums:", np.sum(square, axis=0))
            print("Main diagonal sum:", np.trace(square))
            print("Anti-diagonal sum:", np.trace(np.fliplr(square)))
            accidental_magic_count += 1
        
        random_attempts += 1
    
    if len(random_squares) < n_random:
        print(f"Warning: Could only generate {len(random_squares)} unique random squares")
    
    if accidental_magic_count > 0:
        print(f"\nFound {accidental_magic_count} accidental magic squares in random arrangements!")
    else:
        print("No accidental magic squares found in random arrangements.")
    
    # Add random squares to the result
    non_magic_squares.extend(random_squares)
    
    print(f"\nGenerated squares by level:")
    level_counts = {}
    for level, _ in non_magic_squares:
        level_counts[level] = level_counts.get(level, 0) + 1
    for level in sorted(level_counts.keys()):
        print(f"Level {level}: {level_counts[level]} squares")
    
    return non_magic_squares

def create_axial_points(square):
    """Create 3D points from a square arrangement using the axial representation."""
    n = square.shape[0]
    points = []
    
    for i in range(n):
        for j in range(n):
            point = np.array([
                i - (n-1)/2,  # x-coordinate (row-based)
                j - (n-1)/2,  # y-coordinate (column-based)
                square[i, j] - np.mean(square)  # z-coordinate (value-based)
            ])
            points.append(point)
    
    return np.array(points)

def flatten_square(square):
    """Flatten a square to a 1D array."""
    return square.flatten()

def compute_covariance_constraints(square):
    """Compute the four covariance constraints for a square."""
    points = create_axial_points(square)
    
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    # Create diagonal projections
    main_diag_proj = (x + y) / np.sqrt(2)
    anti_diag_proj = (x - y) / np.sqrt(2)
    
    # Compute covariances
    cov_x_z = np.cov(x, z)[0, 1]
    cov_y_z = np.cov(y, z)[0, 1]
    cov_main_diag = np.cov(main_diag_proj, z)[0, 1]
    cov_anti_diag = np.cov(anti_diag_proj, z)[0, 1]
    
    return np.array([cov_x_z, cov_y_z, cov_main_diag, cov_anti_diag])

def compute_distance_to_manifold(square):
    """Compute distance to the magic square manifold."""
    # For a magic square, all four covariances should be zero
    # So we can measure the distance as the Euclidean norm of the covariances
    covs = compute_covariance_constraints(square)
    return np.linalg.norm(covs)

def is_magic_square(square):
    """Check if a square is a magic square."""
    n = len(square)
    target_sum = n * (n**2 + 1) / 2  # Magic constant for n×n square
    
    # Check rows
    if not all(abs(sum(row) - target_sum) < 1e-10 for row in square):
        return False
    
    # Check columns
    if not all(abs(sum(square[:, i]) - target_sum) < 1e-10 for i in range(n)):
        return False
    
    # Check main diagonal
    if abs(sum(square[i, i] for i in range(n)) - target_sum) >= 1e-10:
        return False
    
    # Check anti-diagonal
    if abs(sum(square[i, n-1-i] for i in range(n)) - target_sum) >= 1e-10:
        return False
    
    # Check if all numbers 1 to n^2 are present
    if not all(i in square for i in range(1, n*n + 1)):
        return False
    
    return True


if __name__ == '__main__':
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Run both UMAP and t-SNE visualizations in 3D and 4D
    print("\nGenerating 3D visualization...")
    visualize_magic_square_manifold(method='tsne', dimensions=3)
    # print("\nGenerating 4D visualization...")
    # visualize_magic_square_manifold(method='tsne', dimensions=4)
    print("Magic square manifold visualization complete!") 