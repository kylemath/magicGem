#!/usr/bin/env python3
"""
Test script for the magic squares analysis pipeline.

This script tests the core components of the analysis pipeline:
1. Generate a small set of magic squares
2. Run geometric analysis
3. Run EMD analysis
4. Run manifold analysis
5. Run predictive modeling
6. Generate visualizations
"""

import os
import numpy as np
from datetime import datetime

from magic_squares.generation.gen import generate_magic_squares
from magic_squares.analysis.analyze import run_geometric_analysis, run_emd_analysis, run_manifold_analysis
from magic_squares.analysis.visualization import (
    plot_historical_context,
    plot_research_framework,
    plot_manifold_structure,
    compute_persistence_diagram
)
from magic_squares.analysis.predictive_modeling import build_predictive_models, evaluate_model_performance

def ensure_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def test_pipeline():
    """Run a test of the analysis pipeline."""
    print("=" * 80)
    print("MAGIC SQUARES ANALYSIS PIPELINE TEST")
    print("=" * 80)
    
    # Create test directories
    plots_dir = os.path.join("magic_squares", "analysis", "plots")
    ensure_directory(plots_dir)
    
    # Step 1: Generate a small set of magic squares
    print("\nStep 1: Generating Magic Squares")
    print("-" * 40)
    squares = generate_magic_squares(4)  # Generate 4x4 magic squares
    # Limit to 10 squares for testing
    if len(squares) > 10:
        squares = squares[:10]
    print(f"Generated {len(squares)} magic squares")
    
    # Step 2: Generate framework figures
    print("\nStep 2: Generating Framework Figures")
    print("-" * 40)
    plot_historical_context(save_dir=plots_dir)
    plot_research_framework(save_dir=plots_dir)
    print("Framework figures generated")
    
    # Step 3: Run geometric analysis
    print("\nStep 3: Running Geometric Analysis")
    print("-" * 40)
    geometric_results = run_geometric_analysis(squares)
    print("Geometric analysis completed")
    
    # Step 4: Run EMD analysis
    print("\nStep 4: Running EMD Analysis")
    print("-" * 40)
    emd_results = run_emd_analysis(squares)
    print("EMD analysis completed")
    
    # Step 5: Run manifold analysis
    print("\nStep 5: Running Manifold Analysis")
    print("-" * 40)
    manifold_results = run_manifold_analysis(squares)
    
    # Generate manifold structure plots
    persistence_data = compute_persistence_diagram(squares)
    manifold_results['persistence_birth'] = persistence_data['birth']
    manifold_results['persistence_death'] = persistence_data['death']
    
    plot_manifold_structure(squares, manifold_results, save_dir=plots_dir)
    print("Manifold analysis completed")
    
    # Step 6: Run predictive modeling
    print("\nStep 6: Running Predictive Modeling")
    print("-" * 40)
    model_results = build_predictive_models(geometric_results['geometric_df'])
    performance_summary = evaluate_model_performance(model_results, save_dir=plots_dir)
    print("Predictive modeling completed")
    
    # Step 7: Verify outputs
    print("\nStep 7: Verifying Outputs")
    print("-" * 40)
    
    # Check for framework figures
    framework_files = [
        os.path.join(plots_dir, "historical_context.png"),
        os.path.join(plots_dir, "research_framework.png")
    ]
    
    for file in framework_files:
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
    
    # Check for geometric analysis outputs
    if 'geometric_df' in geometric_results:
        print(f"✓ Geometric dataframe exists with {len(geometric_results['geometric_df'])} rows")
    else:
        print("✗ Geometric dataframe missing")
    
    # Check for EMD analysis outputs
    if 'distance_matrix' in emd_results:
        print(f"✓ EMD distance matrix exists with shape {emd_results['distance_matrix'].shape}")
    else:
        print("✗ EMD distance matrix missing")
    
    # Check for manifold analysis outputs
    if 'structure_plot' in manifold_results:
        print(f"✓ Manifold structure plot exists at {manifold_results['structure_plot']}")
    else:
        print("✗ Manifold structure plot missing")
    
    # Check for predictive modeling outputs
    if 'performance_summary' in locals() and performance_summary:
        print(f"✓ Predictive modeling performance summary exists")
    else:
        print("✗ Predictive modeling performance summary missing")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_pipeline() 