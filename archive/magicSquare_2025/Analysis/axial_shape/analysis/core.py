import numpy as np
import os

def load_latest_squares():
    """Load magic squares from the .npy file."""
    squares_path = '../../magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, squares_path)
    
    if not os.path.exists(full_path):
        # Try the root directory
        root_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 
                                'magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy')
        if os.path.exists(root_path):
            squares = np.load(root_path)
        else:
            # Create a sample magic square for testing
            squares = np.array([
                [[16, 3, 2, 13],
                 [5, 10, 11, 8],
                 [9, 6, 7, 12],
                 [4, 15, 14, 1]]
            ])
    else:
        squares = np.load(full_path)
        
    return squares 