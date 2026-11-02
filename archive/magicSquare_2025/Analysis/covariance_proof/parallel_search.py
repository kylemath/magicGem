#!/usr/bin/env python3
"""
Parallel Multi-Starting Point Search for Magic Squares

This script implements a parallel search strategy with multiple starting points
to find magic squares using the enhanced gradient approach.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
from datetime import datetime
import concurrent.futures
import random
import json

# Import the enhanced analyzer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_hybrid_approach import EnhancedMagicSquareAnalyzer, run_experiment

class ParallelMagicSquareSearch:
    """Class to manage parallel search for magic squares."""
    
    def __init__(self, results_dir='covariance_proof/parallel_results'):
        """Initialize search manager."""
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Track all results
        self.all_results = []
        self.magic_squares = []
        self.best_near_magic = None
        
        # Timestamp for this search session
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Load previous best configurations if available
        self.best_previous_configs = self._load_previous_best_configs()
        
    def _load_previous_best_configs(self):
        """Load best configurations from previous runs."""
        config_file = f"{self.results_dir}/best_configs_latest.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    configs = json.load(f)
                print(f"Loaded {len(configs)} previous best configurations")
                return configs
            except Exception as e:
                print(f"Error loading previous configurations: {str(e)}")
        return []
        
    def _update_search_config_bias(self, best_configs):
        """Update the search configuration bias based on best results."""
        # This method is called after a search to update the bias for future runs
        # It doesn't affect the current run, but the information is saved for future reference
        
        # Extract the parameters from the best configurations
        best_params = {
            'transition_start': [c['transition_start'] for c in best_configs],
            'transition_end': [c['transition_end'] for c in best_configs],
            'total_steps': [c['total_steps'] for c in best_configs],
            'learning_rate': [c['learning_rate'] for c in best_configs],
            'swaps': [c['swaps'] for c in best_configs]
        }
        
        # Calculate the most common values
        most_common = {}
        for param, values in best_params.items():
            # Count occurrences
            counts = {}
            for v in values:
                counts[v] = counts.get(v, 0) + 1
            
            # Find most common
            most_common[param] = max(counts.items(), key=lambda x: x[1])[0]
        
        # Save the bias information
        bias_info = {
            'timestamp': self.timestamp,
            'most_common_params': most_common,
            'best_config': best_configs[0],
            'magic_found': any(c['metrics']['is_magic'] for c in best_configs)
        }
        
        bias_file = f"{self.results_dir}/search_bias_{self.timestamp}.json"
        with open(bias_file, 'w') as f:
            json.dump(bias_info, f, indent=2)
        
        print(f"Search bias information saved to {bias_file}")
        
    def get_search_config(self, search_id):
        """Generate a configuration for a search instance."""
        # Define parameter ranges
        transition_start_range = [50, 75, 100, 125, 150, 175]  # Added 175
        transition_length_range = [50, 75, 100, 125, 150]  # Added 150
        total_steps_range = [250, 300, 350, 400]  # Added 400
        learning_rate_range = [0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]  # Added more granular options
        swaps_range = [1, 2, 3, 4, 5]  # Added 5
        
        # Randomly select parameters
        transition_start = random.choice(transition_start_range)
        transition_length = random.choice(transition_length_range)
        transition_end = min(transition_start + transition_length, 
                            random.choice(total_steps_range) - 10)
        total_steps = max(transition_end + 50, random.choice(total_steps_range))
        learning_rate = random.choice(learning_rate_range)
        swaps = random.choice(swaps_range)
        
        # Bias toward known good configurations for some percentage of searches
        if search_id % 4 == 0:  # 25% of searches use known good configs
            # Late transition (similar to our successful run)
            transition_start = 150
            transition_end = 200
            total_steps = 250
            learning_rate = 0.1
            swaps = 2
        # Add another bias for extended search with longer steps
        elif search_id % 8 == 1:  # 12.5% of searches use extended configs
            transition_start = 175
            transition_end = 275
            total_steps = 350
            learning_rate = 0.075
            swaps = 3
        # Use previous best configurations if available
        elif self.best_previous_configs and search_id % 3 == 0:  # 33% of remaining searches
            # Select a random config from the top 3
            top_n = min(3, len(self.best_previous_configs))
            best_config = random.choice(self.best_previous_configs[:top_n])
            
            # Use its parameters
            transition_start = best_config['transition_start']
            transition_end = best_config['transition_end']
            total_steps = best_config['total_steps']
            learning_rate = best_config['learning_rate']
            swaps = best_config['swaps']
            
            print(f"Using previous best config for search {search_id} (score: {best_config['metrics']['combined_score']:.6f})")
        
        return {
            'transition_start': transition_start,
            'transition_end': transition_end,
            'total_steps': total_steps,
            'learning_rate': learning_rate,
            'swaps': swaps,
            'search_id': search_id
        }
    
    def run_search_instance(self, config):
        """Run a single search instance with the given configuration."""
        try:
            print(f"\nRunning search instance {config['search_id']}:")
            print(f"Parameters: Start={config['transition_start']}, End={config['transition_end']}, "
                 f"Steps={config['total_steps']}, LR={config['learning_rate']}, Swaps={config['swaps']}")
            
            # Run the experiment with verbose=False to reduce output clutter
            result = run_experiment(
                transition_start=config['transition_start'],
                transition_end=config['transition_end'],
                total_steps=config['total_steps'],
                learning_rate=config['learning_rate'],
                swaps=config['swaps'],
                enforce_monotonic=True,  # Enforce monotonic values from 1-16
                verbose=False  # Less verbose for parallel runs
            )
            
            # Add configuration info to result
            result['config'] = config
            
            # Return result
            return result
        except Exception as e:
            print(f"Error in search instance {config['search_id']}: {str(e)}")
            return {
                'config': config, 
                'error': str(e),
                'final_metrics': {
                    'distance': float('inf'),
                    'sum_error': float('inf'),
                    'int_dev': float('inf'),
                    'is_magic': False,
                    'is_monotonic': False,
                    'monotonic_error': float('inf')
                }
            }
    
    def run_parallel_search(self, num_instances=30, max_workers=4):
        """Run multiple search instances in parallel."""
        print(f"Starting parallel search with {num_instances} instances using {max_workers} workers")
        start_time = time.time()
        
        # Generate configurations
        configs = [self.get_search_config(i) for i in range(num_instances)]
        
        # Run searches in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.run_search_instance, configs))
        
        # Process results
        self.all_results = results
        # Find magic squares that are also monotonic (standard magic squares)
        self.magic_squares = [r for r in results if r.get('final_metrics', {}).get('is_magic', False) 
                             and r.get('final_metrics', {}).get('is_monotonic', False)]
        
        # Find best near-magic square if no exact solutions found
        if not self.magic_squares:
            # Sort by a combined metric (prioritize low distance, sum error, integer deviation, and monotonic error)
            valid_results = [r for r in results if 'error' not in r]
            if valid_results:
                self.best_near_magic = min(
                    valid_results, 
                    key=lambda r: (
                        r['final_metrics']['distance'] + 
                        r['final_metrics']['sum_error'] + 
                        r['final_metrics']['int_dev'] / 4 +  # Lower weight on integer deviation
                        r['final_metrics'].get('monotonic_error', 0) * 2  # Higher weight on monotonic error
                    )
                )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Print summary
        print(f"\nParallel search completed in {elapsed:.2f} seconds")
        print(f"Found {len(self.magic_squares)} standard magic squares (monotonic 1-16)")
        
        # Save results
        self.save_results()
        
        # Save best configurations for future use
        self.save_best_configs()
        
        return self.magic_squares, self.best_near_magic
    
    def save_results(self):
        """Save search results to disk."""
        results_file = f"{self.results_dir}/search_results_{self.timestamp}.json"
        
        # Prepare data for JSON serialization (convert NumPy arrays to lists)
        serializable_results = []
        for r in self.all_results:
            if 'error' in r:
                serializable_results.append(r)
                continue
                
            serializable_r = {
                'config': r['config'],
                'initial_metrics': r['initial_metrics'],
                'final_metrics': r['final_metrics'],
                'computation_time': r['computation_time'],
                'plot_files': r['plot_files']
            }
            
            # Convert NumPy array to list for JSON serialization
            if 'final_square' in r:
                serializable_r['final_square'] = r['final_square'].tolist()
                
            serializable_results.append(serializable_r)
        
        # Save to file
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"Results saved to {results_file}")
        
        # Generate summary visualization
        self.plot_search_results()
        
    def plot_search_results(self):
        """Generate visualization of search results."""
        # Create figure
        plt.figure(figsize=(15, 12))
        
        # Plot 1: Distance vs Sum Error scatter plot
        plt.subplot(2, 2, 1)
        distances = [r.get('final_metrics', {}).get('distance', float('inf')) 
                    for r in self.all_results if 'error' not in r]
        sum_errors = [r.get('final_metrics', {}).get('sum_error', float('inf')) 
                     for r in self.all_results if 'error' not in r]
        is_magic = [r.get('final_metrics', {}).get('is_magic', False) 
                   for r in self.all_results if 'error' not in r]
        
        # Scatter plot by magic status
        for i, (d, s, m) in enumerate(zip(distances, sum_errors, is_magic)):
            if m:
                plt.scatter(d, s, color='green', s=100, marker='*', edgecolor='black', zorder=10)
            else:
                plt.scatter(d, s, color='blue', alpha=0.5, s=30)
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(min(distances) * 0.1 if distances else 1e-6, max(distances) * 10 if distances else 1)
        plt.ylim(min(sum_errors) * 0.1 if sum_errors else 1e-6, max(sum_errors) * 10 if sum_errors else 10)
        plt.title('Final Distance vs Sum Error')
        plt.xlabel('Distance to Manifold')
        plt.ylabel('Magic Sum Error')
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Learning rate vs transition length effect
        plt.subplot(2, 2, 2)
        lr_values = [r.get('config', {}).get('learning_rate', 0) 
                    for r in self.all_results if 'error' not in r]
        trans_lengths = [r.get('config', {}).get('transition_end', 0) - 
                        r.get('config', {}).get('transition_start', 0) 
                        for r in self.all_results if 'error' not in r]
        
        for i, (lr, tl, m) in enumerate(zip(lr_values, trans_lengths, is_magic)):
            if m:
                plt.scatter(lr, tl, color='green', s=100, marker='*', edgecolor='black', zorder=10)
            else:
                plt.scatter(lr, tl, color='blue', alpha=0.5, s=30)
        
        plt.title('Learning Rate vs Transition Length')
        plt.xlabel('Learning Rate')
        plt.ylabel('Transition Length (steps)')
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Transition start vs success
        plt.subplot(2, 2, 3)
        trans_starts = [r.get('config', {}).get('transition_start', 0) 
                       for r in self.all_results if 'error' not in r]
        combined_score = [r.get('final_metrics', {}).get('distance', 0) + 
                         r.get('final_metrics', {}).get('sum_error', 0) 
                         for r in self.all_results if 'error' not in r]
        
        for i, (ts, cs, m) in enumerate(zip(trans_starts, combined_score, is_magic)):
            if m:
                plt.scatter(ts, cs, color='green', s=100, marker='*', edgecolor='black', zorder=10)
            else:
                plt.scatter(ts, cs, color='blue', alpha=0.5, s=30)
        
        plt.yscale('log')
        plt.title('Transition Start vs Combined Score')
        plt.xlabel('Transition Start Step')
        plt.ylabel('Combined Score (lower is better)')
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Performance by swaps
        plt.subplot(2, 2, 4)
        swaps = [r.get('config', {}).get('swaps', 0) 
                for r in self.all_results if 'error' not in r]
        
        # Group by number of swaps
        unique_swaps = sorted(set(swaps))
        swap_distances = [
            [r.get('final_metrics', {}).get('distance', float('inf')) 
             for r in self.all_results 
             if 'error' not in r and r.get('config', {}).get('swaps', 0) == s]
            for s in unique_swaps
        ]
        
        plt.boxplot(swap_distances, labels=unique_swaps)
        plt.yscale('log')
        plt.title('Distance by Initial Perturbation')
        plt.xlabel('Number of Swaps')
        plt.ylabel('Distance to Manifold')
        plt.grid(True, alpha=0.3)
        
        # Add legend and title
        plt.figtext(0.5, 0.95, f'Parallel Search Results - {len(self.all_results)} Instances', 
                   ha='center', fontsize=16)
        plt.figtext(0.5, 0.92, f'Found {len(self.magic_squares)} Magic Squares', 
                   ha='center', fontsize=14, 
                   color='green' if self.magic_squares else 'red')
        
        plt.tight_layout(rect=[0, 0, 1, 0.9])
        plt.savefig(f"{self.results_dir}/search_summary_{self.timestamp}.png")
        plt.close()
        
        # Generate additional analysis plots
        self._plot_parameter_effectiveness()
        
        print(f"Summary visualization saved to {self.results_dir}/search_summary_{self.timestamp}.png")
    
    def _plot_parameter_effectiveness(self):
        """Generate additional plots analyzing parameter effectiveness."""
        # Skip if no valid results
        valid_results = [r for r in self.all_results if 'error' not in r]
        if not valid_results:
            return
            
        # Create figure for parameter effectiveness
        plt.figure(figsize=(15, 10))
        
        # Extract parameters and metrics
        params = {
            'transition_start': [r.get('config', {}).get('transition_start', 0) for r in valid_results],
            'transition_end': [r.get('config', {}).get('transition_end', 0) for r in valid_results],
            'total_steps': [r.get('config', {}).get('total_steps', 0) for r in valid_results],
            'learning_rate': [r.get('config', {}).get('learning_rate', 0) for r in valid_results],
            'swaps': [r.get('config', {}).get('swaps', 0) for r in valid_results]
        }
        
        metrics = {
            'distance': [r.get('final_metrics', {}).get('distance', float('inf')) for r in valid_results],
            'sum_error': [r.get('final_metrics', {}).get('sum_error', float('inf')) for r in valid_results],
            'int_dev': [r.get('final_metrics', {}).get('int_dev', float('inf')) for r in valid_results],
            'monotonic_error': [r.get('final_metrics', {}).get('monotonic_error', 0) for r in valid_results],
            'is_magic': [r.get('final_metrics', {}).get('is_magic', False) for r in valid_results],
            'is_monotonic': [r.get('final_metrics', {}).get('is_monotonic', False) for r in valid_results]
        }
        
        # Combined score (lower is better)
        combined_score = [m + s + i/4 + e*2 for m, s, i, e in 
                         zip(metrics['distance'], metrics['sum_error'], metrics['int_dev'], metrics['monotonic_error'])]
        
        # Plot 1: Transition start vs end effectiveness
        plt.subplot(2, 2, 1)
        sc = plt.scatter(params['transition_start'], params['transition_end'], 
                       c=combined_score, cmap='viridis_r', 
                       s=50, alpha=0.7)
        
        # Mark magic squares with stars
        for i, is_magic in enumerate(metrics['is_magic']):
            if is_magic:
                plt.scatter(params['transition_start'][i], params['transition_end'][i], 
                          color='red', s=150, marker='*', edgecolor='black', zorder=10)
        
        plt.colorbar(sc, label='Combined Score (lower is better)')
        plt.title('Transition Start vs End Effectiveness')
        plt.xlabel('Transition Start')
        plt.ylabel('Transition End')
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Learning rate effectiveness
        plt.subplot(2, 2, 2)
        
        # Group by learning rate
        unique_lr = sorted(set(params['learning_rate']))
        lr_scores = [
            [score for lr, score in zip(params['learning_rate'], combined_score) if lr == u_lr]
            for u_lr in unique_lr
        ]
        
        # Box plot
        plt.boxplot(lr_scores, labels=[f"{lr:.3f}" for lr in unique_lr])
        plt.title('Learning Rate Effectiveness')
        plt.xlabel('Learning Rate')
        plt.ylabel('Combined Score (lower is better)')
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Total steps vs transition length
        plt.subplot(2, 2, 3)
        transition_length = [end - start for start, end in 
                           zip(params['transition_start'], params['transition_end'])]
        
        sc = plt.scatter(params['total_steps'], transition_length, 
                       c=combined_score, cmap='viridis_r', 
                       s=50, alpha=0.7)
        
        # Mark magic squares with stars
        for i, is_magic in enumerate(metrics['is_magic']):
            if is_magic:
                plt.scatter(params['total_steps'][i], transition_length[i], 
                          color='red', s=150, marker='*', edgecolor='black', zorder=10)
        
        plt.colorbar(sc, label='Combined Score (lower is better)')
        plt.title('Total Steps vs Transition Length')
        plt.xlabel('Total Steps')
        plt.ylabel('Transition Length')
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Success rate analysis
        plt.subplot(2, 2, 4)
        
        # Calculate success metrics
        top_10_percent = len(valid_results) // 10
        if top_10_percent > 0:
            # Sort by combined score (lower is better)
            sorted_indices = np.argsort(combined_score)
            top_indices = sorted_indices[:top_10_percent]
            
            # Count parameter frequencies in top performers
            param_names = ['transition_start', 'learning_rate', 'swaps']
            param_counts = {}
            
            for param in param_names:
                values = [params[param][i] for i in top_indices]
                unique_vals = sorted(set(values))
                counts = [values.count(val) for val in unique_vals]
                param_counts[param] = (unique_vals, counts)
            
            # Plot one of the parameters (learning rate)
            param = 'learning_rate'
            plt.bar(
                [str(val) for val in param_counts[param][0]], 
                param_counts[param][1],
                color='skyblue'
            )
            plt.title(f'Top {top_10_percent} Performers: {param} Distribution')
            plt.xlabel(param)
            plt.ylabel('Count')
            plt.grid(True, alpha=0.3)
            
            # Add text with other parameter stats
            stats_text = "Parameter frequencies in top performers:\n"
            for p in param_names:
                if p != param:
                    vals, counts = param_counts[p]
                    most_common_idx = np.argmax(counts)
                    most_common = vals[most_common_idx]
                    stats_text += f"{p}: most common = {most_common} ({counts[most_common_idx]} occurrences)\n"
            
            plt.figtext(0.5, 0.02, stats_text, ha='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/parameter_analysis_{self.timestamp}.png")
        plt.close()
        
        print(f"Parameter effectiveness analysis saved to {self.results_dir}/parameter_analysis_{self.timestamp}.png")
        
        # Generate correlation analysis
        self._analyze_parameter_correlations(params, metrics, combined_score)
    
    def _analyze_parameter_correlations(self, params, metrics, combined_score):
        """Analyze correlations between parameters and success metrics."""
        # Skip if insufficient data
        if len(combined_score) < 5:
            return
            
        # Create correlation matrix
        param_names = list(params.keys())
        metric_names = list(metrics.keys())
        
        # Convert to numpy arrays for correlation
        param_values = np.array([params[p] for p in param_names]).T
        metric_values = np.array([
            metrics['distance'], 
            metrics['sum_error'], 
            metrics['int_dev'],
            metrics['monotonic_error'],
            [1 if m else 0 for m in metrics['is_magic']],  # Convert boolean to int
            [1 if m else 0 for m in metrics['is_monotonic']]  # Convert boolean to int
        ]).T
        
        # Add combined score
        metric_values = np.column_stack((metric_values, combined_score))
        metric_names = metric_names + ['combined_score']
        
        # Calculate correlations
        correlations = np.zeros((len(param_names), len(metric_names)))
        
        for i, param in enumerate(param_names):
            for j, metric in enumerate(metric_names):
                if (metric == 'is_magic' and sum(metrics['is_magic']) == 0) or \
                   (metric == 'is_monotonic' and sum(metrics['is_monotonic']) == 0):
                    # Skip if no magic squares or monotonic squares found
                    correlations[i, j] = 0
                else:
                    # Calculate correlation
                    if metric in ['is_magic', 'is_monotonic']:
                        # Point-biserial correlation for binary variable
                        metric_val = [1 if m else 0 for m in metrics[metric]]
                    else:
                        metric_val = metrics[metric] if metric in metrics else combined_score
                    
                    correlations[i, j] = np.corrcoef(params[param], metric_val)[0, 1]
        
        # Plot correlation matrix
        plt.figure(figsize=(10, 8))
        plt.imshow(correlations, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(label='Correlation Coefficient')
        
        # Add labels
        plt.xticks(np.arange(len(metric_names)), metric_names, rotation=45)
        plt.yticks(np.arange(len(param_names)), param_names)
        
        # Add correlation values
        for i in range(len(param_names)):
            for j in range(len(metric_names)):
                plt.text(j, i, f"{correlations[i, j]:.2f}", 
                       ha="center", va="center", 
                       color="white" if abs(correlations[i, j]) > 0.5 else "black")
        
        plt.title('Parameter-Metric Correlations')
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/correlation_analysis_{self.timestamp}.png")
        plt.close()
        
        print(f"Correlation analysis saved to {self.results_dir}/correlation_analysis_{self.timestamp}.png")
        
        # Save correlation data
        correlation_data = {
            'parameters': param_names,
            'metrics': metric_names,
            'correlations': correlations.tolist()
        }
        
        with open(f"{self.results_dir}/correlations_{self.timestamp}.json", 'w') as f:
            json.dump(correlation_data, f, indent=2)
    
    def save_best_configs(self):
        """Save the best configurations for future use."""
        # Skip if no valid results
        valid_results = [r for r in self.all_results if 'error' not in r and 'combined_score' in r]
        if not valid_results:
            return
        
        # Sort by combined score (lower is better)
        sorted_results = sorted(valid_results, key=lambda r: r['combined_score'])
        
        # Get top 10 or all if less than 10
        top_n = min(10, len(sorted_results))
        best_configs = []
        
        for i in range(top_n):
            result = sorted_results[i]
            config = {
                'transition_start': result['config']['transition_start'],
                'transition_end': result['config']['transition_end'],
                'total_steps': result['config']['total_steps'],
                'learning_rate': result['config']['learning_rate'],
                'swaps': result['config']['swaps'],
                'metrics': {
                    'distance': result['final_metrics']['distance'],
                    'sum_error': result['final_metrics']['sum_error'],
                    'int_dev': result['final_metrics']['int_dev'],
                    'monotonic_error': result['final_metrics'].get('monotonic_error', 0),
                    'is_magic': result['final_metrics']['is_magic'],
                    'is_monotonic': result['final_metrics'].get('is_monotonic', False),
                    'combined_score': result['combined_score']
                }
            }
            best_configs.append(config)
        
        # Save to file
        config_file = f"{self.results_dir}/best_configs_{self.timestamp}.json"
        with open(config_file, 'w') as f:
            json.dump(best_configs, f, indent=2)
        
        # Also save to a fixed filename for easy access in future runs
        with open(f"{self.results_dir}/best_configs_latest.json", 'w') as f:
            json.dump(best_configs, f, indent=2)
        
        print(f"Best {top_n} configurations saved to {config_file}")
        
        # Print the best configuration
        best_config = best_configs[0]
        print("\nBest configuration:")
        print(f"  Transition Start: {best_config['transition_start']}")
        print(f"  Transition End: {best_config['transition_end']}")
        print(f"  Total Steps: {best_config['total_steps']}")
        print(f"  Learning Rate: {best_config['learning_rate']}")
        print(f"  Swaps: {best_config['swaps']}")
        print(f"  Combined Score: {best_config['metrics']['combined_score']:.8f}")
        print(f"  Is Magic: {best_config['metrics']['is_magic']}")
        print(f"  Is Monotonic: {best_config['metrics']['is_monotonic']}")
        
        # Update the get_search_config method to use these best configurations
        self._update_search_config_bias(best_configs)

def analyze_magic_square(square, tolerance=1e-10):
    """Analyze properties of a magic square."""
    if not isinstance(square, np.ndarray):
        square = np.array(square)
    
    n = square.shape[0]
    
    # Check if square is magic
    target_sum = np.sum(square) / n
    
    # Check rows
    row_sums = np.sum(square, axis=1)
    row_magic = all(abs(s - target_sum) < tolerance for s in row_sums)
    
    # Check columns
    col_sums = np.sum(square, axis=0)
    col_magic = all(abs(s - target_sum) < tolerance for s in col_sums)
    
    # Check main diagonal
    main_diag_sum = np.trace(square)
    main_diag_magic = abs(main_diag_sum - target_sum) < tolerance
    
    # Check anti-diagonal
    anti_diag_sum = np.trace(np.fliplr(square))
    anti_diag_magic = abs(anti_diag_sum - target_sum) < tolerance
    
    # Check if it's a proper magic square
    is_magic = row_magic and col_magic and main_diag_magic and anti_diag_magic
    
    # Check if it contains distinct integers
    is_distinct = len(np.unique(square)) == n*n
    
    # Check if it's in normal form (smallest values in top-left)
    is_normal_form = square[0, 0] == np.min(square)
    
    return {
        'is_magic': is_magic,
        'row_magic': row_magic,
        'col_magic': col_magic,
        'main_diag_magic': main_diag_magic,
        'anti_diag_magic': anti_diag_magic,
        'target_sum': target_sum,
        'row_sums': row_sums.tolist(),
        'col_sums': col_sums.tolist(),
        'main_diag_sum': main_diag_sum,
        'anti_diag_sum': anti_diag_sum,
        'is_distinct': is_distinct,
        'is_normal_form': is_normal_form,
        'min_value': np.min(square),
        'max_value': np.max(square),
        'size': n
    }

if __name__ == "__main__":
    print("Parallel Multi-Starting Point Search for Magic Squares")
    print("=====================================================")
    
    # Get command line arguments for number of instances and workers
    import argparse
    parser = argparse.ArgumentParser(description='Run parallel search for magic squares')
    parser.add_argument('--instances', type=int, default=30, 
                       help='Number of search instances to run')
    parser.add_argument('--workers', type=int, default=4, 
                       help='Number of parallel workers')
    parser.add_argument('--extended', action='store_true',
                       help='Run extended search with more instances and broader parameter space')
    args = parser.parse_args()
    
    # Initialize search manager
    search_manager = ParallelMagicSquareSearch()
    
    # Adjust instances for extended search
    num_instances = args.instances
    if args.extended:
        num_instances = max(50, num_instances)
        print(f"Running extended search with {num_instances} instances")
    
    # Run parallel search
    magic_squares, best_near_magic = search_manager.run_parallel_search(
        num_instances=num_instances,
        max_workers=args.workers
    )
    
    # Display results
    if magic_squares:
        print(f"\nFound {len(magic_squares)} standard magic squares!")
        for i, result in enumerate(magic_squares):
            print(f"\nMagic Square {i+1}:")
            square = np.array(result['final_square'])
            print(square)
            
            # Analyze properties
            analysis = analyze_magic_square(square)
            print(f"Magic Sum: {analysis['target_sum']}")
            print(f"Is Distinct: {analysis['is_distinct']}")
            print(f"Min Value: {analysis['min_value']}, Max Value: {analysis['max_value']}")
            print(f"Is Monotonic 1-16: {result['final_metrics']['is_monotonic']}")
            
            # Save detailed information about this magic square
            square_file = f"{search_manager.results_dir}/magic_square_{i+1}_{search_manager.timestamp}.txt"
            with open(square_file, 'w') as f:
                f.write(f"Magic Square {i+1}:\n")
                f.write(f"{square}\n\n")
                f.write(f"Magic Sum: {analysis['target_sum']}\n")
                f.write(f"Is Distinct: {analysis['is_distinct']}\n")
                f.write(f"Min Value: {analysis['min_value']}, Max Value: {analysis['max_value']}\n")
                f.write(f"Is Monotonic 1-16: {result['final_metrics']['is_monotonic']}\n\n")
                f.write("Configuration:\n")
                for k, v in result['config'].items():
                    if k != 'search_id':
                        f.write(f"  {k}: {v}\n")
                f.write("\nMetrics:\n")
                for k, v in result['final_metrics'].items():
                    f.write(f"  {k}: {v}\n")
            
            print(f"Details saved to {square_file}")
    else:
        print("\nNo exact magic squares found.")
        if best_near_magic:
            print("\nBest near-magic square:")
            square = np.array(best_near_magic['final_square'])
            print(square)
            
            # Analyze properties
            analysis = analyze_magic_square(square)
            print(f"Magic Sum: {analysis['target_sum']}")
            print(f"Distance: {best_near_magic['final_metrics']['distance']:.8f}")
            print(f"Sum Error: {best_near_magic['final_metrics']['sum_error']:.8f}")
            print(f"Integer Deviation: {best_near_magic['final_metrics']['int_dev']:.8f}")
            print(f"Monotonic Error: {best_near_magic['final_metrics'].get('monotonic_error', 0):.8f}")
            print(f"Is Monotonic 1-16: {best_near_magic['final_metrics'].get('is_monotonic', False)}")
            
            # Save near-magic square
            square_file = f"{search_manager.results_dir}/near_magic_square_{search_manager.timestamp}.txt"
            with open(square_file, 'w') as f:
                f.write("Best Near-Magic Square:\n")
                f.write(f"{square}\n\n")
                f.write(f"Magic Sum: {analysis['target_sum']}\n")
                f.write(f"Distance: {best_near_magic['final_metrics']['distance']:.8f}\n")
                f.write(f"Sum Error: {best_near_magic['final_metrics']['sum_error']:.8f}\n")
                f.write(f"Integer Deviation: {best_near_magic['final_metrics']['int_dev']:.8f}\n")
                f.write(f"Monotonic Error: {best_near_magic['final_metrics'].get('monotonic_error', 0):.8f}\n")
                f.write(f"Is Monotonic 1-16: {best_near_magic['final_metrics'].get('is_monotonic', False)}\n\n")
                f.write("Configuration:\n")
                for k, v in best_near_magic['config'].items():
                    if k != 'search_id':
                        f.write(f"  {k}: {v}\n")
            
            print(f"Details saved to {square_file}")
        else:
            print("No near-magic square found either.")
    
    print("\nSearch complete. Check the results directory for detailed information and visualizations.")