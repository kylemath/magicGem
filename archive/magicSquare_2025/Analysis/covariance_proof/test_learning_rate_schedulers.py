#!/usr/bin/env python3
"""
Test script for learning rate schedulers

This script tests and visualizes the different learning rate scheduling strategies
implemented in the magic square gradient localization algorithm.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from datetime import datetime

# Import the necessary classes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from magic_square_gradient_flow import MagicSquareAnalyzer
from enhanced_hybrid_approach import EnhancedMagicSquareAnalyzer

def visualize_learning_rate_schedules(total_steps=300, base_lr=0.1):
    """Visualize the different learning rate scheduling strategies."""
    # Initialize analyzer
    analyzer = MagicSquareAnalyzer()
    
    # Learning rate parameters
    max_lr = base_lr * 1.5
    min_lr = base_lr * 0.1
    cycle_length = total_steps // 3
    
    # Collect learning rates for different schedulers
    steps = np.arange(total_steps)
    one_cycle_lrs = [analyzer.compute_one_cycle_learning_rate(step, total_steps, max_lr, min_lr) for step in steps]
    cosine_lrs = [analyzer.compute_cosine_annealing_lr(step, cycle_length, max_lr, min_lr) for step in steps]
    triangular_lrs = [analyzer.compute_triangular_cyclic_lr(step, cycle_length, max_lr, min_lr) for step in steps]
    constant_lrs = [base_lr for _ in steps]
    phase_decayed_lrs = []
    
    for step in steps:
        if step < total_steps / 3:
            phase = 0.0
        elif step > 2 * total_steps / 3:
            phase = 1.0
        else:
            phase = (step - total_steps / 3) / (total_steps / 3)
        phase_decayed_lrs.append(base_lr * (1.0 - 0.5 * phase))
    
    # Plot learning rate schedules
    plt.figure(figsize=(12, 8))
    plt.plot(steps, one_cycle_lrs, 'r-', label='One Cycle Policy')
    plt.plot(steps, cosine_lrs, 'g-', label='Cosine Annealing')
    plt.plot(steps, triangular_lrs, 'b-', label='Triangular Cyclic')
    plt.plot(steps, constant_lrs, 'k--', label='Constant')
    plt.plot(steps, phase_decayed_lrs, 'm-', label='Phase-decayed Constant')
    
    plt.title(f'Learning Rate Scheduling Strategies (Base LR={base_lr})')
    plt.xlabel('Steps')
    plt.ylabel('Learning Rate')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'covariance_proof/lr_schedules_{timestamp}.png')
    plt.close()
    
    print(f"Learning rate schedule visualization saved to covariance_proof/lr_schedules_{timestamp}.png")
    return f'covariance_proof/lr_schedules_{timestamp}.png'

def test_enhanced_analyzer_with_schedulers():
    """Run quick tests with different learning rate schedulers."""
    print("Testing EnhancedMagicSquareAnalyzer with different learning rate schedulers")
    
    # Parameters for quick tests
    total_steps = 100
    transition_start = 30
    transition_end = 70
    learning_rate = 0.1
    
    # Test each scheduler
    schedulers = ['one_cycle', 'cosine_annealing', 'triangular', 'constant']
    results = {}
    
    for scheduler in schedulers:
        print(f"\nTesting {scheduler} scheduler")
        
        # Initialize analyzer
        analyzer = EnhancedMagicSquareAnalyzer()
        
        # Start from a perturbed square
        perturbed = analyzer.perturb_square(swaps=1)
        analyzer.square = perturbed
        analyzer.points = analyzer.create_axial_points()
        
        # Get initial metrics
        initial_distance = analyzer.compute_distance_to_manifold()
        initial_sum_error = analyzer.magic_sum_error()
        print(f"Initial Distance: {initial_distance:.8f}")
        print(f"Initial Sum Error: {initial_sum_error:.8f}")
        
        # Run gradual hybrid descent with selected scheduler
        start_time = time.time()
        trajectories, _, _ = analyzer.perform_gradual_hybrid_descent(
            total_steps=total_steps,
            learning_rate=learning_rate,
            transition_start=transition_start,
            transition_end=transition_end,
            enforce_monotonic=True,
            learning_rate_scheduler=scheduler,
            verbose=False
        )
        end_time = time.time()
        
        # Get final metrics
        final_distance = trajectories['distance'][-1]
        final_sum_error = trajectories['magic_sum_error'][-1]
        final_int_dev = trajectories['integer_deviation'][-1]
        
        print(f"Final Distance: {final_distance:.8f}")
        print(f"Final Sum Error: {final_sum_error:.8f}")
        print(f"Final Integer Deviation: {final_int_dev:.8f}")
        print(f"Computation Time: {end_time - start_time:.2f} seconds")
        
        results[scheduler] = {
            'initial_distance': initial_distance,
            'final_distance': final_distance,
            'initial_sum_error': initial_sum_error,
            'final_sum_error': final_sum_error,
            'final_int_dev': final_int_dev,
            'computation_time': end_time - start_time,
            'trajectories': trajectories
        }
        
        # Plot results for this scheduler
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_file = f'covariance_proof/test_{scheduler}_{timestamp}.png'
        
        plt.figure(figsize=(12, 10))
        
        # Plot learning rate
        plt.subplot(3, 1, 1)
        plt.plot(trajectories['learning_rate'], 'b-')
        plt.title(f'Learning Rate ({scheduler})')
        plt.xlabel('Steps')
        plt.ylabel('Learning Rate')
        plt.grid(True)
        
        # Plot distance
        plt.subplot(3, 1, 2)
        plt.plot(trajectories['distance'], 'r-')
        plt.title('Distance to Manifold')
        plt.xlabel('Steps')
        plt.ylabel('Distance')
        plt.yscale('log')
        plt.grid(True)
        
        # Plot sum error
        plt.subplot(3, 1, 3)
        plt.plot(trajectories['magic_sum_error'], 'g-')
        plt.title('Magic Sum Error')
        plt.xlabel('Steps')
        plt.ylabel('Error')
        plt.yscale('log')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.close()
        
        print(f"Test plots saved to {plot_file}")
    
    # Compare results
    print("\nComparison of Learning Rate Schedulers:")
    print("=======================================")
    print(f"{'Scheduler':<20} {'Initial Dist':>12} {'Final Dist':>12} {'Improvement':>12} {'Time (s)':>10}")
    print("-" * 70)
    
    for scheduler, result in results.items():
        improvement = (result['initial_distance'] - result['final_distance']) / result['initial_distance'] * 100
        print(f"{scheduler:<20} {result['initial_distance']:>12.8f} {result['final_distance']:>12.8f} {improvement:>11.2f}% {result['computation_time']:>10.2f}")
    
    # Plot comparison of trajectories
    plt.figure(figsize=(15, 10))
    
    # Plot distance comparison
    plt.subplot(2, 1, 1)
    for scheduler, result in results.items():
        plt.plot(result['trajectories']['distance'], label=scheduler)
    plt.title('Distance to Manifold Comparison')
    plt.xlabel('Steps')
    plt.ylabel('Distance')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    
    # Plot learning rate comparison
    plt.subplot(2, 1, 2)
    for scheduler, result in results.items():
        plt.plot(result['trajectories']['learning_rate'], label=scheduler)
    plt.title('Learning Rate Comparison')
    plt.xlabel('Steps')
    plt.ylabel('Learning Rate')
    plt.legend()
    plt.grid(True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    comparison_file = f'covariance_proof/scheduler_comparison_{timestamp}.png'
    plt.tight_layout()
    plt.savefig(comparison_file)
    plt.close()
    
    print(f"\nComparison plot saved to {comparison_file}")
    
    return results, comparison_file

if __name__ == "__main__":
    print("Testing Learning Rate Schedulers")
    print("===============================")
    
    # Visualize learning rate schedules
    lr_viz_file = visualize_learning_rate_schedules()
    
    # Test schedulers with enhanced analyzer
    test_enhanced_analyzer_with_schedulers()
    
    print("\nAll tests completed successfully!") 