#!/usr/bin/env python3.9
"""
Numerical verification of every claim in sections/drafts/theory.tex
(Magic Gems, revision v5).  All identities that are claimed to be exact are
checked in exact arithmetic (Python integers / fractions.Fraction); floating
point is used only for ranks/eigenvalues and for the random searches.

Conventions (shared with the other agents):
  cells (i,j), 0 <= i,j <= n-1,  N = n^2
  x_ij = j - (n-1)/2,  y_ij = (n-1)/2 - i,  z_ij = s_ij - (N+1)/2
  Cov(phi, Z) = (1/N) sum (phi - mean phi) z
  R_k = 1{i=k}, C_l = 1{j=l}, D_main = 1{i=j}, D_anti = 1{i+j=n-1}
  E_full(S) = sum_k Cov(R_k,Z)^2 + sum_l Cov(C_l,Z)^2 + Cov(D_main,Z)^2 + Cov(D_anti,Z)^2
              (ALL n rows and ALL n columns -- the symmetric definition)
  E_v4(S)   = same but with k,l <= n-2 (the v4 paper's asymmetric definition)
  E_low(S)  = Cov(X,Z)^2 + Cov(Y,Z)^2 + Cov(D_main,Z)^2 + Cov(D_anti,Z)^2

Output: results.json and SUMMARY.md in the same directory.
"""
import itertools
import json
import math
import os
import sys
import time
from fractions import Fraction

import warnings

import numpy as np

# numpy 2.0 + Apple Accelerate emits spurious "divide by zero / overflow in matmul"
# RuntimeWarnings for perfectly finite float64 products; the results are checked
# explicitly below, so silence just that message.
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_880 = os.path.join(HERE, "..", "..", "data", "magic_squares_880 (1).npy")

RESULTS = {}
FAILED = []


def record(name, ok, **info):
    RESULTS[name] = {"pass": bool(ok), **info}
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + ("" if ok else f"   {info}"))
    if not ok:
        FAILED.append(name)


# ----------------------------------------------------------------------------
# Basic geometry
# ----------------------------------------------------------------------------
def coords(n):
    """x, y as Fraction arrays (n x n)."""
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    c = Fraction(n - 1, 2)
    x = np.array([[Fraction(int(j[a, b])) - c for b in range(n)] for a in range(n)], dtype=object)
    y = np.array([[c - Fraction(int(i[a, b])) for b in range(n)] for a in range(n)], dtype=object)
    return x, y


def coords_float(n):
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    return j - (n - 1) / 2.0, (n - 1) / 2.0 - i


def zvals(S):
    """Centered heights as Fractions."""
    n = S.shape[0]
    N = n * n
    c = Fraction(N + 1, 2)
    return np.array([[Fraction(int(S[a, b])) - c for b in range(n)] for a in range(n)], dtype=object)


def lines(n):
    """List of the 2n+2 lines, each a list of cells, in the order rows, cols, main, anti."""
    L = []
    for k in range(n):
        L.append([(k, j) for j in range(n)])
    for l in range(n):
        L.append([(i, l) for i in range(n)])
    L.append([(i, i) for i in range(n)])
    L.append([(i, n - 1 - i) for i in range(n)])
    return L


def magic_const(n):
    return n * (n * n + 1) // 2


def line_devs(S):
    """Integer line-sum deviations delta_L = sum_L s - M for all 2n+2 lines."""
    n = S.shape[0]
    M = magic_const(n)
    return [sum(int(S[c]) for c in L) - M for L in lines(n)]


def N2_Efull(S):
    """N^2 * E_full(S) as an exact integer = sum_L delta_L^2."""
    return sum(d * d for d in line_devs(S))


def N2_Ev4(S):
    """N^2 * E_v4(S): drops row n-1 and column n-1."""
    n = S.shape[0]
    d = line_devs(S)
    rows, cols, diag = d[:n], d[n:2 * n], d[2 * n:]
    return sum(v * v for v in rows[:-1]) + sum(v * v for v in cols[:-1]) + sum(v * v for v in diag)


def N2_Elow(S):
    """N^2 * E_low(S) exactly (Fraction)."""
    n = S.shape[0]
    x, y = coords(n)
    z = zvals(S)
    cx = sum(x[c] * z[c] for c in itertools.product(range(n), range(n)))
    cy = sum(y[c] * z[c] for c in itertools.product(range(n), range(n)))
    d = line_devs(S)
    dm, da = d[-2], d[-1]
    return cx * cx + cy * cy + Fraction(dm * dm) + Fraction(da * da)


def is_magic(S):
    return all(d == 0 for d in line_devs(S))


def is_semimagic(S):
    n = S.shape[0]
    return all(d == 0 for d in line_devs(S)[:2 * n])


# ----------------------------------------------------------------------------
# D4 action
# ----------------------------------------------------------------------------
def d4_images(S):
    out = []
    for k in range(4):
        R = np.rot90(S, k)
        out.append(R)
        out.append(np.fliplr(R))
    return out


# ----------------------------------------------------------------------------
# Magic square generators
# ----------------------------------------------------------------------------
def siamese(n):
    """de la Loubere (Siamese) method, odd n."""
    assert n % 2 == 1
    S = np.zeros((n, n), dtype=np.int64)
    i, j = 0, n // 2
    for v in range(1, n * n + 1):
        S[i, j] = v
        ni, nj = (i - 1) % n, (j + 1) % n
        if S[ni, nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return S


def doubly_even(n):
    """Standard construction for n divisible by 4."""
    assert n % 4 == 0
    S = np.arange(1, n * n + 1, dtype=np.int64).reshape(n, n)
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    mask = ((i % 4 in (0, 3)) if False else None)
    keep = ((i % 4 == 0) | (i % 4 == 3)) == ((j % 4 == 0) | (j % 4 == 3))
    S[keep] = n * n + 1 - S[keep]
    return S


MAGIC6 = np.array([[35, 1, 6, 26, 19, 24],
                   [3, 32, 7, 21, 23, 25],
                   [31, 9, 2, 22, 27, 20],
                   [8, 28, 33, 17, 10, 15],
                   [30, 5, 34, 12, 14, 16],
                   [4, 36, 29, 13, 18, 11]], dtype=np.int64)


def magic_square(n):
    if n % 2 == 1:
        return siamese(n)
    if n % 4 == 0:
        return doubly_even(n)
    if n == 6:
        return MAGIC6
    raise ValueError(n)


def column_magic_square(n):
    """s_ij = 1 + i + n*((i+j) mod n): a permutation of 1..N with all column sums = M."""
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    return (1 + i + n * ((i + j) % n)).astype(np.int64)


# ----------------------------------------------------------------------------
# 1. Variance lemma, Cov = inner product
# ----------------------------------------------------------------------------
def check_variances():
    ok = True
    for n in range(3, 10):
        N = n * n
        x, y = coords(n)
        rng = np.random.default_rng(n)
        S = rng.permutation(N).reshape(n, n) + 1
        z = zvals(S)
        cells = list(itertools.product(range(n), range(n)))
        mx = sum(x[c] for c in cells) / N
        my = sum(y[c] for c in cells) / N
        mz = sum(z[c] for c in cells) / N
        vx = sum(x[c] ** 2 for c in cells) / N
        vy = sum(y[c] ** 2 for c in cells) / N
        vz = sum(z[c] ** 2 for c in cells) / N
        cxy = sum(x[c] * y[c] for c in cells) / N
        ok &= (mx == 0 and my == 0 and mz == 0)
        ok &= (vx == Fraction(n * n - 1, 12) and vy == Fraction(n * n - 1, 12))
        ok &= (vz == Fraction(N * N - 1, 12))
        ok &= (cxy == 0)
    record("variance_lemma  mean 0, Var X=Var Y=(n^2-1)/12, Var Z=(N^2-1)/12, Cov(X,Y)=0, n=3..9", ok)


# ----------------------------------------------------------------------------
# 2. dim W and the orthogonal decomposition
# ----------------------------------------------------------------------------
def check_dimW():
    dims = {}
    ok = True
    for n in range(3, 9):
        N = n * n
        vecs = []
        cells = list(itertools.product(range(n), range(n)))
        for L in lines(n):
            v = np.zeros(N)
            for (i, j) in L:
                v[i * n + j] = 1.0
            vecs.append(v - v.mean())        # centered indicator
        A = np.array(vecs)                    # (2n+2) x N
        r = np.linalg.matrix_rank(A)
        dims[n] = int(r)
        ok &= (r == 2 * n)
        # Gram matrix structure: rows/cols/diags mutually orthogonal blocks
        G = A @ A.T
        rows, cols = slice(0, n), slice(n, 2 * n)
        ok &= np.allclose(G[rows, cols], 0)
        ok &= np.allclose(G[rows, 2 * n:], 0) and np.allclose(G[cols, 2 * n:], 0)
        ok &= np.allclose(G[rows, rows], n * np.eye(n) - 1)
        eps = -1 if n % 2 == 0 else 0
        ok &= np.allclose(G[2 * n:, 2 * n:], np.array([[n - 1, eps], [eps, n - 1]]))
        # also: rows+cols only has rank 2n-2 (centered)
        ok &= (np.linalg.matrix_rank(A[:2 * n]) == 2 * n - 2)
    record("dim_W = 2n for n=3..8 (rank of centered line indicators); Gram block structure", ok, dims=dims)


def check_projection_lemma():
    """E_full = (1/n)(|P_R z|^2+|P_C z|^2) + (dm^2+da^2)/N^2, and the comparison bounds."""
    ok = True
    worst = {}
    for n in range(3, 9):
        N = n * n
        rng = np.random.default_rng(100 + n)
        cells = list(itertools.product(range(n), range(n)))
        A = []
        for L in lines(n):
            v = np.zeros(N)
            for (i, j) in L:
                v[i * n + j] = 1.0
            A.append(v - v.mean())
        A = np.array(A)
        # orthogonal projector onto W (Euclidean), via SVD
        U, s, Vt = np.linalg.svd(A, full_matrices=False)
        Vt = Vt[s > 1e-9]
        P = Vt.T @ Vt
        PR = np.linalg.pinv(A[:n]) @ A[:n]
        PC = np.linalg.pinv(A[n:2 * n]) @ A[n:2 * n]
        lo_c, hi_c = (n - 2) / n**2, 1.0 / n
        if n % 2 == 1:
            lo_c = (n - 1) / n**2
        ratios = []
        for trial in range(20):
            S = rng.permutation(N).reshape(n, n) + 1
            z = (S - (N + 1) / 2.0).reshape(-1)
            E = N2_Efull(S) / N**2
            d = line_devs(S)
            dm, da = d[-2], d[-1]
            normPRz = (PR @ z) @ (PR @ z) / N
            normPCz = (PC @ z) @ (PC @ z) / N
            E_formula = (normPRz + normPCz) / n + (dm * dm + da * da) / N**2
            ok &= abs(E - E_formula) < 1e-9
            normPWz = (P @ z) @ (P @ z) / N
            if normPWz > 1e-12:
                ratios.append(E / normPWz)
                ok &= (lo_c - 1e-9 <= E / normPWz <= hi_c + 1e-9)
            # Cov(R_k,Z)^2 sum = |rho|^2/N^2 = (1/n) |P_R z|^2
            rho = np.array(d[:n])
            ok &= abs((rho @ rho) / N**2 - normPRz / n) < 1e-9
        worst[n] = (min(ratios), max(ratios), lo_c, hi_c)
    record("projection_lemma  E_full = (1/n)(|P_R z|^2+|P_C z|^2) + (dm^2+da^2)/N^2;"
           " (n-2)/n^2 |P_W z|^2 <= E_full <= (1/n)|P_W z|^2", ok,
           observed_ratio_range={str(k): v for k, v in worst.items()})


# ----------------------------------------------------------------------------
# 3. D4 invariance
# ----------------------------------------------------------------------------
def check_d4():
    ok_sym = True
    noninv_examples = []
    for n in range(3, 8):
        rng = np.random.default_rng(7 + n)
        N = n * n
        for t in range(30):
            S = rng.permutation(N).reshape(n, n) + 1
            Ef = N2_Efull(S)
            El = N2_Elow(S)
            for g in d4_images(S):
                ok_sym &= (N2_Efull(g) == Ef)
                ok_sym &= (N2_Elow(g) == El)
    # non-invariance of v4 energy: on 880 squares with one swap
    sq = np.load(DATA_880)
    cnt_noninv = 0
    cnt_total = 0
    for S in sq[:50]:
        for (a, b) in [((0, 0), (0, 1)), ((1, 2), (3, 3))]:
            T = S.copy()
            T[a], T[b] = S[b], S[a]
            vals = sorted(set(N2_Ev4(g) for g in d4_images(T)))
            cnt_total += 1
            if len(vals) > 1:
                cnt_noninv += 1
                if len(noninv_examples) < 2:
                    noninv_examples.append({"square": T.tolist(), "N2_Ev4_over_D4_orbit": vals,
                                            "N2_Efull": N2_Efull(T)})
    record("D4_invariance  symmetric E_full and E_low invariant under all 8 symmetries (n=3..7, random)",
           ok_sym)
    record("D4_noninvariance_v4  the v4 energy (dropping row/col n-1) is NOT D4-invariant",
           cnt_noninv > 0, fraction_of_tested_swapped_squares_noninvariant=f"{cnt_noninv}/{cnt_total}",
           examples=noninv_examples)


# ----------------------------------------------------------------------------
# 4. Lemma: E_full = 0 iff magic (checked on 880 + n=3 exhaustive + random)
# ----------------------------------------------------------------------------
def all_perms_n3():
    P = np.array(list(itertools.permutations(range(1, 10))), dtype=np.int64)  # 362880 x 9
    return P.reshape(-1, 3, 3)


def check_zero_iff_magic(perms3, sq880):
    ok = True
    # n=3 exhaustive, vectorised
    A = perms3
    M = 15
    rows = A.sum(2) - M
    cols = A.sum(1) - M
    dm = A[:, 0, 0] + A[:, 1, 1] + A[:, 2, 2] - M
    da = A[:, 0, 2] + A[:, 1, 1] + A[:, 2, 0] - M
    N2E = (rows**2).sum(1) + (cols**2).sum(1) + dm**2 + da**2
    magic = (rows == 0).all(1) & (cols == 0).all(1) & (dm == 0) & (da == 0)
    ok &= ((N2E == 0) == magic).all()
    ok &= magic.sum() == 8
    for S in sq880:
        ok &= is_magic(S) and N2_Efull(S) == 0
    record("Efull_zero_iff_magic  exhaustive n=3 (8 magic) and all 880 n=4 squares", ok,
           n3_magic_count=int(magic.sum()))
    return rows, cols, dm, da, magic


# ----------------------------------------------------------------------------
# 5. Moment hierarchy
# ----------------------------------------------------------------------------
def cross_moments(S, kmax):
    """Exact <x^m, z>, <y^m, z> (times N) for m = 0..kmax as Fractions."""
    n = S.shape[0]
    x, y = coords(n)
    z = zvals(S)
    cells = list(itertools.product(range(n), range(n)))
    mx = [sum(x[c] ** m * z[c] for c in cells) for m in range(kmax + 1)]
    my = [sum(y[c] ** m * z[c] for c in cells) for m in range(kmax + 1)]
    return mx, my


def check_hierarchy(sq880, perms3, magic3):
    ok = True
    # (a) semi-magic => all cross moments vanish.  Semi-magic test set:
    tests = []
    for n in [3, 4, 5, 6, 7, 8, 9]:
        Smag = magic_square(n)
        assert is_magic(Smag), n
        tests.append(Smag)
        # row/column permutations of a magic square are semi-magic (generally not magic)
        rng = np.random.default_rng(n)
        for t in range(3):
            T = Smag[rng.permutation(n)][:, rng.permutation(n)]
            assert is_semimagic(T)
            tests.append(T)
    for S in sq880[::40]:
        tests.append(S)
    for S in tests:
        mx, my = cross_moments(S, 6)
        ok &= all(v == 0 for v in mx[1:]) and all(v == 0 for v in my[1:])
    record("hierarchy_a  semi-magic => <x^m,z>=<y^m,z>=0 for m<=6 (magic + row/col-permuted, n=3..9; 880 sample)", ok,
           n_tested=len(tests))

    # (b) k >= n-1 forces equal line sums: real-valued statement via Vandermonde rank
    okb = True
    for n in range(3, 10):
        xs = np.arange(n) - (n - 1) / 2.0
        for k in range(0, n + 1):
            V = np.array([xs**m for m in range(k + 1)])
            r = np.linalg.matrix_rank(V)
            okb &= (r == min(k + 1, n))
            # polynomials of degree <= k span R^n iff k >= n-1
            okb &= ((r == n) == (k >= n - 1))
    record("hierarchy_b  degree-<=k polynomials on n nodes span R^n iff k>=n-1 (Vandermonde rank, n=3..9)", okb)

    # (c) real-valued counterexample for k <= n-2: f_ij = (1/n) (-1)^j C(k+1,j)
    okc = True
    for n in range(3, 10):
        xs = [Fraction(j) - Fraction(n - 1, 2) for j in range(n)]
        ys = [Fraction(n - 1, 2) - Fraction(i) for i in range(n)]
        for k in range(0, n - 1):
            v = [Fraction((-1) ** j * math.comb(k + 1, j)) if j <= k + 1 else Fraction(0) for j in range(n)]
            f = [[v[j] / n for j in range(n)] for i in range(n)]
            okc &= sum(sum(r) for r in f) == 0
            gamma = [sum(f[i][j] for i in range(n)) for j in range(n)]
            rho = [sum(f[i][j] for j in range(n)) for i in range(n)]
            okc &= any(g != 0 for g in gamma) and all(r == 0 for r in rho)
            for m in range(1, k + 1):
                okc &= sum(xs[j] ** m * gamma[j] for j in range(n)) == 0
            # degree k+1 condition FAILS (so the construction is sharp)
            okc &= sum(xs[j] ** (k + 1) * gamma[j] for j in range(n)) != 0
    record("hierarchy_c  finite-difference height function satisfies degree-k but not degree-(k+1) conditions, k<=n-2, n=3..9", okc)

    # n = 3 exhaustive: degree-1 in x,y -> 760; degree-1 + diagonals -> 8; degree-2 -> semi-magic
    A = perms3
    xs = np.array([-1.0, 0.0, 1.0])
    ys = np.array([1.0, 0.0, -1.0])
    rows = (A.sum(2) - 15).astype(float)
    cols = (A.sum(1) - 15).astype(float)
    dm = A[:, 0, 0] + A[:, 1, 1] + A[:, 2, 2] - 15
    da = A[:, 0, 2] + A[:, 1, 1] + A[:, 2, 0] - 15
    dot = lambda A, w: (A * w).sum(1)      # elementwise instead of matmul (avoids Accelerate warnings)
    m1 = (dot(cols, xs) == 0) & (dot(rows, ys) == 0)
    m2 = m1 & (dot(cols, xs**2) == 0) & (dot(rows, ys**2) == 0)
    semi = (rows == 0).all(1) & (cols == 0).all(1)
    low0 = m1 & (dm == 0) & (da == 0)
    n760 = int(m1.sum())
    ok3 = (n760 == 760) and (low0.sum() == 8) and (low0 == magic3).all() and (m2 == semi).all()
    record("hierarchy_n3_exhaustive  760 arrangements with degree-1 balance; +diagonals -> exactly the 8 magic; degree-2 <=> semi-magic",
           ok3, n_degree1=n760, n_degree1_plus_diag=int(low0.sum()), n_semimagic=int(semi.sum()),
           n_degree2=int(m2.sum()))
    ex3 = np.array([[1, 3, 9], [8, 6, 5], [7, 4, 2]])
    mx, my = cross_moments(ex3, 2)
    ok3b = mx[1] == 0 and my[1] == 0 and not is_semimagic(ex3)
    record("hierarchy_n3_example  [[1,3,9],[8,6,5],[7,4,2]] satisfies degree-1 conditions, not semi-magic", ok3b,
           column_devs=line_devs(ex3)[3:6], row_devs=line_devs(ex3)[:3])

    # 4x4 counterexample from the paper: all four low-mode covariances vanish, not magic
    C4 = np.array([[9, 4, 12, 3], [16, 1, 14, 7], [10, 15, 11, 8], [2, 5, 6, 13]])
    mx, my = cross_moments(C4, 3)
    d = line_devs(C4)
    ok4 = (N2_Elow(C4) == 0) and (not is_semimagic(C4)) and mx[1] == 0 and my[1] == 0 and mx[2] == 0 and my[2] != 0
    record("counterexample_4x4  E_low=0, degree-1 in x and y, degree-2 in x only (y fails), not semi-magic", ok4,
           row_devs=d[:4], col_devs=d[4:8], diag_devs=d[8:],
           N_times_moments_x=[str(v) for v in mx], N_times_moments_y=[str(v) for v in my])

    # binomial bound: for n >= 14 the degree-(n-2) conditions force equal line sums for permutations
    okb2 = True
    first = None
    for n in range(3, 61):
        central = math.comb(n - 1, (n - 1) // 2)
        maxdev = n * n * (n - 1) // 2
        if central > maxdev and first is None:
            first = n
        if n >= 14:
            okb2 &= central > maxdev
        else:
            okb2 &= central <= maxdev
    record("hierarchy_binomial_bound  C(n-1,floor((n-1)/2)) > n^2(n-1)/2 exactly for n>=14 (checked n<=60)",
           okb2 and first == 14, first_n=first)


def anneal_to_targets(n, row_target, col_target, seed=0, max_iter=400000):
    """Find a permutation of 1..n^2 with given row/column sums by swap-annealing. Returns S or None."""
    rng = np.random.default_rng(seed)
    N = n * n
    S = rng.permutation(N).reshape(n, n) + 1
    rt = np.asarray(row_target); ct = np.asarray(col_target)

    def cost(S):
        return int(((S.sum(1) - rt) ** 2).sum() + ((S.sum(0) - ct) ** 2).sum())

    c = cost(S)
    T = 50.0
    for it in range(max_iter):
        if c == 0:
            return S
        a = rng.integers(N); b = rng.integers(N)
        if a == b:
            continue
        ia, ja = divmod(int(a), n); ib, jb = divmod(int(b), n)
        d = int(S[ib, jb] - S[ia, ja])
        # incremental cost change
        dc = 0
        if ia != ib:
            ra, rb = int(S[ia].sum() - rt[ia]), int(S[ib].sum() - rt[ib])
            dc += (ra + d) ** 2 - ra ** 2 + (rb - d) ** 2 - rb ** 2
        if ja != jb:
            ca, cb = int(S[:, ja].sum() - ct[ja]), int(S[:, jb].sum() - ct[jb])
            dc += (ca + d) ** 2 - ca ** 2 + (cb - d) ** 2 - cb ** 2
        if dc <= 0 or rng.random() < math.exp(-dc / T):
            S[ia, ja], S[ib, jb] = S[ib, jb], S[ia, ja]
            c += dc
        T = max(0.5, T * 0.99997)
    return None


def check_permutation_threshold():
    """Search for permutation arrangements satisfying the degree-(n-2) conditions in x AND y
    that are not semi-magic (column deviations = v, row deviations = 0 or v), n = 4..13."""
    found = {}
    for n in range(4, 14):
        M = magic_const(n)
        v = np.array([(-1) ** j * math.comb(n - 1, j) for j in range(n)])
        S = None
        t0 = time.time()
        for seed in range(6):
            S = anneal_to_targets(n, [M] * n, M + v, seed=seed, max_iter=300000 if n <= 8 else 600000)
            if S is not None:
                break
        if S is not None:
            mx, my = cross_moments(S, n - 2)
            assert all(val == 0 for val in mx[1:n - 1]) and all(val == 0 for val in my[1:n - 1])
            assert not is_semimagic(S)
            found[n] = {"found": True, "square": S.tolist(), "col_devs": (S.sum(0) - M).tolist(),
                        "seconds": round(time.time() - t0, 1)}
        else:
            found[n] = {"found": False, "seconds": round(time.time() - t0, 1)}
        print(f"   n={n}: degree-(n-2) non-semi-magic permutation {'FOUND' if S is not None else 'not found'} "
              f"({found[n]['seconds']} s)")
    # n=4 must be found (it is the example used in the text)
    record("permutation_threshold_search  degree-(n-2) conditions in x and y with unequal column sums (search, n=4..13)",
           found[4]["found"], **{str(k): v for k, v in found.items()})
    return found


# ----------------------------------------------------------------------------
# 6. Loly's moment of inertia
# ----------------------------------------------------------------------------
def loly_I(S):
    n = S.shape[0]
    x, y = coords(n)
    return sum(Fraction(int(S[c])) * (x[c] ** 2 + y[c] ** 2) for c in itertools.product(range(n), range(n)))


def check_loly(sq880):
    ok = True
    vals = {}
    for n in range(3, 10):
        N = n * n
        S = magic_square(n)
        I = loly_I(S)
        target = Fraction(n * n * (n**4 - 1), 12)
        target2 = Fraction(N * (N + 1) * (n * n - 1), 12)
        ok &= (I == target == target2)
        vals[n] = int(I)
        # semi-magic (row/col permuted) also gives the constant
        rng = np.random.default_rng(n)
        T = S[rng.permutation(n)][:, rng.permutation(n)]
        ok &= (loly_I(T) == target)
        # general identity I = N Cov(Z, X^2+Y^2) + ((N+1)/2) sum(x^2+y^2) on random arrangements
        x, y = coords(n)
        cells = list(itertools.product(range(n), range(n)))
        sxy = sum(x[c] ** 2 + y[c] ** 2 for c in cells)
        ok &= (sxy == Fraction(n * n * (n * n - 1), 6))
        for t in range(3):
            R = rng.permutation(N).reshape(n, n) + 1
            z = zvals(R)
            NcovZQ = sum((x[c] ** 2 + y[c] ** 2) * z[c] for c in cells)   # Q centered or not: z centered
            ok &= (loly_I(R) == NcovZQ + Fraction(N + 1, 2) * sxy)
    for S in sq880:
        ok &= (loly_I(S) == Fraction(16 * 255, 12))
    oeis = {3: 60, 4: 340, 5: 1300, 6: 3885, 7: 9800, 8: 21840, 9: 44280}
    ok &= all(vals[n] == oeis[n] for n in oeis)
    record("loly_constant  I = n^2(n^4-1)/12 for magic (n=3..9) and semi-magic squares and all 880; identity I = N Cov(Z,X^2+Y^2)+((N+1)/2) sum(x^2+y^2)",
           ok, values=vals, oeis_A126275=oeis)


# ----------------------------------------------------------------------------
# 7. Single-swap formula
# ----------------------------------------------------------------------------
def m_count(n, a, b):
    """Number of lines containing exactly one of a, b."""
    return sum(1 for L in lines(n) if ((a in L) != (b in L)))


def potential(S):
    """u(c) = sum of delta_L over lines L containing c."""
    n = S.shape[0]
    d = line_devs(S)
    u = {}
    for c in itertools.product(range(n), range(n)):
        u[c] = sum(d[idx] for idx, L in enumerate(lines(n)) if c in L)
    return u


def check_swap(sq880):
    ok_magic = True
    gap_multiset = {}
    n_swaps = 0
    all_sq = [S for S in sq880] + [np.rot90(siamese(3), k) for k in range(4)] + \
             [np.fliplr(np.rot90(siamese(3), k)) for k in range(4)]
    for S in all_sq:
        n = S.shape[0]
        N = n * n
        cells = list(itertools.product(range(n), range(n)))
        gaps = []
        for a, b in itertools.combinations(cells, 2):
            T = S.copy()
            T[a], T[b] = S[b], S[a]
            d = int(S[a]) - int(S[b])
            m = m_count(n, a, b)
            lhs = N2_Efull(T) - N2_Efull(S)
            ok_magic &= (lhs == d * d * m)
            gaps.append(lhs)
            n_swaps += 1
            # E_low swap formula from a magic square
            x, y = coords(n)
            Dm = lambda c: 1 if c[0] == c[1] else 0
            Da = lambda c: 1 if c[0] + c[1] == n - 1 else 0
            pred = Fraction(d * d) * ((x[a] - x[b]) ** 2 + (y[a] - y[b]) ** 2 + (Dm(a) - Dm(b)) ** 2 + (Da(a) - Da(b)) ** 2)
            ok_magic &= (N2_Elow(T) - N2_Elow(S) == pred)
        g = min(gaps)
        key = f"n={n}"
        gap_multiset.setdefault(key, {})
        gap_multiset[key][str(g)] = gap_multiset[key].get(str(g), 0) + 1
    record("swap_formula_magic  N^2 dE_full = d^2 m(a,b) and E_low analogue, ALL single swaps of the 880 (n=4) and 8 (n=3) squares, exact",
           ok_magic, n_swaps_checked=n_swaps, min_gap_multiset_N2_units=gap_multiset)
    # general formula from arbitrary S: N^2 dE = d^2 m + 2 d (u(a)-u(b)), d = s_b - s_a
    okg = True
    for n in range(3, 8):
        rng = np.random.default_rng(300 + n)
        N = n * n
        cells = list(itertools.product(range(n), range(n)))
        for t in range(5):
            S = rng.permutation(N).reshape(n, n) + 1
            u = potential(S)
            E0 = N2_Efull(S)
            for a, b in rng.choice(len(cells), size=(30, 2)):
                a, b = cells[a], cells[b]
                if a == b:
                    continue
                T = S.copy()
                T[a], T[b] = S[b], S[a]
                d = int(S[b]) - int(S[a])
                okg &= (N2_Efull(T) - E0 == d * d * m_count(n, a, b) + 2 * d * (u[a] - u[b]))
    record("swap_formula_general  N^2 dE_full = d^2 m(a,b) + 2d(u(a)-u(b)) from arbitrary S (random, n=3..7)", okg)
    # m(a,b) characterisation: m>=2; m=2 iff same row or column and both cells off both diagonals; m<=6
    okm = True
    for n in range(3, 9):
        cells = list(itertools.product(range(n), range(n)))
        for a, b in itertools.combinations(cells, 2):
            m = m_count(n, a, b)
            okm &= 2 <= m <= 6
            offdiag = lambda c: c[0] != c[1] and c[0] + c[1] != n - 1
            pred2 = (a[0] == b[0] or a[1] == b[1]) and offdiag(a) and offdiag(b)
            okm &= ((m == 2) == pred2)
        # existence of an m=2 pair for every n>=3
        okm &= any(m_count(n, a, b) == 2 for a, b in itertools.combinations(cells, 2))
    record("m_characterisation  2<=m<=6; m=2 iff same row/column with both cells off both diagonals; m=2 pairs exist, n=3..8", okm)
    # minimum gap bounds 2 <= N^2 Delta_min <= 6 on 880 and n=3
    okmin = True
    for key, ms in gap_multiset.items():
        for g in ms:
            okmin &= 2 <= int(g) <= 6
    record("min_gap_bounds  2/N^2 <= Delta_min <= 6/N^2 on all 888 squares", okmin)


# ----------------------------------------------------------------------------
# 8. Inertia tensor
# ----------------------------------------------------------------------------
def check_inertia(sq880):
    ok = True
    for n in range(3, 9):
        N = n * n
        rng = np.random.default_rng(500 + n)
        x, y = coords(n)
        cells = list(itertools.product(range(n), range(n)))
        for t in range(4):
            S = rng.permutation(N).reshape(n, n) + 1
            z = zvals(S)
            Ixx = sum(y[c] ** 2 + z[c] ** 2 for c in cells)
            Iyy = sum(x[c] ** 2 + z[c] ** 2 for c in cells)
            Izz = sum(x[c] ** 2 + y[c] ** 2 for c in cells)
            Ixy = -sum(x[c] * y[c] for c in cells)
            Ixz = -sum(x[c] * z[c] for c in cells)
            Iyz = -sum(y[c] * z[c] for c in cells)
            ok &= Ixx == Iyy == Fraction(n * n * (n * n - 1) * (n * n + 2), 12)
            ok &= Izz == Fraction(n * n * (n * n - 1), 6)
            ok &= Ixy == 0
            covxz = sum(x[c] * z[c] for c in cells) / N
            covyz = sum(y[c] * z[c] for c in cells) / N
            ok &= Ixz == -N * covxz and Iyz == -N * covyz
    for S in sq880[::20]:
        n = 4; N = 16
        x, y = coords(n); z = zvals(S)
        cells = list(itertools.product(range(n), range(n)))
        ok &= sum(x[c] * z[c] for c in cells) == 0 and sum(y[c] * z[c] for c in cells) == 0
    record("inertia_tensor  I_xx=I_yy=n^2(n^2-1)(n^2+2)/12, I_zz=n^2(n^2-1)/6 for every arrangement; I_xy=0; I_xz=-N Cov(X,Z), I_yz=-N Cov(Y,Z); diagonal for magic", ok)


# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    sq880 = np.load(DATA_880)
    assert sq880.shape == (880, 4, 4)
    print("loading all 9! arrangements for n=3 ...")
    perms3 = all_perms_n3()
    check_variances()
    check_dimW()
    check_projection_lemma()
    check_d4()
    rows, cols, dm, da, magic3 = check_zero_iff_magic(perms3, sq880)
    check_hierarchy(sq880, perms3, magic3)
    check_permutation_threshold()
    check_loly(sq880)
    check_swap(sq880)
    check_inertia(sq880)
    elapsed = time.time() - t0
    RESULTS["_meta"] = {"elapsed_seconds": round(elapsed, 1), "python": sys.version.split()[0],
                        "numpy": np.__version__, "all_pass": not FAILED, "failed": FAILED}
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(RESULTS, f, indent=1, default=str)
    with open(os.path.join(HERE, "SUMMARY.md"), "w") as f:
        f.write("# Verification summary for sections/drafts/theory.tex\n\n")
        f.write(f"Generated by `verify_theory.py` in {elapsed:.0f} s. "
                f"Overall: **{'ALL PASS' if not FAILED else 'FAILURES: ' + ', '.join(FAILED)}**\n\n")
        f.write("| Claim | Status | Notes |\n|---|---|---|\n")
        for k, v in RESULTS.items():
            if k.startswith("_"):
                continue
            notes = {kk: vv for kk, vv in v.items() if kk != "pass" and kk not in ("examples", "square")}
            notes_s = json.dumps(notes, default=str)
            if len(notes_s) > 300:
                notes_s = notes_s[:300] + " ..."
            f.write(f"| `{k}` | {'PASS' if v['pass'] else 'FAIL'} | {notes_s} |\n")
    print(f"\nDone in {elapsed:.0f}s.  {'ALL PASS' if not FAILED else 'FAILED: ' + str(FAILED)}")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
