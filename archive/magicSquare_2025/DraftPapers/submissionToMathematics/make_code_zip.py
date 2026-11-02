#!/usr/bin/env python3
"""Create a lightweight reproducibility ZIP (<50 MB).

It includes:
• All scripts under `magic_squares/` and `axial_shape/` (excluding venv, *.npy) 
• The `run_all.py` orchestration script
• This environment.yml
• A minimal README

Large binary files and intermediate results are excluded.
"""
import shutil
from pathlib import Path
import zipfile
import os

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent

EXCLUDE_PATTERNS = [
    "*.npy",
    "*.csv",
    "*.png",
    "*.jpg",
    "*.pdf",
    "venv/*",
    "*.egg-info/*",
]

DEST_ZIP = HERE / "code_zip" / "magic_square_gems_code.zip"
DEST_ZIP.parent.mkdir(exist_ok=True)


def should_include(path: Path):
    rel = path.relative_to(PROJECT_ROOT)
    for pat in EXCLUDE_PATTERNS:
        if rel.match(pat):
            return False
    return True


def main():
    with zipfile.ZipFile(DEST_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for folder in ["magic_squares", "axial_shape", "spinning_top"]:
            for p in (PROJECT_ROOT / folder).rglob("*"):
                if p.is_file() and should_include(p):
                    zf.write(p, p.relative_to(PROJECT_ROOT))
    size_mb = DEST_ZIP.stat().st_size / 1024 ** 2
    print(f"Created {DEST_ZIP} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main() 