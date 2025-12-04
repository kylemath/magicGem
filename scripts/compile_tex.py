#!/usr/bin/env python3
"""
compile_tex.py
==============
Compile the LaTeX paper to PDF.

This script:
1. Runs pdflatex on main.tex
2. Runs bibtex for references
3. Runs pdflatex twice more for cross-references
4. Moves output PDF to output/

Usage:
    python scripts/compile_tex.py
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report status."""
    print(f"  Running: {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120
        )
        if result.returncode != 0:
            print(f"  ⚠ {description} had warnings/errors")
            # Print last few lines of output for debugging
            if result.stdout:
                try:
                    stdout_text = result.stdout.decode('utf-8', errors='replace')
                    lines = stdout_text.strip().split('\n')
                    for line in lines[-10:]:
                        if 'error' in line.lower() or 'warning' in line.lower():
                            print(f"    {line}")
                except:
                    pass
        else:
            print(f"  ✓ {description} completed")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ✗ {description} timed out")
        return False
    except FileNotFoundError:
        print(f"  ✗ Command not found: {cmd[0]}")
        return False


def check_latex_installed():
    """Check if pdflatex is available."""
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def compile_latex():
    """Compile the LaTeX document."""
    print("Compiling LaTeX document...")
    
    # Check if pdflatex is installed
    if not check_latex_installed():
        print("  ✗ pdflatex not found!")
        print("  Please install LaTeX (e.g., MacTeX, TeX Live, or MiKTeX)")
        print("\n  On macOS: brew install --cask mactex")
        print("  On Ubuntu: sudo apt-get install texlive-full")
        return False
    
    # Check if main.tex exists
    if not Path('main.tex').exists():
        print("  ✗ main.tex not found!")
        return False
    
    # First pdflatex run
    success = run_command(
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
        'pdflatex (pass 1)'
    )
    
    if not success:
        print("  Attempting without -halt-on-error...")
        run_command(
            ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
            'pdflatex (pass 1, lenient)'
        )
    
    # Run bibtex
    if Path('references.bib').exists():
        run_command(['bibtex', 'main'], 'bibtex')
    
    # Second pdflatex run
    run_command(
        ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
        'pdflatex (pass 2)'
    )
    
    # Third pdflatex run for cross-references
    success = run_command(
        ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
        'pdflatex (pass 3)'
    )
    
    return Path('main.pdf').exists()


def move_output():
    """Move output PDF to output directory."""
    print("\nOrganizing output files...")
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Move PDF
    if Path('main.pdf').exists():
        shutil.copy('main.pdf', output_dir / 'magic_gems.pdf')
        print(f"  ✓ PDF saved to output/magic_gems.pdf")
        return True
    else:
        print("  ✗ No PDF generated")
        return False


def clean_auxiliary():
    """Clean up auxiliary LaTeX files."""
    print("\nCleaning auxiliary files...")
    
    aux_extensions = [
        '.aux', '.log', '.bbl', '.blg', '.toc', 
        '.lof', '.lot', '.out', '.nav', '.snm'
    ]
    
    cleaned = 0
    for ext in aux_extensions:
        aux_file = Path(f'main{ext}')
        if aux_file.exists():
            aux_file.unlink()
            cleaned += 1
    
    # Also clean section aux files
    for aux_file in Path('sections').glob('*.aux'):
        aux_file.unlink()
        cleaned += 1
    
    print(f"  ✓ Removed {cleaned} auxiliary files")


def main():
    """Main function."""
    print("="*60)
    print("MAGIC GEMS: LaTeX Compilation Script")
    print("="*60)
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    print(f"Working directory: {os.getcwd()}\n")
    
    # Compile
    success = compile_latex()
    
    if success:
        # Move output
        move_output()
        
        # Clean up
        clean_auxiliary()
        
        print("\n" + "="*60)
        print("✓ Compilation successful!")
        print("  PDF available at: output/magic_gems.pdf")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("✗ Compilation failed")
        print("  Check main.log for details")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

