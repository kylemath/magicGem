"""
Axial Magic Square Analysis
--------------------------
This module provides advanced geometric and topological analysis tools for studying
the axial representation of magic squares, where each square is represented as vectors
from the origin to points in 3D space.

Author: Claude
Date: 2024
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.special import sph_harm_y as sph_harm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import seaborn as sns
from matplotlib.gridspec import GridSpec

try:
    from ripser import ripser
    from persim import plot_diagrams
    RIPSER_AVAILABLE = True
except ImportError:
    print("Warning: ripser not installed. Persistence diagram computation will be unavailable.")
    RIPSER_AVAILABLE = False

try:
    import gudhi
    GUDHI_AVAILABLE = True
except ImportError:
    print("Warning: gudhi not installed. Some topological analyses will be unavailable.")
    GUDHI_AVAILABLE = False

from scipy.stats import moment
import os

# Set default style for all plots
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

def load_magic_squares(cache_dir='analysis/cache'):
    """Load the 880 unique 4x4 magic squares from cache."""
    # TODO: Implement actual loading from cache
    # For now, return a sample magic square
    return [np.array([[16, 3, 2, 13],
                     [5, 10, 11, 8],
                     [9, 6, 7, 12],
                     [4, 15, 14, 1]])]

def square_to_axial(square):
    """
    Convert a magic square to its axial representation.
    
    Parameters:
    -----------
    square : ndarray
        4x4 magic square
        
    Returns:
    --------
    points : ndarray
        Array of 16 3D points representing vector endpoints
    vectors : ndarray
        Array of 16 3D vectors from origin to points
    """
    n = square.shape[0]
    points = []
    
    # Convert to centered coordinates
    for i in range(n):
        for j in range(n):
            # Create point (i, j, value)
            point = np.array([i - (n-1)/2, 
                            j - (n-1)/2, 
                            square[i, j] - np.mean(square)])
            points.append(point)
    
    points = np.array(points)
    vectors = points - np.zeros_like(points)  # Vectors from origin
    
    return points, vectors

def compute_center_of_mass(points, weights=None):
    """
    Compute center of mass of the axial representation.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    weights : ndarray, optional
        Weights for each point (default: uniform)
        
    Returns:
    --------
    ndarray
        3D center of mass
    """
    if weights is None:
        weights = np.ones(len(points))
    weights = weights / np.sum(weights)
    return np.sum(points * weights[:, np.newaxis], axis=0)

def compute_spherical_stats(points):
    """
    Compute statistical properties in spherical coordinates.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
        
    Returns:
    --------
    dict
        Dictionary containing spherical statistics
    """
    # Convert to spherical coordinates (r, theta, phi)
    x, y, z = points.T
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z/r)
    
    return {
        'r_mean': np.mean(r),
        'r_std': np.std(r),
        'theta_mean': np.mean(theta),
        'theta_std': np.std(theta),
        'phi_mean': np.mean(phi),
        'phi_std': np.std(phi),
        'spherical_variance': 1 - np.mean(r)/np.max(r)
    }

def compute_vector_field_properties(points, vectors):
    """
    Analyze the vector field properties of the axial representation.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    vectors : ndarray
        Array of 3D vectors
        
    Returns:
    --------
    dict
        Dictionary containing vector field properties
    """
    # Compute divergence (approximated at origin)
    div = np.mean(np.sum(vectors/np.linalg.norm(points, axis=1)[:, np.newaxis], axis=1))
    
    # Compute curl (approximated at origin)
    curl_x = np.mean(vectors[:, 2] * points[:, 1] - vectors[:, 1] * points[:, 2])
    curl_y = np.mean(vectors[:, 0] * points[:, 2] - vectors[:, 2] * points[:, 0])
    curl_z = np.mean(vectors[:, 1] * points[:, 0] - vectors[:, 0] * points[:, 1])
    
    return {
        'divergence': div,
        'curl': np.array([curl_x, curl_y, curl_z]),
        'field_energy': np.sum(np.linalg.norm(vectors, axis=1)**2)
    }

def compute_spherical_harmonics(points, lmax=4):
    """
    Compute spherical harmonic decomposition of the axial representation.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    lmax : int
        Maximum degree of spherical harmonics
        
    Returns:
    --------
    dict
        Dictionary containing spherical harmonic coefficients
    """
    # Convert to spherical coordinates
    x, y, z = points.T
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z/r)
    
    coeffs = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Ylm = sph_harm(m, l, theta, phi)
            coeffs[f'l{l}m{m}'] = np.abs(np.sum(Ylm))
    
    return coeffs

def compute_persistence_diagram(points):
    """
    Compute persistent homology of the axial representation.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
        
    Returns:
    --------
    dict
        Dictionary containing persistence diagrams
    """
    if not RIPSER_AVAILABLE:
        print("Warning: Skipping persistence diagram computation - ripser not installed")
        return {
            'H0': None,
            'H1': None,
            'total_persistence': None
        }
        
    try:
        # Compute persistence diagrams
        diagrams = ripser(points)['dgms']
        
        return {
            'H0': diagrams[0],  # 0-dimensional features (components)
            'H1': diagrams[1],  # 1-dimensional features (loops)
            'total_persistence': np.sum([np.sum(diag[:, 1] - diag[:, 0]) for diag in diagrams])
        }
    except Exception as e:
        print(f"Error computing persistence diagram: {e}")
        return {
            'H0': None,
            'H1': None,
            'total_persistence': None
        }

def compute_morse_theory_features(points, vectors):
    """
    Analyze the vector field using discrete Morse theory.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    vectors : ndarray
        Array of 3D vectors
        
    Returns:
    --------
    dict
        Dictionary containing Morse theory features
    """
    # Create a graph representation
    G = nx.Graph()
    
    # Add nodes for each point
    for i, point in enumerate(points):
        G.add_node(i, pos=point)
    
    # Add edges based on vector field flow
    for i, v1 in enumerate(vectors):
        for j, v2 in enumerate(vectors):
            if i != j:
                # Add edge if vectors are similar in direction
                cos_sim = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
                if cos_sim > 0.8:  # Threshold for similarity
                    G.add_edge(i, j, weight=cos_sim)
    
    return {
        'num_critical_points': len(list(nx.isolates(G))),
        'flow_components': nx.number_connected_components(G),
        'average_flow_similarity': np.mean([d['weight'] for (u,v,d) in G.edges(data=True)])
    }

def compute_weighted_spherical_moments(points, weights=None, max_order=4):
    """
    Compute weighted moments in spherical shells around the origin.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    weights : ndarray, optional
        Weights for each point
    max_order : int
        Maximum order of moments to compute
        
    Returns:
    --------
    dict
        Dictionary containing spherical shell moments
    """
    if weights is None:
        weights = np.ones(len(points))
    
    # Convert to spherical coordinates
    x, y, z = points.T
    r = np.sqrt(x**2 + y**2 + z**2)
    
    moments = {}
    for k in range(max_order + 1):
        # Compute k-th moment of weighted radial distribution
        moments[f'radial_moment_{k}'] = np.sum(weights * r**k) / np.sum(weights)
    
    return moments

def analyze_axial_symmetries(points, vectors):
    """
    Analyze symmetries in the axial representation.
    
    Parameters:
    -----------
    points : ndarray
        Array of 3D points
    vectors : ndarray
        Array of 3D vectors
        
    Returns:
    --------
    dict
        Dictionary containing symmetry properties
    """
    # Compute principal axes
    inertia_tensor = np.zeros((3, 3))
    for p in points:
        r2 = np.sum(p**2)
        inertia_tensor += np.eye(3) * r2 - np.outer(p, p)
    
    eigenvals, eigenvecs = np.linalg.eigh(inertia_tensor)
    
    # Check for rotational symmetries
    rot_symmetry_scores = []
    for angle in np.linspace(0, 2*np.pi, 36):
        # Rotate points around z-axis
        c, s = np.cos(angle), np.sin(angle)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        rotated_points = points @ R.T
        
        # Compute similarity score
        dists = np.min(np.linalg.norm(rotated_points[:, np.newaxis] - points, axis=2), axis=1)
        rot_symmetry_scores.append(np.mean(dists))
    
    return {
        'principal_moments': eigenvals,
        'principal_axes': eigenvecs,
        'rotational_symmetry': 1.0 - min(rot_symmetry_scores)/max(rot_symmetry_scores),
        'spherical_asymmetry': np.std(eigenvals)/np.mean(eigenvals)
    }

def visualize_axial_representation(square, points, vectors, save_path=None):
    """
    Create a publication-ready figure showing the axial representation.
    
    Parameters:
    -----------
    square : ndarray
        Original magic square
    points : ndarray
        3D points from axial representation
    vectors : ndarray
        Array of 3D vectors from origin to points
    save_path : str, optional
        Path to save the figure
    """
    fig = plt.figure(figsize=(15, 5))
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1, 1.2, 1.2])
    
    # Plot original square
    ax1 = fig.add_subplot(gs[0])
    im = ax1.imshow(square, cmap='viridis')
    cbar1 = plt.colorbar(im, ax=ax1)
    cbar1.set_label('Value', fontsize=10)
    ax1.set_title('Original Magic Square')
    # Add row and column labels
    ax1.set_xticks(range(square.shape[1]))
    ax1.set_yticks(range(square.shape[0]))
    ax1.set_xticklabels([f'Col {i+1}' for i in range(square.shape[1])])
    ax1.set_yticklabels([f'Row {i+1}' for i in range(square.shape[0])])
    
    # Plot 3D points
    ax2 = fig.add_subplot(gs[1], projection='3d')
    scatter = ax2.scatter(points[:, 0], points[:, 1], points[:, 2], 
                         c=square.flatten(), cmap='viridis',
                         s=100)  # Increased point size
    cbar2 = plt.colorbar(scatter, ax=ax2)
    cbar2.set_label('Value', fontsize=10)
    ax2.set_title('Axial Points')
    
    # Improve 3D point visualization
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    
    # Add grid
    ax2.grid(True)
    
    # Plot vector field
    ax3 = fig.add_subplot(gs[2], projection='3d')
    
    # Plot vectors from origin to points
    for p in points:
        # Draw line from origin to point
        ax3.plot([0, p[0]], [0, p[1]], [0, p[2]], 
                 'b-', alpha=0.3, linewidth=1)
    
    # Plot points
    ax3.scatter(points[:, 0], points[:, 1], points[:, 2], 
                c='red', s=50, alpha=0.6)
    
    # Plot origin
    ax3.scatter([0], [0], [0], c='black', s=100, marker='*', label='Origin')
    
    ax3.set_title('Vector Field')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.legend()
    
    # Add grid
    ax3.grid(True)
    
    # Adjust 3D plot views for better visualization
    for ax in [ax2, ax3]:
        ax.view_init(elev=20, azim=45)  # Adjust viewing angle
        
        # Set equal aspect ratio
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()
        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)
        plot_radius = 0.5*max([x_range, y_range, z_range])
        
        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig

def visualize_geometric_analysis(points, results, save_path=None):
    """
    Create a publication-ready figure showing geometric analysis results.
    """
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 2, figure=fig)
    
    # Spherical coordinates distribution
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    x, y, z = points.T
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z/r)
    
    scatter = ax1.scatter(r*np.sin(phi)*np.cos(theta),
                         r*np.sin(phi)*np.sin(theta),
                         r*np.cos(phi),
                         c=r, cmap='viridis')
    plt.colorbar(scatter, ax=ax1)
    ax1.set_title('Spherical Distribution')
    
    # Radial distribution
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(r, bins=20, density=True)
    ax2.set_title('Radial Distribution')
    ax2.set_xlabel('Radius')
    ax2.set_ylabel('Density')
    
    # Principal axes
    ax3 = fig.add_subplot(gs[1, 0], projection='3d')
    eigenvals = results['symmetries']['principal_moments']
    eigenvecs = results['symmetries']['principal_axes']
    
    for length, vec in zip(eigenvals, eigenvecs):
        ax3.quiver(0, 0, 0, vec[0], vec[1], vec[2],
                  length=length/np.max(eigenvals),
                  color='r', alpha=0.8)
    ax3.set_title('Principal Axes')
    
    # Spherical moments
    ax4 = fig.add_subplot(gs[1, 1])
    moments = [v for k, v in results['spherical_moments'].items()]
    ax4.plot(range(len(moments)), moments, 'o-')
    ax4.set_title('Spherical Moments')
    ax4.set_xlabel('Moment Order')
    ax4.set_ylabel('Moment Value')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig

def visualize_harmonic_analysis(points, results, save_path=None):
    """
    Create a publication-ready figure showing spherical harmonic analysis.
    """
    fig = plt.figure(figsize=(15, 12))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1.2, 1, 0.8])
    
    # Extract harmonic coefficients
    coeffs = results['spherical_harmonics']
    l_max = int(np.sqrt(len(coeffs)))
    
    # Create coefficient matrix
    coeff_matrix = np.zeros((l_max + 1, 2*l_max + 1))
    for key, value in coeffs.items():
        l = int(key[1:].split('m')[0])
        m = int(key.split('m')[1])
        coeff_matrix[l, m + l_max] = value
    
    # Plot coefficient heatmap
    ax1 = fig.add_subplot(gs[0, :])
    sns.heatmap(coeff_matrix, cmap='viridis', ax=ax1, 
                cbar_kws={'label': 'Coefficient Magnitude'})
    ax1.set_title('Spherical Harmonic Coefficients')
    ax1.set_xlabel('m (Angular Order)')
    ax1.set_ylabel('l (Degree)')
    
    # Add text annotations for significant coefficients
    significant_threshold = 0.1 * np.max(coeff_matrix)
    for l in range(coeff_matrix.shape[0]):
        for m in range(coeff_matrix.shape[1]):
            if coeff_matrix[l, m] > significant_threshold:
                ax1.text(m, l, f'{coeff_matrix[l, m]:.2f}', 
                        ha='center', va='center', color='white')
    
    # Plot dominant modes reconstruction from different angles
    thetas = [0, 45]  # Different viewing angles
    for idx, theta_view in enumerate(thetas):
        ax = fig.add_subplot(gs[1, idx], projection='3d')
        
        # Generate spherical grid
        phi = np.linspace(0, np.pi, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        phi_grid, theta_grid = np.meshgrid(phi, theta)
        
        # Compute reconstruction
        r_recon = np.zeros_like(theta_grid)
        for l in range(min(3, l_max + 1)):
            for m in range(-l, l + 1):
                if abs(coeffs.get(f'l{l}m{m}', 0)) > significant_threshold:
                    Ylm = sph_harm(m, l, theta_grid, phi_grid)
                    r_recon += coeffs[f'l{l}m{m}'] * np.abs(Ylm)
        
        # Convert to Cartesian coordinates
        x = r_recon * np.sin(phi_grid) * np.cos(theta_grid)
        y = r_recon * np.sin(phi_grid) * np.sin(theta_grid)
        z = r_recon * np.cos(phi_grid)
        
        # Plot surface
        surf = ax.plot_surface(x, y, z, cmap='viridis',
                             alpha=0.8)
        plt.colorbar(surf, ax=ax, label='Radial Distance')
        
        # Set view angle
        ax.view_init(elev=20, azim=theta_view)
        ax.set_title(f'Reconstruction (View: {theta_view}°)')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    
    # Plot symmetry analysis
    ax4 = fig.add_subplot(gs[2, :])
    
    # Compute contribution by degree l
    l_contributions = np.zeros(l_max + 1)
    for l in range(l_max + 1):
        l_coeffs = [v for k, v in coeffs.items() if int(k[1:].split('m')[0]) == l]
        l_contributions[l] = np.sum(np.abs(l_coeffs))
    
    # Plot degree contributions
    bars = ax4.bar(range(l_max + 1), l_contributions)
    ax4.set_xlabel('Spherical Harmonic Degree (l)')
    ax4.set_ylabel('Total Contribution')
    ax4.set_title('Contribution by Degree (Measure of Symmetry)')
    
    # Add percentage labels
    total_contrib = np.sum(l_contributions)
    for bar, contrib in zip(bars, l_contributions):
        percentage = (contrib / total_contrib) * 100
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{percentage:.1f}%',
                ha='center', va='bottom')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig

def visualize_topology(points, results, save_path=None):
    """
    Create a publication-ready figure showing topological analysis results.
    """
    if not RIPSER_AVAILABLE:
        print("Cannot create topology visualization - ripser not installed")
        return None
        
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 2, figure=fig)
    
    # Plot persistence diagram
    ax1 = fig.add_subplot(gs[0, :])
    plot_diagrams(results['persistence']['H0'], ax=ax1, show=False)
    plot_diagrams(results['persistence']['H1'], ax=ax1, show=False)
    ax1.set_title('Persistence Diagram')
    
    # Plot Morse graph
    ax2 = fig.add_subplot(gs[1, 0])
    G = nx.Graph()
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if i < j:
                dist = np.linalg.norm(p1 - p2)
                if dist < np.mean(results['spherical_stats']['r_mean']):
                    G.add_edge(i, j, weight=dist)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax2, node_size=100, node_color='b', alpha=0.6)
    ax2.set_title('Morse Graph')
    
    # Plot flow field
    ax3 = fig.add_subplot(gs[1, 1], projection='3d')
    for i, (p1, v1) in enumerate(zip(points, points)):
        for j, (p2, v2) in enumerate(zip(points, points)):
            if i < j:
                cos_sim = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
                if cos_sim > 0.8:
                    ax3.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                            'b-', alpha=0.2)
    ax3.scatter(points[:, 0], points[:, 1], points[:, 2], c='r', s=50)
    ax3.set_title('Vector Field Flow')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig

def visualize_rotational_symmetry(points, results, save_path=None):
    """
    Create a visualization specifically demonstrating the 4-fold rotational symmetry.
    """
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 3, figure=fig, height_ratios=[1.2, 1])
    
    # Extract harmonic coefficients
    coeffs = results['spherical_harmonics']
    l_max = int(np.sqrt(len(coeffs)))
    
    # Plot points from different viewing angles around z-axis
    angles = [0, 45, 90]  # Show 0°, 45°, and 90° views
    for idx, angle in enumerate(angles):
        ax = fig.add_subplot(gs[0, idx], projection='3d')
        
        # Plot points
        scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                           c='blue', alpha=0.6)
        
        # Plot lines from origin to points to emphasize structure
        for p in points:
            ax.plot([0, p[0]], [0, p[1]], [0, p[2]], 
                   'b-', alpha=0.2)
        
        ax.view_init(elev=20, azim=angle)
        ax.set_title(f'View from {angle}°')
        
        # Set equal aspect ratio
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()
        plot_radius = 0.5*max([abs(x_limits[1] - x_limits[0]),
                              abs(y_limits[1] - y_limits[0]),
                              abs(z_limits[1] - z_limits[0])])
        ax.set_xlim3d([-plot_radius, plot_radius])
        ax.set_ylim3d([-plot_radius, plot_radius])
        ax.set_zlim3d([-plot_radius, plot_radius])
        
        # Add z-axis to emphasize rotation axis
        ax.plot([0, 0], [0, 0], [-plot_radius, plot_radius], 
                'r--', linewidth=2, label='Rotation Axis (Z)')
        ax.legend()
    
    # Create coefficient matrix for visualization
    coeff_matrix = np.zeros((l_max + 1, 2*l_max + 1))
    for key, value in coeffs.items():
        l = int(key[1:].split('m')[0])
        m = int(key.split('m')[1])
        coeff_matrix[l, m + l_max] = value
    
    # Plot coefficient pattern
    ax_coeff = fig.add_subplot(gs[1, :])
    im = sns.heatmap(coeff_matrix, cmap='viridis', ax=ax_coeff,
                     cbar_kws={'label': 'Coefficient Magnitude'})
    
    # Add arrows to highlight diagonal pattern
    for l in range(l_max + 1):
        m = l  # Diagonal pattern where m = l
        if coeffs.get(f'l{l}m{m}', 0) > 0.1 * np.max(list(coeffs.values())):
            ax_coeff.annotate('',
                            xy=(m + l_max, l),  # End of arrow
                            xytext=(m + l_max - 0.5, l - 0.5),  # Start of arrow
                            arrowprops=dict(facecolor='white', shrink=0.05),
                            )
    
    ax_coeff.set_title('Spherical Harmonic Coefficients\n(Arrows highlight 4-fold rotational symmetry pattern)')
    ax_coeff.set_xlabel('m (Angular Order)')
    ax_coeff.set_ylabel('l (Degree)')
    
    # Add text explanation
    text = ("4-fold rotational symmetry appears as:\n"
           "1. Strong coefficients when m = l\n"
           "2. Pattern repeats every 90° (π/2 radians)\n"
           "3. Strength decreases with higher l")
    plt.figtext(0.02, 0.02, text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig

def test_analysis():
    """Test the analysis functions and create visualizations."""
    # Load magic squares
    squares = load_magic_squares()
    
    # Analyze first square
    square = squares[0]
    points, vectors = square_to_axial(square)
    
    # Run analyses
    results = {
        'center_of_mass': compute_center_of_mass(points),
        'spherical_stats': compute_spherical_stats(points),
        'vector_field': compute_vector_field_properties(points, vectors),
        'spherical_harmonics': compute_spherical_harmonics(points),
        'persistence': compute_persistence_diagram(points),
        'morse_theory': compute_morse_theory_features(points, vectors),
        'spherical_moments': compute_weighted_spherical_moments(points),
        'symmetries': analyze_axial_symmetries(points, vectors)
    }
    
    # Create visualizations
    os.makedirs('figures', exist_ok=True)
    
    visualize_axial_representation(square, points, vectors, 'figures/axial_representation.png')
    visualize_geometric_analysis(points, results, 'figures/geometric_analysis.png')
    visualize_harmonic_analysis(points, results, 'figures/harmonic_analysis.png')
    visualize_topology(points, results, 'figures/topology_analysis.png')
    visualize_rotational_symmetry(points, results, 'figures/rotational_symmetry.png')
    
    # Print numerical results
    print("\nAxial Magic Square Analysis Results:")
    print("====================================")
    for analysis_name, analysis_results in results.items():
        print(f"\n{analysis_name}:")
        if isinstance(analysis_results, dict):
            for key, value in analysis_results.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {analysis_results}")

if __name__ == '__main__':
    test_analysis() 