#!/usr/bin/env python3
"""Exact verification of the statements about the permutation threshold k*(n) (Theorem on k*(n)).

  python3 kstar_verify.py [NMAX] [--resume LOG]   (default NMAX = 100; writes kstar_verify.json)
  --resume LOG reuses the upper bounds U(n) printed in a previous log of this script.

1. Witnesses (lower bounds).  Every arrangement in kstar_witnesses.json (14 <= n <= 40) and in
   data_witnesses_variances.json (5 <= n <= 13) is checked to be a permutation of 1..n^2 with all row sums
   M(n) and column deviations gamma != 0.  The order K of vanishing of P_gamma(t) = sum_j gamma_j t^j at t = 1 is
   computed from the binomial moments sum_j C(j,r) gamma_j; the arrangement satisfies the degree-(K-1)
   conditions and is not semi-magic, so k*(n) >= K.
2. Upper bounds.  Lambda_{n,k} = {gamma in Z^n : (t-1)^{k+1} | P_gamma}.  If Lambda_{n,k} contains no nonzero
   vector satisfying the column-feasibility inequalities (F1) |gamma_j| <= n^2(n-1)/2 and (F2) "the p largest
   (smallest) entries sum to at most (at least -) p n (N - p n)/2", then k*(n) <= k.  Every vector satisfying
   (F2) has ||gamma||^2 <= n^5(n^2-1)/12 (majorisation), so it suffices to enumerate the lattice vectors in
   that ball.  LLL reduction (sympy, exact) followed by Fincke--Pohst enumeration with exact rational
   Gram--Schmidt.  Feasibility is monotone in k, so U(n) := 1 + (largest k with a feasible vector).
3. Level n-3 for 18 <= n <= 400 (rank-2 lattices, explicit box), and the range n >= 27 in which the bound
   floor(sqrt(2(n-1) log(n^4/4))) of Theorem 3.7(a) (Schur's bound, Lemma 3.9) gives k*(n) <= n-3.
"""
import json, os, sys, time
from fractions import Fraction as Fr
from math import comb, isqrt, floor, ceil, log
from sympy import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))


def deviations(S):
    n = len(S); N = n * n; M = n * (N + 1) // 2
    assert sorted(v for r in S for v in r) == list(range(1, N + 1))
    rho = [sum(r) - M for r in S]
    gam = [sum(S[i][j] for i in range(n)) - M for j in range(n)]
    return rho, gam


def vanishing_order(g):
    K = 0
    while K < len(g) and sum(comb(j, K) * g[j] for j in range(len(g))) == 0:
        K += 1
    return K


def feasible(g, n):
    N = n * n
    if 2 * max(abs(v) for v in g) > n * n * (n - 1):
        return False
    s = sorted(g, reverse=True); a = b = 0
    for p in range(1, n + 1):
        a += s[p - 1]; b += s[n - p]
        if 2 * a > p * n * (N - p * n) or -2 * b > p * n * (N - p * n):
            return False
    return True


def basis(n, k):
    K = k + 1
    c = [(-1) ** (K - l) * comb(K, l) for l in range(K + 1)]
    B = []
    for i in range(n - K):
        v = [0] * n
        for l, cl in enumerate(c):
            v[i + l] = cl
        B.append(v)
    return B


def has_feasible(n, k):
    """True iff Lambda_{n,k} has a nonzero vector satisfying F1-F2 (exact)."""
    B = basis(n, k)
    if len(B) > 1:
        B = [list(map(int, r)) for r in Matrix(B).lll().tolist()]
    r = len(B)
    dot = lambda u, v: sum(a * b for a, b in zip(u, v))
    Bs, nn, mu = [], [], [[Fr(0)] * r for _ in range(r)]
    for i in range(r):
        v = [Fr(x) for x in B[i]]
        for j in range(i):
            mu[i][j] = dot(B[i], Bs[j]) / nn[j]
            v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
        Bs.append(v); nn.append(dot(v, v))
    R2 = Fr(n ** 5 * (n * n - 1), 12)
    x = [0] * r

    def rec(i, partial):
        ci = -sum(x[j] * mu[j][i] for j in range(i + 1, r))
        rem = R2 - partial
        rad = isqrt(int(rem / nn[i])) + 1
        for xi in range(floor(ci) - rad, ceil(ci) + rad + 1):
            q = partial + (xi - ci) ** 2 * nn[i]
            if q > R2:
                continue
            x[i] = xi
            if i == 0:
                if any(x):
                    g = [sum(x[t] * B[t][j] for t in range(r)) for j in range(n)]
                    if feasible(g, n):
                        x[i] = 0
                        return True
            elif rec(i - 1, q):
                x[i] = 0
                return True
        x[i] = 0
        return False

    return rec(r - 1, Fr(0))


def upper_bound(n):
    k = n - 2
    while k >= 1 and not has_feasible(n, k):
        k -= 1
    return k + 1


def level_n_minus_3(n):
    """Exhaustive check of the rank-2 lattice Lambda_{n,n-3}: gamma = (t-1)^{n-2}(a+bt); returns F1-feasible (a,b)."""
    H2 = n * n * (n - 1); K = n - 2
    c = lambda j: (-1) ** (K - j) * comb(K, j) if 0 <= j <= K else 0
    j = K // 2
    A = [[c(j), c(j - 1)], [c(j + 1), c(j)]]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    amax = H2 * (abs(A[1][1]) + abs(A[0][1])) // (2 * abs(det)) + 1
    bmax = H2 * (abs(A[1][0]) + abs(A[0][0])) // (2 * abs(det)) + 1
    hits = []
    for a in range(-amax, amax + 1):
        for b in range(-bmax, bmax + 1):
            if (a or b) and all(2 * abs(a * c(i) + b * c(i - 1)) <= H2 for i in range(n)):
                hits.append((a, b))
    return hits


def main():
    args = [a for a in sys.argv[1:]]
    resume = {}
    if '--resume' in args:
        import re
        k = args.index('--resume'); logf = args[k + 1]; del args[k:k + 2]
        resume = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'^(\d+) U\(n\) = (\d+)', open(logf).read(), re.M)}
    NMAX = int(args[0]) if args else 100
    out = {}
    # 1. witnesses
    W = json.load(open(os.path.join(HERE, 'kstar_witnesses.json')))
    O = json.load(open(os.path.join(HERE, 'data_witnesses_variances.json')))['witnesses_k_star_n_minus_1']['squares']
    lower = {}
    for S in list(O.values()) + [w['square'] for w in W.values()]:
        rho, g = deviations(S)
        assert not any(rho) and any(g)
        n = len(S); lower[n] = (vanishing_order(g), max(map(abs, g)))
    out['witness_lower_bounds'] = {n: {'k*>=': lower[n][0], 'max|gamma_j|': lower[n][1], 'F1 bound': n * n * (n - 1) // 2} for n in sorted(lower)}
    print('witnesses verified: n =', sorted(lower))
    # 3. level n-3
    bad = [n for n in range(14, 401) if level_n_minus_3(n)]
    out['level_n_minus_3_not_excluded_14_400'] = bad
    print('level n-3 not excluded by F1 for n in [14,400]:', bad)
    first = None
    for n in range(3, 10 ** 6 + 1):
        ok = (n - 2) ** 2 > 2 * (n - 1) * log(n ** 4 / 4)
        if ok and first is None: first = n
        if not ok: first = None
    out['theorem_a_gives_n_minus_3_from'] = first
    print('Theorem 3.7(a) gives k* <= n-3 for all n in [%d, 10^6]' % first)
    # 2. upper bounds
    U = {}
    for n in range(14, NMAX + 1):
        t = time.time(); U[n] = resume[n] if n in resume else upper_bound(n)
        out['upper_bounds'] = U
        print(n, 'U(n) =', U[n], ('= lower bound (exact)' if n in lower and lower[n][0] == U[n] else ''), '%.1fs' % (time.time() - t), flush=True)
        out['exact'] = {n: U[n] for n in U if n in lower and lower[n][0] == U[n]}
        json.dump(out, open(os.path.join(HERE, 'kstar_verify.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
