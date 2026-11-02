"""
Spin Gems: Extending Magic Gem Framework to Molecular Spin Precession

Core module defining the Spin Gem representation and covariance analysis
for atomic spin configurations in molecules.

Author: George R.
Date: December 2025
"""

import numpy as np
from typing import Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class Atom:
    """Represents an atom with position and spin state."""
    position: np.ndarray  # (x, y, z) in Angstroms
    spin: float           # Spin projection S_z (in units of hbar)
    element: str          # Element symbol
    mass: float           # Atomic mass (amu)
    

@dataclass 
class SpinGem:
    """A Spin Gem: geometric representation of a molecular spin configuration."""
    atoms: List[Atom]
    centered_positions: np.ndarray   # N x 3 array, centered
    centered_spins: np.ndarray       # N array, centered
    point_cloud: np.ndarray          # N x 4 array: (x, y, z, s)
    covariance_matrix: np.ndarray    # 4 x 4 covariance matrix
    spin_covariance_energy: float    # Sum of Cov(x,s)^2 + Cov(y,s)^2 + Cov(z,s)^2
    

def create_spin_gem(atoms: List[Atom]) -> SpinGem:
    """Construct a Spin Gem from a list of atoms."""
    N = len(atoms)
    positions = np.array([a.position for a in atoms])
    spins = np.array([a.spin for a in atoms])
    
    # Center positions at centroid
    centroid = positions.mean(axis=0)
    centered_positions = positions - centroid
    
    # Center spins at mean
    mean_spin = spins.mean()
    centered_spins = spins - mean_spin
    
    # Construct 4D point cloud: (x, y, z, s)
    point_cloud = np.column_stack([centered_positions, centered_spins])
    
    # Compute covariance matrix
    cov_matrix = np.cov(point_cloud.T, bias=True)
    
    # Spin covariance energy
    cov_xs = cov_matrix[0, 3]
    cov_ys = cov_matrix[1, 3]
    cov_zs = cov_matrix[2, 3]
    spin_cov_energy = cov_xs**2 + cov_ys**2 + cov_zs**2
    
    return SpinGem(
        atoms=atoms,
        centered_positions=centered_positions,
        centered_spins=centered_spins,
        point_cloud=point_cloud,
        covariance_matrix=cov_matrix,
        spin_covariance_energy=spin_cov_energy
    )


def generate_symmetric_molecule(n_atoms: int, 
                                 geometry: str = 'regular_polygon',
                                 radius: float = 1.5) -> List[Atom]:
    """Generate atoms in symmetric geometric arrangements."""
    atoms = []
    
    if geometry == 'regular_polygon':
        angles = np.linspace(0, 2*np.pi, n_atoms, endpoint=False)
        for i, theta in enumerate(angles):
            pos = np.array([radius * np.cos(theta), 
                           radius * np.sin(theta), 0.0])
            spin = 0.5 if i % 2 == 0 else -0.5
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'tetrahedron':
        vertices = np.array([
            [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
        ]) * radius / np.sqrt(3)
        spins = [0.5, 0.5, -0.5, -0.5]
        for pos, spin in zip(vertices, spins):
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'octahedron':
        vertices = np.array([
            [1, 0, 0], [-1, 0, 0], [0, 1, 0], 
            [0, -1, 0], [0, 0, 1], [0, 0, -1]
        ]) * radius
        spins = [0.5, -0.5, 0.5, -0.5, 0.5, -0.5]
        for pos, spin in zip(vertices, spins):
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'cube':
        vertices = np.array([
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
        ]) * radius / np.sqrt(3)
        spins = [0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5]
        for pos, spin in zip(vertices, spins):
            atoms.append(Atom(pos, spin, 'H', 1.008))
    
    return atoms


def magic_square_to_spin_gem(magic_square: np.ndarray) -> SpinGem:
    """Convert a magic square to a Spin Gem representation."""
    n = magic_square.shape[0]
    atoms = []
    
    for i in range(n):
        for j in range(n):
            x = j - (n - 1) / 2
            y = (n - 1) / 2 - i
            z = 0.0
            spin = magic_square[i, j] - (n**2 + 1) / 2
            atoms.append(Atom(np.array([x, y, z]), spin, 'X', 1.0))
    
    return create_spin_gem(atoms)


def precession_dynamics(spin_gem: SpinGem, 
                        B_field: np.ndarray,
                        gamma: float = 1.0,
                        t_max: float = 10.0,
                        dt: float = 0.01) -> Dict:
    """Simulate classical spin precession in an external magnetic field."""
    N = len(spin_gem.atoms)
    times = np.arange(0, t_max, dt)
    n_steps = len(times)
    
    spin_vectors = np.zeros((N, 3))
    for i, atom in enumerate(spin_gem.atoms):
        spin_vectors[i, 2] = atom.spin
    
    magnetization = np.zeros((n_steps, 3))
    covariance_energy = np.zeros(n_steps)
    
    for t_idx, t in enumerate(times):
        magnetization[t_idx] = spin_vectors.sum(axis=0)
        
        # Compute current covariance energy
        r = spin_gem.centered_positions
        s_z = spin_vectors[:, 2]
        s_centered = s_z - s_z.mean()
        cov_xs = np.mean(r[:, 0] * s_centered)
        cov_ys = np.mean(r[:, 1] * s_centered)
        cov_zs = np.mean(r[:, 2] * s_centered)
        covariance_energy[t_idx] = cov_xs**2 + cov_ys**2 + cov_zs**2
        
        # Precess each spin
        for i in range(N):
            s = spin_vectors[i]
            dsdt = gamma * np.cross(s, B_field)
            spin_vectors[i] = s + dsdt * dt
    
    return {
        'times': times,
        'magnetization': magnetization,
        'covariance_energy': covariance_energy
    }


if __name__ == '__main__':
    print("Testing Spin Gem Core Module")
    print("=" * 50)
    
    # Test tetrahedron
    atoms = generate_symmetric_molecule(4, 'tetrahedron')
    gem = create_spin_gem(atoms)
    print(f"\nTetrahedron: E = {gem.spin_covariance_energy:.6e}")
    
    # Test Lo Shu
    lo_shu = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    gem = magic_square_to_spin_gem(lo_shu)
    print(f"Lo Shu: E = {gem.spin_covariance_energy:.6e}")
    print(f"Is Magic: {gem.spin_covariance_energy < 1e-10}")
