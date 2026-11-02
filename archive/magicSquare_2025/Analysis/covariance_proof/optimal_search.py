#!/usr/bin/env python3
"""
Optimal Parameter Search for Magic Squares

This script implements a focused search using the best parameters identified
from previous parallel searches to maximize the chance of finding magic squares.
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
from parallel_search import analyze_magic_square

class OptimalParameterSearch:
    """Class to manage focused search with optimal parameters."""
    
    def __init__(self, results_dir='covariance_proof/optimal_results'):
        """Initialize search manager."""
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Track all results
        self.all_results = []
        self.magic_squares = []
        self.best_near_magic = None
        
        # Timestamp for this search session
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Load best configurations from previous searches
        self.best_configs = self._load_best_configs()
        
    def _load_best_configs(self):
        """Load best configurations from previous searches."""
        config_file = "covariance_proof/parallel_results/best_configs_latest.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    configs = json.load(f)
                print(f"Loaded {len(configs)} best configurations from previous searches")
                return configs
            except Exception as e:
                print(f"Error loading configurations: {str(e)}")
        
        # Default configurations if file not found
        return [
            {
                "transition_start": 150,
                "transition_end": 275,
                "total_steps": 325,
                "learning_rate": 0.15,
                "swaps": 2
            },
            {
                "transition_start": 75,
                "transition_end": 125,
                "total_steps": 250,
                "learning_rate": 0.1,
                "swaps": 1
            },
            {
                "transition_start": 175,
                "transition_end": 275,
                "total_steps": 350,
                "learning_rate": 0.075,
                "swaps": 3
            }
        ]
    
    def get_optimal_configs(self, num_instances):
        """Generate optimal configurations for search instances."""
        configs = []
        
        # Use the top configurations directly
        top_configs = min(len(self.best_configs), 5)  # Use up to top 5 configs
        
        # Calculate how many instances to allocate to each strategy
        direct_use = int(num_instances * 0.4)  # 40% direct use of best configs
        small_variation = int(num_instances * 0.4)  # 40% small variations
        exploration = num_instances - direct_use - small_variation  # 20% exploration
        
        # 1. Direct use of best configurations
        for i in range(direct_use):
            # Cycle through top configs
            base_config = self.best_configs[i % top_configs]
            config = base_config.copy()
            if isinstance(config, dict) and 'metrics' in config:
                config.pop('metrics', None)  # Remove metrics if present
            config['search_id'] = i
            config['strategy'] = 'direct'
            configs.append(config)
        
        # 2. Small variations of best configurations
        for i in range(small_variation):
            base_config = self.best_configs[i % top_configs]
            
            # Extract base parameters
            if isinstance(base_config, dict) and 'metrics' in base_config:
                base_params = {k: v for k, v in base_config.items() if k != 'metrics'}
            else:
                base_params = base_config.copy()
            
            # Apply small variations
            variation_type = i % 4
            if variation_type == 0:
                # Vary transition start
                base_params['transition_start'] = max(50, base_params['transition_start'] + 
                                                   random.choice([-25, -10, 10, 25]))
            elif variation_type == 1:
                # Vary transition end
                base_params['transition_end'] = max(base_params['transition_start'] + 50, 
                                                 base_params['transition_end'] + 
                                                 random.choice([-25, -10, 10, 25]))
            elif variation_type == 2:
                # Vary learning rate
                base_params['learning_rate'] = max(0.05, min(0.2, base_params['learning_rate'] * 
                                                         random.uniform(0.8, 1.2)))
            else:
                # Vary swaps
                base_params['swaps'] = max(1, min(5, base_params['swaps'] + 
                                              random.choice([-1, 0, 1])))
            
            # Ensure total_steps is sufficient
            base_params['total_steps'] = max(base_params['total_steps'], 
                                          base_params['transition_end'] + 50)
            
            base_params['search_id'] = direct_use + i
            base_params['strategy'] = 'variation'
            configs.append(base_params)
        
        # 3. Exploration of promising parameter space
        for i in range(exploration):
            # Define optimal ranges based on our findings
            transition_start_range = [75, 100, 125, 150, 175]
            transition_length_range = [75, 100, 125, 150]
            total_steps_range = [250, 300, 325, 350, 375]
            learning_rate_range = [0.075, 0.1, 0.125, 0.15, 0.175]
            swaps_range = [1, 2, 3]
            
            # Randomly select parameters from optimal ranges
            transition_start = random.choice(transition_start_range)
            transition_length = random.choice(transition_length_range)
            transition_end = transition_start + transition_length
            total_steps = max(transition_end + 50, random.choice(total_steps_range))
            learning_rate = random.choice(learning_rate_range)
            swaps = random.choice(swaps_range)
            
            config = {
                'transition_start': transition_start,
                'transition_end': transition_end,
                'total_steps': total_steps,
                'learning_rate': learning_rate,
                'swaps': swaps,
                'search_id': direct_use + small_variation + i,
                'strategy': 'exploration'
            }
            configs.append(config)
        
        return configs
    
    def run_search_instance(self, config):
        """Run a single search instance with the given configuration."""
        try:
            print(f"\nRunning search instance {config['search_id']} (Strategy: {config['strategy']}):")
            print(f"Parameters: Start={config['transition_start']}, End={config['transition_end']}, "
                 f"Steps={config['total_steps']}, LR={config['learning_rate']}, Swaps={config['swaps']}")
            
            # Run the experiment with verbose=False to reduce output clutter
            result = run_experiment(
                transition_start=config['transition_start'],
                transition_end=config['transition_end'],
                total_steps=config['total_steps'],
                learning_rate=config['learning_rate'],
                swaps=config['swaps'],
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
                    'is_magic': False
                }
            }
    
    def run_optimal_search(self, num_instances=30, max_workers=4):
        """Run multiple search instances with optimal parameters."""
        print(f"Starting optimal parameter search with {num_instances} instances using {max_workers} workers")
        start_time = time.time()
        
        # Generate optimal configurations
        configs = self.get_optimal_configs(num_instances)
        
        # Run searches in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.run_search_instance, configs))
        
        # Process results
        self.all_results = results
        self.magic_squares = [r for r in results if r.get('final_metrics', {}).get('is_magic', False)]
        
        # Find best near-magic square if no exact solutions found
        if not self.magic_squares:
            # Sort by a combined metric (prioritize low distance, sum error, and integer deviation)
            valid_results = [r for r in results if 'error' not in r]
            if valid_results:
                self.best_near_magic = min(
                    valid_results, 
                    key=lambda r: (
                        r['final_metrics']['distance'] + 
                        r['final_metrics']['sum_error'] + 
                        r['final_metrics']['int_dev'] / 4  # Lower weight on integer deviation
                    )
                )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Print summary
        print(f"\nOptimal search completed in {elapsed:.2f} seconds")
        print(f"Found {len(self.magic_squares)} exact magic squares")
        
        # Analyze results by strategy
        self._analyze_results_by_strategy()
        
        # Save results
        self.save_results()
        
        return self.magic_squares, self.best_near_magic
    
    def _analyze_results_by_strategy(self):
        """Analyze results by strategy type."""
        strategies = {}
        
        for result in self.all_results:
            if 'error' in result:
                continue
                
            strategy = result['config'].get('strategy', 'unknown')
            if strategy not in strategies:
                strategies[strategy] = {
                    'count': 0,
                    'magic_count': 0,
                    'avg_distance': 0,
                    'avg_sum_error': 0,
                    'avg_int_dev': 0
                }
            
            strategies[strategy]['count'] += 1
            if result['final_metrics'].get('is_magic', False):
                strategies[strategy]['magic_count'] += 1
            
            strategies[strategy]['avg_distance'] += result['final_metrics']['distance']
            strategies[strategy]['avg_sum_error'] += result['final_metrics']['sum_error']
            strategies[strategy]['avg_int_dev'] += result['final_metrics']['int_dev']
        
        # Calculate averages
        for strategy, data in strategies.items():
            if data['count'] > 0:
                data['avg_distance'] /= data['count']
                data['avg_sum_error'] /= data['count']
                data['avg_int_dev'] /= data['count']
                data['success_rate'] = data['magic_count'] / data['count'] * 100
        
        # Print results
        print("\nResults by Strategy:")
        print("===================")
        for strategy, data in strategies.items():
            print(f"\nStrategy: {strategy}")
            print(f"  Total runs: {data['count']}")
            print(f"  Magic squares found: {data['magic_count']}")
            print(f"  Success rate: {data['success_rate']:.1f}%")
            print(f"  Avg distance: {data['avg_distance']:.6f}")
            print(f"  Avg sum error: {data['avg_sum_error']:.6f}")
            print(f"  Avg integer deviation: {data['avg_int_dev']:.6f}")
        
        # Save strategy analysis
        self.strategy_analysis = strategies
    
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
        
        # Save strategy analysis
        strategy_file = f"{self.results_dir}/strategy_analysis_{self.timestamp}.json"
        with open(strategy_file, 'w') as f:
            json.dump(self.strategy_analysis, f, indent=2)
        
        print(f"Results saved to {results_file}")
        print(f"Strategy analysis saved to {strategy_file}")
        
        # Save magic squares
        if self.magic_squares:
            for i, result in enumerate(self.magic_squares):
                square = np.array(result['final_square'])
                
                # Analyze properties
                analysis = analyze_magic_square(square)
                
                # Save detailed information about this magic square
                square_file = f"{self.results_dir}/magic_square_{i+1}_{self.timestamp}.txt"
                with open(square_file, 'w') as f:
                    f.write(f"Magic Square {i+1}:\n")
                    f.write(str(square) + "\n\n")
                    f.write(f"Configuration:\n")
                    for k, v in result['config'].items():
                        f.write(f"  {k}: {v}\n")
                    f.write("\nProperties:\n")
                    for k, v in analysis.items():
                        f.write(f"  {k}: {v}\n")
                
                print(f"Detailed information saved to {square_file}")

if __name__ == "__main__":
    print("Optimal Parameter Search for Magic Squares")
    print("=========================================")
    
    # Get command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Run optimal parameter search for magic squares')
    parser.add_argument('--instances', type=int, default=30, 
                       help='Number of search instances to run')
    parser.add_argument('--workers', type=int, default=4, 
                       help='Number of parallel workers')
    args = parser.parse_args()
    
    # Initialize search manager
    search_manager = OptimalParameterSearch()
    
    # Run optimal search
    magic_squares, best_near_magic = search_manager.run_optimal_search(
        num_instances=args.instances,
        max_workers=args.workers
    )
    
    # Display results
    if magic_squares:
        print(f"\nFound {len(magic_squares)} magic squares!")
        for i, result in enumerate(magic_squares):
            print(f"\nMagic Square {i+1}:")
            square = np.array(result['final_square'])
            print(square)
            
            # Analyze properties
            analysis = analyze_magic_square(square)
            print(f"Magic Sum: {analysis['target_sum']}")
            print(f"Is Distinct: {analysis['is_distinct']}")
            print(f"Min Value: {analysis['min_value']}, Max Value: {analysis['max_value']}")
            print(f"Strategy: {result['config']['strategy']}")
    else:
        print("\nNo exact magic squares found.")
        
        if best_near_magic:
            print("\nBest near-magic square:")
            print(best_near_magic['final_square'])
            print(f"Distance: {best_near_magic['final_metrics']['distance']:.8f}")
            print(f"Sum Error: {best_near_magic['final_metrics']['sum_error']:.8f}")
            print(f"Integer Deviation: {best_near_magic['final_metrics']['int_dev']:.8f}")
            
            # Configuration that produced this result
            print("\nConfiguration:")
            for k, v in best_near_magic['config'].items():
                print(f"  {k}: {v}")
    
    print("\nSearch complete. Check the results directory for detailed information.") 