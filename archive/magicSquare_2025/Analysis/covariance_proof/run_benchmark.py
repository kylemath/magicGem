#!/usr/bin/env python3
"""
Benchmark Script for Magic Square Optimization with One-Cycle Policy

This script runs a large batch of experiments with the one-cycle learning rate 
scheduler to establish benchmarks for magic square optimization performance.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import seaborn as sns
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import confusion_matrix

# Import the necessary modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_hybrid_approach import EnhancedMagicSquareAnalyzer, run_experiment
from parallel_search import analyze_magic_square

# Configuration parameters
DEFAULT_TRIALS = 30
DEFAULT_WORKERS = 8
DEFAULT_STEPS = 400
BENCHMARK_DIR = 'covariance_proof/benchmark_results'
SCHEDULER = 'one_cycle'  # Focus on our best performer

# Custom JSON encoder to handle numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def run_single_experiment(config):
    """Run a single experiment with the given configuration."""
    # Extract parameters
    trial_id = config['trial_id']
    transition_start = config['transition_start']
    transition_end = config['transition_end']
    total_steps = config['total_steps']
    learning_rate = config['learning_rate']
    swaps = config['swaps']
    
    print(f"Starting trial {trial_id}: TS={transition_start}, TE={transition_end}, Steps={total_steps}, LR={learning_rate}, Swaps={swaps}")
    
    # Run experiment
    result = run_experiment(
        transition_start=transition_start,
        transition_end=transition_end,
        total_steps=total_steps,
        learning_rate=learning_rate,
        swaps=swaps,
        enforce_monotonic=True,
        learning_rate_scheduler=SCHEDULER,
        verbose=False  # Disable verbose output for batch runs
    )
    
    # Add trial ID to the result
    result['trial_id'] = trial_id
    
    # Check if we found a magic square
    if result['final_metrics']['is_magic']:
        print(f"★ Found a magic square in trial {trial_id}! ★")
    
    print(f"Completed trial {trial_id}: Final distance = {result['final_metrics']['distance']:.8f}")
    
    return result

def run_benchmark(num_trials=DEFAULT_TRIALS, max_workers=DEFAULT_WORKERS, total_steps=DEFAULT_STEPS):
    """Run benchmark with multiple trials and parameter configurations."""
    print(f"\nRunning benchmark with {num_trials} trials, {max_workers} workers, and {total_steps} steps")
    
    # Ensure output directory exists
    os.makedirs(BENCHMARK_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Set up parameter variations for the experiments
    configurations = []
    
    # Base configuration ranges
    base_lr_values = [0.1, 0.12, 0.15]
    swap_values = [1, 2, 3]
    
    # Try different transition phase lengths and positions
    trial_id = 1
    for lr in base_lr_values:
        for swaps in swap_values:
            # Short transition phase early
            configurations.append({
                'trial_id': trial_id,
                'transition_start': int(total_steps * 0.2),
                'transition_end': int(total_steps * 0.4),
                'total_steps': total_steps,
                'learning_rate': lr,
                'swaps': swaps
            })
            trial_id += 1
            
            # Long transition phase middle
            configurations.append({
                'trial_id': trial_id,
                'transition_start': int(total_steps * 0.3),
                'transition_end': int(total_steps * 0.7),
                'total_steps': total_steps,
                'learning_rate': lr,
                'swaps': swaps
            })
            trial_id += 1
            
            # Late transition phase
            configurations.append({
                'trial_id': trial_id,
                'transition_start': int(total_steps * 0.5),
                'transition_end': int(total_steps * 0.8),
                'total_steps': total_steps,
                'learning_rate': lr,
                'swaps': swaps
            })
            trial_id += 1
    
    # Ensure we have at least the requested number of trials
    while len(configurations) < num_trials:
        # Add more random configurations if needed
        configurations.append({
            'trial_id': trial_id,
            'transition_start': np.random.randint(int(total_steps * 0.2), int(total_steps * 0.5)),
            'transition_end': np.random.randint(int(total_steps * 0.6), int(total_steps * 0.9)),
            'total_steps': total_steps,
            'learning_rate': np.random.choice(base_lr_values),
            'swaps': np.random.choice(swap_values)
        })
        trial_id += 1
    
    # Limit configurations to the requested number
    configurations = configurations[:num_trials]
    
    start_time = time.time()
    results = []
    
    # Run experiments with parallel processing
    if max_workers > 1:
        print(f"Running {len(configurations)} experiments in parallel with {max_workers} workers")
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(run_single_experiment, config) for config in configurations]
            
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error in experiment: {str(e)}")
    else:
        print(f"Running {len(configurations)} experiments sequentially")
        for config in configurations:
            try:
                result = run_single_experiment(config)
                results.append(result)
            except Exception as e:
                print(f"Error in experiment: {str(e)}")
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nCompleted {len(results)} experiments in {total_time:.2f} seconds")
    
    # Process and analyze results
    magic_squares = [r for r in results if r['final_metrics']['is_magic']]
    success_rate = len(magic_squares) / len(results) * 100
    
    print(f"\nBenchmark Results Summary:")
    print(f"Total experiments: {len(results)}")
    print(f"Magic squares found: {len(magic_squares)}")
    print(f"Success rate: {success_rate:.2f}%")
    
    # Calculate statistics
    final_distances = [r['final_metrics']['distance'] for r in results]
    final_sum_errors = [r['final_metrics']['sum_error'] for r in results]
    int_deviations = [r['final_metrics']['int_dev'] for r in results]
    
    print(f"Average final distance: {np.mean(final_distances):.8f}")
    print(f"Median final distance: {np.median(final_distances):.8f}")
    print(f"Min final distance: {np.min(final_distances):.8f}")
    print(f"Average sum error: {np.mean(final_sum_errors):.8f}")
    print(f"Average integer deviation: {np.mean(int_deviations):.8f}")
    
    # Save detailed results
    results_file = f"{BENCHMARK_DIR}/benchmark_results_{timestamp}.json"
    
    # Make results JSON serializable
    serializable_results = []
    for result in results:
        serializable_result = {
            'trial_id': result['trial_id'],
            'parameters': result['parameters'],
            'initial_metrics': result['initial_metrics'],
            'final_metrics': result['final_metrics'],
            'computation_time': result['computation_time']
        }
        
        # Convert NumPy arrays to lists for any arrays
        if 'final_square' in result:
            serializable_result['final_square'] = result['final_square'].tolist()
        
        serializable_results.append(serializable_result)
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2, cls=NumpyEncoder)
    
    # Create a DataFrame for analysis
    df_data = []
    for result in results:
        config = result['parameters']
        metrics = result['final_metrics']
        
        df_data.append({
            'trial_id': result['trial_id'],
            'transition_start': config['transition_start'],
            'transition_end': config['transition_end'],
            'transition_length': config['transition_end'] - config['transition_start'],
            'total_steps': config['total_steps'],
            'learning_rate': config['learning_rate'],
            'swaps': config['swaps'],
            'final_distance': metrics['distance'],
            'sum_error': metrics['sum_error'],
            'int_deviation': metrics['int_dev'],
            'is_magic': metrics['is_magic'],
            'computation_time': result['computation_time']
        })
    
    df = pd.DataFrame(df_data)
    
    # Save to CSV
    csv_file = f"{BENCHMARK_DIR}/benchmark_data_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    
    # Generate visualizations
    visualize_benchmark_results(df, timestamp)
    
    # Save any magic squares found
    if magic_squares:
        for i, result in enumerate(magic_squares):
            square = np.array(result['final_square'])
            
            # Save visualization of the magic square
            plt.figure(figsize=(8, 8))
            plt.imshow(square, cmap='viridis')
            plt.colorbar()
            plt.title(f"Magic Square #{i+1}")
            
            for i in range(square.shape[0]):
                for j in range(square.shape[1]):
                    plt.text(j, i, f"{square[i, j]:.1f}", ha="center", va="center", color="w")
            
            magic_square_file = f"{BENCHMARK_DIR}/magic_square_{i+1}_{timestamp}.png"
            plt.tight_layout()
            plt.savefig(magic_square_file)
            plt.close()
            
            print(f"Magic square visualization saved to {magic_square_file}")
    
    return results, df, results_file, csv_file

def visualize_benchmark_results(df, timestamp):
    """Create visualizations for benchmark results."""
    # Set Seaborn style
    sns.set(style="whitegrid")
    
    # Create output directory for visualizations
    viz_dir = f"{BENCHMARK_DIR}/visualizations_{timestamp}"
    os.makedirs(viz_dir, exist_ok=True)
    
    # 1. Parameter correlation with final distance
    plt.figure(figsize=(15, 10))
    
    # Transition start vs final distance
    plt.subplot(2, 3, 1)
    sns.scatterplot(data=df, x='transition_start', y='final_distance', hue='learning_rate')
    plt.title('Transition Start vs Final Distance')
    plt.yscale('log')
    
    # Transition length vs final distance
    plt.subplot(2, 3, 2)
    sns.scatterplot(data=df, x='transition_length', y='final_distance', hue='learning_rate')
    plt.title('Transition Length vs Final Distance')
    plt.yscale('log')
    
    # Learning rate vs final distance
    plt.subplot(2, 3, 3)
    sns.boxplot(data=df, x='learning_rate', y='final_distance')
    plt.title('Learning Rate vs Final Distance')
    plt.yscale('log')
    
    # Swaps vs final distance
    plt.subplot(2, 3, 4)
    sns.boxplot(data=df, x='swaps', y='final_distance')
    plt.title('Initial Perturbation vs Final Distance')
    plt.yscale('log')
    
    # Computation time by learning rate
    plt.subplot(2, 3, 5)
    sns.boxplot(data=df, x='learning_rate', y='computation_time')
    plt.title('Computation Time by Learning Rate')
    
    # Distance vs integer deviation
    plt.subplot(2, 3, 6)
    sns.scatterplot(data=df, x='final_distance', y='int_deviation', hue='learning_rate')
    plt.title('Distance vs Integer Deviation')
    plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/parameter_correlations.png")
    plt.close()
    
    # 2. Distribution of final metrics
    plt.figure(figsize=(15, 6))
    
    # Final distance distribution
    plt.subplot(1, 3, 1)
    sns.histplot(df['final_distance'], kde=True)
    plt.title('Final Distance Distribution')
    plt.xlabel('Distance')
    plt.xscale('log')
    
    # Sum error distribution
    plt.subplot(1, 3, 2)
    sns.histplot(df['sum_error'], kde=True)
    plt.title('Sum Error Distribution')
    plt.xlabel('Error')
    plt.xscale('log')
    
    # Integer deviation distribution
    plt.subplot(1, 3, 3)
    sns.histplot(df['int_deviation'], kde=True)
    plt.title('Integer Deviation Distribution')
    plt.xlabel('Deviation')
    
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/metric_distributions.png")
    plt.close()
    
    # 3. Find optimal parameter combinations
    # Sort data by final distance
    top_results = df.sort_values('final_distance').head(10)
    
    plt.figure(figsize=(12, 8))
    
    # Plot parallel coordinates for top results
    # Normalize the data for better visualization
    from sklearn.preprocessing import MinMaxScaler
    
    # Select columns to plot
    params = ['transition_start', 'transition_length', 'learning_rate', 'swaps', 
              'final_distance', 'sum_error', 'int_deviation']
    
    # Create a copy for normalization
    top_norm = top_results[params].copy()
    
    # Scale the data
    scaler = MinMaxScaler()
    top_scaled = scaler.fit_transform(top_norm)
    top_scaled_df = pd.DataFrame(top_scaled, columns=params)
    
    # Add trial_id for reference
    top_scaled_df['trial_id'] = top_results['trial_id'].values
    
    # Plot parallel coordinates
    pd.plotting.parallel_coordinates(top_scaled_df, 'trial_id')
    plt.title('Parameter Combinations for Top 10 Results')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/optimal_parameters.png")
    plt.close()
    
    # 4. Heatmap for transition parameters vs final distance
    # Create bins for transition start and length
    df['ts_bin'] = pd.cut(df['transition_start'], bins=5)
    df['tl_bin'] = pd.cut(df['transition_length'], bins=5)
    
    # Create a pivot table
    pivot = df.pivot_table(
        values='final_distance', 
        index='ts_bin',
        columns='tl_bin',
        aggfunc='mean'
    )
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, fmt=".6f", cmap="YlGnBu")
    plt.title('Average Final Distance by Transition Parameters')
    plt.xlabel('Transition Length')
    plt.ylabel('Transition Start')
    
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/transition_heatmap.png")
    plt.close()
    
    print(f"Benchmark visualizations saved to {viz_dir}")

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Run benchmark for magic square optimization')
    parser.add_argument('--trials', type=int, default=DEFAULT_TRIALS, 
                        help=f'Number of trials to run (default: {DEFAULT_TRIALS})')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS, 
                        help=f'Number of parallel workers (default: {DEFAULT_WORKERS})')
    parser.add_argument('--steps', type=int, default=DEFAULT_STEPS, 
                        help=f'Number of optimization steps per trial (default: {DEFAULT_STEPS})')
    args = parser.parse_args()
    
    print("Magic Square Optimization Benchmark - One-Cycle Policy")
    print("=====================================================")
    
    # Run benchmark
    results, df, results_file, csv_file = run_benchmark(
        num_trials=args.trials,
        max_workers=args.workers,
        total_steps=args.steps
    )
    
    print("\nBenchmark complete!")
    print(f"Results saved to: {results_file}")
    print(f"CSV data saved to: {csv_file}")
    
    # Print optimal parameter combinations
    top_5 = df.sort_values('final_distance').head(5)
    
    print("\nTop 5 Parameter Combinations:")
    print("============================")
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"{i}. Trial {row['trial_id']}:")
        print(f"   Transition: {row['transition_start']}-{row['transition_end']} (Length: {row['transition_length']})")
        print(f"   Learning Rate: {row['learning_rate']}, Swaps: {row['swaps']}")
        print(f"   Final Distance: {row['final_distance']:.8f}")
        print(f"   Sum Error: {row['sum_error']:.8f}")
        print(f"   Integer Deviation: {row['int_deviation']:.6f}")
        print(f"   Is Magic: {row['is_magic']}")
        print() 