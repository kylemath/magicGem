import numpy as np
import time
import multiprocessing as mp
from itertools import product
import os

def check_partial_sums(square, n, pos):
    """Check if partial rows, columns, and diagonals exceed the magic sum"""
    magic_sum = n * (n * n + 1) // 2  # 34 for 4x4
    
    # Check completed rows
    row = pos // n
    if pos % n == n-1:  # End of row
        if sum(square[row]) != magic_sum:
            return False
    
    # Check completed columns
    col = pos % n
    if pos >= n*(n-1):  # Bottom row
        if sum(square[i][col] for i in range(n)) != magic_sum:
            return False
    
    # Check main diagonal if complete
    if pos == n*n-1:
        if sum(square[i][i] for i in range(n)) != magic_sum:
            return False
        if sum(square[i][n-1-i] for i in range(n)) != magic_sum:
            return False
            
    return True

def is_valid(square, n, row, col, num):
    # Check if number is already used
    for i in range(n):
        for j in range(n):
            if square[i][j] == num:
                return False
    
    # Early sum checking for rows
    current_row_sum = sum(square[row])
    if current_row_sum + num > 34:  # Magic sum for 4x4
        return False
        
    # Early sum checking for columns
    current_col_sum = sum(square[i][col] for i in range(n))
    if current_col_sum + num > 34:
        return False
    
    # Early diagonal sum checking
    if row == col:  # Main diagonal
        diag_sum = sum(square[i][i] for i in range(n))
        if diag_sum + num > 34:
            return False
            
    if row + col == n-1:  # Other diagonal
        diag_sum = sum(square[i][n-1-i] for i in range(n))
        if diag_sum + num > 34:
            return False
    
    return True

def calculate_possible_attempts():
    """Calculate a more realistic estimate of possible attempts"""
    remaining_positions = 1
    for i in range(1, 17):  # 16!
        remaining_positions *= i
    return remaining_positions, 16, remaining_positions//16

def verify_known_square():
    """Verify our validation logic works with a known valid square"""
    known_square = np.array([
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ])
    
    # Test if our validation functions work
    n = 4
    for pos in range(n*n):
        row, col = pos // n, pos % n
        if not check_partial_sums(known_square, n, pos):
            print(f"check_partial_sums failed at position {pos}")
            return False
        if not is_valid(np.zeros((n,n)), n, row, col, known_square[row][col]):
            print(f"is_valid failed for number {known_square[row][col]} at position {pos}")
            return False
    return True

def solve_magic_square_worker(args):
    n, first_num, first_pos = args
    square = np.zeros((n, n), dtype=int)
    magic_squares = []
    stats = {'attempts': 0}
    
    # Place the first number
    row, col = first_pos // n, first_pos % n
    square[row][col] = first_num
    
    # Continue solving from the next position
    solve_magic_square_recursive(square, n, first_pos + 1, magic_squares, stats)
    
    # Print squares found by this worker
    for i, square in enumerate(magic_squares, 1):
        print(f"\nFound magic square #{i} (worker {first_num},{first_pos}):")
        print(square)
    
    return magic_squares, stats['attempts']

def solve_magic_square_recursive(square, n, pos, magic_squares, stats):
    stats['attempts'] += 1
    
    if pos >= n * n:
        return
    
    row = pos // n
    col = pos % n
    
    for num in range(1, n*n + 1):
        if is_valid(square, n, row, col, num):
            square[row][col] = num
            
            if check_partial_sums(square, n, pos):
                if pos == n*n - 1:  # Last position
                    magic_squares.append(np.copy(square))
                else:
                    solve_magic_square_recursive(square, n, pos + 1, magic_squares, stats)
            
            square[row][col] = 0  # Backtrack

def save_magic_squares(magic_squares, elapsed_time):
    """Save magic squares to files with timestamp and statistics"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Create data directory if it doesn't exist
    data_dir = "../data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Save in numpy format
    np_filename = os.path.join(data_dir, f"magic_squares_{timestamp}.npy")
    np.save(np_filename, np.array(magic_squares))
    
    # Save in text format with statistics
    txt_filename = os.path.join(data_dir, f"magic_squares_{timestamp}.txt")
    with open(txt_filename, 'w') as f:
        f.write(f"4x4 Magic Squares Found: {len(magic_squares)}\n")
        f.write(f"Time taken: {elapsed_time:.2f} seconds\n\n")
        
        for i, square in enumerate(magic_squares, 1):
            f.write(f"Magic Square #{i}:\n")
            f.write(str(square) + "\n\n")
    
    print(f"\nSquares saved to {np_filename} and {txt_filename}")

def solve_magic_square_worker_wrapper(args_with_counter):
    args, counter = args_with_counter[:-1], args_with_counter[-1]
    return solve_magic_square_worker(args + (counter,))

def generate_magic_squares(n_squares=100, order=4):
    """
    Generate a set of magic squares.
    
    Parameters:
    -----------
    n_squares : int
        Number of squares to generate
    order : int
        Order of the magic squares (size of each side)
        
    Returns:
    --------
    np.ndarray
        Array of magic squares with shape (n_squares, order, order)
    """
    # For now, just generate random squares as a placeholder
    # In a real implementation, this would use proper magic square generation algorithms
    squares = []
    for _ in range(n_squares):
        square = np.random.permutation(order * order).reshape(order, order) + 1
        squares.append(square)
    
    return np.array(squares)

if __name__ == '__main__':
    # Generate magic squares
    n = 4
    magic_squares = generate_magic_squares(n)