#!/usr/bin/env python3
"""Publication figure generator for Paper D:
'Spectral Energy Landscapes, Multiscale Window Entropies, and Continuous
Bubble Relaxation of Magic Squares' (Kyle Elliott Mathewson).

Generates 6 300-DPI publication figures (.pdf and .png) in paper_D_solver/figures/:
  - fig1_spectral_operator.pdf/.png
  - fig2_window_entropy_880.pdf/.png
  - fig3_octupole_complement.pdf/.png
  - fig4_s9_landscape_traps.pdf/.png
  - fig5_s16_descent_basins.pdf/.png
  - fig6_bubble_trinity_regimes.pdf/.png
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
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.0,
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

    fig = plt.figure(figsize=(11.6, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.32)

    # Panel (a): Spectrum of unprojected L_n vs zero-mean rationalized \tilde{L}_n
    ax0 = fig.add_subplot(gs[0, 0])
    orders = [3, 4, 5, 6, 7, 8]
    for idx, n in enumerate(orders):
        st = spec_tab[str(n)]
        unproj = {float(k): int(v) for k, v in st["unprojected_eigenvalues"].items()}
        zmean = {float(k): int(v) for k, v in st["zero_mean_eigenvalues"].items()}

        # Plot unprojected irrational eigenvalues (hollow red diamonds)
        for ev, mult in unproj.items():
            if abs(ev - round(ev)) > 1e-3:
                ax0.scatter(
                    n - 0.14, ev, s=55, marker="D", facecolors="none",
                    edgecolors="#d95f02", linewidths=1.5, zorder=4,
                    label=r"Unprojected $L_n$ ($\lambda_{\pm} \notin \mathbb{Z}$)" if idx == 0 and ev > n else None,
                )
                ax0.annotate(
                    f"{ev:.2f}", (n - 0.18, ev), xytext=(-26, -3 if ev < n else 3),
                    textcoords="offset points", fontsize=7.2, color="#b34800",
                )

        # Plot rationalized zero-mean eigenvalues (filled navy circles)
        for ev, mult in zmean.items():
            s_size = 38 + 3.5 * min(mult, 25)
            color = "#1b9e77" if ev == 0 else "#2b5c8f"
            ax0.scatter(
                n + 0.12, ev, s=s_size, marker="o", color=color,
                edgecolors="white", linewidths=0.6, zorder=5,
                label=(r"Zero-mean $\widetilde{L}_n|_{\mathbf{1}^\perp}$ ($\mu \in \mathbb{Z}$)" if idx == 0 and ev == n else
                       (r"Magic kernel ($\mu=0$, mult $n^2-2n-1$)" if idx == 0 and ev == 0 else None)),
            )
            ax0.annotate(
                f"{int(round(ev))}$^{{[{mult}]}}$", (n + 0.17, ev),
                xytext=(3, -3), textcoords="offset points", fontsize=7.5,
                color="#0f3c66" if ev > 0 else "#116649", fontweight="bold",
            )

    # Mean eigenvalue line \bar{\mu} = 2
    ax0.axhline(2.0, color="#7570b3", linestyle="--", linewidth=1.3, zorder=2,
                label=r"Universal mean eigenvalue $\bar{\mu}(\widetilde{L}_n) = 2$")
    ax0.set_xticks(orders)
    ax0.set_xticklabels([f"$n={n}$\n($N={n*n}$)" for n in orders])
    ax0.set_xlim(2.35, 8.8)
    ax0.set_ylim(-1.2, 24.5)
    ax0.set_ylabel(r"Eigenvalue $\lambda(L_n)$ / $\mu(\widetilde{L}_n)$")
    ax0.set_title(r"(a) Spectral Rationalization of $L_n = A_n^\top A_n$ on $\mathbf{1}^\perp$", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=7.6)

    # Panel (b): 4x4 Low-Mode Counterexample S_low
    ax1 = fig.add_subplot(gs[0, 1])
    sq = np.array(low_ex["square"], dtype=int)
    z_sq = 2 * sq - 17
    im = ax1.imshow(z_sq, cmap="RdBu_r", vmin=-16, vmax=16, aspect="equal")
    for r in range(4):
        for c in range(4):
            val = sq[r, c]
            z_v = z_sq[r, c]
            txt_col = "white" if abs(z_v) >= 9 else "#1a1a1a"
            ax1.text(
                c, r, f"{val}\n($Z={z_v:+d}$)",
                ha="center", va="center", fontsize=8.0, color=txt_col, fontweight="bold"
            )

    rows_z = low_ex["rows_Z"]
    cols_z = low_ex["cols_Z"]
    for r, rz in enumerate(rows_z):
        ax1.text(3.68, r, f"$R_{{r{r+1}}}={rz:+d}$", va="center", ha="left",
                 fontsize=8.2, color="#b2182b", fontweight="bold")
    for c, cz in enumerate(cols_z):
        ax1.text(c, 3.68, f"$R_{{c{c+1}}}$\n${cz:+d}$", va="top", ha="center",
                 fontsize=8.0, color="#b2182b", fontweight="bold")

    ax1.text(
        1.5, -0.72,
        r"$\langle X,Z\rangle = 0,\; \langle Y,Z\rangle = 0,\; R_{D_+} = 0,\; R_{D_-} = 0$ ($E_{\mathrm{low}}=0$)"
        + "\n"
        + r"Yet $\mathcal{H}_{\mathrm{line}}(S_{\mathrm{low}}) = \sum R_L^2 = 1,584 > 0$ (5D high-mode residual)",
        ha="center", va="center", fontsize=8.1,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#adb5bd"),
    )
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_xticklabels([f"Col {j+1}" for j in range(4)])
    ax1.set_yticklabels([f"Row {i+1}" for i in range(4)])
    ax1.set_xlim(-0.5, 4.65)
    ax1.set_ylim(4.25, -1.05)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.set_title(r"(b) Order-4 Low-Mode Counterexample $S_{\mathrm{low}}$", fontweight="bold", pad=12)

    save_fig(fig, "fig1_spectral_operator")


def make_fig2_window_entropy(data: dict) -> None:
    sec3 = data["section3_multiscale"]
    per_sq = sec3["per_square_metrics"]

    fig = plt.figure(figsize=(11.8, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.34)

    # Panel (a): Multiscale normalized window entropy H_1(k)/H_max(k) across constructive families
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
        vals = [st[f"Hnorm_p1_k{k}"] for k in ks]
        x_norm = [k / n for k in ks]
        ax0.plot(x_norm, vals, marker=mk, color=col, linewidth=1.7, markersize=5.5, label=label)

    ax0.set_xlabel(r"Relative window scale $k / n$ ($1 \leq k \leq n-1$)")
    ax0.set_ylabel(r"Normalized window entropy $\widetilde{H}_1(k)$")
    ax0.set_ylim(0.89, 1.005)
    ax0.set_title(r"(a) Multiscale Window Entropy ($n=3..8$)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="lower right", frameon=True, framealpha=0.94, fontsize=7.8)

    # Panel (b): Joint census across all 880 order-4 squares of (W_{2x2}^{int}, \widetilde{H}_1(2))
    ax1 = fig.add_subplot(gs[0, 1])
    cmap = plt.get_cmap("tab20")
    for g in range(1, 13):
        pts = [x for x in per_sq if x["group"] == g]
        xs = [x["w2_non_tor"] for x in pts]
        ys = [x["Hnorm_p1_k2"] for x in pts]
        if g == 1:
            ax1.scatter(xs, ys, s=34, color="#d95f02", edgecolors="black", linewidths=0.5,
                        zorder=6, label="Group I (Panmagic, $N=48$, $W_{2\\times 2}=0$)")
        elif g == 3:
            ax1.scatter(xs, ys, s=28, color="#1b9e77", alpha=0.85, zorder=5,
                        label="Group III (Associative, $N=48$, $B_{\\mathrm{comp}}=0$)")
        elif g == 6:
            ax1.scatter(xs, ys, s=16, color="#8da0cb", alpha=0.55, zorder=2,
                        label="Group VI ($N=304$, generic)")
        else:
            ax1.scatter(xs, ys, s=18, color=cmap((g - 1) % 20), alpha=0.65, zorder=3,
                        label=f"Groups II, IV--V, VII--XII" if g == 2 else None)

    ax1.axvline(0, color="#d95f02", linestyle="--", linewidth=1.2, alpha=0.8)
    ax1.annotate(
        "Theorem 3.1:\n48 Group I Panmagic\n$W_{2\\times 2}^{\\mathrm{int}} = W_{2\\times 2}^{\\mathrm{tor}} = 0$",
        xy=(15, 0.970), xytext=(120, 0.946),
        arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.2),
        fontsize=7.5, fontweight="bold", color="#b34800",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff5eb", edgecolor="#d95f02"),
    )
    ax1.set_xlabel(r"Interior $2\times 2$ quartet energy $W_{2\times 2}^{\mathrm{int}}(S) = \sum_{r,c=1}^{3} Q_{rc}(S)^2$")
    ax1.set_ylabel(r"Normalized $2\times 2$ window entropy $\widetilde{H}_1(2)$")
    ax1.set_ylim(0.936, 1.003)
    ax1.set_title(r"(b) $2\times 2$ Quartet Energy vs. Entropy (All 880 Squares)", fontweight="bold", pad=8)
    ax1.grid(True, linestyle=":", alpha=0.45)
    ax1.legend(loc="lower right", frameon=True, framealpha=0.94, fontsize=7.3)

    save_fig(fig, "fig2_window_entropy_880")


def make_fig3_octupole_complement(data: dict) -> None:
    sec3 = data["section3_multiscale"]
    per_sq = sec3["per_square_metrics"]
    grp_sum = sec3["group_summary"]

    fig = plt.figure(figsize=(11.8, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.05], wspace=0.34)

    # Panel (a): Toroidal vs Interior 2x2 Window Energy by Dudeney Group I-XII
    ax0 = fig.add_subplot(gs[0, 0])
    groups = list(range(1, 13))
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    mean_int = [grp_sum[str(g)]["w2_non_tor_mean"] for g in groups]
    mean_tor = [grp_sum[str(g)]["w2_tor_mean"] for g in groups]
    min_int = [grp_sum[str(g)]["w2_non_tor_min"] for g in groups]
    max_int = [grp_sum[str(g)]["w2_non_tor_max"] for g in groups]

    x = np.arange(len(groups))
    w = 0.36
    ax0.bar(x - w / 2, mean_int, width=w, color="#2b5c8f", label=r"Interior $W_{2\times 2}^{\mathrm{int}}$ (9 windows)")
    ax0.bar(x + w / 2, mean_tor, width=w, color="#66a61e", alpha=0.85, label=r"Toroidal $W_{2\times 2}^{\mathrm{tor}}$ (16 windows)")
    ax0.errorbar(
        x - w / 2, mean_int,
        yerr=[np.array(mean_int) - np.array(min_int), np.array(max_int) - np.array(mean_int)],
        fmt="none", ecolor="#1a3a5c", elinewidth=1.0, capsize=2.2,
    )
    ax0.set_xticks(x)
    ax0.set_xticklabels(roman)
    ax0.set_xlabel("Dudeney Group (I--XII)")
    ax0.set_ylabel(r"Mean $2\times 2$ quartet energy (min--max range)")
    ax0.set_title(r"(a) Interior & Toroidal $2\times 2$ Energy by Group", fontweight="bold", pad=8)
    ax0.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax0.legend(loc="upper left", frameon=True, fontsize=7.8)

    # Panel (b): Mixed octupole moment |M_xyz(S)| distribution & anomalous zeros
    ax1 = fig.add_subplot(gs[0, 1])
    rng = np.random.default_rng(12345)
    for g in groups:
        vals = [abs(item["m_xyz"]) for item in per_sq if item["group"] == g]
        jitter = rng.uniform(-0.22, 0.22, size=len(vals))
        col = "#1b9e77" if g == 3 else ("#e7298a" if g in (9, 10) else "#7570b3")
        ax1.scatter(
            np.full(len(vals), g - 1) + jitter, vals,
            s=16, color=col, alpha=0.65,
        )
        ax1.plot([g - 1 - 0.28, g - 1 + 0.28], [np.mean(vals)] * 2, color="black", lw=1.6)

    ax1.axhline(0, color="#1b9e77", linestyle="--", lw=1.1)
    ax1.annotate(
        "Group III (48 associative):\n$B_{\\mathrm{comp}}=0 \\Rightarrow M_{xyz}=0$",
        xy=(2, 4), xytext=(0.1, 415),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.2),
        fontsize=7.6, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )
    ax1.annotate(
        "8 Non-Associative Zeros\n(4 in Group IX, 4 in Group X;\n$B_{\\mathrm{comp}}=8$ yet $M_{xyz}=0$)",
        xy=(8.5, 4), xytext=(5.6, 330),
        arrowprops=dict(arrowstyle="->", color="#e7298a", lw=1.2),
        fontsize=7.6, fontweight="bold", color="#a8135d",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fdf0f6", edgecolor="#e7298a"),
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(roman)
    ax1.set_xlabel("Dudeney Group (I--XII)")
    ax1.set_ylabel(r"Octupole magnitude $|M_{xyz}(S)| = |\sum X_j Y_i Z_{ij}|$")
    ax1.set_ylim(-20, 480)
    ax1.set_title(r"(b) Centrosymmetric Parity & Octupole Census", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

    save_fig(fig, "fig3_octupole_complement")


def make_fig4_s9_landscape() -> None:
    # Compute exact S_9 energy histogram and display S_trap^(3)
    A3 = build_incidence_matrix(3).astype(int)
    vals = (-8, -6, -4, -2, 0, 2, 4, 6, 8)
    all_perms = np.array(list(itertools.permutations(vals)), dtype=np.int32)
    R = all_perms @ A3.T
    H_all = np.sum(R * R, axis=1)

    fig = plt.figure(figsize=(11.2, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.28)

    # Panel (a): Exhaustive S_9 energy distribution
    ax0 = fig.add_subplot(gs[0, 0])
    bins = np.linspace(0, 1400, 45)
    ax0.hist(H_all, bins=bins, color="#2b5c8f", edgecolor="white", linewidth=0.4, alpha=0.88)
    ax0.axvline(480.0, color="#d95f02", linestyle="--", linewidth=1.6,
                label=r"Exact ensemble mean $\mathbb{E}[\mathcal{H}_{\mathrm{line}}] = 2\|\mathbf{z}\|^2 = 480$")
    ax0.axvline(0.0, color="#1b9e77", linestyle="-", linewidth=1.8,
                label=r"8 Lo Shu ground states ($\mathcal{H}_{\mathrm{line}}=0$, $74.53\%$ basin)")
    ax0.axvline(8.0, color="#e7298a", linestyle=":", linewidth=1.8,
                label=r"8 Antipodal trap states $S_{\mathrm{trap}}^{(3)}$ ($\mathcal{H}_{\mathrm{line}}=8$, $25.47\%$ basin)")

    ax0.set_xlabel(r"Centred line-indicator Hamiltonian $\mathcal{H}_{\mathrm{line}}(S) = \mathbf{z}^\top L_3 \mathbf{z}$")
    ax0.set_ylabel(r"Number of permutations in $S_9$ ($9! = 362,880$)")
    ax0.set_title(r"(a) Exhaustive $S_9$ Energy Landscape & Basin Partition", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="upper right", frameon=True, framealpha=0.92)

    # Panel (b): Side-by-side comparison of S_trap^(3) vs Lo Shu and the (2,2)-double swap escape
    ax1 = fig.add_subplot(gs[0, 1])
    s_trap = np.array([[2, 6, 7], [9, 5, 1], [3, 4, 8]], dtype=int)
    z_trap = 2 * s_trap - 10
    ax1.imshow(z_trap, cmap="YlOrRd", vmin=-12, vmax=12, aspect="equal", alpha=0.25)

    for r in range(3):
        for c in range(3):
            v = s_trap[r, c]
            zv = z_trap[r, c]
            ax1.text(c, r, f"{v}\n($Z={zv:+d}$)", ha="center", va="center",
                     fontsize=9.5, fontweight="bold", color="#1a1a1a")

    # Annotate row/col/diag sums
    ax1.text(2.62, 0, "$\Sigma=15$ ($R=0$)", va="center", fontsize=8.2, color="#1b9e77", fontweight="bold")
    ax1.text(2.62, 1, "$\Sigma=15$ ($R=0$)", va="center", fontsize=8.2, color="#1b9e77", fontweight="bold")
    ax1.text(2.62, 2, "$\Sigma=15$ ($R=0$)", va="center", fontsize=8.2, color="#1b9e77", fontweight="bold")

    ax1.text(0, 2.65, "$\Sigma=14$\n($R=-2$)", ha="center", va="top", fontsize=8.2, color="#d95f02", fontweight="bold")
    ax1.text(1, 2.65, "$\Sigma=15$\n($R=0$)", ha="center", va="top", fontsize=8.2, color="#1b9e77", fontweight="bold")
    ax1.text(2, 2.65, "$\Sigma=16$\n($R=+2$)", ha="center", va="top", fontsize=8.2, color="#d95f02", fontweight="bold")

    # Draw double-swap arrows (2 <-> 4) and (3 <-> 1) or (6 <-> 4) and (7 <-> 9)
    ax1.annotate(
        "", xy=(1, 2), xytext=(0, 0),
        arrowprops=dict(arrowstyle="<->", color="#e7298a", lw=2.0, connectionstyle="arc3,rad=0.22"),
    )
    ax1.annotate(
        "", xy=(2, 1), xytext=(0, 2),
        arrowprops=dict(arrowstyle="<->", color="#2b5c8f", lw=2.0, connectionstyle="arc3,rad=-0.22"),
    )
    ax1.text(
        1.0, -0.73,
        r"Strict local minimum under all 36 $2$-cycles ($\min \Delta\mathcal{H}_{\mathrm{line}} = +4$)"
        + "\n"
        + r"and all 168 $3$-cycles ($\min \Delta\mathcal{H}_{\mathrm{line}} = +8$). Escapes to Lo Shu via"
        + "\n"
        + r"simultaneous $(2,2)$-cycle $(2\leftrightarrow 4)(3\leftrightarrow 1)$!",
        ha="center", va="center", fontsize=7.9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fdf0f6", edgecolor="#e7298a"),
    )

    ax1.set_xticks(range(3))
    ax1.set_yticks(range(3))
    ax1.set_xticklabels(["Col 1", "Col 2", "Col 3"])
    ax1.set_yticklabels(["Row 1", "Row 2", "Row 3"])
    ax1.set_xlim(-0.55, 3.65)
    ax1.set_ylim(3.25, -1.05)
    for sp in ("top", "right", "bottom", "left"):
        ax1.spines[sp].set_visible(False)
    ax1.set_title(r"(b) Antipodal Trap $S_{\mathrm{trap}}^{(3)}$ ($\mathcal{H}_{\mathrm{line}}=8$) & $(2,2)$-Swap Escape", fontweight="bold", pad=12)

    save_fig(fig, "fig4_s9_landscape_traps")


def make_fig5_s16_descent(data: dict) -> None:
    sec4 = data["section4_swap_landscape"]["n4_benchmark"]
    hist_data = sec4["terminal_H_histogram"]

    # Generate 40 sample greedy 2-cycle trajectories on S_16 for Panel (a)
    A4 = build_incidence_matrix(4).astype(int)
    L4 = A4.T @ A4
    diag_L4 = np.diag(L4)
    pairs4 = [(a, b) for a in range(16) for b in range(a + 1, 16)]
    rng = random.Random(20261102)
    base_vals4 = [centered_height(s, 4) for s in range(1, 17)]

    trajs_magic = []
    trajs_trapped = []
    trapped_example = None

    for _ in range(80):
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
        if curve[-1] == 0 and len(trajs_magic) < 18:
            trajs_magic.append(curve)
        elif curve[-1] > 0 and len(trajs_trapped) < 25:
            trajs_trapped.append(curve)
            if curve[-1] == 8 and trapped_example is None:
                trapped_example = z_arr.copy()

    fig = plt.figure(figsize=(11.2, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.05], wspace=0.26)

    # Panel (a): Steepest-descent trajectories on S_16
    ax0 = fig.add_subplot(gs[0, 0])
    for i, c in enumerate(trajs_trapped):
        ax0.plot(range(len(c)), np.array(c) + 4, color="#d95f02", alpha=0.45, lw=1.1,
                 label=r"Trapped in spurious local minimum ($81.75\%$)" if i == 0 else None)
    for i, c in enumerate(trajs_magic):
        ax0.plot(range(len(c)), np.array(c) + 4, color="#1b9e77", alpha=0.75, lw=1.4,
                 label=r"Converged to ground state $\mathcal{H}_{\mathrm{line}}=0$ ($18.25\%$)" if i == 0 else None)

    ax0.set_yscale("log")
    ax0.set_xlabel("Steepest-descent transposition step $t$")
    ax0.set_ylabel(r"Shifted line energy $\mathcal{H}_{\mathrm{line}}(S_t) + 4$ (log scale)")
    ax0.set_title(r"(a) Order-4 ($S_{16}$) Steepest-Descent Relaxation Trajectories", fontweight="bold", pad=8)
    ax0.grid(True, which="both", linestyle=":", alpha=0.45)
    ax0.legend(loc="upper right", frameon=True, framealpha=0.92)

    # Panel (b): Terminal local-minimum energy distribution across 2,000 random starts
    ax1 = fig.add_subplot(gs[0, 1])
    ks = [int(k) for k in hist_data.keys() if int(k) <= 64]
    vs = [hist_data[str(k)] for k in ks]
    colors = ["#1b9e77" if k == 0 else "#d95f02" for k in ks]
    ax1.bar([str(k) for k in ks], vs, color=colors, edgecolor="white", width=0.72)
    for idx, (k, v) in enumerate(zip(ks, vs)):
        if v >= 30:
            ax1.text(idx, v + 8, f"{v}", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    ax1.annotate(
        "Ground-state basin:\n365 / 2,000 (18.25%)\nreach $\\mathcal{H}_{\\mathrm{line}}=0$",
        xy=(0, 365), xytext=(4.2, 415),
        arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.3),
        fontsize=8.0, fontweight="bold", color="#0f6648",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#eefaf4", edgecolor="#1b9e77"),
    )
    ax1.annotate(
        "Dominant trap band:\n$\\mathcal{H}_{\\mathrm{line}} \\in \\{8, 12, 16\\}$\ncaptures 57.1% of starts",
        xy=(2, 305), xytext=(5.5, 295),
        arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.3),
        fontsize=8.0, fontweight="bold", color="#b34800",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff5eb", edgecolor="#d95f02"),
    )
    ax1.set_ylim(0, 535)
    ax1.set_xlabel(r"Terminal $2$-cycle local minimum energy $\mathcal{H}_{\mathrm{line}}(S_\infty)$")
    ax1.set_ylabel("Count out of 2,000 uniform random starts")
    ax1.set_title(r"(b) Terminal Local-Minimum Spectrum in $S_{16}$ ($n=4$)", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)

    save_fig(fig, "fig5_s16_descent_basins")


def make_fig6_bubble_trinity(data: dict) -> None:
    sec5 = data["section5_bubble_trinity"]
    regimes = sec5["regime_metrics"]
    bench = sec5["solver_benchmarks"]

    fig = plt.figure(figsize=(11.8, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0], wspace=0.34)

    # Panel (a): Continuous Bubble-Trinity induced energy decay across Regimes I-IV
    ax0 = fig.add_subplot(gs[0, 0])
    styles = {
        "I_Frozen_Lattice": ("Regime I: Frozen Lattice ($k_w=7.0, k_f=0$)", "#7570b3", "--", "s"),
        "II_Slow_Drift": ("Regime II: Slow Drift ($k_w=2.6, k_f=1.0$)", "#2b5c8f", "-.", "^"),
        "III_Field_Storm": ("Regime III: Field Storm ($k_w=0.8, k_f=3.2$)", "#d95f02", "-", "o"),
        "IV_Centrifugal_Balance": ("Regime IV: Centrifugal Balance ($k_s=0.85$)", "#1b9e77", "-", "D"),
    }
    steps = [10 * i for i in range(25)]
    for key, (label, col, ls, mk) in styles.items():
        y = regimes[key]["trajectory_H_decimated"]
        ax0.plot(steps, y, color=col, linestyle=ls, marker=mk, markersize=4.2,
                 markevery=3, linewidth=1.7, label=label)

    ax0.set_xlabel(r"Continuous Langevin integration step $t$ ($\Delta t = 0.025$)")
    ax0.set_ylabel(r"Kernel-induced line Hamiltonian $\mathcal{H}_{\mathrm{ind}}(t)$")
    ax0.set_title(r"(a) Continuous Bubble-Trinity Relaxation (Regimes I--IV)", fontweight="bold", pad=8)
    ax0.grid(True, linestyle=":", alpha=0.45)
    ax0.legend(loc="lower left", frameon=True, framealpha=0.92, fontsize=7.8)

    # Panel (b): Ground-state synthesis rate vs step budget (Standard 2-cycle SA vs Field-Guided 2+3-cycle Settle)
    ax1 = fig.add_subplot(gs[0, 1])
    budgets = sorted(int(k) for k in bench.keys())
    sa2 = [bench[str(b)]["sa_2cycle_only_pct"] for b in budgets]
    hyb = [bench[str(b)]["hybrid_settle_pct"] for b in budgets]

    x = np.arange(len(budgets))
    w = 0.36
    b1 = ax1.bar(x - w / 2, sa2, width=w, color="#8da0cb", edgecolor="white",
                 label="Unbiased $2$-cycle Simulated Annealing")
    b2 = ax1.bar(x + w / 2, hyb, width=w, color="#1b9e77", edgecolor="white",
                 label="Field-Guided $2+3$-Cycle Hybrid Settling")

    for rect in b1:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width() / 2, h + 1.2, f"{h:.1f}%",
                 ha="center", va="bottom", fontsize=7.5, color="#3b4d71")
    for rect in b2:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width() / 2, h + 1.2, f"{h:.1f}%",
                 ha="center", va="bottom", fontsize=7.5, color="#0f6648", fontweight="bold")

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{b:,}" for b in budgets])
    ax1.set_ylim(0, 80)
    ax1.set_xlabel("Discrete settling step budget $B$")
    ax1.set_ylabel(r"Order-4 ground-state recovery rate ($\mathcal{H}_{\mathrm{line}}=0$, %)")
    ax1.set_title(r"(b) Ground-State Synthesis: $2$-Cycle SA vs. Hybrid Settling", fontweight="bold", pad=8)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.45)
    ax1.legend(loc="upper left", frameon=True, framealpha=0.92)

    save_fig(fig, "fig6_bubble_trinity_regimes")


def main() -> None:
    print("=== Generating Publication Figures for Paper D ===")
    data = json.loads(RESULTS_JSON.read_text(encoding="utf-8"))
    make_fig1_spectral(data)
    make_fig2_window_entropy(data)
    make_fig3_octupole_complement(data)
    make_fig4_s9_landscape()
    make_fig5_s16_descent(data)
    make_fig6_bubble_trinity(data)
    print("All 6 Paper D figures generated successfully!")


if __name__ == "__main__":
    main()
