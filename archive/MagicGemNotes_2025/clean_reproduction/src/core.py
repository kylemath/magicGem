"""
Core Utilities for Magic Square Analysis
=========================================

This module provides fundamental functions for working with 4x4 magic squares,
including verification, enumeration, and symmetry reduction.

Author: Kyle Elliott Mathewson
University of Alberta
"""

import numpy as np
import os
from itertools import permutations
from typing import List, Tuple, Set

# Fixed random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Magic constant for 4x4 squares
MAGIC_CONSTANT = 34


def is_magic(square: np.ndarray) -> bool:
    """
    Check if a square is a magic square.
    
    A magic square has all rows, columns, and both main diagonals
    summing to the magic constant (34 for 4x4).
    
    Parameters
    ----------
    square : np.ndarray
        4x4 array to check
        
    Returns
    -------
    bool
        True if the square is magic
    """
    n = square.shape[0]
    target = n * (n**2 + 1) // 2  # Magic constant: 34 for n=4
    
    # Check rows
    if not np.all(np.sum(square, axis=1) == target):
        return False
    
    # Check columns
    if not np.all(np.sum(square, axis=0) == target):
        return False
    
    # Check main diagonal
    if np.trace(square) != target:
        return False
    
    # Check anti-diagonal
    if np.trace(np.fliplr(square)) != target:
        return False
    
    # Check distinct values (1 to n^2)
    if not np.array_equal(np.sort(square.flatten()), np.arange(1, n**2 + 1)):
        return False
        
    return True


def compute_covariance_sum(square: np.ndarray) -> float:
    """
    Compute the sum of absolute covariances for the zero-covariance test.
    
    Returns |Cov(x,z)| + |Cov(y,z)| where x,y are centered coordinates
    and z is centered value.
    
    Parameters
    ----------
    square : np.ndarray
        4x4 array
        
    Returns
    -------
    float
        Sum of absolute covariances (0 for magic squares)
    """
    n = square.shape[0]
    
    # Create centered coordinates
    indices = np.arange(n) - (n - 1) / 2
    x_coords = np.repeat(indices, n)
    y_coords = np.tile(indices, n)
    z_values = square.flatten() - np.mean(square)
    
    # Compute covariances
    cov_xz = np.mean(x_coords * z_values)
    cov_yz = np.mean(y_coords * z_values)
    
    return abs(cov_xz) + abs(cov_yz)


def get_transformations(square: np.ndarray) -> List[np.ndarray]:
    """
    Generate all 8 transformations of a square under D4 (dihedral group).
    
    Parameters
    ----------
    square : np.ndarray
        4x4 array
        
    Returns
    -------
    List[np.ndarray]
        List of 8 transformed squares
    """
    transforms = [square]
    
    # Rotations
    for k in range(1, 4):
        transforms.append(np.rot90(square, k))
    
    # Reflections
    flipped = np.fliplr(square)
    transforms.append(flipped)
    for k in range(1, 4):
        transforms.append(np.rot90(flipped, k))
    
    return transforms


def canonical_form(square: np.ndarray) -> np.ndarray:
    """
    Return the canonical (lexicographically smallest) form of a magic square
    under D4 transformations.
    
    Parameters
    ----------
    square : np.ndarray
        4x4 magic square
        
    Returns
    -------
    np.ndarray
        Canonical form of the square
    """
    transforms = get_transformations(square)
    # Convert to tuples for comparison
    tuples = [tuple(t.flatten()) for t in transforms]
    min_idx = tuples.index(min(tuples))
    return transforms[min_idx]


def find_unique_squares(squares: List[np.ndarray]) -> List[np.ndarray]:
    """
    Reduce a list of squares to unique ones under D4 symmetry.
    
    Parameters
    ----------
    squares : List[np.ndarray]
        List of magic squares
        
    Returns
    -------
    List[np.ndarray]
        List of unique squares (canonical forms)
    """
    seen: Set[Tuple[int, ...]] = set()
    unique = []
    
    for sq in squares:
        canonical = canonical_form(sq)
        key = tuple(canonical.flatten().astype(int))
        if key not in seen:
            seen.add(key)
            unique.append(canonical)
    
    return unique


def reduce_to_unique(squares: List[np.ndarray]) -> List[np.ndarray]:
    """Alias for find_unique_squares."""
    return find_unique_squares(squares)


def generate_all_4x4_squares() -> np.ndarray:
    """
    Generate all 880 unique 4x4 magic squares using optimized backtracking.
    
    This function systematically searches through permutations, using
    constraint propagation to prune the search space efficiently.
    
    Returns
    -------
    np.ndarray
        Array of shape (880, 4, 4) containing all unique magic squares
    """
    squares = []
    target = MAGIC_CONSTANT  # 34
    
    def is_valid_partial(grid: List[int], pos: int) -> bool:
        """Check if partial grid is still valid."""
        row, col = pos // 4, pos % 4
        
        # Check partial row sum (can't exceed target)
        row_start = row * 4
        row_sum = sum(grid[row_start:pos+1])
        remaining_cells = 3 - col
        if row_sum > target:
            return False
        if remaining_cells > 0:
            # Minimum possible remaining = sum of smallest unused
            min_remaining = remaining_cells  # At minimum, use values >= 1
            if row_sum + min_remaining > target:
                pass  # Could prune more aggressively, but keep simple
        
        # Check partial column sum
        col_sum = sum(grid[i*4 + col] for i in range(row + 1))
        if col_sum > target:
            return False
        
        # If row complete, check exact sum
        if col == 3:
            if sum(grid[row*4:(row+1)*4]) != target:
                return False
        
        # If column complete, check exact sum
        if row == 3:
            if sum(grid[i*4 + col] for i in range(4)) != target:
                return False
        
        return True
    
    def backtrack(grid: List[int], pos: int, used: Set[int]) -> None:
        """Recursive backtracking."""
        if pos == 16:
            arr = np.array(grid).reshape(4, 4)
            if is_magic(arr):
                squares.append(arr.copy())
            return
        
        for val in range(1, 17):
            if val in used:
                continue
            
            grid[pos] = val
            
            if is_valid_partial(grid, pos):
                used.add(val)
                backtrack(grid, pos + 1, used)
                used.remove(val)
            
            grid[pos] = 0
    
    print("  Starting backtracking search...")
    backtrack([0] * 16, 0, set())
    print(f"  Found {len(squares)} magic squares (before symmetry reduction)")
    
    # Reduce to unique under D4 symmetry
    unique_squares = find_unique_squares(squares)
    print(f"  Reduced to {len(unique_squares)} unique squares")
    
    return np.array(unique_squares) if unique_squares else np.zeros((0, 4, 4))


def load_squares(cache_dir: str = None) -> np.ndarray:
    """
    Load the full dataset of 880 unique 4x4 magic squares.
    
    Attempts to load from multiple sources in order:
    1. NumPy cache file
    2. JSON file (web assets)
    3. Generate via backtracking (slow, last resort)
    
    Parameters
    ----------
    cache_dir : str, optional
        Directory to cache/load squares
        
    Returns
    -------
    np.ndarray
        Array of shape (880, 4, 4)
    """
    import json
    
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    cache_file = os.path.join(cache_dir, 'magic_squares_880.npy')
    
    # Try to load from NumPy cache
    if os.path.exists(cache_file):
        squares = np.load(cache_file)
        if len(squares) == 880:
            return squares
    
    # Try to load from JSON (web assets)
    json_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'web', 'assets', 'data', 'unique_squares.json'),
        os.path.join(os.path.dirname(__file__), '..', 'data', 'unique_squares.json'),
    ]
    
    for json_path in json_paths:
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    data = json.load(f)
                
                # Parse JSON data
                if isinstance(data[0], dict):
                    squares = [np.array(s['values']).reshape(4, 4) for s in data]
                else:
                    squares = [np.array(s).reshape(4, 4) if len(np.array(s).shape) == 1 else np.array(s) for s in data]
                
                squares = np.array(squares)
                
                if len(squares) == 880:
                    # Verify and cache
                    valid_count = sum(1 for sq in squares if is_magic(sq))
                    if valid_count == 880:
                        os.makedirs(cache_dir, exist_ok=True)
                        np.save(cache_file, squares)
                        print(f"Loaded 880 squares from {json_path}")
                        return squares
            except Exception as e:
                print(f"Warning: Could not load from {json_path}: {e}")
    
    # Last resort: generate (this is slow)
    print("Generating all 880 unique 4x4 magic squares...")
    print("This may take several minutes on first run...")
    squares = generate_all_4x4_squares()
    
    # Cache for future use
    if len(squares) > 0:
        os.makedirs(cache_dir, exist_ok=True)
        np.save(cache_file, squares)
        print(f"Cached {len(squares)} squares to {cache_file}")
    
    return squares


# Sample magic squares for quick testing
DURER_SQUARE = np.array([
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1]
])

SAMPLE_SQUARES = [
    DURER_SQUARE,
    np.array([
        [1, 15, 14, 4],
        [12, 6, 7, 9],
        [8, 10, 11, 5],
        [13, 3, 2, 16]
    ]),
    np.array([
        [2, 16, 13, 3],
        [11, 5, 8, 10],
        [7, 9, 12, 6],
        [14, 4, 1, 15]
    ])
]


if __name__ == '__main__':
    print("Magic Square Core Module")
    print("=" * 40)
    
    # Verify sample squares
    print("\nVerifying sample squares:")
    for i, sq in enumerate(SAMPLE_SQUARES):
        print(f"  Square {i+1}: is_magic = {is_magic(sq)}, "
              f"cov_sum = {compute_covariance_sum(sq):.6f}")
    
    # Generate all squares
    print("\nLoading/generating all 880 magic squares...")
    squares = load_squares()
    print(f"Loaded {len(squares)} unique magic squares")
    
    # Verify all are magic
    all_magic = all(is_magic(sq) for sq in squares)
    print(f"All squares are magic: {all_magic}")
    
    # Verify all have zero covariance
    max_cov = max(compute_covariance_sum(sq) for sq in squares)
    print(f"Maximum covariance sum: {max_cov:.10f}")
