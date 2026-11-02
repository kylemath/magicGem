import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import core functions
from magic_squares.src.analysis.core import reduce_to_unique, find_unique_squares

def square_to_points(square):
    """Convert a magic square to a set of 3D points."""
    n = square.shape[0]
    points = []
    for i in range(n):
        for j in range(n):
            points.append([i, j, square[i, j]])
    return np.array(points)

def classify_points(points, hull, tolerance=1e-10):
    """Classify points as vertices, face points, or interior points."""
    vertex_points = []
    face_points = []
    interior_points = []
    
    # Get hull vertices
    vertices = points[hull.vertices]
    vertex_indices = set(hull.vertices)
    
    # Get equations for each face
    equations = hull.equations
    
    # Classify each point
    for i, point in enumerate(points):
        if i in vertex_indices:
            vertex_points.append(point)
            continue
        
        # Check if point lies on any face
        on_face = False
        for eq in equations:
            # Equation is in form: ax + by + cz + d = 0
            dist = np.abs(np.dot(eq[:-1], point) + eq[-1])
            if dist < tolerance:
                on_face = True
                break
        
        if on_face:
            face_points.append(point)
        else:
            interior_points.append(point)
    
    return (np.array(vertex_points), 
            np.array(face_points) if face_points else np.empty((0, 3)), 
            np.array(interior_points) if interior_points else np.empty((0, 3)))

def compute_angular_uniformity(points):
    """Compute angular uniformity of points."""
    # Center the points
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    
    # Convert to spherical coordinates (ignore radius)
    xy = centered_points[:, 0]**2 + centered_points[:, 1]**2
    theta = np.arctan2(centered_points[:, 1], centered_points[:, 0])
    phi = np.arctan2(np.sqrt(xy), centered_points[:, 2])
    
    # Compute angular dispersion
    theta_std = np.std(theta)
    phi_std = np.std(phi)
    
    # Normalize to [0, 1] where 1 is perfectly uniform
    max_std = np.pi  # Maximum possible standard deviation
    theta_uniformity = 1 - (theta_std / max_std)
    phi_uniformity = 1 - (phi_std / max_std)
    
    # Return average uniformity
    return (theta_uniformity + phi_uniformity) / 2

def compute_all_features(square: np.ndarray) -> Dict[str, Any]:
    """
    Compute comprehensive features for a single magic square.
    
    Parameters:
    -----------
    square : np.ndarray
        4x4 magic square array
        
    Returns:
    --------
    Dict[str, Any]
        Dictionary containing all computed features
    """
    features = {}
    
    # 1. Basic square properties
    features['magic_sum'] = np.sum(square[0, :])  # Should be same for all rows/cols/diags
    features['mean'] = np.mean(square)
    features['std'] = np.std(square)
    
    # 2. Row/Column/Diagonal statistics
    features['row_sums_std'] = np.std([np.sum(row) for row in square])
    features['col_sums_std'] = np.std([np.sum(square[:, i]) for i in range(square.shape[1])])
    features['main_diag_sum'] = np.trace(square)
    features['anti_diag_sum'] = np.trace(np.fliplr(square))
    
    # 3. Geometric embedding features
    points = square_to_points(square)
    try:
        hull = ConvexHull(points)
        
        # 3.1 Basic hull properties
        features['hull_volume'] = hull.volume
        features['hull_area'] = hull.area
        features['hull_density'] = len(points) / hull.volume if hull.volume > 0 else 0
        features['area_volume_ratio'] = hull.area / hull.volume if hull.volume > 0 else 0
        
        # 3.2 Point classification
        vertex_points, face_points, interior_points = classify_points(points, hull)
        features['n_vertices'] = len(vertex_points)
        features['n_face_points'] = len(face_points)
        features['n_interior_points'] = len(interior_points)
        features['vertex_ratio'] = len(vertex_points) / len(points)
        features['face_ratio'] = len(face_points) / len(points)
        features['interior_ratio'] = len(interior_points) / len(points)
        
        # 3.3 Angular uniformity
        features['angular_uniformity'] = compute_angular_uniformity(points)
        
        # 3.4 Eigenvalue analysis
        # Compute covariance matrix
        centered_points = points - np.mean(points, axis=0)
        cov_matrix = np.cov(centered_points.T)
        eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
        
        # Sort eigenvalues in descending order
        idx = eigenvals.argsort()[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        features['eigenvalue_1'] = eigenvals[0]
        features['eigenvalue_2'] = eigenvals[1]
        features['eigenvalue_3'] = eigenvals[2]
        features['eigenvalue_ratio_21'] = eigenvals[1] / eigenvals[0] if eigenvals[0] != 0 else 0
        features['eigenvalue_ratio_32'] = eigenvals[2] / eigenvals[1] if eigenvals[1] != 0 else 0
        features['eigenvalue_ratio_31'] = eigenvals[2] / eigenvals[0] if eigenvals[0] != 0 else 0
        
        # 3.5 Hull shape analysis
        features['aspect_ratio_21'] = np.sqrt(eigenvals[1] / eigenvals[0]) if eigenvals[0] != 0 else 0
        features['aspect_ratio_31'] = np.sqrt(eigenvals[2] / eigenvals[0]) if eigenvals[0] != 0 else 0
            
        # 3.6 Spatial distribution
        centroid = np.mean(points, axis=0)
        dists_to_centroid = np.linalg.norm(points - centroid, axis=1)
        features['mean_dist_to_centroid'] = np.mean(dists_to_centroid)
        features['std_dist_to_centroid'] = np.std(dists_to_centroid)
        features['max_dist_to_centroid'] = np.max(dists_to_centroid)
        
        # 3.7 Face analysis
        if hasattr(hull, 'equations'):
            features['n_faces'] = len(hull.equations)
            face_areas = []
            for simplex in hull.simplices:
                pts = points[simplex]
                # Compute face area using cross product
                v1 = pts[1] - pts[0]
                v2 = pts[2] - pts[0]
                face_area = np.linalg.norm(np.cross(v1, v2)) / 2
                face_areas.append(face_area)
            features['mean_face_area'] = np.mean(face_areas)
            features['std_face_area'] = np.std(face_areas)
            features['face_area_ratio'] = np.std(face_areas) / np.mean(face_areas) if np.mean(face_areas) > 0 else 0
        
        # 3.8 Compactness measures
        features['sphericity'] = (36 * np.pi * hull.volume**2)**(1/3) / hull.area if hull.area > 0 else 0
        
    except Exception as e:
        print(f"Warning: Error computing geometric features: {str(e)}")
        # Fill geometric features with NaN
        geometric_features = [
            'hull_volume', 'hull_area', 'hull_density', 'area_volume_ratio',
            'n_vertices', 'n_face_points', 'n_interior_points',
            'vertex_ratio', 'face_ratio', 'interior_ratio',
            'angular_uniformity',
            'eigenvalue_1', 'eigenvalue_2', 'eigenvalue_3',
            'eigenvalue_ratio_21', 'eigenvalue_ratio_32', 'eigenvalue_ratio_31',
            'aspect_ratio_21', 'aspect_ratio_31',
            'mean_dist_to_centroid', 'std_dist_to_centroid', 'max_dist_to_centroid',
            'n_faces', 'mean_face_area', 'std_face_area', 'face_area_ratio',
            'sphericity'
        ]
        for feat in geometric_features:
            features[feat] = np.nan
    
    # 4. 2x2 subsquare analysis
    subsquare_sums = []
    for i in range(3):
        for j in range(3):
            subsquare = square[i:i+2, j:j+2]
            subsquare_sums.append(np.sum(subsquare))
    features['subsquare_sum_mean'] = np.mean(subsquare_sums)
    features['subsquare_sum_std'] = np.std(subsquare_sums)
    features['subsquare_sum_range'] = np.max(subsquare_sums) - np.min(subsquare_sums)
    
    # 5. Local structure analysis
    # 5.1 Local gradients
    gradients = []
    for i in range(square.shape[0]):
        for j in range(square.shape[1]):
            neighbors = []
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < square.shape[0] and 0 <= nj < square.shape[1]:
                    neighbors.append(square[ni, nj])
            if neighbors:
                gradients.append(np.mean(np.abs(square[i,j] - np.array(neighbors))))
    
    features['mean_local_gradient'] = np.mean(gradients)
    features['std_local_gradient'] = np.std(gradients)
    
    return features

def analyze_all_squares(squares: List[np.ndarray], output_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Analyze all magic squares and compute their features.
    
    Parameters:
    -----------
    squares : List[np.ndarray]
        List of magic squares to analyze
    output_dir : str, optional
        Directory to save results
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing all computed features for all squares
    """
    print(f"\nAnalyzing {len(squares)} magic squares...")
    
    # First find the unique squares
    print("\nIdentifying unique squares...")
    unique_squares = find_unique_squares(squares)
    unique_squares_set = {str(square.tolist()) for square in unique_squares}
    print(f"Found {len(unique_squares)} unique squares")
    
    # Compute features for all squares
    all_features = []
    for i, square in enumerate(squares):
        if i % 100 == 0:
            print(f"Processing square {i+1}/{len(squares)}...")
        features = compute_all_features(square)
        
        # Add square ID and square itself first
        features_ordered = {
            'square_id': i,
            'square': str(square.tolist()),
            'is_unique': str(square.tolist()) in unique_squares_set
        }
        # Add all other features
        features_ordered.update(features)
        
        all_features.append(features_ordered)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_features)
    
    # Save results if output directory is provided
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f'magic_square_features_{timestamp}.csv')
        df.to_csv(filename, index=False)
        print(f"\nSaved features to {filename}")
        
        # Also save summary statistics
        summary_file = os.path.join(output_dir, f'feature_summary_{timestamp}.txt')
        with open(summary_file, 'w') as f:
            f.write("Magic Square Feature Analysis Summary\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Number of squares analyzed: {len(squares)}\n")
            f.write(f"Number of unique squares: {len(unique_squares)} ({len(unique_squares)/len(squares)*100:.1f}%)\n\n")
            f.write("Feature Statistics:\n")
            f.write("-" * 20 + "\n\n")
            stats = df.describe()
            f.write(stats.to_string())
            
        print(f"Saved summary statistics to {summary_file}")
    
    return df

if __name__ == '__main__':
    # Load all magic squares from the dataset
    try:
        # Try loading from magic_squares directory first
        squares_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'magic_squares', 'src', 'analysis', 'cache', 'magic_squares_20241031_133039.npy'
        )
        if os.path.exists(squares_path):
            squares = np.load(squares_path)
            print(f"Loaded {len(squares)} squares from {squares_path}")
        else:
            # Try alternative paths
            alt_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../../magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy'
            )
            if os.path.exists(alt_path):
                squares = np.load(alt_path)
                print(f"Loaded {len(squares)} squares from {alt_path}")
            else:
                raise FileNotFoundError("Could not find magic squares dataset")
    except Exception as e:
        print(f"Error loading squares: {str(e)}")
        print("Using sample square for testing...")
        # Use sample square if loading fails
        squares = [np.array([
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1]
        ])]
    
    # Set output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'features')
    
    # Analyze squares
    df = analyze_all_squares(squares, output_dir)
    
    # Print summary
    print("\nFeature Summary:")
    print(df.describe()) 