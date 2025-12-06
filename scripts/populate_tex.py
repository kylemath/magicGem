#!/usr/bin/env python3
"""
populate_tex.py
===============
Populate LaTeX files with computed statistics from data files.

This script reads JSON files from data/ and replaces placeholder values
in main.tex with actual computed statistics.

Usage:
    python scripts/populate_tex.py
"""

import sys
import os
import re
import json
from pathlib import Path


def load_json(filepath):
    """Load JSON file, return empty dict if not found."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  Warning: {filepath} not found")
        return {}


def format_number(value, precision=4):
    """Format a number for LaTeX."""
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return str(value)
    if abs(value) < 1e-10:
        return "0"
    if abs(value) < 0.001:
        return f"{value:.2e}"
    return f"{value:.{precision}f}"


def format_probability(value):
    """Format a probability as 1/X."""
    if value is None or value == 0:
        return "N/A"
    inverse = int(round(1 / value))
    return f"{inverse:,}"


def populate_main_tex():
    """Replace placeholders in main.tex with computed values."""
    print("Populating main.tex with computed statistics...")
    
    # Load data files
    summary_3 = load_json('data/summary_3x3.json')
    summary_4 = load_json('data/summary_4x4.json')
    summary_5 = load_json('data/summary_5x5.json')
    perturbation = load_json('data/perturbation_3x3.json')
    comparison = load_json('data/magic_vs_random_3x3.json')
    
    # Define replacements
    replacements = {
        'PLACEHOLDER_MAGIC_PROB_3': format_probability(
            summary_3.get('num_magic_squares', 8) / summary_3.get('total_arrangements', 362880)
        ),
        'PLACEHOLDER_HULL_VOL_3': format_number(summary_3.get('hull_volume')),
        'PLACEHOLDER_HULL_AREA_3': format_number(summary_3.get('hull_area')),
        'PLACEHOLDER_COV_XZ': format_number(summary_3.get('cov_xz'), 6),
        'PLACEHOLDER_COV_YZ': format_number(summary_3.get('cov_yz'), 6),
        'PLACEHOLDER_COV_XZ_RANDOM': format_number(
            comparison.get('random', {}).get('mean_cov_xz', summary_3.get('random_cov_xz_mean'))
        ),
        'PLACEHOLDER_COV_XZ_STD': format_number(
            comparison.get('random', {}).get('std_cov_xz', summary_3.get('random_cov_xz_std'))
        ),
        'PLACEHOLDER_PERTURB_PROP': format_number(
            perturbation.get('proportion_larger', 1.0) * 100, 1
        ),
    }
    
    # Read main.tex
    main_tex_path = Path('main.tex')
    if not main_tex_path.exists():
        print("  Error: main.tex not found")
        return False
    
    content = main_tex_path.read_text()
    
    # Perform replacements
    for placeholder, value in replacements.items():
        if placeholder in content:
            content = content.replace(placeholder, str(value))
            print(f"  ✓ Replaced {placeholder} with {value}")
        else:
            print(f"  - {placeholder} not found in main.tex")
    
    # Write back
    main_tex_path.write_text(content)
    print("✓ main.tex updated")
    
    return True


def create_stats_file():
    """Create a separate stats.tex file with all computed values."""
    print("\nCreating stats.tex with all statistics...")
    
    # Load all summaries
    summary_3 = load_json('data/summary_3x3.json')
    summary_4 = load_json('data/summary_4x4.json')
    summary_5 = load_json('data/summary_5x5.json')
    perturbation = load_json('data/perturbation_3x3.json')
    comparison = load_json('data/magic_vs_random_3x3.json')
    
    # Generate LaTeX commands
    commands = [
        "% Auto-generated statistics file",
        "% Do not edit manually - regenerate with populate_tex.py",
        "",
        "% 3x3 Statistics",
        f"\\newcommand{{\\numMagicThreeComputed}}{{{summary_3.get('num_magic_squares', 8)}}}",
        f"\\newcommand{{\\totalArrangementsThreeComputed}}{{{summary_3.get('total_arrangements', 362880):,}}}",
        f"\\newcommand{{\\hullVolumeThreeComputed}}{{{format_number(summary_3.get('hull_volume'))}}}",
        f"\\newcommand{{\\hullAreaThreeComputed}}{{{format_number(summary_3.get('hull_area'))}}}",
        f"\\newcommand{{\\covXZMagicComputed}}{{{format_number(summary_3.get('cov_xz'), 10)}}}",
        f"\\newcommand{{\\covYZMagicComputed}}{{{format_number(summary_3.get('cov_yz'), 10)}}}",
        "",
        "% Random comparison",
        f"\\newcommand{{\\covXZRandomMeanComputed}}{{{format_number(summary_3.get('random_cov_xz_mean'))}}}",
        f"\\newcommand{{\\covXZRandomStdComputed}}{{{format_number(summary_3.get('random_cov_xz_std'))}}}",
        "",
        "% Perturbation analysis",
        f"\\newcommand{{\\perturbPropLargerComputed}}{{{format_number(perturbation.get('proportion_larger', 1.0) * 100, 1)}}}",
        "",
        "% 4x4 Statistics",
        f"\\newcommand{{\\hullVolumeFourComputed}}{{{format_number(summary_4.get('hull_volume') if summary_4 else None)}}}",
        "",
        "% 5x5 Statistics",
        f"\\newcommand{{\\hullVolumeFiveComputed}}{{{format_number(summary_5.get('hull_volume'))}}}",
        f"\\newcommand{{\\covXZFiveComputed}}{{{format_number(summary_5.get('cov_xz'), 10)}}}",
    ]
    
    stats_path = Path('sections/stats.tex')
    stats_path.write_text('\n'.join(commands))
    print(f"✓ Created {stats_path}")
    
    return True


def verify_figures():
    """Verify that all referenced figures exist."""
    print("\nVerifying figures...")
    
    required_figures = [
        'figures/fig01_lo_shu.pdf',
        'figures/fig02_construction_3x3.pdf',
        'figures/fig03_magic_gem_3x3.pdf',
        'figures/fig04_vectors_3x3.pdf',
        'figures/fig05_symmetries.pdf',
        'figures/fig06_covariance_3x3.pdf',
        'figures/fig07_hull_volume_3x3.pdf',
        'figures/fig08_magic_square_4x4.pdf',
        'figures/fig09_construction_4x4.pdf',
        'figures/fig10_magic_gem_4x4.pdf',
        'figures/fig11_vectors_4x4.pdf',
        'figures/fig12_covariance_4x4.pdf',
        'figures/fig13_hull_volume_4x4.pdf',
        'figures/fig14_magic_square_5x5.pdf',
        'figures/fig15_construction_5x5.pdf',
        'figures/fig16_magic_gem_5x5.pdf',
        'figures/fig17_vectors_5x5.pdf',
        'figures/fig18_covariance_5x5.pdf',
        'figures/fig19_hull_volume_5x5.pdf',
        'figures/fig20_comparison_all_orders.pdf',
        'figures/fig21_energy_landscape_n3.pdf',
        'figures/fig22_perturbation_gaps.pdf',
        'figures/fig23_scaling_analysis.pdf',
    ]
    
    all_present = True
    missing_count = 0
    for fig in required_figures:
        if Path(fig).exists():
            print(f"  ✓ {fig}")
        else:
            print(f"  ✗ {fig} MISSING")
            all_present = False
            missing_count += 1
    
    if missing_count > 0:
        print(f"\n  {missing_count} figures missing - run analysis to generate them")
    
    return all_present


def main():
    """Main function."""
    print("="*60)
    print("MAGIC GEMS: LaTeX Population Script")
    print("="*60)
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    print(f"Working directory: {os.getcwd()}\n")
    
    # Populate main.tex
    success = populate_main_tex()
    
    # Create stats file
    create_stats_file()
    
    # Verify figures
    figures_ok = verify_figures()
    
    print("\n" + "="*60)
    if success and figures_ok:
        print("✓ LaTeX files ready for compilation!")
    else:
        print("⚠ Some issues detected - check output above")
    print("="*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

