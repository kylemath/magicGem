#!/usr/bin/env python3
"""Second, independent implementation of the upper bounds k*(n) <= k for 14 <= n <= 40.

  python3 kstar_enum_independent.py [n ...]          (default: 14..40; about a minute in total)
  python3 kstar_enum_independent.py --certificate     also writes kstar_certificates.json

Written separately from kstar_verify.py (which uses SymPy's LLL and its own Fincke--Pohst routine): exact LLL
reduction in rational arithmetic (delta = 99/100), exact Gram--Schmidt data, and a Schnorr--Euchner style
enumeration of all vectors of Lambda_{n,k} = {gamma in Z^n : (t-1)^{k+1} | P_gamma} with
||gamma||_2^2 <= R^2 = n^5(n^2-1)/12 (the l2 bound of the majorisation lemma).  Each vector found is tested
against the inequalities (10): for every p, the p largest entries sum to at most pn(N-pn)/2 and the p smallest
to at least -pn(N-pn)/2.  At k = k*(n) no nonzero vector satisfies (10), which proves k*(n) <= k.

The certificate records, for each n: k, the reduced basis, the exact squared Gram--Schmidt norms, R^2, and every
nonzero vector of the ball with a violated instance (p, sign, J) of (10) with p minimal.  It is checked by
kstar_check_certificates.py.
"""
import json, math, os, sys
from fractions import Fraction as F
from math import comb, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
KSTAR = {14: 12, 15: 13, 16: 14, 17: 15, 18: 15, 19: 16, 20: 16, 21: 17, 22: 17, 23: 18, 24: 18, 25: 19, 26: 19,
         27: 20, 28: 21, 29: 21, 30: 22, 31: 22, 32: 23, 33: 23, 34: 23, 35: 24, 36: 24, 37: 25, 38: 25, 39: 26,
         40: 26}


def basis(n, k):
    """The basis t^i (t-1)^{k+1}, 0 <= i < n-k-1, as coefficient vectors."""
    base = [(-1) ** (k + 1 - j) * comb(k + 1, j) for j in range(k + 2)]
    return [[0] * i + base + [0] * (n - k - 2 - i) for i in range(n - k - 1)]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def gram_schmidt(B):
    Bs, nrm = [], []
    mu = [[F(0)] * len(B) for _ in B]
    for i, b in enumerate(B):
        v = [F(x) for x in b]
        for j in range(i):
            mu[i][j] = F(dot(b, Bs[j])) / nrm[j]
            v = [a - mu[i][j] * c for a, c in zip(v, Bs[j])]
        Bs.append(v); nrm.append(dot(v, v))
    return mu, nrm


def lll(B, delta=F(99, 100)):
    B = [list(b) for b in B]; k = 1
    mu, nrm = gram_schmidt(B)
    while k < len(B):
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]; mu, nrm = gram_schmidt(B)
        if nrm[k] >= (delta - mu[k][k - 1] ** 2) * nrm[k - 1]:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]; mu, nrm = gram_schmidt(B); k = max(k - 1, 1)
    return B, mu, nrm


def enumerate_ball(B, mu, nrm, R2):
    """All nonzero integer combinations x with ||sum x_i b_i||^2 <= R2 (exact)."""
    d = len(B); out = []; x = [0] * d

    def rec(i, partial):
        c = -sum(x[j] * mu[j][i] for j in range(i + 1, d))
        rem = R2 - partial
        if rem < 0:
            return
        r = isqrt(int(rem / nrm[i]) + 1) + 1
        for xi in range(math.floor(c - r), math.ceil(c + r) + 1):
            t = (xi - c) ** 2 * nrm[i]
            if t <= rem:
                x[i] = xi
                if i == 0:
                    out.append(list(x))
                else:
                    rec(i - 1, partial + t)
        x[i] = 0
    rec(d - 1, F(0))
    return [v for v in out if any(v)]


def violation(g, n):
    """Minimal p (and sign, column set J) with |sum_{j in J} g_j| > pn(N-pn)/2, or None if g satisfies (10)."""
    N = n * n
    up = sorted(range(n), key=lambda j: -g[j]); dn = sorted(range(n), key=lambda j: g[j])
    for p in range(1, n + 1):
        bound2 = p * n * (N - p * n)
        if 2 * sum(g[j] for j in up[:p]) > bound2:
            return p, '+', sorted(up[:p])
        if -2 * sum(g[j] for j in dn[:p]) > bound2:
            return p, '-', sorted(dn[:p])
    return None


def run(n, k):
    R2 = F(n ** 5 * (n * n - 1), 12)
    B, mu, nrm = lll(basis(n, k))
    vecs = []
    if min(nrm) <= R2:
        for x in enumerate_ball(B, mu, nrm, R2):
            vecs.append([sum(c * b[j] for c, b in zip(x, B)) for j in range(n)])
    return B, nrm, R2, vecs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ns = [int(a) for a in args] or sorted(KSTAR)
    cert = {}
    for n in ns:
        k = KSTAR[n]
        B, nrm, R2, vecs = run(n, k)
        viol = [violation(g, n) for g in vecs]
        assert all(v is not None for v in viol), 'a vector satisfies (10): k*(%d) <= %d is not proved' % (n, k)
        print('n=%d k=%d rank=%d min|b*|^2/R^2=%.3f vectors_in_ball=%d feasible=0 p_needed=%s'
              % (n, k, len(B), float(min(nrm) / R2), len(vecs), sorted({v[0] for v in viol})), flush=True)
        cert[str(n)] = {'k': k, 'R2': str(R2), 'basis': B, 'gs_norms_sq': [str(t) for t in nrm],
                        'vectors': [{'gamma': g, 'p': v[0], 'sign': v[1], 'J': v[2]} for g, v in zip(vecs, viol)]}
    if '--certificate' in sys.argv:
        with open(os.path.join(HERE, 'kstar_certificates.json'), 'w') as f:
            json.dump(cert, f, indent=1)
        print('wrote kstar_certificates.json')


if __name__ == '__main__':
    main()
