"""Compatibility shim: exposes generation subpackage originally under magic_squares.src.generation."""
from importlib import import_module
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

_mod = import_module("generation")
sys.modules[__name__] = _mod
globals().update(_mod.__dict__) 