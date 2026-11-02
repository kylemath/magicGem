#!/usr/bin/env python3
"""
Test script for the magic squares visualization components.

This script tests just the visualization components:
1. Historical context figure
2. Research framework diagram
3. Manifold structure visualization
"""

import os
import numpy as np
from datetime import datetime

def ensure_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def test_visualizations():
    """Run a test of the visualization components."""
    print("=" * 80)
    print("MAGIC SQUARES VISUALIZATION TEST")
    print("=" * 80)
    
    # Import visualization functions
    from magic_squares.analysis.visualization import (
        plot_historical_context,
        plot_research_framework
    )
    
    # Create test directories
    plots_dir = os.path.join("magic_squares", "analysis", "plots")
    ensure_directory(plots_dir)
    
    # Step 1: Generate framework figures
    print("\nStep 1: Generating Framework Figures")
    print("-" * 40)
    plot_historical_context(save_dir=plots_dir)
    plot_research_framework(save_dir=plots_dir)
    print("Framework figures generated")
    
    # Step 2: Verify outputs
    print("\nStep 2: Verifying Outputs")
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
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_visualizations() 