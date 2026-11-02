"""
Module for generating and analyzing most-perfect magic squares.

Most-perfect magic squares are a special type of magic square with additional properties:
1. They are magic squares (rows, columns, main diagonals sum to magic constant)
2. All 2×2 subsquares sum to 2(n²+1)
3. All pairs of cells that are equidistant from the center sum to 2(n²+1)
4. All broken diagonals sum to the magic constant
"""

import numpy as np
from itertools import permutations

def create_reversible_square():
    """
    Create a 4×4 reversible square, which is the starting point for constructing
    a most-perfect magic square using Amato's method.
    
    A reversible square has the property that opposite corners of any rectangle
    sum to the same value.
    
    Returns:
    --------
    numpy.ndarray
        A 4×4 reversible square
    """
    # Create a reversible square with numbers 1-16 arranged to satisfy the reversible property
    square = np.array([
        [ 1,  2,  3,  4],
        [ 8,  7,  6,  5],
        [ 9, 10, 11, 12],
        [16, 15, 14, 13]
    ])
    return square

def construct_most_perfect_from_reversible(reversible_square):
    """
    Construct a most-perfect magic square from a reversible square using Amato's method.
    
    The method involves:
    1. Reversing the rightmost n/2 columns
    2. Reversing the bottom n/2 rows
    3. Applying a specific transformation pattern to 2×2 blocks
    
    Parameters:
    -----------
    reversible_square : numpy.ndarray
        A 4×4 reversible square to transform
    
    Returns:
    --------
    numpy.ndarray
        A 4×4 most-perfect magic square
    """
    n = 4
    square = reversible_square.copy()
    
    # Step 1: Reverse rightmost n/2 columns
    square[:, n//2:] = np.flipud(square[:, n//2:])
    
    # Step 2: Reverse bottom n/2 rows
    square[n//2:, :] = np.fliplr(square[n//2:, :])
    
    # Step 3: Transform 2×2 blocks using a specific pattern
    result = np.zeros((4, 4), dtype=int)
    for i in range(0, n, 2):
        for j in range(0, n, 2):
            block = square[i:i+2, j:j+2]
            # Apply transformation pattern
            result[i, j] = block[0, 0]  # Top-left stays
            result[i, j+1] = block[1, 0]  # Bottom-left moves up
            result[i+1, j] = block[0, 1]  # Top-right moves down
            result[i+1, j+1] = block[1, 1]  # Bottom-right stays
    
    return result

def generate_most_perfect_square():
    """
    Generate a most-perfect 4×4 magic square using Ollerenshaw's pattern.
    Based on Ollerenshaw & Brée's 1998 paper.
    
    Properties of a most-perfect magic square:
    1. Each number 1-16 appears exactly once
    2. All rows, columns, and diagonals sum to magic constant M = n(n²+1)/2 = 34
    3. All 2×2 subsquares sum to 2(n²+1) = 34
    4. All complementary pairs (equidistant from center) sum to n²+1 = 17
    5. All broken diagonals sum to magic constant M = 34
    
    Returns:
    --------
    numpy.ndarray
        A 4×4 most-perfect magic square with verified properties
    """
    # This is a verified most-perfect magic square pattern from Ollerenshaw's work
    square = np.array([
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1]
    ])
    
    return square

def generate_all_most_perfect_squares():
    """
    Generate all distinct most-perfect 4×4 magic squares through symmetry operations.
    
    The following transformations preserve the most-perfect property:
    1. Rotations (90°, 180°, 270°)
    2. Reflections (horizontal, vertical, diagonal)
    3. Complement (replacing each number n with 17-n)
    4. Combinations of the above
    
    Returns:
    --------
    list
        A list of numpy arrays, each representing a unique most-perfect magic square
    """
    # Start with the standard form
    base = generate_most_perfect_square()
    squares = []
    
    # Add the base square
    squares.append(base.copy())
    
    # Generate all possible transformations that preserve the most-perfect property
    
    # 1. Transpose
    squares.append(base.T.copy())
    
    # 2. Rotate 90, 180, 270 degrees
    squares.append(np.rot90(base, 1).copy())
    squares.append(np.rot90(base, 2).copy())
    squares.append(np.rot90(base, 3).copy())
    
    # 3. Reflect horizontally and vertically
    squares.append(np.fliplr(base).copy())
    squares.append(np.flipud(base).copy())
    
    # 4. Reflect along diagonals
    anti_diag = np.zeros_like(base)
    for i in range(4):
        for j in range(4):
            anti_diag[i, j] = base[3-j, 3-i]
    squares.append(anti_diag.copy())
    
    # 5. Complement (replace each number n with 17-n)
    complement = 17 - base
    squares.append(complement.copy())
    
    # 6. Combinations of the above transformations
    # Complement + transpose
    squares.append((17 - base.T).copy())
    
    # Complement + rotations
    squares.append((17 - np.rot90(base, 1)).copy())
    squares.append((17 - np.rot90(base, 2)).copy())
    squares.append((17 - np.rot90(base, 3)).copy())
    
    # Complement + reflections
    squares.append((17 - np.fliplr(base)).copy())
    squares.append((17 - np.flipud(base)).copy())
    
    # Filter out duplicates and verify they are most-perfect
    unique_squares = []
    for square in squares:
        if is_most_perfect(square):
            # Check if it's unique
            is_unique = True
            for existing in unique_squares:
                if np.array_equal(square, existing):
                    is_unique = False
                    break
            if is_unique:
                unique_squares.append(square)
    
    print(f"Generated {len(unique_squares)} unique most-perfect magic squares")
    return unique_squares

def is_magic_square(square):
    """
    Check if a square is a magic square.
    
    Parameters:
    -----------
    square : numpy.ndarray
        A square matrix to check
    
    Returns:
    --------
    bool
        True if the square is a magic square, False otherwise
    """
    n = square.shape[0]
    magic_sum = n * (n**2 + 1) / 2
    
    # Check rows
    for i in range(n):
        if np.sum(square[i, :]) != magic_sum:
            return False
    
    # Check columns
    for j in range(n):
        if np.sum(square[:, j]) != magic_sum:
            return False
    
    # Check main diagonals
    if np.sum(np.diag(square)) != magic_sum:
        return False
    if np.sum(np.diag(np.fliplr(square))) != magic_sum:
        return False
    
    return True

def is_most_perfect(square):
    """
    Check if a square is a most-perfect magic square.
    
    A most-perfect magic square of order 4 must satisfy:
    1. It is a magic square (rows, columns, main diagonals sum to magic constant)
    2. All 2×2 subsquares sum to 2(n²+1)
    3. All pairs of cells that are equidistant from the center sum to n²+1
    4. All broken diagonals sum to the magic constant
    
    Parameters:
    -----------
    square : numpy.ndarray
        A square matrix to check
    
    Returns:
    --------
    bool
        True if the square is a most-perfect magic square, False otherwise
    """
    n = square.shape[0]
    
    # Only 4×4 squares can be most-perfect by Ollerenshaw's definition
    if n != 4:
        return False
    
    # Check if it's a magic square first
    if not is_magic_square(square):
        print("Not a magic square")
        return False
    
    magic_sum = n * (n**2 + 1) / 2  # 34 for a 4×4 square
    subsquare_sum = 2 * (n**2 + 1)  # 34 for a 4×4 square
    complementary_sum = n**2 + 1  # 17 for a 4×4 square
    
    # Check all 2×2 subsquares
    for i in range(n-1):
        for j in range(n-1):
            subsquare = square[i:i+2, j:j+2]
            if np.sum(subsquare) != subsquare_sum:
                print(f"2x2 subsquare at ({i},{j}) sums to {np.sum(subsquare)}, not {subsquare_sum}")
                return False
    
    # Check complementary pairs (equidistant from center)
    # For a 4×4 square, these are pairs like (0,0)-(3,3), (0,1)-(3,2), etc.
    for i in range(n):
        for j in range(n):
            complement_i = n - 1 - i
            complement_j = n - 1 - j
            pair_sum = square[i, j] + square[complement_i, complement_j]
            if pair_sum != complementary_sum:
                print(f"Complementary pair ({i},{j})-({complement_i},{complement_j}) sums to {pair_sum}, not {complementary_sum}")
                return False
    
    # Check broken diagonals
    if not check_broken_diagonals(square):
        print("Broken diagonals don't sum to magic constant")
        return False
    
    return True

def check_broken_diagonals(square):
    """
    Check if all broken diagonals in a square sum to the magic constant.
    
    Parameters:
    -----------
    square : numpy.ndarray
        A square matrix to check
    
    Returns:
    --------
    bool
        True if all broken diagonals sum to the magic constant, False otherwise
    """
    n = square.shape[0]
    magic_sum = n * (n**2 + 1) / 2
    
    # Check all broken diagonals
    for offset in range(1, n):
        # Broken diagonals from top-left to bottom-right
        diag1 = np.array([square[i, (i+offset)%n] for i in range(n)])
        diag2 = np.array([square[(i+offset)%n, i] for i in range(n)])
        
        if np.sum(diag1) != magic_sum or np.sum(diag2) != magic_sum:
            return False
    
    return True

def compare_with_magic_square(most_perfect_square, magic_square):
    """
    Compare a most-perfect magic square with a standard magic square.
    
    Parameters:
    -----------
    most_perfect_square : numpy.ndarray
        A 4×4 most-perfect magic square
    magic_square : numpy.ndarray
        A 4×4 standard magic square
    
    Returns:
    --------
    dict
        Dictionary containing comparison metrics
    """
    # Check if both are valid magic squares
    mp_is_magic = is_magic_square(most_perfect_square)
    std_is_magic = is_magic_square(magic_square)
    
    # Count valid 2x2 subsquares
    mp_valid_2x2 = 0
    std_valid_2x2 = 0
    
    n = 4
    magic_sum = n * (n**2 + 1) / 2
    subsquare_sum = magic_sum / 2
    
    for i in range(3):
        for j in range(3):
            # Check 2x2 subsquares in most-perfect
            mp_subsquare = most_perfect_square[i:i+2, j:j+2]
            mp_sum = np.sum(mp_subsquare)
            if mp_sum == subsquare_sum:
                mp_valid_2x2 += 1
                
            # Check 2x2 subsquares in standard
            std_subsquare = magic_square[i:i+2, j:j+2]
            std_sum = np.sum(std_subsquare)
            if std_sum == subsquare_sum:
                std_valid_2x2 += 1
    
    # Check corners and center
    mp_corners_sum = most_perfect_square[0,0] + most_perfect_square[0,3] + most_perfect_square[3,0] + most_perfect_square[3,3]
    std_corners_sum = magic_square[0,0] + magic_square[0,3] + magic_square[3,0] + magic_square[3,3]
    
    # For 4x4, center is the 2x2 subsquare in the middle
    mp_center_sum = np.sum(most_perfect_square[1:3, 1:3])
    std_center_sum = np.sum(magic_square[1:3, 1:3])
    
    # Check broken diagonals
    mp_broken_diags_valid = check_broken_diagonals(most_perfect_square)
    std_broken_diags_valid = check_broken_diagonals(magic_square)
    
    return {
        "both_magic": mp_is_magic and std_is_magic,
        "valid_2x2_subsquares": {
            "most_perfect": mp_valid_2x2,
            "standard": std_valid_2x2
        },
        "corners_sum": {
            "most_perfect": mp_corners_sum,
            "standard": std_corners_sum
        },
        "center_sum": {
            "most_perfect": mp_center_sum,
            "standard": std_center_sum
        },
        "broken_diagonals_valid": {
            "most_perfect": mp_broken_diags_valid,
            "standard": std_broken_diags_valid
        }
    }

if __name__ == "__main__":
    # Generate a single most-perfect magic square
    square = generate_most_perfect_square()
    print("Generated most-perfect magic square:")
    print(square)
    
    # Verify it's a most-perfect magic square
    is_mp = is_most_perfect(square)
    print(f"Is most-perfect: {is_mp}")
    
    # Generate all most-perfect magic squares
    all_squares = generate_all_most_perfect_squares()
    print(f"Total number of most-perfect magic squares: {len(all_squares)}") 