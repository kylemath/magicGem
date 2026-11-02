#!/usr/bin/env python3
"""
Magic Squares: Complete Reproduction Script
============================================

This script reproduces ALL results from the paper:
"From Discrete Constraints to Continuous Geometry"

It runs in stages, each of which can be run independently:
1. Setup & Data Loading
2. Hero Figures (Magic Gems visualization)
3. Alternative Hypothesis Testing (300k samples)
4. Comprehensive Geometric Analysis
5. Benchmark Comparison
6. LaTeX Compilation

Usage:
    python reproduce_all.py              # Run all stages
    python reproduce_all.py --stage 2    # Run specific stage
    python reproduce_all.py --quick      # Quick mode (fewer samples)

Author: Kyle Elliott Mathewson, University of Alberta
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path

# Ensure we're in the right directory
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

# Add src to path
sys.path.insert(0, str(SCRIPT_DIR / 'src'))


def print_header(title):
    """Print a formatted header."""
    width = 70
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)
    print()


def print_stage(num, title):
    """Print a stage header."""
    print()
    print(f"[Stage {num}] {title}")
    print("-" * 50)


def run_stage_1():
    """Stage 1: Setup & Data Loading"""
    print_stage(1, "Setup & Data Loading")
    
    import json
    import numpy as np
    
    # Load magic squares
    json_path = SCRIPT_DIR / 'web/assets/data/unique_squares.json'
    if json_path.exists():
        with open(json_path, 'r') as f:
            data = json.load(f)
            if isinstance(data[0], dict):
                squares = [np.array(s['values']).reshape(4, 4) for s in data]
            else:
                squares = [np.array(s) for s in data]
        print(f"  ✓ Loaded {len(squares)} magic squares from JSON")
    else:
        print(f"  ✗ JSON file not found: {json_path}")
        return None
    
    # Verify magic property
    n_valid = 0
    for sq in squares:
        target = 34
        if (np.all(np.sum(sq, axis=0) == target) and 
            np.all(np.sum(sq, axis=1) == target) and
            np.trace(sq) == target and 
            np.trace(np.fliplr(sq)) == target):
            n_valid += 1
    
    print(f"  ✓ Verified {n_valid}/{len(squares)} are valid magic squares")
    
    return squares


def run_stage_2():
    """Stage 2: Hero Figures"""
    print_stage(2, "Hero Figures (Magic Gems Visualization)")
    
    from src.create_hero_figures import (
        create_hero_figure,
        create_magic_vs_random_figure,
        create_physical_intuition_figure,
        create_21_configurations_gallery
    )
    
    output_dir = SCRIPT_DIR / 'paper/figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("  Creating hero figure (4-panel transformation)...")
    create_hero_figure(save_path=str(output_dir / 'hero_figure.png'))
    
    print("  Creating magic vs random comparison...")
    create_magic_vs_random_figure(save_path=str(output_dir / 'magic_vs_random.png'))
    
    print("  Creating physical intuition figure...")
    create_physical_intuition_figure(save_path=str(output_dir / 'physical_intuition.png'))
    
    print("  Creating 21 configurations gallery...")
    try:
        create_21_configurations_gallery(save_path=str(output_dir / 'configurations_gallery.png'))
    except Exception as e:
        print(f"    Warning: {e}")
    
    print("  ✓ Hero figures complete")


def run_stage_3(quick=False):
    """Stage 3: Alternative Hypothesis Testing"""
    print_stage(3, "Alternative Hypothesis Testing")
    
    from src.alternative_hypotheses import run_alternative_hypothesis_analysis
    
    n_samples = 10000 if quick else 100000
    print(f"  Generating {n_samples:,} samples per category...")
    print("  (This may take a few minutes...)")
    
    run_alternative_hypothesis_analysis(
        n_random=n_samples,
        n_one_swap=n_samples,
        n_two_swap=n_samples,
        output_dir='paper/figures'
    )
    
    print("  ✓ Alternative hypothesis testing complete")


def run_stage_4():
    """Stage 4: Comprehensive Geometric Analysis"""
    print_stage(4, "Comprehensive Geometric Analysis")
    
    try:
        from src.analysis_integrated import run_full_analysis
        import json
        
        # Load squares
        with open('web/assets/data/unique_squares.json', 'r') as f:
            data = json.load(f)
        import numpy as np
        if isinstance(data[0], dict):
            squares = [np.array(s['values']).reshape(4, 4) for s in data]
        else:
            squares = [np.array(s) for s in data]
        
        run_full_analysis(squares, output_dir='paper/figures')
        print("  ✓ Geometric analysis complete")
    except Exception as e:
        print(f"  Warning: Analysis pipeline error: {e}")
        print("  Continuing with available modules...")


def run_stage_5():
    """Stage 5: Benchmark Comparison"""
    print_stage(5, "Benchmark Comparison")
    
    try:
        from src.benchmark import MagicSquareBenchmark
        import os
        
        print("  Running benchmarks (this may take a minute)...")
        benchmark = MagicSquareBenchmark(n=4, num_trials=10)
        benchmark.run_benchmark()
        
        os.makedirs('results/benchmark', exist_ok=True)
        benchmark.save_results('results/benchmark')
        
        print("  ✓ Benchmark complete")
    except Exception as e:
        print(f"  Warning: Benchmark error: {e}")


def run_stage_6():
    """Stage 6: LaTeX Compilation"""
    print_stage(6, "LaTeX Compilation")
    
    paper_dir = SCRIPT_DIR / 'paper'
    
    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ✗ pdflatex not found. Please install LaTeX to compile the paper.")
        return
    
    print("  Running pdflatex (pass 1)...")
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
        cwd=paper_dir, capture_output=True
    )
    
    print("  Running bibtex...")
    subprocess.run(
        ['bibtex', 'main'],
        cwd=paper_dir, capture_output=True
    )
    
    print("  Running pdflatex (pass 2)...")
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
        cwd=paper_dir, capture_output=True
    )
    
    print("  Running pdflatex (pass 3)...")
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
        cwd=paper_dir, capture_output=True
    )
    
    # Check if PDF was created
    pdf_path = paper_dir / 'main.pdf'
    if pdf_path.exists():
        size_mb = pdf_path.stat().st_size / 1024 / 1024
        print(f"  ✓ PDF generated: main.pdf ({size_mb:.1f} MB)")
        
        # Copy to web assets
        web_pdf = SCRIPT_DIR / 'web/assets/pdf/paper.pdf'
        web_pdf.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy(pdf_path, web_pdf)
        print(f"  ✓ PDF copied to web assets")
    else:
        print("  ✗ PDF generation failed")


def main():
    parser = argparse.ArgumentParser(
        description='Reproduce all results from the Magic Squares paper'
    )
    parser.add_argument(
        '--stage', type=int, choices=[1, 2, 3, 4, 5, 6],
        help='Run specific stage only'
    )
    parser.add_argument(
        '--quick', action='store_true',
        help='Quick mode: fewer samples for faster execution'
    )
    parser.add_argument(
        '--skip-latex', action='store_true',
        help='Skip LaTeX compilation'
    )
    args = parser.parse_args()
    
    print_header("MAGIC SQUARES: COMPLETE REPRODUCTION")
    print(f"Working directory: {SCRIPT_DIR}")
    print(f"Quick mode: {args.quick}")
    
    start_time = time.time()
    
    stages = {
        1: ('Setup & Data Loading', run_stage_1),
        2: ('Hero Figures', run_stage_2),
        3: ('Alternative Hypothesis Testing', lambda: run_stage_3(args.quick)),
        4: ('Comprehensive Geometric Analysis', run_stage_4),
        5: ('Benchmark Comparison', run_stage_5),
        6: ('LaTeX Compilation', run_stage_6),
    }
    
    if args.stage:
        # Run specific stage
        name, func = stages[args.stage]
        func()
    else:
        # Run all stages
        for num, (name, func) in stages.items():
            if num == 6 and args.skip_latex:
                print_stage(6, "LaTeX Compilation (SKIPPED)")
                continue
            try:
                func()
            except Exception as e:
                print(f"  ✗ Error in stage {num}: {e}")
                print("  Continuing with next stage...")
    
    elapsed = time.time() - start_time
    
    print_header("REPRODUCTION COMPLETE")
    print(f"Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print()
    print("Generated outputs:")
    print(f"  • Figures: paper/figures/")
    print(f"  • Paper PDF: paper/main.pdf")
    print(f"  • Web dashboard: web/index.html")
    print()
    print("To view the web dashboard:")
    print("  cd web && python3 -m http.server 8000")
    print("  Then open: http://localhost:8000")
    print()


if __name__ == '__main__':
    main()

