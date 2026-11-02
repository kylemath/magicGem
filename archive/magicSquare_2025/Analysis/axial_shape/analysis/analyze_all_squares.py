import numpy as np
import pandas as pd
from axialDay2 import AxialAnalyzer
import os
from tqdm import tqdm  # for progress bar

def load_squares():
    """Load the 880 unique magic squares."""
    squares_path = '../../magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, squares_path)
    
    if not os.path.exists(full_path):
        # Try the root directory
        root_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 
                                'magic_squares/src/analysis/cache/magic_squares_20241031_133039.npy')
        if os.path.exists(root_path):
            return np.load(root_path)
        raise FileNotFoundError(f"Could not find magic squares file at {full_path} or {root_path}")
    
    return np.load(full_path)

def analyze_squares(squares):
    """Analyze all squares and collect metrics."""
    results = []
    eigenvectors_list = []  # New list to store eigenvectors
    
    for i, square in enumerate(tqdm(squares, desc="Analyzing squares")):
        analyzer = AxialAnalyzer(square)
        metrics = analyzer.compute_balance_metrics()
        
        # Extract key metrics
        result = {
            'square_id': i,
            'balance_measure': metrics['balance_measure'],
            'rms_distance': metrics['rms_distance'],
            'condition_number': metrics['condition_number'],
            'skewness_magnitude': metrics['skewness_magnitude'],
            'eigenvalue_1': metrics['eigenvalues'][0],
            'eigenvalue_2': metrics['eigenvalues'][1],
            'eigenvalue_3': metrics['eigenvalues'][2],
            'mean_vector_magnitude': np.linalg.norm(metrics['mean_vector'])
        }
        results.append(result)
        eigenvectors_list.append(metrics['eigenvectors'])  # Store eigenvectors
    
    return pd.DataFrame(results), np.array(eigenvectors_list)  # Return both results and eigenvectors

def analyze_and_save():
    """Main function to run analysis and save results."""
    # Create output directory
    os.makedirs('figures_all_squares', exist_ok=True)
    
    # Load squares
    print("Loading magic squares...")
    squares = load_squares()
    print(f"Loaded {len(squares)} squares")
    
    # Analyze squares
    print("Analyzing squares...")
    results_df, eigenvectors = analyze_squares(squares)  # Get both results and eigenvectors
    
    # Save results
    results_df.to_csv('figures_all_squares/balance_metrics.csv', index=False)
    np.save('figures_all_squares/eigenvectors.npy', eigenvectors)  # Save eigenvectors
    
    # Compute summary statistics
    summary = results_df.describe()
    summary.to_csv('figures_all_squares/balance_metrics_summary.csv')
    
    # Print key findings
    print("\nAnalysis Complete!")
    print("\nSummary Statistics:")
    print("==================")
    print(f"Average balance measure: {results_df['balance_measure'].mean():.3f}")
    print(f"Average condition number: {results_df['condition_number'].mean():.3f}")
    print(f"Average skewness magnitude: {results_df['skewness_magnitude'].mean():.3f}")
    
    # Find interesting squares
    most_balanced = results_df.loc[results_df['balance_measure'].idxmin()]
    least_balanced = results_df.loc[results_df['balance_measure'].idxmax()]
    most_symmetric = results_df.loc[results_df['condition_number'].idxmin()]
    
    print("\nInteresting Squares:")
    print("==================")
    print(f"Most balanced square ID: {most_balanced['square_id']}")
    print(f"Least balanced square ID: {least_balanced['square_id']}")
    print(f"Most symmetric square ID: {most_symmetric['square_id']}")

if __name__ == '__main__':
    analyze_and_save() 