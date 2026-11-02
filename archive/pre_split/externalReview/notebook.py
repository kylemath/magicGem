"""externalReview/notebook.py

Reproducible computations supporting the revised referee report.

What this script does
- Shows that the paper's 4-term energy E(S)=0 does NOT characterize magic squares for n>=4.
- Produces explicit n=4 counterexamples (E=0 but not magic).
- Demonstrates why naive random sampling is unlikely to hit these counterexamples.
- Visualizes the 'low-mode test functions' viewpoint: covariances are inner products with a
  small set of test functions on the grid.

Outputs
- Writes figures into externalReview/figures/.

Run
  python3 externalReview/notebook.py

"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root is importable (so `import src` works when this script lives in externalReview/)
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

try:
    from src.analysis import compute_total_magic_energy_v2
    from src.magic_squares import is_magic_square
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "Could not import project modules from `src/`. Try running from repo root."
    ) from e


OUT_DIR = os.path.join("externalReview", "figures")


@dataclass(frozen=True)
class Example:
    n: int
    grid: np.ndarray
    label: str


def ensure_out_dir() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)


def line_sums(arr: np.ndarray) -> dict:
    n = arr.shape[0]
    return {
        "M": int(n * (n * n + 1) // 2),
        "row": arr.sum(axis=1).astype(int).tolist(),
        "col": arr.sum(axis=0).astype(int).tolist(),
        "diag_main": int(np.trace(arr)),
        "diag_anti": int(np.trace(np.fliplr(arr))),
    }


def paper_energy_components(arr: np.ndarray) -> dict:
    # Uses the project implementation aligned with the manuscript definitions.
    res = compute_total_magic_energy_v2(arr)
    return {
        "E_total": float(res["E_total"]),
        "cov_xz": float(res["cov_xz"]),
        "cov_yz": float(res["cov_yz"]),
        "cov_main_z": float(res["cov_main_z"]),
        "cov_anti_z": float(res["cov_anti_z"]),
        "E_cov": float(res["E_cov"]),
        "E_diag": float(res["E_diag"]),
    }


def n4_hillclimb_zero_solutions(
    *,
    target: int = 12,
    seed: int = 2,
    max_restarts: int = 2000,
    steps_per_restart: int = 50_000,
) -> List[np.ndarray]:
    """Find n=4 permutations with A=B=C=D=0 in *integer arithmetic*.

    This is not meant to be optimal—just a robust way to surface explicit counterexamples.

    Internally we use z2 = 2*v - 17 (odd integers with mean 0), so covariances vanish iff
    the corresponding weighted sums vanish.
    """

    rnd = np.random.default_rng(seed)

    n = 4
    n_sq = n * n
    values = np.arange(1, n_sq + 1, dtype=np.int32)

    # scaled coordinates for half-integer x,y: x2 = 2x, y2 = 2y
    x2 = np.array([-3, -1, 1, 3], dtype=np.int32)
    y2 = np.array([3, 1, -1, -3], dtype=np.int32)

    # weights in row-major order
    wx = np.tile(x2, n)  # repeats across each row
    wy = np.repeat(y2, n)

    main_idx = np.array([i * n + i for i in range(n)], dtype=np.int32)
    anti_idx = np.array([i * n + (n - 1 - i) for i in range(n)], dtype=np.int32)

    def constraints(z2_flat: np.ndarray) -> Tuple[int, int, int, int]:
        A = int((z2_flat * wx).sum())
        B = int((z2_flat * wy).sum())
        C = int(z2_flat[main_idx].sum())
        D = int(z2_flat[anti_idx].sum())
        return A, B, C, D

    def obj(r: Tuple[int, int, int, int]) -> int:
        return int(r[0] * r[0] + r[1] * r[1] + r[2] * r[2] + r[3] * r[3])

    # precompute per-position weights for swap delta
    W = np.zeros((n_sq, 4), dtype=np.int32)
    for i in range(n):
        for j in range(n):
            idx = i * n + j
            W[idx, 0] = x2[j]
            W[idx, 1] = y2[i]
            W[idx, 2] = 1 if i == j else 0
            W[idx, 3] = 1 if i + j == n - 1 else 0

    sols: List[np.ndarray] = []
    seen = set()

    for _ in range(max_restarts):
        perm = rnd.permutation(values)
        z2 = (2 * perm - 17).astype(np.int32)
        r = constraints(z2)
        f = obj(r)

        for _step in range(steps_per_restart):
            if f == 0:
                flat = tuple(perm.tolist())
                if flat not in seen:
                    seen.add(flat)
                    sols.append(perm.reshape(4, 4).copy())
                break

            i1, i2 = rnd.choice(n_sq, size=2, replace=False)
            a = int(z2[i1])
            b = int(z2[i2])
            if a == b:
                continue

            d = b - a
            wdiff = (W[i1] - W[i2]).astype(np.int64)
            dr = (d * wdiff).astype(np.int64)
            new_r = (r[0] + int(dr[0]), r[1] + int(dr[1]), r[2] + int(dr[2]), r[3] + int(dr[3]))
            new_f = obj(new_r)

            if new_f <= f:
                # accept swap
                perm[i1], perm[i2] = perm[i2], perm[i1]
                z2[i1], z2[i2] = z2[i2], z2[i1]
                r, f = new_r, new_f

        if len(sols) >= target:
            break

    return sols


def estimate_random_hit_rate_n4(*, n_samples: int = 500_000, seed: int = 0) -> float:
    """Estimate P(A=B=C=D=0) for n=4 by uniform random permutations.

    Expectation: extremely tiny; naive Monte Carlo will usually return 0.
    """

    n = 4
    n_sq = n * n
    rng = np.random.default_rng(seed)

    x2 = np.array([-3, -1, 1, 3], dtype=np.int32)
    y2 = np.array([3, 1, -1, -3], dtype=np.int32)
    wx = np.tile(x2, n)
    wy = np.repeat(y2, n)
    main_idx = np.array([i * n + i for i in range(n)], dtype=np.int32)
    anti_idx = np.array([i * n + (n - 1 - i) for i in range(n)], dtype=np.int32)

    # vectorized random permutations via argsort of random keys
    keys = rng.random((n_samples, n_sq), dtype=np.float64)
    perm = np.argsort(keys, axis=1).astype(np.int32) + 1  # (n_samples,16)
    z2 = 2 * perm - 17

    A = (z2 * wx).sum(axis=1)
    B = (z2 * wy).sum(axis=1)
    C = z2[:, main_idx].sum(axis=1)
    D = z2[:, anti_idx].sum(axis=1)

    hits = ((A == 0) & (B == 0) & (C == 0) & (D == 0)).sum()
    return float(hits) / float(n_samples)


def plot_test_functions_n4() -> str:
    """Heatmaps of the four 'test functions' the manuscript uses."""

    n = 4

    # centered coordinate functions (x,y)
    j = np.arange(n) - (n - 1) / 2
    i = (n - 1) / 2 - np.arange(n)
    X = np.tile(j, (n, 1))
    Y = np.tile(i, (n, 1)).T

    Dm = np.eye(n)
    Da = np.fliplr(np.eye(n))

    # mean-centered diagonal indicators (constant component irrelevant for <f,phi> when f is mean zero)
    Dm_c = Dm - Dm.mean()
    Da_c = Da - Da.mean()

    mats = [X, Y, Dm_c, Da_c]
    titles = ["X (column coordinate)", "Y (row coordinate)", "Main diag indicator (centered)", "Anti-diag indicator (centered)"]

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.4), constrained_layout=True)
    for ax, M, t in zip(axes, mats, titles):
        im = ax.imshow(M, cmap="coolwarm", interpolation="nearest")
        ax.set_title(t, fontsize=10)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        for (r, c), val in np.ndenumerate(M):
            ax.text(c, r, f"{val:.1f}", ha="center", va="center", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)

    path = os.path.join(OUT_DIR, "n4_test_functions.png")
    fig.suptitle("n=4: the four test functions behind E(S)", fontsize=12, y=1.02)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_zero_energy_examples(examples: List[Example]) -> str:
    """Show a small gallery of E=0 non-magic examples alongside line-sum deviations."""

    k = len(examples)
    fig, axes = plt.subplots(k, 2, figsize=(10, 3.0 * k), constrained_layout=True)
    if k == 1:
        axes = np.array([axes])

    for r, ex in enumerate(examples):
        arr = ex.grid
        n = ex.n
        stats = line_sums(arr)
        M = stats["M"]

        # left: grid
        ax = axes[r, 0]
        im = ax.imshow(arr, cmap="viridis", interpolation="nearest")
        ax.set_title(f"{ex.label} (n={n})")
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        for (i, j), val in np.ndenumerate(arr):
            ax.text(j, i, str(int(val)), ha="center", va="center", fontsize=9, color="white")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)

        # right: deviations
        ax2 = axes[r, 1]
        row_dev = np.array(stats["row"]) - M
        col_dev = np.array(stats["col"]) - M
        x = np.arange(n)
        ax2.axhline(0, color="k", lw=1)
        ax2.bar(x - 0.15, row_dev, width=0.3, label="row sum − M")
        ax2.bar(x + 0.15, col_dev, width=0.3, label="col sum − M")
        ax2.set_xticks(x)
        ax2.set_xlabel("index")
        ax2.set_ylabel("deviation")
        ax2.set_title(f"Line-sum deviations (M={M}); diag ok: {stats['diag_main']==M and stats['diag_anti']==M}")
        ax2.legend(loc="upper right", fontsize=9)

    path = os.path.join(OUT_DIR, "zero_energy_nonmagic_examples.png")
    fig.suptitle("Explicit counterexamples: E(S)=0 but S is not magic", fontsize=13)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def main() -> None:
    ensure_out_dir()

    # (1) Confirm the paper-energy counterexample already used in the first review
    counterexample = np.array(
        [
            [9, 4, 12, 3],
            [16, 1, 14, 7],
            [10, 15, 11, 8],
            [2, 5, 6, 13],
        ],
        dtype=int,
    )

    ce_energy = paper_energy_components(counterexample)
    ce_magic = bool(is_magic_square(counterexample))
    ce_lines = line_sums(counterexample)

    print("n=4 counterexample (from review 1):")
    print(counterexample)
    print("is_magic_square:", ce_magic)
    print("energy components:", ce_energy)
    print("line sums:", ce_lines)

    # (2) Find additional n=4 E=0 permutations by hillclimbing
    sols = n4_hillclimb_zero_solutions(target=8, seed=2, max_restarts=1000, steps_per_restart=50_000)
    print(f"\nFound {len(sols)} n=4 zero-energy solutions via hillclimb.")

    # (3) Estimate random hit rate (expected 0 for moderate sample sizes)
    hit_rate = estimate_random_hit_rate_n4(n_samples=500_000, seed=0)
    print("Estimated random hit rate P(E=0) for n=4 via 500k samples:", hit_rate)

    # (4) Make figures
    f1 = plot_test_functions_n4()

    # assemble a few examples (ensure non-magic)
    examples: List[Example] = [Example(n=4, grid=counterexample, label="Example A")]

    added = 0
    for g in sols:
        if not is_magic_square(g):
            examples.append(Example(n=4, grid=g, label=f"Example {chr(ord('B') + added)}"))
            added += 1
        if len(examples) >= 4:
            break

    f2 = plot_zero_energy_examples(examples)

    print("\nWrote figures:")
    print(" -", f1)
    print(" -", f2)


if __name__ == "__main__":
    main()
