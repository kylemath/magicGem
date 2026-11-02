#!/usr/bin/env python3
"""
Improved Basin Hopping Algorithm for Magic Square Optimization

This script implements an enhanced basin hopping algorithm based on our successful
approach, with better distinctness enforcement to prevent uniform matrices.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
import random
from datetime import datetime
import math

# Import the enhanced analyzer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_hybrid_approach import EnhancedMagicSquareAnalyzer

class ImprovedBasinHoppingOptimizer:
    """Improved basin hopping optimizer with effective distinctness constraints."""
    
    def __init__(self, size=4, results_dir='covariance_proof/improved_results'):
        """Initialize the optimizer."""
        self.size = size
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Create analyzer
        self.analyzer = EnhancedMagicSquareAnalyzer(size=size)
        
        # Optimization parameters
        self.max_iterations = 50  # Maximum basin hopping iterations
        self.local_steps = 300    # Steps in each local optimization
        self.temperature = 2.0    # Initial temperature for acceptance probability
        self.step_size = 2.0      # Size of random perturbations
        self.cooling_rate = 0.98  # Temperature cooling rate
        
        # Distinctness parameters - strengthened compared to previous version
        self.distinctness_weight = 5.0  # Much stronger weight for distinctness
        self.min_required_distinct = 0.8 * (size * size)  # At least 80% of values should be distinct
        
        # Trajectory tracking
        self.trajectory = {
            'energy': [],
            'distance': [],
            'sum_error': [],
            'int_dev': [],
            'distinctness': [],
            'acceptance': [],
            'step_size': [],
            'temperature': []
        }
        
        # Results tracking
        self.best_square = None
        self.best_energy = float('inf')
        self.best_distance = float('inf')
        self.best_sum_error = float('inf')
        self.best_int_dev = float('inf')
        self.best_distinctness = 0.0
        self.found_magic = False
        
        # Timing
        self.start_time = None
        self.elapsed_time = 0
        
        # Timestamp
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def initialize_square(self):
        """Initialize with a standard magic square and perturb it."""
        # Start with the standard magic square
        self.analyzer.square = self.analyzer.create_magic_square().astype(float)
        self.analyzer.points = self.analyzer.create_axial_points()
        
        # Apply a moderate perturbation (4 swaps was optimal in previous runs)
        perturbed = self.analyzer.perturb_square(swaps=4)
        self.analyzer.square = perturbed
        self.analyzer.points = self.analyzer.create_axial_points()
        
    def compute_distinctness(self, square=None):
        """
        Compute how distinct the elements in the square are.
        Returns distinctness value (0-1) with 1 being completely distinct.
        """
        if square is None:
            square = self.analyzer.square
            
        # Round to nearest integers for distinctness check
        rounded = np.round(square)
        
        # Count unique values and their frequencies
        values, counts = np.unique(rounded, return_counts=True)
        unique_count = len(values)
        max_unique = self.size * self.size
        
        # Basic distinctness ratio
        distinctness_ratio = unique_count / max_unique
        
        # Add a penalty for elements that appear multiple times
        duplicate_penalty = np.sum(counts[counts > 1] - 1) / max_unique
        
        # Combined distinctness score (0-1)
        distinctness = max(0, distinctness_ratio - 0.5 * duplicate_penalty)
        
        return distinctness
    
    def compute_energy(self, square=None):
        """Compute the energy (combined score) of a square."""
        if square is not None:
            # Save current state
            current_square = self.analyzer.square.copy()
            
            # Set new square
            self.analyzer.square = square.copy()
            self.analyzer.points = self.analyzer.create_axial_points()
            
            # Compute metrics
            distance = self.analyzer.compute_distance_to_manifold()
            sum_error = self.analyzer.magic_sum_error()
            int_dev = np.sum(np.abs(self.analyzer.square - np.round(self.analyzer.square)))
            distinctness = self.compute_distinctness()
            
            # Restore state
            self.analyzer.square = current_square
            self.analyzer.points = self.analyzer.create_axial_points()
        else:
            # Compute metrics for current square
            distance = self.analyzer.compute_distance_to_manifold()
            sum_error = self.analyzer.magic_sum_error()
            int_dev = np.sum(np.abs(self.analyzer.square - np.round(self.analyzer.square)))
            distinctness = self.compute_distinctness()
        
        # Strong distinctness penalty to prevent uniform matrices
        distinctness_penalty = self.distinctness_weight * (1.0 - distinctness)**2
        
        # Energy combines all metrics with weights
        energy = (1.5 * distance + 
                 sum_error + 
                 int_dev / 5 + 
                 distinctness_penalty)
        
        return energy, distance, sum_error, int_dev, distinctness
        
    def acceptance_probability(self, old_energy, new_energy):
        """Calculate probability of accepting a worse solution."""
        if new_energy < old_energy:
            return 1.0  # Always accept better solutions
        
        # Otherwise, accept with Boltzmann probability
        return math.exp((old_energy - new_energy) / self.temperature)
    
    def local_optimization(self, verbose=True):
        """Perform local optimization using enhanced hybrid approach."""
        # Configure for local optimization
        transition_start = 100  # Start transition later
        transition_end = 250    # End transition later
        
        if verbose:
            print(f"Starting local optimization...")
        
        # Run local optimization
        trajectories, squares, initial_square = self.analyzer.perform_gradual_hybrid_descent(
            total_steps=self.local_steps,
            learning_rate=0.08,  # Lower learning rate for stability
            transition_start=transition_start,
            transition_end=transition_end,
            verbose=False  # Less verbose for basin hopping
        )
        
        # Check if we found a magic square
        is_magic = self.analyzer.is_magic()
        
        # Return optimization results
        return {
            'final_square': self.analyzer.square.copy(),
            'is_magic': is_magic,
            'distance': trajectories['distance'][-1],
            'sum_error': trajectories['magic_sum_error'][-1],
            'int_dev': trajectories['integer_deviation'][-1],
            'trajectories': trajectories
        }
    
    def random_perturbation(self):
        """Apply a random perturbation to escape local minimum."""
        # Save current square
        original_square = self.analyzer.square.copy()
        
        # Strategy 1: Swap random elements with variable swaps
        swaps = max(1, int(self.step_size))
        perturbed = self.analyzer.perturb_square(swaps=swaps)
        
        # Strategy 2: Add targeted noise to increase diversity
        distinctness = self.compute_distinctness(perturbed)
        if distinctness < 0.7:  # If distinctness is too low
            # Create noise that increases value spread
            rounded = np.round(perturbed)
            unique_vals = np.unique(rounded)
            
            if len(unique_vals) < 5:  # Very low distinctness
                # Add significant noise to break uniformity
                noise = np.random.uniform(-5, 5, perturbed.shape)
                perturbed = perturbed + noise
                
                # Ensure we don't have negative values
                if np.min(perturbed) < 0:
                    perturbed = perturbed - np.min(perturbed) + 1
        
        # Apply perturbation
        self.analyzer.square = perturbed
        self.analyzer.points = self.analyzer.create_axial_points()
        
        return original_square
    
    def ensure_distinctness(self):
        """Explicitly ensure the square has sufficient distinct values."""
        square = self.analyzer.square.copy()
        rounded = np.round(square)
        
        # Count unique values
        unique_vals = np.unique(rounded)
        
        if len(unique_vals) < self.min_required_distinct:
            # Find duplicate values
            values, counts = np.unique(rounded, return_counts=True)
            duplicates = [(val, count) for val, count in zip(values, counts) if count > 1]
            
            # Sort duplicates by frequency (most frequent first)
            duplicates.sort(key=lambda x: x[1], reverse=True)
            
            # For each duplicate, replace some occurrences
            for val, count in duplicates:
                if len(unique_vals) >= self.min_required_distinct:
                    break
                    
                # Find positions of this value
                pos = np.argwhere(rounded == val)
                
                # Keep one occurrence, replace others
                to_replace = pos[1:min(count, 5)]  # Replace up to 4 duplicates at once
                
                for i, j in to_replace:
                    # Try to find an unused value
                    new_val = val
                    while new_val in unique_vals or new_val == val:
                        # Create a value somewhat close to the original
                        spread = np.max(square) - np.min(square)
                        offset = random.uniform(-spread/4, spread/4)
                        new_val = round(val + offset)
                    
                    # Replace the value
                    self.analyzer.square[i, j] = float(new_val)
                    unique_vals = np.append(unique_vals, new_val)
                    
                    if len(unique_vals) >= self.min_required_distinct:
                        break
            
            # Recompute points
            self.analyzer.points = self.analyzer.create_axial_points()
    
    def run_basin_hopping(self, verbose=True):
        """Run the basin hopping algorithm."""
        self.start_time = time.time()
        
        # Initialize square
        self.initialize_square()
        
        # Compute initial energy
        energy, distance, sum_error, int_dev, distinctness = self.compute_energy()
        
        if verbose:
            print(f"Initial state: Energy={energy:.6f}, Distance={distance:.6f}, "
                 f"Sum Error={sum_error:.6f}, Int Dev={int_dev:.6f}, "
                 f"Distinctness={distinctness:.6f}")
        
        # Track best solution
        self.best_square = self.analyzer.square.copy()
        self.best_energy = energy
        self.best_distance = distance
        self.best_sum_error = sum_error
        self.best_int_dev = int_dev
        self.best_distinctness = distinctness
        
        # Initialize trajectory
        self.trajectory['energy'].append(energy)
        self.trajectory['distance'].append(distance)
        self.trajectory['sum_error'].append(sum_error)
        self.trajectory['int_dev'].append(int_dev)
        self.trajectory['distinctness'].append(distinctness)
        self.trajectory['acceptance'].append(1.0)
        self.trajectory['step_size'].append(self.step_size)
        self.trajectory['temperature'].append(self.temperature)
        
        # Start basin hopping iterations
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"\nBasin hopping iteration {iteration+1}/{self.max_iterations}")
                print(f"Temperature: {self.temperature:.6f}, Step size: {self.step_size:.2f}")
            
            # Apply random perturbation
            original_square = self.random_perturbation()
            
            # Ensure sufficient distinctness before local optimization
            self.ensure_distinctness()
            
            # Run local optimization from perturbed state
            result = self.local_optimization(verbose=verbose)
            
            # Apply post-optimization distinctness enforcement
            self.analyzer.square = result['final_square'].copy()
            self.analyzer.points = self.analyzer.create_axial_points()
            self.ensure_distinctness()
            
            # Compute new energy
            new_energy, new_distance, new_sum_error, new_int_dev, new_distinctness = self.compute_energy()
            
            if verbose:
                print(f"After local optimization: Energy={new_energy:.6f}, Distance={new_distance:.6f}, "
                     f"Sum Error={new_sum_error:.6f}, Int Dev={new_int_dev:.6f}, "
                     f"Distinctness={new_distinctness:.6f}")
            
            # Check if we found a magic square
            if new_distance < 0.01 and new_sum_error < 0.01 and new_distinctness > 0.9:
                is_magic = self.analyzer.is_magic()
                
                if is_magic:
                    self.found_magic = True
                    self.best_square = self.analyzer.square.copy()
                    self.best_energy = new_energy
                    self.best_distance = new_distance
                    self.best_sum_error = new_sum_error
                    self.best_int_dev = new_int_dev
                    self.best_distinctness = new_distinctness
                    
                    if verbose:
                        print(f"Found a magic square! Saving result.")
                    
                    # Save the magic square
                    self.save_magic_square(self.analyzer.square, iteration)
            
            # Determine whether to accept the new solution
            p_accept = self.acceptance_probability(energy, new_energy)
            accept = random.random() < p_accept
            
            if verbose:
                print(f"Acceptance probability: {p_accept:.4f} -> {'Accepted' if accept else 'Rejected'}")
            
            if accept:
                # Accept new solution
                energy = new_energy
                distance = new_distance
                sum_error = new_sum_error
                int_dev = new_int_dev
                distinctness = new_distinctness
            else:
                # Reject new solution, revert to original
                self.analyzer.square = original_square
                self.analyzer.points = self.analyzer.create_axial_points()
            
            # Track best solution if better
            if new_energy < self.best_energy:
                self.best_square = self.analyzer.square.copy()
                self.best_energy = new_energy
                self.best_distance = new_distance
                self.best_sum_error = new_sum_error
                self.best_int_dev = new_int_dev
                self.best_distinctness = new_distinctness
                
                if verbose:
                    print(f"New best solution found! Energy: {self.best_energy:.6f}")
            
            # Update trajectory
            self.trajectory['energy'].append(energy)
            self.trajectory['distance'].append(distance)
            self.trajectory['sum_error'].append(sum_error)
            self.trajectory['int_dev'].append(int_dev)
            self.trajectory['distinctness'].append(distinctness)
            self.trajectory['acceptance'].append(p_accept)
            self.trajectory['step_size'].append(self.step_size)
            self.trajectory['temperature'].append(self.temperature)
            
            # Adjust parameters
            self.temperature *= self.cooling_rate  # Cool down
            
            # Adjust step size based on acceptance rate
            if iteration % 5 == 0 and iteration > 0:
                # Get recent acceptance rate
                recent_accepts = self.trajectory['acceptance'][-5:]
                accept_rate = sum(1 for p in recent_accepts if p > 0.5) / len(recent_accepts)
                
                # Adjust step size
                if accept_rate > 0.7:
                    self.step_size *= 1.2  # Increase step size
                elif accept_rate < 0.3:
                    self.step_size *= 0.8  # Decrease step size
                
                # Ensure step size is within reasonable bounds
                self.step_size = max(1.0, min(10.0, self.step_size))
                
                if verbose:
                    print(f"Adjusted step size to {self.step_size:.2f} based on acceptance rate {accept_rate:.2f}")
        
        # Record elapsed time
        self.elapsed_time = time.time() - self.start_time
        
        # Plot optimization trajectory
        self.plot_trajectory()
        
        return self.found_magic, self.best_square, self.best_energy
    
    def save_magic_square(self, square, iteration):
        """Save a discovered magic square to file."""
        # Create a filename with timestamp and iteration
        filename = f"{self.results_dir}/magic_square_bh_{iteration}_{self.timestamp}.txt"
        
        # Calculate magic properties
        n = self.size
        target_sum = np.sum(square) / n
        row_sums = np.sum(square, axis=1)
        col_sums = np.sum(square, axis=0)
        main_diag_sum = np.trace(square)
        anti_diag_sum = np.trace(np.fliplr(square))
        is_distinct = len(np.unique(np.round(square))) == n*n
        
        # Write to file
        with open(filename, 'w') as f:
            f.write(f"Magic Square discovered by Improved Basin Hopping (Iteration {iteration}):\n\n")
            f.write(str(square) + "\n\n")
            f.write(f"Magic Sum: {target_sum}\n")
            f.write(f"Row Sums: {row_sums}\n")
            f.write(f"Column Sums: {col_sums}\n")
            f.write(f"Main Diagonal Sum: {main_diag_sum}\n")
            f.write(f"Anti-Diagonal Sum: {anti_diag_sum}\n")
            f.write(f"Contains Distinct Values: {is_distinct}\n")
            f.write(f"Minimum Value: {np.min(square)}\n")
            f.write(f"Maximum Value: {np.max(square)}\n")
        
        print(f"Magic square saved to {filename}")
    
    def plot_trajectory(self):
        """Plot the optimization trajectory."""
        plt.figure(figsize=(15, 12))
        
        # Energy trajectory
        plt.subplot(3, 3, 1)
        plt.plot(self.trajectory['energy'])
        plt.title('Energy Trajectory')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Energy')
        plt.yscale('log')
        plt.grid(True)
        
        # Distance trajectory
        plt.subplot(3, 3, 2)
        plt.plot(self.trajectory['distance'])
        plt.title('Distance to Manifold')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Distance')
        plt.yscale('log')
        plt.grid(True)
        
        # Sum error trajectory
        plt.subplot(3, 3, 3)
        plt.plot(self.trajectory['sum_error'])
        plt.title('Magic Sum Error')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Error')
        plt.yscale('log')
        plt.grid(True)
        
        # Integer deviation trajectory
        plt.subplot(3, 3, 4)
        plt.plot(self.trajectory['int_dev'])
        plt.title('Integer Deviation')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Deviation')
        plt.grid(True)
        
        # Distinctness trajectory
        plt.subplot(3, 3, 5)
        plt.plot(self.trajectory['distinctness'])
        plt.title('Distinctness')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Distinctness')
        plt.ylim(0, 1.1)
        plt.grid(True)
        
        # Acceptance probability
        plt.subplot(3, 3, 6)
        plt.plot(self.trajectory['acceptance'])
        plt.title('Acceptance Probability')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Probability')
        plt.ylim(0, 1.1)
        plt.grid(True)
        
        # Temperature
        plt.subplot(3, 3, 7)
        plt.plot(self.trajectory['temperature'])
        plt.title('Temperature')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Temperature')
        plt.grid(True)
        
        # Step size
        plt.subplot(3, 3, 8)
        plt.plot(self.trajectory['step_size'])
        plt.title('Step Size')
        plt.xlabel('Basin Hopping Iteration')
        plt.ylabel('Step Size')
        plt.grid(True)
        
        # Best square visualization
        plt.subplot(3, 3, 9)
        if self.best_square is not None:
            # Create a table with the square values
            cell_text = [[f"{val:.1f}" for val in row] for row in self.best_square]
            
            # Color cells based on how close they are to integers
            int_dev = np.abs(self.best_square - np.round(self.best_square))
            cell_colors = plt.cm.RdYlGn_r(int_dev / max(0.5, np.max(int_dev)))
            
            plt.table(cellText=cell_text, cellColours=cell_colors, loc='center',
                     bbox=[0, 0, 1, 1])
        
        plt.title('Best Square')
        plt.axis('off')
        
        # Add title with results
        result_text = f"Improved Basin Hopping Results - {'Magic Square Found' if self.found_magic else 'No Magic Square Found'}"
        plt.figtext(0.5, 0.95, result_text, ha='center', fontsize=16, 
                   color='green' if self.found_magic else 'red')
        
        details_text = f"Best Energy: {self.best_energy:.6f} | Distance: {self.best_distance:.6f} | "
        details_text += f"Sum Error: {self.best_sum_error:.6f} | Int Dev: {self.best_int_dev:.6f} | "
        details_text += f"Distinctness: {self.best_distinctness:.6f}"
        plt.figtext(0.5, 0.92, details_text, ha='center', fontsize=12)
        
        time_text = f"Elapsed Time: {self.elapsed_time:.2f} seconds"
        plt.figtext(0.5, 0.89, time_text, ha='center', fontsize=10)
        
        plt.tight_layout(rect=[0, 0, 1, 0.88])
        
        # Save plot
        plot_file = f"{self.results_dir}/improved_basin_hopping_trajectory_{self.timestamp}.png"
        plt.savefig(plot_file)
        plt.close()
        
        print(f"Trajectory plot saved to {plot_file}")

def run_improved_basin_hopping():
    """Run the improved basin hopping optimization."""
    print("Improved Basin Hopping Magic Square Optimization")
    print("===============================================")
    
    # Create optimizer
    optimizer = ImprovedBasinHoppingOptimizer()
    
    # Run optimization
    found_magic, best_square, best_energy = optimizer.run_basin_hopping(verbose=True)
    
    # Print results
    print("\nImproved Basin Hopping Results:")
    print(f"Found Magic Square: {found_magic}")
    print(f"Best Energy: {best_energy:.6f}")
    print(f"Best Square:")
    print(best_square)
    
    # Check if the best square is magic
    analyzer = EnhancedMagicSquareAnalyzer()
    analyzer.square = best_square
    analyzer.points = analyzer.create_axial_points()
    is_magic = analyzer.is_magic()
    
    print(f"Is Magic (by definition): {is_magic}")
    
    if not found_magic and not is_magic:
        print("\nBest near-magic square properties:")
        distance = analyzer.compute_distance_to_manifold()
        sum_error = analyzer.magic_sum_error()
        int_dev = np.sum(np.abs(analyzer.square - np.round(analyzer.square)))
        
        # Check distinctness
        rounded = np.round(analyzer.square)
        unique_count = len(np.unique(rounded))
        distinctness = unique_count / (analyzer.size * analyzer.size)
        
        print(f"Distance to Manifold: {distance:.8f}")
        print(f"Magic Sum Error: {sum_error:.8f}")
        print(f"Integer Deviation: {int_dev:.8f}")
        print(f"Distinctness: {distinctness:.8f} ({unique_count}/{analyzer.size*analyzer.size} unique values)")
    
    return found_magic, best_square

if __name__ == "__main__":
    # Run improved basin hopping
    found_magic, best_square = run_improved_basin_hopping() 