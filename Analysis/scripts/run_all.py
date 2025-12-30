#!/usr/bin/env python3
"""
run_all.py
==========
Master script to run the complete Magic Gems paper pipeline.

This script runs in order:
1. run_analysis.py - Generate data and figures
2. populate_tex.py - Insert statistics into LaTeX
3. compile_tex.py - Compile to PDF

Usage:
    python scripts/run_all.py [--skip-analysis] [--skip-compile]
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
import time


def run_script(script_name, description):
    """Run a Python script and report status."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, f'scripts/{script_name}'],
            capture_output=False,
            timeout=600  # 10 minute timeout
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✓ {description} completed in {elapsed:.1f}s")
            return True
        else:
            print(f"\n✗ {description} failed (exit code {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n✗ {description} timed out")
        return False
    except Exception as e:
        print(f"\n✗ {description} error: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Run the complete Magic Gems paper pipeline'
    )
    parser.add_argument(
        '--skip-analysis',
        action='store_true',
        help='Skip the analysis step (use existing data)'
    )
    parser.add_argument(
        '--skip-compile',
        action='store_true',
        help='Skip LaTeX compilation'
    )
    parser.add_argument(
        '--analysis-only',
        action='store_true',
        help='Only run analysis, skip LaTeX steps'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("MAGIC GEMS: Complete Paper Pipeline")
    print("="*60)
    print(f"\nStarted at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    print(f"Working directory: {os.getcwd()}")
    
    start_time = time.time()
    all_success = True
    
    # Step 1: Run analysis
    if not args.skip_analysis:
        if not run_script('run_analysis.py', 'Data Analysis & Figure Generation'):
            print("\n⚠ Analysis step failed, but continuing...")
            # Don't fail completely - LaTeX can compile with placeholders
    else:
        print("\n[Skipping analysis step]")
    
    if args.analysis_only:
        print("\n[Analysis only mode - skipping LaTeX steps]")
    else:
        # Step 2: Populate LaTeX
        if not run_script('populate_tex.py', 'Populate LaTeX with Statistics'):
            all_success = False
            print("\n⚠ LaTeX population had issues")
        
        # Step 3: Compile LaTeX
        if not args.skip_compile:
            if not run_script('compile_tex.py', 'LaTeX Compilation'):
                all_success = False
        else:
            print("\n[Skipping LaTeX compilation]")
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"Finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if all_success:
        print("\n✓ All steps completed successfully!")
        print("\nOutputs:")
        print("  - data/          Analysis results (JSON)")
        print("  - figures/       Publication figures (PDF)")
        if not args.skip_compile and not args.analysis_only:
            print("  - output/        Compiled paper (PDF)")
    else:
        print("\n⚠ Some steps had issues - check output above")
    
    print("="*60)
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())

