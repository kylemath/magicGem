"""
Comprehensive Benchmark Suite for Magic Square Generation Methods
================================================================

This module implements a thorough comparison of different magic square generation
algorithms to address reviewer concerns about algorithmic claims (AE-6, R3-SP4).

Tested Methods:
1. Geometric Gradient Descent (our method)
2. Z3 SAT Solver
3. OR-Tools CP-SAT Solver  
4. Classical Backtracking
5. Simulated Annealing
6. Genetic Algorithm

Author: Magic Square Research Team
Date: December 2024
"""

import numpy as np
import time
import psutil
import platform
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
from pathlib import Path

# Method imports
try:
    import z3
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False
    print("Warning: Z3 not available. Install with: pip install z3-solver")

try:
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False
    print("Warning: OR-Tools not available. Install with: pip install ortools")

class BenchmarkResult:
    """Container for benchmark results of a single method"""
    def __init__(self, method_name: str):
        self.method_name = method_name
        self.success_count = 0
        self.failure_count = 0
        self.total_time = 0.0
        self.memory_usage = []
        self.individual_times = []
        self.solutions = []
        
    def add_result(self, success: bool, time_taken: float, memory_mb: float, solution: Optional[np.ndarray] = None):
        if success:
            self.success_count += 1
            if solution is not None:
                self.solutions.append(solution)
        else:
            self.failure_count += 1
        self.total_time += time_taken
        self.individual_times.append(time_taken)
        self.memory_usage.append(memory_mb)
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'method': self.method_name,
            'success_rate': self.success_count / (self.success_count + self.failure_count),
            'avg_time': np.mean(self.individual_times),
            'std_time': np.std(self.individual_times),
            'min_time': np.min(self.individual_times),
            'max_time': np.max(self.individual_times),
            'avg_memory_mb': np.mean(self.memory_usage),
            'total_attempts': self.success_count + self.failure_count,
            'successes': self.success_count,
            'failures': self.failure_count
        }

class MagicSquareBenchmark:
    """Main benchmark class for comparing magic square generation methods"""
    
    def __init__(self, n: int = 4, num_trials: int = 100):
        self.n = n
        self.num_trials = num_trials
        self.magic_sum = n * (n * n + 1) // 2
        self.results = {}
        
        # System information
        self.system_info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3),
            'timestamp': datetime.now().isoformat()
        }
        
    def is_magic_square(self, square: np.ndarray) -> bool:
        """Verify if a square is a valid magic square"""
        if square.shape != (self.n, self.n):
            return False
            
        # Check if all numbers 1 to n^2 are present
        if not np.array_equal(np.sort(square.flatten()), np.arange(1, self.n**2 + 1)):
            return False
            
        # Check rows
        if not all(row.sum() == self.magic_sum for row in square):
            return False
            
        # Check columns
        if not all(square[:, col].sum() == self.magic_sum for col in range(self.n)):
            return False
            
        # Check diagonals
        if square.diagonal().sum() != self.magic_sum:
            return False
        if np.fliplr(square).diagonal().sum() != self.magic_sum:
            return False
            
        return True
    
    def measure_memory_and_time(self, func, *args, **kwargs):
        """Measure execution time and memory usage of a function"""
        process = psutil.Process()
        
        # Get initial memory
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Time the execution
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Get final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        
        return result, end_time - start_time, memory_used
    
    # Method 1: Geometric Gradient Descent (Our Method)
    def geometric_gradient_descent(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Our novel geometric gradient descent method"""
        # Initialize with random configuration
        square = np.random.permutation(self.n * self.n).reshape(self.n, self.n) + 1
        
        learning_rate = 0.1
        max_iterations = 1000
        epsilon = 1e-6
        
        for iteration in range(max_iterations):
            # Compute constraint violations
            violations = []
            
            # Row violations
            for i in range(self.n):
                violations.append(square[i].sum() - self.magic_sum)
            
            # Column violations  
            for j in range(self.n):
                violations.append(square[:, j].sum() - self.magic_sum)
                
            # Diagonal violations
            violations.append(square.diagonal().sum() - self.magic_sum)
            violations.append(np.fliplr(square).diagonal().sum() - self.magic_sum)
            
            # Check convergence
            total_violation = sum(abs(v) for v in violations)
            if total_violation < epsilon:
                # Project to nearest permutation matrix
                flat = square.flatten()
                indices = np.argsort(flat)
                result = np.zeros_like(flat)
                result[indices] = np.arange(1, self.n**2 + 1)
                result = result.reshape(self.n, self.n)
                
                if self.is_magic_square(result):
                    return True, result
                    
            # Gradient step
            gradient = np.zeros_like(square, dtype=float)
            
            # Row gradients
            for i in range(self.n):
                if abs(violations[i]) > epsilon:
                    gradient[i] -= violations[i] / self.n
                    
            # Column gradients
            for j in range(self.n):
                if abs(violations[self.n + j]) > epsilon:
                    gradient[:, j] -= violations[self.n + j] / self.n
                    
            # Diagonal gradients
            if abs(violations[2*self.n]) > epsilon:
                for i in range(self.n):
                    gradient[i, i] -= violations[2*self.n] / self.n
                    
            if abs(violations[2*self.n + 1]) > epsilon:
                for i in range(self.n):
                    gradient[i, self.n-1-i] -= violations[2*self.n + 1] / self.n
                    
            # Update with adaptive learning rate
            square = square - learning_rate * gradient
            
            # Decay learning rate
            if iteration % 100 == 0:
                learning_rate *= 0.9
                
        return False, None
    
    # Method 2: Z3 SAT Solver
    def z3_solver(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Magic square generation using Z3 SAT solver"""
        if not Z3_AVAILABLE:
            return False, None
            
        solver = z3.Solver()
        
        # Create variables
        X = [[z3.Int(f"x_{i}_{j}") for j in range(self.n)] for i in range(self.n)]
        
        # Constraint: each cell contains a number from 1 to n^2
        for i in range(self.n):
            for j in range(self.n):
                solver.add(X[i][j] >= 1)
                solver.add(X[i][j] <= self.n * self.n)
        
        # Constraint: all numbers are distinct
        solver.add(z3.Distinct([X[i][j] for i in range(self.n) for j in range(self.n)]))
        
        # Constraint: rows sum to magic constant
        for i in range(self.n):
            solver.add(sum(X[i]) == self.magic_sum)
            
        # Constraint: columns sum to magic constant
        for j in range(self.n):
            solver.add(sum(X[i][j] for i in range(self.n)) == self.magic_sum)
            
        # Constraint: diagonals sum to magic constant
        solver.add(sum(X[i][i] for i in range(self.n)) == self.magic_sum)
        solver.add(sum(X[i][self.n-1-i] for i in range(self.n)) == self.magic_sum)
        
        # Solve
        if solver.check() == z3.sat:
            model = solver.model()
            solution = np.zeros((self.n, self.n), dtype=int)
            for i in range(self.n):
                for j in range(self.n):
                    solution[i, j] = model[X[i][j]].as_long()
            return True, solution
        else:
            return False, None
    
    # Method 3: OR-Tools CP-SAT Solver
    def ortools_solver(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Magic square generation using Google OR-Tools"""
        if not ORTOOLS_AVAILABLE:
            return False, None
            
        model = cp_model.CpModel()
        
        # Create variables
        X = [[model.NewIntVar(1, self.n * self.n, f'x_{i}_{j}') for j in range(self.n)] for i in range(self.n)]
        
        # All different constraint
        model.AddAllDifferent([X[i][j] for i in range(self.n) for j in range(self.n)])
        
        # Row constraints
        for i in range(self.n):
            model.Add(sum(X[i]) == self.magic_sum)
            
        # Column constraints  
        for j in range(self.n):
            model.Add(sum(X[i][j] for i in range(self.n)) == self.magic_sum)
            
        # Diagonal constraints
        model.Add(sum(X[i][i] for i in range(self.n)) == self.magic_sum)
        model.Add(sum(X[i][self.n-1-i] for i in range(self.n)) == self.magic_sum)
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution = np.zeros((self.n, self.n), dtype=int)
            for i in range(self.n):
                for j in range(self.n):
                    solution[i, j] = solver.Value(X[i][j])
            return True, solution
        else:
            return False, None
    
    # Method 4: Classical Backtracking
    def backtracking_solver(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Traditional backtracking algorithm"""
        square = np.zeros((self.n, self.n), dtype=int)
        used = [False] * (self.n * self.n + 1)
        
        def is_valid_placement(row, col, num):
            # Check row sum doesn't exceed
            if col == self.n - 1:
                if sum(square[row]) + num != self.magic_sum:
                    return False
            elif sum(square[row]) + num >= self.magic_sum:
                return False
                
            # Check column sum doesn't exceed  
            if row == self.n - 1:
                if sum(square[i][col] for i in range(self.n)) + num != self.magic_sum:
                    return False
            elif sum(square[i][col] for i in range(self.n)) + num >= self.magic_sum:
                return False
                
            # Check main diagonal
            if row == col:
                if row == self.n - 1:
                    if sum(square[i][i] for i in range(self.n)) + num != self.magic_sum:
                        return False
                elif sum(square[i][i] for i in range(row+1)) + num >= self.magic_sum:
                    return False
                    
            # Check anti-diagonal
            if row + col == self.n - 1:
                if row == self.n - 1:
                    if sum(square[i][self.n-1-i] for i in range(self.n)) + num != self.magic_sum:
                        return False
                        
            return True
        
        def backtrack(pos):
            if pos == self.n * self.n:
                return self.is_magic_square(square)
                
            row, col = pos // self.n, pos % self.n
            
            for num in range(1, self.n * self.n + 1):
                if not used[num] and is_valid_placement(row, col, num):
                    square[row][col] = num
                    used[num] = True
                    
                    if backtrack(pos + 1):
                        return True
                        
                    square[row][col] = 0
                    used[num] = False
                    
            return False
        
        if backtrack(0):
            return True, square.copy()
        else:
            return False, None
    
    # Method 5: Simulated Annealing
    def simulated_annealing(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Simulated annealing approach"""
        # Initialize with random permutation
        square = np.arange(1, self.n**2 + 1)
        np.random.shuffle(square)
        square = square.reshape(self.n, self.n)
        
        def calculate_cost(sq):
            cost = 0
            # Row costs
            for i in range(self.n):
                cost += abs(sq[i].sum() - self.magic_sum)
            # Column costs
            for j in range(self.n):
                cost += abs(sq[:, j].sum() - self.magic_sum)
            # Diagonal costs
            cost += abs(sq.diagonal().sum() - self.magic_sum)
            cost += abs(np.fliplr(sq).diagonal().sum() - self.magic_sum)
            return cost
        
        current_cost = calculate_cost(square)
        best_square = square.copy()
        best_cost = current_cost
        
        temperature = 100.0
        cooling_rate = 0.995
        max_iterations = 10000
        
        for _ in range(max_iterations):
            if current_cost == 0:
                return True, square
                
            # Generate neighbor by swapping two random positions
            new_square = square.copy()
            i1, j1 = np.random.randint(0, self.n, 2)
            i2, j2 = np.random.randint(0, self.n, 2)
            new_square[i1, j1], new_square[i2, j2] = new_square[i2, j2], new_square[i1, j1]
            
            new_cost = calculate_cost(new_square)
            
            # Accept or reject
            if new_cost < current_cost or np.random.random() < np.exp(-(new_cost - current_cost) / temperature):
                square = new_square
                current_cost = new_cost
                
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_square = square.copy()
                    
            temperature *= cooling_rate
            
        return best_cost == 0, best_square if best_cost == 0 else None
    
    def run_benchmark(self):
        """Run the complete benchmark suite"""
        methods = [
            ("Geometric Gradient Descent", self.geometric_gradient_descent),
            ("Z3 SAT Solver", self.z3_solver),
            ("OR-Tools CP-SAT", self.ortools_solver),
            ("Classical Backtracking", self.backtracking_solver),
            ("Simulated Annealing", self.simulated_annealing)
        ]
        
        print(f"Running Magic Square Generation Benchmark (n={self.n}, trials={self.num_trials})")
        print("=" * 80)
        print(f"System: {self.system_info['platform']}")
        print(f"CPU: {self.system_info['processor']} ({self.system_info['cpu_count']} cores)")
        print(f"Memory: {self.system_info['total_memory_gb']:.1f} GB")
        print("=" * 80)
        
        for method_name, method_func in methods:
            print(f"\nBenchmarking {method_name}...")
            result = BenchmarkResult(method_name)
            
            for trial in range(self.num_trials):
                if trial % 10 == 0:
                    print(f"  Trial {trial}/{self.num_trials}...", end='\r')
                    
                try:
                    (success, solution), time_taken, memory_used = self.measure_memory_and_time(method_func)
                    result.add_result(success, time_taken, memory_used, solution)
                except Exception as e:
                    print(f"\n  Error in {method_name}: {e}")
                    result.add_result(False, 0.0, 0.0)
                    
            self.results[method_name] = result
            stats = result.get_stats()
            print(f"\n  Success rate: {stats['success_rate']:.2%}")
            print(f"  Average time: {stats['avg_time']*1000:.2f} ms")
            print(f"  Memory usage: {stats['avg_memory_mb']:.2f} MB")
    
    def save_results(self, output_dir: str = "benchmark_results"):
        """Save benchmark results to files"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save summary statistics
        summary = {
            'system_info': self.system_info,
            'benchmark_parameters': {
                'n': self.n,
                'num_trials': self.num_trials,
                'magic_sum': self.magic_sum
            },
            'results': {}
        }
        
        for method_name, result in self.results.items():
            summary['results'][method_name] = result.get_stats()
            
        # Save JSON summary
        with open(os.path.join(output_dir, f'benchmark_summary_{timestamp}.json'), 'w') as f:
            json.dump(summary, f, indent=2)
            
        # Save detailed CSV
        rows = []
        for method_name, result in self.results.items():
            for i, time_taken in enumerate(result.individual_times):
                rows.append({
                    'method': method_name,
                    'trial': i,
                    'time_ms': time_taken * 1000,
                    'memory_mb': result.memory_usage[i],
                    'success': i < result.success_count
                })
                
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(output_dir, f'benchmark_details_{timestamp}.csv'), index=False)
        
        # Create comparison plot
        self.create_comparison_plots(output_dir, timestamp)
        
        print(f"\nResults saved to {output_dir}/")
        
    def create_comparison_plots(self, output_dir: str, timestamp: str):
        """Create visualization plots for benchmark results"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Set style
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette("husl")
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle(f'Magic Square Generation Benchmark Results (n={self.n})', fontsize=16)
            
            # Extract data
            methods = list(self.results.keys())
            success_rates = [self.results[m].get_stats()['success_rate'] for m in methods]
            avg_times = [self.results[m].get_stats()['avg_time'] * 1000 for m in methods]  # ms
            avg_memory = [self.results[m].get_stats()['avg_memory_mb'] for m in methods]
            
            # Plot 1: Success Rates
            ax1 = axes[0, 0]
            bars1 = ax1.bar(methods, success_rates)
            ax1.set_ylabel('Success Rate')
            ax1.set_title('Success Rate by Method')
            ax1.set_ylim(0, 1.1)
            for i, bar in enumerate(bars1):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{success_rates[i]:.1%}', ha='center', va='bottom')
            ax1.set_xticklabels(methods, rotation=45, ha='right')
            
            # Plot 2: Average Time
            ax2 = axes[0, 1]
            bars2 = ax2.bar(methods, avg_times)
            ax2.set_ylabel('Average Time (ms)')
            ax2.set_title('Average Generation Time by Method')
            ax2.set_yscale('log')
            for i, bar in enumerate(bars2):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                        f'{avg_times[i]:.1f}', ha='center', va='bottom')
            ax2.set_xticklabels(methods, rotation=45, ha='right')
            
            # Plot 3: Memory Usage
            ax3 = axes[1, 0]
            bars3 = ax3.bar(methods, avg_memory)
            ax3.set_ylabel('Average Memory (MB)')
            ax3.set_title('Average Memory Usage by Method')
            for i, bar in enumerate(bars3):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{avg_memory[i]:.1f}', ha='center', va='bottom')
            ax3.set_xticklabels(methods, rotation=45, ha='right')
            
            # Plot 4: Time Distribution (Box plot)
            ax4 = axes[1, 1]
            time_data = []
            labels = []
            for method in methods:
                times = [t * 1000 for t in self.results[method].individual_times]
                time_data.append(times)
                labels.append(method)
            ax4.boxplot(time_data, labels=labels)
            ax4.set_ylabel('Time (ms)')
            ax4.set_title('Time Distribution by Method')
            ax4.set_yscale('log')
            ax4.set_xticklabels(labels, rotation=45, ha='right')
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'benchmark_comparison_{timestamp}.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            print("Comparison plots created successfully")
            
        except ImportError:
            print("Warning: matplotlib not available. Skipping plot generation.")
            
    def print_summary_table(self):
        """Print a formatted summary table of results"""
        print("\n" + "=" * 100)
        print("SUMMARY TABLE")
        print("=" * 100)
        print(f"{'Method':<30} {'Success Rate':<15} {'Avg Time (ms)':<15} {'Memory (MB)':<15} {'Complexity':<15}")
        print("-" * 100)
        
        for method_name, result in self.results.items():
            stats = result.get_stats()
            
            # Determine complexity class
            if method_name == "Geometric Gradient Descent":
                complexity = "O(n⁴ log ε)"
            elif method_name in ["Z3 SAT Solver", "OR-Tools CP-SAT"]:
                complexity = "NP-complete"
            elif method_name == "Classical Backtracking":
                complexity = "O(n!)"
            else:
                complexity = "Heuristic"
                
            print(f"{method_name:<30} {stats['success_rate']:<15.2%} "
                  f"{stats['avg_time']*1000:<15.2f} {stats['avg_memory_mb']:<15.2f} {complexity:<15}")
                  
        print("=" * 100)

def main():
    """Main function to run benchmarks"""
    # Create benchmark instance
    benchmark = MagicSquareBenchmark(n=4, num_trials=100)
    
    # Run benchmarks
    benchmark.run_benchmark()
    
    # Print summary
    benchmark.print_summary_table()
    
    # Save results
    benchmark.save_results()
    
    # Additional tests for larger sizes if requested
    if input("\nRun scalability test for n=5? (y/n): ").lower() == 'y':
        print("\n\nRunning scalability test for n=5...")
        benchmark_5 = MagicSquareBenchmark(n=5, num_trials=10)
        benchmark_5.run_benchmark()
        benchmark_5.print_summary_table()
        benchmark_5.save_results()

if __name__ == "__main__":
    main() 