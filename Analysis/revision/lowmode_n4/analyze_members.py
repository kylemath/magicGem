#!/usr/bin/env python3
"""
Analyse the explicit list of L_4 members written by `lowmode_enum 4 L members_n4.bin`
(uint8, 16 bytes per arrangement, row-major, values 1..16) and produce

  * members_analysis.json : breakdown by (#row sums = 34, #column sums = 34), D4-orbit count,
                            E_full statistics, the six gallery squares
  * fig_lowmode_gallery.pdf : six non-magic members drawn as 4x4 grids with line sums
  * fig_lowmode_vs_full_n4.pdf : E_low vs symmetric E_full scatter (random vs L_4 members)

Usage: python3 analyze_members.py members_n4.bin
"""
import sys, os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = os.path.dirname(os.path.abspath(__file__))
n, N, M = 4, 16, 34
PAPER_EXAMPLE = np.array([[9, 4, 12, 3], [16, 1, 14, 7], [10, 15, 11, 8], [2, 5, 6, 13]])

rcParams.update({"font.family": "serif", "font.size": 8, "pdf.fonttype": 42})
INK, MUTED, ACCENT, GRID = "#1a1a1a", "#777777", "#c0392b", "#d9d9d9"

def line_sums(S):
    """S: (m,4,4) -> rows (m,4), cols (m,4), diag main (m,), diag anti (m,)"""
    rows = S.sum(axis=2); cols = S.sum(axis=1)
    dm = S[:, np.arange(n), np.arange(n)].sum(axis=1)
    da = S[:, np.arange(n), n - 1 - np.arange(n)].sum(axis=1)
    return rows, cols, dm, da

def energies(S):
    """E_low and symmetric E_full (all 2n line indicators + 2 diagonals), per the paper's covariance definition."""
    rows, cols, dm, da = line_sums(S.astype(np.int64))
    x = np.arange(n) - (n - 1) / 2            # x_j
    y = (n - 1) / 2 - np.arange(n)            # y_i
    covX = (cols - M).astype(float) @ x / N   # (1/N) sum_j x_j C_j'
    covY = (rows - M).astype(float) @ y / N
    covDm = (dm - M) / N                      # (1/N) sum_diag z  (indicator with mean subtracted)
    covDa = (da - M) / N
    E_low = covX**2 + covY**2 + covDm**2 + covDa**2
    E_full = (((rows - M) / N)**2).sum(1) + (((cols - M) / N)**2).sum(1) + covDm**2 + covDa**2
    return E_low, E_full

def d4_orbit_count(S):
    """Number of D4 orbits among the arrangements S (m,4,4) -- S must be D4-closed."""
    m = len(S)
    weights = (np.uint64(17) ** np.arange(16, dtype=np.uint64))
    def code(T):
        return (T.reshape(len(T), 16).astype(np.uint64) * weights).sum(axis=1)
    best = None
    for k in range(4):
        R = np.rot90(S, k, axes=(1, 2))
        for T in (R, np.transpose(R, (0, 2, 1))):
            c = code(np.ascontiguousarray(T))
            best = c if best is None else np.minimum(best, c)
    return int(np.unique(best).size)

def draw_square(ax, S, title):
    rows, cols, dm, da = line_sums(S[None].astype(np.int64))
    rows, cols, dm, da = rows[0], cols[0], int(dm[0]), int(da[0])
    ax.set_xlim(-0.9, 5.0); ax.set_ylim(-1.2, 4.6); ax.set_aspect("equal"); ax.axis("off")
    for i in range(n):
        for j in range(n):
            ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, fill=False, lw=0.6, ec=GRID))
            ax.text(j + 0.5, n - 1 - i + 0.5, str(int(S[i, j])), ha="center", va="center", fontsize=9, color=INK)
    for i in range(n):
        c = INK if rows[i] == M else ACCENT
        ax.text(n + 0.35, n - 1 - i + 0.5, str(int(rows[i])), ha="left", va="center", fontsize=8, color=c,
                fontweight="normal" if rows[i] == M else "bold")
    for j in range(n):
        c = INK if cols[j] == M else ACCENT
        ax.text(j + 0.5, -0.35, str(int(cols[j])), ha="center", va="top", fontsize=8, color=c,
                fontweight="normal" if cols[j] == M else "bold")
    ax.text(n + 0.35, -0.35, f"↘{dm}", ha="left", va="top", fontsize=7, color=MUTED)
    ax.text(-0.15, -0.35, f"↙{da}", ha="right", va="top", fontsize=7, color=MUTED)
    ax.text(2, 4.35, title, ha="center", va="center", fontsize=8, color=INK)

def main():
    path = sys.argv[1]
    S = np.fromfile(path, dtype=np.uint8).reshape(-1, n, n)
    m = len(S)
    rows, cols, dm, da = line_sums(S.astype(np.int64))
    assert np.all(dm == M) and np.all(da == M)
    rk = (rows == M).sum(1); ck = (cols == M).sum(1)
    hist = {}
    for a in range(5):
        for b in range(5):
            c = int(((rk == a) & (ck == b)).sum())
            if c: hist[f"{a},{b}"] = c
    E_low, E_full = energies(S)
    assert np.allclose(E_low, 0)
    out = {"count": m, "hist_rows_cols_equal_34": hist,
           "rows_all_34": int((rk == 4).sum()), "cols_all_34": int((ck == 4).sum()),
           "magic": int(((rk == 4) & (ck == 4)).sum()),
           "rows_all_not_cols": int(((rk == 4) & (ck < 4)).sum()),
           "cols_all_not_rows": int(((ck == 4) & (rk < 4)).sum()),
           "neither_all": int(((rk < 4) & (ck < 4)).sum()),
           "no_line_equal_34": int(((rk == 0) & (ck == 0)).sum()),
           "row_sum_multiset_counts": {},
           "E_full_nonmagic": {"min": float(E_full[E_full > 0].min()), "max": float(E_full.max()),
                               "mean": float(E_full[E_full > 0].mean()), "median": float(np.median(E_full[E_full > 0]))}}
    # row-sum deviation patterns (sorted (R_i - 34)), top 10
    dev = np.sort(rows - M, axis=1)
    u, cnt = np.unique(dev, axis=0, return_counts=True)
    order = np.argsort(-cnt)[:10]
    out["row_sum_multiset_counts"] = {str(u[i].tolist()): int(cnt[i]) for i in order}
    out["distinct_row_deviation_patterns"] = int(len(u))
    # paper example present?
    pe = PAPER_EXAMPLE.astype(np.uint8).reshape(16)
    out["paper_example_in_L4"] = bool((S.reshape(m, 16) == pe).all(1).any())
    out["d4_orbits"] = d4_orbit_count(S)
    out["d4_orbits_times_8_equals_count"] = out["d4_orbits"] * 8 == m

    # gallery: six categories
    rng = np.random.default_rng(20261007)
    cats = [((0, 0), "no row or column equals 34"), ((1, 0), "one row equals 34"), ((0, 1), "one column equals 34"),
            ((1, 1), "one row and one column equal 34"), ((4, 0), "all rows equal 34 (no column)"),
            ((0, 4), "all columns equal 34 (no row)")]
    gallery = []
    for (a, b), label in cats:
        idx = np.flatnonzero((rk == a) & (ck == b))
        if (a, b) == (0, 0):
            k = int(np.flatnonzero((S.reshape(m, 16) == pe).all(1))[0])
        else:
            k = int(rng.choice(idx))
        gallery.append({"category": [a, b], "label": label, "square": S[k].astype(int).tolist(),
                        "row_sums": rows[k].tolist(), "col_sums": cols[k].tolist(),
                        "E_full": float(E_full[k])})
    out["gallery"] = gallery
    # extra categories (4,1) and (1,4) examples for the text
    for (a, b) in ((4, 1), (1, 4)):
        idx = np.flatnonzero((rk == a) & (ck == b)); k = int(rng.choice(idx))
        out[f"example_{a}_{b}"] = {"square": S[k].astype(int).tolist(), "row_sums": rows[k].tolist(), "col_sums": cols[k].tolist()}

    fig, axes = plt.subplots(2, 3, figsize=(6.5, 4.6))
    for ax, g in zip(axes.ravel(), gallery):
        draw_square(ax, np.array(g["square"]), g["label"])
    fig.text(0.5, 0.01, "Row sums (right) and column sums (below); red bold = sum ≠ 34. Both diagonals (corners) sum to 34 in every panel.",
             ha="center", va="bottom", fontsize=7, color=MUTED)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.07, wspace=0.15, hspace=0.1)
    fig.savefig(os.path.join(HERE, "fig_lowmode_gallery.pdf"))
    plt.close(fig)

    # scatter E_low vs E_full
    perm_rng = np.random.default_rng(1)
    R = np.array([perm_rng.permutation(16) + 1 for _ in range(5000)]).reshape(-1, 4, 4)
    El_r, Ef_r = energies(R)
    sub = rng.choice(m, 3000, replace=False)
    El_m, Ef_m = E_low[sub], E_full[sub]
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    ax.scatter(El_r, Ef_r, s=5, c=MUTED, alpha=0.35, lw=0, label="5000 uniform random arrangements")
    ax.scatter(El_m, Ef_m, s=6, c=ACCENT, alpha=0.6, lw=0, label="3000 members of $L_4$ (sampled)")
    ax.scatter([0], [0], s=40, marker="*", c=INK, zorder=5, label="magic squares (7040)")
    ax.set_xlabel("$E_{\\mathrm{low}}$"); ax.set_ylabel("$E_{\\mathrm{full}}$ (symmetric, all $2n$ lines)")
    ax.set_xlim(left=-0.02 * El_r.max()); ax.set_ylim(bottom=-0.02 * Ef_r.max())
    ax.spines[["top", "right"]].set_visible(False); ax.grid(True, color=GRID, lw=0.4)
    ax.legend(frameon=False, fontsize=7, loc="lower right", markerscale=1.5)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_lowmode_vs_full_n4.pdf")); plt.close(fig)
    out["scatter"] = {"random_E_low_mean": float(El_r.mean()), "random_E_full_mean": float(Ef_r.mean()),
                      "L4_E_full_sample_mean": float(Ef_m.mean())}

    with open(os.path.join(HERE, "members_analysis.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("gallery",)}, indent=1))
    for g in gallery:
        print(g["label"], g["square"], "rows", g["row_sums"], "cols", g["col_sums"])

if __name__ == "__main__":
    main()
