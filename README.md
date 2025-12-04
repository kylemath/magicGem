# Magic Gems

**A Polyhedral Framework for Magic Squares**

This repository contains the code and paper for *Magic Gems*, a novel geometric representation of magic squares as three-dimensional polyhedra.

## Overview

A **Magic Gem** is constructed by:
1. Placing an n×n magic square on a centered coordinate grid
2. Using cell values as z-coordinates (centered around 0)
3. Treating each point as a vector from the origin
4. Computing the convex hull to form a polyhedron

**Key Result**: Magic squares are characterized by **zero covariance** between spatial position (x, y) and assigned value (z).

## Project Structure

```
magicGem/
├── main.tex                 # Main LaTeX paper
├── references.bib           # Bibliography
├── sections/                # LaTeX paper sections
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── background.tex
│   ├── methodology.tex
│   ├── results.tex
│   ├── discussion.tex
│   ├── conclusion.tex
│   └── appendix.tex
├── src/                     # Python source code
│   ├── __init__.py
│   ├── magic_squares.py     # Magic square generation/validation
│   ├── magic_gems.py        # Gem construction & geometry
│   ├── analysis.py          # Statistical analysis
│   └── figures.py           # Figure generation
├── scripts/                 # Automation scripts
│   ├── run_analysis.py      # Run all analyses
│   ├── populate_tex.py      # Insert stats into LaTeX
│   ├── compile_tex.py       # Compile to PDF
│   └── run_all.py           # Master pipeline script
├── data/                    # Generated data (JSON)
├── figures/                 # Generated figures (PDF)
├── output/                  # Compiled paper (PDF)
└── requirements.txt         # Python dependencies
```

## Quick Start

### 1. Set up environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the complete pipeline

```bash
# Run everything: analysis, populate LaTeX, compile PDF
python scripts/run_all.py
```

### 3. Or run individual steps

```bash
# Generate data and figures only
python scripts/run_analysis.py

# Insert statistics into LaTeX
python scripts/populate_tex.py

# Compile LaTeX to PDF
python scripts/compile_tex.py
```

## Key Modules

### `src/magic_squares.py`
- Generate and validate magic squares
- Siamese method for odd orders
- Symmetry group operations (D4)

### `src/magic_gems.py`
- Convert magic squares to 3D coordinates
- Compute convex hulls
- Calculate moment of inertia tensors
- Rotation-invariant signatures

### `src/analysis.py`
- Zero-covariance theorem validation
- Magic vs. random arrangement comparison
- Perturbation analysis
- Manifold structure exploration

### `src/figures.py`
- Publication-quality 3D visualizations
- Covariance distribution plots
- Construction process illustrations

## Example Usage

```python
from src.magic_squares import get_canonical_3x3, is_magic_square
from src.magic_gems import square_to_magic_gem, square_to_coordinates
from src.analysis import test_zero_covariance

# Get the Lo Shu square
lo_shu = get_canonical_3x3()
print("Lo Shu Magic Square:")
print(lo_shu)

# Convert to Magic Gem
gem = square_to_magic_gem(lo_shu)
print(f"\nHull Volume: {gem['properties']['hull_volume']:.4f}")

# Verify zero covariance
coords = square_to_coordinates(lo_shu)
cov = test_zero_covariance(coords)
print(f"Cov(X,Z) = {cov['cov_xz']}")  # Should be 0
print(f"Cov(Y,Z) = {cov['cov_yz']}")  # Should be 0
```

## Main Theorem

**Zero-Covariance Theorem**: An n×n arrangement of {1, ..., n²} is a magic square if and only if:
- Cov(X, Z) = 0
- Cov(Y, Z) = 0

where X, Y are the centered grid coordinates and Z is the centered cell value.

## Requirements

- Python 3.8+
- NumPy, SciPy, Matplotlib
- LaTeX (for PDF compilation): MacTeX, TeX Live, or MiKTeX

## License

MIT License

## Citation

If you use this work, please cite:

```bibtex
@article{magicgems2024,
  title={Magic Gems: A Polyhedral Framework for Magic Squares},
  author={[Author]},
  year={2024}
}
```

