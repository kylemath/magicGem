"""
magic_squares.py
================
Core functions for generating and validating magic squares of order n.

A magic square is an n×n grid filled with distinct integers such that
the sum of each row, column, and main diagonal equals the magic constant.
"""

import numpy as np
from itertools import permutations
from typing import List, Tuple, Generator
import json


def magic_constant(n: int) -> int:
    """
    Compute the magic constant for an n×n magic square using integers 1 to n².
    
    M = n(n² + 1) / 2
    
    Parameters
    ----------
    n : int
        Order of the magic square
        
    Returns
    -------
    int
        The magic constant
    """
    return n * (n**2 + 1) // 2


def is_magic_square(grid: np.ndarray) -> bool:
    """
    Check if a given n×n grid is a valid magic square.
    
    Parameters
    ----------
    grid : np.ndarray
        Square array to validate
        
    Returns
    -------
    bool
        True if grid is a valid magic square
    """
    n = grid.shape[0]
    if grid.shape != (n, n):
        return False
    
    target = magic_constant(n)
    
    # Check rows
    if not all(grid[i, :].sum() == target for i in range(n)):
        return False
    
    # Check columns
    if not all(grid[:, j].sum() == target for j in range(n)):
        return False
    
    # Check main diagonal
    if np.trace(grid) != target:
        return False
    
    # Check anti-diagonal
    if np.trace(np.fliplr(grid)) != target:
        return False
    
    # Check distinct integers 1 to n²
    expected = set(range(1, n**2 + 1))
    if set(grid.flatten()) != expected:
        return False
    
    return True


def generate_all_3x3_magic_squares() -> List[np.ndarray]:
    """
    Generate all valid 3×3 magic squares by exhaustive search.
    
    Returns
    -------
    List[np.ndarray]
        List of all valid 3×3 magic squares (8 total, related by symmetry)
    """
    magic_squares = []
    for perm in permutations(range(1, 10)):
        grid = np.array(perm).reshape(3, 3)
        if is_magic_square(grid):
            magic_squares.append(grid)
    return magic_squares


def get_canonical_3x3() -> np.ndarray:
    """
    Return the canonical (Lo Shu) 3×3 magic square.
    
    Returns
    -------
    np.ndarray
        The Lo Shu magic square
    """
    return np.array([
        [2, 7, 6],
        [9, 5, 1],
        [4, 3, 8]
    ])


def generate_symmetry_group(square: np.ndarray) -> List[np.ndarray]:
    """
    Generate all 8 symmetries (D4 group) of a magic square.
    
    Parameters
    ----------
    square : np.ndarray
        A magic square
        
    Returns
    -------
    List[np.ndarray]
        All 8 rotations and reflections
    """
    symmetries = []
    current = square.copy()
    
    # 4 rotations
    for _ in range(4):
        symmetries.append(current.copy())
        current = np.rot90(current)
    
    # Reflect and 4 more rotations
    current = np.fliplr(square)
    for _ in range(4):
        symmetries.append(current.copy())
        current = np.rot90(current)
    
    return symmetries


def canonical_form(square: np.ndarray) -> np.ndarray:
    """
    Return the canonical form of a magic square (lexicographically smallest).
    
    Parameters
    ----------
    square : np.ndarray
        A magic square
        
    Returns
    -------
    np.ndarray
        Canonical representative of equivalence class
    """
    symmetries = generate_symmetry_group(square)
    # Convert to tuples for comparison
    as_tuples = [tuple(s.flatten()) for s in symmetries]
    min_tuple = min(as_tuples)
    return np.array(min_tuple).reshape(square.shape)


def count_arrangements(n: int) -> int:
    """
    Count total possible arrangements of n² distinct integers in n×n grid.
    
    Returns n²!
    """
    from math import factorial
    return factorial(n**2)


def generate_random_arrangement(n: int) -> np.ndarray:
    """
    Generate a random arrangement of integers 1 to n² in an n×n grid.
    """
    arr = np.arange(1, n**2 + 1)
    np.random.shuffle(arr)
    return arr.reshape(n, n)


def generate_4x4_magic_squares(limit: int = 1000) -> List[np.ndarray]:
    """
    Generate 4×4 magic squares using known construction methods.
    
    There are 880 essentially different 4×4 magic squares.
    This uses the doubly-even construction method.
    
    Parameters
    ----------
    limit : int
        Maximum number to generate
        
    Returns
    -------
    List[np.ndarray]
        List of valid 4×4 magic squares
    """
    magic_squares = []
    
    # For 4×4, we use the "diagonal" method
    # Swap elements on diagonals with their complement (17 - x)
    def construct_4x4():
        grid = np.arange(1, 17).reshape(4, 4)
        # Mark diagonal positions
        for i in range(4):
            for j in range(4):
                # Main diagonal and anti-diagonal positions
                if i == j or i + j == 3:
                    grid[i, j] = 17 - grid[i, j]
        return grid
    
    base_square = construct_4x4()
    if is_magic_square(base_square):
        # Generate all symmetries
        for sym in generate_symmetry_group(base_square):
            if len(magic_squares) < limit:
                magic_squares.append(sym)
    
    return magic_squares


def get_canonical_4x4() -> np.ndarray:
    """
    Return the canonical 4×4 magic square (Dürer's square variant).
    
    Returns
    -------
    np.ndarray
        A 4×4 magic square
    """
    # This is the doubly-even diagonal method result
    grid = np.arange(1, 17).reshape(4, 4)
    for i in range(4):
        for j in range(4):
            if i == j or i + j == 3:
                grid[i, j] = 17 - grid[i, j]
    return grid


def siamese_method(n: int) -> np.ndarray:
    """
    Generate an n×n magic square using the Siamese (de la Loubère) method.
    Works for odd n only.
    
    Parameters
    ----------
    n : int
        Odd integer order
        
    Returns
    -------
    np.ndarray
        Magic square of order n
    """
    if n % 2 == 0:
        raise ValueError("Siamese method only works for odd n")
    
    grid = np.zeros((n, n), dtype=int)
    
    # Start position: middle of top row
    i, j = 0, n // 2
    
    for num in range(1, n**2 + 1):
        grid[i, j] = num
        
        # Move up and right
        new_i, new_j = (i - 1) % n, (j + 1) % n
        
        # If cell is occupied, move down instead
        if grid[new_i, new_j] != 0:
            new_i, new_j = (i + 1) % n, j
        
        i, j = new_i, new_j
    
    return grid


def save_magic_squares(squares: List[np.ndarray], filepath: str):
    """Save magic squares to JSON file."""
    data = [sq.tolist() for sq in squares]
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_magic_squares(filepath: str) -> List[np.ndarray]:
    """Load magic squares from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return [np.array(sq) for sq in data]


if __name__ == "__main__":
    # Test basic functionality
    print("3×3 Magic Constant:", magic_constant(3))
    print("4×4 Magic Constant:", magic_constant(4))
    print("5×5 Magic Constant:", magic_constant(5))
    
    lo_shu = get_canonical_3x3()
    print("\nLo Shu Square:")
    print(lo_shu)
    print("Is magic:", is_magic_square(lo_shu))
    
    all_3x3 = generate_all_3x3_magic_squares()
    print(f"\nTotal 3×3 magic squares: {len(all_3x3)}")
    
    siamese_5 = siamese_method(5)
    print("\n5×5 Siamese Magic Square:")
    print(siamese_5)
    print("Is magic:", is_magic_square(siamese_5))

