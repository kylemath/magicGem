#!/usr/bin/env python3
"""Rebuild every result, figure and the final PDF.

This script is intended for reviewers and authors alike.
Running `python run_all.py` from inside the **submissionToMathematics** folder will:

1. Create a fresh timestamped `repro_runs/<timestamp>/` directory
2. Launch the canonical analysis pipeline shipped with the repository
3. Copy the resulting high-resolution figures into `figures/`
4. Compile `submission.tex` with pdfLaTeX twice (bibliography handled by biber)
5. Produce `submission.pdf` in the current directory

All heavy computations are encapsulated in the `magic_squares/run_analysis.py` entry
point; this wrapper simply orchestrates file locations and ensures MDPI-compliant
figure resolution.
"""
from pathlib import Path
import subprocess
import sys
import datetime
import shutil
import os
from shutil import which

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

REPRO_DIR = HERE / "repro_runs" / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FIG_DIR = HERE / "figures"


def run(cmd, cwd=None):
    """Utility helper to run a shell command and stream output."""
    print(f"\n[run_all] $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or ROOT, check=True)
    return result


def main():
    REPRO_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(exist_ok=True)

    # --------------------------------------------------------------
    # 1. Execute the canonical analysis pipeline
    # --------------------------------------------------------------
    pipeline_cmd = [sys.executable, "-m", "magic_squares.run_analysis", "--analysis", "all", "--generate", "--skip-existing", "--no-report"]
    run(pipeline_cmd, cwd=ROOT)

    # --------------------------------------------------------------
    # 2. Collect latest plots into the submission figures directory
    # --------------------------------------------------------------
    plot_root_candidates = [ROOT / "magic_squares" / "analysis" / "plots", ROOT / "magic_squares" / "src" / "analysis" / "plots"]
    plot_dirs = []
    for cand in plot_root_candidates:
        if cand.exists():
            plot_dirs += list(cand.glob("*"))
    if not plot_dirs:
        print("❌ No plot directories found — skipping figure copy step.")
        plot_dirs = []
    else:
        latest_plot_dir = sorted(plot_dirs, key=os.path.getmtime)[-1]
        for png in latest_plot_dir.glob("*.png"):
            dest = FIG_DIR / png.name
            shutil.copy2(png, dest)
            print(f"Copied figure: {dest.relative_to(HERE)}")

    # --------------------------------------------------------------
    # 3. Compile the LaTeX manuscript (if a TeX engine is available)
    # --------------------------------------------------------------
    if which("pdflatex") and which("biber"):
        tex_cmd = ["pdflatex", "-interaction=nonstopmode", "submission.tex"]
        bib_cmd = ["biber", "submission"]
        run(tex_cmd, cwd=HERE)
        run(bib_cmd, cwd=HERE)
        run(tex_cmd, cwd=HERE)
        run(tex_cmd, cwd=HERE)
        print("\n✅ Reproducibility run complete. Output PDF: submission.pdf")
    else:
        print("⚠️  pdflatex/biber not found — skipping PDF compilation. LaTeX sources are ready.")


if __name__ == "__main__":
    main() 