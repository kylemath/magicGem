import numpy as np
from scipy.spatial import ConvexHull
import ot  # Make sure POT is installed: pip install POT
import numba  # Make sure numba is installed: pip install numba
import pandas as pd

def square_to_points(square):
    """
    Convert a magic square to a set of 3D points.
    
    Parameters:
    -----------
    square : ndarray
        A magic square array
        
    Returns:
    --------
    ndarray
        Array of 3D points (i, j, value)
    """
    n = square.shape[0]
    points = []
    for i in range(n):
        for j in range(n):
            points.append([i, j, square[i, j]])
    return np.array(points)

def classify_points(points, hull, tolerance=1e-10):
    """
    Classify points as vertices, face points, or interior points.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    hull : ConvexHull
        Convex hull of the points
    tolerance : float
        Tolerance for numerical comparisons
        
    Returns:
    --------
    tuple
        (vertex_points, face_points, interior_points)
    """
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
    """
    Compute the angular uniformity of a set of 3D points.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
        
    Returns:
    --------
    float
        Angular uniformity measure (0 to 1)
    """
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

def compute_eigenvalue_ratios(squares):
    """
    Compute eigenvalue ratios for each magic square.
    
    Parameters:
    -----------
    squares : ndarray
        Array of magic squares
        
    Returns:
    --------
    dict
        Dictionary containing eigenvalue ratios
    """
    ratios = {
        'lambda2_lambda1': [],
        'lambda3_lambda2': [],
        'lambda3_lambda1': []
    }
    
    for square in squares:
        # Convert to point cloud
        points = square_to_points(square)
        
        # Center the points
        centroid = np.mean(points, axis=0)
        centered_points = points - centroid
        
        # Compute covariance matrix
        cov_matrix = np.cov(centered_points.T)
        
        # Compute eigenvalues
        eigenvals = np.linalg.eigvals(cov_matrix)
        eigenvals = np.sort(np.abs(eigenvals))[::-1]  # Sort in descending order
        
        # Compute ratios (handle potential division by zero)
        if eigenvals[0] != 0:
            ratios['lambda2_lambda1'].append(eigenvals[1] / eigenvals[0])
        else:
            ratios['lambda2_lambda1'].append(np.nan)
            
        if eigenvals[1] != 0:
            ratios['lambda3_lambda2'].append(eigenvals[2] / eigenvals[1])
        else:
            ratios['lambda3_lambda2'].append(np.nan)
            
        if eigenvals[0] != 0:
            ratios['lambda3_lambda1'].append(eigenvals[2] / eigenvals[0])
        else:
            ratios['lambda3_lambda1'].append(np.nan)
    
    return ratios

def compute_square_geometry(square):
    """
    Compute geometric properties of a magic square.
    
    Parameters:
    -----------
    square : ndarray
        A magic square array
        
    Returns:
    --------
    dict
        Dictionary containing geometric properties
    """
    # Convert to point cloud
    points = square_to_points(square)
    
    try:
        # Compute convex hull
        hull = ConvexHull(points)
        
        # Store hull vertices and simplices directly
        hull_vertices = points[hull.vertices]
        hull_faces = [points[simplex] for simplex in hull.simplices]
        
        # Center the points
        centroid = np.mean(points, axis=0)
        centered_points = points - centroid
        
        # Compute covariance matrix and eigendecomposition
        cov_matrix = np.cov(centered_points.T)
        eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
        
        # Sort eigenvalues and eigenvectors in descending order
        idx = eigenvals.argsort()[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        return {
            'points': points,
            'hull_vertices': hull_vertices,
            'hull_faces': hull_faces,
            'hull_volume': hull.volume,
            'hull_area': hull.area,
            'cov_matrix': cov_matrix,
            'eigenvalues': eigenvals,
            'eigenvectors': eigenvecs
        }
    except Exception as e:
        print(f"Error computing geometry: {str(e)}")
        return None

def point_on_face(point, face_points, tolerance=1e-10):
    """Check if a point lies on a triangular face"""
    # Calculate normal vector of the face
    v1 = face_points[1] - face_points[0]
    v2 = face_points[2] - face_points[0]
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)
    
    # Check if point lies on the plane of the face
    v = point - face_points[0]
    dist_to_plane = abs(np.dot(v, normal))
    if dist_to_plane > tolerance:
        return False
    
    # Check if point is within the triangle
    # Using barycentric coordinates
    def same_side(p1, p2, a, b):
        cp1 = np.cross(b-a, p1-a)
        cp2 = np.cross(b-a, p2-a)
        return np.dot(cp1, cp2) >= 0
    
    return (same_side(point, face_points[0], face_points[1], face_points[2]) and
            same_side(point, face_points[1], face_points[0], face_points[2]) and
            same_side(point, face_points[2], face_points[0], face_points[1]))

def categorize_points(geo):
    """Categorize points as vertices, face points, or interior points"""
    points = geo['points']
    hull_vertices = geo['hull_vertices']
    faces = geo['hull_faces']
    
    vertex_points = []
    face_points = []
    interior_points = []
    
    for point in points:
        if any(np.allclose(point, vertex) for vertex in hull_vertices):
            vertex_points.append(point)
        else:
            # Check if point lies on any face
            on_face = False
            for face in faces:
                if point_on_face(point, face, tolerance=1e-10):
                    on_face = True
                    break
            if on_face:
                face_points.append(point)
            else:
                interior_points.append(point)
    
    return {
        'vertex_points': np.array(vertex_points) if vertex_points else np.empty((0, 3)),
        'face_points': np.array(face_points) if face_points else np.empty((0, 3)),
        'interior_points': np.array(interior_points) if interior_points else np.empty((0, 3))
    }

def analyze_patterns(squares):
    """
    Analyze point distribution patterns in magic squares.
    
    Parameters:
    -----------
    squares : list
        List of magic squares to analyze
        
    Returns:
    --------
    dict
        Dictionary containing pattern analysis results
    """
    # Initialize pattern counters
    patterns = {}
    total_squares = len(squares)
    
    # Process each square
    for i, square in enumerate(squares):
        if i % 100 == 0:
            print(f"Processing square {i+1}/{total_squares}...")
            
        # Compute geometry
        geo = compute_square_geometry(square)
        if geo is None:
            continue
            
        # Get point categories using categorize_points
        point_categories = categorize_points(geo)
        vertex_points = point_categories['vertex_points']
        face_points = point_categories['face_points']
        interior_points = point_categories['interior_points']
        
        # Create pattern key
        pattern = (len(vertex_points), len(face_points), len(interior_points))
        
        # Update pattern count
        if pattern in patterns:
            patterns[pattern]['count'] += 1
            patterns[pattern]['squares'].append(square)
        else:
            patterns[pattern] = {
                'count': 1,
                'squares': [square],
                'vertices': len(vertex_points),
                'faces': len(face_points),
                'interior': len(interior_points)
            }
    
    # Convert to list and sort by frequency
    pattern_list = []
    for pattern, data in patterns.items():
        pattern_list.append({
            'pattern': pattern,
            'count': data['count'],
            'frequency': data['count'] / total_squares,
            'vertices': data['vertices'],
            'faces': data['faces'],
            'interior': data['interior'],
            'example_square': data['squares'][0]
        })
    
    pattern_list.sort(key=lambda x: x['count'], reverse=True)
    
    return {
        'total_squares': total_squares,
        'unique_patterns': len(patterns),
        'patterns': pattern_list
    }

def compute_geometric_comparison(standard_squares, most_perfect_squares):
    """
    Compare geometric properties between standard and most-perfect magic squares.
    
    Parameters:
    -----------
    standard_squares : list
        List of standard magic squares
    most_perfect_squares : list
        List of most-perfect magic squares
        
    Returns:
    --------
    dict
        Dictionary containing comparison results
    """
    # Compute geometric properties
    standard_geometries = [compute_square_geometry(square) for square in standard_squares]
    most_perfect_geometries = [compute_square_geometry(square) for square in most_perfect_squares]
    
    # Filter out None values
    standard_geometries = [geo for geo in standard_geometries if geo is not None]
    most_perfect_geometries = [geo for geo in most_perfect_geometries if geo is not None]
    
    # Get point categories
    standard_point_categories = []
    for geo in standard_geometries:
        vertex_points, face_points, interior_points = classify_points(geo['points'], geo['hull'])
        standard_point_categories.append({
            'vertex_points': vertex_points,
            'face_points': face_points,
            'interior_points': interior_points
        })
    
    most_perfect_point_categories = []
    for geo in most_perfect_geometries:
        vertex_points, face_points, interior_points = classify_points(geo['points'], geo['hull'])
        most_perfect_point_categories.append({
            'vertex_points': vertex_points,
            'face_points': face_points,
            'interior_points': interior_points
        })
    
    # Compute statistics
    standard_stats = {
        'vertices': np.mean([len(cats['vertex_points']) for cats in standard_point_categories]),
        'faces': np.mean([len(cats['face_points']) for cats in standard_point_categories]),
        'interior': np.mean([len(cats['interior_points']) for cats in standard_point_categories]),
        'volume': np.mean([geo['hull_volume'] for geo in standard_geometries]),
        'area': np.mean([geo['hull_area'] for geo in standard_geometries])
    }
    
    most_perfect_stats = {
        'vertices': np.mean([len(cats['vertex_points']) for cats in most_perfect_point_categories]),
        'faces': np.mean([len(cats['face_points']) for cats in most_perfect_point_categories]),
        'interior': np.mean([len(cats['interior_points']) for cats in most_perfect_point_categories]),
        'volume': np.mean([geo['hull_volume'] for geo in most_perfect_geometries]),
        'area': np.mean([geo['hull_area'] for geo in most_perfect_geometries])
    }
    
    return {
        'standard': standard_stats,
        'most_perfect': most_perfect_stats,
        'standard_raw': {
            'geometries': standard_geometries,
            'point_categories': standard_point_categories
        },
        'most_perfect_raw': {
            'geometries': most_perfect_geometries,
            'point_categories': most_perfect_point_categories
        }
    }

def compute_emd_between_square_types(standard_squares, most_perfect_squares, n_samples=10):
    """
    Compute Earth Mover's Distance between standard and most-perfect magic squares.
    
    Parameters:
    -----------
    standard_squares : list of numpy.ndarray
        List of standard 4×4 magic squares
    most_perfect_squares : list of numpy.ndarray
        List of most-perfect 4×4 magic squares
    n_samples : int
        Number of squares to sample from each type for comparison
        
    Returns:
    --------
    dict
        Dictionary containing EMD statistics
    """
    # Sample squares if there are too many
    if len(standard_squares) > n_samples:
        standard_sample = np.random.choice(len(standard_squares), n_samples, replace=False)
        standard_squares_sample = [standard_squares[i] for i in standard_sample]
    else:
        standard_squares_sample = standard_squares
    
    if len(most_perfect_squares) > n_samples:
        most_perfect_sample = np.random.choice(len(most_perfect_squares), n_samples, replace=False)
        most_perfect_squares_sample = [most_perfect_squares[i] for i in most_perfect_sample]
    else:
        most_perfect_squares_sample = most_perfect_squares
    
    # Compute EMD between all pairs
    emd_values = []
    
    for std_square in standard_squares_sample:
        for mp_square in most_perfect_squares_sample:
            # Flatten squares to 1D distributions
            a = std_square.flatten() / np.sum(std_square)  # Normalize
            b = mp_square.flatten() / np.sum(mp_square)    # Normalize
            
            # Create cost matrix based on value differences
            n = len(a)
            cost_matrix = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    cost_matrix[i, j] = abs(a[i] - b[j])
            
            # Compute EMD
            emd = ot.emd2(a, b, cost_matrix)
            emd_values.append(emd)
    
    # Compute statistics
    emd_stats = {
        'mean': np.mean(emd_values),
        'std': np.std(emd_values),
        'min': np.min(emd_values),
        'max': np.max(emd_values),
        'median': np.median(emd_values),
        'values': emd_values
    }
    
    return emd_stats

def identify_distinctive_geometric_features(standard_squares, most_perfect_squares):
    """
    Identify the most distinctive geometric features that differentiate 
    standard magic squares from most-perfect magic squares.
    
    Parameters:
    -----------
    standard_squares : list of numpy.ndarray
        List of standard 4×4 magic squares
    most_perfect_squares : list of numpy.ndarray
        List of most-perfect 4×4 magic squares
        
    Returns:
    --------
    dict
        Dictionary containing the most distinctive features and their statistics
    """
    # Compute all geometric properties
    comparison = compute_geometric_comparison(standard_squares, most_perfect_squares)
    
    # Calculate effect sizes for each feature to identify the most distinctive ones
    distinctive_features = {}
    
    # Helper function to calculate Cohen's d effect size
    def cohens_d(mean1, std1, mean2, std2):
        # Pooled standard deviation
        pooled_std = np.sqrt(((std1 ** 2) + (std2 ** 2)) / 2)
        # Effect size
        return abs(mean1 - mean2) / pooled_std if pooled_std > 0 else 0
    
    # Calculate effect sizes for hull volume
    vol_effect = cohens_d(
        comparison['hull_volume']['standard']['mean'],
        comparison['hull_volume']['standard']['std'],
        comparison['hull_volume']['most_perfect']['mean'],
        comparison['hull_volume']['most_perfect']['std']
    )
    distinctive_features['hull_volume'] = {
        'effect_size': vol_effect,
        'standard_mean': comparison['hull_volume']['standard']['mean'],
        'most_perfect_mean': comparison['hull_volume']['most_perfect']['mean']
    }
    
    # Calculate effect sizes for hull area
    area_effect = cohens_d(
        comparison['hull_area']['standard']['mean'],
        comparison['hull_area']['standard']['std'],
        comparison['hull_area']['most_perfect']['mean'],
        comparison['hull_area']['most_perfect']['std']
    )
    distinctive_features['hull_area'] = {
        'effect_size': area_effect,
        'standard_mean': comparison['hull_area']['standard']['mean'],
        'most_perfect_mean': comparison['hull_area']['most_perfect']['mean']
    }
    
    # Calculate effect sizes for compactness
    compactness_effect = cohens_d(
        comparison['compactness']['standard']['mean'],
        comparison['compactness']['standard']['std'],
        comparison['compactness']['most_perfect']['mean'],
        comparison['compactness']['most_perfect']['std']
    )
    distinctive_features['compactness'] = {
        'effect_size': compactness_effect,
        'standard_mean': comparison['compactness']['standard']['mean'],
        'most_perfect_mean': comparison['compactness']['most_perfect']['mean']
    }
    
    # Calculate effect sizes for point distribution
    for point_type in ['vertices', 'face_points', 'interior_points']:
        effect = cohens_d(
            comparison['point_distribution']['standard'][point_type]['mean'],
            comparison['point_distribution']['standard'][point_type]['std'],
            comparison['point_distribution']['most_perfect'][point_type]['mean'],
            comparison['point_distribution']['most_perfect'][point_type]['std']
        )
        distinctive_features[f'point_distribution_{point_type}'] = {
            'effect_size': effect,
            'standard_mean': comparison['point_distribution']['standard'][point_type]['mean'],
            'most_perfect_mean': comparison['point_distribution']['most_perfect'][point_type]['mean']
        }
    
    # Sort features by effect size
    sorted_features = sorted(
        distinctive_features.items(), 
        key=lambda x: x[1]['effect_size'], 
        reverse=True
    )
    
    # Return the top distinctive features
    return {
        'most_distinctive': sorted_features[0][0] if sorted_features else None,
        'all_features': dict(sorted_features),
        'raw_comparison': comparison
    }

@numba.jit(nopython=True)
def _compute_cost_matrix(points1, points2):
    """
    Compute the cost matrix between two sets of points.
    
    Parameters:
    -----------
    points1 : ndarray
        First set of points with shape (n_points, 3)
    points2 : ndarray
        Second set of points with shape (n_points, 3)
        
    Returns:
    --------
    ndarray
        Cost matrix with shape (n_points, n_points)
    """
    n_points = points1.shape[0]
    cost_matrix = np.zeros((n_points, n_points))
    
    for i in range(n_points):
        for j in range(n_points):
            # Compute Euclidean distance between points
            diff = 0.0
            for k in range(3):  # 3D points
                diff += (points1[i, k] - points2[j, k])**2
            cost_matrix[i, j] = np.sqrt(diff)
    
    return cost_matrix

def compute_optimized_emd(square1, square2):
    """
    Compute Earth Mover's Distance between two magic squares.
    
    Parameters:
    -----------
    square1 : numpy.ndarray
        First magic square (already normalized)
    square2 : numpy.ndarray
        Second magic square (already normalized)
        
    Returns:
    --------
    float
        EMD value
    """
    n = square1.shape[0]
    n_points = n * n
    
    # Convert squares to point clouds
    points1 = np.column_stack((np.repeat(np.arange(n), n), 
                             np.tile(np.arange(n), n),
                             square1.flatten()))
    points2 = np.column_stack((np.repeat(np.arange(n), n),
                             np.tile(np.arange(n), n),
                             square2.flatten()))
    
    # Compute cost matrix
    cost_matrix = _compute_cost_matrix(points1, points2)
    
    # Equal weights for each point
    weights = np.ones(n_points) / n_points
    
    # Compute EMD
    return float(ot.emd2(weights, weights, cost_matrix))

def compute_multiscale_emd(square1, square2, scales=[1, 2, 4]):
    """
    Compute EMD between two squares at multiple scales.
    
    Parameters:
    -----------
    square1 : numpy.ndarray
        First magic square (already normalized)
    square2 : numpy.ndarray
        Second magic square (already normalized)
    scales : list
        List of scales to compute EMD at
        
    Returns:
    --------
    dict
        Dictionary containing EMD values at each scale
    """
    results = {}
    
    for scale in scales:
        # Downsample squares
        a = downsample_square(square1, scale)
        b = downsample_square(square2, scale)
        
        # Convert squares to point clouds
        n = a.shape[0]
        n_points = n * n
        points1 = np.column_stack((np.repeat(np.arange(n), n), 
                                 np.tile(np.arange(n), n),
                                 a.flatten()))
        points2 = np.column_stack((np.repeat(np.arange(n), n),
                                 np.tile(np.arange(n), n),
                                 b.flatten()))
        
        # Compute cost matrix
        cost_matrix = _compute_cost_matrix(points1, points2)
        
        # Equal weights for each point
        weights = np.ones(n_points) / n_points
        
        # Compute EMD
        results[scale] = float(ot.emd2(weights, weights, cost_matrix))
    
    return results

def compute_emd_matrix(squares, optimized=True, n_samples=None):
    """
    Compute Earth Mover's Distance matrix between all pairs of magic squares.
    
    Parameters:
    -----------
    squares : list of numpy.ndarray
        List of magic squares
    optimized : bool
        Whether to use optimized EMD computation
    n_samples : int or None
        Number of squares to sample (None = use all)
        
    Returns:
    --------
    tuple
        (distance_matrix, indices) where:
        - distance_matrix: numpy.ndarray of pairwise distances
        - indices: list of indices of sampled squares
    """
    # Sample squares if requested
    if n_samples is not None and n_samples < len(squares):
        indices = np.random.choice(len(squares), n_samples, replace=False)
        sampled_squares = [squares[i] for i in indices]
    else:
        sampled_squares = squares
        indices = np.arange(len(squares))
    
    n = len(sampled_squares)
    distance_matrix = np.zeros((n, n))
    
    # Choose EMD function based on optimization flag
    emd_func = compute_optimized_emd if optimized else lambda s1, s2: ot.emd2(
        s1.flatten() / np.sum(s1.flatten()),
        s2.flatten() / np.sum(s2.flatten()),
        _compute_cost_matrix(s1.flatten() / np.sum(s1.flatten()), 
                            s2.flatten() / np.sum(s2.flatten()))
    )
    
    # Compute distances
    for i in range(n):
        for j in range(i+1, n):
            distance = emd_func(sampled_squares[i], sampled_squares[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # Symmetric
    
    return distance_matrix, indices

def downsample_square(square, scale):
    """
    Downsample a square by averaging blocks of size scale x scale.
    
    Parameters:
    -----------
    square : numpy.ndarray
        Input square to downsample
    scale : int
        Scale factor for downsampling
        
    Returns:
    --------
    numpy.ndarray
        Downsampled square
    """
    n = square.shape[0]
    if scale == 1:
        return square
    
    # Ensure scale divides n evenly
    if n % scale != 0:
        raise ValueError(f"Scale {scale} must divide square size {n} evenly")
    
    new_n = n // scale
    result = np.zeros((new_n, new_n))
    
    for i in range(new_n):
        for j in range(new_n):
            # Average the block
            block = square[i*scale:(i+1)*scale, j*scale:(j+1)*scale]
            result[i, j] = np.mean(block)
    
    return result