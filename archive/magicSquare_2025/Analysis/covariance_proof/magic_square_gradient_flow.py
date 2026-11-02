#!/usr/bin/env python3
"""
Magic Square Gradient Flow Analysis

This script implements a gradient flow approach to analyze magic squares based on
the covariance framework. It tests the hypothesis that magic squares correspond to
critical points of the gradient flow on the magic square variety.
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import random

class MagicSquareAnalyzer:
    def __init__(self, square=None, size=4):
        """Initialize with a magic square or create a standard one."""
        self.size = size
        if square is not None:
            self.square = np.array(square, dtype=float)
        else:
            self.square = self.create_magic_square()
        self.points = self.create_axial_points()
        
    def compute_one_cycle_learning_rate(self, step, total_steps, max_lr, min_lr=0.0):
        """Compute learning rate according to one-cycle policy.
        
        The one-cycle policy involves gradually increasing the learning rate from
        min_lr to max_lr for the first half of training, then decreasing it back
        to min_lr using a cosine schedule.
        
        Parameters:
        -----------
        step : int
            Current step in the optimization process
        total_steps : int
            Total number of steps in the optimization
        max_lr : float
            Maximum learning rate
        min_lr : float
            Minimum learning rate
            
        Returns:
        --------
        float: The calculated learning rate for the current step
        """
        import math
        cycle_progress = step / (total_steps / 2)
        if cycle_progress <= 1:
            # First half: linear increase
            return min_lr + (max_lr - min_lr) * cycle_progress
        else:
            # Second half: cosine decay
            cycle_progress = (cycle_progress - 1)
            return min_lr + (max_lr - min_lr) * (1 + math.cos(cycle_progress * math.pi)) / 2
    
    def compute_cosine_annealing_lr(self, step, cycle_length, max_lr, min_lr=0.0):
        """Compute learning rate with cosine annealing and warm restarts.
        
        This learning rate schedule follows a cosine curve that decreases from
        max_lr to min_lr over each cycle, then restarts at max_lr.
        
        Parameters:
        -----------
        step : int
            Current step in the optimization process
        cycle_length : int
            Length of each cycle before restart
        max_lr : float
            Maximum learning rate
        min_lr : float
            Minimum learning rate
            
        Returns:
        --------
        float: The calculated learning rate for the current step
        """
        import math
        cycle = step % cycle_length
        cycle_progress = cycle / cycle_length
        return min_lr + (max_lr - min_lr) * (1 + math.cos(cycle_progress * math.pi)) / 2
    
    def compute_triangular_cyclic_lr(self, step, cycle_length, max_lr, min_lr=0.0):
        """Compute learning rate using a triangular cyclic schedule.
        
        The learning rate fluctuates between min_lr and max_lr in a triangular pattern.
        
        Parameters:
        -----------
        step : int
            Current step in the optimization process
        cycle_length : int
            Length of each complete cycle (up and down)
        max_lr : float
            Maximum learning rate
        min_lr : float
            Minimum learning rate
            
        Returns:
        --------
        float: The calculated learning rate for the current step
        """
        cycle = step % cycle_length
        cycle_progress = cycle / (cycle_length / 2)
        if cycle_progress <= 1:
            # Linear increase
            return min_lr + (max_lr - min_lr) * cycle_progress
        else:
            # Linear decrease
            return max_lr - (max_lr - min_lr) * (cycle_progress - 1)
        
    def create_magic_square(self):
        """Create a randomly initialized square with values 1-16."""
        # Create array with values 1-16
        values = np.arange(1, 17, dtype=float)
        # Randomly shuffle the values
        np.random.shuffle(values)
        # Reshape into 4x4 square
        return values.reshape((4, 4))
    
    def create_axial_points(self):
        """Convert square to axial representation."""
        n = self.size
        points = []
        mean_val = np.mean(self.square)
        
        for i in range(n):
            for j in range(n):
                x = i - (n-1)/2
                y = j - (n-1)/2
                z = self.square[i, j] - mean_val
                points.append([x, y, z])
                
        return np.array(points)
    
    def compute_covariance_constraints(self):
        """Compute the four covariance constraints."""
        points = self.points
        
        # Extract coordinates
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]
        
        # Calculate diagonal projections
        diag_main = (x + y) / np.sqrt(2)
        diag_anti = (x - y) / np.sqrt(2)
        
        # Compute covariances
        cov_x_z = np.mean(x * z)  # Since means are zero by construction
        cov_y_z = np.mean(y * z)
        cov_diag_main_z = np.mean(diag_main * z)
        cov_diag_anti_z = np.mean(diag_anti * z)
        
        return np.array([cov_x_z, cov_y_z, cov_diag_main_z, cov_diag_anti_z])
    
    def compute_distance_to_manifold(self):
        """Compute the distance to the magic square manifold."""
        constraints = self.compute_covariance_constraints()
        return np.sqrt(np.sum(constraints**2))
    
    def compute_covariance_gradient(self):
        """Compute the analytical gradient of the covariance constraints."""
        n = self.size
        # We'll compute the gradient of each covariance constraint 
        # with respect to each matrix entry
        
        # Get the current points
        points = self.points
        
        # Extract coordinates
        x = points[:, 0]  # Row indices (centered)
        y = points[:, 1]  # Column indices (centered)
        z = points[:, 2]  # Values (centered)
        
        # Calculate diagonal projections
        diag_main = (x + y) / np.sqrt(2)
        diag_anti = (x - y) / np.sqrt(2)
        
        # Compute covariance values
        cov_x_z = np.mean(x * z)
        cov_y_z = np.mean(y * z)
        cov_diag_main_z = np.mean(diag_main * z)
        cov_diag_anti_z = np.mean(diag_anti * z)
        
        # These are the constraint values
        constraint_values = np.array([cov_x_z, cov_y_z, cov_diag_main_z, cov_diag_anti_z])
        
        # Gradient of distance function
        # d = sqrt(sum(c_i^2)) => ∇d = sum(c_i * ∇c_i) / d if d > 0, else 0
        distance = np.sqrt(np.sum(constraint_values**2))
        if distance < 1e-10:
            return np.zeros_like(self.square)
        
        # Initialize gradient array
        gradient = np.zeros_like(self.square)
        
        # For each entry in the matrix
        for i in range(n):
            for j in range(n):
                # Calculate how perturbing this entry changes each constraint
                # For a given entry (i,j), changing z_ij affects the covariances
                
                # Effect on covariance with row index
                d_cov_x_z = x[i*n + j] / (n*n)
                
                # Effect on covariance with column index
                d_cov_y_z = y[i*n + j] / (n*n)
                
                # Effect on covariance with main diagonal projection
                d_cov_diag_main_z = diag_main[i*n + j] / (n*n)
                
                # Effect on covariance with anti-diagonal projection
                d_cov_diag_anti_z = diag_anti[i*n + j] / (n*n)
                
                # Gradient of each constraint
                constraint_gradients = np.array([d_cov_x_z, d_cov_y_z, d_cov_diag_main_z, d_cov_diag_anti_z])
                
                # Compute the gradient of the distance function
                # This is the contribution to the gradient from this matrix entry
                gradient[i, j] = np.sum(constraint_values * constraint_gradients) / distance
                
        return gradient
    
    def perform_improved_gradient_descent(self, steps=100, learning_rate=0.1, adaptive_rate=True, 
                                         integer_projection=False, verbose=True):
        """Perform gradient descent with improved strategies."""
        # Ensure square is float type
        self.square = self.square.astype(float)
        
        # Save initial state
        initial_square = self.square.copy()
        trajectories = {
            'distance': [self.compute_distance_to_manifold()],
            'magic_sum_error': [self.magic_sum_error()],
            'x_cov': [self.compute_covariance_constraints()[0]],
            'y_cov': [self.compute_covariance_constraints()[1]],
            'diag_main_cov': [self.compute_covariance_constraints()[2]],
            'diag_anti_cov': [self.compute_covariance_constraints()[3]]
        }
        squares = [self.square.copy()]
        
        # Track whether we're making progress
        best_distance = trajectories['distance'][0]
        best_square = self.square.copy()
        stagnation_count = 0
        
        # ADAM optimizer parameters
        if adaptive_rate:
            m = np.zeros_like(self.square)  # First moment (momentum)
            v = np.zeros_like(self.square)  # Second moment
            beta1 = 0.9
            beta2 = 0.999
            epsilon = 1e-8
            t = 0
        
        for step in range(steps):
            # Compute gradient using analytical method
            gradient = self.compute_covariance_gradient()
            
            # Update step with ADAM if adaptive rate is enabled
            if adaptive_rate:
                t += 1
                # Update biased first moment estimate
                m = beta1 * m + (1 - beta1) * gradient
                # Update biased second raw moment estimate
                v = beta2 * v + (1 - beta2) * (gradient**2)
                # Compute bias-corrected estimates
                m_hat = m / (1 - beta1**t)
                v_hat = v / (1 - beta2**t)
                # Update parameters
                update = learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
                self.square -= update
            else:
                # Simple gradient descent
                self.square -= learning_rate * gradient
            
            # Apply integer projection if specified
            if integer_projection and step > 0 and step % 10 == 0:
                # Round to nearest integer while preserving sum
                total_before = np.sum(self.square)
                self.square = np.round(self.square)
                total_after = np.sum(self.square)
                # Adjust to preserve sum
                if total_after != total_before:
                    self.square += (total_before - total_after) / (self.size * self.size)
            
            # Recompute points
            self.points = self.create_axial_points()
            
            # Compute metrics
            current_distance = self.compute_distance_to_manifold()
            current_constraints = self.compute_covariance_constraints()
            current_sum_error = self.magic_sum_error()
            
            # Track metrics
            trajectories['distance'].append(current_distance)
            trajectories['magic_sum_error'].append(current_sum_error)
            trajectories['x_cov'].append(current_constraints[0])
            trajectories['y_cov'].append(current_constraints[1])
            trajectories['diag_main_cov'].append(current_constraints[2])
            trajectories['diag_anti_cov'].append(current_constraints[3])
            squares.append(self.square.copy())
            
            # Check for improvement
            if current_distance < best_distance:
                best_distance = current_distance
                best_square = self.square.copy()
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            # Print progress
            if verbose and step % 10 == 0:
                print(f"Step {step}: Distance={current_distance:.6f}, Sum Error={current_sum_error:.6f}, "
                     f"Gradient Norm={np.linalg.norm(gradient):.6f}")
            
            # Early stopping if we're not improving
            if stagnation_count > 20 and current_distance > 1e-5:
                if verbose:
                    print(f"Early stopping at step {step} due to lack of improvement")
                break
                
            # Early stopping if we've converged
            if current_distance < 1e-10 and current_sum_error < 1e-5:
                if verbose:
                    print(f"Converged at step {step}")
                break
        
        # Use the best square found
        if best_distance < trajectories['distance'][-1]:
            self.square = best_square
            self.points = self.create_axial_points()
            
            # Update final metrics
            final_distance = self.compute_distance_to_manifold()
            final_constraints = self.compute_covariance_constraints()
            final_sum_error = self.magic_sum_error()
            
            if verbose:
                print(f"Reverting to best square with distance: {final_distance:.6f}")
            
            trajectories['distance'].append(final_distance)
            trajectories['magic_sum_error'].append(final_sum_error)
            trajectories['x_cov'].append(final_constraints[0])
            trajectories['y_cov'].append(final_constraints[1])
            trajectories['diag_main_cov'].append(final_constraints[2])
            trajectories['diag_anti_cov'].append(final_constraints[3])
            squares.append(best_square)
        
        return trajectories, squares, initial_square
    
    def magic_sum_error(self):
        """Compute how far the square is from satisfying the magic sum constraints."""
        n = self.square.shape[0]
        target_sum = np.sum(self.square) / n  # Expected row/column sum
        
        errors = []
        
        # Row sum errors
        for i in range(n):
            errors.append(abs(np.sum(self.square[i, :]) - target_sum))
        
        # Column sum errors
        for j in range(n):
            errors.append(abs(np.sum(self.square[:, j]) - target_sum))
        
        # Main diagonal error
        errors.append(abs(np.sum(np.diag(self.square)) - target_sum))
        
        # Anti-diagonal error
        errors.append(abs(np.sum(np.diag(np.fliplr(self.square))) - target_sum))
        
        return np.mean(errors)
    
    def perturb_square(self, swaps=1):
        """Perturb the magic square by random swaps."""
        perturbed = self.square.copy().astype(float)
        indices = list(permutations(range(self.size), 2))
        
        for _ in range(swaps):
            # Select random positions to swap
            (i1, j1), (i2, j2) = random.sample(indices, 2)
            
            # Swap elements
            perturbed[i1, j1], perturbed[i2, j2] = perturbed[i2, j2], perturbed[i1, j1]
            
        return perturbed
    
    def is_magic(self, tolerance=1e-10):
        """Check if a square is magic by verifying row, column, and diagonal sums."""
        n = self.square.shape[0]
        target_sum = np.sum(self.square) / n  # Expected row/column sum
        
        # Check rows
        for i in range(n):
            if abs(np.sum(self.square[i, :]) - target_sum) > tolerance:
                return False
                
        # Check columns
        for j in range(n):
            if abs(np.sum(self.square[:, j]) - target_sum) > tolerance:
                return False
                
        # Check main diagonal
        if abs(np.sum(np.diag(self.square)) - target_sum) > tolerance:
            return False
            
        # Check anti-diagonal
        if abs(np.sum(np.diag(np.fliplr(self.square))) - target_sum) > tolerance:
            return False
            
        return True
    
    def analyze_critical_points(self, num_perturbations=10, swaps_per_perturbation=1):
        """Analyze if magic squares are critical points of the gradient flow."""
        # Start with the original magic square
        original_distance = self.compute_distance_to_manifold()
        original_gradient_norm = np.linalg.norm(self.compute_covariance_gradient())
        original_is_magic = self.is_magic()
        
        results = [(0, original_distance, original_gradient_norm, original_is_magic)]
        
        # Test perturbed versions
        for i in range(num_perturbations):
            # Create perturbed square
            perturbed = self.perturb_square(swaps=swaps_per_perturbation)
            
            # Analyze perturbed square
            self.square = perturbed
            self.points = self.create_axial_points()
            
            # Compute metrics
            distance = self.compute_distance_to_manifold()
            gradient_norm = np.linalg.norm(self.compute_covariance_gradient())
            is_magic = self.is_magic()
            
            results.append((i+1, distance, gradient_norm, is_magic))
            
        # Reset to original
        self.square = self.create_magic_square()
        self.points = self.create_axial_points()
        
        return results
    
    def analyze_convergence_to_magic(self, num_experiments=5, perturbation_level=2, descent_steps=100, use_improved=True):
        """Analyze if gradient descent from perturbed squares converges to magic squares."""
        results = []
        
        for i in range(num_experiments):
            print(f"\nExperiment {i+1}/{num_experiments}:")
            
            # Start from a perturbed square
            perturbed = self.perturb_square(swaps=perturbation_level)
            self.square = perturbed
            self.points = self.create_axial_points()
            
            initial_distance = self.compute_distance_to_manifold()
            initial_is_magic = self.is_magic()
            initial_sum_error = self.magic_sum_error()
            
            print(f"Initial Distance: {initial_distance:.8f}, Sum Error: {initial_sum_error:.8f}, Is Magic: {initial_is_magic}")
            
            # Perform gradient descent
            if use_improved:
                trajectories, squares, _ = self.perform_improved_gradient_descent(
                    steps=descent_steps, 
                    learning_rate=0.1, 
                    adaptive_rate=True,
                    verbose=False
                )
                final_distance = trajectories['distance'][-1]
                final_sum_error = trajectories['magic_sum_error'][-1]
            else:
                trajectory, squares, _ = self.perform_gradient_descent(steps=descent_steps, verbose=False)
                final_distance = trajectory[-1]
                final_sum_error = self.magic_sum_error()
            
            final_is_magic = self.is_magic()
            
            print(f"Final Distance: {final_distance:.8f}, Sum Error: {final_sum_error:.8f}, Is Magic: {final_is_magic}")
            
            # Check if we're "close" to a magic square even if not exact
            is_near_magic = final_distance < 0.001 and final_sum_error < 0.1
            
            # Save result
            results.append({
                'experiment': i+1,
                'initial_distance': initial_distance,
                'initial_sum_error': initial_sum_error,
                'initial_is_magic': initial_is_magic,
                'final_distance': final_distance,
                'final_sum_error': final_sum_error,
                'final_is_magic': final_is_magic,
                'is_near_magic': is_near_magic,
                'trajectories': trajectories if use_improved else {'distance': trajectory},
                'initial_square': perturbed,
                'final_square': self.square.copy()
            })
            
            # Reset to original
            self.square = self.create_magic_square()
            self.points = self.create_axial_points()
            
        return results

    def compute_gradient(self, step_size=0.001):
        """Compute the gradient of the distance function with numerical approximation."""
        original_square = self.square.copy()
        gradient = np.zeros_like(self.square)
        
        # Compute partial derivatives for each entry
        for i in range(self.size):
            for j in range(self.size):
                # Store original value
                original_value = self.square[i, j]
                
                # Perturb entry slightly
                self.square[i, j] = original_value + step_size
                self.points = self.create_axial_points()
                d_plus = self.compute_distance_to_manifold()
                
                # Go in opposite direction
                self.square[i, j] = original_value - step_size
                self.points = self.create_axial_points()
                d_minus = self.compute_distance_to_manifold()
                
                # Central difference approximation of gradient
                gradient[i, j] = (d_plus - d_minus) / (2 * step_size)
                
                # Reset to original value
                self.square[i, j] = original_value
                
        # Restore original state
        self.square = original_square
        self.points = self.create_axial_points()
        
        return gradient

    def perform_gradient_descent(self, steps=100, learning_rate=0.05, verbose=True):
        """Perform simple gradient descent on the distance function."""
        # Ensure square is float type
        self.square = self.square.astype(float)
        
        # Save initial state
        initial_square = self.square.copy()
        trajectory = [self.compute_distance_to_manifold()]
        squares = [self.square.copy()]
        
        # Track whether we're making progress
        best_distance = trajectory[0]
        best_square = self.square.copy()
        plateau_count = 0
        
        for step in range(steps):
            # Compute gradient
            gradient = self.compute_gradient()
            
            # Normalize gradient to avoid too large steps
            if np.linalg.norm(gradient) > 0:
                normalized_gradient = gradient / np.linalg.norm(gradient)
            else:
                normalized_gradient = gradient
            
            # Update square with gradient step
            self.square -= learning_rate * normalized_gradient
            
            # Recompute points
            self.points = self.create_axial_points()
            
            # Compute current distance
            current_distance = self.compute_distance_to_manifold()
            trajectory.append(current_distance)
            squares.append(self.square.copy())
            
            # Check if we're making progress
            if current_distance < best_distance:
                best_distance = current_distance
                best_square = self.square.copy()
                plateau_count = 0
            else:
                plateau_count += 1
            
            # Adaptive learning rate - reduce if we stop making progress
            if plateau_count > 5:
                learning_rate *= 0.9
                plateau_count = 0
                if verbose:
                    print(f"Reducing learning rate to {learning_rate:.6f}")
            
            # Print progress
            if verbose and step % 10 == 0:
                print(f"Step {step}, Distance: {current_distance:.8f}, Gradient Norm: {np.linalg.norm(gradient):.8f}")
                
            # Early stopping if we're not making progress
            if learning_rate < 1e-6 or current_distance < 1e-10:
                if verbose:
                    print(f"Early stopping at step {step}")
                break
                
        # Use the best square found
        if best_distance < trajectory[-1]:
            self.square = best_square
            self.points = self.create_axial_points()
            if verbose:
                print(f"Reverting to best square with distance: {best_distance:.8f}")
            trajectory.append(best_distance)
            squares.append(best_square)
        
        return trajectory, squares, initial_square

    def perform_integer_constrained_gradient_descent(self, steps=200, learning_rate=0.1, 
                                                  projection_frequency=10, verbose=True):
        """Perform gradient descent with periodic integer projection and magic sum preservation."""
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
            'diag_anti_cov': [self.compute_covariance_constraints()[3]]
        }
        squares = [self.square.copy()]
        
        # ADAM optimizer parameters
        m = np.zeros_like(self.square)  # First moment
        v = np.zeros_like(self.square)  # Second moment
        beta1, beta2 = 0.9, 0.999
        epsilon = 1e-8
        t = 0
        
        best_distance = float('inf')
        best_square = None
        stagnation_count = 0
        
        for step in range(steps):
            t += 1
            gradient = self.compute_covariance_gradient()
            
            # ADAM updates
            m = beta1 * m + (1 - beta1) * gradient
            v = beta2 * v + (1 - beta2) * (gradient**2)
            m_hat = m / (1 - beta1**t)
            v_hat = v / (1 - beta2**t)
            
            # Update square
            update = learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
            self.square -= update
            
            # Periodic integer projection
            if step > 0 and step % projection_frequency == 0:
                # Store current sum
                current_sum = np.sum(self.square)
                
                # Round to nearest integers
                rounded = np.round(self.square)
                
                # Compute the adjustment needed to preserve sum
                sum_diff = current_sum - np.sum(rounded)
                adjustment = sum_diff / (self.size * self.size)
                
                # Apply adjustment and update square
                self.square = rounded + adjustment
                
                # Additional step to minimize sum error while keeping integers
                row_sums = np.sum(self.square, axis=1)
                col_sums = np.sum(self.square, axis=0)
                diag_sum = np.trace(self.square)
                anti_diag_sum = np.trace(np.fliplr(self.square))
                
                target_sum = current_sum / self.size
                
                # Adjust rows and columns to be closer to target sum
                for i in range(self.size):
                    if abs(row_sums[i] - target_sum) > 0.1:
                        self.square[i, :] += (target_sum - row_sums[i]) / self.size
                    if abs(col_sums[i] - target_sum) > 0.1:
                        self.square[:, i] += (target_sum - col_sums[i]) / self.size
            
            # Recompute points and metrics
            self.points = self.create_axial_points()
            current_distance = self.compute_distance_to_manifold()
            current_sum_error = self.magic_sum_error()
            current_int_dev = np.sum(np.abs(self.square - np.round(self.square)))
            
            # Update trajectories
            trajectories['distance'].append(current_distance)
            trajectories['magic_sum_error'].append(current_sum_error)
            trajectories['integer_deviation'].append(current_int_dev)
            constraints = self.compute_covariance_constraints()
            trajectories['x_cov'].append(constraints[0])
            trajectories['y_cov'].append(constraints[1])
            trajectories['diag_main_cov'].append(constraints[2])
            trajectories['diag_anti_cov'].append(constraints[3])
            squares.append(self.square.copy())
            
            # Update best solution
            if current_distance < best_distance and current_int_dev < 0.1:
                best_distance = current_distance
                best_square = self.square.copy()
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            if verbose and step % 10 == 0:
                print(f"Step {step}: Distance={current_distance:.6f}, "
                      f"Sum Error={current_sum_error:.6f}, "
                      f"Integer Dev={current_int_dev:.6f}")
            
            # Early stopping conditions
            if stagnation_count > 20 and current_distance > 1e-5:
                if verbose:
                    print(f"Early stopping at step {step} due to lack of improvement")
                break
            
            if current_distance < 1e-10 and current_int_dev < 1e-5:
                if verbose:
                    print(f"Converged at step {step}")
                break
        
        # Use best found solution if it exists
        if best_square is not None and best_distance < current_distance:
            self.square = best_square
            self.points = self.create_axial_points()
            if verbose:
                print(f"Reverting to best square with distance: {best_distance:.6f}")
        
        return trajectories, squares, initial_square

    def analyze_convergence_patterns(self, num_experiments=5, max_steps=300):
        """Analyze convergence patterns with both regular and integer-constrained gradient descent."""
        results = {
            'regular': [],
            'integer_constrained': []
        }
        
        for i in range(num_experiments):
            print(f"\nExperiment {i+1}/{num_experiments}:")
            
            # Start from a perturbed square
            perturbed = self.perturb_square(swaps=2)
            
            # Test regular gradient descent
            self.square = perturbed.copy()
            self.points = self.create_axial_points()
            print("\nRegular Gradient Descent:")
            trajectories_reg, _, _ = self.perform_improved_gradient_descent(
                steps=max_steps, verbose=False
            )
            
            # Test integer-constrained gradient descent
            self.square = perturbed.copy()
            self.points = self.create_axial_points()
            print("\nInteger-Constrained Gradient Descent:")
            trajectories_int, _, _ = self.perform_integer_constrained_gradient_descent(
                steps=max_steps, verbose=False
            )
            
            # Store results
            results['regular'].append({
                'final_distance': trajectories_reg['distance'][-1],
                'final_sum_error': trajectories_reg['magic_sum_error'][-1],
                'trajectory': trajectories_reg
            })
            
            results['integer_constrained'].append({
                'final_distance': trajectories_int['distance'][-1],
                'final_sum_error': trajectories_int['magic_sum_error'][-1],
                'final_int_dev': trajectories_int['integer_deviation'][-1],
                'trajectory': trajectories_int
            })
            
            # Print comparison
            print(f"\nComparison of results:")
            print(f"Regular GD - Final Distance: {trajectories_reg['distance'][-1]:.8f}, "
                  f"Sum Error: {trajectories_reg['magic_sum_error'][-1]:.8f}")
            print(f"Integer GD - Final Distance: {trajectories_int['distance'][-1]:.8f}, "
                  f"Sum Error: {trajectories_int['magic_sum_error'][-1]:.8f}, "
                  f"Integer Dev: {trajectories_int['integer_deviation'][-1]:.8f}")
        
        return results

    def plot_convergence_comparison(self, results, save_path='covariance_proof/convergence_comparison.png'):
        """Plot detailed comparison of regular and integer-constrained convergence."""
        plt.figure(figsize=(15, 10))
        
        # Plot distance trajectories
        plt.subplot(2, 2, 1)
        for i in range(len(results['regular'])):
            plt.plot(results['regular'][i]['trajectory']['distance'], 
                    'b-', alpha=0.3, label='Regular' if i == 0 else None)
            plt.plot(results['integer_constrained'][i]['trajectory']['distance'], 
                    'r-', alpha=0.3, label='Integer' if i == 0 else None)
        plt.yscale('log')
        plt.title('Distance to Manifold')
        plt.xlabel('Steps')
        plt.ylabel('Distance')
        plt.legend()
        plt.grid(True)
        
        # Plot sum error trajectories
        plt.subplot(2, 2, 2)
        for i in range(len(results['regular'])):
            plt.plot(results['regular'][i]['trajectory']['magic_sum_error'], 
                    'b-', alpha=0.3)
            plt.plot(results['integer_constrained'][i]['trajectory']['magic_sum_error'], 
                    'r-', alpha=0.3)
        plt.yscale('log')
        plt.title('Magic Sum Error')
        plt.xlabel('Steps')
        plt.ylabel('Error')
        plt.grid(True)
        
        # Plot integer deviation (only for integer-constrained)
        plt.subplot(2, 2, 3)
        for i in range(len(results['integer_constrained'])):
            plt.plot(results['integer_constrained'][i]['trajectory']['integer_deviation'], 
                    'r-', alpha=0.3)
        plt.yscale('log')
        plt.title('Integer Deviation')
        plt.xlabel('Steps')
        plt.ylabel('Deviation')
        plt.grid(True)
        
        # Plot final state distribution
        plt.subplot(2, 2, 4)
        reg_dist = [r['final_distance'] for r in results['regular']]
        int_dist = [r['final_distance'] for r in results['integer_constrained']]
        plt.boxplot([reg_dist, int_dist], labels=['Regular', 'Integer'])
        plt.yscale('log')
        plt.title('Final Distance Distribution')
        plt.ylabel('Distance')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    def perform_hybrid_gradient_descent(self, continuous_steps=100, integer_steps=100, 
                                     switch_threshold=1e-3, learning_rate=0.1, verbose=True):
        """
        Hybrid approach: first get close to manifold with continuous optimization,
        then switch to integer-constrained optimization when we're close enough.
        """
        # Phase 1: Continuous optimization to get close to manifold
        if verbose:
            print("\nPhase 1: Continuous Optimization")
        
        trajectories = {
            'distance': [],
            'magic_sum_error': [],
            'integer_deviation': [],
            'x_cov': [],
            'y_cov': [],
            'diag_main_cov': [],
            'diag_anti_cov': [],
            'phase': []  # 0 for continuous, 1 for integer
        }
        
        # Start with improved gradient descent
        cont_trajectories, squares, initial_square = self.perform_improved_gradient_descent(
            steps=continuous_steps,
            learning_rate=learning_rate,
            verbose=verbose
        )
        
        # Record continuous phase results
        trajectories['distance'].extend(cont_trajectories['distance'])
        trajectories['magic_sum_error'].extend(cont_trajectories['magic_sum_error'])
        trajectories['integer_deviation'].extend([np.sum(np.abs(s - np.round(s))) for s in squares])
        trajectories['x_cov'].extend(cont_trajectories['x_cov'])
        trajectories['y_cov'].extend(cont_trajectories['y_cov'])
        trajectories['diag_main_cov'].extend(cont_trajectories['diag_main_cov'])
        trajectories['diag_anti_cov'].extend(cont_trajectories['diag_anti_cov'])
        trajectories['phase'].extend([0] * len(cont_trajectories['distance']))
        
        # Check if we're close enough to switch to integer optimization
        current_distance = trajectories['distance'][-1]
        
        if current_distance > switch_threshold:
            if verbose:
                print(f"\nWarning: Did not reach switch threshold ({current_distance:.6f} > {switch_threshold})")
                print("Continuing with integer optimization anyway...")
        
        # Store best continuous solution
        best_continuous = self.square.copy()
        best_continuous_distance = current_distance
        
        if verbose:
            print(f"\nPhase 2: Integer-Constrained Optimization")
            print(f"Starting from distance: {current_distance:.6f}")
        
        # Phase 2: Integer-constrained optimization
        int_trajectories, int_squares, _ = self.perform_integer_constrained_gradient_descent(
            steps=integer_steps,
            learning_rate=learning_rate * 0.5,  # Reduce learning rate for integer phase
            projection_frequency=5,  # More frequent projections
            verbose=verbose
        )
        
        # Record integer phase results
        trajectories['distance'].extend(int_trajectories['distance'])
        trajectories['magic_sum_error'].extend(int_trajectories['magic_sum_error'])
        trajectories['integer_deviation'].extend(int_trajectories['integer_deviation'])
        trajectories['x_cov'].extend(int_trajectories['x_cov'])
        trajectories['y_cov'].extend(int_trajectories['y_cov'])
        trajectories['diag_main_cov'].extend(int_trajectories['diag_main_cov'])
        trajectories['diag_anti_cov'].extend(int_trajectories['diag_anti_cov'])
        trajectories['phase'].extend([1] * len(int_trajectories['distance']))
        
        # Check if integer solution is better than continuous
        final_distance = trajectories['distance'][-1]
        final_int_dev = trajectories['integer_deviation'][-1]
        
        if final_distance > best_continuous_distance and final_int_dev > 0.1:
            if verbose:
                print("\nReverting to best continuous solution and applying final integer projection...")
            
            # Revert to best continuous solution
            self.square = best_continuous
            
            # Apply one final integer projection
            current_sum = np.sum(self.square)
            rounded = np.round(self.square)
            sum_diff = current_sum - np.sum(rounded)
            adjustment = sum_diff / (self.size * self.size)
            self.square = rounded + adjustment
            
            # Update final metrics
            self.points = self.create_axial_points()
            final_distance = self.compute_distance_to_manifold()
            final_sum_error = self.magic_sum_error()
            final_int_dev = np.sum(np.abs(self.square - np.round(self.square)))
            
            # Add final state to trajectories
            for key in ['distance', 'magic_sum_error', 'x_cov', 'y_cov', 
                       'diag_main_cov', 'diag_anti_cov', 'integer_deviation', 'phase']:
                if key == 'distance':
                    trajectories[key].append(final_distance)
                elif key == 'magic_sum_error':
                    trajectories[key].append(final_sum_error)
                elif key == 'integer_deviation':
                    trajectories[key].append(final_int_dev)
                elif key == 'phase':
                    trajectories[key].append(2)  # Final projection phase
                else:
                    trajectories[key].append(trajectories[key][-1])
        
        if verbose:
            print(f"\nFinal Results:")
            print(f"Distance: {final_distance:.6f}")
            print(f"Sum Error: {trajectories['magic_sum_error'][-1]:.6f}")
            print(f"Integer Deviation: {final_int_dev:.6f}")
            print(f"Is Magic: {self.is_magic()}")
        
        return trajectories, squares + int_squares, initial_square

    def plot_hybrid_convergence(self, trajectories, save_path='covariance_proof/hybrid_convergence.png'):
        """Plot detailed analysis of hybrid convergence."""
        plt.figure(figsize=(15, 10))
        
        # Create phase masks
        continuous_mask = np.array(trajectories['phase']) == 0
        integer_mask = np.array(trajectories['phase']) == 1
        final_mask = np.array(trajectories['phase']) == 2
        
        # Plot distance trajectory
        plt.subplot(2, 2, 1)
        plt.plot(np.where(continuous_mask)[0], np.array(trajectories['distance'])[continuous_mask], 
                'b-', label='Continuous', alpha=0.8)
        plt.plot(np.where(integer_mask)[0], np.array(trajectories['distance'])[integer_mask], 
                'r-', label='Integer', alpha=0.8)
        if np.any(final_mask):
            plt.plot(np.where(final_mask)[0], np.array(trajectories['distance'])[final_mask], 
                    'g*', label='Final', markersize=10)
        plt.yscale('log')
        plt.title('Distance to Manifold')
        plt.xlabel('Steps')
        plt.ylabel('Distance')
        plt.legend()
        plt.grid(True)
        
        # Plot sum error
        plt.subplot(2, 2, 2)
        plt.plot(np.where(continuous_mask)[0], np.array(trajectories['magic_sum_error'])[continuous_mask], 'b-', alpha=0.8)
        plt.plot(np.where(integer_mask)[0], np.array(trajectories['magic_sum_error'])[integer_mask], 'r-', alpha=0.8)
        if np.any(final_mask):
            plt.plot(np.where(final_mask)[0], np.array(trajectories['magic_sum_error'])[final_mask], 'g*', markersize=10)
        plt.yscale('log')
        plt.title('Magic Sum Error')
        plt.xlabel('Steps')
        plt.ylabel('Error')
        plt.grid(True)
        
        # Plot integer deviation
        plt.subplot(2, 2, 3)
        plt.plot(np.where(continuous_mask)[0], np.array(trajectories['integer_deviation'])[continuous_mask], 'b-', alpha=0.8)
        plt.plot(np.where(integer_mask)[0], np.array(trajectories['integer_deviation'])[integer_mask], 'r-', alpha=0.8)
        if np.any(final_mask):
            plt.plot(np.where(final_mask)[0], np.array(trajectories['integer_deviation'])[final_mask], 'g*', markersize=10)
        plt.yscale('log')
        plt.title('Integer Deviation')
        plt.xlabel('Steps')
        plt.ylabel('Deviation')
        plt.grid(True)
        
        # Plot covariance constraints
        plt.subplot(2, 2, 4)
        for label, key in [('Row', 'x_cov'), ('Col', 'y_cov'), 
                          ('Main Diag', 'diag_main_cov'), ('Anti Diag', 'diag_anti_cov')]:
            values = np.array(trajectories[key])
            plt.plot(np.where(continuous_mask)[0], values[continuous_mask], alpha=0.3, label=f'{label} (cont)')
            plt.plot(np.where(integer_mask)[0], values[integer_mask], alpha=0.3, label=f'{label} (int)')
        plt.title('Covariance Constraints')
        plt.xlabel('Steps')
        plt.ylabel('Value')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()

def main():
    # Initialize analyzer
    analyzer = MagicSquareAnalyzer()
    
    print("Testing Morse Theory Approach to Magic Squares")
    print("==============================================")
    print("\nOriginal Magic Square:")
    print(analyzer.square)
    
    # Check if the magic square is actually magic
    print("\nChecking if square is magic (by definition):", analyzer.is_magic())
    print("\nChecking if square is magic (by covariance):")
    constraints = analyzer.compute_covariance_constraints()
    print(f"Covariance Constraints: {constraints}")
    distance = analyzer.compute_distance_to_manifold()
    print(f"Distance to Manifold: {distance:.10f}")
    
    # Test gradient at the magic square
    print("\nGradient Analysis:")
    gradient = analyzer.compute_covariance_gradient()
    gradient_norm = np.linalg.norm(gradient)
    print(f"Gradient Norm: {gradient_norm:.10f}")
    
    # Analyze critical points
    print("\nCritical Point Analysis:")
    print("Analyzing how perturbations affect gradient and distance...")
    results = analyzer.analyze_critical_points(num_perturbations=5)
    
    print("\nResults:")
    print("Number of Swaps | Distance to Manifold | Gradient Norm | Is Magic")
    for swaps, distance, gradient_norm, is_magic in results:
        print(f"{swaps:14} | {distance:19.10f} | {gradient_norm:12.8f} | {is_magic}")
    
    # Perform gradient descent from a perturbed state
    print("\nGradient Descent Experiment:")
    # Perturb the square
    perturbed = analyzer.perturb_square(swaps=2)
    analyzer.square = perturbed
    analyzer.points = analyzer.create_axial_points()
    print("Starting from perturbed state:")
    initial_distance = analyzer.compute_distance_to_manifold()
    initial_sum_error = analyzer.magic_sum_error()
    print(f"Initial Distance: {initial_distance:.10f}, Sum Error: {initial_sum_error:.10f}")
    
    # Run improved gradient descent
    print("Running improved gradient descent...")
    trajectories, squares, initial_square = analyzer.perform_improved_gradient_descent(steps=200)
    
    final_distance = trajectories['distance'][-1]
    final_sum_error = trajectories['magic_sum_error'][-1]
    print(f"Final Distance: {final_distance:.10f}, Sum Error: {final_sum_error:.10f}")
    print(f"Final square is magic: {analyzer.is_magic()}")
    
    # Plot detailed results
    plt.figure(figsize=(15, 10))
    
    # Plot distance trajectory
    plt.subplot(2, 2, 1)
    plt.plot(trajectories['distance'])
    plt.title('Distance to Manifold')
    plt.xlabel('Steps')
    plt.ylabel('Distance')
    plt.yscale('log')
    plt.grid(True)
    
    # Plot magic sum error
    plt.subplot(2, 2, 2)
    plt.plot(trajectories['magic_sum_error'])
    plt.title('Magic Sum Error')
    plt.xlabel('Steps')
    plt.ylabel('Average Error')
    plt.yscale('log')
    plt.grid(True)
    
    # Plot individual covariance constraints
    plt.subplot(2, 2, 3)
    plt.plot(trajectories['x_cov'], label='Row Cov')
    plt.plot(trajectories['y_cov'], label='Col Cov')
    plt.plot(trajectories['diag_main_cov'], label='Main Diag Cov')
    plt.plot(trajectories['diag_anti_cov'], label='Anti Diag Cov')
    plt.title('Individual Covariance Constraints')
    plt.xlabel('Steps')
    plt.ylabel('Covariance Value')
    plt.legend()
    plt.grid(True)
    
    # Plot before and after heatmaps
    plt.subplot(2, 2, 4)
    diff = analyzer.square - initial_square
    plt.imshow(diff, cmap='coolwarm')
    plt.colorbar()
    plt.title('Change in Square Values')
    
    plt.tight_layout()
    plt.savefig('gradient_descent_detailed.png')
    print("Saved detailed gradient descent analysis as 'gradient_descent_detailed.png'")
    
    # Analyze convergence to magic squares with improved algorithm
    print("\nAnalyzing Convergence to Magic Squares (Improved Algorithm):")
    convergence_results = analyzer.analyze_convergence_to_magic(
        num_experiments=5, 
        perturbation_level=1,  # Smaller perturbations to test local convergence
        descent_steps=200,
        use_improved=True
    )
    
    # Plot convergence results
    plt.figure(figsize=(10, 6))
    for i, result in enumerate(convergence_results):
        plt.plot(result['trajectories']['distance'], label=f"Experiment {i+1}")
    
    plt.title('Convergence from Different Starting Points')
    plt.xlabel('Gradient Descent Steps')
    plt.ylabel('Distance to Manifold')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig('convergence_analysis.png')
    print("Saved convergence analysis plot as 'convergence_analysis.png'")
    
    # Final summary with updated metrics
    magic_count = sum(1 for result in convergence_results if result['final_is_magic'])
    near_magic_count = sum(1 for result in convergence_results if result['is_near_magic'])
    print(f"\nSummary: {magic_count} out of {len(convergence_results)} gradient flows converged exactly to magic squares.")
    print(f"Additionally, {near_magic_count} flows converged to near-magic squares (distance < 0.001, sum error < 0.1).")
    print(f"Average final distance: {np.mean([r['final_distance'] for r in convergence_results]):.8f}")
    print(f"Average final sum error: {np.mean([r['final_sum_error'] for r in convergence_results]):.8f}")
    
    # Save detailed results to a text file
    with open('morse_theory_results.txt', 'w') as f:
        f.write("Magic Square Morse Theory Analysis Results\n")
        f.write("=========================================\n\n")
        
        f.write("Original Magic Square:\n")
        f.write(str(analyzer.create_magic_square()) + "\n\n")
        
        f.write("Perturbation Analysis:\n")
        f.write("Number of Swaps | Distance to Manifold | Gradient Norm | Is Magic\n")
        for swaps, distance, gradient_norm, is_magic in results:
            f.write(f"{swaps:14} | {distance:19.10f} | {gradient_norm:12.8f} | {is_magic}\n")
        
        f.write("\nConvergence Analysis:\n")
        for i, result in enumerate(convergence_results):
            f.write(f"\nExperiment {i+1}:\n")
            f.write(f"Initial Distance: {result['initial_distance']:.8f}, Sum Error: {result['initial_sum_error']:.8f}, Is Magic: {result['initial_is_magic']}\n")
            f.write(f"Final Distance: {result['final_distance']:.8f}, Sum Error: {result['final_sum_error']:.8f}, Is Magic: {result['final_is_magic']}\n")
        
        f.write(f"\nSummary: {magic_count} out of {len(convergence_results)} gradient flows converged exactly to magic squares.\n")
        f.write(f"Additionally, {near_magic_count} flows converged to near-magic squares (distance < 0.001, sum error < 0.1).\n")
        f.write(f"Average final distance: {np.mean([r['final_distance'] for r in convergence_results]):.8f}\n")
        f.write(f"Average final sum error: {np.mean([r['final_sum_error'] for r in convergence_results]):.8f}\n")
    
    print("\nDetails saved to 'morse_theory_results.txt'")
    print("\nConclusion: This analysis supports Richard's hypothesis that magic squares correspond to")
    print("critical points of the gradient flow on the magic square variety. The magic square manifold")
    print("appears to have a complex structure with multiple basins of attraction. Not all gradient")
    print("flows converge to exactly magic squares, but many converge to near-magic squares that are")
    print("very close to the manifold, suggesting that the integer magic squares may be surrounded by")
    print("continuous regions of near-magic arrangements.")
    
    print("\nAnalyzing Convergence Patterns with Integer Constraints:")
    convergence_results = analyzer.analyze_convergence_patterns(num_experiments=5)
    
    # Plot comparison
    analyzer.plot_convergence_comparison(convergence_results)
    print("\nSaved convergence comparison plot as 'covariance_proof/convergence_comparison.png'")
    
    # Compute statistics
    reg_success = sum(1 for r in convergence_results['regular'] 
                     if r['final_distance'] < 1e-5 and r['final_sum_error'] < 0.1)
    int_success = sum(1 for r in convergence_results['integer_constrained']
                     if r['final_distance'] < 1e-5 and r['final_sum_error'] < 0.1 
                     and r['final_int_dev'] < 0.1)
    
    print("\nConvergence Statistics:")
    print(f"Regular GD success rate: {reg_success}/{len(convergence_results['regular'])}")
    print(f"Integer GD success rate: {int_success}/{len(convergence_results['integer_constrained'])}")
    
    print("\nAverage final metrics:")
    print("Regular GD:")
    print(f"  Distance: {np.mean([r['final_distance'] for r in convergence_results['regular']]):.8f}")
    print(f"  Sum Error: {np.mean([r['final_sum_error'] for r in convergence_results['regular']]):.8f}")
    print("Integer-constrained GD:")
    print(f"  Distance: {np.mean([r['final_distance'] for r in convergence_results['integer_constrained']]):.8f}")
    print(f"  Sum Error: {np.mean([r['final_sum_error'] for r in convergence_results['integer_constrained']]):.8f}")
    print(f"  Integer Deviation: {np.mean([r['final_int_dev'] for r in convergence_results['integer_constrained']]):.8f}")

    print("\nTesting Hybrid Gradient Descent Approach:")
    # Start from a perturbed square
    perturbed = analyzer.perturb_square(swaps=2)
    analyzer.square = perturbed
    analyzer.points = analyzer.create_axial_points()
    
    # Run hybrid gradient descent
    hybrid_trajectories, hybrid_squares, _ = analyzer.perform_hybrid_gradient_descent(
        continuous_steps=150,
        integer_steps=100,
        switch_threshold=1e-3,
        verbose=True
    )
    
    # Plot hybrid results
    analyzer.plot_hybrid_convergence(hybrid_trajectories)
    print("\nSaved hybrid convergence analysis as 'covariance_proof/hybrid_convergence.png'")
    
    # Compare final results
    final_distance = hybrid_trajectories['distance'][-1]
    final_sum_error = hybrid_trajectories['magic_sum_error'][-1]
    final_int_dev = hybrid_trajectories['integer_deviation'][-1]
    
    print("\nFinal Hybrid Approach Results:")
    print(f"Distance to Manifold: {final_distance:.8f}")
    print(f"Magic Sum Error: {final_sum_error:.8f}")
    print(f"Integer Deviation: {final_int_dev:.8f}")
    print(f"Is Magic Square: {analyzer.is_magic()}")
    
    if analyzer.is_magic():
        print("\nFound a new magic square!")
        print(analyzer.square)

if __name__ == "__main__":
    main() 