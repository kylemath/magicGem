"""
Generate figures for the Spin Gem paper.
Author: George R., December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spin_gem_core import (
    Atom, SpinGem, create_spin_gem, generate_symmetric_molecule,
    magic_square_to_spin_gem, precession_dynamics
)

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'


def fig1_spin_gem_concept():
    """Figure 1: Conceptual illustration of Spin Gems."""
    fig = plt.figure(figsize=(14, 5))
    
    atoms = generate_symmetric_molecule(6, 'regular_polygon', radius=1.5)
    positions = np.array([a.position for a in atoms])
    spins = np.array([a.spin for a in atoms])
    
    # Panel A: Molecule with spin arrows
    ax1 = fig.add_subplot(131, projection='3d')
    colors = plt.cm.coolwarm((spins - spins.min()) / (spins.max() - spins.min() + 1e-10))
    ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c=colors, s=200, edgecolors='k')
    for i, (pos, spin) in enumerate(zip(positions, spins)):
        ax1.quiver(pos[0], pos[1], pos[2], 0, 0, spin * 2, color=colors[i], arrow_length_ratio=0.3)
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('z')
    ax1.set_title('(a) Hexagonal Molecule')
    
    # Panel B: Spin Gem
    ax2 = fig.add_subplot(132, projection='3d')
    gem = create_spin_gem(atoms)
    cloud = gem.point_cloud
    colors2 = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    ax2.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 3], c=colors2, s=150, edgecolors='k')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('Spin')
    ax2.set_title('(b) Spin Gem Point Cloud')
    
    # Panel C: Covariance matrix
    ax3 = fig.add_subplot(133)
    cov = gem.covariance_matrix
    im = ax3.imshow(cov, cmap='RdBu_r', vmin=-np.abs(cov).max(), vmax=np.abs(cov).max())
    ax3.set_xticks([0, 1, 2, 3]); ax3.set_xticklabels(['x', 'y', 'z', 's'])
    ax3.set_yticks([0, 1, 2, 3]); ax3.set_yticklabels(['x', 'y', 'z', 's'])
    ax3.set_title('(c) Covariance Matrix')
    for i in range(4):
        for j in range(4):
            ax3.text(j, i, f'{cov[i,j]:.2f}', ha='center', va='center', fontsize=9)
    plt.colorbar(im, ax=ax3, fraction=0.046)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig1_spin_gem_concept.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 1")


def fig2_magic_vs_random():
    """Figure 2: Magic vs random configurations."""
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    geometries = ['tetrahedron', 'octahedron', 'cube']
    
    for col, geom in enumerate(geometries):
        atoms = generate_symmetric_molecule(0, geom)
        positions = np.array([a.position for a in atoms])
        
        # Sample random spins
        energies = []
        for _ in range(5000):
            spins = np.random.uniform(-1, 1, len(positions))
            temp_atoms = [Atom(pos, spin, 'H', 1.0) for pos, spin in zip(positions, spins)]
            gem = create_spin_gem(temp_atoms)
            energies.append(gem.spin_covariance_energy)
        
        axes[0, col].hist(energies, bins=50, density=True, alpha=0.7, color='steelblue')
        axes[0, col].axvline(0, color='red', linestyle='--', linewidth=2, label='Magic')
        axes[0, col].set_xlabel('Energy E')
        axes[0, col].set_ylabel('Density')
        axes[0, col].set_title(f'{geom.capitalize()}')
        axes[0, col].set_yscale('log')
        axes[0, col].legend()
        
        # Best configuration
        best_idx = np.argmin(energies)
        ax3d = fig.add_subplot(2, 3, 4 + col, projection='3d')
        ax3d.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=100, c='steelblue')
        ax3d.set_title(f'Min E = {energies[best_idx]:.2e}')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig2_magic_vs_random.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 2")


def fig3_magic_square_connection():
    """Figure 3: Magic square connection."""
    fig = plt.figure(figsize=(14, 5))
    lo_shu = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    
    # Panel A: Magic square
    ax1 = fig.add_subplot(131)
    ax1.imshow(lo_shu, cmap='YlOrRd', vmin=1, vmax=9)
    for i in range(3):
        for j in range(3):
            ax1.text(j, i, str(lo_shu[i, j]), ha='center', va='center', fontsize=20, fontweight='bold')
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_title('(a) Lo Shu Magic Square')
    
    # Panel B: As Spin Gem
    ax2 = fig.add_subplot(132, projection='3d')
    gem = magic_square_to_spin_gem(lo_shu)
    cloud = gem.point_cloud
    colors = plt.cm.coolwarm((cloud[:, 3] - cloud[:, 3].min()) / (cloud[:, 3].max() - cloud[:, 3].min() + 1e-10))
    ax2.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 3], c=colors, s=200, edgecolors='k')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('Spin')
    ax2.set_title('(b) Lo Shu as Spin Gem')
    
    # Panel C: Covariance distribution
    ax3 = fig.add_subplot(133)
    cov_x, cov_y = [], []
    for _ in range(500):
        arr = np.random.permutation(np.arange(1, 10)).reshape(3, 3)
        g = magic_square_to_spin_gem(arr)
        cov_x.append(g.covariance_matrix[0, 3])
        cov_y.append(g.covariance_matrix[1, 3])
    ax3.scatter(cov_x, cov_y, alpha=0.3, s=10, c='gray', label='Random')
    ax3.scatter([0], [0], c='red', s=200, marker='*', label='Lo Shu')
    ax3.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax3.axvline(0, color='k', linestyle='--', alpha=0.3)
    ax3.set_xlabel('Cov(x, spin)'); ax3.set_ylabel('Cov(y, spin)')
    ax3.set_title('(c) Covariance Distribution')
    ax3.legend()
    ax3.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig3_magic_square_connection.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 3")


def fig4_precession_dynamics():
    """Figure 4: Precession dynamics."""
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    
    atoms = generate_symmetric_molecule(0, 'octahedron')
    gem = create_spin_gem(atoms)
    B_field = np.array([0.0, 0.0, 1.0])
    dyn = precession_dynamics(gem, B_field, gamma=2.0, t_max=20.0)
    
    # Top row: balanced
    axes[0, 0].set_title('Magic Config (Initial)')
    axes[0, 1].plot(dyn['times'], dyn['magnetization'][:, 0], label='Mx')
    axes[0, 1].plot(dyn['times'], dyn['magnetization'][:, 1], label='My')
    axes[0, 1].plot(dyn['times'], dyn['magnetization'][:, 2], label='Mz')
    axes[0, 1].set_xlabel('Time'); axes[0, 1].set_ylabel('Magnetization')
    axes[0, 1].legend()
    axes[0, 2].plot(dyn['times'], dyn['covariance_energy'], color='green')
    axes[0, 2].set_xlabel('Time'); axes[0, 2].set_ylabel('Energy E(t)')
    
    # Bottom row: random
    for a in atoms:
        a.spin = np.random.uniform(-0.5, 0.5)
    gem_rand = create_spin_gem(atoms)
    dyn_rand = precession_dynamics(gem_rand, B_field, gamma=2.0, t_max=20.0)
    
    axes[1, 0].set_title('Random Config (Initial)')
    axes[1, 1].plot(dyn_rand['times'], dyn_rand['magnetization'][:, 0], label='Mx')
    axes[1, 1].plot(dyn_rand['times'], dyn_rand['magnetization'][:, 1], label='My')
    axes[1, 1].plot(dyn_rand['times'], dyn_rand['magnetization'][:, 2], label='Mz')
    axes[1, 1].set_xlabel('Time'); axes[1, 1].legend()
    axes[1, 2].plot(dyn_rand['times'], dyn_rand['covariance_energy'], color='orange')
    axes[1, 2].set_xlabel('Time')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig4_precession_dynamics.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 4")


def fig5_energy_landscape():
    """Figure 5: Energy landscape."""
    fig = plt.figure(figsize=(14, 5))
    
    tetra_pos = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) / np.sqrt(3)
    
    N = 50
    x_range = np.linspace(-1, 1, N)
    y_range = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x_range, y_range)
    E = np.zeros_like(X)
    
    for i in range(N):
        for j in range(N):
            spins = [X[i, j], Y[i, j], -X[i, j], -Y[i, j]]
            atoms = [Atom(pos, s, 'H', 1.0) for pos, s in zip(tetra_pos, spins)]
            gem = create_spin_gem(atoms)
            E[i, j] = gem.spin_covariance_energy
    
    # Surface
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot_surface(X, Y, E, cmap='viridis', alpha=0.8)
    ax1.set_xlabel('s₀'); ax1.set_ylabel('s₁'); ax1.set_zlabel('E')
    ax1.set_title('(a) Energy Surface')
    
    # Contour
    ax2 = fig.add_subplot(132)
    ax2.contourf(X, Y, E, levels=20, cmap='viridis')
    ax2.plot([0], [0], 'r*', markersize=15, label='Magic')
    ax2.set_xlabel('s₀'); ax2.set_ylabel('s₁')
    ax2.set_title('(b) Contours'); ax2.legend()
    
    # Radial
    ax3 = fig.add_subplot(133)
    radii = np.sqrt(X**2 + Y**2).flatten()
    energies = E.flatten()
    ax3.scatter(radii, energies, alpha=0.3, s=5)
    ax3.set_xlabel('Distance from Origin'); ax3.set_ylabel('Energy')
    ax3.set_title('(c) Radial Profile')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig5_energy_landscape_3d.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 5")


def fig6_scaling():
    """Figure 6: Scaling with atoms."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    
    n_list = [4, 6, 8, 10, 12, 16]
    means, mins = [], []
    
    for n in n_list:
        atoms = generate_symmetric_molecule(n, 'regular_polygon', radius=2.0)
        positions = np.array([a.position for a in atoms])
        energies = []
        for _ in range(2000):
            spins = np.random.uniform(-1, 1, n)
            temp_atoms = [Atom(pos, s, 'H', 1.0) for pos, s in zip(positions, spins)]
            gem = create_spin_gem(temp_atoms)
            energies.append(gem.spin_covariance_energy)
        means.append(np.mean(energies))
        mins.append(np.min(energies))
    
    axes[0].plot(n_list, means, 'o-', label='Mean')
    axes[0].plot(n_list, mins, 's--', label='Min')
    axes[0].set_xlabel('N atoms'); axes[0].set_ylabel('Energy')
    axes[0].set_title('(a) Scaling')
    axes[0].legend()
    axes[0].set_yscale('log')
    
    # Distributions
    for n in [4, 8, 12]:
        atoms = generate_symmetric_molecule(n, 'regular_polygon')
        positions = np.array([a.position for a in atoms])
        energies = []
        for _ in range(3000):
            spins = np.random.uniform(-1, 1, n)
            temp_atoms = [Atom(pos, s, 'H', 1.0) for pos, s in zip(positions, spins)]
            gem = create_spin_gem(temp_atoms)
            energies.append(gem.spin_covariance_energy)
        axes[1].hist(energies, bins=30, density=True, alpha=0.5, label=f'N={n}')
    axes[1].set_xlabel('Energy'); axes[1].set_ylabel('Density')
    axes[1].set_title('(b) Distributions'); axes[1].legend()
    axes[1].set_yscale('log')
    
    # Probability
    thresholds = [0.01, 0.001]
    for thresh in thresholds:
        probs = []
        for n in n_list:
            atoms = generate_symmetric_molecule(n, 'regular_polygon')
            positions = np.array([a.position for a in atoms])
            count = 0
            for _ in range(5000):
                spins = np.random.uniform(-1, 1, n)
                temp_atoms = [Atom(pos, s, 'H', 1.0) for pos, s in zip(positions, spins)]
                gem = create_spin_gem(temp_atoms)
                if gem.spin_covariance_energy < thresh:
                    count += 1
            probs.append(count / 5000)
        axes[2].semilogy(n_list, probs, 'o-', label=f'E < {thresh}')
    axes[2].set_xlabel('N atoms'); axes[2].set_ylabel('Probability')
    axes[2].set_title('(c) Rarity'); axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig6_scaling_atoms.png'), bbox_inches='tight')
    plt.close()
    print("Created Figure 6")


if __name__ == '__main__':
    print("Generating Spin Gem Figures")
    print("=" * 50)
    fig1_spin_gem_concept()
    fig2_magic_vs_random()
    fig3_magic_square_connection()
    fig4_precession_dynamics()
    fig5_energy_landscape()
    fig6_scaling()
    print("=" * 50)
    print(f"Figures saved to: {FIG_DIR}")
