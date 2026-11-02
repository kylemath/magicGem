"""Compatibility shim: expose existing analysis implementation under magic_squares.analysis.*

This allows legacy scripts (e.g., run_analysis.py) that import
`magic_squares.analysis` to continue working even though the code now
lives in `magic_squares/src/analysis`.
"""
from importlib import import_module
import sys
from pathlib import Path

# Determine absolute path to the package root
ROOT = Path(__file__).resolve().parent.parent

# Path to src directory
SRC_DIR = ROOT / "src"
# Add to sys.path if necessary so that 'analysis' top-level module is importable
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import the actual module implementation and re-export its attributes
_mod = import_module("magic_squares.src.analysis")
sys.modules[__name__] = _mod
globals().update(_mod.__dict__)

# -------------------------------------------------------------------
# Backward-compatibility wrappers
# -------------------------------------------------------------------

def run_analysis_pipeline(*args, **kwargs):  # type: ignore
    """Wrapper that infers `squares` argument when omitted.

    Legacy callers expected a no-arg version that internally loads/generates
    squares.  We replicate that behaviour by calling the helper from
    `magic_squares.src.analysis.core`.
    """
    if args:
        # Assume caller supplied squares explicitly → delegate to original
        return _mod.run_analysis_pipeline(*args, **kwargs)

    # No positional args supplied → handle legacy scenario
    from importlib import import_module as _import_module
    core = _import_module("magic_squares.src.analysis.core")

    try:
        squares = core.load_latest_squares()
        if squares is None or len(squares) == 0:
            raise ValueError("No existing squares.")
    except Exception:
        from magic_squares.generation.gen import generate_magic_squares
        squares = generate_magic_squares(4)

    return _mod.run_analysis_pipeline(squares, **kwargs) 