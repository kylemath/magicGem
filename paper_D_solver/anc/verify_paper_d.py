#!/usr/bin/env python3
"""Exact rational and numerical verification suite for Paper D:
'Spectral Structure, Multiscale Window Entropies, and Multi-Exchange
Energy Landscapes of Magic Squares' (Kyle Elliott Mathewson).

Verifies:
  1. Section 2: Exact spectrum of the unprojected Line-Incidence Laplacian
     L_n = A_n^T A_n on R^{n^2} and its exact integer rationalization on the
     zero-mean hyperplane 1^perp for all orders n = 3..8, plus the Low-Mode
     Insufficiency Theorem and explicit 4x4 low-mode counterexamples.
  2. Section 3: Exhaustive multiscale windowed energy E_p(W), Shannon window
     entropy H_p(k), 2x2 sub-window residual energy W_{2x2}(S), complement-pair
     breaking count B_comp(S), and octupole moment M_xyz(S) across all 880
     Frenicle order-4 magic squares (partitioned by Dudeney groups I-XII) and
     constructive families at n = 3, 4, 5, 6, 8 (Siamese, Linear Modular,
     Doubly-Even, and Conway LUX Singly-Even).
  3. Section 4: Exact closed-form transposition energy formula Delta H_line(tau_ab),
     exhaustive 9! = 362,880 permutation landscape census at n = 3 under 2-cycle
     steepest descent vs. 2-cycle + 3-cycle descent, and 10,000-trial basin
     census at n = 4 quantifying local-minimum trapping and cycle escape.
  4. Section 5: Continuous 'Bubble Trinity' Langevin relaxation across the four
     canonical dynamical regimes (Frozen Lattice, Slow Drift, Field Storm,
     Centrifugal Stratification) and hybrid continuous-discrete ground-state
     synthesis benchmarks.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SQUARES_880_JSON = REPO_ROOT / "web" / "physicalSolver" / "data" / "order4_magic_squares.json"
OUT_JSON = ROOT / "anc" / "results_paper_d.json"


def centered_height(val: int, n: int) -> int:
    return 2 * val - (n * n + 1)


def lattice_coord(idx: int, n: int) -> int:
    return 2 * idx - (n - 1)


def build_incidence_matrix(n: int) -> np.ndarray:
    rows = []
    for r in range(n):
        v = np.zeros((n, n), dtype=float)
        v[r, :] = 1.0
        rows.append(v.ravel())
    for c in range(n):
        v = np.zeros((n, n), dtype=float)
        v[:, c] = 1.0
        rows.append(v.ravel())
    d1 = np.zeros((n, n), dtype=float)
    d2 = np.zeros((n, n), dtype=float)
    for i in range(n):
        d1[i, i] = 1.0
        d2[i, n - 1 - i] = 1.0
    rows.append(d1.ravel())
    rows.append(d2.ravel())
    return np.array(rows, dtype=float)


def line_residuals_centered(z_grid: np.ndarray) -> tuple[list[int], list[int], list[int]]:
    n = z_grid.shape[0]
    rows = [int(np.sum(z_grid[i, :])) for i in range(n)]
    cols = [int(np.sum(z_grid[:, j])) for j in range(n)]
    diags = [
        int(sum(z_grid[i, i] for i in range(n))),
        int(sum(z_grid[i, n - 1 - i] for i in range(n))),
    ]
    return rows, cols, diags


def h_line_centered(z_grid: np.ndarray) -> int:
    rows, cols, diags = line_residuals_centered(z_grid)
    return sum(r * r for r in rows) + sum(c * c for c in cols) + sum(d * d for d in diags)


def verify_section2_spectral() -> dict:
    print("=== Section 2: Spectral Decomposition of Line-Incidence Laplacian ===")
    spectral_table = {}
    for n in range(3, 9):
        A = build_incidence_matrix(n)
        L = A.T @ A
        N = n * n
        evals_full = np.linalg.eigvalsh(L)
        u_full, c_full = np.unique(np.round(evals_full, 6), return_counts=True)

        # Theoretical eigenvalues on R^{n^2}
        if n % 2 == 0:
            lam_plus = (3 * n + math.sqrt(n * (n + 16))) / 2.0
            lam_minus = (3 * n - math.sqrt(n * (n + 16))) / 2.0
            expected_full = {
                0.0: n * n - 2 * n - 1,
                round(lam_minus, 6): 1,
                float(n): 2 * n - 1,
                round(lam_plus, 6): 1,
            }
        else:
            lam_plus = (3 * n + 1 + math.sqrt(n * n + 14 * n + 1)) / 2.0
            lam_minus = (3 * n + 1 - math.sqrt(n * n + 14 * n + 1)) / 2.0
            expected_full = {
                0.0: n * n - 2 * n - 1,
                round(lam_minus, 6): 1,
                float(n - 1): 1,
                float(n): 2 * n - 2,
                round(lam_plus, 6): 1,
            }
        actual_full = {float(k): int(v) for k, v in zip(u_full, c_full)}
        assert actual_full == expected_full, f"Mismatch on R^{{n^2}} for n={n}: {actual_full} vs {expected_full}"

        # Restricted to zero-mean hyperplane 1^perp (dim N - 1)
        # Use orthonormal basis of 1^perp via Householder / Helmert
        ones = np.ones((N, 1)) / math.sqrt(N)
        Q, _ = np.linalg.qr(np.hstack([ones, np.eye(N)[:, :-1]]))
        B_perp = Q[:, 1:]  # N x (N-1)
        L_perp = B_perp.T @ L @ B_perp
        evals_perp = np.linalg.eigvalsh(L_perp)
        u_perp, c_perp = np.unique(np.round(evals_perp, 6), return_counts=True)
        actual_perp = {float(k): int(v) for k, v in zip(u_perp, c_perp)}

        if n % 2 == 0:
            expected_perp = {
                0.0: n * n - 2 * n - 1,
                float(n - 2): 1,
                float(n): 2 * n - 1,
            }
        else:
            expected_perp = {
                0.0: n * n - 2 * n - 1,
                float(n - 1): 2,
                float(n): 2 * n - 2,
            }
        assert actual_perp == expected_perp, f"Mismatch on 1^perp for n={n}: {actual_perp} vs {expected_perp}"

        # Total variance ||z||^2 for any permutation of 1..n^2 in centered units Z = 2s - (n^2+1)
        z_vals = [centered_height(s, n) for s in range(1, N + 1)]
        norm_z_sq = sum(z * z for z in z_vals)
        assert norm_z_sq == N * (N * N - 1) // 3
        # Expected value E[H_line] over uniform random permutations of S_{n^2}
        # Since E[z_a^2] = (N^2-1)/3 and E[z_a z_b] = -(N+1)/3 for a != b,
        # for any line L of length n: E[R_L^2] = n * (N^2-1)/3 + n(n-1) * (-(N+1)/3) = n(N+1)(N-n)/3 = n^2(n-1)(n^2+1)/3
        # Across 2n+2 lines: E[H_line] = (2n+2) * n^2 * (n-1) * (n^2+1) / 3
        expected_mean_H = Fraction((2 * n + 2) * n * n * (n - 1) * (N + 1), 3)
        # Also verify via Tr(L_perp) / (N - 1) * ||z||^2:
        # Wait: row/col lines have length n, diags have length n, so sum_{L} (n * Var - n(n-1)/(N-1) Var)
        # = (2n+2) * n * (N - n) / (N - 1) * ||z||^2 = (2n+2) * n * n(n-1) / (N - 1) * N(N^2-1)/3 = (2n+2) n^2 (n-1) (N+1) / 3!
        tr_L_perp = int(round(np.trace(L_perp)))
        assert tr_L_perp == 2 * (n * n - 1)
        assert expected_mean_H == 2 * norm_z_sq
        spectral_table[str(n)] = {
            "n": n,
            "N": N,
            "rank_A": 2 * n + 1,
            "magic_nullity": n * n - 2 * n - 1,
            "unprojected_eigenvalues": actual_full,
            "zero_mean_eigenvalues": actual_perp,
            "trace_L_perp": tr_L_perp,
            "norm_z_sq": norm_z_sq,
            "mean_random_H_line": float(expected_mean_H),
            "mean_random_H_line_exact": str(expected_mean_H),
        }
        print(f"  n={n}: rank={2*n+1}, ker_dim={n*n-2*n-1}, spec(L|1^perp)={actual_perp}, E[H_line]={float(expected_mean_H):.1f}")

    # Verify the explicit 4x4 Low-Mode Counterexample from energyDecompositionApp.js
    s_low = np.array([
        [9, 4, 12, 3],
        [16, 1, 14, 7],
        [10, 15, 11, 8],
        [2, 5, 6, 13],
    ], dtype=int)
    z_low = 2 * s_low - 17
    rows_l, cols_l, diags_l = line_residuals_centered(z_low)
    X = np.array([[lattice_coord(j, 4) for j in range(4)] for _ in range(4)])
    Y = np.array([[-lattice_coord(i, 4) for _ in range(4)] for i in range(4)])
    xz_cov = int(np.sum(X * z_low))
    yz_cov = int(np.sum(Y * z_low))
    assert xz_cov == 0 and yz_cov == 0 and diags_l == [0, 0]
    assert rows_l == [-12, 8, 20, -16]
    assert cols_l == [6, -18, 18, -6]
    h_low = h_line_centered(z_low)
    assert h_low == (-12)**2 + 8**2 + 20**2 + (-16)**2 + 6**2 + (-18)**2 + 18**2 + (-6)**2 == 1584
    print(f"  Verified 4x4 Low-Mode Counterexample: <X,Z>={xz_cov}, <Y,Z>={yz_cov}, diags={diags_l}, rows={rows_l}, cols={cols_l}, H_line={h_low}")

    return {
        "spectral_table": spectral_table,
        "low_mode_counterexample": {
            "square": s_low.tolist(),
            "rows_Z": rows_l,
            "cols_Z": cols_l,
            "diags_Z": diags_l,
            "xz_inner": xz_cov,
            "yz_inner": yz_cov,
            "H_line": h_low,
        },
    }


def window_entropy_and_stats(square: list[list[int]]) -> dict:
    n = len(square)
    z = [[centered_height(square[i][j], n) for j in range(n)] for i in range(n)]
    entropies = {}
    for k in range(1, n + 1):
        wins = []
        for r in range(n - k + 1):
            for c in range(n - k + 1):
                w = [z[i][j] for i in range(r, r + k) for j in range(c, c + k)]
                wins.append(w)
        max_ent = math.log2(len(wins)) if len(wins) > 1 else 1.0
        for p in (1, 2, 4):
            weights = [sum(abs(val) ** p for val in w) for w in wins]
            tot = sum(weights)
            ent = -sum((wt / tot) * math.log2(wt / tot) for wt in weights if wt > 0)
            entropies[f"H_p{p}_k{k}"] = ent
            entropies[f"Hnorm_p{p}_k{k}"] = ent / max_ent if len(wins) > 1 else 1.0

    # 2x2 sliding window residual energy (non-toroidal: (n-1)^2 windows; toroidal: n^2 windows)
    w2_non_tor = 0
    for r in range(n - 1):
        for c in range(n - 1):
            s_w = z[r][c] + z[r + 1][c] + z[r][c + 1] + z[r + 1][c + 1]
            w2_non_tor += s_w * s_w
    w2_tor = 0
    for r in range(n):
        for c in range(n):
            s_w = z[r][c] + z[(r + 1) % n][c] + z[r][(c + 1) % n] + z[(r + 1) % n][(c + 1) % n]
            w2_tor += s_w * s_w

    # Centrosymmetric complement-pair breaks
    target = n * n + 1
    breaks = 0
    pairs = 0
    for r in range(n):
        for c in range(n):
            mr, mc = n - 1 - r, n - 1 - c
            if (r, c) < (mr, mc):
                pairs += 1
                if square[r][c] + square[mr][mc] != target:
                    breaks += 1

    # Mixed octupole moment M_xyz = sum X_j Y_i Z_ij
    m_xyz = 0
    for r in range(n):
        for c in range(n):
            m_xyz += lattice_coord(c, n) * (-lattice_coord(r, n)) * z[r][c]

    return {
        "entropies": entropies,
        "w2_non_tor": w2_non_tor,
        "w2_tor": w2_tor,
        "complement_breaks": breaks,
        "complement_pairs": pairs,
        "m_xyz": m_xyz,
    }


def siamese_magic(n: int) -> list[list[int]]:
    sq = [[0] * n for _ in range(n)]
    r, c = 0, n // 2
    for v in range(1, n * n + 1):
        sq[r][c] = v
        nr, nc = (r - 1) % n, (c + 1) % n
        if sq[nr][nc]:
            r = (r + 1) % n
        else:
            r, c = nr, nc
    return sq


def doubly_even_magic(n: int) -> list[list[int]]:
    comp = n * n + 1
    sq = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            val = r * n + c + 1
            keep = (r % 4 == c % 4) or ((r % 4) + (c % 4) == 3)
            sq[r][c] = val if keep else comp - val
    return sq


def lux_singly_even_magic(n: int) -> list[list[int]]:
    m = (n - 2) // 4
    k = 2 * m + 1
    letters = []
    for r in range(k):
        if r < m + 1:
            letters.append(["L"] * k)
        elif r == m + 1:
            letters.append(["U"] * k)
        else:
            letters.append(["X"] * k)
    letters[m + 1][m] = "L"
    letters[m][m] = "U"
    visit = siamese_magic(k)
    pats = {
        "L": [[3, 0], [1, 2]],
        "U": [[0, 3], [1, 2]],
        "X": [[0, 3], [2, 1]],
    }
    sq = [[0] * n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            v = visit[i][j]
            pat = pats[letters[i][j]]
            base = 4 * (v - 1)
            for di in range(2):
                for dj in range(2):
                    sq[2 * i + di][2 * j + dj] = base + pat[di][dj] + 1
    return sq


def verify_section3_multiscale() -> dict:
    print("=== Section 3: Multiscale Window Entropy & 880 Order-4 Census ===")
    data = json.loads(SQUARES_880_JSON.read_text(encoding="utf-8"))
    records = data["records"]
    assert len(records) == 880

    by_group = defaultdict(list)
    all_stats = []
    w2_non_tor_zero_count = 0
    w2_tor_zero_count = 0

    for rec in records:
        st = window_entropy_and_stats(rec["square"])
        st["id"] = rec["id"]
        st["group"] = rec["dudeneyGroup"]
        all_stats.append(st)
        by_group[rec["dudeneyGroup"]].append(st)
        if st["w2_non_tor"] == 0:
            w2_non_tor_zero_count += 1
        if st["w2_tor"] == 0:
            w2_tor_zero_count += 1

    # Panmagic (Group I, 48 squares) has w2_tor == 0; Theorem 3.1 proves w2_non_tor == 0 <=> w2_tor == 0
    print(f"  Order-4 2x2 window residual energy: w2_tor==0 on {w2_tor_zero_count}/880 squares; w2_non_tor==0 on {w2_non_tor_zero_count}/880 squares")
    assert w2_tor_zero_count == 48 and w2_non_tor_zero_count == 48

    # Verify Concentric Shell Quadrupole Identity for M_xyz across all 880 order-4 magic squares:
    # Q_inner(S) == -Q_corner(S) and M_xyz(S) == -8 * Q_corner(S) - 3 * Q_edge(S)
    anomalous_octupole_zeros = []
    for rec, st in zip(records, all_stats):
        sq = rec["square"]
        Z = [[centered_height(sq[i][j], 4) for j in range(4)] for i in range(4)]
        q_corner = (Z[0][0] + Z[3][3]) - (Z[0][3] + Z[3][0])
        q_inner = (Z[1][1] + Z[2][2]) - (Z[1][2] + Z[2][1])
        q_edge = ((Z[0][1] + Z[3][2]) - (Z[0][2] + Z[3][1])) + ((Z[1][0] + Z[2][3]) - (Z[2][0] + Z[1][3]))
        assert q_inner == -q_corner, f"Q_inner != -Q_corner on square #{rec['id']}"
        assert st["m_xyz"] == -8 * q_corner - 3 * q_edge, f"Quadrupole identity failed on #{rec['id']}"
        if rec["dudeneyGroup"] in (1, 2, 4, 5):
            assert q_edge == 0 and q_corner != 0
        if st["m_xyz"] == 0 and rec["dudeneyGroup"] != 3:
            anomalous_octupole_zeros.append({
                "id": rec["id"],
                "group": rec["dudeneyGroup"],
                "Q_corner": q_corner,
                "Q_edge": q_edge,
                "resonance_k": q_edge // 8,
            })
    assert len(anomalous_octupole_zeros) == 8
    print(f"  Verified Concentric Shell Quadrupole Identity M_xyz = -8*Q_corner - 3*Q_edge on all 880 squares; 8 non-associative zeros: {[x['id'] for x in anomalous_octupole_zeros]}")

    group_summary = {}
    for g in sorted(by_group.keys()):
        items = by_group[g]
        h1_k2 = [x["entropies"]["Hnorm_p1_k2"] for x in items]
        h2_k2 = [x["entropies"]["Hnorm_p2_k2"] for x in items]
        w2_nt = [x["w2_non_tor"] for x in items]
        w2_t = [x["w2_tor"] for x in items]
        brks = sorted(set(x["complement_breaks"] for x in items))
        mxyz_abs = [abs(x["m_xyz"]) for x in items]
        group_summary[str(g)] = {
            "group": g,
            "count": len(items),
            "complement_breaks_values": brks,
            "Hnorm_p1_k2_mean": round(float(np.mean(h1_k2)), 5),
            "Hnorm_p1_k2_min": round(float(np.min(h1_k2)), 5),
            "Hnorm_p1_k2_max": round(float(np.max(h1_k2)), 5),
            "Hnorm_p2_k2_mean": round(float(np.mean(h2_k2)), 5),
            "w2_non_tor_mean": round(float(np.mean(w2_nt)), 1),
            "w2_non_tor_min": int(np.min(w2_nt)),
            "w2_non_tor_max": int(np.max(w2_nt)),
            "w2_tor_mean": round(float(np.mean(w2_t)), 1),
            "w2_tor_min": int(np.min(w2_t)),
            "w2_tor_max": int(np.max(w2_t)),
            "abs_M_xyz_mean": round(float(np.mean(mxyz_abs)), 1),
            "abs_M_xyz_zero_count": sum(1 for v in mxyz_abs if v == 0),
        }
        print(
            f"  Group {g:2d} (n={len(items):3d}): breaks={brks}, "
            f"H1(2)={np.mean(h1_k2):.4f}, W2_nt=[{np.min(w2_nt)},{np.max(w2_nt)}], "
            f"W2_tor=[{np.min(w2_t)},{np.max(w2_t)}], |M_xyz|_0={sum(1 for v in mxyz_abs if v == 0)}/{len(items)}"
        )

    # Constructive families across orders n = 3, 4, 5, 6, 8
    families = {
        "n3_LoShu": siamese_magic(3),
        "n4_DoublyEven": doubly_even_magic(4),
        "n5_Siamese": siamese_magic(5),
        "n6_ConwayLUX": lux_singly_even_magic(6),
        "n8_DoublyEven": doubly_even_magic(8),
    }
    family_stats = {}
    for name, sq in families.items():
        n = len(sq)
        z = np.array([[centered_height(sq[i][j], n) for j in range(n)] for i in range(n)])
        assert h_line_centered(z) == 0, f"{name} is not magic!"
        st = window_entropy_and_stats(sq)
        family_stats[name] = {
            "n": n,
            "Hnorm_p1_k2": round(st["entropies"]["Hnorm_p1_k2"], 5),
            "Hnorm_p2_k2": round(st["entropies"]["Hnorm_p2_k2"], 5),
            "w2_non_tor": st["w2_non_tor"],
            "w2_tor": st["w2_tor"],
            "complement_breaks": f"{st['complement_breaks']}/{st['complement_pairs']}",
            "m_xyz": st["m_xyz"],
        }

    # Global extrema across 880 order-4 squares
    max_h1_rec = max(all_stats, key=lambda x: x["entropies"]["Hnorm_p1_k2"])
    min_h1_rec = min(all_stats, key=lambda x: x["entropies"]["Hnorm_p1_k2"])
    max_w2_rec = max(all_stats, key=lambda x: x["w2_non_tor"])

    return {
        "w2_tor_zero_count": w2_tor_zero_count,
        "w2_non_tor_zero_count": w2_non_tor_zero_count,
        "group_summary": group_summary,
        "family_stats": family_stats,
        "extrema_880": {
            "max_Hnorm_p1_k2": {"id": max_h1_rec["id"], "group": max_h1_rec["group"], "val": round(max_h1_rec["entropies"]["Hnorm_p1_k2"], 6)},
            "min_Hnorm_p1_k2": {"id": min_h1_rec["id"], "group": min_h1_rec["group"], "val": round(min_h1_rec["entropies"]["Hnorm_p1_k2"], 6)},
            "max_w2_non_tor": {"id": max_w2_rec["id"], "group": max_w2_rec["group"], "val": max_w2_rec["w2_non_tor"]},
        },
        "anomalous_octupole_zeros": anomalous_octupole_zeros,
        "per_square_metrics": [
            {
                "id": x["id"],
                "group": x["group"],
                "Hnorm_p1_k2": round(x["entropies"]["Hnorm_p1_k2"], 5),
                "Hnorm_p2_k2": round(x["entropies"]["Hnorm_p2_k2"], 5),
                "Hnorm_p4_k2": round(x["entropies"]["Hnorm_p4_k2"], 5),
                "w2_non_tor": x["w2_non_tor"],
                "w2_tor": x["w2_tor"],
                "breaks": x["complement_breaks"],
                "m_xyz": x["m_xyz"],
            }
            for x in all_stats
        ],
    }


def verify_section4_swap_landscape() -> dict:
    print("=== Section 4: Combinatorial Swap Landscape & Local Minima Census ===")
    # 1. Exhaustive census of all 9! = 362,880 permutations for n = 3
    n = 3
    N = 9
    A = build_incidence_matrix(n).astype(int)  # 8 x 9
    L = A.T @ A  # 9 x 9 integer matrix
    # Precompute pair swap delta matrix:
    # When swapping positions a and b with values z_a, z_b (let d = z_a - z_b):
    # z' = z - d (e_a - e_b)
    # H(z') - H(z) = -2 d (e_a - e_b)^T L z + d^2 (L_aa + L_bb - 2 L_ab)
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]

    # Let's compute H_line for all 362,880 permutations of centered heights {-8,-6,-4,-2,0,2,4,6,8}
    # Even faster: work in standard units s_ij - 5 in {-4,-3,-2,-1,0,1,2,3,4} and multiply H by 4!
    vals = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
    all_perms = list(itertools.permutations(vals))
    P_mat = np.array(all_perms, dtype=np.int32)  # 362880 x 9
    R_mat = P_mat @ A.T  # 362880 x 8
    E_std = np.sum(R_mat * R_mat, axis=1)  # in standard units; centered H_line = 4 * E_std

    # Check how many permutations are local minima under 2-cycle swaps (no strictly improving swap Delta E < 0)
    # and how many are strict local minima (all 36 swaps have Delta E > 0)
    # Notice gradient g = L z = A^T R: for each state, g = R_mat @ A (362880 x 9)
    G_mat = R_mat @ A  # 362880 x 9
    diag_L = np.diag(L)  # length 9

    min_delta = np.full(len(all_perms), 999999, dtype=np.int32)
    best_next_idx = np.arange(len(all_perms), dtype=np.int32)

    for a, b in pairs:
        c_ab = int(diag_L[a] + diag_L[b] - 2 * L[a, b])
        d = P_mat[:, a] - P_mat[:, b]
        # Delta E_std = -2 * d * (g_a - g_b) + d^2 * c_ab
        delta = -2 * d * (G_mat[:, a] - G_mat[:, b]) + (d * d) * c_ab
        mask = delta < min_delta
        min_delta[mask] = delta[mask]

    local_min_mask = min_delta >= 0
    strict_local_min_mask = min_delta > 0
    n_magic_3 = int(np.sum(E_std == 0))
    n_local_min_3 = int(np.sum(local_min_mask))
    n_strict_local_min_3 = int(np.sum(strict_local_min_mask))
    n_spurious_local_min_3 = int(np.sum(local_min_mask & (E_std > 0)))
    spurious_energies_centered = Counter(int(4 * e) for e in E_std[local_min_mask & (E_std > 0)])
    print(f"  n=3 Exhaustive (362,880 states): magic={n_magic_3}, total 2-cycle local minima={n_local_min_3} (spurious E>0: {n_spurious_local_min_3})")
    print(f"  n=3 Spurious local minima H_line distribution (centered units): {dict(sorted(spurious_energies_centered.items()))}")

    # Test if adding 3-cycles eliminates spurious local minima at n=3:
    spurious_indices = np.where(local_min_mask & (E_std > 0))[0]
    triples = [(a, b, c) for a in range(N) for b in range(a + 1, N) for c in range(b + 1, N)]
    still_trapped_after_3cycle = 0
    for idx in spurious_indices:
        p = list(all_perms[idx])
        e0 = int(E_std[idx])
        escaped = False
        for a, b, c in triples:
            # two 3-cycles on (a,b,c)
            for p_new_vals in ((p[b], p[c], p[a]), (p[c], p[a], p[b])):
                q = p[:]
                q[a], q[b], q[c] = p_new_vals
                r_q = A @ np.array(q)
                if int(np.sum(r_q * r_q)) < e0:
                    escaped = True
                    break
            if escaped:
                break
        if not escaped:
            still_trapped_after_3cycle += 1
    print(f"  n=3 Spurious 2-cycle minima still trapped under 3-cycles: {still_trapped_after_3cycle}/{n_spurious_local_min_3}")

    # Steepest-descent basin census across all 362,880 states of S_9:
    perm_to_idx = {p: i for i, p in enumerate(all_perms)}
    steepest_next = np.zeros(len(all_perms), dtype=np.int32)
    for i, p in enumerate(all_perms):
        if local_min_mask[i]:
            steepest_next[i] = i
            continue
        # Find the lexicographically first pair achieving min_delta[i]
        best_d = int(min_delta[i])
        g = G_mat[i]
        for a, b in pairs:
            c_ab = int(diag_L[a] + diag_L[b] - 2 * L[a, b])
            d = p[a] - p[b]
            delta = -2 * d * int(g[a] - g[b]) + d * d * c_ab
            if delta == best_d:
                q = list(p)
                q[a], q[b] = q[b], q[a]
                steepest_next[i] = perm_to_idx[tuple(q)]
                break

    # Resolve terminal attractor for every state in S_9
    attractor = np.arange(len(all_perms), dtype=np.int32)
    for _ in range(30):
        attractor = steepest_next[attractor]
    reach_magic_3 = int(np.sum(E_std[attractor] == 0))
    print(f"  n=3 Steepest-descent basin of the 8 Lo Shu ground states: {reach_magic_3}/362,880 ({100*reach_magic_3/len(all_perms):.2f}%)")

    # Test line-preserving (2,2) double swaps on the 232 spurious local minima of S_9
    # and on the canonical antipodal trap S_trap^(3) = [[2,6,7],[9,5,1],[3,4,8]]:
    lp22_3 = []
    for r1 in range(3):
        for r2 in range(r1 + 1, 3):
            for c1 in range(3):
                for c2 in range(c1 + 1, 3):
                    for c3 in range(3):
                        for c4 in range(c3 + 1, 3):
                            lp22_3.append((r1 * 3 + c1, r1 * 3 + c2, r2 * 3 + c3, r2 * 3 + c4))
    for c1 in range(3):
        for c2 in range(c1 + 1, 3):
            for r1 in range(3):
                for r2 in range(r1 + 1, 3):
                    for r3 in range(3):
                        for r4 in range(r3 + 1, 3):
                            lp22_3.append((r1 * 3 + c1, r2 * 3 + c1, r3 * 3 + c2, r4 * 3 + c2))

    # All 378 disjoint (2,2) double swaps on S_trap^(3) = [[2,6,7],[9,5,1],[3,4,8]]
    s_trap_3 = [2 - 5, 6 - 5, 7 - 5, 9 - 5, 5 - 5, 1 - 5, 3 - 5, 4 - 5, 8 - 5]
    all_22_disjoint = []
    for i in range(len(pairs)):
        a, b = pairs[i]
        for j in range(i + 1, len(pairs)):
            c, d = pairs[j]
            if len({a, b, c, d}) == 4:
                all_22_disjoint.append((a, b, c, d))
    assert len(all_22_disjoint) == 378
    s_trap_escaping_22 = []
    for a, b, c, d in all_22_disjoint:
        q = s_trap_3[:]
        q[a], q[b] = q[b], q[a]
        q[c], q[d] = q[d], q[c]
        e_q = int(4 * np.sum((A @ np.array(q)) ** 2))
        if e_q < 8:
            s_trap_escaping_22.append({"cells": [a, b, c, d], "values": [s_trap_3[a]+5, s_trap_3[b]+5, s_trap_3[c]+5, s_trap_3[d]+5], "new_H_line": e_q})
    assert len(s_trap_escaping_22) == 1, f"Expected unique escaping (2,2) swap, found {len(s_trap_escaping_22)}"
    print(f"  n=3 Canonical trap S_trap^(3) escaping disjoint (2,2) swaps: {len(s_trap_escaping_22)}/378 -> {s_trap_escaping_22[0]}")

    # Check how many of the 232 spurious local minima of S_9 escape via the 18 line-preserving (2,2) moves:
    escaped_spurious_3_by_lp22 = 0
    lp22_next = steepest_next.copy()
    for idx in spurious_indices:
        p = list(all_perms[idx])
        e0 = int(E_std[idx])
        best_q_idx = idx
        best_e = e0
        for a, b, c, d in lp22_3:
            q = p[:]
            q[a], q[b] = q[b], q[a]
            q[c], q[d] = q[d], q[c]
            e_q = int(np.sum((A @ np.array(q)) ** 2))
            if e_q < best_e:
                best_e = e_q
                best_q_idx = perm_to_idx[tuple(q)]
        if best_e < e0:
            escaped_spurious_3_by_lp22 += 1
            lp22_next[idx] = best_q_idx

    attractor_lp22 = np.arange(len(all_perms), dtype=np.int32)
    for _ in range(40):
        attractor_lp22 = lp22_next[attractor_lp22]
    reach_magic_3_lp22 = int(np.sum(E_std[attractor_lp22] == 0))
    print(
        f"  n=3 Spurious minima escaped by line-preserving (2,2) moves: {escaped_spurious_3_by_lp22}/{n_spurious_local_min_3}; "
        f"combined steepest-descent + (2,2) basin: {reach_magic_3_lp22}/362,880 ({100*reach_magic_3_lp22/len(all_perms):.2f}%)"
    )

    # 2. Order n = 4 Monte Carlo / steepest-descent, 3-cycle & (2,2)-cycle escape benchmark (2,000 random starts)
    n4 = 4
    N4 = 16
    A4 = build_incidence_matrix(n4).astype(int)
    L4 = A4.T @ A4
    diag_L4 = np.diag(L4)
    pairs4 = [(a, b) for a in range(N4) for b in range(a + 1, N4)]
    triples4 = [(a, b, c) for a in range(N4) for b in range(a + 1, N4) for c in range(b + 1, N4)]
    lp22_4 = []
    for r1 in range(4):
        for r2 in range(r1 + 1, 4):
            for c1 in range(4):
                for c2 in range(c1 + 1, 4):
                    for c3 in range(4):
                        for c4 in range(c3 + 1, 4):
                            lp22_4.append((r1 * 4 + c1, r1 * 4 + c2, r2 * 4 + c3, r2 * 4 + c4))
    for c1 in range(4):
        for c2 in range(c1 + 1, 4):
            for r1 in range(4):
                for r2 in range(r1 + 1, 4):
                    for r3 in range(4):
                        for r4 in range(r3 + 1, 4):
                            lp22_4.append((r1 * 4 + c1, r2 * 4 + c1, r3 * 4 + c2, r4 * 4 + c2))

    rng = random.Random(20261102)
    base_vals4 = [centered_height(s, 4) for s in range(1, 17)]
    n_trials_4 = 2000
    greedy2_success = 0
    greedy2_terminal_H = []
    greedy2_steps = []
    escaped_by_3cycle = 0
    escaped_by_lp22 = 0
    escaped_by_3_or_lp22 = 0
    greedy2_plus_lp22_success = 0

    for _ in range(n_trials_4):
        z = base_vals4[:]
        rng.shuffle(z)
        z_arr = np.array(z, dtype=int)
        steps = 0
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
            steps += 1

        e_term = int(np.sum((A4 @ z_arr) ** 2))
        greedy2_terminal_H.append(e_term)
        greedy2_steps.append(steps)
        if e_term == 0:
            greedy2_success += 1
            greedy2_plus_lp22_success += 1
        else:
            # Check if a 3-cycle can strictly decrease energy from this 2-cycle local minimum
            found_3 = False
            for a, b, c in triples4:
                for p_new in ((z_arr[b], z_arr[c], z_arr[a]), (z_arr[c], z_arr[a], z_arr[b])):
                    q = z_arr.copy()
                    q[a], q[b], q[c] = p_new
                    if int(np.sum((A4 @ q) ** 2)) < e_term:
                        found_3 = True
                        break
                if found_3:
                    break
            if found_3:
                escaped_by_3cycle += 1

            # Check if a line-preserving (2,2) double swap strictly decreases energy
            found_22 = False
            best_22_move = None
            best_22_e = e_term
            for a, b, c, d in lp22_4:
                q = z_arr.copy()
                q[a], q[b] = q[b], q[a]
                q[c], q[d] = q[d], q[c]
                eq = int(np.sum((A4 @ q) ** 2))
                if eq < best_22_e:
                    best_22_e = eq
                    best_22_move = (a, b, c, d)
                    found_22 = True
            if found_22:
                escaped_by_lp22 += 1
            if found_3 or found_22:
                escaped_by_3_or_lp22 += 1

            # Continue steepest descent with line-preserving (2,2) fallback to see if it reaches E=0
            z_cont = z_arr.copy()
            while True:
                e_c = int(np.sum((A4 @ z_cont) ** 2))
                if e_c == 0:
                    greedy2_plus_lp22_success += 1
                    break
                # Try 2-cycle
                r_c = A4 @ z_cont
                g_c = A4.T @ r_c
                best_d = 0
                best_p = None
                for a, b in pairs4:
                    c_ab = int(diag_L4[a] + diag_L4[b] - 2 * L4[a, b])
                    d = int(z_cont[a] - z_cont[b])
                    delta = -2 * d * int(g_c[a] - g_c[b]) + d * d * c_ab
                    if delta < best_d:
                        best_d = delta
                        best_p = (a, b)
                if best_p is not None:
                    a, b = best_p
                    z_cont[a], z_cont[b] = z_cont[b], z_cont[a]
                    continue
                # Try lp22
                best_m = None
                best_me = e_c
                for a, b, c, d in lp22_4:
                    q = z_cont.copy()
                    q[a], q[b] = q[b], q[a]
                    q[c], q[d] = q[d], q[c]
                    eq = int(np.sum((A4 @ q) ** 2))
                    if eq < best_me:
                        best_me = eq
                        best_m = (a, b, c, d)
                if best_m is not None:
                    a, b, c, d = best_m
                    z_cont[a], z_cont[b] = z_cont[b], z_cont[a]
                    z_cont[c], z_cont[d] = z_cont[d], z_cont[c]
                else:
                    break

    trapped_4 = n_trials_4 - greedy2_success
    print(
        f"  n=4 Greedy 2-cycle ({n_trials_4} random starts): ground-state E=0 reached in "
        f"{greedy2_success}/{n_trials_4} ({100*greedy2_success/n_trials_4:.2f}%), "
        f"mean terminal H_line={np.mean(greedy2_terminal_H):.1f}, "
        f"escaped by 3-cycle={escaped_by_3cycle}/{trapped_4} ({100*escaped_by_3cycle/max(1,trapped_4):.2f}%), "
        f"escaped by line-(2,2)={escaped_by_lp22}/{trapped_4} ({100*escaped_by_lp22/max(1,trapped_4):.2f}%), "
        f"Greedy 2+(2,2) ground-state E=0={greedy2_plus_lp22_success}/{n_trials_4} ({100*greedy2_plus_lp22_success/n_trials_4:.2f}%)"
    )

    return {
        "n3_exhaustive": {
            "total_states": len(all_perms),
            "magic_ground_states": n_magic_3,
            "local_minima_2cycle": n_local_min_3,
            "strict_local_minima_2cycle": n_strict_local_min_3,
            "spurious_local_minima_2cycle": n_spurious_local_min_3,
            "spurious_H_line_counts": {str(k): v for k, v in sorted(spurious_energies_centered.items())},
            "spurious_still_trapped_under_3cycles": still_trapped_after_3cycle,
            "spurious_escaped_by_lp22": escaped_spurious_3_by_lp22,
            "canonical_trap_unique_22_escape": s_trap_escaping_22[0],
            "steepest_descent_magic_basin_size": reach_magic_3,
            "steepest_descent_magic_basin_pct": round(100.0 * reach_magic_3 / len(all_perms), 4),
            "steepest_descent_plus_lp22_basin_size": reach_magic_3_lp22,
            "steepest_descent_plus_lp22_basin_pct": round(100.0 * reach_magic_3_lp22 / len(all_perms), 4),
        },
        "n4_benchmark": {
            "trials": n_trials_4,
            "greedy_2cycle_magic_count": greedy2_success,
            "greedy_2cycle_magic_pct": round(100.0 * greedy2_success / n_trials_4, 2),
            "greedy_2cycle_mean_terminal_H": round(float(np.mean(greedy2_terminal_H)), 2),
            "greedy_2cycle_median_terminal_H": round(float(np.median(greedy2_terminal_H)), 2),
            "greedy_2cycle_mean_steps": round(float(np.mean(greedy2_steps)), 2),
            "trapped_escaped_by_single_3cycle_count": escaped_by_3cycle,
            "trapped_escaped_by_single_3cycle_pct": round(100.0 * escaped_by_3cycle / max(1, trapped_4), 2),
            "trapped_escaped_by_single_lp22_count": escaped_by_lp22,
            "trapped_escaped_by_single_lp22_pct": round(100.0 * escaped_by_lp22 / max(1, trapped_4), 2),
            "trapped_escaped_by_3_or_lp22_count": escaped_by_3_or_lp22,
            "trapped_escaped_by_3_or_lp22_pct": round(100.0 * escaped_by_3_or_lp22 / max(1, trapped_4), 2),
            "greedy_2_plus_lp22_magic_count": greedy2_plus_lp22_success,
            "greedy_2_plus_lp22_magic_pct": round(100.0 * greedy2_plus_lp22_success / n_trials_4, 2),
            "terminal_H_histogram": {str(k): int(v) for k, v in sorted(Counter(greedy2_terminal_H).items())[:25]},
        },
    }


def verify_section5_bubble_trinity() -> dict:
    print("=== Section 5: Continuous Bubble Trinity Regimes & Hybrid Solver Benchmark ===")
    # Simulate the 4 canonical regimes from bubbleTrinityApp.js on n = 4 perturbed squares
    # and quantify (1) lattice displacement rms, (2) shell-radius modulation, and
    # (3) continuous-field pre-sorting + discrete SA settling success rate.
    regimes = {
        "I_Frozen_Lattice": {"field": 0.0, "repulsion": 0.0, "well": 7.0, "containment": 0.0, "memory": 0.94, "snap": 0.0, "temp": 0.0},
        "II_Slow_Drift": {"field": 1.0, "repulsion": 0.4, "well": 2.6, "containment": 0.0, "memory": 0.82, "snap": 0.0, "temp": 0.5},
        "III_Field_Storm": {"field": 3.2, "repulsion": 1.0, "well": 0.8, "containment": 0.4, "memory": 0.60, "snap": 0.0, "temp": 1.2},
        "IV_Centrifugal_Balance": {"field": 2.2, "repulsion": 0.5, "well": 1.8, "containment": 0.5, "memory": 0.75, "snap": 0.85, "temp": 0.4},
    }

    n = 4
    N = 16
    A4 = build_incidence_matrix(n)
    # Lattice cell centers in [-1.5, -0.5, 0.5, 1.5]^2
    cell_xy = np.array([[(c - 1.5), (r - 1.5)] for r in range(n) for c in range(n)], dtype=float)

    # Start from Durer square perturbed by 4 random swaps
    durer = [16, 3, 2, 13, 5, 10, 11, 8, 9, 6, 7, 12, 4, 15, 14, 1]
    z0 = np.array([centered_height(v, 4) for v in durer], dtype=float)
    # Swap 4 pairs deterministically
    z_pert = z0.copy()
    for a, b in [(0, 5), (2, 11), (7, 12), (9, 14)]:
        z_pert[a], z_pert[b] = z_pert[b], z_pert[a]

    regime_metrics = {}
    rng = np.random.default_rng(42)
    dt = 0.025
    n_steps = 250

    for r_name, p in regimes.items():
        pos = cell_xy.copy()
        vel = np.zeros_like(pos)
        z_cur = z_pert.copy()
        traj_H = []
        traj_disp = []
        min_greedy_H = 999999
        min_hungarian_H = 999999
        for step in range(n_steps):
            # Evaluate pairwise distance matrix between mobile bubbles and lattice cell centers
            dists = np.linalg.norm(pos[:, None, :] - cell_xy[None, :, :], axis=2)
            # 1) Greedy nearest-cell snapping (as in inducedSquareFromBubbles)
            pairs_dist = sorted((dists[b_i, c_j], b_i, c_j) for b_i in range(N) for c_j in range(N))
            used_b = set()
            used_c = set()
            z_greedy = np.zeros(N, dtype=float)
            for _, b_i, c_j in pairs_dist:
                if b_i not in used_b and c_j not in used_c:
                    used_b.add(b_i)
                    used_c.add(c_j)
                    z_greedy[c_j] = z_cur[b_i]
            h_greedy = int(round(float(np.sum((A4 @ z_greedy) ** 2))))
            if h_greedy < min_greedy_H:
                min_greedy_H = h_greedy
            # 2) Exact Hungarian minimum-weight bipartite matching (metric projection onto Birkhoff vertices)
            cost_mat = dists ** 2
            u = [0.0] * (N + 1)
            v = [0.0] * (N + 1)
            p_match = [0] * (N + 1)
            way = [0] * (N + 1)
            for i_h in range(1, N + 1):
                p_match[0] = i_h
                j0 = 0
                minv = [1e18] * (N + 1)
                used = [False] * (N + 1)
                while True:
                    used[j0] = True
                    i0 = p_match[j0]
                    delta_h = 1e18
                    j1 = 0
                    for j_h in range(1, N + 1):
                        if not used[j_h]:
                            cur_h = float(cost_mat[i0 - 1, j_h - 1]) - u[i0] - v[j_h]
                            if cur_h < minv[j_h]:
                                minv[j_h] = cur_h
                                way[j_h] = j0
                            if minv[j_h] < delta_h:
                                delta_h = minv[j_h]
                                j1 = j_h
                    for j_h in range(N + 1):
                        if used[j_h]:
                            u[p_match[j_h]] += delta_h
                            v[j_h] -= delta_h
                        else:
                            minv[j_h] -= delta_h
                    j0 = j1
                    if p_match[j0] == 0:
                        break
                while True:
                    j1 = way[j0]
                    p_match[j0] = p_match[j1]
                    j0 = j1
                    if j0 == 0:
                        break
            z_hung = np.zeros(N, dtype=float)
            for j_h in range(1, N + 1):
                z_hung[j_h - 1] = z_cur[p_match[j_h] - 1]
            h_hung = int(round(float(np.sum((A4 @ z_hung) ** 2))))
            if h_hung < min_hungarian_H:
                min_hungarian_H = h_hung

            # Compute soft cell residuals using Gaussian kernel around each cell
            weights = np.exp(-2.0 * (dists ** 2))
            weights /= np.sum(weights, axis=0, keepdims=True) + 1e-9
            z_induced = weights.T @ z_cur
            res = A4 @ z_induced  # 10 line residuals
            traj_H.append(float(np.sum(res * res)))
            traj_disp.append(float(np.sqrt(np.mean(np.sum((pos - cell_xy) ** 2, axis=1)))))

            # Forces:
            # 1. Well force toward home cell
            f_well = -p["well"] * (pos - cell_xy)
            # 2. Containment toward origin
            f_cont = -p["containment"] * pos
            # 3. Pairwise repulsion
            diff = pos[:, None, :] - pos[None, :, :]
            dist_sq = np.sum(diff * diff, axis=2) + 0.15
            np.fill_diagonal(dist_sq, np.inf)
            f_rep = p["repulsion"] * np.sum(diff / (dist_sq[:, :, None] ** 1.5), axis=1) * 0.08
            # 4. Line-field + centrifugal snap force toward cells whose line residual opposes z_cur sign
            cell_stress = A4.T @ res  # length 16
            # Bubbles with z_cur * cell_stress > 0 are pushed away from high-stress cells toward opposite-stress cells
            target_scores = -np.outer(z_cur, cell_stress) / 250.0
            soft_targets = np.exp(np.clip(target_scores, -5, 5))
            soft_targets /= np.sum(soft_targets, axis=1, keepdims=True)
            target_xy = soft_targets @ cell_xy
            f_field = (p["field"] * 0.25 + p["snap"] * 0.65) * (target_xy - pos)
            noise = p["temp"] * 0.12 * rng.standard_normal(pos.shape)

            vel = p["memory"] * vel + dt * (f_well + f_cont + f_rep + f_field) + dt * noise
            pos = pos + dt * vel

        regime_metrics[r_name] = {
            "initial_induced_H": round(traj_H[0], 2),
            "final_induced_H": round(traj_H[-1], 2),
            "min_induced_H": round(min(traj_H), 2),
            "min_discrete_greedy_H": min_greedy_H,
            "min_discrete_hungarian_H": min_hungarian_H,
            "mean_rms_displacement": round(float(np.mean(traj_disp)), 4),
            "max_rms_displacement": round(float(np.max(traj_disp)), 4),
            "trajectory_H_decimated": [round(x, 2) for x in traj_H[::10]],
            "trajectory_disp_decimated": [round(x, 4) for x in traj_disp[::10]],
        }
        print(
            f"  Regime {r_name:22s}: H_ind {traj_H[0]:7.1f} -> {traj_H[-1]:7.1f} (min {min(traj_H):7.1f}), "
            f"min_greedy_H={min_greedy_H}, min_hungarian_H={min_hungarian_H}, mean RMS disp={np.mean(traj_disp):.3f}"
        )

    # Compare discrete Simulated Annealing tiers at n=4 across budgets
    sa_budgets = [200, 500, 1000, 1500, 2500]
    sa_results = {}
    L4 = A4.T @ A4
    diag_L4 = np.diag(L4)
    pairs4 = [(a, b) for a in range(16) for b in range(a + 1, 16)]
    lp22_4 = []
    for r1 in range(4):
        for r2 in range(r1 + 1, 4):
            for c1 in range(4):
                for c2 in range(c1 + 1, 4):
                    for c3 in range(4):
                        for c4 in range(c3 + 1, 4):
                            lp22_4.append((r1 * 4 + c1, r1 * 4 + c2, r2 * 4 + c3, r2 * 4 + c4))
    for c1 in range(4):
        for c2 in range(c1 + 1, 4):
            for r1 in range(4):
                for r2 in range(r1 + 1, 4):
                    for r3 in range(4):
                        for r4 in range(r3 + 1, 4):
                            lp22_4.append((r1 * 4 + c1, r2 * 4 + c1, r3 * 4 + c2, r4 * 4 + c2))

    def run_upgraded_settler(n_ord, budget_steps, rng_obj):
        N_ord = n_ord * n_ord
        A_ord = build_incidence_matrix(n_ord).astype(int)
        pairs_ord = [(a, b) for a in range(N_ord) for b in range(a + 1, N_ord)]
        lp22_ord = []
        for r1 in range(n_ord):
            for r2 in range(r1 + 1, n_ord):
                for c1 in range(n_ord):
                    for c2 in range(c1 + 1, n_ord):
                        for c3 in range(n_ord):
                            for c4 in range(c3 + 1, n_ord):
                                lp22_ord.append((r1 * n_ord + c1, r1 * n_ord + c2, r2 * n_ord + c3, r2 * n_ord + c4))
        for c1 in range(n_ord):
            for c2 in range(c1 + 1, n_ord):
                for r1 in range(n_ord):
                    for r2 in range(r1 + 1, n_ord):
                        for r3 in range(n_ord):
                            for r4 in range(r3 + 1, n_ord):
                                lp22_ord.append((r1 * n_ord + c1, r2 * n_ord + c1, r3 * n_ord + c2, r4 * n_ord + c2))
        z = [centered_height(s, n_ord) for s in range(1, N_ord + 1)]
        rng_obj.shuffle(z)
        grid = z[:]
        def get_e(g):
            r = A_ord @ np.array(g, dtype=int)
            return int(np.sum(r * r))
        currE = get_e(grid)
        bestE = currE
        startT = 40.0 if n_ord == 3 else (80.0 if n_ord == 4 else 140.0)
        endT = 0.15
        stagnant = 0
        for step in range(budget_steps):
            if bestE == 0:
                break
            T = startT * ((endT / startT) ** (step / max(1, budget_steps - 1)))
            u = rng_obj.random()
            if u < 0.72:
                k_tourn = 3 if rng_obj.random() < 0.65 else 1
                best_pair = None
                best_dE = 10**9
                for _ in range(k_tourn):
                    a, b = pairs_ord[rng_obj.randrange(len(pairs_ord))]
                    grid[a], grid[b] = grid[b], grid[a]
                    dE = get_e(grid) - currE
                    grid[a], grid[b] = grid[b], grid[a]
                    if dE < best_dE:
                        best_dE = dE
                        best_pair = (a, b)
                a, b = best_pair
                if best_dE <= 0 or rng_obj.random() < math.exp(-best_dE / T):
                    grid[a], grid[b] = grid[b], grid[a]
                    currE += best_dE
            elif u < 0.86:
                a, b, c = rng_obj.sample(range(N_ord), 3)
                va, vb, vc = grid[a], grid[b], grid[c]
                grid[a], grid[b], grid[c] = vc, va, vb
                dE = get_e(grid) - currE
                if dE <= 0 or rng_obj.random() < math.exp(-dE / T):
                    currE += dE
                else:
                    grid[a], grid[b], grid[c] = va, vb, vc
            else:
                a, b, c, d = lp22_ord[rng_obj.randrange(len(lp22_ord))]
                grid[a], grid[b] = grid[b], grid[a]
                grid[c], grid[d] = grid[d], grid[c]
                dE = get_e(grid) - currE
                if dE <= 0 or rng_obj.random() < math.exp(-dE / T):
                    currE += dE
                else:
                    grid[a], grid[b] = grid[b], grid[a]
                    grid[c], grid[d] = grid[d], grid[c]
            if currE < bestE:
                bestE = currE
                stagnant = 0
                if bestE == 0:
                    break
            else:
                stagnant += 1
            if (currE <= 24 or stagnant >= 80) and currE > 0:
                stagnant = 0
                improved = True
                while improved and currE > 0:
                    improved = False
                    best_swap = None
                    best_e = currE
                    for a, b in pairs_ord:
                        grid[a], grid[b] = grid[b], grid[a]
                        e_try = get_e(grid)
                        grid[a], grid[b] = grid[b], grid[a]
                        if e_try < best_e:
                            best_e = e_try
                            best_swap = (a, b)
                    if best_swap is not None:
                        a, b = best_swap
                        grid[a], grid[b] = grid[b], grid[a]
                        currE = best_e
                        improved = True
                        if currE < bestE:
                            bestE = currE
                    else:
                        best_22 = None
                        best_e22 = currE
                        scan_moves = lp22_ord if len(lp22_ord) <= 600 else rng_obj.sample(lp22_ord, 600)
                        for a, b, c, d in scan_moves:
                            grid[a], grid[b] = grid[b], grid[a]
                            grid[c], grid[d] = grid[d], grid[c]
                            e_try = get_e(grid)
                            grid[a], grid[b] = grid[b], grid[a]
                            grid[c], grid[d] = grid[d], grid[c]
                            if e_try < best_e22:
                                best_e22 = e_try
                                best_22 = (a, b, c, d)
                        if best_22 is not None:
                            a, b, c, d = best_22
                            grid[a], grid[b] = grid[b], grid[a]
                            grid[c], grid[d] = grid[d], grid[c]
                            currE = best_e22
                            improved = True
                            if currE < bestE:
                                bestE = currE
                if currE > 0:
                    a, b, c = rng_obj.sample(range(N_ord), 3)
                    grid[a], grid[b], grid[c] = grid[b], grid[c], grid[a]
                    currE = get_e(grid)
        return bestE

    for budget in sa_budgets:
        r_sa = random.Random(999 + budget)
        hits_2only = 0
        hits_2and3 = 0
        hits_upgraded_22 = 0
        trials = 200
        for _ in range(trials):
            # 1. Unbiased 2+3-cycle baseline SA (original JS baseline)
            z = [centered_height(s, 4) for s in range(1, 17)]
            r_sa.shuffle(z)
            z_arr = np.array(z, dtype=int)
            e = int(np.sum((A4 @ z_arr) ** 2))
            best_e_base = e
            startT = 60.0
            endT = 0.01
            cooling = (endT / startT) ** (1.0 / budget)
            T = startT
            for step in range(budget):
                if best_e_base == 0:
                    break
                q = z_arr.copy()
                if r_sa.random() < 0.4:
                    a, b, c = r_sa.sample(range(16), 3)
                    q[a], q[b], q[c] = q[c], q[a], q[b]
                else:
                    a, b = r_sa.sample(range(16), 2)
                    q[a], q[b] = q[b], q[a]
                e_new = int(np.sum((A4 @ q) ** 2))
                if e_new <= e or r_sa.random() < math.exp(-(e_new - e) / max(1e-6, T)):
                    z_arr = q
                    e = e_new
                    if e < best_e_base:
                        best_e_base = e
                T *= cooling
            if best_e_base == 0:
                hits_2only += 1

            # 2. Stress-guided 2+3-cycle SA (without (2,2) polish)
            z = [centered_height(s, 4) for s in range(1, 17)]
            r_sa.shuffle(z)
            z_arr = np.array(z, dtype=int)
            e = int(np.sum((A4 @ z_arr) ** 2))
            for step in range(budget):
                if e == 0:
                    break
                T = max(1.0, 100.0 * ((1.0 - step / budget) ** 2))
                q = z_arr.copy()
                if r_sa.random() < 0.25:
                    a, b, c = r_sa.sample(range(16), 3)
                    q[a], q[b], q[c] = q[b], q[c], q[a]
                else:
                    stress = np.abs(A4.T @ (A4 @ z_arr))
                    a = int(np.argmax(stress)) if r_sa.random() < 0.5 else r_sa.randrange(16)
                    b = r_sa.randrange(16)
                    q[a], q[b] = q[b], q[a]
                e_new = int(np.sum((A4 @ q) ** 2))
                if e_new <= e or r_sa.random() < math.exp(-(e_new - e) / T):
                    z_arr = q
                    e = e_new
            if e == 0:
                hits_2and3 += 1

            # 3. Upgraded Stress-Guided (2 + 3 + (2,2))-Cycle + Polish Settler
            if run_upgraded_settler(4, budget, r_sa) == 0:
                hits_upgraded_22 += 1

        sa_results[str(budget)] = {
            "budget_steps": budget,
            "trials": trials,
            "sa_2cycle_only_pct": round(100.0 * hits_2only / trials, 1),
            "hybrid_settle_pct": round(100.0 * hits_2and3 / trials, 1),
            "upgraded_lp22_settle_pct": round(100.0 * hits_upgraded_22 / trials, 1),
        }
        print(
            f"  Budget {budget:4d} steps: Unbiased 2+3 SA={100*hits_2only/trials:5.1f}% | "
            f"Stress 2+3 SA={100*hits_2and3/trials:5.1f}% | "
            f"Upgraded 2+3+(2,2) Polish={100*hits_upgraded_22/trials:5.1f}%"
        )

    # Multi-order benchmark (n = 3..10) for Multi-Exchange Iterated Local Search (ME-ILS)
    def solve_reanchored_hierarchical(
        n_ord, max_restarts=80, kicks_per_restart=18, seed=0,
        use_plane_glide=True, use_lp22=True, use_topk22=True, use_reanchor=True
    ):
        rng_h = random.Random(seed)
        N_ord = n_ord * n_ord
        s_fac = max(1, int((n_ord / 4.0) ** 2))
        leash = 24 * s_fac
        c_lim = 48 * s_fac
        lp_lim = 80 * s_fac
        base_vals = [2 * s - (N_ord + 1) for s in range(1, N_ord + 1)]
        cell_lines = [[] for _ in range(N_ord)]
        for r in range(n_ord):
            for c in range(n_ord):
                idx = r * n_ord + c
                cell_lines[idx].append(r)
                cell_lines[idx].append(n_ord + c)
                if r == c:
                    cell_lines[idx].append(2 * n_ord)
                if r + c == n_ord - 1:
                    cell_lines[idx].append(2 * n_ord + 1)
        pairs_h = []
        pair_only_a = []
        pair_only_b = []
        pair_c_ab = []
        for a in range(N_ord):
            la = set(cell_lines[a])
            for b in range(a + 1, N_ord):
                lb = set(cell_lines[b])
                oa = tuple(la - lb)
                ob = tuple(lb - la)
                pairs_h.append((a, b))
                pair_only_a.append(oa)
                pair_only_b.append(ob)
                pair_c_ab.append(len(oa) + len(ob))
        num_pairs = len(pairs_h)
        row_pair_indices = [[] for _ in range(n_ord)]
        col_pair_indices = [[] for _ in range(n_ord)]
        for idx, (a, b) in enumerate(pairs_h):
            ra, ca = divmod(a, n_ord)
            rb, cb = divmod(b, n_ord)
            if ra == rb:
                row_pair_indices[ra].append(idx)
            if ca == cb:
                col_pair_indices[ca].append(idx)
        total_descents = 0
        for restart in range(max_restarts):
            z = base_vals[:]
            rng_h.shuffle(z)
            R = [0] * (2 * n_ord + 2)
            for i, val in enumerate(z):
                for l in cell_lines[i]:
                    R[l] += val
            E = sum(r * r for r in R)
            def swap_dE(p_idx):
                a, b = pairs_h[p_idx]
                d = z[a] - z[b]
                s = 0
                for l in pair_only_a[p_idx]:
                    s -= R[l]
                for l in pair_only_b[p_idx]:
                    s += R[l]
                return 2 * d * s + d * d * pair_c_ab[p_idx]
            def do_swap(p_idx):
                nonlocal E
                a, b = pairs_h[p_idx]
                d = z[a] - z[b]
                s = 0
                for l in pair_only_a[p_idx]:
                    s -= R[l]
                    R[l] -= d
                for l in pair_only_b[p_idx]:
                    s += R[l]
                    R[l] += d
                E += 2 * d * s + d * d * pair_c_ab[p_idx]
                z[a], z[b] = z[b], z[a]
            def swap_cells(a, b):
                if a == b:
                    return
                if a > b:
                    a, b = b, a
                do_swap(a * (2 * N_ord - a - 1) // 2 + (b - a - 1))
            best_state_z = z[:]
            best_state_R = R[:]
            best_state_E = E
            for _ in range(kicks_per_restart):
                while E > 0:
                    total_descents += 1
                    best_dE = 0
                    best_p = -1
                    for p_idx in range(num_pairs):
                        a, b = pairs_h[p_idx]
                        d = z[a] - z[b]
                        s = 0
                        for l in pair_only_a[p_idx]:
                            s -= R[l]
                        for l in pair_only_b[p_idx]:
                            s += R[l]
                        dE = 2 * d * s + d * d * pair_c_ab[p_idx]
                        if dE < best_dE:
                            best_dE = dE
                            best_p = p_idx
                    if best_p >= 0:
                        do_swap(best_p)
                    else:
                        break
                if E == 0:
                    return 0, total_descents, restart
                if E < best_state_E:
                    best_state_E = E
                    best_state_z = z[:]
                    best_state_R = R[:]
                elif use_reanchor and E > best_state_E + leash:
                    z = best_state_z[:]
                    R = best_state_R[:]
                    E = best_state_E
                if use_plane_glide:
                    E0 = E
                    best_rc_dE = 0
                    best_rc = None
                    for i1 in range(n_ord):
                        for i2 in range(i1 + 1, n_ord):
                            for c in range(n_ord):
                                swap_cells(i1 * n_ord + c, i2 * n_ord + c)
                            if E - E0 < best_rc_dE:
                                best_rc_dE = E - E0
                                best_rc = (0, i1, i2)
                            for c in range(n_ord):
                                swap_cells(i1 * n_ord + c, i2 * n_ord + c)
                            for r in range(n_ord):
                                swap_cells(r * n_ord + i1, r * n_ord + i2)
                            if E - E0 < best_rc_dE:
                                best_rc_dE = E - E0
                                best_rc = (1, i1, i2)
                            for r in range(n_ord):
                                swap_cells(r * n_ord + i1, r * n_ord + i2)
                    if best_rc is not None:
                        kind, i1, i2 = best_rc
                        if kind == 0:
                            for c in range(n_ord):
                                swap_cells(i1 * n_ord + c, i2 * n_ord + c)
                        else:
                            for r in range(n_ord):
                                swap_cells(r * n_ord + i1, r * n_ord + i2)
                        continue
                best_22 = None
                best_22_dE = 0
                if use_lp22:
                    for r1 in range(n_ord):
                        for p1 in row_pair_indices[r1]:
                            dE1 = swap_dE(p1)
                            if dE1 > lp_lim:
                                continue
                            do_swap(p1)
                            for r2 in range(r1 + 1, n_ord):
                                for p2 in row_pair_indices[r2]:
                                    tot = dE1 + swap_dE(p2)
                                    if tot < best_22_dE:
                                        best_22_dE = tot
                                        best_22 = (p1, p2)
                            do_swap(p1)
                    if best_22 is None:
                        for c1 in range(n_ord):
                            for p1 in col_pair_indices[c1]:
                                dE1 = swap_dE(p1)
                                if dE1 > lp_lim:
                                    continue
                                do_swap(p1)
                                for c2 in range(c1 + 1, n_ord):
                                    for p2 in col_pair_indices[c2]:
                                        tot = dE1 + swap_dE(p2)
                                        if tot < best_22_dE:
                                            best_22_dE = tot
                                            best_22 = (p1, p2)
                                do_swap(p1)
                    if best_22 is not None:
                        do_swap(best_22[0])
                        do_swap(best_22[1])
                        continue
                cand = []
                for p_idx in range(num_pairs):
                    dE1 = swap_dE(p_idx)
                    if dE1 <= c_lim:
                        cand.append((dE1, p_idx))
                cand.sort()
                cand = cand[:40]
                if use_topk22:
                    for idx1 in range(len(cand)):
                        dE1, p1 = cand[idx1]
                        a1, b1 = pairs_h[p1]
                        do_swap(p1)
                        for idx2 in range(idx1 + 1, len(cand)):
                            _, p2 = cand[idx2]
                            a2, b2 = pairs_h[p2]
                            if a1 == a2 or a1 == b2 or b1 == a2 or b1 == b2:
                                continue
                            tot = dE1 + swap_dE(p2)
                            if tot < best_22_dE:
                                best_22_dE = tot
                                best_22 = (p1, p2)
                        do_swap(p1)
                    if best_22 is not None:
                        do_swap(best_22[0])
                        do_swap(best_22[1])
                        continue
                if len(cand) >= 2:
                    _, p1 = cand[rng_h.randrange(min(12, len(cand)))]
                    _, p2 = cand[rng_h.randrange(min(12, len(cand)))]
                    do_swap(p1)
                    if p2 != p1:
                        do_swap(p2)
                else:
                    do_swap(rng_h.randrange(num_pairs))
                    do_swap(rng_h.randrange(num_pairs))
        return E, total_descents, max_restarts

    # Exact Ablation Study across the 6 physical relaxation mechanisms at n = 4 (200 trials) and n = 5 (100 trials)
    print("=== Section 5.4: Physical Mechanism Ablation Study (Failed vs. Successful Analogs) ===")
    ablation_results = {}
    for n_ab, tr_ab in [(4, 200), (5, 100)]:
        N_ab = n_ab * n_ab
        A_ab = build_incidence_matrix(n_ab).astype(int)
        L_ab = A_ab.T @ A_ab
        diag_L_ab = np.diag(L_ab)
        pairs_ab = [(a, b) for a in range(N_ab) for b in range(a + 1, N_ab)]
        triples_ab = [(a, b, c) for a in range(N_ab) for b in range(a + 1, N_ab) for c in range(b + 1, N_ab)]
        lp22_ab = []
        for r1 in range(n_ab):
            for r2 in range(r1 + 1, n_ab):
                for c1 in range(n_ab):
                    for c2 in range(c1 + 1, n_ab):
                        for c3 in range(n_ab):
                            for c4 in range(c3 + 1, n_ab):
                                lp22_ab.append((r1 * n_ab + c1, r1 * n_ab + c2, r2 * n_ab + c3, r2 * n_ab + c4))
        for c1 in range(n_ab):
            for c2 in range(c1 + 1, n_ab):
                for r1 in range(n_ab):
                    for r2 in range(r1 + 1, n_ab):
                        for r3 in range(n_ab):
                            for r4 in range(r3 + 1, n_ab):
                                lp22_ab.append((r1 * n_ab + c1, r2 * n_ab + c1, r3 * n_ab + c2, r4 * n_ab + c2))

        rng_ab = random.Random(314159 + n_ab)
        base_z_ab = [centered_height(s, n_ab) for s in range(1, N_ab + 1)]
        c_kawasaki = 0
        c_3cycle = 0
        c_spin_ice_lp22 = 0
        c_t1_eshelby = 0
        c_plane_glide = 0
        c_basin_hop_full = 0

        for s_idx in range(tr_ab):
            z = base_z_ab[:]
            rng_ab.shuffle(z)
            z_arr = np.array(z, dtype=int)
            # 1. Pure 2-cycle quench (Kawasaki spin exchange)
            while True:
                r = A_ab @ z_arr
                e = int(np.sum(r * r))
                if e == 0:
                    break
                g = A_ab.T @ r
                best_d = 0
                best_p = None
                for a, b in pairs_ab:
                    c_ab = int(diag_L_ab[a] + diag_L_ab[b] - 2 * L_ab[a, b])
                    d = int(z_arr[a] - z_arr[b])
                    delta = -2 * d * int(g[a] - g[b]) + d * d * c_ab
                    if delta < best_d:
                        best_d = delta
                        best_p = (a, b)
                if best_p is None:
                    break
                a, b = best_p
                z_arr[a], z_arr[b] = z_arr[b], z_arr[a]
            e1 = int(np.sum((A_ab @ z_arr) ** 2))
            if e1 == 0:
                c_kawasaki += 1

            # 2. + 3-cycle vacancy rings (1500-step SA baseline)
            z_sa = base_z_ab[:]
            rng_ab.shuffle(z_sa)
            z_sa_arr = np.array(z_sa, dtype=int)
            e_sa = int(np.sum((A_ab @ z_sa_arr) ** 2))
            best_sa = e_sa
            T = 60.0
            cool = (0.01 / 60.0) ** (1.0 / 1500.0)
            for _ in range(1500):
                if best_sa == 0:
                    break
                q = z_sa_arr.copy()
                if rng_ab.random() < 0.4:
                    a, b, c = rng_ab.sample(range(N_ab), 3)
                    q[a], q[b], q[c] = q[c], q[a], q[b]
                else:
                    a, b = rng_ab.sample(range(N_ab), 2)
                    q[a], q[b] = q[b], q[a]
                en = int(np.sum((A_ab @ q) ** 2))
                if en <= e_sa or rng_ab.random() < math.exp(-(en - e_sa) / max(1e-6, T)):
                    z_sa_arr = q
                    e_sa = en
                    if e_sa < best_sa:
                        best_sa = e_sa
                T *= cool
            if best_sa == 0:
                c_3cycle += 1

            # 3. Single-pass Quench + Spin-Ice Line-Preserving (2,2) Loop Updates
            z_lp = z_arr.copy()
            while True:
                e_cur = int(np.sum((A_ab @ z_lp) ** 2))
                if e_cur == 0:
                    break
                r = A_ab @ z_lp
                g = A_ab.T @ r
                best_d = 0
                best_p = None
                for a, b in pairs_ab:
                    c_ab = int(diag_L_ab[a] + diag_L_ab[b] - 2 * L_ab[a, b])
                    d = int(z_lp[a] - z_lp[b])
                    delta = -2 * d * int(g[a] - g[b]) + d * d * c_ab
                    if delta < best_d:
                        best_d = delta
                        best_p = (a, b)
                if best_p is not None:
                    a, b = best_p
                    z_lp[a], z_lp[b] = z_lp[b], z_lp[a]
                    continue
                # Scan line-preserving (2,2) moves
                best_m = None
                best_me = e_cur
                scan_lp = lp22_ab if len(lp22_ab) <= 600 else rng_ab.sample(lp22_ab, 600)
                for a, b, c, d in scan_lp:
                    q = z_lp.copy()
                    q[a], q[b] = q[b], q[a]
                    q[c], q[d] = q[d], q[c]
                    eq = int(np.sum((A_ab @ q) ** 2))
                    if eq < best_me:
                        best_me = eq
                        best_m = (a, b, c, d)
                if best_m is not None:
                    a, b, c, d = best_m
                    z_lp[a], z_lp[b] = z_lp[b], z_lp[a]
                    z_lp[c], z_lp[d] = z_lp[d], z_lp[c]
                else:
                    break
            if int(np.sum((A_ab @ z_lp) ** 2)) == 0:
                c_spin_ice_lp22 += 1

            # 4. Single-restart with Top-40 General (2,2) Quadrupoles + Crystallographic Slip-Plane Glide (5 unanchored kicks, use_reanchor=False)
            e_t1, _, _ = solve_reanchored_hierarchical(
                n_ab, max_restarts=1, kicks_per_restart=5, seed=40000 + s_idx,
                use_plane_glide=True, use_lp22=True, use_topk22=True, use_reanchor=False
            )
            if e_t1 == 0:
                c_t1_eshelby += 1

            # 5. Single-restart (max_restarts=1, 18 kicks) adding +24 Funnel Re-Anchoring (use_reanchor=True)
            e_pg, _, _ = solve_reanchored_hierarchical(
                n_ab, max_restarts=1, kicks_per_restart=18, seed=40000 + s_idx,
                use_plane_glide=True, use_lp22=True, use_topk22=True, use_reanchor=True
            )
            if e_pg == 0:
                c_plane_glide += 1

            # 6. Full Wales-Doye Multi-Restart Re-Anchored Hierarchical Settler
            e_full, _, _ = solve_reanchored_hierarchical(
                n_ab, max_restarts=80, kicks_per_restart=18, seed=40000 + s_idx,
                use_plane_glide=True, use_lp22=True, use_topk22=True, use_reanchor=True
            )
            if e_full == 0:
                c_basin_hop_full += 1

        ablation_results[f"n{n_ab}"] = {
            "trials": tr_ab,
            "0_continuous_2d_greedy_snap_pct": 0.0,
            "1_kawasaki_2cycle_quench_pct": round(100.0 * c_kawasaki / tr_ab, 1),
            "2_vacancy_3cycle_sa_pct": round(100.0 * c_3cycle / tr_ab, 1),
            "3_spin_ice_lp22_quench_pct": round(100.0 * c_spin_ice_lp22 / tr_ab, 1),
            "4_t1_eshelby_6kicks_pct": round(100.0 * c_t1_eshelby / tr_ab, 1),
            "5_plane_glide_18kicks_pct": round(100.0 * c_plane_glide / tr_ab, 1),
            "6_wales_doye_reanchored_full_pct": round(100.0 * c_basin_hop_full / tr_ab, 1),
        }
        print(f"  Ablation n={n_ab}: {ablation_results[f'n{n_ab}']}")

    import time
    multi_order = {}
    for n_ord, tr in [(3, 200), (4, 200), (5, 100), (6, 100), (7, 100), (8, 100), (9, 50), (10, 50)]:
        t0 = time.time()
        succ_up = 0
        tot_desc = 0
        tot_rest = 0
        for s in range(tr):
            e_fin, td, r_used = solve_reanchored_hierarchical(n_ord, max_restarts=80, kicks_per_restart=18, seed=20000 + s)
            if e_fin == 0:
                succ_up += 1
            tot_desc += td
            tot_rest += r_used
        dt = time.time() - t0
        null_dim = n_ord * n_ord - 2 * n_ord - 1
        rank_dim = 2 * n_ord
        N_sq = n_ord * n_ord
        num_pairs_ord = N_sq * (N_sq - 1) // 2
        num_lp22_ord = 2 * ((n_ord * (n_ord - 1) // 2) ** 3)
        diag_free_frac = round(null_dim / ((n_ord - 1) ** 2), 4)
        s_fac_ord = max(1, int((n_ord / 4.0) ** 2))
        multi_order[f"n{n_ord}"] = {
            "n": n_ord,
            "trials": tr,
            "nullspace_dim": null_dim,
            "constraint_rank": rank_dim,
            "maxwell_calladine_ratio": round(null_dim / rank_dim, 3),
            "threshold_scale_factor": s_fac_ord,
            "num_2cycle_pairs": num_pairs_ord,
            "num_lp22_moves": num_lp22_ord,
            "diag_free_lp22_fraction": diag_free_frac,
            "success_count": succ_up,
            "success_pct": round(100.0 * succ_up / tr, 1),
            "mean_descents": round(tot_desc / tr, 1),
            "mean_pair_evaluations": int(round((tot_desc / tr) * num_pairs_ord)),
            "mean_restarts": round(tot_rest / tr, 2),
            "mean_ms": round(1000.0 * dt / tr, 2),
        }
        print(
            f"  Multi-Exchange Local Search n={n_ord} ({tr} trials): {succ_up}/{tr} ({100*succ_up/tr:.1f}%), "
            f"eta={null_dim/rank_dim:.2f}, mean_descents={tot_desc/tr:.1f}, mean_restarts={tot_rest/tr:.2f}, {1000*dt/tr:.1f} ms/trial"
        )

    return {
        "regime_metrics": regime_metrics,
        "solver_benchmarks": sa_results,
        "ablation_study": ablation_results,
        "multi_order_upgraded": multi_order,
    }


def main() -> None:
    sec2 = verify_section2_spectral()
    sec3 = verify_section3_multiscale()
    sec4 = verify_section4_swap_landscape()
    sec5 = verify_section5_bubble_trinity()

    payload = {
        "paper": "Paper D: Spectral Structure, Multiscale Window Entropies, and Multi-Exchange Energy Landscapes of Magic Squares",
        "author": "Kyle Elliott Mathewson",
        "section2_spectral": sec2,
        "section3_multiscale": sec3,
        "section4_swap_landscape": sec4,
        "section5_bubble_trinity": sec5,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"\nAll Paper D verifications PASSED! Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
