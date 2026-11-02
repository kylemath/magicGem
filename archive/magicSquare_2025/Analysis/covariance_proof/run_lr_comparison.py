#!/usr/bin/env python3
"""
Learning Rate Scheduler Comparison for Magic Square Optimization

This script compares the effectiveness of different learning rate scheduling 
strategies for magic square optimization, measuring convergence speed, 
solution quality, and computational efficiency.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

# Import the necessary modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_hybrid_approach import EnhancedMagicSquareAnalyzer, run_experiment
from parallel_search import analyze_magic_square

def run_scheduler_experiment(scheduler_name, total_steps=300, trials=5):
    """Run experiments for a specific scheduler with multiple trials."""
    print(f"\nRunning experiments for {scheduler_name} scheduler ({trials} trials)...")
    
    results = []
    found_magic_squares = []
    
    for trial in range(1, trials + 1):
        print(f"  Trial {trial}/{trials}")
        
        # Use standard parameters
        transition_start = 100
        transition_end = 200 
        learning_rate = 0.1
        
        # Run experiment
        result = run_experiment(
            transition_start=transition_start,
            transition_end=transition_end,
            total_steps=total_steps,
            learning_rate=learning_rate,
            swaps=2,  # Moderate perturbation level
            enforce_monotonic=True,
            learning_rate_scheduler=scheduler_name,
            verbose=False  # Disable verbose output for batch runs
        )
        
        # Track if we found a magic square
        if result['final_metrics']['is_magic']:
            print(f"    Found a magic square in trial {trial}!")
            found_magic_squares.append(result)
        
        # Store result
        results.append(result)
    
    return {
        'scheduler': scheduler_name,
        'all_results': results,
        'magic_squares': found_magic_squares,
        'summary': get_summary_statistics(results)
    }

def get_summary_statistics(results):
    """Compute summary statistics from a list of experiment results."""
    # Extract metrics
    initial_distances = [r['initial_metrics']['distance'] for r in results]
    final_distances = [r['final_metrics']['distance'] for r in results]
    initial_sum_errors = [r['initial_metrics']['sum_error'] for r in results]
    final_sum_errors = [r['final_metrics']['sum_error'] for r in results]
    int_devs = [r['final_metrics']['int_dev'] for r in results]
    compute_times = [r['computation_time'] for r in results]
    magic_count = sum(1 for r in results if r['final_metrics']['is_magic'])
    
    # Calculate improvement percentages
    improvements = [100 * (initial - final) / max(initial, 1e-10) 
                   for initial, final in zip(initial_distances, final_distances)]
    
    return {
        'num_trials': len(results),
        'avg_initial_distance': np.mean(initial_distances),
        'avg_final_distance': np.mean(final_distances),
        'min_final_distance': np.min(final_distances),
        'avg_initial_sum_error': np.mean(initial_sum_errors),
        'avg_final_sum_error': np.mean(final_sum_errors),
        'avg_int_dev': np.mean(int_devs),
        'avg_compute_time': np.mean(compute_times),
        'avg_improvement_pct': np.mean(improvements),
        'magic_squares_found': magic_count,
        'success_rate': 100 * magic_count / len(results)
    }

def generate_comparison_report(experiment_results, output_dir='covariance_proof/lr_comparison'):
    """Generate detailed comparison report with visualizations."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. Save raw results
    results_file = f"{output_dir}/lr_comparison_results_{timestamp}.json"
    
    # Convert NumPy arrays for JSON serialization
    serializable_results = []
    for scheduler_result in experiment_results:
        serializable_result = {
            'scheduler': scheduler_result['scheduler'],
            'summary': scheduler_result['summary'],
            'magic_squares_count': len(scheduler_result['magic_squares'])
        }
        serializable_results.append(serializable_result)
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    # 2. Generate comparison visualizations
    
    # Get schedulers and summaries
    schedulers = [r['scheduler'] for r in experiment_results]
    summaries = [r['summary'] for r in experiment_results]
    
    # Comparative bar chart for key metrics
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    
    # Final distance
    axs[0, 0].bar(schedulers, [s['avg_final_distance'] for s in summaries])
    axs[0, 0].set_title('Average Final Distance')
    axs[0, 0].set_ylabel('Distance')
    axs[0, 0].set_yscale('log')
    
    # Final sum error
    axs[0, 1].bar(schedulers, [s['avg_final_sum_error'] for s in summaries])
    axs[0, 1].set_title('Average Final Sum Error')
    axs[0, 1].set_ylabel('Error')
    axs[0, 1].set_yscale('log')
    
    # Integer deviation
    axs[1, 0].bar(schedulers, [s['avg_int_dev'] for s in summaries])
    axs[1, 0].set_title('Average Integer Deviation')
    axs[1, 0].set_ylabel('Deviation')
    
    # Success rate
    axs[1, 1].bar(schedulers, [s['success_rate'] for s in summaries])
    axs[1, 1].set_title('Success Rate (%)')
    axs[1, 1].set_ylabel('Percentage')
    
    plt.tight_layout()
    summary_file = f"{output_dir}/lr_comparison_metrics_{timestamp}.png"
    plt.savefig(summary_file)
    plt.close()
    
    # Performance improvement chart
    plt.figure(figsize=(12, 6))
    
    bars = plt.bar(schedulers, [s['avg_improvement_pct'] for s in summaries])
    
    # Add computation time annotations
    for i, bar in enumerate(bars):
        height = bar.get_height()
        time_value = summaries[i]['avg_compute_time']
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{time_value:.2f}s',
                ha='center', va='bottom', rotation=0)
    
    plt.title('Average Distance Improvement (%) and Computation Time')
    plt.ylabel('Improvement %')
    plt.grid(axis='y')
    
    improv_file = f"{output_dir}/lr_comparison_improvement_{timestamp}.png"
    plt.savefig(improv_file)
    plt.close()
    
    # Generate summary table
    print("\n===== Learning Rate Scheduler Comparison =====")
    print(f"{'Scheduler':<20} {'Avg Final Dist':>15} {'Improvement %':>15} {'Success Rate':>15} {'Compute Time':>15}")
    print("-" * 80)
    
    for scheduler, summary in zip(schedulers, summaries):
        print(f"{scheduler:<20} {summary['avg_final_distance']:>15.8f} {summary['avg_improvement_pct']:>15.2f}% {summary['success_rate']:>15.2f}% {summary['avg_compute_time']:>15.2f}s")
    
    print(f"\nDetailed results saved to {results_file}")
    print(f"Comparison metrics chart saved to {summary_file}")
    print(f"Improvement comparison chart saved to {improv_file}")
    
    return results_file, summary_file, improv_file

def run_full_comparison(total_steps=300, trials_per_scheduler=5, max_workers=4):
    """Run full comparison of all learning rate schedulers."""
    start_time = time.time()
    
    # List of schedulers to test
    schedulers = ['one_cycle', 'cosine_annealing', 'triangular', 'constant']
    
    # Run experiments with parallel processing
    all_results = []
    
    if max_workers > 1:
        # Parallel execution
        print(f"Running experiments in parallel with {max_workers} workers")
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_scheduler = {
                executor.submit(run_scheduler_experiment, scheduler, total_steps, trials_per_scheduler): scheduler
                for scheduler in schedulers
            }
            
            for future in future_to_scheduler:
                scheduler = future_to_scheduler[future]
                try:
                    result = future.result()
                    all_results.append(result)
                    print(f"Completed experiments for {scheduler}")
                except Exception as e:
                    print(f"Error in experiments for {scheduler}: {str(e)}")
    else:
        # Sequential execution
        print("Running experiments sequentially")
        for scheduler in schedulers:
            result = run_scheduler_experiment(scheduler, total_steps, trials_per_scheduler)
            all_results.append(result)
    
    # Generate comparison report
    results_file, summary_file, improv_file = generate_comparison_report(all_results)
    
    # Display any magic squares found
    magic_count = sum(len(r['magic_squares']) for r in all_results)
    if magic_count > 0:
        print(f"\nFound {magic_count} magic squares across all experiments:")
        for i, result in enumerate(all_results):
            if result['magic_squares']:
                print(f"\n{result['scheduler']} scheduler found {len(result['magic_squares'])} magic squares:")
                for j, ms_result in enumerate(result['magic_squares']):
                    print(f"  Magic Square {j+1}:")
                    print(np.array(ms_result['final_square']))
    
    end_time = time.time()
    print(f"\nFull comparison completed in {end_time - start_time:.2f} seconds")
    
    return all_results, results_file, summary_file, improv_file

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Compare learning rate schedulers for magic square optimization')
    parser.add_argument('--steps', type=int, default=300, help='Total optimization steps')
    parser.add_argument('--trials', type=int, default=5, help='Trials per scheduler')
    parser.add_argument('--workers', type=int, default=1, help='Number of parallel workers')
    args = parser.parse_args()
    
    print("Learning Rate Scheduler Comparison for Magic Square Optimization")
    print("=============================================================")
    print(f"Total Steps: {args.steps}, Trials per Scheduler: {args.trials}, Workers: {args.workers}")
    
    # Run comparison
    run_full_comparison(
        total_steps=args.steps,
        trials_per_scheduler=args.trials,
        max_workers=args.workers
    ) 