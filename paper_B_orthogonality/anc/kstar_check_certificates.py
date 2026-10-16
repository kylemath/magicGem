#!/usr/bin/env python3
"""Check kstar_certificates.json (exact arithmetic, standard library only): python3 kstar_check_certificates.py
The vector list of each n is checked to be complete: empty if min |b_i*|^2 > R^2, else equal to the exact
Fincke--Pohst enumeration of all nonzero lattice vectors (v and -v both listed) with |v|^2 <= R^2."""
import json, os
from fractions import Fraction as F
from math import comb
cert = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kstar_certificates.json')))
def gso(B):  # exact Gram--Schmidt: squared norms |b_i*|^2 and coefficients mu[i][j], j < i
    Bs, out, mu = [], [], []
    for b in B:
        v, mu_i = [F(x) for x in b], []
        for u, nu in zip(Bs, out):
            m = sum(a * c for a, c in zip(b, u)) / nu; v = [a - m * c for a, c in zip(v, u)]; mu_i.append(m)
        Bs.append(v); out.append(sum(a * a for a in v)); mu.append(mu_i)
    return out, mu
gs_norms = lambda B: gso(B)[0]
def ball(B, R2):  # Fincke--Pohst: every nonzero v = sum x_i b_i with |v|^2 = sum_i (x_i - c_i)^2 |b_i*|^2 <= R2, exact
    nrm, mu = gso(B); d, found = len(B), []
    def rec(i, x, rem):  # x = (x_{i+1}, ..., x_{d-1}) fixed; rem = R2 minus their contribution
        if i < 0:
            if any(x): found.append(tuple(sum(xi * b[j] for xi, b in zip(x, B)) for j in range(len(B[0]))))
            return
        c = -sum(mu[j][i] * x[j - i - 1] for j in range(i + 1, d))
        for step in (-1, 1):  # all integers t with (t - c)^2 |b_i*|^2 <= rem: walk outward from floor(c)
            t = c.numerator // c.denominator + (step > 0)
            while (t - c) ** 2 * nrm[i] <= rem: rec(i - 1, [t] + x, rem - (t - c) ** 2 * nrm[i]); t += step
    rec(d - 1, [], F(R2))
    return found
def prod(xs):
    p = F(1)
    for x in xs: p *= x
    return p
in_lattice = lambda g, k: all(sum(comb(j, r) * g[j] for j in range(len(g))) == 0 for r in range(k + 1))
for key, c in sorted(cert.items(), key=lambda t: int(t[0])):
    n, k, B, N = int(key), c['k'], c['basis'], int(key) ** 2
    R2, nrm = F(c['R2']), gs_norms(B)
    std = [[0] * i + [(-1) ** (k + 1 - j) * comb(k + 1, j) for j in range(k + 2)] + [0] * (n - k - 2 - i) for i in range(n - k - 1)]
    assert R2 == F(n ** 5 * (n * n - 1), 12) and len(B) == n - k - 1 and all(in_lattice(b, k) for b in B)
    assert prod(nrm) == prod(gs_norms(std)), 'basis does not generate Lambda_{n,k}'  # same rank, same covolume
    assert [str(t) for t in nrm] == c['gs_norms_sq']
    if min(nrm) > R2: assert not c['vectors']  # every nonzero lattice vector has norm^2 >= min |b_i*|^2 > R^2
    else:  # the list is the whole ball (both v and -v), by exact enumeration over the certified basis
        found = ball(B, R2); assert len(found) == len(set(found)) and set(found) == {tuple(v['gamma']) for v in c['vectors']}
    for v in c['vectors']:
        g, p, J = v['gamma'], v['p'], v['J']
        s = sum(g[j] for j in J) * (1 if v['sign'] == '+' else -1)
        assert in_lattice(g, k) and any(g) and sum(x * x for x in g) <= R2 and len(set(J)) == p
        assert 2 * s > p * n * (N - p * n), 'listed vector satisfies (10)'
    print('n=%d k=%d: basis of Lambda_{n,k} ok, min|b*|^2/R^2 = %.3f, %d vectors in the ball (%s), each violates (10)'
          % (n, k, float(min(nrm) / R2), len(c['vectors']), 'min |b*|^2 > R^2' if min(nrm) > R2 else 'complete by enumeration'))
print('all certificates verified')
