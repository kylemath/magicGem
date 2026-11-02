#!/usr/bin/env python3
"""Generate LaTeX table snippets from cached analysis results.

Usage:  python tools/generate_tables.py [results.pkl] [out_dir]
Produces .tex files (geometric_stats.tex, emd_stats.tex, manifold_stats.tex)
that can be \input{} from the manuscript.
"""
import sys
from pathlib import Path
import pickle
import pandas as pd


def df_to_latex(df: pd.DataFrame, caption: str, label: str) -> str:
    return df.to_latex(float_format="%.3f", caption=caption, label=label, column_format="lrrrr", escape=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_tables.py <results.pkl> [out_dir]")
        sys.exit(1)
    res_path = Path(sys.argv[1]).expanduser()
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    with res_path.open("rb") as f:
        results = pickle.load(f)

    # Geometric statistics
    if "geometric_analysis" in results:
        geo_df = results["geometric_analysis"]["geometric_df"]
        tex = df_to_latex(geo_df.describe().loc[["mean", "std", "min", "max"]].T,
                          caption="Summary statistics of geometric properties.",
                          label="tab:geom-stats")
        (out_dir / "geometric_stats.tex").write_text(tex)
        print("✓ geometric_stats.tex written")

    # EMD distance stats
    if "emd_analysis" in results:
        dist = results["emd_analysis"]["distance_stats"]
        n_neighbors = len(dist["mean_distances"])
        index_labels = [f"{i+1}{'st' if i==0 else 'nd' if i==1 else 'rd' if i==2 else 'th'}" for i in range(n_neighbors)]
        df = pd.DataFrame({"mean": dist["mean_distances"], "std": dist["std_distances"]},
                          index=index_labels)
        tex = df_to_latex(df, caption="Nearest–neighbour EMD statistics.", label="tab:emd-nn")
        (out_dir / "emd_stats.tex").write_text(tex)
        print("✓ emd_stats.tex written")

    # Manifold stats
    if "manifold_analysis" in results:
        man = results["manifold_analysis"]
        df = pd.Series(man).to_frame("value")
        tex = df_to_latex(df, caption="Manifold–level summary metrics.", label="tab:manifold")
        (out_dir / "manifold_stats.tex").write_text(tex)
        print("✓ manifold_stats.tex written")


if __name__ == "__main__":
    main() 