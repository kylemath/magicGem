"""
Advanced Magic Square Analysis - Day 2
-------------------------------------
This module extends the original axialSquareStorm analysis with:
1. Enhanced symmetry group detection
2. Vector field flow analysis
3. Advanced visualization of symmetry orbits
4. Persistence homology analysis

Author: Claude
Date: 2024
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.special import sph_harm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import seaborn as sns
from matplotlib.gridspec import GridSpec
import os
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation

class AxialAnalyzer:
    def __init__(self, square):
        """Initialize with a magic square."""
        self.square = np.array(square)
        self.points, self.vectors = self._square_to_axial()
        self.center = np.mean(self.points, axis=0)
        
        # Set visualization style
        plt.style.use('default')  # Use default style instead of seaborn
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3

    def _square_to_axial(self):
        """Convert magic square to axial representation."""
        n = self.square.shape[0]
        points = []
        
        for i in range(n):
            for j in range(n):
                point = np.array([
                    i - (n-1)/2,
                    j - (n-1)/2,
                    self.square[i, j] - np.mean(self.square)
                ])
                points.append(point)
        
        points = np.array(points)
        vectors = points - np.zeros_like(points)
        return points, vectors

    def analyze_symmetry_groups(self):
        """
        Analyze rotational and reflectional symmetries.
        Returns dict with symmetry properties.
        """
        symmetries = {
            'rotational_orders': [],
            'reflection_planes': [],
            'symmetry_score': 0
        }
        
        # Test rotational symmetries with more lenient threshold
        for n in [2, 3, 4, 6]:  # Common symmetry orders
            angle = 2 * np.pi / n
            R = Rotation.from_rotvec([0, 0, angle]).as_matrix()
            rotated_points = self.points @ R.T
            
            # Check if rotated points match original
            dists = np.min(np.linalg.norm(
                rotated_points[:, np.newaxis] - self.points, axis=2
            ), axis=1)
            
            if np.mean(dists) < 0.5:  # More lenient threshold
                symmetries['rotational_orders'].append(n)
        
        # Test reflection planes with more lenient threshold
        axes = [[1,0,0], [0,1,0], [1,1,0], [1,-1,0]]
        for axis in axes:
            axis = np.array(axis) / np.linalg.norm(axis)
            reflected_points = self.points - 2 * np.outer(
                np.dot(self.points, axis), axis
            )
            
            dists = np.min(np.linalg.norm(
                reflected_points[:, np.newaxis] - self.points, axis=2
            ), axis=1)
            
            if np.mean(dists) < 0.5:  # More lenient threshold
                symmetries['reflection_planes'].append(axis.tolist())
        
        # Compute overall symmetry score
        symmetries['symmetry_score'] = (
            len(symmetries['rotational_orders']) + 
            len(symmetries['reflection_planes'])
        )
        
        return symmetries

    def analyze_vector_field_flow(self):
        """
        Analyze the flow patterns in the vector field.
        Returns dict with flow properties.
        """
        # Compute vector field properties
        flow = {
            'divergence': [],
            'curl': [],
            'flow_lines': [],
            'critical_points': []
        }
        
        # Compute divergence at each point
        for i, point in enumerate(self.points):
            # Find nearest neighbors
            dists = np.linalg.norm(self.points - point, axis=1)
            nearest = np.argsort(dists)[1:5]  # 4 nearest neighbors
            
            # Compute approximate divergence
            div = 0
            for j in nearest:
                dir_vec = (self.points[j] - point) / (dists[j] + 1e-10)  # Avoid division by zero
                div += np.dot(self.vectors[j] - self.vectors[i], dir_vec)
            flow['divergence'].append(div)
        
        # Compute curl at each point with safety checks
        for point, vec in zip(self.points, self.vectors):
            curl = np.zeros(3)
            # Approximate curl using central differences
            dx = np.array([0.1, 0, 0])
            dy = np.array([0, 0.1, 0])
            dz = np.array([0, 0, 0.1])
            
            # Find nearest points for derivatives
            for delta in [dx, dy, dz]:
                pos = point + delta
                neg = point - delta
                # Find closest actual points
                pos_idx = np.argmin(np.linalg.norm(self.points - pos, axis=1))
                neg_idx = np.argmin(np.linalg.norm(self.points - neg, axis=1))
                
                # Approximate derivatives
                dvx = (self.vectors[pos_idx][0] - self.vectors[neg_idx][0]) / 0.2
                dvy = (self.vectors[pos_idx][1] - self.vectors[neg_idx][1]) / 0.2
                dvz = (self.vectors[pos_idx][2] - self.vectors[neg_idx][2]) / 0.2
                
                curl += np.cross([dvx, dvy, dvz], delta/0.1)
            
            flow['curl'].append(curl)
        
        # Find critical points with more lenient threshold
        magnitudes = np.linalg.norm(self.vectors, axis=1)
        critical_mask = magnitudes < np.mean(magnitudes) * 0.3  # More lenient threshold
        flow['critical_points'] = self.points[critical_mask]
        
        return flow

    def visualize_symmetry_orbits(self, save_path=None):
        """
        Create visualization showing symmetry orbits of points.
        """
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2)
        
        # Plot original points with symmetry axes
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        scatter = ax1.scatter(self.points[:,0], self.points[:,1], self.points[:,2], 
                   c=self.square.flatten(), cmap='viridis', alpha=0.6)
        plt.colorbar(scatter, ax=ax1, label='Value')
        
        # Plot symmetry axes
        max_range = np.max(np.abs(self.points)) * 1.2
        symmetries = self.analyze_symmetry_groups()
        
        for order in symmetries['rotational_orders']:
            ax1.plot([0, 0], [0, 0], [-max_range, max_range],
                    'r--', label=f'{order}-fold axis')
        
        if len(symmetries['rotational_orders']) > 0:
            ax1.legend()
        
        ax1.set_title('Points Colored by Value')
        
        # Plot orbit diagram
        ax2 = fig.add_subplot(gs[0, 1], projection='3d')
        colors = plt.cm.rainbow(np.linspace(0, 1, len(self.points)))
        
        for point, color in zip(self.points, colors):
            # Generate orbit points
            orbit = [point]
            for angle in np.linspace(0, 2*np.pi, 24):
                R = Rotation.from_rotvec([0, 0, angle]).as_matrix()
                orbit.append(point @ R.T)
            orbit = np.array(orbit)
            
            # Plot orbit
            ax2.plot(orbit[:,0], orbit[:,1], orbit[:,2], 
                    c=color, alpha=0.3)
        
        ax2.set_title('Point Orbits')
        
        # Plot vector field with flow
        ax3 = fig.add_subplot(gs[1, :], projection='3d')
        
        # Plot original vectors
        for p, v in zip(self.points, self.vectors):
            ax3.quiver(p[0], p[1], p[2], 
                      v[0], v[1], v[2],
                      color='blue', alpha=0.6)
        
        # Compute and plot flow lines
        flow = self.analyze_vector_field_flow()
        
        # Plot critical points
        if len(flow['critical_points']) > 0:
            ax3.scatter(flow['critical_points'][:,0],
                       flow['critical_points'][:,1],
                       flow['critical_points'][:,2],
                       c='red', s=100, label='Critical Points')
        
        # Add curl vectors if they exist and are non-zero
        curl = np.array(flow['curl'])
        if len(curl) > 0 and np.any(curl != 0):
            max_curl = np.max(np.abs(curl))
            if max_curl > 0:
                scale = max_range / (max_curl * 2)
                ax3.quiver(self.points[:,0], self.points[:,1], self.points[:,2],
                          curl[:,0]*scale, curl[:,1]*scale, curl[:,2]*scale,
                          color='green', alpha=0.4, label='Curl')
        
        ax3.set_title('Vector Field Flow')
        ax3.legend()
        
        # Improve 3D visualization
        for ax in [ax1, ax2, ax3]:
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.view_init(elev=20, azim=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        return fig

    def create_flow_animation(self, save_path=None):
        """
        Create an animation showing vector field flow over time.
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        def update(frame):
            ax.clear()
            
            # Rotate points
            angle = frame * 2 * np.pi / 180
            R = Rotation.from_rotvec([0, 0, angle]).as_matrix()
            rotated_points = self.points @ R.T
            rotated_vectors = self.vectors @ R.T
            
            # Calculate and plot mean vector
            mean_point = np.mean(rotated_points, axis=0)
            mean_vector = np.mean(rotated_vectors, axis=0)
            ax.quiver(0, 0, 0,
                     mean_vector[0], mean_vector[1], mean_vector[2],
                     color='red', alpha=1.0, linewidth=2, label='Mean Vector')
            
            # Plot original vectors
            ax.quiver(rotated_points[:,0], rotated_points[:,1], rotated_points[:,2],
                     rotated_vectors[:,0], rotated_vectors[:,1], rotated_vectors[:,2],
                     color='blue', alpha=0.6, label='Field Vectors')
            
            # Plot flow lines with arrows
            for p in rotated_points:
                # Generate flow line
                flow_line = [p]
                current = p.copy()
                for step in range(10):
                    # Find nearest point and its vector
                    idx = np.argmin(np.linalg.norm(rotated_points - current, axis=1))
                    v = rotated_vectors[idx]
                    next_point = current + v * 0.1
                    flow_line.append(next_point)
                    
                    # Add arrow at every third step
                    if step % 3 == 2:
                        direction = v / (np.linalg.norm(v) + 1e-10)
                        ax.quiver(current[0], current[1], current[2],
                                direction[0]*0.5, direction[1]*0.5, direction[2]*0.5,
                                color='green', alpha=0.4)
                    
                    current = next_point
                
                flow_line = np.array(flow_line)
                ax.plot(flow_line[:,0], flow_line[:,1], flow_line[:,2],
                       'g-', alpha=0.2, label='Flow Lines' if p is rotated_points[0] else '')
            
            # Set consistent view limits
            max_range = np.max(np.abs(self.points)) * 1.2
            ax.set_xlim([-max_range, max_range])
            ax.set_ylim([-max_range, max_range])
            ax.set_zlim([-max_range, max_range])
            
            # Add legend and improve appearance
            ax.set_title(f'Vector Field Flow (Rotation: {frame}°)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        
        ani = FuncAnimation(fig, update, frames=range(0, 360, 5),
                          interval=50)
        
        if save_path:
            ani.save(save_path, writer='pillow', fps=30)
        
        return ani

    def visualize_orbit_surface(self, save_path=None):
        """
        Create a 3D surface visualization connecting all point orbits.
        """
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(1, 2)
        
        # First subplot: Surface with wireframe
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        
        # Generate dense orbit points
        n_angles = 50  # Number of points per orbit
        n_points = len(self.points)
        theta = np.linspace(0, 2*np.pi, n_angles)
        
        # Create arrays to store surface points
        X = np.zeros((n_points, n_angles))
        Y = np.zeros((n_points, n_angles))
        Z = np.zeros((n_points, n_angles))
        
        # Generate orbit points for each original point
        for i, point in enumerate(self.points):
            for j, angle in enumerate(theta):
                R = Rotation.from_rotvec([0, 0, angle]).as_matrix()
                rotated = point @ R.T
                X[i,j] = rotated[0]
                Y[i,j] = rotated[1]
                Z[i,j] = rotated[2]
        
        # Create surface plot with custom coloring
        values = self.square.flatten()[:, np.newaxis] * np.ones((1, n_angles))
        surf = ax1.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(values/np.max(values)),
                              alpha=0.6, shade=True)
        
        # Add wireframe for structure visibility
        ax1.plot_wireframe(X, Y, Z, color='black', alpha=0.1, linewidth=0.5)
        
        # Add original points
        scatter = ax1.scatter(self.points[:,0], self.points[:,1], self.points[:,2],
                            c=self.square.flatten(), cmap='viridis',
                            s=100, alpha=1.0)
        
        # Second subplot: Transparent view with orbit lines
        ax2 = fig.add_subplot(gs[0, 1], projection='3d')
        
        # Plot orbit lines
        for i in range(n_points):
            ax2.plot(X[i,:], Y[i,:], Z[i,:], 'b-', alpha=0.3)
        
        # Plot surface with high transparency
        surf2 = ax2.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(values/np.max(values)),
                               alpha=0.2, shade=True)
        
        # Add original points
        scatter2 = ax2.scatter(self.points[:,0], self.points[:,1], self.points[:,2],
                             c=self.square.flatten(), cmap='viridis',
                             s=100, alpha=1.0)
        
        # Improve both plots
        for ax in [ax1, ax2]:
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.view_init(elev=20, azim=45)
            
            # Set consistent view limits
            max_range = np.max(np.abs(self.points)) * 1.2
            ax.set_xlim([-max_range, max_range])
            ax.set_ylim([-max_range, max_range])
            ax.set_zlim([-max_range, max_range])
        
        ax1.set_title('Orbit Surface (Solid)')
        ax2.set_title('Orbit Surface (Transparent)')
        
        # Add colorbar
        plt.colorbar(scatter, ax=ax1, label='Value')
        plt.colorbar(scatter2, ax=ax2, label='Value')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        return fig

    def compute_balance_metrics(self):
        """
        Compute balance metrics and higher moments of the point distribution.
        Returns dict with balance measure and moment analysis.
        """
        # 1. Balance Measure
        mean_vector = np.mean(self.vectors, axis=0)
        squared_magnitudes = np.sum(self.vectors**2, axis=1)
        rms_distance = np.sqrt(np.mean(squared_magnitudes))
        balance = np.linalg.norm(mean_vector) / rms_distance

        # 2. Second Moment (Covariance Matrix)
        covariance = np.cov(self.vectors.T)
        eigenvals, eigenvecs = np.linalg.eigh(covariance)
        
        # Compute condition number (ratio of largest to smallest eigenvalue)
        # This indicates how "asymmetric" the distribution is
        condition_number = eigenvals[-1] / eigenvals[0]
        
        # 3. Third Moment (Skewness)
        centered_vectors = self.vectors - mean_vector
        skewness = np.zeros(3)  # One for each dimension
        for i in range(3):
            sigma = np.std(self.vectors[:, i])
            if sigma > 0:  # Avoid division by zero
                skewness[i] = np.mean((centered_vectors[:, i])**3) / (sigma**3)
        
        # Compute overall skewness magnitude
        skewness_magnitude = np.linalg.norm(skewness)
        
        return {
            'balance_measure': balance,
            'mean_vector': mean_vector,
            'rms_distance': rms_distance,
            'covariance': covariance,
            'eigenvalues': eigenvals,
            'eigenvectors': eigenvecs,
            'condition_number': condition_number,
            'skewness': skewness,
            'skewness_magnitude': skewness_magnitude
        }

    def visualize_balance_analysis(self, save_path=None):
        """
        Create visualization showing balance metrics and moment analysis.
        """
        metrics = self.compute_balance_metrics()
        
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2)
        
        # 1. Plot points with mean vector and principal axes
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        
        # Plot points
        scatter = ax1.scatter(self.points[:,0], self.points[:,1], self.points[:,2],
                            c=self.square.flatten(), cmap='viridis',
                            s=100, alpha=0.8)
        plt.colorbar(scatter, ax=ax1, label='Value')
        
        # Plot mean vector
        ax1.quiver(0, 0, 0,
                  metrics['mean_vector'][0],
                  metrics['mean_vector'][1],
                  metrics['mean_vector'][2],
                  color='red', alpha=1.0, linewidth=2,
                  label=f'Mean Vector (Balance: {metrics["balance_measure"]:.3f})')
        
        # Plot principal axes (eigenvectors)
        for i, (val, vec) in enumerate(zip(metrics['eigenvalues'], metrics['eigenvectors'].T)):
            # Scale vector by its eigenvalue
            scaled_vec = vec * np.sqrt(val)
            ax1.quiver(0, 0, 0,
                      scaled_vec[0], scaled_vec[1], scaled_vec[2],
                      color=['g', 'b', 'y'][i], alpha=0.6,
                      label=f'Principal Axis {i+1}')
        
        ax1.set_title('Point Distribution and Principal Axes')
        ax1.legend()
        
        # 2. Plot covariance ellipsoid
        ax2 = fig.add_subplot(gs[0, 1], projection='3d')
        
        # Generate points on unit sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))
        
        # Transform points using eigenvalues and eigenvectors
        points = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)
        transformed_points = (points @ metrics['eigenvectors']) * np.sqrt(metrics['eigenvalues'])
        
        # Reshape back to grid
        x_t = transformed_points[:,0].reshape(x.shape)
        y_t = transformed_points[:,1].reshape(y.shape)
        z_t = transformed_points[:,2].reshape(z.shape)
        
        # Plot ellipsoid
        ax2.plot_surface(x_t, y_t, z_t, alpha=0.3, cmap='viridis')
        ax2.set_title(f'Covariance Ellipsoid\nCondition Number: {metrics["condition_number"]:.2f}')
        
        # 3. Plot skewness vectors
        ax3 = fig.add_subplot(gs[1, 0])
        dimensions = ['X', 'Y', 'Z']
        skewness = metrics['skewness']
        bars = ax3.bar(dimensions, skewness)
        
        # Color bars based on sign
        for bar, sk in zip(bars, skewness):
            bar.set_color('red' if sk > 0 else 'blue')
        
        ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax3.set_title(f'Skewness by Dimension\nMagnitude: {metrics["skewness_magnitude"]:.2f}')
        ax3.set_ylabel('Skewness')
        
        # 4. Plot eigenvalue spectrum
        ax4 = fig.add_subplot(gs[1, 1])
        eigenvals = metrics['eigenvalues']
        ax4.bar(['1st', '2nd', '3rd'], eigenvals)
        ax4.set_title('Eigenvalue Spectrum\n(Indicates spread in principal directions)')
        ax4.set_ylabel('Eigenvalue')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        return fig, metrics

def test_analysis():
    """Test the enhanced analysis functions."""
    # Create output directory
    os.makedirs('figures_day2', exist_ok=True)
    
    # Example magic square
    square = np.array([
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ])
    
    # Create analyzer
    analyzer = AxialAnalyzer(square)
    
    # Run analyses
    symmetries = analyzer.analyze_symmetry_groups()
    flow = analyzer.analyze_vector_field_flow()
    balance_metrics = analyzer.compute_balance_metrics()
    
    # Create visualizations
    analyzer.visualize_symmetry_orbits('figures_day2/symmetry_orbits.png')
    analyzer.create_flow_animation('figures_day2/vector_flow.gif')
    analyzer.visualize_orbit_surface('figures_day2/orbit_surface.png')
    analyzer.visualize_balance_analysis('figures_day2/balance_analysis.png')
    
    # Print results
    print("\nSymmetry Analysis Results:")
    print("=========================")
    print(f"Rotational symmetries: {symmetries['rotational_orders']}")
    print(f"Reflection planes: {len(symmetries['reflection_planes'])}")
    print(f"Overall symmetry score: {symmetries['symmetry_score']}")
    
    print("\nVector Field Analysis:")
    print("====================")
    print(f"Number of critical points: {len(flow['critical_points'])}")
    print(f"Average curl magnitude: {np.mean(np.linalg.norm(flow['curl'], axis=1))}")
    print(f"Average divergence: {np.mean(flow['divergence'])}")
    
    print("\nBalance Analysis:")
    print("================")
    print(f"Balance measure: {balance_metrics['balance_measure']:.3f}")
    print(f"RMS distance: {balance_metrics['rms_distance']:.3f}")
    print(f"Condition number: {balance_metrics['condition_number']:.3f}")
    print(f"Skewness magnitude: {balance_metrics['skewness_magnitude']:.3f}")
    print("\nEigenvalues:")
    for i, val in enumerate(balance_metrics['eigenvalues']):
        print(f"  Principal axis {i+1}: {val:.3f}")

if __name__ == '__main__':
    test_analysis() 