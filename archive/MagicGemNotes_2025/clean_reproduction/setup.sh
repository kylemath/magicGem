#!/bin/bash
# ============================================================================
# Magic Squares: Complete Environment Setup
# ============================================================================
#
# This script sets up the complete environment for reproducing all results
# from the paper "From Discrete Constraints to Continuous Geometry"
#
# Usage:
#   ./setup.sh           # Full setup
#   ./setup.sh --quick   # Skip LaTeX check
#
# Author: Kyle Elliott Mathewson, University of Alberta
# ============================================================================

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "Magic Squares: Environment Setup"
echo "=============================================="
echo ""
echo "Working directory: $SCRIPT_DIR"
echo ""

# ============================================================================
# Step 1: Check Python version
# ============================================================================

echo "[Step 1] Checking Python version..."

if command -v python3.9 &> /dev/null; then
    PYTHON_CMD="python3.9"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "ERROR: Python 3 not found. Please install Python 3.9+."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "  Found Python: $PYTHON_VERSION"

# ============================================================================
# Step 2: Create virtual environment
# ============================================================================

echo ""
echo "[Step 2] Creating virtual environment..."

if [ -d "venv" ]; then
    echo "  Existing venv found. Removing..."
    rm -rf venv
fi

$PYTHON_CMD -m venv venv
echo "  ✓ Virtual environment created"

# Activate venv
source venv/bin/activate
echo "  ✓ Virtual environment activated"

# ============================================================================
# Step 3: Upgrade pip and install dependencies
# ============================================================================

echo ""
echo "[Step 3] Installing dependencies..."

pip install --upgrade pip > /dev/null 2>&1
echo "  ✓ pip upgraded"

pip install -r requirements.txt > /dev/null 2>&1
echo "  ✓ Requirements installed"

# Verify key packages
echo ""
echo "  Installed packages:"
pip show numpy | grep -E "^(Name|Version):" | tr '\n' ' ' && echo ""
pip show scipy | grep -E "^(Name|Version):" | tr '\n' ' ' && echo ""
pip show matplotlib | grep -E "^(Name|Version):" | tr '\n' ' ' && echo ""
pip show pot | grep -E "^(Name|Version):" | tr '\n' ' ' && echo ""

# ============================================================================
# Step 4: Verify core module
# ============================================================================

echo ""
echo "[Step 4] Verifying core module..."

python -c "
import sys
sys.path.insert(0, 'src')
from core import is_magic, DURER_SQUARE, compute_covariance_sum
assert is_magic(DURER_SQUARE), 'Dürer square validation failed'
assert compute_covariance_sum(DURER_SQUARE) < 1e-10, 'Covariance test failed'
print('  ✓ Core module verified')
"

# ============================================================================
# Step 5: Check LaTeX (optional)
# ============================================================================

if [ "$1" != "--quick" ]; then
    echo ""
    echo "[Step 5] Checking LaTeX installation..."
    
    if command -v pdflatex &> /dev/null; then
        echo "  ✓ pdflatex found"
        if command -v bibtex &> /dev/null; then
            echo "  ✓ bibtex found"
        else
            echo "  ⚠ bibtex not found (bibliography may not compile)"
        fi
    else
        echo "  ⚠ pdflatex not found. Paper compilation will be skipped."
        echo "    To install on macOS: brew install --cask mactex-no-gui"
        echo "    To install on Ubuntu: sudo apt-get install texlive-full"
    fi
else
    echo ""
    echo "[Step 5] Skipping LaTeX check (--quick mode)"
fi

# ============================================================================
# Step 6: Generate magic squares cache
# ============================================================================

echo ""
echo "[Step 6] Generating magic squares cache..."

python -c "
import sys
sys.path.insert(0, 'src')
from core import load_squares
squares = load_squares()
print(f'  ✓ Loaded/generated {len(squares)} magic squares')
"

# ============================================================================
# Complete
# ============================================================================

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "To reproduce all results:"
echo "  source venv/bin/activate"
echo "  python reproduce_all.py"
echo ""
echo "To run quick mode (fewer samples):"
echo "  python reproduce_all.py --quick"
echo ""
echo "To compile LaTeX only:"
echo "  python reproduce_all.py --stage 6"
echo ""
