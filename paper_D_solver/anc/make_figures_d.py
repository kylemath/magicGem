#!/usr/bin/env python3
"""Publication figure generator for Paper D:
'Can Physical Forces Find a Magic Square? Spectral Energy Landscapes,
Window Entropies, and Interactive Relaxation Dynamics' (Kyle Elliott Mathewson).

Generates 7 300-DPI publication figures (.pdf and .png) in paper_D_solver/figures/:
  - fig1_spectral_operator.pdf/.png
  - fig2_window_entropy_880.pdf/.png
  - fig3_octupole_complement.pdf/.png
  - fig4_s9_landscape_traps.pdf/.png
  - fig5_s16_descent_basins.pdf/.png
  - fig6_bubble_trinity_regimes.pdf/.png
  - fig7_multi_order_dimensional_relief.pdf/.png
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

HALO = dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.88)


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
                    label=r"Unprojected $L_n$ ($\lambda_{\pm} \notin \mathbb{Z}$)" if idx == 0 and ev > n else None,
                )
                y_off = 8 if ev > n else -12
                ax0.annotate(
                    f"{ev:.2f}", (n - 0.15, ev), xytext=(0, y_off),
                    textcoords="offset points", ha="center", va="center",
                    fontsize=6.8, color="#b34800", fontweight="bold", bbox=HALO, zorder=6,
                )

        # Plot rationalized zero-mean eigenvalues (filled navy/green circles)
        for ev, mult in zmean.items():
            s_size = 38 + 3.2 * min(mult, 25)
            color = "#1b9e77" if ev == 0 else "#2b5c8f"
            ax0.scatter(
                n + 0.10, ev, s=s_size, marker="o", color=color,
                edgecolors="white", linewidths=0.7, zorder=5,
                label=(r"Zero-mean $\widetilde{L}_n|_{\mathbf{1}^\perp}$ ($\mu \in \mathbb{Z}$)" if idx == 0 and ev == n else
                       (r"Magic kernel ($\mu=0$, mult $n^2-2n-1$)" if idx == 0 and ev == 0 else None)),
            )
            ev_int = int(round(ev))
            if n == 3 and ev_int == 2:
                xy_off = (6, -6)
            elif n == 3 and ev_int == 3:
                xy_off = (6, 5)
            elif ev_int == 2:
                xy_off = (6, 6)
            elif ev_int == 0:
                xy_off = (6, 0)
            elif n in (7, 8) and ev_int == 6:
                xy_off = (6, -5)
            else:
                xy_off = (6, 3)
            ax0.annotate(
                f"{ev_int}$^{{[{mult}]}}$", (n + 0.13, ev),
                xytext=xy_off, textcoords="offset points", va="center", fontsize=7.3,
                color="#0f3c66" if ev > 0 else "#0f6648", fontweight="bold", bbox=HALO, zorder=6,
            )

    # Mean eigenvalue line \bar{\mu} = 2
    ax0.axhline(2.0, color="#7570b3", linestyle="--", linewidth=1.4, zorder=2,
                label=r"Universal mean eigenvalue $\bar{\mu}(\widetilde{L}_n) = 2$")
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
    ax1.plot([-0.38, 3.38], [-0.38, 3.38], color="#ffd166", linestyle="--", linewidth=2.0, alpha=0.85, zorder=2)
    ax1.plot([3.38, -0.38], [-0.38, 3.38], color="#ffd166", linestyle="--", linewidth=2.0, alpha=0.85, zorder=2)

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
        ax1.text(3.60, r, f"$\\Sigma={s_row}$\n($R_{{r{r+1}}}={rz:+d}$)", va="center", ha="left",
                 fontsize=7.3, color="#b2182b", fontweight="bold")
    for c, cz in enumerate(cols_z):
        s_col = int(np.sum(sq[:, c]))
        ax1.text(c, 3.60, f"$\\Sigma={s_col}$\n($R_{{c{c+1}}}={cz:+d}$)", va="top", ha="center",
                 fontsize=7.2, color="#b2182b", fontweight="bold")

    # Unified diagonal sum badge in bottom-right corner (zero overlap with top banner!)
    ax1.text(3.60, 3.60, "$D_\\pm: \\Sigma=34$\n($R_{D_\\pm}=0$)", va="top", ha="left",
             fontsize=7.1, color="#0f6648", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.18", facecolor="#eefaf4", edgecolor="#1b9e77"))

    # Top banner summarizing low-mode balance vs hidden polynomial waves
    ax1.text(
        1.5, -0.82,
        r"Balanced Tilt & Diagonals: $\langle X,Z\rangle = \langle Y,Z\rangle = R_{D_\pm} = 0 \Rightarrow E_{\mathrm{low}} = 0$"
        + "\n"
        + r"Unchecked Quadratic/Cubic Waves ($2n-4=4\mathrm{D}$): $\mathcal{H}_{\mathrm{line}}(S_{\mathrm{low}}) = 1,584 > 0$",
        ha="center", va="center", fontsize=7.1, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff5f5", edgecolor="#b2182b"),
    )

    x_coords = [-3, -1, +1, +3]
    y_coords = [+3, +1, -1, -3]
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_xticklabels([f"Col {j+1}\n($X={x_coords[j]:+d}$)" for j in range(4)], fontsize=7.4)
    ax1.set_yticklabels([f"Row {i+1}\n($Y={y_coords[i]:+d}$)" for i in range(4)], fontsize=7.4)
    ax1.set_xlim(-0.55, 4.75)
    ax1.set_ylim(4.32, -1.22)
    for sp in ("top", "right", "bottom", "left"):
        ax1.spines[sp].set_visible(False)
    ax1.set_title(r"(b) The Balanced $4\times 4$ Impostor Square $S_{\mathrm{low}}$", fontweight="bold", pad=10)

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
        ("Lo Shu ($n=3$, odd)", siamese_magic(3), "#1b9e77", "o"),
        ("Doubly-Even ($n=4$, $4k$)", doubly_even_magic(4), "#2b5c8f", "s"),
        ("Siamese ($n=5$, odd)", siamese_magic(5), "#d95f02", "^"),
        ("Conway LUX ($n=6$, $4k+2$)", lux_singly_even_magic(6), "#e7298a", "D"),
        ("Doubly-Even ($n=8$, $4k$)", doubly_even_magic(8), "#7570b3", "v"),
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

    # Place callout in the open upper-left region of Panel (a) so it never collides with the lower-right legend
    ax0.annotate(
        "Hollow markers at $k=2$:\n$\\widetilde{H}_2(2)$ drops to $0.915$ ($n=4$)\n& $0.906$ ($n=8$) from corner clustering",
        xy=(0.25, 0.906), xytext=(0.12, 0.980),
        arrowprops=dict(arrowstyle="->", color="#7570b3", lw=1.1),
        fontsize=6.6, color="#0f3c66", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#f0f4f8", edgecolor="#2b5c8f"),
    )
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
                label="Groups II, IV–V, VII–XII ($N=480$)")
    ax1.scatter([x["w2_non_tor"] for x in pts_g6], [x["Hnorm_p1_k2"] for x in pts_g6],
                s=18, marker="o", color="#6baed6", alpha=0.60, zorder=3,
                label="Group VI ($N=304$, generic)")
    ax1.scatter([x["w2_non_tor"] for x in pts_g3], [x["Hnorm_p1_k2"] for x in pts_g3],
                s=30, marker="s", color="#1b9e77", alpha=0.88, zorder=5,
                label=r"Group III (Associative, $N=48$, $B_{\mathrm{comp}}=0$)")
    ax1.scatter([x["w2_non_tor"] for x in pts_g1], [x["Hnorm_p1_k2"] for x in pts_g1],
                s=38, marker="o", color="#d95f02", edgecolors="black", linewidths=0.6, zorder=6,
                label=r"Group I (Panmagic, $N=48$, $W_{2\times 2}=0$)")

    # Highlight extremal squares #123 (max entropy) and #599 (min entropy)
    sq123_meta = next(x for x in per_sq if x["id"] == 123)
    sq599_meta = next(x for x in per_sq if x["id"] == 599)
    ax1.scatter([sq123_meta["w2_non_tor"]], [sq123_meta["Hnorm_p1_k2"]],
                s=75, marker="*", color="#e7298a", edgecolors="black", linewidths=0.6, zorder=8)
    ax1.scatter([sq599_meta["w2_non_tor"]], [sq599_meta["Hnorm_p1_k2"]],
                s=65, marker="v", color="#b2182b", edgecolors="black", linewidths=0.6, zorder=8)

    ax1.annotate(
        f"Max #123 ($\\widetilde{{H}}_1(2)=0.9997$)",
        xy=(sq123_meta["w2_non_tor"], sq123_meta["Hnorm_p1_k2"]),
        xytext=(820, 0.9990),
        arrowprops=dict(arrowstyle="->", color="#e7298a", lw=1.1),
        fontsize=6.8, fontweight="bold", color="#a8135d", bbox=HALO, zorder=9,
    )
    # Place Min #599 label in the bottom-left space so it never touches the lower-right legend!
    ax1.annotate(
        f"Min #599\n($\\widetilde{{H}}_1(2)=0.9403$)",
        xy=(sq599_meta["w2_non_tor"], sq599_meta["Hnorm_p1_k2"]),
        xytext=(35, 0.9415),
        arrowprops=dict(arrowstyle="->", color="#b2182b", lw=1.1),
        fontsize=6.8, fontweight="bold", color="#8c1120", bbox=HALO, zorder=9,
    )

    ax1.axvline(0, color="#d95f02", linestyle="--", linewidth=1.2, alpha=0.85)
    ax1.annotate(
        "Lemma 3.1: 48 Panmagic\n$W_{2\\times 2}^{\\mathrm{int}} = W_{2\\times 2}^{\\mathrm{tor}} = 0$",
        xy=(10, 0.971), xytext=(80, 0.956),
        arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.2),
        fontsize=6.8, fontweight="bold", color="#b34800",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#fff5eb", edgecolor="#d95f02"),
    )
    ax1.set_xlabel(r"Interior $2\times 2$ quartet energy $W_{2\times 2}^{\mathrm{int}}(S) = \sum_{r,c=1}^{3} Q_{rc}(S)^2$")
    ax1.set_ylabel(r"Normalized $2\times 2$ window entropy $\widetilde{H}_1(2)$")
    ax1.set_ylim(0.936, 1.004)
    ax1.set_title(r"(b) $2\times 2$ Quartet Energy vs. Entropy ($880$ Squares)", fontweight="bold", pad=8)
    ax1.grid(True, linestyle=":", alpha=0.45)
    ax1.legend(loc="lower right", frameon=True, framealpha=0.94, fontsize=6.6)

    # Panel (c): Visual 4x4 board textures comparing Max Entropy #123 vs Min Entropy #599
    gs_c = gs[0, 2].subgridspec(2, 1, hspace=0.38)
    for sub_idx, (sq_id, title_tag, border_col) in enumerate([
        (123, r"(c1) Max Entropy #123 ($\widetilde{H}_1(2)=0.9997$)", "#1b9e77"),
        (599, r"(c2) Min Entropy #599 ($\widetilde{H}_1(2)=0.9403$)", "#b2182b"),
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

        # Annotate corner 2x2 window L1 weights w_1(W_{1,1}) and w_1(W_{3,3})
        w_tl = int(np.sum(z_abs[0:2, 0:2]))
        w_br = int(np.sum(z_abs[2:4, 2:4]))
        rect_tl = mpatches.Rectangle((-0.46, -0.46), 1.92, 1.92, fill=False, edgecolor=border_col, linewidth=1.8, linestyle="-")
        rect_br = mpatches.Rectangle((1.54, 1.54), 1.92, 1.92, fill=False, edgecolor="#2b5c8f", linewidth=1.8, linestyle="--")
        ax_c.add_patch(rect_tl)
        ax_c.add_patch(rect_br)
        ax_c.text(3.62, 0.5, f"Top-L $2\\times 2$:\n$w_1={w_tl}$", va="center", ha="left",
                  fontsize=6.8, fontweight="bold", color=border_col)
        ax_c.text(3.62, 2.5, f"Bot-R $2\\times 2$:\n$w_1={w_br}$", va="center", ha="left",
                  fontsize=6.8, fontweight="bold", color="#2b5c8f")

        ax_c.set_xticks([])
        ax_c.set_yticks([])
        ax_c.set_xlim(-0.55, 5.35)
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
    ax0.bar(x - w / 2, mean_int, width=w, color="#2b5c8f", label=r"Mean Interior $W_{2\times 2}^{\mathrm{int}}$ (9 windows)")
    ax0.bar(x + w / 2, mean_tor, width=w, color="#66a61e", alpha=0.88, label=r"Mean Toroidal $W_{2\times 2}^{\mathrm{tor}}$ (16 windows)")

    # Reference lines at ||z||^2 = 1360 and 2||z||^2 = 2720
    ax0.axhline(1360, color="#1a3a5c", linestyle="--", linewidth=1.1, alpha=0.8,
                label=r"$\|\mathbf{z}\|^2 = 1,360$ (Groups II, III, V)")
    ax0.axhline(2720, color="#3d6611", linestyle=":", linewidth=1.2, alpha=0.8,
                label=r"$2\|\mathbf{z}\|^2 = 2,720$ (Groups II, III, V)")
    ax0.annotate(
        "Group I:\n$W_{2\\times 2}=0$",
        xy=(0, 20), xytext=(0.4, 620),
        arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.1),
        fontsize=6.9, fontweight="bold", color="#b34800", bbox=HALO,
    )

    ax0.set_xticks(x)
    ax0.set_xticklabels(roman, fontsize=7.6)
    ax0.set_ylim(0, 4100)
    ax0.set_xlabel("Dudeney Group (I--XII)")
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
    ax1.scatter([2], [0], s=75, marker="o", color="#1b9e77", edgecolors="black", linewidths=0.8, zorder=6)
    ax1.scatter([8, 9], [0, 0], s=75, marker="*", color="#e7298a", edgecolors="black", linewidths=0.7, zorder=6)

    ax1.axhline(0, color="#1b9e77", linestyle="--", lw=1.1)
    ax1.annotate(
        "48 Associative Zeros (Group III):\n$B_{\\mathrm{comp}}=0 \\Rightarrow Q_{\\mathrm{corner}}=Q_{\\mathrm{edge}}=0$",
        xy=(2, 6), xytext=(0.05, 415),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.2),
        fontsize=6.7, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )
    ax1.annotate(
        "8 Non-Assoc. Zeros (IX & X):\n$B_{\\mathrm{comp}}=8, 8Q_{\\mathrm{corner}} = -3Q_{\\mathrm{edge}}$",
        xy=(8.5, 6), xytext=(3.8, 330),
        arrowprops=dict(arrowstyle="->", color="#e7298a", lw=1.2),
        fontsize=6.7, fontweight="bold", color="#a8135d",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#fdf0f6", edgecolor="#e7298a"),
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(roman, fontsize=7.6)
    ax1.set_xlabel("Dudeney Group (I--XII)")
    ax1.set_ylabel(r"Octupole magnitude $|M_{xyz}(S)| = |\sum X_j Y_i Z_{ij}|$")
    ax1.set_ylim(-24, 485)
    ax1.set_title(r"(b) Octupole Census & the $48+8=56$ Zeros", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

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

    ax2.text(
        1.5, 4.18,
        r"Prop. 3.2 on #208 (Group IX, $B_{\mathrm{comp}}=8$):" + "\n"
        + r"Corners ($\pm 9$): $Q_{\mathrm{corner}} = -12$, Inner ($\pm 1$): $Q_{\mathrm{inner}} = +12$" + "\n"
        + r"Edges ($\pm 3$): $Q_{\mathrm{edge}} = +32 \Rightarrow M_{xyz} = -8(-12) - 3(32) = 0$",
        ha="center", va="top", fontsize=6.4, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.22", facecolor="#fdf0f6", edgecolor="#e7298a"),
    )
    ax2.set_xticks(range(4))
    ax2.set_yticks(range(4))
    ax2.set_xticklabels([f"$X={x:+d}$" for x in X_c], fontsize=7.0)
    ax2.set_yticklabels([f"$Y={y:+d}$" for y in Y_r], fontsize=7.0)
    ax2.set_xlim(-0.55, 3.55)
    ax2.set_ylim(5.15, -0.55)
    for sp in ("top", "right", "bottom", "left"):
        ax2.spines[sp].set_visible(False)
    ax2.set_title("(c) Concentric Shell Identity (#208)", fontweight="bold", pad=8)

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
                label=r"Ensemble mean $\mathbb{E}[\mathcal{H}_{\mathrm{line}}] = 2\|\mathbf{z}\|^2 = 480$")
    ax0.axvline(0.0, color="#1b9e77", linestyle="-", linewidth=1.8,
                label=r"8 Lo Shu ground states ($\mathcal{H}_{\mathrm{line}}=0$, $74.53\%$)")
    ax0.axvline(8.0, color="#e7298a", linestyle=":", linewidth=1.8,
                label=r"8 Antipodal traps $S_{\mathrm{trap}}^{(3)}$ ($\mathcal{H}_{\mathrm{line}}=8$, $25.47\%$)")
    ax0.axvline(720.0, color="#7570b3", linestyle="-.", linewidth=1.4,
                label=r"Global maximum $\max_{S\in S_9}\mathcal{H}_{\mathrm{line}}(S) = 720$")

    ax0.set_xlabel(r"Centred line-indicator Hamiltonian $\mathcal{H}_{\mathrm{line}}(S) = \mathbf{z}^\top L_3 \mathbf{z}$")
    ax0.set_ylabel(r"Number of permutations in $S_9$ ($9! = 362,880$)")
    ax0.set_xlim(-22, 790)
    ax0.set_ylim(0, 37500)
    ax0.set_title(r"(a) Exhaustive $S_9$ Energy Landscape ($362,880$ States)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=6.9)

    # Inset zooming in on low-energy states H_line in {0, 4, 8, 12, 16, 20, 24} with white background card
    ax_ins = ax0.inset_axes([0.14, 0.36, 0.42, 0.32])
    ax_ins.patch.set_facecolor("white")
    ax_ins.patch.set_alpha(0.96)
    low_H_vals = [0, 4, 8, 12, 16, 20, 24]
    low_counts = [int(np.sum(H_all == h)) for h in low_H_vals]
    bar_cols = ["#1b9e77" if h == 0 else ("#e7298a" if h == 8 else "#6baed6") for h in low_H_vals]
    x_ins = np.arange(len(low_H_vals))
    ax_ins.bar(x_ins, low_counts, color=bar_cols, edgecolor="white", width=0.68)
    ax_ins.set_xticks(x_ins)
    ax_ins.set_xticklabels([str(h) for h in low_H_vals])
    for idx_h, (h_v, cnt) in enumerate(zip(low_H_vals, low_counts)):
        ax_ins.text(idx_h, cnt + 6, f"{cnt}", ha="center", va="bottom", fontsize=6.2, fontweight="bold")
    ax_ins.set_ylim(0, 195)
    ax_ins.set_title(r"Low-Energy Zoom ($\mathcal{H}_{\mathrm{line}} \leq 24$)", fontsize=6.8, fontweight="bold", pad=2)
    ax_ins.set_xlabel(r"$\mathcal{H}_{\mathrm{line}}$ (0 states at $\mathcal{H}=4$)", fontsize=6.2, labelpad=1, bbox=HALO)
    ax_ins.tick_params(labelsize=6.0)

    # Panel (b): 3-Stage Unlocking Transition S_trap^(3) (H=8) -> Saddle (H=12) -> S_LoShu (H=0)
    gs_b = gs[0, 1].subgridspec(2, 3, height_ratios=[1.35, 0.55], wspace=0.28, hspace=0.28)
    boards = [
        (
            np.array([[2, 6, 7], [9, 5, 1], [3, 4, 8]], dtype=int),
            r"1. Trap $S_{\mathrm{trap}}^{(3)}$ ($\mathcal{H}_{\mathrm{line}}=8$)",
            "#e7298a",
            [(0, 1), (0, 2)],
            "Cols: $14, 15, 16$\nAll $2$- & $3$-cycles fail",
        ),
        (
            np.array([[2, 7, 6], [9, 5, 1], [3, 4, 8]], dtype=int),
            r"2. Saddle $\tau_1 S_{\mathrm{trap}}^{(3)}$ ($\mathcal{H}^\ddagger=12$)",
            "#d95f02",
            [(2, 0), (2, 1)],
            "After $\\tau_1=(6\\leftrightarrow 7)$:\n$C_1=14, C_2=16, D_-=14$",
        ),
        (
            np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]], dtype=int),
            r"3. Ground State $S_{\mathrm{LoShu}}$ ($\mathcal{H}=0$)",
            "#1b9e77",
            [],
            "After $\\tau_2=(3\\leftrightarrow 4)$:\nAll 8 lines sum to $15$",
        ),
    ]

    for b_idx, (b_mat, b_title, b_col, swap_cells, b_sub) in enumerate(boards):
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
                    bbox=dict(boxstyle="circle,pad=0.18", facecolor="white", edgecolor=b_col, lw=1.6) if is_hi else None,
                )
        for c in range(3):
            csum = int(np.sum(b_mat[:, c]))
            ccol = "#1b9e77" if csum == 15 else "#d95f02"
            ax_b.text(c, 2.68, f"$\\Sigma={csum}$", ha="center", va="top", fontsize=7.0, fontweight="bold", color=ccol)

        ax_b.text(1.0, 3.35, b_sub, ha="center", va="top", fontsize=6.8, color="#222222",
                  bbox=dict(boxstyle="round,pad=0.20", facecolor="#f8f9fa", edgecolor=b_col, lw=1.1))
        ax_b.set_xticks([])
        ax_b.set_yticks([])
        ax_b.set_xlim(-0.55, 2.55)
        ax_b.set_ylim(4.25, -0.55)
        for sp in ("top", "right", "bottom", "left"):
            ax_b.spines[sp].set_visible(True)
            ax_b.spines[sp].set_color(b_col)
            ax_b.spines[sp].set_linewidth(1.3)
        ax_b.set_title(b_title, fontsize=8.0, fontweight="bold", color=b_col, pad=5)

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
    ax_rc.annotate(r"Trap $\mathcal{H}=8$", (0, 8), xytext=(10, 4), textcoords="offset points",
                   fontsize=7.2, fontweight="bold", color="#a8135d", bbox=HALO)
    ax_rc.annotate(r"Single-Swap Saddle $\mathcal{H}^\ddagger=12$ ($\Delta\mathcal{H}^\ddagger=+4$)",
                   (1, 12), xytext=(0, 5), textcoords="offset points", ha="center",
                   fontsize=7.2, fontweight="bold", color="#b34800", bbox=HALO)
    ax_rc.annotate(r"Lo Shu $\mathcal{H}=0$ ($100\%$ basin)", (2, 0), xytext=(-10, 6), textcoords="offset points",
                   ha="right", fontsize=7.2, fontweight="bold", color="#0f6648", bbox=HALO)
    ax_rc.set_xlim(-0.2, 2.2)
    ax_rc.set_ylim(-1.5, 17.5)
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
        color="#d95f02", alpha=0.18, label=r"Trapped 20%–80% envelope ($81.75\%$ of starts)"
    )
    ax0.fill_between(
        steps_arr, np.percentile(mat_magic, 20, axis=0), np.percentile(mat_magic, 80, axis=0),
        color="#1b9e77", alpha=0.18, label=r"Ground-state 20%–80% envelope ($18.25\%$ of starts)"
    )

    for i, c in enumerate(trajs_trapped[:6]):
        y_c = np.array(c) + 4.0
        ax0.plot(range(len(c)), y_c, color="#d95f02", alpha=0.80, lw=1.3)
        ax0.scatter([len(c) - 1], [y_c[-1]], s=28, marker="o", color="#b34800", edgecolors="white", linewidths=0.6, zorder=6,
                    label=r"Trapped local minimum halt ($\Delta\mathcal{H}_{\mathrm{line}} > 0$)" if i == 0 else None)

    for i, c in enumerate(trajs_magic[:6]):
        y_c = np.array(c) + 4.0
        ax0.plot(range(len(c)), y_c, color="#1b9e77", alpha=0.88, lw=1.5)
        ax0.scatter([len(c) - 1], [y_c[-1]], s=34, marker="*", color="#0f6648", zorder=6,
                    label=r"Magic ground state reached ($\mathcal{H}_{\mathrm{line}} = 0$)" if i == 0 else None)

    ax0.axhspan(12.0, 20.0, color="#ffd166", alpha=0.22, zorder=1)
    ax0.axhline(4.0, color="#1b9e77", linestyle="--", linewidth=1.3, zorder=2)
    ax0.text(0.3, 4.35, r"Magic Ground State $\mathcal{H}_{\mathrm{line}} = 0$", fontsize=7.1, fontweight="bold", color="#0f6648", bbox=HALO)
    ax0.text(0.3, 14.5, r"Dominant Trap Band $\mathcal{H}_{\mathrm{line}} \in \{8,12,16\}$", fontsize=7.0, fontweight="bold", color="#9c2f00")

    ax0.set_yscale("log")
    ax0.set_yticks([4, 12, 20, 104, 1004, 2724])
    ax0.set_yticklabels([r"$0$", r"$8$", r"$16$", r"$100$", r"$1,000$", r"$2,720$"])
    ax0.set_xlim(-0.2, 14.5)
    ax0.set_ylim(3.2, 5500)
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
    ax1.bar(x_idx, vs, color=colors, edgecolor="white", width=0.74, label=r"Terminal $2$-cycle local minima ($2,000$ trials)")
    ax1.bar(x_idx, esc_vs, color="#2b5c8f", edgecolor="white", width=0.74, hatch="//", alpha=0.85,
            label=r"Unlocked by a single $(2,2)$ plaquette move ($16.6\%$ of traps)")

    for idx, (k, v) in enumerate(zip(ks, vs)):
        if v >= 30:
            ax1.text(idx, v + 7, f"{v}", ha="center", va="bottom", fontsize=7.1, fontweight="bold", bbox=HALO)

    ax1.annotate(
        "Ground-state basin:\n$365/2,000$ ($18.25\\%$)\n$\\to 509/2,000$ ($25.45\\%$)\nwith $(2,2)$ plaquettes",
        xy=(0, 365), xytext=(3.8, 395),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.3),
        fontsize=7.2, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )
    ax1.annotate(
        "Frustration band $\\mathcal{H}_{\\mathrm{line}} \\in \\{8, 12, 16\\}$:\n$1,142/2,000$ ($57.1\\%$) of starts;\n$(2,2)$ escapes $4.8\\times$ more traps than $3$-cycles",
        xy=(2, 305), xytext=(4.3, 245),
        arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.3),
        fontsize=7.1, fontweight="bold", color="#b34800",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="#fff5eb", edgecolor="#d95f02"),
    )
    ax1.set_xticks(x_idx)
    ax1.set_xticklabels([str(k) for k in ks], fontsize=7.6)
    ax1.set_ylim(0, 545)
    ax1.set_xlabel(r"Terminal $2$-cycle local-minimum energy $\mathcal{H}_{\mathrm{line}}(S_\infty)$")
    ax1.set_ylabel("Count out of $2,000$ uniform random starts")
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
        "I_Frozen_Lattice": ("I. Frozen Lattice ($k_w=7.0, k_f=0$)", "#7570b3", "--", "s"),
        "II_Slow_Drift": ("II. Slow Drift ($k_w=2.6, k_f=1.0$)", "#2b5c8f", "-.", "^"),
        "III_Field_Storm": ("III. Field Storm ($k_w=0.8, k_f=3.2$)", "#d95f02", "-", "o"),
        "IV_Centrifugal_Balance": ("IV. Centrifugal Balance ($k_s=0.85$)", "#1b9e77", "-", "D"),
    }
    steps = [10 * i for i in range(25)]
    for key, (label, col, ls, mk) in styles.items():
        y = regimes[key]["trajectory_H_decimated"]
        ax0.plot(steps, y, color=col, linestyle=ls, marker=mk, markersize=4.2,
                 markevery=3, linewidth=1.7, label=label)

    y_iv = np.array(regimes["IV_Centrifugal_Balance"]["trajectory_H_decimated"])
    ax0.axhline(2336, color="#b2182b", linestyle="--", linewidth=1.4,
                label=r"Discrete Hungarian snap $\mathcal{H}_{\mathrm{line}} = 2,336$ ($0\%$)")
    ax0.axhline(1480, color="#e7298a", linestyle=":", linewidth=1.3,
                label=r"Min greedy snap $\min\mathcal{H}_{\mathrm{line}} = 1,480$ ($0\%$)")
    ax0.fill_between(steps, y_iv, 2336, color="#b2182b", alpha=0.08)

    ax0.annotate(
        "Amplitude-Averaging Gap:\n$\\mathcal{H}_{\\mathrm{ind}}(t)$ drops $37.5\\%$ via border blending,\nyet discrete Hungarian snap stays at $2,336$",
        xy=(160, 1125), xytext=(15, 1850),
        arrowprops=dict(arrowstyle="->", color="#b2182b", lw=1.2),
        fontsize=6.5, fontweight="bold", color="#8c1120",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#fff5f5", edgecolor="#b2182b"),
    )

    ax0.set_ylim(980, 2500)
    ax0.set_xlabel(r"Continuous integration step $t$ ($\Delta t = 0.025$)")
    ax0.set_ylabel(r"Continuous $\mathcal{H}_{\mathrm{ind}}(t)$ vs. Discrete $\mathcal{H}_{\mathrm{line}}$")
    ax0.set_title(r"(a) Kernel Drift vs. Discrete Snap Reality", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="lower left", frameon=True, framealpha=0.92, fontsize=6.3)

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
    ax_b.set_xlabel("Bubbles park on cell borders to blend\n$+Z$ (red) & $-Z$ (blue) without swapping",
                    fontsize=6.8, fontweight="bold", color="#8c1120", labelpad=6)
    ax_b.set_title("(b) Preset IV Border-Parking", fontweight="bold", pad=8)

    # Panel (c): Operator Ablation Hierarchy with concise labels so there is zero cross-panel overlap
    ax1 = fig.add_subplot(gs[0, 2])
    tiers = [
        ("0_continuous_2d_greedy_snap_pct", "Tier 0: 2D Bubble Drift\n(Greedy & Hungarian)"),
        ("1_kawasaki_2cycle_quench_pct", "Tier 1: $2$-Exchange Quench\n(Pair swaps)"),
        ("2_vacancy_3cycle_sa_pct", "Tier 2: $(2+3)$-Cycle SA\n(Thermal walk)"),
        ("3_spin_ice_lp22_quench_pct", "Tier 3: $+$ $(2,2)$ Plaquette\n(Row/col 4-loops)"),
        ("4_t1_eshelby_6kicks_pct", "Tier 4: $+$ Cand. $(2,2)$\n(& Row/col swaps)"),
        ("5_plane_glide_18kicks_pct", "Tier 5: $+$ Funnel Leash\n(Tethered kicks)"),
        ("6_wales_doye_reanchored_full_pct", "Tier 6: $+$ ME-ILS\n($\\leq 80$ restarts)"),
    ]
    y_pos = np.arange(len(tiers))
    n4_rates = [ablation["n4"][k] for k, _ in tiers]
    n5_rates = [ablation["n5"][k] for k, _ in tiers]

    ax1.axhspan(-0.5, 2.5, color="#fff5eb", alpha=0.55, zorder=0)
    ax1.axhspan(2.5, 6.5, color="#eefaf4", alpha=0.55, zorder=0)

    h = 0.36
    ax1.barh(y_pos - h / 2, n4_rates, height=h, color="#2b5c8f", edgecolor="white",
             label="Order $n=4$ ($S_{16}$, $200$ trials)", zorder=3)
    ax1.barh(y_pos + h / 2, n5_rates, height=h, color="#1b9e77", edgecolor="white",
             label="Order $n=5$ ($S_{25}$, $100$ trials)", zorder=3)

    for idx, (r4, r5) in enumerate(zip(n4_rates, n5_rates)):
        c4 = "#8c1120" if r4 == 0 else ("#0f3c66" if r4 < 100 else "#0f6648")
        fw = "bold" if r4 in (0.0, 100.0) else "normal"
        ax1.text(r4 + 1.4, idx - h / 2, f"{r4:.1f}%", va="center", ha="left",
                 fontsize=7.0, color=c4, fontweight=fw, bbox=HALO, zorder=4)
        ax1.text(r5 + 1.4, idx + h / 2, f"{r5:.1f}%", va="center", ha="left",
                 fontsize=7.0, color="#0f6648" if r5 == 100 else "#b34800",
                 fontweight="bold" if r5 == 100 else "normal", bbox=HALO, zorder=4)

    ax1.axhline(2.5, color="#d95f02", linestyle="--", linewidth=1.2, alpha=0.85, zorder=4)
    ax1.text(118, 1.85, "Tiers 0–2: Baselines", fontsize=6.7, color="#b34800", fontweight="bold", ha="right")
    ax1.text(118, 3.15, "Tiers 3–6: Multi-Exchange", fontsize=6.7, color="#0f6648", fontweight="bold", ha="right")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([lbl for _, lbl in tiers], fontsize=6.9)
    ax1.invert_yaxis()
    ax1.set_xlim(0, 122)
    ax1.set_ylim(6.5, -0.5)
    ax1.set_xlabel(r"Ground-state synthesis rate ($\mathcal{H}_{\mathrm{line}}=0$, %)")
    ax1.set_title(r"(c) 6-Tier Operator Ablation ($n=4,5$)", fontweight="bold", pad=8)
    ax1.grid(True, axis="x", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.94, fontsize=6.7)

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
                  linewidth=2.1, label="Mean restarts to $\\mathcal{H}_{\\mathrm{line}}=0$ (left axis)", zorder=4)
    l2 = ax0_r.plot(orders, descents, color="#2b5c8f", linestyle="--", marker="s", markersize=5.2,
                    linewidth=1.8, label="Mean $2$-exchange descents to $\\mathcal{H}_{\\mathrm{line}}=0$ (right axis)", zorder=3)

    for n_val, r_val in zip(orders, restarts):
        if n_val == 3:
            xy_o = (0, 8)
        elif n_val == 4:
            xy_o = (12, -8)
        elif n_val == 5:
            xy_o = (-14, 6)
        elif n_val == 6:
            xy_o = (-14, -10)
        else:
            xy_o = (0, -13)
        ax0.annotate(
            f"{r_val:.2f}", (n_val, r_val), xytext=xy_o, textcoords="offset points",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color="#a8135d", bbox=HALO, zorder=6,
        )

    ax0.annotate(
        "Frustration Peak ($n=5$)\n$\\eta_{\\mathrm{MC}}=1.40$: $8.03$ restarts",
        xy=(5, 8.03), xytext=(5.8, 9.25),
        arrowprops=dict(arrowstyle="->", color="#e7298a", lw=1.2),
        fontsize=6.9, fontweight="bold", color="#a8135d",
        bbox=dict(boxstyle="round,pad=0.22", facecolor="#fdf0f6", edgecolor="#e7298a"),
    )
    ax0.annotate(
        "Nullspace Dimensional Relief ($n\\geq 6$):\n$f_{\\mathrm{null}}(n) = 1 - 2/(n-1)^2 \\to 97.5\\%$\ndrops restarts to $3.34$ at $n=10$",
        xy=(10, 3.34), xytext=(5.5, 0.95),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.2),
        fontsize=6.9, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.22", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )

    ax0.set_xticks(orders)
    ax0.set_xticklabels([f"$n={n}$\n(${eta:.1f}$)" for n, eta in zip(orders, eta_mc)], fontsize=7.4)
    ax0.set_xlim(2.6, 10.4)
    ax0.set_ylim(-0.6, 11.4)
    ax0_r.set_ylim(-35, 630)
    ax0.set_xlabel("Order $n$ and nullspace-to-constraint ratio $\\eta_{\\mathrm{MC}} = (n^2-2n-1)/(2n)$")
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
                     label=r"Magic nullspace $\dim\ker(\widetilde{L}_n) = n^2-2n-1$", zorder=3)
    b_rank = ax1.bar(x + w / 2, rank_vals, width=w, color="#8da0cb", edgecolor="white",
                     label=r"Constraint rank $\mathrm{rank}(\widetilde{L}_n) = 2n$", zorder=3)

    l_time = ax1_r.plot(x + w / 2, times_ms, color="#d95f02", marker="D", markersize=5.0,
                        linewidth=1.9, label="Mean synthesis time per square (ms, right axis)", zorder=5)

    for idx_b, (rect, f_pct) in enumerate(zip(b_null, f_null_pct)):
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2 - 0.04, h + 1.5,
            f"{int(h)}\n({f_pct:.0f}%)",
            ha="center", va="bottom", fontsize=6.2, fontweight="bold", color="#0f6648", bbox=HALO, zorder=6,
        )

    ax1.annotate(
        "Labels on green bars:\n$\\dim\\ker(\\widetilde{L}_n)$ and diagonal-free\n$(2,2)$ fraction $f_{\\mathrm{null}}(n)$ ($50\\%\\to 98\\%$)",
        xy=(4 - w / 2, null_dims[4]), xytext=(0.05, 58),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.1),
        fontsize=6.7, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.20", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"$n={n}$" for n in orders], fontsize=7.8)
    ax1.set_ylim(0, 102)
    ax1_r.set_ylim(0, 1080)
    ax1.set_xlabel("Magic square order $n$ ($100.0\\%$ synthesis across all $n=3\\dots 10$)")
    ax1.set_ylabel("Subspace dimension in $\\mathbf{1}^\\perp \\subset \\mathbb{R}^{n^2-1}$")
    ax1_r.set_ylabel("Mean synthesis time per square (ms)", color="#b34800")
    ax1.set_title("(b) Quadratic Nullspace Expansion & $f_{\\mathrm{null}}(n)$", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax1_r.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left", frameon=True, framealpha=0.94, fontsize=6.7)

    save_fig(fig, "fig7_multi_order_dimensional_relief")


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
    print("All 7 Paper D figures generated successfully!")


if __name__ == "__main__":
    main()
