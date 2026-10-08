#!/usr/bin/env python3
"""Check kstar_certificates.json (exact arithmetic, standard library only): python3 kstar_check_certificates.py"""
import json, os
from fractions import Fraction as F
from math import comb
cert = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kstar_certificates.json')))
def gs_norms(B):  # squared Gram--Schmidt norms, exact
    Bs, out = [], []
    for b in B:
        v = [F(x) for x in b]
        for u, nu in zip(Bs, out):
            m = sum(a * c for a, c in zip(b, u)) / nu; v = [a - m * c for a, c in zip(v, u)]
        Bs.append(v); out.append(sum(a * a for a in v))
    return out
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
    for v in c['vectors']:
        g, p, J = v['gamma'], v['p'], v['J']
        s = sum(g[j] for j in J) * (1 if v['sign'] == '+' else -1)
        assert in_lattice(g, k) and any(g) and sum(x * x for x in g) <= R2 and len(set(J)) == p
        assert 2 * s > p * n * (N - p * n), 'listed vector satisfies (10)'
    print('n=%d k=%d: basis of Lambda_{n,k} ok, min|b*|^2/R^2 = %.3f, %d vectors in the ball, each violates (10)'
          % (n, k, float(min(nrm) / R2), len(c['vectors'])))
print('all certificates verified')
