#!/usr/bin/env python3
"""Publication figure generator for Paper D:
'Can Physical Forces Find a Magic Square? Spectral Energy Landscapes,
Window Entropies, and Interactive Relaxation Dynamics' (Kyle Elliott Mathewson).

Generates 9 300-DPI publication figures (.pdf and .png) in paper_D_solver/figures/:
  - fig1_spectral_operator.pdf/.png
  - fig2_window_entropy_880.pdf/.png
  - fig3_octupole_complement.pdf/.png
  - fig4_s9_landscape_traps.pdf/.png
  - fig5_s16_descent_basins.pdf/.png
  - fig6_bubble_trinity_regimes.pdf/.png
  - fig7_multi_order_dimensional_relief.pdf/.png
  - fig8_scan_3_to_50.pdf/.png
  - fig9_competition_46_48_100.pdf/.png
"""

from __future__ import annotations

import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from verify_paper_d import (
    SQUARES_880_JSON,
    build_incidence_matrix,
    centered_height,
    doubly_even_magic,
    h_line_centered,
    lattice_coord,
    line_residuals_centered,
    lux_singly_even_magic,
    siamese_magic,
    window_entropy_and_stats,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS_JSON = ROOT / "anc" / "results_paper_d.json"
FIG_DIR = ROOT / "figures"

# Publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9.2,
    "axes.titlesize": 10.2,
    "axes.labelsize": 9.2,
    "xtick.labelsize": 8.2,
    "ytick.labelsize": 8.2,
    "legend.fontsize": 7.6,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def save_fig(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = FIG_DIR / f"{stem}.pdf"
    png_path = FIG_DIR / f"{stem}.png"
    fig.savefig(pdf_path, bbox_inches="tight", dpi=300)
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  Saved {pdf_path.name} and {png_path.name}")


def make_fig1_spectral(data: dict) -> None:
    sec2 = data["section2_spectral"]
    spec_tab = sec2["spectral_table"]
    low_ex = sec2["low_mode_counterexample"]

    fig = plt.figure(figsize=(12.4, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.05], wspace=0.30)

    # Panel (a): Spectrum of unprojected L_n vs zero-mean rationalized \tilde{L}_n
    ax0 = fig.add_subplot(gs[0, 0])
    orders = [3, 4, 5, 6, 7, 8]

    # Plot faint theoretical branch guide curves
    n_grid = np.linspace(2.8, 8.3, 120)
    ax0.plot(n_grid, n_grid, color="#2b5c8f", linestyle="-", linewidth=0.9, alpha=0.28, zorder=1)
    ax0.plot(n_grid, n_grid - 1.0, color="#2b5c8f", linestyle=":", linewidth=0.8, alpha=0.24, zorder=1)
    ax0.plot(n_grid, n_grid - 2.0, color="#2b5c8f", linestyle="--", linewidth=0.8, alpha=0.24, zorder=1)
    lam_plus_curve = (3.0 * n_grid + np.sqrt(n_grid * (n_grid + 16.0))) / 2.0
    ax0.plot(n_grid, lam_plus_curve, color="#d95f02", linestyle=":", linewidth=0.9, alpha=0.28, zorder=1)

    for idx, n in enumerate(orders):
        st = spec_tab[str(n)]
        unproj = {float(k): int(v) for k, v in st["unprojected_eigenvalues"].items()}
        zmean = {float(k): int(v) for k, v in st["zero_mean_eigenvalues"].items()}

        # Plot unprojected irrational eigenvalues (hollow orange diamonds)
        for ev, mult in unproj.items():
            if abs(ev - round(ev)) > 1e-3:
                ax0.scatter(
                    n - 0.15, ev, s=52, marker="D", facecolors="white",
                    edgecolors="#d95f02", linewidths=1.5, zorder=4,
                    label=r"Unprojected spectrum ($L_n$)" if idx == 0 and ev > n else None,
                )

        # Plot rationalized zero-mean eigenvalues (filled navy/green circles)
        for ev, mult in zmean.items():
            s_size = 38 + 3.2 * min(mult, 25)
            color = "#1b9e77" if ev == 0 else "#2b5c8f"
            ax0.scatter(
                n + 0.10, ev, s=s_size, marker="o", color=color,
                edgecolors="white", linewidths=0.7, zorder=5,
                label=(r"Zero-mean spectrum ($\widetilde{L}_n|_{\mathbf{1}^\perp}$)" if idx == 0 and ev == n else
                       (r"Kernel ($\mu=0$)" if idx == 0 and ev == 0 else None)),
            )

    # Mean eigenvalue line \bar{\mu} = 2
    ax0.axhline(2.0, color="#7570b3", linestyle="--", linewidth=1.4, zorder=2,
                label=r"Mean eigenvalue ($\bar{\mu}=2$)")
    ax0.set_xticks(orders)
    ax0.set_xticklabels([f"$n={n}$\n($N={n*n}$)" for n in orders])
    ax0.set_xlim(2.35, 8.85)
    ax0.set_ylim(-1.8, 23.5)
    ax0.set_ylabel(r"Eigenvalue $\lambda(L_n)$ on $\mathbb{R}^{n^2}$ vs. $\mu(\widetilde{L}_n)$ on $\mathbf{1}^\perp$")
    ax0.set_title(r"(a) Zero-Mean Integer Spectrum of $\widetilde{L}_n$ on $\mathbf{1}^\perp$", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=7.4)

    # Panel (b): 4x4 Balanced Impostor Square S_low
    ax1 = fig.add_subplot(gs[0, 1])
    sq = np.array(low_ex["square"], dtype=int)
    z_sq = 2 * sq - 17
    ax1.imshow(z_sq, cmap="RdBu_r", vmin=-17, vmax=17, aspect="equal", alpha=0.88)

    # Draw golden diagonal balance guides along D_+ and D_-
    ax1.plot([-0.38, 3.38], [-0.38, 3.38], color="#ffd166", linestyle="--", linewidth=1.2, alpha=0.45, zorder=2)
    ax1.plot([3.38, -0.38], [-0.38, 3.38], color="#ffd166", linestyle="--", linewidth=1.2, alpha=0.45, zorder=2)

    for r in range(4):
        for c in range(4):
            val = sq[r, c]
            z_v = z_sq[r, c]
            txt_col = "white" if abs(z_v) >= 9 else "#111111"
            ax1.text(
                c, r, f"{val}\n($Z={z_v:+d}$)",
                ha="center", va="center", fontsize=7.8, color=txt_col, fontweight="bold", zorder=4,
            )

    rows_z = low_ex["rows_Z"]
    cols_z = low_ex["cols_Z"]
    for r, rz in enumerate(rows_z):
        s_row = int(np.sum(sq[r, :]))
        ax1.text(3.55, r, f"$\\Sigma={s_row}$", va="center", ha="left",
                 fontsize=7.8, color="#333333", fontweight="bold")
    for c, cz in enumerate(cols_z):
        s_col = int(np.sum(sq[:, c]))
        ax1.text(c, 3.55, f"$\\Sigma={s_col}$", va="top", ha="center",
                 fontsize=7.8, color="#333333", fontweight="bold")

    x_coords = [-3, -1, +1, +3]
    y_coords = [+3, +1, -1, -3]
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_xticklabels([f"Col {j+1}\n($X={x_coords[j]:+d}$)" for j in range(4)], fontsize=7.4)
    ax1.set_yticklabels([f"Row {i+1}\n($Y={y_coords[i]:+d}$)" for i in range(4)], fontsize=7.4)
    ax1.set_xlim(-0.55, 4.35)
    ax1.set_ylim(4.35, -0.55)
    for sp in ("top", "right", "bottom", "left"):
        ax1.spines[sp].set_visible(False)
    ax1.set_title(r"(b) Balanced $4\times 4$ Impostor Square $S_{\mathrm{low}}$", fontweight="bold", pad=8)

    save_fig(fig, "fig1_spectral_operator")


def make_fig2_window_entropy(data: dict) -> None:
    sec3 = data["section3_multiscale"]
    per_sq = sec3["per_square_metrics"]
    raw_880 = json.loads(SQUARES_880_JSON.read_text(encoding="utf-8"))["records"]

    fig = plt.figure(figsize=(13.6, 4.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.18, 0.92], wspace=0.34)

    # Panel (a): Multiscale normalized window entropy \widetilde{H}_1(k) & \widetilde{H}_2(2)
    ax0 = fig.add_subplot(gs[0, 0])
    families = [
        ("Lo Shu ($n=3$)", siamese_magic(3), "#1b9e77", "o"),
        ("Doubly-Even ($n=4$)", doubly_even_magic(4), "#2b5c8f", "s"),
        ("Siamese ($n=5$)", siamese_magic(5), "#d95f02", "^"),
        ("Conway LUX ($n=6$)", lux_singly_even_magic(6), "#e7298a", "D"),
        ("Doubly-Even ($n=8$)", doubly_even_magic(8), "#7570b3", "v"),
    ]
    for label, sq, col, mk in families:
        n = len(sq)
        st = window_entropy_and_stats(sq)["entropies"]
        ks = list(range(1, n))
        vals_p1 = [st[f"Hnorm_p1_k{k}"] for k in ks]
        x_norm = [k / n for k in ks]
        ax0.plot(x_norm, vals_p1, marker=mk, color=col, linewidth=1.7, markersize=5.2, label=label)
        # Also plot \widetilde{H}_2(2) at k=2 as hollow marker connected by vertical drop
        h2_k2 = st["Hnorm_p2_k2"]
        h1_k2 = st["Hnorm_p1_k2"]
        ax0.plot([2 / n, 2 / n], [h2_k2, h1_k2], color=col, linestyle=":", linewidth=1.1, alpha=0.75)
        ax0.scatter([2 / n], [h2_k2], s=36, marker=mk, facecolors="white", edgecolors=col, linewidths=1.4, zorder=5)

    ax0.set_xlabel(r"Relative window scale $k / n$ ($1 \leq k \leq n-1$)")
    ax0.set_ylabel(r"Normalized window entropy $\widetilde{H}_1(k)$ (solid) & $\widetilde{H}_2(2)$ (hollow)")
    ax0.set_ylim(0.892, 1.006)
    ax0.set_title("(a) Multiscale Window Entropy ($n=3$–$8$)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="lower right", frameon=True, framealpha=0.94, fontsize=6.9)

    # Panel (b): Joint census across all 880 order-4 squares with clean 4-category palette
    ax1 = fig.add_subplot(gs[0, 1])
    pts_g1 = [x for x in per_sq if x["group"] == 1]
    pts_g3 = [x for x in per_sq if x["group"] == 3]
    pts_g6 = [x for x in per_sq if x["group"] == 6]
    pts_other = [x for x in per_sq if x["group"] not in (1, 3, 6)]

    ax1.scatter([x["w2_non_tor"] for x in pts_other], [x["Hnorm_p1_k2"] for x in pts_other],
                s=18, marker="D", color="#9e9ac8", alpha=0.55, zorder=2,
                label="Groups II, IV–V, VII–XII")
    ax1.scatter([x["w2_non_tor"] for x in pts_g6], [x["Hnorm_p1_k2"] for x in pts_g6],
                s=18, marker="o", color="#6baed6", alpha=0.60, zorder=3,
                label="Group VI")
    ax1.scatter([x["w2_non_tor"] for x in pts_g3], [x["Hnorm_p1_k2"] for x in pts_g3],
                s=30, marker="s", color="#1b9e77", alpha=0.88, zorder=5,
                label="Group III (Associative)")
    ax1.scatter([x["w2_non_tor"] for x in pts_g1], [x["Hnorm_p1_k2"] for x in pts_g1],
                s=38, marker="o", color="#d95f02", edgecolors="black", linewidths=0.6, zorder=6,
                label="Group I (Panmagic)")

    # Highlight extremal squares #123 (max entropy) and #599 (min entropy)
    sq123_meta = next(x for x in per_sq if x["id"] == 123)
    sq599_meta = next(x for x in per_sq if x["id"] == 599)
    ax1.scatter([sq123_meta["w2_non_tor"]], [sq123_meta["Hnorm_p1_k2"]],
                s=75, marker="*", color="#e7298a", edgecolors="black", linewidths=0.6, zorder=8,
                label="Max entropy (#123)")
    ax1.scatter([sq599_meta["w2_non_tor"]], [sq599_meta["Hnorm_p1_k2"]],
                s=65, marker="v", color="#b2182b", edgecolors="black", linewidths=0.6, zorder=8,
                label="Min entropy (#599)")

    ax1.axvline(0, color="#d95f02", linestyle="--", linewidth=1.2, alpha=0.85)
    ax1.set_xlabel(r"Interior $2\times 2$ quartet energy $W_{2\times 2}^{\mathrm{int}}(S) = \sum_{r,c=1}^{3} Q_{rc}(S)^2$")
    ax1.set_ylabel(r"Normalized $2\times 2$ window entropy $\widetilde{H}_1(2)$")
    ax1.set_ylim(0.936, 1.022)
    ax1.set_title(r"(b) $2\times 2$ Quartet Energy vs. Entropy ($880$ Squares)", fontweight="bold", pad=8)
    ax1.grid(True, linestyle=":", alpha=0.45)
    ax1.legend(loc="upper right", ncol=2, frameon=True, framealpha=0.94, fontsize=6.5)

    # Panel (c): Visual 4x4 board textures comparing Max Entropy #123 vs Min Entropy #599
    gs_c = gs[0, 2].subgridspec(2, 1, hspace=0.38)
    for sub_idx, (sq_id, title_tag, border_col) in enumerate([
        (123, r"(c1) Maximum Entropy Square (#123)", "#1b9e77"),
        (599, r"(c2) Minimum Entropy Square (#599)", "#b2182b"),
    ]):
        ax_c = fig.add_subplot(gs_c[sub_idx, 0])
        sq_grid = np.array(raw_880[sq_id - 1]["square"], dtype=int)
        z_abs = np.abs(2 * sq_grid - 17)
        ax_c.imshow(z_abs, cmap="YlOrRd", vmin=0, vmax=17, aspect="equal", alpha=0.82)
        for r in range(4):
            for c in range(4):
                v = sq_grid[r, c]
                za = z_abs[r, c]
                ax_c.text(c, r, f"{v}\n$|Z|={za}$", ha="center", va="center",
                          fontsize=5.8, fontweight="bold", color="white" if za >= 13 else "#1a1a1a")

        # Outline corner 2x2 window L1 weights
        rect_tl = mpatches.Rectangle((-0.46, -0.46), 1.92, 1.92, fill=False, edgecolor=border_col, linewidth=1.8, linestyle="-")
        rect_br = mpatches.Rectangle((1.54, 1.54), 1.92, 1.92, fill=False, edgecolor="#2b5c8f", linewidth=1.8, linestyle="--")
        ax_c.add_patch(rect_tl)
        ax_c.add_patch(rect_br)

        ax_c.set_xticks([])
        ax_c.set_yticks([])
        ax_c.set_xlim(-0.55, 3.55)
        ax_c.set_ylim(3.55, -0.55)
        for sp in ("top", "right", "bottom", "left"):
            ax_c.spines[sp].set_visible(False)
        ax_c.set_title(title_tag, fontweight="bold", fontsize=8.4, pad=4)

    save_fig(fig, "fig2_window_entropy_880")


def make_fig3_octupole_complement(data: dict) -> None:
    sec3 = data["section3_multiscale"]
    per_sq = sec3["per_square_metrics"]
    grp_sum = sec3["group_summary"]
    raw_880 = json.loads(SQUARES_880_JSON.read_text(encoding="utf-8"))["records"]

    fig = plt.figure(figsize=(13.6, 4.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.12, 0.98], wspace=0.38)

    # Panel (a): Toroidal vs Interior 2x2 Window Energy by Dudeney Group I-XII
    ax0 = fig.add_subplot(gs[0, 0])
    groups = list(range(1, 13))
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    mean_int = [grp_sum[str(g)]["w2_non_tor_mean"] for g in groups]
    mean_tor = [grp_sum[str(g)]["w2_tor_mean"] for g in groups]

    x = np.arange(len(groups))
    w = 0.38
    ax0.bar(x - w / 2, mean_int, width=w, color="#2b5c8f", label=r"Mean interior ($W_{2\times 2}^{\mathrm{int}}$)")
    ax0.bar(x + w / 2, mean_tor, width=w, color="#66a61e", alpha=0.88, label=r"Mean toroidal ($W_{2\times 2}^{\mathrm{tor}}$)")

    # Reference lines at ||z||^2 = 1360 and 2||z||^2 = 2720
    ax0.axhline(1360, color="#1a3a5c", linestyle="--", linewidth=1.1, alpha=0.8,
                label=r"$\|\mathbf{z}\|^2 = 1,360$ baseline")
    ax0.axhline(2720, color="#3d6611", linestyle=":", linewidth=1.2, alpha=0.8,
                label=r"$2\|\mathbf{z}\|^2 = 2,720$ baseline")

    ax0.set_xticks(x)
    ax0.set_xticklabels(roman, fontsize=7.6)
    ax0.set_ylim(0, 4400)
    ax0.set_xlabel("Dudeney Group (I–XII)")
    ax0.set_ylabel(r"Group-mean $2\times 2$ quartet energy")
    ax0.set_title(r"(a) Interior & Toroidal $2\times 2$ Energy by Group", fontweight="bold", pad=8)
    ax0.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.92, fontsize=6.8)

    # Panel (b): Mixed octupole moment |M_xyz(S)| distribution & the 56 zeros
    ax1 = fig.add_subplot(gs[0, 1])
    rng = np.random.default_rng(12345)
    for g in groups:
        vals = [abs(item["m_xyz"]) for item in per_sq if item["group"] == g]
        jitter = rng.uniform(-0.20, 0.20, size=len(vals))
        col = "#1b9e77" if g == 3 else ("#e7298a" if g in (9, 10) else "#7570b3")
        ax1.scatter(
            np.full(len(vals), g - 1) + jitter, vals,
            s=15, color=col, alpha=0.62, zorder=3,
        )
        ax1.plot([g - 1 - 0.26, g - 1 + 0.26], [np.mean(vals)] * 2, color="black", lw=1.5, zorder=4)

    # Highlight the 48 Group III zeros and 8 Group IX/X zeros explicitly at y=0
    ax1.scatter([2], [0], s=75, marker="o", color="#1b9e77", edgecolors="black", linewidths=0.8, zorder=6,
                label="Associative zeros (Group III)")
    ax1.scatter([8, 9], [0, 0], s=75, marker="*", color="#e7298a", edgecolors="black", linewidths=0.7, zorder=6,
                label="Shell-resonance zeros (Groups IX–X)")

    ax1.axhline(0, color="#1b9e77", linestyle="--", lw=1.1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(roman, fontsize=7.6)
    ax1.set_xlabel("Dudeney Group (I–XII)")
    ax1.set_ylabel(r"Octupole magnitude $|M_{xyz}(S)| = |\sum X_j Y_i Z_{ij}|$")
    ax1.set_ylim(-24, 600)
    ax1.set_title(r"(b) Mixed Octupole Magnitude by Group", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.92, fontsize=6.8)

    # Panel (c): Concentric Shell Quadrupole Identity on Non-Associative Square #208 (Group IX)
    ax2 = fig.add_subplot(gs[0, 2])
    sq208 = np.array(raw_880[208 - 1]["square"], dtype=int)
    z208 = 2 * sq208 - 17
    shell_color_grid = np.zeros((4, 4, 3), dtype=float)
    for r in range(4):
        for c in range(4):
            if (r in (0, 3)) and (c in (0, 3)):
                shell_color_grid[r, c] = [0.99, 0.88, 0.82]  # Corner, weight 9
            elif (r in (1, 2)) and (c in (1, 2)):
                shell_color_grid[r, c] = [0.93, 0.90, 0.98]  # Inner, weight 1
            else:
                shell_color_grid[r, c] = [0.85, 0.95, 0.92]  # Edge, weight 3

    ax2.imshow(shell_color_grid, aspect="equal")
    X_c = [-3, -1, +1, +3]
    Y_r = [+3, +1, -1, -3]
    for r in range(4):
        for c in range(4):
            xy_w = X_c[c] * Y_r[r]
            v = sq208[r, c]
            zv = z208[r, c]
            col_txt = "#9c2f00" if abs(xy_w) == 9 else ("#0b5852" if abs(xy_w) == 3 else "#4a2c82")
            ax2.text(
                c, r, f"{v} ($Z={zv:+d}$)\n$XY={xy_w:+d}$",
                ha="center", va="center", fontsize=5.8, fontweight="bold", color=col_txt,
            )

    # Draw inner 2x2 core boundary
    rect_inner = mpatches.Rectangle((0.5, 0.5), 2.0, 2.0, fill=False, edgecolor="#4a2c82", linewidth=1.6, linestyle="--")
    ax2.add_patch(rect_inner)

    ax2.set_xticks(range(4))
    ax2.set_yticks(range(4))
    ax2.set_xticklabels([f"$X={x:+d}$" for x in X_c], fontsize=7.0)
    ax2.set_yticklabels([f"$Y={y:+d}$" for y in Y_r], fontsize=7.0)
    ax2.set_xlim(-0.55, 3.55)
    ax2.set_ylim(3.55, -0.55)
    for sp in ("top", "right", "bottom", "left"):
        ax2.spines[sp].set_visible(False)
    ax2.set_title("(c) Concentric Shell Decomposition (Square #208)", fontweight="bold", pad=8)

    save_fig(fig, "fig3_octupole_complement")


def make_fig4_s9_landscape() -> None:
    A3 = build_incidence_matrix(3).astype(int)
    vals = (-8, -6, -4, -2, 0, 2, 4, 6, 8)
    all_perms = np.array(list(itertools.permutations(vals)), dtype=np.int32)
    R = all_perms @ A3.T
    H_all = np.sum(R * R, axis=1)

    fig = plt.figure(figsize=(12.8, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.02, 1.25], wspace=0.26)

    # Panel (a): Exhaustive S_9 energy distribution + low-energy zoom inset
    ax0 = fig.add_subplot(gs[0, 0])
    bins = np.linspace(0, 760, 39)
    ax0.hist(H_all, bins=bins, color="#2b5c8f", edgecolor="white", linewidth=0.4, alpha=0.88)
    ax0.axvline(480.0, color="#d95f02", linestyle="--", linewidth=1.6,
                label=r"Ensemble mean ($2\|\mathbf{z}\|^2 = 480$)")
    ax0.axvline(0.0, color="#1b9e77", linestyle="-", linewidth=1.8,
                label=r"Lo Shu ground state ($\mathcal{H}=0$)")
    ax0.axvline(8.0, color="#e7298a", linestyle=":", linewidth=1.8,
                label=r"Antipodal trap ($\mathcal{H}=8$)")
    ax0.axvline(720.0, color="#7570b3", linestyle="-.", linewidth=1.4,
                label=r"Global maximum")

    ax0.set_xlabel(r"Centred line-indicator Hamiltonian $\mathcal{H}_{\mathrm{line}}(S) = \mathbf{z}^\top L_3 \mathbf{z}$")
    ax0.set_ylabel(r"Number of permutations in $S_9$ ($9! = 362,880$)")
    ax0.set_xlim(-22, 790)
    ax0.set_ylim(0, 39500)
    ax0.set_title(r"(a) Exhaustive $S_9$ Energy Landscape ($362,880$ States)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=6.9)

    # Inset zooming in on low-energy states H_line in {0, 4, 8, 12, 16, 20, 24} with white background card
    ax_ins = ax0.inset_axes([0.10, 0.43, 0.38, 0.30])
    ax_ins.patch.set_facecolor("white")
    ax_ins.patch.set_alpha(0.96)
    low_H_vals = [0, 4, 8, 12, 16, 20, 24]
    low_counts = [int(np.sum(H_all == h)) for h in low_H_vals]
    bar_cols = ["#1b9e77" if h == 0 else ("#e7298a" if h == 8 else "#6baed6") for h in low_H_vals]
    x_ins = np.arange(len(low_H_vals))
    ax_ins.bar(x_ins, low_counts, color=bar_cols, edgecolor="white", width=0.68)
    ax_ins.set_xticks(x_ins)
    ax_ins.set_xticklabels([str(h) for h in low_H_vals])
    ax_ins.set_ylim(0, 60)
    ax_ins.set_title(r"Low-Energy Zoom ($\mathcal{H}_{\mathrm{line}} \leq 24$)", fontsize=6.8, fontweight="bold", pad=2)
    ax_ins.set_xlabel(r"$\mathcal{H}_{\mathrm{line}}$", fontsize=6.8, labelpad=2)
    ax_ins.tick_params(labelsize=6.0)

    # Panel (b): 3-Stage Unlocking Transition S_trap^(3) (H=8) -> Saddle (H=12) -> S_LoShu (H=0)
    ax_b_head = fig.add_subplot(gs[0, 1])
    ax_b_head.set_axis_off()
    ax_b_head.set_title(r"(b) 3-Stage Combination-Lock Escape Pathway", fontweight="bold", pad=8)

    gs_b = gs[0, 1].subgridspec(2, 3, height_ratios=[1.35, 0.55], wspace=0.28, hspace=0.28)
    boards = [
        (
            np.array([[2, 6, 7], [9, 5, 1], [3, 4, 8]], dtype=int),
            r"1. Trap State",
            "#e7298a",
            [(0, 1), (0, 2)],
        ),
        (
            np.array([[2, 7, 6], [9, 5, 1], [3, 4, 8]], dtype=int),
            r"2. Saddle State",
            "#d95f02",
            [(2, 0), (2, 1)],
        ),
        (
            np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]], dtype=int),
            r"3. Ground State",
            "#1b9e77",
            [],
        ),
    ]

    for b_idx, (b_mat, b_title, b_col, swap_cells) in enumerate(boards):
        ax_b = fig.add_subplot(gs_b[0, b_idx])
        z_mat = 2 * b_mat - 10
        ax_b.imshow(z_mat, cmap="YlOrRd", vmin=-12, vmax=12, aspect="equal", alpha=0.24)
        for r in range(3):
            for c in range(3):
                v = b_mat[r, c]
                is_hi = (r, c) in swap_cells
                ax_b.text(
                    c, r, f"{v}", ha="center", va="center",
                    fontsize=10.5, fontweight="bold",
                    color=b_col if is_hi else "#1a1a1a",
                )
                if is_hi:
                    rect = mpatches.Rectangle((c - 0.44, r - 0.44), 0.88, 0.88, fill=False,
                                             edgecolor=b_col, linewidth=1.8, linestyle="-")
                    ax_b.add_patch(rect)
        for c in range(3):
            csum = int(np.sum(b_mat[:, c]))
            ccol = "#1b9e77" if csum == 15 else "#d95f02"
            ax_b.text(c, 2.68, f"$\\Sigma={csum}$", ha="center", va="top", fontsize=7.0, fontweight="bold", color=ccol)

        ax_b.set_xticks([])
        ax_b.set_yticks([])
        ax_b.set_xlim(-0.55, 2.55)
        ax_b.set_ylim(3.25, -0.55)
        for sp in ("top", "right", "bottom", "left"):
            ax_b.spines[sp].set_visible(True)
            ax_b.spines[sp].set_color(b_col)
            ax_b.spines[sp].set_linewidth(1.3)
        ax_b.set_title(b_title, fontsize=8.2, fontweight="bold", color=b_col, pad=5)

    # Bottom reaction-coordinate energy profile across the (2,2) double swap
    ax_rc = fig.add_subplot(gs_b[1, :])
    rc_x = np.linspace(0, 2, 200)
    rc_y = np.where(
        rc_x <= 1.0,
        8.0 + 4.0 * np.sin(0.5 * np.pi * rc_x) ** 2,
        12.0 * np.cos(0.5 * np.pi * (rc_x - 1.0)) ** 2,
    )
    ax_rc.plot(rc_x, rc_y, color="#2b5c8f", linewidth=2.0)
    ax_rc.fill_between(rc_x, 0, rc_y, color="#2b5c8f", alpha=0.10)
    ax_rc.scatter([0, 1, 2], [8, 12, 0], s=55, color=["#e7298a", "#d95f02", "#1b9e77"], zorder=5)
    ax_rc.set_xlim(-0.2, 2.2)
    ax_rc.set_ylim(-1.5, 14.5)
    ax_rc.set_xticks([0, 1, 2])
    ax_rc.set_xticklabels([
        r"Start: $S_{\mathrm{trap}}^{(3)}$",
        r"Step 1: $\tau_1 = (6\leftrightarrow 7)$ in Row 1",
        r"Step 2: $\tau_2 = (3\leftrightarrow 4)$ in Row 3",
    ], fontsize=7.4)
    ax_rc.set_ylabel(r"Energy $\mathcal{H}_{\mathrm{line}}$", fontsize=7.8)
    ax_rc.grid(True, linestyle=":", alpha=0.45)

    save_fig(fig, "fig4_s9_landscape_traps")


def make_fig5_s16_descent(data: dict) -> None:
    sec4 = data["section4_swap_landscape"]["n4_benchmark"]
    hist_data = sec4["terminal_H_histogram"]

    A4 = build_incidence_matrix(4).astype(int)
    L4 = A4.T @ A4
    diag_L4 = np.diag(L4)
    pairs4 = [(a, b) for a in range(16) for b in range(a + 1, 16)]
    lp22_4 = []
    for r1 in range(4):
        for r2 in range(r1 + 1, 4):
            for c1 in range(4):
                for c2 in range(c1 + 1, 4):
                    lp22_4.append((4 * r1 + c1, 4 * r1 + c2, 4 * r2 + c1, 4 * r2 + c2))
                    lp22_4.append((4 * c1 + r1, 4 * c2 + r1, 4 * c1 + r2, 4 * c2 + r2))

    rng = random.Random(20261102)
    base_vals4 = [centered_height(s, 4) for s in range(1, 17)]

    trajs_magic = []
    trajs_trapped = []
    escaped_by_bin = Counter()
    total_by_bin = Counter()

    for _ in range(300):
        z = base_vals4[:]
        rng.shuffle(z)
        z_arr = np.array(z, dtype=int)
        curve = [int(np.sum((A4 @ z_arr) ** 2))]
        while True:
            r = A4 @ z_arr
            e = int(np.sum(r * r))
            if e == 0:
                break
            g = A4.T @ r
            best_delta = 0
            best_pair = None
            for a, b in pairs4:
                c_ab = int(diag_L4[a] + diag_L4[b] - 2 * L4[a, b])
                d = int(z_arr[a] - z_arr[b])
                delta = -2 * d * int(g[a] - g[b]) + d * d * c_ab
                if delta < best_delta:
                    best_delta = delta
                    best_pair = (a, b)
            if best_pair is None:
                break
            a, b = best_pair
            z_arr[a], z_arr[b] = z_arr[b], z_arr[a]
            curve.append(int(np.sum((A4 @ z_arr) ** 2)))

        e_term = curve[-1]
        total_by_bin[e_term] += 1
        if e_term == 0:
            trajs_magic.append(curve)
        else:
            trajs_trapped.append(curve)
            for a, b, c, d in lp22_4:
                q = z_arr.copy()
                q[a], q[b] = q[b], q[a]
                q[c], q[d] = q[d], q[c]
                if int(np.sum((A4 @ q) ** 2)) < e_term:
                    escaped_by_bin[e_term] += 1
                    break

    fig = plt.figure(figsize=(12.2, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.08], wspace=0.28)

    # Panel (a): Steepest-descent relaxation ribbons + 6 exemplars + terminal halting markers
    ax0 = fig.add_subplot(gs[0, 0])
    max_t = 14
    steps_arr = np.arange(max_t + 1)

    def pad_curves(curves: list[list[int]]) -> np.ndarray:
        mat = np.zeros((len(curves), max_t + 1), dtype=float)
        for i, c in enumerate(curves):
            for t in range(max_t + 1):
                mat[i, t] = (c[t] if t < len(c) else c[-1]) + 4.0
        return mat

    mat_trapped = pad_curves(trajs_trapped)
    mat_magic = pad_curves(trajs_magic)

    ax0.fill_between(
        steps_arr, np.percentile(mat_trapped, 20, axis=0), np.percentile(mat_trapped, 80, axis=0),
        color="#d95f02", alpha=0.18, label=r"Trapped envelope ($20\%–80\%$)"
    )
    ax0.fill_between(
        steps_arr, np.percentile(mat_magic, 20, axis=0), np.percentile(mat_magic, 80, axis=0),
        color="#1b9e77", alpha=0.18, label=r"Ground-state envelope ($20\%–80\%$)"
    )

    for i, c in enumerate(trajs_trapped[:6]):
        y_c = np.array(c) + 4.0
        ax0.plot(range(len(c)), y_c, color="#d95f02", alpha=0.80, lw=1.3)
        ax0.scatter([len(c) - 1], [y_c[-1]], s=28, marker="o", color="#b34800", edgecolors="white", linewidths=0.6, zorder=6,
                    label=r"Local minimum halt" if i == 0 else None)

    for i, c in enumerate(trajs_magic[:6]):
        y_c = np.array(c) + 4.0
        ax0.plot(range(len(c)), y_c, color="#1b9e77", alpha=0.88, lw=1.5)
        ax0.scatter([len(c) - 1], [y_c[-1]], s=34, marker="*", color="#0f6648", zorder=6,
                    label=r"Ground-state termination" if i == 0 else None)

    ax0.axhspan(12.0, 20.0, color="#ffd166", alpha=0.22, zorder=1)
    ax0.axhline(4.0, color="#1b9e77", linestyle="--", linewidth=1.3, zorder=2)

    ax0.set_yscale("log")
    ax0.set_yticks([4, 12, 20, 104, 1004, 2724])
    ax0.set_yticklabels([r"$0$", r"$8$", r"$16$", r"$100$", r"$1,000$", r"$2,720$"])
    ax0.set_xlim(-0.2, 14.5)
    ax0.set_ylim(3.2, 6000)
    ax0.set_xlabel("Steepest-descent $2$-cycle transposition step $t$")
    ax0.set_ylabel(r"Line-indicator energy $\mathcal{H}_{\mathrm{line}}(S_t)$ (log scale)")
    ax0.set_title(r"(a) Order-4 ($S_{16}$) Steepest-Descent Envelopes & Halting", fontweight="bold", pad=8)
    ax0.grid(True, which="major", linestyle=":", alpha=0.45)
    ax0.legend(loc="upper right", frameon=True, framealpha=0.94, fontsize=6.9)

    # Panel (b): Terminal local-minimum spectrum across 2,000 starts + (2,2) plaquette escape yield
    ax1 = fig.add_subplot(gs[0, 1])
    ks = [int(k) for k in hist_data.keys() if int(k) <= 60]
    vs = [hist_data[str(k)] for k in ks]
    esc_vs = [
        0 if k == 0 else int(round(vs[i] * (escaped_by_bin[k] / max(1, total_by_bin[k]))))
        for i, k in enumerate(ks)
    ]

    x_idx = np.arange(len(ks))
    colors = ["#1b9e77" if k == 0 else "#d95f02" for k in ks]
    ax1.bar(x_idx, vs, color=colors, edgecolor="white", width=0.74, label=r"$2$-Cycle local minima")
    ax1.bar(x_idx, esc_vs, color="#2b5c8f", edgecolor="white", width=0.74, hatch="//", alpha=0.85,
            label=r"$(2,2)$ Plaquette escape yield")

    ax1.set_xticks(x_idx)
    ax1.set_xticklabels([str(k) for k in ks], fontsize=7.6)
    ax1.set_ylim(0, 520)
    ax1.set_xlabel(r"Terminal $2$-cycle local-minimum energy $\mathcal{H}_{\mathrm{line}}(S_\infty)$")
    ax1.set_ylabel("Count out of 2,000 uniform random starts")
    ax1.set_title(r"(b) $S_{16}$ Local-Minimum Spectrum & $(2,2)$ Escape Yield", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.94, fontsize=6.8)

    save_fig(fig, "fig5_s16_descent_basins")


def make_fig6_bubble_trinity(data: dict) -> None:
    sec5 = data["section5_bubble_trinity"]
    regimes = sec5["regime_metrics"]
    ablation = sec5["ablation_study"]

    fig = plt.figure(figsize=(14.4, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.02, 0.84, 1.18], wspace=0.62)

    # Panel (a): Continuous kernel energy H_ind(t) vs Discrete Snapped Energy H_line
    ax0 = fig.add_subplot(gs[0, 0])
    styles = {
        "I_Frozen_Lattice": ("I. Frozen Lattice", "#7570b3", "--", "s"),
        "II_Slow_Drift": ("II. Slow Drift", "#2b5c8f", "-.", "^"),
        "III_Field_Storm": ("III. Field Storm", "#d95f02", "-", "o"),
        "IV_Centrifugal_Balance": ("IV. Centrifugal Balance", "#1b9e77", "-", "D"),
    }
    steps = [10 * i for i in range(25)]
    for key, (label, col, ls, mk) in styles.items():
        y = regimes[key]["trajectory_H_decimated"]
        ax0.plot(steps, y, color=col, linestyle=ls, marker=mk, markersize=4.2,
                 markevery=3, linewidth=1.7, label=label)

    y_iv = np.array(regimes["IV_Centrifugal_Balance"]["trajectory_H_decimated"])
    ax0.axhline(2336, color="#b2182b", linestyle="--", linewidth=1.4,
                label=r"Hungarian discrete snap")
    ax0.axhline(1480, color="#e7298a", linestyle=":", linewidth=1.3,
                label=r"Greedy discrete snap")
    ax0.fill_between(steps, y_iv, 2336, color="#b2182b", alpha=0.08)

    ax0.set_ylim(950, 2550)
    ax0.set_xlabel(r"Continuous integration step $t$ ($\Delta t = 0.025$)")
    ax0.set_ylabel(r"Continuous $\mathcal{H}_{\mathrm{ind}}(t)$ vs. Discrete $\mathcal{H}_{\mathrm{line}}$")
    ax0.set_title(r"(a) Kernel Drift vs. Discrete Snap Reality", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper right", frameon=True, framealpha=0.92, fontsize=6.3)

    # Panel (b): Spatial 2D Bubble Border-Parking Diagram in Preset IV (Centrifugal Balance)
    ax_b = fig.add_subplot(gs[0, 1])
    A4 = build_incidence_matrix(4)
    cell_xy = np.array([[(c - 1.5), (r - 1.5)] for r in range(4) for c in range(4)], dtype=float)
    durer = [16, 3, 2, 13, 5, 10, 11, 8, 9, 6, 7, 12, 4, 15, 14, 1]
    z_pert = np.array([centered_height(v, 4) for v in durer], dtype=float)
    for a, b in [(0, 5), (2, 11), (7, 12), (9, 14)]:
        z_pert[a], z_pert[b] = z_pert[b], z_pert[a]
    s_pert = ((z_pert + 17) / 2).astype(int)

    p = {"field": 2.2, "repulsion": 0.5, "well": 1.8, "containment": 0.5, "memory": 0.75, "snap": 0.85, "temp": 0.4}
    rng = np.random.default_rng(42)
    for _ in range(3 * 250):
        rng.standard_normal((16, 2))
    pos = cell_xy.copy()
    vel = np.zeros_like(pos)
    pos_hist = [pos.copy()]
    for _ in range(250):
        dists = np.linalg.norm(pos[:, None, :] - cell_xy[None, :, :], axis=2)
        weights = np.exp(-2.0 * (dists ** 2))
        weights /= np.sum(weights, axis=0, keepdims=True) + 1e-9
        res = A4 @ (weights.T @ z_pert)
        f_well = -p["well"] * (pos - cell_xy)
        f_cont = -p["containment"] * pos
        diff = pos[:, None, :] - pos[None, :, :]
        dist_sq = np.sum(diff * diff, axis=2) + 0.15
        np.fill_diagonal(dist_sq, np.inf)
        f_rep = p["repulsion"] * np.sum(diff / (dist_sq[:, :, None] ** 1.5), axis=1) * 0.08
        cell_stress = A4.T @ res
        target_scores = -np.outer(z_pert, cell_stress) / 250.0
        soft_targets = np.exp(np.clip(target_scores, -5, 5))
        soft_targets /= np.sum(soft_targets, axis=1, keepdims=True)
        f_field = (p["field"] * 0.25 + p["snap"] * 0.65) * ((soft_targets @ cell_xy) - pos)
        vel = p["memory"] * vel + 0.025 * (f_well + f_cont + f_rep + f_field) + 0.025 * p["temp"] * 0.12 * rng.standard_normal(pos.shape)
        pos = pos + 0.025 * vel
        pos_hist.append(pos.copy())
    pos_hist = np.array(pos_hist)

    for g_line in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        ax_b.axhline(g_line, color="#adb5bd", linestyle="-", linewidth=1.0, zorder=1)
        ax_b.axvline(g_line, color="#adb5bd", linestyle="-", linewidth=1.0, zorder=1)

    cmap_b = plt.get_cmap("RdBu_r")
    for idx_p in range(16):
        col_p = cmap_b((z_pert[idx_p] + 16.0) / 32.0)
        ax_b.plot(pos_hist[:, idx_p, 0], pos_hist[:, idx_p, 1], color=col_p, linewidth=1.1, alpha=0.55, zorder=2)
        ax_b.scatter([cell_xy[idx_p, 0]], [cell_xy[idx_p, 1]], s=18, marker="+", color="#6c757d", zorder=3)
        rad_s = 115 + 8.0 * abs(z_pert[idx_p])
        ax_b.scatter([pos[idx_p, 0]], [pos[idx_p, 1]], s=rad_s, color=col_p, edgecolors="black", linewidths=0.8, zorder=5)
        txt_c = "white" if abs(z_pert[idx_p]) >= 9 else "#111111"
        ax_b.text(pos[idx_p, 0], pos[idx_p, 1], f"{s_pert[idx_p]}", ha="center", va="center",
                  fontsize=6.6, fontweight="bold", color=txt_c, zorder=6)

    ax_b.set_xlim(-2.05, 2.05)
    ax_b.set_ylim(2.05, -2.05)
    ax_b.set_aspect("equal")
    ax_b.set_xticks([-1.5, -0.5, 0.5, 1.5])
    ax_b.set_yticks([-1.5, -0.5, 0.5, 1.5])
    ax_b.set_xticklabels(["Col 1", "Col 2", "Col 3", "Col 4"], fontsize=7.2)
    ax_b.set_yticklabels(["Row 1", "Row 2", "Row 3", "Row 4"], fontsize=7.2)
    ax_b.set_xlabel("Grid column $x$", fontsize=7.2, labelpad=6)
    ax_b.set_ylabel("Grid row $y$", fontsize=7.2, labelpad=6)
    ax_b.set_title("(b) Preset IV Border-Parking", fontweight="bold", pad=8)

    # Panel (c): Operator Ablation Hierarchy with concise labels so there is zero cross-panel overlap
    ax1 = fig.add_subplot(gs[0, 2])
    tiers = [
        ("0_continuous_2d_greedy_snap_pct", "Tier 0: 2D Bubble Drift"),
        ("1_kawasaki_2cycle_quench_pct", "Tier 1: 2-Exchange Quench"),
        ("2_vacancy_3cycle_sa_pct", "Tier 2: (2+3)-Cycle SA"),
        ("3_spin_ice_lp22_quench_pct", "Tier 3: + (2,2) Plaquette"),
        ("4_t1_eshelby_6kicks_pct", "Tier 4: + Candidate Swaps"),
        ("5_plane_glide_18kicks_pct", "Tier 5: + Funnel Leash"),
        ("6_wales_doye_reanchored_full_pct", "Tier 6: + ME-ILS Restarts"),
    ]
    y_pos = np.arange(len(tiers))
    n4_rates = [ablation["n4"][k] for k, _ in tiers]
    n5_rates = [ablation["n5"][k] for k, _ in tiers]

    ax1.axhspan(-0.5, 2.5, color="#fff5eb", alpha=0.55, zorder=0)
    ax1.axhspan(2.5, 6.5, color="#eefaf4", alpha=0.55, zorder=0)

    h = 0.36
    ax1.barh(y_pos - h / 2, n4_rates, height=h, color="#2b5c8f", edgecolor="white",
             label="Order $n=4$", zorder=3)
    ax1.barh(y_pos + h / 2, n5_rates, height=h, color="#1b9e77", edgecolor="white",
             label="Order $n=5$", zorder=3)

    ax1.axhline(2.5, color="#d95f02", linestyle="--", linewidth=1.2, alpha=0.85, zorder=4)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([lbl for _, lbl in tiers], fontsize=6.9)
    ax1.invert_yaxis()
    ax1.set_xlim(0, 105)
    ax1.set_ylim(6.5, -0.5)
    ax1.set_xlabel(r"Ground-state synthesis rate ($\mathcal{H}_{\mathrm{line}}=0$, %)")
    ax1.set_title(r"(c) 6-Tier Operator Ablation ($n=4,5$)", fontweight="bold", pad=8)
    ax1.grid(True, axis="x", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.94, fontsize=6.8)

    save_fig(fig, "fig6_bubble_trinity_regimes")


def make_fig7_dimensional_relief(data: dict) -> None:
    multi = data["section5_bubble_trinity"]["multi_order_upgraded"]
    orders = [int(k[1:]) for k in sorted(multi.keys(), key=lambda x: int(x[1:]))]
    null_dims = [n * n - 2 * n - 1 for n in orders]
    eta_mc = [(n * n - 2 * n - 1) / (2.0 * n) for n in orders]
    f_null_pct = [100.0 * (1.0 - 2.0 / ((n - 1) ** 2)) for n in orders]
    restarts = [multi[f"n{n}"]["mean_restarts"] for n in orders]
    descents = [multi[f"n{n}"]["mean_descents"] for n in orders]
    times_ms = [multi[f"n{n}"]["mean_ms"] for n in orders]

    fig = plt.figure(figsize=(12.6, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.05], wspace=0.34)

    # Panel (a): Mean restarts and mean 2-cycle descents vs order n = 3..10
    ax0 = fig.add_subplot(gs[0, 0])
    ax0_r = ax0.twinx()

    ax0.axvspan(4.5, 6.3, color="#fdf0f6", alpha=0.65, zorder=0)
    ax0.axvspan(6.3, 10.3, color="#eefaf4", alpha=0.65, zorder=0)

    l1 = ax0.plot(orders, restarts, color="#e7298a", marker="o", markersize=6.0,
                  linewidth=2.1, label="Restarts", zorder=4)
    l2 = ax0_r.plot(orders, descents, color="#2b5c8f", linestyle="--", marker="s", markersize=5.2,
                    linewidth=1.8, label="Descent loops", zorder=3)

    ax0.set_xticks(orders)
    ax0.set_xticklabels([f"$n={n}$\n(${eta:.1f}$)" for n, eta in zip(orders, eta_mc)], fontsize=7.4)
    ax0.set_xlim(2.6, 10.4)
    ax0.set_ylim(0, 10.5)
    ax0_r.set_ylim(0, 550)
    ax0.set_xlabel(r"Grid order $n$ (Maxwell–Calladine ratio $\eta_{\mathrm{MC}}$)")
    ax0.set_ylabel("Mean restarts required to reach $\\mathcal{H}_{\\mathrm{line}}=0$", color="#a8135d")
    ax0_r.set_ylabel("Mean $O(1)$ $2$-exchange descent loops", color="#2b5c8f")
    ax0.set_title("(a) Frustration Peak ($n=5$) & Nullspace Relief ($n=6$–$10$)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax0.legend(lines, labels, loc="upper left", frameon=True, framealpha=0.94, fontsize=6.9)

    # Panel (b): Quadratic Nullspace Expansion vs Constraint Rank & Runtime (with f_null annotated on bars)
    ax1 = fig.add_subplot(gs[0, 1])
    ax1_r = ax1.twinx()

    x = np.arange(len(orders))
    w = 0.36
    rank_vals = [2 * n for n in orders]
    # Place Magic Nullspace on left (x - w/2) and Constraint Rank on right (x + w/2), with runtime plotted over right bars (x + w/2)
    b_null = ax1.bar(x - w / 2, null_dims, width=w, color="#1b9e77", edgecolor="white",
                     label=r"Magic nullspace $\dim\ker(\widetilde{L}_n)$", zorder=3)
    b_rank = ax1.bar(x + w / 2, rank_vals, width=w, color="#8da0cb", edgecolor="white",
                     label=r"Constraint rank $\operatorname{rank}(\widetilde{L}_n)$", zorder=3)

    l_time = ax1_r.plot(x + w / 2, times_ms, color="#d95f02", marker="D", markersize=5.0,
                        linewidth=1.9, label="Runtime (ms)", zorder=5)

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"$n={n}$" for n in orders], fontsize=7.8)
    ax1.set_ylim(0, 95)
    ax1_r.set_ylim(0, 1120)
    ax1.set_xlabel("Magic square order $n$")
    ax1.set_ylabel("Subspace dimension in $\\mathbf{1}^\\perp \\subset \\mathbb{R}^{n^2-1}$")
    ax1_r.set_ylabel("Mean synthesis time per square (ms)", color="#b34800")
    ax1.set_title("(b) Quadratic Nullspace Expansion, Constraint Rank & Runtime", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax1_r.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left", frameon=True, framealpha=0.94, fontsize=6.7)

    save_fig(fig, "fig7_multi_order_dimensional_relief")


def make_fig8_scan_3_to_50(data: dict) -> None:
    d_base = data["section5_bubble_trinity"]["multi_order_upgraded"]
    sec6 = data["section6_large_scale_competition"]
    d_scan = sec6["scan_10_to_50"]
    bili = sec6["bilinear_scaling"]

    orders = list(range(3, 51))
    restarts = []
    descents = []
    times_s = []
    for n in orders:
        row = d_base[f"n{n}"] if n < 10 else d_scan[f"n{n}"]
        restarts.append(row["mean_restarts"])
        descents.append(row["mean_descents"])
        times_s.append(row["mean_ms"] / 1000.0)

    restarts_arr = np.array(restarts, dtype=float)
    descents_arr = np.array(descents, dtype=float)
    desc_per_run = descents_arr / (restarts_arr + 1.0)

    mov_avg_n = orders[4:-2]
    mov_avg_r = [float(np.mean(restarts_arr[i - 2:i + 3])) for i in range(4, len(orders) - 2)]

    fig = plt.figure(figsize=(13.4, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.14, 1.02], wspace=0.32)

    # Panel (a): Complete Order-by-Order Scan n = 3..50 (48 consecutive orders, 100% solved)
    ax0 = fig.add_subplot(gs[0, 0])
    ax0_r = ax0.twinx()

    ax0.axvspan(4.5, 6.5, color="#fdf0f6", alpha=0.65, zorder=0)
    ax0.axvspan(6.5, 50.8, color="#eefaf4", alpha=0.50, zorder=0)

    l_raw = ax0.plot(orders, restarts_arr, color="#e7298a", marker="o", markersize=3.6,
                     linewidth=1.0, alpha=0.48, label="Per-order restarts", zorder=3)
    l_ma = ax0.plot(mov_avg_n, mov_avg_r, color="#a8135d", linewidth=2.3,
                    label="5-order moving average", zorder=5)
    l_desc = ax0_r.plot(orders, desc_per_run, color="#2b5c8f", linestyle="--", marker="s", markersize=3.2,
                        markevery=2, linewidth=1.8,
                        label="Descents per restart", zorder=4)

    ax0.set_xlim(2.0, 51.2)
    ax0.set_ylim(0, 21.0)
    ax0_r.set_ylim(0, 220)
    ax0.set_xticks([3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax0.set_xlabel("Magic square order $n$")
    ax0.set_ylabel("Mean restarts required to reach $\\mathcal{H}_{\\mathrm{line}}=0$", color="#a8135d")
    ax0_r.set_ylabel("Mean $2$-exchange descents per restart", color="#2b5c8f")
    ax0.set_title("(a) Full Order-by-Order Scaling Census ($n=3\\dots 50$)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)

    lines = l_raw + l_ma + l_desc
    labels = [l.get_label() for l in lines]
    ax0.legend(lines, labels, loc="upper left", frameon=True, framealpha=0.94, fontsize=6.4)

    # Panel (b): Measured All-Pairs ME-ILS (n=10..50) vs Bilinear-Identity + Active-Set ME-ILS (n=10..100)
    ax1 = fig.add_subplot(gs[0, 1])
    n_meas = np.array(orders[7:], dtype=float)
    t_meas = np.array(times_s[7:], dtype=float)

    n_bili = np.array([10, 20, 30, 40, 46, 48, 50, 100], dtype=float)
    t_bili = np.array([bili[f"n{int(k)}"]["mean_s"] for k in n_bili], dtype=float)
    r_bili = np.array([bili[f"n{int(k)}"]["mean_restarts"] for k in n_bili], dtype=float)
    t_bili_per_run = t_bili / (r_bili + 1.0)

    n_grid = np.logspace(1.0, 2.05, 120)
    c_allpairs = np.median(t_meas[-15:] / (n_meas[-15:] ** 5.92))
    t_allpairs_ext = c_allpairs * (n_grid ** 5.92)

    ax1.loglog(n_meas, t_meas, "o-", color="#d95f02", markersize=3.5, linewidth=1.3, alpha=0.85,
               label="Baseline All-Pairs (measured)")
    ax1.loglog(n_grid[n_grid >= 50], t_allpairs_ext[n_grid >= 50], "--", color="#d95f02", linewidth=1.3,
               label="Baseline All-Pairs (extrapolated)")
    ax1.loglog(n_bili, t_bili, "D-", color="#1b9e77", markersize=5.0, linewidth=2.0,
               label="Bilinear + Active-Set (total time)")
    ax1.loglog(n_bili, t_bili_per_run, "s-.", color="#2b5c8f", markersize=4.2, linewidth=1.6,
               label="Bilinear + Active-Set (time/restart)")

    ax1.set_xlim(8.5, 125.0)
    ax1.set_ylim(0.005, 4e4)
    ax1.set_xticks([10, 20, 30, 50, 70, 100])
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.set_xlabel("Magic square order $n$ (log scale)")
    ax1.set_ylabel("Wall-clock synthesis time (seconds, log scale)")
    ax1.set_title("(b) Algebraic $O(n^3)$ Per-Restart Scaling up to $n=100$", fontweight="bold", pad=8)
    ax1.grid(True, which="both", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=6.3)

    save_fig(fig, "fig8_scan_3_to_50")


def make_fig9_competition_46_48_100(data: dict) -> None:
    fig = plt.figure(figsize=(14.4, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.14, 1.10, 1.00], wspace=0.34)

    orders_lbl = ["$n = 46$\n(2,116 cells)\nsingly-even", "$n = 48$\n(2,304 cells)\ndoubly-even", "$n = 100$\n(10,000 cells)\ndoubly-even"]
    x = np.arange(3)
    w = 0.19

    t_sa = [3.02, 2.99, 3.04]
    t_cbls = [168.06, 152.89, 3582.92]
    t_base = [386.13, 280.95, 7420.0]
    t_bili = [11.12, 8.02, 147.70]
    bili_seeds = [[18.34, 5.29, 9.73], [7.12, 6.90, 10.03], [62.02, 347.02, 34.06]]

    # Panel (a): Wall-Clock Time
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.bar(x - 1.5 * w, t_sa, w, label="Simulated Annealing", color="#cbd5e1", edgecolor="#475569", hatch="//")
    ax0.bar(x - 0.5 * w, t_cbls, w, label="Defective-Line CBLS", color="#fdae61", edgecolor="#9c2f00", hatch="..")
    ax0.bar(x + 0.5 * w, t_base, w, label="Baseline All-Pairs ME-ILS", color="#2b5c8f", edgecolor="#16324f")
    ax0.bar(x + 1.5 * w, t_bili, w, label="Bilinear + Active-Set ME-ILS", color="#1b9e77", edgecolor="#0f6648", linewidth=1.2)

    for i in range(3):
        ax0.scatter([x[i] + 1.5 * w] * 3, bili_seeds[i], color="#0a3d2a", zorder=6, s=18, alpha=0.88)

    ax0.set_yscale("log")
    ax0.set_ylim(0.8, 80000.0)
    ax0.set_xticks(x)
    ax0.set_xticklabels(orders_lbl, fontsize=7.6)
    ax0.set_ylabel("Mean wall-clock time (seconds, log scale)")
    ax0.set_title("(a) Speed Competition: Time to Ground State", fontweight="bold", pad=8)
    ax0.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=6.3)

    # Panel (b): Total Operator Evaluations
    ax1 = fig.add_subplot(gs[0, 1])
    ev_sa = [3.0e6, 3.0e6, 3.0e6]
    ev_cbls = [1.582e10, 1.488e10, 3.484e11]
    ev_base = [1.848e10, 1.379e10, 3.600e11]
    ev_bili = [1.021e9, 7.332e8, 1.879e10]

    ax1.bar(x - 1.5 * w, ev_sa, w, color="#cbd5e1", edgecolor="#475569", hatch="//")
    ax1.bar(x - 0.5 * w, ev_cbls, w, color="#fdae61", edgecolor="#9c2f00", hatch="..")
    ax1.bar(x + 0.5 * w, ev_base, w, color="#2b5c8f", edgecolor="#16324f")
    ax1.bar(x + 1.5 * w, ev_bili, w, color="#1b9e77", edgecolor="#0f6648", linewidth=1.2)

    ax1.set_yscale("log")
    ax1.set_ylim(3e5, 3e12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(orders_lbl, fontsize=7.6)
    ax1.set_ylabel("Total operator evaluations")
    ax1.set_title("(b) Compute Competition: Operator Evaluations", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

    # Panel (c): Final Residual Energy H_line
    ax2 = fig.add_subplot(gs[0, 2])
    e_sa_m = [124.0, 124.0, 3148.0]
    e_cbls_m = [30.7, 10.7, 50.7]

    ax2.bar(x - 1.5 * w, [e + 0.5 for e in e_sa_m], w, color="#cbd5e1", edgecolor="#475569", hatch="//")
    ax2.bar(x - 0.5 * w, [e + 0.5 for e in e_cbls_m], w, color="#fdae61", edgecolor="#9c2f00", hatch="..")
    ax2.bar(x + 0.5 * w, [0.5, 0.5, 0.5], w, color="#2b5c8f", edgecolor="#16324f")
    ax2.bar(x + 1.5 * w, [0.5, 0.5, 0.5], w, color="#1b9e77", edgecolor="#0f6648", linewidth=1.2)

    ax2.axhline(8.0, color="#b2182b", linestyle=":", linewidth=1.4, label=r"Trap threshold ($\mathcal{H}_{\mathrm{line}} = 8$)")
    ax2.set_yscale("log")
    ax2.set_ylim(0.35, 8000.0)
    ax2.set_yticks([0.5, 2, 8, 32, 128, 512, 2048])
    ax2.set_yticklabels(["$0$ (MAGIC)", "$2$", "$8$", "$32$", "$128$", "$512$", "2,048"], fontsize=7.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(orders_lbl, fontsize=7.6)
    ax2.set_ylabel("Mean final residual energy $\\mathcal{H}_{\\mathrm{line}}(S_\\infty)$")
    ax2.set_title("(c) Endgame Trap Barrier vs. Exact Escape", fontweight="bold", pad=8)
    ax2.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax2.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=6.3)

    save_fig(fig, "fig9_competition_46_48_100")


def main() -> None:
    print("=== Generating Publication Figures for Paper D ===")
    data = json.loads(RESULTS_JSON.read_text(encoding="utf-8"))
    make_fig1_spectral(data)
    make_fig2_window_entropy(data)
    make_fig3_octupole_complement(data)
    make_fig4_s9_landscape()
    make_fig5_s16_descent(data)
    make_fig6_bubble_trinity(data)
    make_fig7_dimensional_relief(data)
    make_fig8_scan_3_to_50(data)
    make_fig9_competition_46_48_100(data)
    print("All 9 Paper D figures generated successfully!")


if __name__ == "__main__":
    main()
