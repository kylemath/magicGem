import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from axialSquareStorm import square_to_axial, compute_spherical_harmonics
from scipy.special import sph_harm_y as sph_harm  # Using the new recommended function

# Collection of magic squares with their geometric properties
MAGIC_SQUARES = {
    "8v_4f_4i": {  # 8 vertices, 4 face points, 4 interior points
        "square": np.array([
            [1, 6, 11, 16],
            [14, 12, 5, 3],
            [15, 9, 8, 2],
            [4, 7, 10, 13]
        ]),
        "description": "8 vertices, 4 face points, 4 interior points"
    },
    "9v_3f_4i": {  # 9 vertices, 3 face points, 4 interior points
        "square": np.array([
            [1, 5, 16, 12],
            [15, 14, 3, 2],
            [10, 11, 6, 7],
            [8, 4, 9, 13]
        ]),
        "description": "9 vertices, 3 face points, 4 interior points"
    },
    "10v_2f_4i": {  # 10 vertices, 2 face points, 4 interior points
        "square": np.array([
            [1, 3, 14, 16],
            [15, 13, 4, 2],
            [10, 6, 11, 7],
            [8, 12, 5, 9]
        ]),
        "description": "10 vertices, 2 face points, 4 interior points"
    },
    "10v_4f_2i": {  # 10 vertices, 4 face points, 2 interior points
        "square": np.array([
            [1, 4, 13, 16],
            [15, 14, 3, 2],
            [8, 5, 12, 9],
            [10, 11, 6, 7]
        ]),
        "description": "10 vertices, 4 face points, 2 interior points"
    },
    "10v_6f_0i": {  # 10 vertices, 6 face points, 0 interior points
        "square": np.array([
            [1, 4, 13, 16],
            [8, 14, 3, 9],
            [15, 5, 12, 2],
            [10, 11, 6, 7]
        ]),
        "description": "10 vertices, 6 face points, 0 interior points"
    },
    "11v_1f_4i": {  # 11 vertices, 1 face point, 4 interior points
        "square": np.array([
            [1, 4, 14, 15],
            [16, 13, 3, 2],
            [11, 10, 8, 5],
            [6, 7, 9, 12]
        ]),
        "description": "11 vertices, 1 face point, 4 interior points"
    },
    "12v_0f_4i": {  # 12 vertices, 0 face points, 4 interior points
        "square": np.array([
            [1, 3, 14, 16],
            [10, 13, 4, 7],
            [15, 6, 11, 2],
            [8, 12, 5, 9]
        ]),
        "description": "12 vertices, 0 face points, 4 interior points"
    },
    "16v_0f_0i": {  # 16 vertices, 0 face points, 0 interior points
        "square": np.array([
            [1, 4, 13, 16],
            [8, 15, 2, 9],
            [14, 5, 12, 3],
            [11, 10, 7, 6]
        ]),
        "description": "16 vertices, 0 face points, 0 interior points"
    }
}

def create_shape_reconstruction(points, n_grid=50):
    """
    Create a direct geometric reconstruction of the point cloud shape.
    Uses radial basis functions for interpolation to create a smooth surface
    that better respects the actual point distribution.
    """
    x, y, z = points.T
    
    # Create a grid that encompasses all points with some padding
    padding = 0.2  # 20% padding
    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)
    z_min, z_max = np.min(z), np.max(z)
    
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min
    
    x_grid = np.linspace(x_min - padding * x_range, x_max + padding * x_range, n_grid)
    y_grid = np.linspace(y_min - padding * y_range, y_max + padding * y_range, n_grid)
    z_grid = np.linspace(z_min - padding * z_range, z_max + padding * z_range, n_grid)
    
    # Create 3D grid points
    X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid)
    grid_points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    
    # Compute distances from each grid point to each data point
    def rbf(r, epsilon=1.0):
        return np.exp(-(epsilon * r) ** 2)
    
    # Create implicit surface using RBF
    surface = np.zeros(len(grid_points))
    for p in points:
        # Distance from current point to all grid points
        distances = np.sqrt(np.sum((grid_points - p) ** 2, axis=1))
        surface += rbf(distances)
    
    # Normalize surface values
    surface = surface.reshape(n_grid, n_grid, n_grid)
    surface = (surface - np.min(surface)) / (np.max(surface) - np.min(surface))
    
    # Extract isosurface
    from skimage import measure
    verts, faces, _, _ = measure.marching_cubes(surface, level=0.1)
    
    # Scale vertices back to original coordinate system
    verts[:, 0] = x_grid[0] + verts[:, 0] * (x_grid[-1] - x_grid[0]) / (n_grid - 1)
    verts[:, 1] = y_grid[0] + verts[:, 1] * (y_grid[-1] - y_grid[0]) / (n_grid - 1)
    verts[:, 2] = z_grid[0] + verts[:, 2] * (z_grid[-1] - z_grid[0]) / (n_grid - 1)
    
    return verts, faces

def create_visualization(square_key="8v_4f_4i", make_gif=False, view_angles=None):
    """
    Create visualization for a specific magic square.
    """
    if square_key not in MAGIC_SQUARES:
        raise ValueError(f"Invalid square_key. Choose from: {list(MAGIC_SQUARES.keys())}")
    
    if view_angles is None:
        view_angles = (20, 45)
    
    # Get the selected magic square and its description
    square_data = MAGIC_SQUARES[square_key]
    square = square_data["square"]
    description = square_data["description"]
    
    # Convert to axial representation
    points, vectors = square_to_axial(square)
    print(f"\nProcessing {square_key}:")
    print(f"Number of points: {len(points)}")
    
    # Create the shape reconstruction
    verts, faces = create_shape_reconstruction(points)
    
    # Set up the figure
    plt.rcParams['figure.dpi'] = 300
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    def plot_frame(ax, azim):
        ax.clear()
        
        # Plot the original points
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                  c='red', s=50, label='Original Points')
        
        # Plot the surface mesh
        mesh = ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2],
                             triangles=faces,
                             cmap='viridis',
                             alpha=0.6,
                             edgecolor='white',
                             linewidth=0.1)
        
        # Set consistent view limits
        max_range = np.max([
            np.max(np.abs(points)),
            np.max(np.abs(verts))
        ]) * 1.2
        
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        # Set viewing angle
        ax.view_init(elev=view_angles[0], azim=azim)
        
        # Add labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Shape Reconstruction\n{description}')
        
        # Add colorbar
        if not hasattr(plot_frame, 'colorbar'):
            plot_frame.colorbar = plt.colorbar(mesh, ax=ax, shrink=0.8, 
                                             label='Surface Height')
        
        # Add grid and legend
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Maintain aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        return mesh
    
    if make_gif:
        frames = np.arange(0, 360, 2)
        ani = FuncAnimation(fig, lambda frame: plot_frame(ax, frame), 
                          frames=frames, interval=50)
        filename = f'figures/shape_reconstruction_{square_key}.gif'
        ani.save(filename, writer='pillow', fps=30)
        print(f"\nSaved animation to {filename}")
    else:
        plot_frame(ax, view_angles[1])
        filename = f'figures/shape_reconstruction_{square_key}_elev{view_angles[0]}_azim{view_angles[1]}.png'
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        print(f"\nSaved static view to {filename}")
    
    plt.show()

if __name__ == "__main__":
    view_angles = (30, 60)
    
    print("Generating view for square with minimum vertices (8)...")
    create_visualization("8v_4f_4i", make_gif=False, view_angles=view_angles)
    
    print("\nGenerating view for square with maximum vertices (16)...")
    create_visualization("16v_0f_0i", make_gif=False, view_angles=view_angles) 