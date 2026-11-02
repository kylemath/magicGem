import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from axialSquareStorm import square_to_axial, compute_spherical_harmonics, load_magic_squares
from scipy.special import sph_harm_y as sph_harm  # Using the new recommended function

def create_harmonic_reconstruction(points, max_l=4):
    # Compute spherical harmonics
    results = {'spherical_harmonics': compute_spherical_harmonics(points)}
    coeffs = results['spherical_harmonics']
    
    # Generate spherical grid with higher resolution for smoother visualization
    phi = np.linspace(0, np.pi, 100)
    theta = np.linspace(0, 2*np.pi, 100)
    phi_grid, theta_grid = np.meshgrid(phi, theta)
    
    # Compute reconstruction using significant terms
    r_recon = np.zeros_like(theta_grid)
    significant_threshold = 0.1 * max(coeffs.values())
    
    for l in range(max_l + 1):
        for m in range(-l, l + 1):
            coeff = coeffs.get(f'l{l}m{m}', 0)
            if abs(coeff) > significant_threshold:
                Ylm = sph_harm(m, l, theta_grid, phi_grid)
                r_recon += coeff * np.abs(Ylm)
    
    # Convert to Cartesian coordinates
    x = r_recon * np.sin(phi_grid) * np.cos(theta_grid)
    y = r_recon * np.sin(phi_grid) * np.sin(theta_grid)
    z = r_recon * np.cos(phi_grid)
    
    return x, y, z, r_recon

# Load the magic square and convert to axial representation
square = np.array([[16, 3, 2, 13],
                   [5, 10, 11, 8],
                   [9, 6, 7, 12],
                   [4, 15, 14, 1]])
points, vectors = square_to_axial(square)

# Create the harmonic reconstruction
x, y, z, r_recon = create_harmonic_reconstruction(points)

# Set up the figure with high-quality settings
plt.rcParams['figure.dpi'] = 300
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Function to update the plot
def update(frame):
    ax.clear()
    
    # Plot the surface with improved visual settings
    surf = ax.plot_surface(x, y, z, 
                          cmap='viridis',
                          alpha=0.8,
                          rstride=2,
                          cstride=2,
                          linewidth=0.5,
                          edgecolors='w')
    
    # Set consistent view limits
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    
    # Set viewing angle
    ax.view_init(elev=20, azim=frame)
    
    # Add labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Harmonic Reconstruction (Rotating View)')
    
    # Add colorbar
    if not hasattr(update, 'colorbar'):
        update.colorbar = plt.colorbar(surf, ax=ax, shrink=0.8, label='Radial Distance')
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Maintain aspect ratio
    ax.set_box_aspect([1, 1, 1])

# Create animation with smoother rotation
frames = np.arange(0, 360, 2)  # 2-degree steps for smooth rotation
ani = FuncAnimation(fig, update, frames=frames, interval=50)

# Save animation with higher quality
ani.save('figures/axial_harmonic_rotation.gif', writer='pillow', fps=30)

plt.show() 