#!/usr/bin/env python3
"""
Enhanced Hybrid Approach for Magic Square Gradient Flow

This script implements an improved hybrid approach with gradual phase transition
between continuous and integer optimization, as outlined in the gradient locator plan.
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import random
import time
import os
import sys
from datetime import datetime

# Import the base MagicSquareAnalyzer class
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from magic_square_gradient_flow import MagicSquareAnalyzer

class EnhancedMagicSquareAnalyzer(MagicSquareAnalyzer):
    """Enhanced analyzer with gradual phase transition and adaptive projection."""
    
    def perform_gradual_hybrid_descent(self, total_steps=250, learning_rate=0.1, 
                                      transition_start=100, transition_end=200,
                                      max_projection_freq=5, initial_projection_freq=50,
                                      enforce_monotonic=True, learning_rate_scheduler='one_cycle',
                                      verbose=True):
        """
        Perform gradient descent with gradual transition from continuous to integer optimization.
        
        Parameters:
        -----------
        total_steps : int
            Total number of optimization steps
        learning_rate : float
            Initial learning rate
        transition_start : int
            Step at which to begin phase transition
        transition_end : int
            Step at which to complete phase transition
        max_projection_freq : int
            Maximum frequency of integer projections (minimum steps between projections)
        initial_projection_freq : int
            Initial frequency of integer projections
        enforce_monotonic : bool
            Whether to enforce monotonic values from 1-16
        learning_rate_scheduler : str
            Type of learning rate scheduler to use ('one_cycle', 'cosine_annealing', 'triangular', 'constant')
        verbose : bool
            Whether to print progress
        """
        # Ensure square is float type
        self.square = self.square.astype(float)
        
        # Save initial state
        initial_square = self.square.copy()
        trajectories = {
            'distance': [self.compute_distance_to_manifold()],
            'magic_sum_error': [self.magic_sum_error()],
            'integer_deviation': [np.sum(np.abs(self.square - np.round(self.square)))],
            'x_cov': [self.compute_covariance_constraints()[0]],
            'y_cov': [self.compute_covariance_constraints()[1]],
            'diag_main_cov': [self.compute_covariance_constraints()[2]],
            'diag_anti_cov': [self.compute_covariance_constraints()[3]],
            'phase': [0],  # Phase parameter from 0 (continuous) to 1 (integer)
            'temperature': [1.0],  # Controls how much integer properties are enforced
            'projection_strength': [0.0],  # How strongly we project to integers
            'monotonic_error': [0.0 if not enforce_monotonic else self.compute_monotonic_error()],
            'learning_rate': [learning_rate]  # Track learning rate changes
        }
        squares = [self.square.copy()]
        
        # ADAM optimizer parameters
        m = np.zeros_like(self.square)  # First moment
        v = np.zeros_like(self.square)  # Second moment
        beta1, beta2 = 0.9, 0.999
        epsilon = 1e-8
        t = 0
        
        # Best solution tracking
        best_distance = trajectories['distance'][0]
        best_square = self.square.copy()
        best_combined_score = float('inf')
        stagnation_count = 0
        
        # Adaptive parameters
        current_projection_freq = initial_projection_freq
        last_projection_step = 0
        
        # Learning rate parameters
        max_lr = learning_rate * 1.5  # Peak learning rate 
        min_lr = learning_rate * 0.1  # Minimum learning rate
        cycle_length = total_steps // 3  # For cyclic learning rate schedules
        
        if verbose:
            print(f"Using learning rate scheduler: {learning_rate_scheduler}")
            print(f"Min LR: {min_lr}, Max LR: {max_lr}, Cycle Length: {cycle_length}")
        
        for step in range(total_steps):
            t += 1
            
            # Compute phase parameter (0 to 1)
            if step < transition_start:
                phase = 0.0  # Pure continuous phase
            elif step > transition_end:
                phase = 1.0  # Pure integer phase
            else:
                # Linear transition
                phase = (step - transition_start) / (transition_end - transition_start)
            
            # Temperature parameter - starts high (1.0) and decreases
            temperature = max(0.01, 1.0 - 0.99 * phase)
            
            # Projection strength increases with phase
            projection_strength = phase
            
            # Update projection frequency based on phase
            if phase > 0:
                # As phase increases, projection frequency decreases (more frequent projections)
                current_projection_freq = max(max_projection_freq, 
                                            int(initial_projection_freq * (1 - 0.9 * phase)))
            
            # Compute gradient with analytical method
            gradient = self.compute_covariance_gradient()
            
            # Add monotonic constraint gradient if enabled
            if enforce_monotonic and phase > 0.5:
                monotonic_gradient = self.compute_monotonic_gradient()
                # Gradually increase the weight of the monotonic constraint
                monotonic_weight = min(1.0, (phase - 0.5) * 2)
                gradient = gradient + monotonic_weight * monotonic_gradient
            
            # Update with ADAM optimizer
            m = beta1 * m + (1 - beta1) * gradient
            v = beta2 * v + (1 - beta2) * (gradient**2)
            m_hat = m / (1 - beta1**t)
            v_hat = v / (1 - beta2**t)
            
            # Calculate learning rate based on selected scheduler
            current_phase_adjusted_max_lr = max_lr * (1.0 - 0.3 * phase)  # Reduce max lr gradually with phase
            
            if learning_rate_scheduler == 'one_cycle':
                current_lr = self.compute_one_cycle_learning_rate(
                    step=step,
                    total_steps=total_steps,
                    max_lr=current_phase_adjusted_max_lr,
                    min_lr=min_lr
                )
            elif learning_rate_scheduler == 'cosine_annealing':
                current_lr = self.compute_cosine_annealing_lr(
                    step=step,
                    cycle_length=cycle_length,
                    max_lr=current_phase_adjusted_max_lr,
                    min_lr=min_lr
                )
            elif learning_rate_scheduler == 'triangular':
                current_lr = self.compute_triangular_cyclic_lr(
                    step=step,
                    cycle_length=cycle_length,
                    max_lr=current_phase_adjusted_max_lr,
                    min_lr=min_lr
                )
            else:  # Default to constant learning rate with phase adjustment
                current_lr = learning_rate * (1.0 - 0.5 * phase)
            
            # Update square
            update = current_lr * m_hat / (np.sqrt(v_hat) + epsilon)
            self.square -= update
            
            # Track learning rate
            trajectories['learning_rate'].append(current_lr)
            
            # Soft integer projection with increasing strength
            if phase > 0 and (step - last_projection_step >= current_projection_freq):
                last_projection_step = step
                
                if verbose and step % 10 == 0:
                    print(f"Applying projection at step {step} with strength {projection_strength:.3f}")
                
                # Compute rounded version
                rounded = np.round(self.square)
                
                # Soft transition to integers with temperature
                # At high temperature (early), we stay closer to continuous
                # At low temperature (late), we get closer to integers
                self.square = (1 - projection_strength) * self.square + projection_strength * rounded
                
                # Apply monotonic constraint if enabled and in late phase
                if enforce_monotonic and phase > 0.7:
                    self.apply_monotonic_constraint(strength=projection_strength)
                
                # Preserve magic sum constraints
                if projection_strength > 0.5:  # Only in later stages
                    current_sum = np.sum(self.square)
                    target_sum = current_sum / self.size  # Expected row/column sum
                    
                    # Adjust rows to be closer to target sum
                    for i in range(self.size):
                        row_sum = np.sum(self.square[i, :])
                        if abs(row_sum - target_sum) > 0.1:
                            self.square[i, :] += (target_sum - row_sum) / self.size
                    
                    # Adjust columns to be closer to target sum
                    for j in range(self.size):
                        col_sum = np.sum(self.square[:, j])
                        if abs(col_sum - target_sum) > 0.1:
                            self.square[:, j] += (target_sum - col_sum) / self.size
                    
                    # Adjust diagonals if we're in late stages
                    if projection_strength > 0.8:
                        # Main diagonal adjustment
                        diag_sum = np.trace(self.square)
                        if abs(diag_sum - target_sum) > 0.1:
                            diag_indices = np.arange(self.size)
                            self.square[diag_indices, diag_indices] += (target_sum - diag_sum) / self.size
                        
                        # Anti-diagonal adjustment
                        anti_diag_sum = np.trace(np.fliplr(self.square))
                        if abs(anti_diag_sum - target_sum) > 0.1:
                            anti_diag_indices = np.arange(self.size)
                            self.square[anti_diag_indices, self.size - 1 - anti_diag_indices] += (target_sum - anti_diag_sum) / self.size
            
            # Recompute points and metrics
            self.points = self.create_axial_points()
            current_distance = self.compute_distance_to_manifold()
            current_sum_error = self.magic_sum_error()
            current_int_dev = np.sum(np.abs(self.square - np.round(self.square)))
            current_monotonic_error = 0.0 if not enforce_monotonic else self.compute_monotonic_error()
            
            # Track metrics
            trajectories['distance'].append(current_distance)
            trajectories['magic_sum_error'].append(current_sum_error)
            trajectories['integer_deviation'].append(current_int_dev)
            trajectories['monotonic_error'].append(current_monotonic_error)
            constraints = self.compute_covariance_constraints()
            trajectories['x_cov'].append(constraints[0])
            trajectories['y_cov'].append(constraints[1])
            trajectories['diag_main_cov'].append(constraints[2])
            trajectories['diag_anti_cov'].append(constraints[3])
            trajectories['phase'].append(phase)
            trajectories['temperature'].append(temperature)
            trajectories['projection_strength'].append(projection_strength)
            squares.append(self.square.copy())
            
            # Combined score - weighted combination of distance, integer properties, and monotonic constraint
            # Early phase: prioritize distance
            # Late phase: prioritize integer properties, sum error, and monotonic constraint
            distance_weight = max(0.1, 1.0 - phase)
            integer_weight = 1.0 - distance_weight
            
            # Include monotonic error in combined score if enabled
            if enforce_monotonic:
                combined_score = (
                    distance_weight * current_distance + 
                    integer_weight * (0.3 * current_int_dev + 0.3 * current_sum_error + 0.4 * current_monotonic_error)
                )
            else:
                combined_score = (
                    distance_weight * current_distance + 
                    integer_weight * (0.5 * current_int_dev + 0.5 * current_sum_error)
                )
            
            # Track best solution based on combined score
            if combined_score < best_combined_score:
                best_combined_score = combined_score
                best_distance = current_distance
                best_square = self.square.copy()
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            # Print progress
            if verbose and step % 10 == 0:
                monotonic_info = f", Monotonic Error={current_monotonic_error:.6f}" if enforce_monotonic else ""
                print(f"Step {step}: Phase={phase:.2f}, Temp={temperature:.2f}, "
                     f"Distance={current_distance:.6f}, Sum Error={current_sum_error:.6f}, "
                     f"Integer Dev={current_int_dev:.6f}{monotonic_info}, Score={combined_score:.6f}")
            
            # Apply random perturbation if stuck in local minimum
            if stagnation_count > 30 and phase < 0.5:
                if verbose:
                    print(f"Applying random perturbation at step {step}")
                # Small random perturbation to escape local minimum
                perturbation = np.random.normal(0, 0.1, size=self.square.shape)
                self.square += perturbation
                stagnation_count = 0
            
            # Early stopping if we've converged
            if current_distance < 1e-10 and current_int_dev < 0.1 and current_sum_error < 0.1:
                if not enforce_monotonic or current_monotonic_error < 0.1:
                    if verbose:
                        print(f"Convergence achieved at step {step}!")
                    break
        
        # Final integer projection if we're close
        if best_distance < 0.01 and not self.is_magic():
            if verbose:
                print("\nApplying final integer projection to best solution...")
            
            # Save current state
            current_square = self.square.copy()
            
            # Load best solution
            self.square = best_square.copy()
            
            # Integer projection
            rounded = np.round(self.square)
            
            # Apply monotonic constraint if enabled
            if enforce_monotonic:
                rounded = self.apply_monotonic_constraint(square=rounded, strength=1.0, return_result=True)
            
            # Compute the magic sum
            magic_sum = np.sum(self.square) / self.size
            
            # Attempt to create proper integer magic square
            self.square = rounded
            self.points = self.create_axial_points()
            
            # Check if it's magic
            is_magic_after_rounding = self.is_magic()
            
            if not is_magic_after_rounding:
                # Revert to previous state
                self.square = current_square
                self.points = self.create_axial_points()
                
                if verbose:
                    print("Final projection did not yield a magic square, reverting...")
        
        return trajectories, squares, initial_square
    
    def compute_monotonic_error(self, square=None):
        """Compute error between current square and monotonic values 1-16."""
        if square is None:
            square = self.square
            
        # Create target values 1-16
        target_values = np.arange(1, self.size*self.size + 1).reshape(self.size, self.size)
        
        # Compute error as sum of squared differences between sorted values and target
        flat_square = square.flatten()
        sorted_indices = np.argsort(flat_square)
        sorted_square = np.zeros_like(flat_square)
        sorted_square[sorted_indices] = np.arange(1, self.size*self.size + 1)
        sorted_square = sorted_square.reshape(self.size, self.size)
        
        return np.sum((sorted_square - target_values)**2) / (self.size*self.size)
    
    def compute_monotonic_gradient(self):
        """Compute gradient to push values toward monotonic 1-16 range."""
        flat_square = self.square.flatten()
        sorted_indices = np.argsort(flat_square)
        
        # Create target values 1-16
        target_values = np.arange(1, self.size*self.size + 1)
        
        # Initialize gradient
        gradient = np.zeros_like(flat_square)
        
        # For each value, compute gradient direction to move toward its target value
        for i, idx in enumerate(sorted_indices):
            gradient[idx] = 2 * (flat_square[idx] - target_values[i])
        
        return gradient.reshape(self.size, self.size)
    
    def apply_monotonic_constraint(self, square=None, strength=1.0, return_result=False):
        """Apply monotonic constraint to push values toward 1-16 range."""
        if square is None:
            square = self.square
        else:
            square = square.copy()
            
        # Get flat version and sorted indices
        flat_square = square.flatten()
        sorted_indices = np.argsort(flat_square)
        
        # Create target values 1-16
        target_values = np.arange(1, self.size*self.size + 1)
        
        # Create a new array with values pushed toward their targets
        new_flat = flat_square.copy()
        for i, idx in enumerate(sorted_indices):
            new_flat[idx] = (1 - strength) * flat_square[idx] + strength * target_values[i]
        
        new_square = new_flat.reshape(self.size, self.size)
        
        if return_result:
            return new_square
        else:
            self.square = new_square
            return None
    
    def plot_gradual_descent_results(self, trajectories, save_dir='covariance_proof'):
        """Plot detailed results of gradual hybrid descent."""
        # Create timestamp for unique filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Plot phase transitions and metrics
        plt.figure(figsize=(15, 12))
        
        # Plot phase parameter
        plt.subplot(3, 3, 1)
        plt.plot(trajectories['phase'], 'r-')
        plt.title('Phase Transition')
        plt.xlabel('Steps')
        plt.ylabel('Phase (0=Continuous, 1=Integer)')
        plt.grid(True)
        
        # Plot distance to manifold
        plt.subplot(3, 3, 2)
        plt.plot(trajectories['distance'])
        plt.title('Distance to Manifold')
        plt.xlabel('Steps')
        plt.ylabel('Distance')
        plt.yscale('log')
        plt.grid(True)
        
        # Plot magic sum error
        plt.subplot(3, 3, 3)
        plt.plot(trajectories['magic_sum_error'])
        plt.title('Magic Sum Error')
        plt.xlabel('Steps')
        plt.ylabel('Error')
        plt.yscale('log')
        plt.grid(True)
        
        # Plot integer deviation
        plt.subplot(3, 3, 4)
        plt.plot(trajectories['integer_deviation'])
        plt.title('Integer Deviation')
        plt.xlabel('Steps')
        plt.ylabel('Deviation')
        plt.yscale('log')
        plt.grid(True)
        
        # Plot temperature
        plt.subplot(3, 3, 5)
        plt.plot(trajectories['temperature'], 'g-')
        plt.title('Temperature')
        plt.xlabel('Steps')
        plt.ylabel('Temperature')
        plt.grid(True)
        
        # Plot projection strength
        plt.subplot(3, 3, 6)
        plt.plot(trajectories['projection_strength'], 'm-')
        plt.title('Projection Strength')
        plt.xlabel('Steps')
        plt.ylabel('Strength')
        plt.grid(True)
        
        # Plot learning rate trajectory
        plt.subplot(3, 3, 7)
        plt.plot(trajectories['learning_rate'], 'b-')
        plt.title('Learning Rate (One-Cycle Policy)')
        plt.xlabel('Steps')
        plt.ylabel('Learning Rate')
        plt.grid(True)
        
        # Plot monotonic error if available
        if 'monotonic_error' in trajectories and len(trajectories['monotonic_error']) > 0 and max(trajectories['monotonic_error']) > 0:
            plt.subplot(3, 3, 8)
            plt.plot(trajectories['monotonic_error'], 'c-')
            plt.title('Monotonic Error')
            plt.xlabel('Steps')
            plt.ylabel('Error')
            plt.yscale('log')
            plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{save_dir}/gradual_descent_{timestamp}.png')
        plt.close()
        
        # Plot covariance constraints
        plt.figure(figsize=(15, 6))
        
        plt.subplot(1, 2, 1)
        for label, key in [('Row', 'x_cov'), ('Col', 'y_cov'), 
                         ('Main Diag', 'diag_main_cov'), ('Anti Diag', 'diag_anti_cov')]:
            plt.plot(trajectories[key], label=label)
        plt.title('Covariance Constraints')
        plt.xlabel('Steps')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        
        # Plot final square heatmap
        plt.subplot(1, 2, 2)
        plt.imshow(self.square, cmap='viridis')
        plt.colorbar()
        plt.title('Final Square')
        
        plt.tight_layout()
        plt.savefig(f'{save_dir}/covariance_final_{timestamp}.png')
        plt.close()
        
        return f'{save_dir}/gradual_descent_{timestamp}.png', f'{save_dir}/covariance_final_{timestamp}.png'

def run_experiment(transition_start=100, transition_end=200, total_steps=300, 
                 learning_rate=0.1, swaps=2, enforce_monotonic=True, 
                 learning_rate_scheduler='one_cycle', verbose=True):
    """Run an experiment with given parameters."""
    # Initialize analyzer
    analyzer = EnhancedMagicSquareAnalyzer()
    
    # Start from a perturbed square
    perturbed = analyzer.perturb_square(swaps=swaps)
    analyzer.square = perturbed
    analyzer.points = analyzer.create_axial_points()
    
    print(f"\nRunning Enhanced Hybrid Approach with:")
    print(f"Transition: {transition_start}-{transition_end} of {total_steps} steps")
    print(f"Learning Rate: {learning_rate}, Initial Perturbation: {swaps} swaps")
    print(f"Learning Rate Scheduler: {learning_rate_scheduler}")
    print(f"Enforce Monotonic Values: {enforce_monotonic}")
    
    # Get initial metrics
    initial_distance = analyzer.compute_distance_to_manifold()
    initial_sum_error = analyzer.magic_sum_error()
    initial_int_dev = np.sum(np.abs(analyzer.square - np.round(analyzer.square)))
    initial_monotonic_error = 0.0 if not enforce_monotonic else analyzer.compute_monotonic_error()
    
    print(f"Initial Distance: {initial_distance:.8f}")
    print(f"Initial Sum Error: {initial_sum_error:.8f}")
    print(f"Initial Integer Deviation: {initial_int_dev:.8f}")
    if enforce_monotonic:
        print(f"Initial Monotonic Error: {initial_monotonic_error:.8f}")
    
    # Run gradual hybrid descent
    start_time = time.time()
    trajectories, squares, _ = analyzer.perform_gradual_hybrid_descent(
        total_steps=total_steps,
        learning_rate=learning_rate,
        transition_start=transition_start,
        transition_end=transition_end,
        enforce_monotonic=enforce_monotonic,
        learning_rate_scheduler=learning_rate_scheduler,
        verbose=verbose
    )
    end_time = time.time()
    
    # Get final metrics
    final_distance = trajectories['distance'][-1]
    final_sum_error = trajectories['magic_sum_error'][-1]
    final_int_dev = trajectories['integer_deviation'][-1]
    final_monotonic_error = 0.0 if not enforce_monotonic else trajectories['monotonic_error'][-1]
    is_magic = analyzer.is_magic()
    
    # Check if values are monotonic from 1-16
    is_monotonic = False
    if enforce_monotonic:
        rounded = np.round(analyzer.square)
        sorted_values = np.sort(rounded.flatten())
        expected_values = np.arange(1, analyzer.size*analyzer.size + 1)
        is_monotonic = np.allclose(sorted_values, expected_values)
    
    print(f"\nFinal Results:")
    print(f"Distance: {final_distance:.8f}")
    print(f"Sum Error: {final_sum_error:.8f}")
    print(f"Integer Deviation: {final_int_dev:.8f}")
    if enforce_monotonic:
        print(f"Monotonic Error: {final_monotonic_error:.8f}")
        print(f"Is Monotonic 1-16: {is_monotonic}")
    print(f"Is Magic Square: {is_magic}")
    print(f"Computation Time: {end_time - start_time:.2f} seconds")
    
    # Plot results
    plot_files = analyzer.plot_gradual_descent_results(trajectories)
    print(f"Plots saved to: {plot_files[0]} and {plot_files[1]}")
    
    return {
        'parameters': {
            'transition_start': transition_start,
            'transition_end': transition_end,
            'total_steps': total_steps,
            'learning_rate': learning_rate,
            'swaps': swaps,
            'enforce_monotonic': enforce_monotonic
        },
        'initial_metrics': {
            'distance': initial_distance,
            'sum_error': initial_sum_error,
            'int_dev': initial_int_dev,
            'monotonic_error': initial_monotonic_error if enforce_monotonic else 0.0
        },
        'final_metrics': {
            'distance': final_distance,
            'sum_error': final_sum_error,
            'int_dev': final_int_dev,
            'monotonic_error': final_monotonic_error if enforce_monotonic else 0.0,
            'is_magic': is_magic,
            'is_monotonic': is_monotonic if enforce_monotonic else False
        },
        'computation_time': end_time - start_time,
        'plot_files': plot_files,
        'final_square': analyzer.square.copy()
    }

if __name__ == "__main__":
    print("Enhanced Hybrid Approach for Magic Square Gradient Flow")
    print("======================================================")
    
    # Run a few experiments with different parameters
    results = []
    
    # Experiment 1: Early transition
    print("\nExperiment 1: Early Phase Transition")
    results.append(run_experiment(transition_start=50, transition_end=150, total_steps=250))
    
    # Experiment 2: Late transition
    print("\nExperiment 2: Late Phase Transition")
    results.append(run_experiment(transition_start=150, transition_end=200, total_steps=250))
    
    # Experiment 3: Gradual transition
    print("\nExperiment 3: Gradual Transition")
    results.append(run_experiment(transition_start=50, transition_end=200, total_steps=250))
    
    # Experiment 4: Higher learning rate
    print("\nExperiment 4: Higher Learning Rate")
    results.append(run_experiment(transition_start=100, transition_end=200, 
                               total_steps=250, learning_rate=0.2))
    
    # Experiment 5: More initial perturbation
    print("\nExperiment 5: More Initial Perturbation")
    results.append(run_experiment(transition_start=100, transition_end=200, 
                               total_steps=250, swaps=3))
    
    # Summarize results
    print("\nSummary of Experiments:")
    print("======================")
    print("| Exp | Trans Start | Trans End | Steps | LR | Swaps | Final Dist | Sum Error | Int Dev | Monotonic? | Magic? |")
    print("|-----|-------------|-----------|-------|----|----|-----------|-----------|---------|-----------|--------|")
    
    for i, result in enumerate(results):
        p = result['parameters']
        m = result['final_metrics']
        print(f"| {i+1} | {p['transition_start']:11} | {p['transition_end']:9} | {p['total_steps']:5} | {p['learning_rate']:.1f} | {p['swaps']:2} | {m['distance']:.8f} | {m['sum_error']:.8f} | {m['int_dev']:.6f} | {m['is_monotonic']} | {m['is_magic']} |")
    
    # Save magic squares if found
    magic_squares = [r for r in results if r['final_metrics']['is_magic']]
    if magic_squares:
        print(f"\nFound {len(magic_squares)} magic squares!")
        for i, result in enumerate(magic_squares):
            print(f"\nMagic Square {i+1}:")
            print(result['final_square'])
    else:
        print("\nNo exact magic squares found in these experiments.")
        
        # Find best near-magic square
        best_result = min(results, key=lambda r: r['final_metrics']['distance'] + r['final_metrics']['sum_error'] + r['final_metrics']['int_dev'])
        print("\nBest near-magic square (Experiment", results.index(best_result) + 1, "):")
        print(best_result['final_square'])
        print(f"Distance: {best_result['final_metrics']['distance']:.8f}")
        print(f"Sum Error: {best_result['final_metrics']['sum_error']:.8f}")
        print(f"Integer Deviation: {best_result['final_metrics']['int_dev']:.8f}")