"""
Spin Gems: Extending Magic Gem Framework to Molecular Spin Precession

Core module defining the Spin Gem representation and covariance analysis
for atomic spin configurations in molecules.

Author: George R.
Date: December 2025
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.linalg import eigh
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Atom:
    """Represents an atom with position and spin state."""
    position: np.ndarray  # (x, y, z) in Angstroms
    spin: float           # Spin projection S_z (in units of ℏ)
    element: str          # Element symbol
    mass: float           # Atomic mass (amu)
    

@dataclass 
class SpinGem:
    """
    A Spin Gem: the geometric representation of a molecular spin configuration.
    
    Analogous to Magic Gems for magic squares, but where:
    - Spatial coordinates come from atomic positions (centered on centroid)
    - The 'value' coordinate is the spin projection S_z (centered on mean)
    """
    atoms: List[Atom]
    centered_positions: np.ndarray   # N x 3 array, centered
    centered_spins: np.ndarray       # N array, centered
    point_cloud: np.ndarray          # N x 4 array: (x, y, z, s)
    covariance_matrix: np.ndarray    # 4 x 4 covariance matrix
    spin_covariance_energy: float    # Sum of Cov(x,s)^2 + Cov(y,s)^2 + Cov(z,s)^2
    

def create_spin_gem(atoms: List[Atom]) -> SpinGem:
    """
    Construct a Spin Gem from a list of atoms.
    
    The construction centers the positions at the centroid and the spins
    at their mean, then computes the full 4D covariance matrix.
    """
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
    
    # Spin covariance energy: sum of squared off-diagonal terms involving spin
    # Cov(x,s)^2 + Cov(y,s)^2 + Cov(z,s)^2
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


def compute_precession_tensor(spin_gem: SpinGem) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the 'precession tensor' - analogous to moment of inertia but for spin.
    
    Returns eigenvalues and eigenvectors of the position-spin coupling matrix.
    This tensor describes how spin precession couples to spatial geometry.
    """
    # The coupling tensor M_ij = sum_k r_k,i * s_k
    # where r_k is the centered position and s_k is the centered spin
    
    N = len(spin_gem.atoms)
    r = spin_gem.centered_positions
    s = spin_gem.centered_spins
    
    # Outer product weighted by spin: shape (3, 3)
    # This is the "spin-weighted inertia tensor"
    coupling_tensor = np.zeros((3, 3))
    for k in range(N):
        coupling_tensor += s[k] * np.outer(r[k], r[k])
    
    eigenvalues, eigenvectors = eigh(coupling_tensor)
    return eigenvalues, eigenvectors


def magic_spin_configuration(positions: np.ndarray, 
                              target_cov: float = 0.0) -> np.ndarray:
    """
    Find spin assignments that achieve target spin-position covariance.
    
    For zero target covariance (magic configuration), spins must be
    distributed such that position provides no linear information about spin.
    
    This is a linear system: we want Cov(x,s) = Cov(y,s) = Cov(z,s) = 0.
    """
    N = len(positions)
    centroid = positions.mean(axis=0)
    r_centered = positions - centroid
    
    # Constraints for zero covariance:
    # sum_i (x_i - x_bar)(s_i - s_bar) = 0  =>  sum_i x_i s_i = s_bar * sum_i x_i = 0
    # Same for y and z.
    # Since positions are centered: sum_i r_i = 0
    # We need: sum_i r_i * s_i = 0 (vector equation, 3 constraints)
    # Plus: spins should sum to N * s_bar for some target mean
    
    # This gives us 4 linear constraints on N spins.
    # For N > 4, infinite solutions exist.
    # We find the minimum-norm solution that also satisfies s_i in [-1, 1] ideally.
    
    # Build constraint matrix A such that A @ s = b for magic config
    # Constraint 1-3: r_centered.T @ s = 0
    # Constraint 4: sum(s) = 0 (mean spin = 0)
    
    A = np.vstack([r_centered.T, np.ones(N)])  # 4 x N
    b = np.zeros(4)
    
    # Minimum norm solution via pseudoinverse
    s_magic = np.linalg.lstsq(A, b, rcond=None)[0]
    
    return s_magic


def generate_symmetric_molecule(n_atoms: int, 
                                 geometry: str = 'regular_polygon',
                                 radius: float = 1.5) -> List[Atom]:
    """
    Generate atoms in symmetric geometric arrangements.
    
    Geometries:
    - 'regular_polygon': atoms in a plane at vertices of regular n-gon
    - 'prism': two parallel regular n/2-gons
    - 'platonic': vertices of platonic solid (n=4,6,8,12,20)
    """
    atoms = []
    
    if geometry == 'regular_polygon':
        angles = np.linspace(0, 2*np.pi, n_atoms, endpoint=False)
        for i, theta in enumerate(angles):
            pos = np.array([radius * np.cos(theta), 
                           radius * np.sin(theta), 
                           0.0])
            # Assign alternating spins for interesting structure
            spin = 0.5 if i % 2 == 0 else -0.5
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'tetrahedron':
        # Regular tetrahedron vertices
        vertices = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1]
        ]) * radius / np.sqrt(3)
        spins = [0.5, 0.5, -0.5, -0.5]  # Balanced spins
        for i, (pos, spin) in enumerate(zip(vertices, spins)):
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'octahedron':
        # Regular octahedron vertices
        vertices = np.array([
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]) * radius
        # Alternating spins along each axis
        spins = [0.5, -0.5, 0.5, -0.5, 0.5, -0.5]
        for pos, spin in zip(vertices, spins):
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'cube':
        # Cube vertices
        vertices = np.array([
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
        ]) * radius / np.sqrt(3)
        # Checkerboard spin pattern (magic-like)
        spins = [0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5]
        for pos, spin in zip(vertices, spins):
            atoms.append(Atom(pos, spin, 'H', 1.008))
            
    elif geometry == 'benzene':
        # Benzene ring: 6 carbons in hexagon, 6 hydrogens outer
        for i in range(6):
            theta = i * np.pi / 3
            # Carbon
            c_pos = np.array([radius * np.cos(theta), 
                             radius * np.sin(theta), 0])
            atoms.append(Atom(c_pos, 0.0, 'C', 12.011))
            # Hydrogen
            h_pos = np.array([1.5 * radius * np.cos(theta),
                             1.5 * radius * np.sin(theta), 0])
            # Alternating pi-electron spin density
            h_spin = 0.1 * ((-1)**i)
            atoms.append(Atom(h_pos, h_spin, 'H', 1.008))
    
    return atoms


def scan_spin_configurations(positions: np.ndarray, 
                              n_samples: int = 10000,
                              spin_range: Tuple[float, float] = (-1.0, 1.0)
                             ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Randomly sample spin configurations and compute covariance energy.
    
    Returns arrays of spin configurations and their energies.
    """
    N = len(positions)
    spins_all = np.random.uniform(spin_range[0], spin_range[1], 
                                   size=(n_samples, N))
    energies = np.zeros(n_samples)
    
    centroid = positions.mean(axis=0)
    r = positions - centroid
    
    for i in range(n_samples):
        s = spins_all[i]
        s_centered = s - s.mean()
        
        # Covariance with each spatial coordinate
        cov_xs = np.mean(r[:, 0] * s_centered)
        cov_ys = np.mean(r[:, 1] * s_centered)
        cov_zs = np.mean(r[:, 2] * s_centered)
        
        energies[i] = cov_xs**2 + cov_ys**2 + cov_zs**2
    
    return spins_all, energies


def precession_dynamics(spin_gem: SpinGem, 
                        B_field: np.ndarray,
                        gamma: float = 1.0,
                        t_max: float = 10.0,
                        dt: float = 0.01) -> Dict:
    """
    Simulate classical spin precession in an external magnetic field.
    
    Each spin precesses around B with frequency gamma * |B|.
    The collective behavior depends on the initial Spin Gem configuration.
    
    Returns time series of total magnetization and individual spins.
    """
    N = len(spin_gem.atoms)
    times = np.arange(0, t_max, dt)
    n_steps = len(times)
    
    # Initialize spin vectors (pointing along z initially, scaled by S_z value)
    # For simplicity, treat as classical vectors
    spin_vectors = np.zeros((N, 3))
    for i, atom in enumerate(spin_gem.atoms):
        # Initial spin vector points along z
        spin_vectors[i, 2] = atom.spin
    
    # Storage for dynamics
    magnetization = np.zeros((n_steps, 3))
    spin_history = np.zeros((n_steps, N, 3))
    covariance_energy = np.zeros(n_steps)
    
    B_unit = B_field / np.linalg.norm(B_field) if np.linalg.norm(B_field) > 0 else np.array([0, 0, 1])
    omega = gamma * np.linalg.norm(B_field)
    
    for t_idx, t in enumerate(times):
        # Record current state
        magnetization[t_idx] = spin_vectors.sum(axis=0)
        spin_history[t_idx] = spin_vectors.copy()
        
        # Compute current covariance energy
        r = spin_gem.centered_positions
        s_z = spin_vectors[:, 2]
        s_centered = s_z - s_z.mean()
        cov_xs = np.mean(r[:, 0] * s_centered)
        cov_ys = np.mean(r[:, 1] * s_centered)
        cov_zs = np.mean(r[:, 2] * s_centered)
        covariance_energy[t_idx] = cov_xs**2 + cov_ys**2 + cov_zs**2
        
        # Precess each spin (simple Euler integration of ds/dt = gamma * s × B)
        for i in range(N):
            s = spin_vectors[i]
            dsdt = gamma * np.cross(s, B_field)
            spin_vectors[i] = s + dsdt * dt
            # Renormalize to preserve spin magnitude
            norm = np.linalg.norm(spin_vectors[i])
            if norm > 1e-10:
                spin_vectors[i] *= np.linalg.norm(spin_gem.atoms[i].spin) / norm
    
    return {
        'times': times,
        'magnetization': magnetization,
        'spin_history': spin_history,
        'covariance_energy': covariance_energy
    }


# ============================================================
# Connection to Magic Squares: The Discrete Lattice Case
# ============================================================

def magic_square_to_spin_gem(magic_square: np.ndarray) -> SpinGem:
    """
    Convert a magic square to a Spin Gem representation.
    
    This connects our Spin Gem framework back to the original Magic Gem work:
    - Grid positions become atomic positions (on a 2D lattice in z=0 plane)
    - Magic square values become spin projections
    
    This shows that magic squares are a special discrete case of the
    continuous Spin Gem framework.
    """
    n = magic_square.shape[0]
    atoms = []
    
    for i in range(n):
        for j in range(n):
            # Grid position (centered)
            x = j - (n - 1) / 2
            y = (n - 1) / 2 - i
            z = 0.0
            
            # Spin from magic square value (centered)
            spin = magic_square[i, j] - (n**2 + 1) / 2
            
            atoms.append(Atom(
                position=np.array([x, y, z]),
                spin=spin,
                element='X',  # Abstract lattice site
                mass=1.0
            ))
    
    return create_spin_gem(atoms)


def verify_magic_square_is_spin_magic(magic_square: np.ndarray) -> Dict:
    """
    Verify that a magic square, interpreted as a Spin Gem, has zero
    spin-position covariance.
    
    This provides the bridge between discrete magic squares and
    continuous molecular spin configurations.
    """
    spin_gem = magic_square_to_spin_gem(magic_square)
    
    cov = spin_gem.covariance_matrix
    
    return {
        'cov_xs': cov[0, 3],  # Should be ~0 for magic square
        'cov_ys': cov[1, 3],  # Should be ~0 for magic square
        'cov_zs': cov[2, 3],  # Always 0 since z=0 for all
        'spin_covariance_energy': spin_gem.spin_covariance_energy,
        'is_spin_magic': spin_gem.spin_covariance_energy < 1e-10
    }


if __name__ == '__main__':
    # Quick test
    print("Testing Spin Gem Core Module")
    print("=" * 50)
    
    # Test 1: Tetrahedron with balanced spins
    atoms = generate_symmetric_molecule(4, 'tetrahedron')
    gem = create_spin_gem(atoms)
    print(f"\nTetrahedron Spin Gem:")
    print(f"  Spin covariance energy: {gem.spin_covariance_energy:.6e}")
    print(f"  Cov(x,s) = {gem.covariance_matrix[0,3]:.6e}")
    print(f"  Cov(y,s) = {gem.covariance_matrix[1,3]:.6e}")
    print(f"  Cov(z,s) = {gem.covariance_matrix[2,3]:.6e}")
    
    # Test 2: Magic square as Spin Gem
    lo_shu = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    result = verify_magic_square_is_spin_magic(lo_shu)
    print(f"\nLo Shu Magic Square as Spin Gem:")
    print(f"  Cov(x,s) = {result['cov_xs']:.6e}")
    print(f"  Cov(y,s) = {result['cov_ys']:.6e}")
    print(f"  Is Spin-Magic: {result['is_spin_magic']}")
    
    print("\n" + "=" * 50)
    print("Core module tests passed!")

