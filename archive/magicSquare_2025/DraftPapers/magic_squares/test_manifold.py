#!/usr/bin/env python3
"""
Focused test script for magic squares manifold analysis.

This script tests only the manifold analysis components to enable rapid debugging
without running the full pipeline each time.
"""

import os
import numpy as np
from datetime import datetime

def ensure_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def test_manifold_analysis():
    """Test just the manifold analysis components."""
    print("=" * 80)
    print("MAGIC SQUARES MANIFOLD ANALYSIS TEST")
    print("=" * 80)
    
    # Import required functions
    from magic_squares.analysis.visualization import analyze_manifold
    
    # Load squares from cache
    data_file = 'magic_squares/data/magic_squares_20241031_133039.npy'
    print(f"\nLoading squares from {data_file}")
    squares = np.load(data_file)
    print(f"Loaded {len(squares)} squares")
    
    # Take a small sample for testing
    np.random.seed(42)  # For reproducibility
    sample_size = 100
    sample_indices = np.random.choice(len(squares), sample_size, replace=False)
    squares = squares[sample_indices]
    print(f"Using a sample of {sample_size} squares for testing")
    
    # Create cache directory if it doesn't exist
    cache_dir = os.path.join("magic_squares", "analysis", "cache")
    ensure_directory(cache_dir)
    
    # Normalize squares for manifold analysis
    print("\nNormalizing squares...")
    normalized_squares = [square / np.sum(square) for square in squares]
    
    try:
        # Run manifold analysis
        print("\nRunning manifold analysis...")
        manifold_stats = analyze_manifold(normalized_squares)
        
        # Print results
        print("\nManifold Analysis Results:")
        print("-" * 40)
        
        print("\nDimension Estimates:")
        for method, stats in manifold_stats['dimension_estimates'].items():
            if 'dimension' in stats:
                print(f"{method}: {stats['dimension']:.2f}")
            else:
                print(f"{method}: {stats['dimension_min']:.2f}-{stats['dimension_max']:.2f}")
        
        print("\nLocal Structure:")
        local = manifold_stats['local_structure']
        print(f"Average neighborhood size: {local['avg_neighborhood_size']:.4f} ± {local['std_neighborhood_size']:.4f}")
        print(f"Local variation: {local['local_variation']:.4f}")
        
        print("\nCurvature:")
        curv = manifold_stats['curvature']
        print(f"Triangle inequality violation rate: {curv['violation_rate']*100:.2f}%")
        print(f"Maximum violation: {curv['max_violation']:.4f}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print("\nError during manifold analysis:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Print additional debugging information
        print("\nDebugging Information:")
        print("-" * 40)
        
        # Check cache file
        cache_file = os.path.join(cache_dir, "emd_distances.pkl")
        if os.path.exists(cache_file):
            import pickle
            print(f"\nExamining cache file: {cache_file}")
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                print(f"Cache data type: {type(cache_data)}")
                if isinstance(cache_data, tuple):
                    print(f"Cache data is a tuple with {len(cache_data)} elements")
                    for i, item in enumerate(cache_data):
                        print(f"Element {i} type: {type(item)}")
                        if isinstance(item, np.ndarray):
                            print(f"Element {i} shape: {item.shape}")
            except Exception as cache_error:
                print(f"Error reading cache: {str(cache_error)}")
        else:
            print(f"Cache file not found: {cache_file}")
        
        return 1
    
    return 0

if __name__ == "__main__":
    exit(test_manifold_analysis()) 