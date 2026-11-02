#!/usr/bin/env python3
"""
Magic Squares Analysis Pipeline Runner

This script runs the complete magic squares analysis pipeline, including:
1. Generation of standard and most-perfect magic squares
2. Geometric analysis
3. EMD analysis
4. Manifold analysis
5. Report generation

Usage:
    python run_analysis.py [--generate] [--most-perfect] [--analysis ANALYSIS] [--skip-existing] [--no-report]

Options:
    --generate       Generate new magic squares (otherwise uses existing data)
    --most-perfect   Include analysis of most-perfect magic squares
    --analysis       Specify which analysis to run (options: all, geometric, emd, manifold)
    --skip-existing  Skip steps that have already been computed
    --no-report      Skip report generation
"""

import os
import sys
import argparse
import time
import pickle
from datetime import datetime

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the magic squares analysis pipeline")
    parser.add_argument("--generate", action="store_true", 
                        help="Generate new magic squares (otherwise uses existing data)")
    parser.add_argument("--most-perfect", action="store_true",
                        help="Include analysis of most-perfect magic squares")
    parser.add_argument("--analysis", type=str, default="all",
                        choices=["all", "geometric", "emd", "manifold"],
                        help="Specify which analysis to run")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip steps that have already been computed")
    parser.add_argument("--no-report", action="store_true",
                        help="Skip report generation")
    args = parser.parse_args()
    
    start_time = time.time()
    
    # Print header
    print("="*80)
    print(f"Magic Squares Analysis Pipeline - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Import necessary modules
    from magic_squares.analysis.core import load_latest_squares
    
    # Check if we need to generate new squares or use existing ones
    if args.generate:
        print("\nGenerating magic squares...")
        from magic_squares.generation.gen import generate_magic_squares
        
        # Generate 4x4 magic squares
        squares = generate_magic_squares(n_squares=880, order=4)
        print(f"Generated {len(squares)} magic squares")
    else:
        # Try to load existing squares
        print("\nLoading existing magic squares...")
        try:
            squares = load_latest_squares()
            if squares is not None and len(squares) > 0:
                print(f"Loaded {len(squares)} magic squares successfully")
            else:
                print("No existing magic squares found. Use --generate to create new ones.")
                return 1
        except Exception as e:
            print(f"Error loading existing magic squares: {e}")
            print("Use --generate to create new ones.")
            return 1
    
    # Handle most-perfect magic squares if requested
    most_perfect_squares = None
    if args.most_perfect:
        print("\nProcessing most-perfect magic squares...")
        try:
            from magic_squares.generation.most_perfect import generate_all_most_perfect_squares
            most_perfect_squares = generate_all_most_perfect_squares()
            print(f"Generated {len(most_perfect_squares)} most-perfect magic squares")
        except Exception as e:
            print(f"Error generating most-perfect magic squares: {e}")
            print("Continuing with standard magic squares only.")
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join("magic_squares", "analysis", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Run the analysis pipeline
    print(f"\nRunning analysis pipeline (mode: {args.analysis})...")
    
    # Initialize results dictionary
    results = {}
    
    # Import appropriate analysis functions based on requested analysis
    if args.analysis == "all":
        from magic_squares.analysis.analyze import run_analysis_pipeline
        
        # Check if we should skip existing results
        if args.skip_existing:
            results_file = os.path.join(results_dir, "all_results.pkl")
            if os.path.exists(results_file):
                print(f"Loading existing results from {results_file}")
                with open(results_file, 'rb') as f:
                    results = pickle.load(f)
                print("Existing results loaded successfully")
            else:
                # Pass most-perfect squares to the analysis pipeline if available
                if most_perfect_squares is not None:
                    results = run_analysis_pipeline(squares, most_perfect_squares=most_perfect_squares)
                else:
                    results = run_analysis_pipeline(squares)
                
                # Save results
                with open(results_file, 'wb') as f:
                    pickle.dump(results, f)
                print(f"Results saved to {results_file}")
        else:
            # Pass most-perfect squares to the analysis pipeline if available
            if most_perfect_squares is not None:
                results = run_analysis_pipeline(squares, most_perfect_squares=most_perfect_squares)
            else:
                results = run_analysis_pipeline(squares)
            
            # Save results
            results_file = os.path.join(results_dir, "all_results.pkl")
            with open(results_file, 'wb') as f:
                pickle.dump(results, f)
            print(f"Results saved to {results_file}")
    else:
        # Handle specific analysis types
        results_file = os.path.join(results_dir, f"{args.analysis}_results.pkl")
        
        # Check if we should skip existing results
        if args.skip_existing and os.path.exists(results_file):
            print(f"Loading existing results from {results_file}")
            with open(results_file, 'rb') as f:
                results = pickle.load(f)
            print("Existing results loaded successfully")
        else:
            # Import specific analysis modules
            if args.analysis == "geometric":
                from magic_squares.analysis.analyze import run_geometric_analysis
                results = run_geometric_analysis(squares)
            elif args.analysis == "emd":
                from magic_squares.analysis.analyze import run_emd_analysis
                results = run_emd_analysis(squares)
            elif args.analysis == "manifold":
                from magic_squares.analysis.analyze import run_manifold_analysis
                results = run_manifold_analysis(squares)
            
            # Add most-perfect analysis if requested
            if most_perfect_squares is not None and args.analysis == "geometric":
                from magic_squares.analysis.analyze import run_most_perfect_analysis
                most_perfect_results = run_most_perfect_analysis(squares)
                # Merge results
                results.update(most_perfect_results)
            
            # Save results
            with open(results_file, 'wb') as f:
                pickle.dump(results, f)
            print(f"Results saved to {results_file}")
    
    if results is None or len(results) == 0:
        print("\nAnalysis failed or produced no results. Please check the error messages above.")
        return 1
    
    # Generate report if not skipped
    if not args.no_report:
        print("\nGenerating report...")
        from magic_squares.analysis.report_generator import generate_report
        
        report_dir = generate_report(results)
        
        # Print summary with report information
        elapsed_time = time.time() - start_time
        print("\n" + "="*80)
        print(f"Analysis completed in {elapsed_time:.2f} seconds")
        print(f"Report generated in: {report_dir}")
        print("="*80)
    else:
        # Print summary without report information
        elapsed_time = time.time() - start_time
        print("\n" + "="*80)
        print(f"Analysis completed in {elapsed_time:.2f} seconds")
        print(f"Report generation skipped")
        print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 