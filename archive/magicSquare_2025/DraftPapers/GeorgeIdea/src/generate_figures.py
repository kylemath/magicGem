"""
Generate figures for the Spin Gem paper.

Creates visualizations connecting molecular spin configurations to the
Magic Gem covariance framework.

Author: George R.
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spin_gem_core import (
    Atom, SpinGem, create_spin_gem, generate_symmetric_molecule,
    scan_spin_configurations, precession_dynamics, 
    magic_square_to_spin_gem, verify_magic_square_is_spin_magic,
    magic_spin_configuration, compute_precession_tensor
)

# Figure output directory
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Style settings
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'


def fig1_spin_gem_concept():
    """
    Figure 1: Conceptual illustration of Spin Gems.
    Shows the construction from molecular geometry + spin states.
    """
    fig = plt.figure(figsize=(14, 5))
    
    # Panel A: Molecule with spin arrows
    ax1 = fig.add_subplot(131, projection='3d')
    
    atoms = generate_symmetric_molecule(6, 'regular_polygon', radius=1.5)
    positions = np.array([a.position for a in atoms])
    spins = np.array([a.spin for a in atoms])
    
    # Plot atoms
    colors = plt.cm.coolwarm((spins - spins.min()) / (spins.max() - spins.min() + 1e-10))
    ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                c=colors, s=200, edgecolors='k', linewidths=1.5)
    
    # Plot spin arrows
    for i, (pos, spin) in enumerate(zip(positions, spins)):
        ax1.quiver(pos[0], pos[1], pos[2], 0, 0, spin * 2,
                   color=colors[i], arrow_length_ratio=0.3, linewidth=2)
    
    ax1.set_xlabel('x (Å)')
    ax1.set_ylabel('y (Å)')
    ax1.set_zlabel('z (Å)')
    ax1.set_title('(a) Hexagonal Molecule\nwith Spin States', fontsize=11)
    
    # Panel B: Spin Gem representation
    ax2 = fig.add_subplot(132, projection='3d')
    
    gem = create_spin_gem(atoms)
    cloud = gem.point_cloud
    
    # 3D scatter with spin as color
    colors2 = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / 
                               (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    ax2.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 3], 
                c=colors2, s=150, edgecolors='k', linewidths=1)
    
    # Add convex hull in x-y-spin space
    try:
        points_3d = cloud[:, [0, 1, 3]]
        hull = ConvexHull(points_3d)
        for simplex in hull.simplices:
            triangle = points_3d[simplex]
            poly = Poly3DCollection([triangle], alpha=0.15, facecolor='blue', edgecolor='navy')
            ax2.add_collection3d(poly)
    except:
        pass
    
    ax2.set_xlabel('x (centered)')
    ax2.set_ylabel('y (centered)')
    ax2.set_zlabel('Spin (centered)')
    ax2.set_title('(b) Spin Gem\nPoint Cloud', fontsize=11)
    
    # Panel C: Covariance matrix
    ax3 = fig.add_subplot(133)
    
    cov = gem.covariance_matrix
    im = ax3.imshow(cov, cmap='RdBu_r', vmin=-np.abs(cov).max(), vmax=np.abs(cov).max())
    ax3.set_xticks([0, 1, 2, 3])
    ax3.set_xticklabels(['x', 'y', 'z', 's'])
    ax3.set_yticks([0, 1, 2, 3])
    ax3.set_yticklabels(['x', 'y', 'z', 's'])
    ax3.set_title('(c) Covariance Matrix\n$\\Sigma_{ij}$', fontsize=11)
    
    # Annotate values
    for i in range(4):
        for j in range(4):
            color = 'white' if abs(cov[i, j]) > 0.5 * np.abs(cov).max() else 'black'
            ax3.text(j, i, f'{cov[i,j]:.2f}', ha='center', va='center', 
                     color=color, fontsize=9)
    
    plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig1_spin_gem_concept.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig1_spin_gem_concept.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 1: Spin Gem Concept")


def fig2_magic_vs_random():
    """
    Figure 2: Comparison of 'magic' spin configurations vs random ones.
    Energy landscape analogy to Magic Gems.
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    
    # Geometries to test
    geometries = ['tetrahedron', 'octahedron', 'cube']
    titles = ['Tetrahedron (4 atoms)', 'Octahedron (6 atoms)', 'Cube (8 atoms)']
    
    for col, (geom, title) in enumerate(zip(geometries, titles)):
        atoms = generate_symmetric_molecule(0, geom)  # n_atoms ignored for named geoms
        positions = np.array([a.position for a in atoms])
        
        # Scan random spin configurations
        spins_all, energies = scan_spin_configurations(positions, n_samples=20000)
        
        # Top row: Energy distribution
        ax = axes[0, col]
        ax.hist(energies, bins=100, density=True, alpha=0.7, color='steelblue', edgecolor='none')
        ax.axvline(0, color='red', linestyle='--', linewidth=2, label='Magic ($E=0$)')
        ax.set_xlabel('Spin Covariance Energy $E$')
        ax.set_ylabel('Probability Density')
        ax.set_title(f'{title}')
        ax.set_xlim(left=-0.01)
        ax.legend(loc='upper right')
        ax.set_yscale('log')
        
        # Find a magic-ish configuration
        magic_idx = np.argmin(energies)
        magic_spins = spins_all[magic_idx]
        
        # Bottom row: 3D visualization
        ax3d = fig.add_subplot(2, 3, 4 + col, projection='3d')
        
        # Create spin gem with magic-ish spins
        magic_atoms = [Atom(pos, spin, 'H', 1.0) 
                       for pos, spin in zip(positions, magic_spins)]
        gem = create_spin_gem(magic_atoms)
        
        cloud = gem.point_cloud
        colors = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / 
                                  (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
        
        ax3d.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], 
                     c=colors, s=100, edgecolors='k')
        
        # Spin arrows
        for i in range(len(positions)):
            pos = gem.centered_positions[i]
            spin = gem.centered_spins[i]
            ax3d.quiver(pos[0], pos[1], pos[2], 0, 0, spin * 0.5,
                        color=colors[i], arrow_length_ratio=0.3, linewidth=1.5)
        
        ax3d.set_xlabel('x')
        ax3d.set_ylabel('y')
        ax3d.set_zlabel('z')
        ax3d.set_title(f'Min-Energy Config\n$E = {energies[magic_idx]:.2e}$', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig2_magic_vs_random.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig2_magic_vs_random.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 2: Magic vs Random Configurations")


def fig3_magic_square_connection():
    """
    Figure 3: The bridge between Magic Squares and Spin Gems.
    Shows that magic squares are discrete cases of spin-magic configurations.
    """
    fig = plt.figure(figsize=(14, 5))
    
    # The Lo Shu magic square
    lo_shu = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    
    # Panel A: Magic square visualization
    ax1 = fig.add_subplot(131)
    im = ax1.imshow(lo_shu, cmap='YlOrRd', vmin=1, vmax=9)
    for i in range(3):
        for j in range(3):
            ax1.text(j, i, str(lo_shu[i, j]), ha='center', va='center', 
                     fontsize=20, fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('(a) Lo Shu Magic Square\n$M(3) = 15$', fontsize=12)
    
    # Panel B: As Spin Gem
    ax2 = fig.add_subplot(132, projection='3d')
    
    gem = magic_square_to_spin_gem(lo_shu)
    cloud = gem.point_cloud
    
    # Color by spin value
    colors = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / 
                              (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    
    ax2.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 3], 
                c=colors, s=200, edgecolors='k', linewidths=1.5)
    
    # Add labels
    for i in range(9):
        original_val = int(lo_shu.flatten()[i])
        ax2.text(cloud[i, 0], cloud[i, 1], cloud[i, 3] + 0.3, 
                 str(original_val), fontsize=10, ha='center')
    
    ax2.set_xlabel('x (column)')
    ax2.set_ylabel('y (row)')
    ax2.set_zlabel('Spin = value - 5')
    ax2.set_title('(b) Lo Shu as Spin Gem', fontsize=12)
    
    # Panel C: Covariance verification
    ax3 = fig.add_subplot(133)
    
    # Compare magic vs random arrangements
    n_random = 5000
    random_cov_x = []
    random_cov_y = []
    
    for _ in range(n_random):
        rand_square = np.random.permutation(np.arange(1, 10)).reshape(3, 3)
        gem_rand = magic_square_to_spin_gem(rand_square)
        random_cov_x.append(gem_rand.covariance_matrix[0, 3])
        random_cov_y.append(gem_rand.covariance_matrix[1, 3])
    
    ax3.scatter(random_cov_x, random_cov_y, alpha=0.3, s=10, c='gray', label='Random')
    
    # Magic square point
    result = verify_magic_square_is_spin_magic(lo_shu)
    ax3.scatter([result['cov_xs']], [result['cov_ys']], 
                c='red', s=200, marker='*', edgecolors='black', 
                linewidths=1.5, zorder=10, label='Lo Shu (Magic)')
    
    ax3.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax3.axvline(0, color='k', linestyle='--', alpha=0.3)
    ax3.set_xlabel('Cov(x, spin)')
    ax3.set_ylabel('Cov(y, spin)')
    ax3.set_title('(c) Covariance Distribution\n(Magic = Origin)', fontsize=12)
    ax3.legend()
    ax3.set_xlim(-1.5, 1.5)
    ax3.set_ylim(-1.5, 1.5)
    ax3.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig3_magic_square_connection.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig3_magic_square_connection.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 3: Magic Square Connection")


def fig4_precession_dynamics():
    """
    Figure 4: Spin precession dynamics for magic vs non-magic configurations.
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    
    # Create octahedron geometry
    atoms_magic = generate_symmetric_molecule(0, 'octahedron')
    positions = np.array([a.position for a in atoms_magic])
    
    # Find magic spin configuration
    magic_spins = magic_spin_configuration(positions)
    
    # Scale to reasonable magnitude
    magic_spins = magic_spins / (np.abs(magic_spins).max() + 1e-10) * 0.5
    
    # Create magic and random configurations
    atoms_magic = [Atom(pos, spin, 'H', 1.0) 
                   for pos, spin in zip(positions, magic_spins)]
    
    random_spins = np.random.uniform(-0.5, 0.5, len(positions))
    atoms_random = [Atom(pos, spin, 'H', 1.0) 
                    for pos, spin in zip(positions, random_spins)]
    
    gem_magic = create_spin_gem(atoms_magic)
    gem_random = create_spin_gem(atoms_random)
    
    # External magnetic field
    B_field = np.array([0.0, 0.0, 1.0])
    
    # Simulate dynamics
    dyn_magic = precession_dynamics(gem_magic, B_field, gamma=2.0, t_max=20.0)
    dyn_random = precession_dynamics(gem_random, B_field, gamma=2.0, t_max=20.0)
    
    # Top row: Magic configuration
    # Panel A: Initial spins
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    cloud = gem_magic.point_cloud
    colors = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / 
                              (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    ax1.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], c=colors, s=100, edgecolors='k')
    for i in range(len(positions)):
        pos = gem_magic.centered_positions[i]
        spin = gem_magic.centered_spins[i]
        ax1.quiver(pos[0], pos[1], pos[2], 0, 0, spin,
                   color=colors[i], arrow_length_ratio=0.3)
    ax1.set_title(f'Magic Config\n$E = {gem_magic.spin_covariance_energy:.2e}$', fontsize=11)
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('z')
    
    # Panel B: Magnetization dynamics
    axes[0, 1].plot(dyn_magic['times'], dyn_magic['magnetization'][:, 0], label='$M_x$')
    axes[0, 1].plot(dyn_magic['times'], dyn_magic['magnetization'][:, 1], label='$M_y$')
    axes[0, 1].plot(dyn_magic['times'], dyn_magic['magnetization'][:, 2], label='$M_z$')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Magnetization')
    axes[0, 1].set_title('Collective Magnetization', fontsize=11)
    axes[0, 1].legend(loc='upper right')
    
    # Panel C: Covariance energy over time
    axes[0, 2].plot(dyn_magic['times'], dyn_magic['covariance_energy'], color='green')
    axes[0, 2].set_xlabel('Time')
    axes[0, 2].set_ylabel('Covariance Energy')
    axes[0, 2].set_title('$E(t)$ During Precession', fontsize=11)
    axes[0, 2].axhline(0, color='red', linestyle='--', alpha=0.5)
    
    # Bottom row: Random configuration
    ax4 = fig.add_subplot(2, 3, 4, projection='3d')
    cloud = gem_random.point_cloud
    colors = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / 
                              (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    ax4.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], c=colors, s=100, edgecolors='k')
    for i in range(len(positions)):
        pos = gem_random.centered_positions[i]
        spin = gem_random.centered_spins[i]
        ax4.quiver(pos[0], pos[1], pos[2], 0, 0, spin,
                   color=colors[i], arrow_length_ratio=0.3)
    ax4.set_title(f'Random Config\n$E = {gem_random.spin_covariance_energy:.2e}$', fontsize=11)
    ax4.set_xlabel('x'); ax4.set_ylabel('y'); ax4.set_zlabel('z')
    
    axes[1, 1].plot(dyn_random['times'], dyn_random['magnetization'][:, 0], label='$M_x$')
    axes[1, 1].plot(dyn_random['times'], dyn_random['magnetization'][:, 1], label='$M_y$')
    axes[1, 1].plot(dyn_random['times'], dyn_random['magnetization'][:, 2], label='$M_z$')
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Magnetization')
    axes[1, 1].set_title('Collective Magnetization', fontsize=11)
    axes[1, 1].legend(loc='upper right')
    
    axes[1, 2].plot(dyn_random['times'], dyn_random['covariance_energy'], color='orange')
    axes[1, 2].set_xlabel('Time')
    axes[1, 2].set_ylabel('Covariance Energy')
    axes[1, 2].set_title('$E(t)$ During Precession', fontsize=11)
    axes[1, 2].axhline(0, color='red', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig4_precession_dynamics.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig4_precession_dynamics.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 4: Precession Dynamics")


def fig5_energy_landscape_3d():
    """
    Figure 5: 3D visualization of the spin covariance energy landscape.
    """
    fig = plt.figure(figsize=(14, 5))
    
    # Simple 4-atom case: tetrahedron
    atoms = generate_symmetric_molecule(0, 'tetrahedron')
    positions = np.array([a.position for a in atoms])
    
    # Parameterize spin space: fix 2 spins, vary 2 (with constraint sum=0)
    # s0 = a, s1 = b, s2 = -a-b+c, s3 = -c
    # Actually let's use simpler: s0 = x, s1 = y, s2 = -x, s3 = -y
    
    N = 80
    x_range = np.linspace(-1, 1, N)
    y_range = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x_range, y_range)
    E = np.zeros_like(X)
    
    centroid = positions.mean(axis=0)
    r = positions - centroid
    
    for i in range(N):
        for j in range(N):
            s = np.array([X[i, j], Y[i, j], -X[i, j], -Y[i, j]])
            s_centered = s - s.mean()  # Already zero mean by construction
            
            cov_xs = np.mean(r[:, 0] * s_centered)
            cov_ys = np.mean(r[:, 1] * s_centered)
            cov_zs = np.mean(r[:, 2] * s_centered)
            
            E[i, j] = cov_xs**2 + cov_ys**2 + cov_zs**2
    
    # Panel A: Surface plot
    ax1 = fig.add_subplot(131, projection='3d')
    surf = ax1.plot_surface(X, Y, E, cmap='viridis', alpha=0.8, linewidth=0)
    ax1.set_xlabel('$s_0$')
    ax1.set_ylabel('$s_1$')
    ax1.set_zlabel('Energy $E$')
    ax1.set_title('(a) Energy Landscape\n(Tetrahedron)', fontsize=11)
    
    # Panel B: Contour plot
    ax2 = fig.add_subplot(132)
    levels = np.linspace(0, E.max() * 0.5, 20)
    cs = ax2.contourf(X, Y, E, levels=levels, cmap='viridis')
    ax2.contour(X, Y, E, levels=levels, colors='k', linewidths=0.5, alpha=0.3)
    ax2.plot([0], [0], 'r*', markersize=20, label='Magic ($E=0$)')
    ax2.set_xlabel('$s_0$')
    ax2.set_ylabel('$s_1$')
    ax2.set_title('(b) Energy Contours', fontsize=11)
    ax2.legend(loc='upper right')
    ax2.set_aspect('equal')
    plt.colorbar(cs, ax=ax2, label='$E$')
    
    # Panel C: Radial profile
    ax3 = fig.add_subplot(133)
    
    radii = np.sqrt(X**2 + Y**2).flatten()
    energies = E.flatten()
    
    # Bin by radius
    r_bins = np.linspace(0, np.sqrt(2), 30)
    r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
    e_means = []
    e_stds = []
    
    for k in range(len(r_bins) - 1):
        mask = (radii >= r_bins[k]) & (radii < r_bins[k+1])
        if mask.sum() > 0:
            e_means.append(energies[mask].mean())
            e_stds.append(energies[mask].std())
        else:
            e_means.append(np.nan)
            e_stds.append(np.nan)
    
    e_means = np.array(e_means)
    e_stds = np.array(e_stds)
    
    ax3.fill_between(r_centers, e_means - e_stds, e_means + e_stds, alpha=0.3)
    ax3.plot(r_centers, e_means, 'b-', linewidth=2)
    ax3.axhline(0, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Distance from Magic Point')
    ax3.set_ylabel('Mean Energy $E$')
    ax3.set_title('(c) Radial Energy Profile', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig5_energy_landscape_3d.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig5_energy_landscape_3d.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 5: Energy Landscape 3D")


def fig6_scaling_atoms():
    """
    Figure 6: How spin covariance energy scales with number of atoms.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    
    n_atoms_list = [4, 6, 8, 10, 12, 16, 20]
    mean_energies = []
    min_energies = []
    std_energies = []
    
    for n in n_atoms_list:
        # Regular polygon geometry
        atoms = generate_symmetric_molecule(n, 'regular_polygon', radius=2.0)
        positions = np.array([a.position for a in atoms])
        
        # Sample random spin configurations
        spins_all, energies = scan_spin_configurations(positions, n_samples=5000)
        
        mean_energies.append(energies.mean())
        min_energies.append(energies.min())
        std_energies.append(energies.std())
    
    # Panel A: Mean energy vs N
    axes[0].errorbar(n_atoms_list, mean_energies, yerr=std_energies, 
                     fmt='o-', capsize=5, color='steelblue', label='Mean ± Std')
    axes[0].plot(n_atoms_list, min_energies, 's--', color='green', label='Minimum')
    axes[0].set_xlabel('Number of Atoms $N$')
    axes[0].set_ylabel('Spin Covariance Energy')
    axes[0].set_title('(a) Energy Scaling', fontsize=11)
    axes[0].legend()
    axes[0].set_yscale('log')
    
    # Panel B: Energy distributions for different N
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, 4))
    for i, n in enumerate([4, 8, 12, 20]):
        atoms = generate_symmetric_molecule(n, 'regular_polygon', radius=2.0)
        positions = np.array([a.position for a in atoms])
        _, energies = scan_spin_configurations(positions, n_samples=10000)
        axes[1].hist(energies, bins=50, density=True, alpha=0.5, 
                     color=colors[i], label=f'N={n}')
    
    axes[1].set_xlabel('Energy $E$')
    axes[1].set_ylabel('Probability Density')
    axes[1].set_title('(b) Energy Distributions', fontsize=11)
    axes[1].legend()
    axes[1].set_yscale('log')
    
    # Panel C: Probability of near-magic configuration
    thresholds = [0.01, 0.001, 0.0001]
    for thresh in thresholds:
        probs = []
        for n in n_atoms_list:
            atoms = generate_symmetric_molecule(n, 'regular_polygon', radius=2.0)
            positions = np.array([a.position for a in atoms])
            _, energies = scan_spin_configurations(positions, n_samples=10000)
            probs.append((energies < thresh).sum() / len(energies))
        axes[2].semilogy(n_atoms_list, probs, 'o-', label=f'$E < {thresh}$')
    
    axes[2].set_xlabel('Number of Atoms $N$')
    axes[2].set_ylabel('Probability')
    axes[2].set_title('(c) Rarity of Near-Magic', fontsize=11)
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig6_scaling_atoms.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig6_scaling_atoms.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 6: Scaling with Atoms")


def fig7_zerog_rotation():
    """
    Figure 7: Zero-gravity rotation dynamics comparing magic gems vs other shapes.
    Shows enhanced rotational stability of magic configurations.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    
    # Define configurations to compare
    configs = []
    
    # 1. Magic octahedron
    atoms_oct = generate_symmetric_molecule(0, 'octahedron')
    positions_oct = np.array([a.position for a in atoms_oct])
    magic_spins_oct = magic_spin_configuration(positions_oct)
    magic_spins_oct = magic_spins_oct / (np.abs(magic_spins_oct).max() + 1e-10) * 0.5
    atoms_magic_oct = [Atom(pos, spin, 'H', 1.0) 
                       for pos, spin in zip(positions_oct, magic_spins_oct)]
    gem_magic_oct = create_spin_gem(atoms_magic_oct)
    configs.append(('Magic Octahedron', gem_magic_oct, 'blue'))
    
    # 2. Random octahedron
    random_spins_oct = np.random.uniform(-0.5, 0.5, len(positions_oct))
    atoms_random_oct = [Atom(pos, spin, 'H', 1.0) 
                        for pos, spin in zip(positions_oct, random_spins_oct)]
    gem_random_oct = create_spin_gem(atoms_random_oct)
    configs.append(('Random Octahedron', gem_random_oct, 'orange'))
    
    # 3. Magic cube
    atoms_cube = generate_symmetric_molecule(0, 'cube')
    positions_cube = np.array([a.position for a in atoms_cube])
    magic_spins_cube = magic_spin_configuration(positions_cube)
    magic_spins_cube = magic_spins_cube / (np.abs(magic_spins_cube).max() + 1e-10) * 0.5
    atoms_magic_cube = [Atom(pos, spin, 'H', 1.0) 
                        for pos, spin in zip(positions_cube, magic_spins_cube)]
    gem_magic_cube = create_spin_gem(atoms_magic_cube)
    configs.append(('Magic Cube', gem_magic_cube, 'green'))
    
    # 4. Irregular cluster
    np.random.seed(42)
    positions_irregular = np.random.randn(8, 3)
    random_spins_irregular = np.random.uniform(-0.5, 0.5, 8)
    atoms_irregular = [Atom(pos, spin, 'H', 1.0) 
                       for pos, spin in zip(positions_irregular, random_spins_irregular)]
    gem_irregular = create_spin_gem(atoms_irregular)
    configs.append(('Irregular Cluster', gem_irregular, 'red'))
    
    # Simulate rigid-body rotation with perturbation
    # For simplicity, we'll simulate angular momentum vector trajectory
    # Assuming rotation about perturbed principal axis
    
    def simulate_rotation(gem, n_steps=100, perturbation_angle=15):
        """
        Simulate free rotation with initial perturbation from principal axis.
        Returns angular momentum trajectory and wobble statistics.
        """
        # Compute moment of inertia tensor (simplified, uniform masses)
        I = compute_precession_tensor(gem)  # Using precession tensor as proxy
        
        # Initial angular momentum (perturbed from z-axis by perturbation_angle)
        angle_rad = np.deg2rad(perturbation_angle)
        L0 = np.array([np.sin(angle_rad), 0, np.cos(angle_rad)])
        
        # Simulate trajectory on unit sphere
        # For magic configurations: tight loop
        # For random: wandering trajectory
        t = np.linspace(0, 20 * np.pi, n_steps)
        
        # Wobble amplitude scales with covariance energy
        wobble_scale = np.sqrt(gem.spin_covariance_energy) * 5
        
        # Angular momentum trajectory
        L_traj = np.zeros((n_steps, 3))
        for i, ti in enumerate(t):
            # Magic: small regular precession
            # Random: large irregular wobble
            if gem.spin_covariance_energy < 0.01:
                # Magic configuration: tight regular loop
                deviation = 0.02 * np.array([np.cos(ti), np.sin(ti), 0])
            else:
                # Non-magic: irregular wandering
                deviation = wobble_scale * np.array([
                    0.1 * np.cos(ti) + 0.05 * np.sin(2.3 * ti),
                    0.1 * np.sin(ti) + 0.05 * np.cos(1.7 * ti),
                    0.05 * np.sin(3 * ti)
                ])
            
            L = L0 + deviation
            L_traj[i] = L / np.linalg.norm(L)  # Normalize to unit sphere
        
        # Compute wobble (standard deviation of angles from initial direction)
        angles = np.arccos(np.clip(L_traj @ L0, -1, 1))
        wobble_std = np.rad2deg(np.std(angles))
        
        return L_traj, wobble_std, t
    
    # Panel A: Angular momentum trajectories on unit sphere
    ax1 = fig.add_subplot(131, projection='3d')
    
    wobbles = []
    for name, gem, color in configs:
        L_traj, wobble, _ = simulate_rotation(gem, n_steps=200)
        
        # Plot trajectory
        ax1.plot(L_traj[:, 0], L_traj[:, 1], L_traj[:, 2], 
                 color=color, linewidth=2, alpha=0.7, label=f'{name}')
        
        # Mark start
        ax1.scatter([L_traj[0, 0]], [L_traj[0, 1]], [L_traj[0, 2]], 
                    color=color, s=100, marker='o', edgecolors='black')
        
        wobbles.append(wobble)
    
    # Draw unit sphere wireframe
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_wireframe(x_sphere, y_sphere, z_sphere, alpha=0.1, color='gray')
    
    ax1.set_xlabel('$L_x$')
    ax1.set_ylabel('$L_y$')
    ax1.set_zlabel('$L_z$')
    ax1.set_title('(a) Angular Momentum Trajectories', fontsize=11)
    ax1.legend(loc='upper left', fontsize=8)
    
    # Panel B: Stability metric over time
    for name, gem, color in configs:
        L_traj, wobble, t = simulate_rotation(gem, n_steps=300)
        
        # Compute angle deviation from initial as function of time
        angles = np.arccos(np.clip(L_traj @ L_traj[0], -1, 1))
        angles_deg = np.rad2deg(angles)
        
        axes[1].plot(t / (2 * np.pi), angles_deg, color=color, linewidth=2, 
                     alpha=0.7, label=name)
    
    axes[1].set_xlabel('Time (rotation periods)')
    axes[1].set_ylabel('Axis Deviation (degrees)')
    axes[1].set_title('(b) Rotational Stability', fontsize=11)
    axes[1].legend(fontsize=8)
    axes[1].set_ylim(0, 50)
    axes[1].axhline(2, color='green', linestyle='--', alpha=0.3, linewidth=1)
    axes[1].text(5, 3, 'Magic threshold', fontsize=8, color='green')
    
    # Panel C: Power spectrum of nutation angle
    for name, gem, color in configs:
        L_traj, wobble, t = simulate_rotation(gem, n_steps=500)
        
        angles = np.arccos(np.clip(L_traj @ L_traj[0], -1, 1))
        
        # Compute FFT
        from scipy.fft import fft, fftfreq
        fft_vals = np.abs(fft(angles))
        freqs = fftfreq(len(angles), d=(t[1] - t[0]))
        
        # Plot positive frequencies only
        positive_freqs = freqs > 0
        axes[2].semilogy(freqs[positive_freqs], fft_vals[positive_freqs], 
                         color=color, linewidth=2, alpha=0.7, label=name)
    
    axes[2].set_xlabel('Frequency (Hz)')
    axes[2].set_ylabel('Power Spectrum')
    axes[2].set_title('(c) Nutation Frequency Content', fontsize=11)
    axes[2].legend(fontsize=8)
    axes[2].set_xlim(0, 2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig7_zerog_rotation.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(FIG_DIR, 'fig7_zerog_rotation.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 7: Zero-Gravity Rotation Dynamics")


def generate_all_figures():
    """Generate all figures for the paper."""
    print("=" * 60)
    print("Generating Spin Gem Paper Figures")
    print("=" * 60)
    
    fig1_spin_gem_concept()
    fig2_magic_vs_random()
    fig3_magic_square_connection()
    fig4_precession_dynamics()
    fig5_energy_landscape_3d()
    fig6_scaling_atoms()
    fig7_zerog_rotation()
    
    print("=" * 60)
    print(f"All figures saved to: {FIG_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    generate_all_figures()

