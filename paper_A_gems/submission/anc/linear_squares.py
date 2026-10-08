"""
linear_squares.py -- vertex counts of the gems of all linear ("cyclic") magic squares of odd order n:
    s(i,j) = n*<a1 i + a2 j + alpha> + <b1 i + b2 j + beta> + 1,   <t> = t mod n,
over all a1,a2,b1,b2,alpha,beta in Z_n that give a magic square (rows, columns, both diagonals), up to D4.
Exact hulls (gem_geometry.exact_hull).  Usage: python3 linear_squares.py 5 7 9 11   (n = 11 takes about 2-3 min)
Writes results_linear_squares.json and linear_squares.log.  The Siamese square is linear (Section 5) and is checked
to be among the classes with the minimal vertex count for n >= 7.
"""
import sys, os, json, itertools, time
import numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull
from siamese_util import siamese

def d4forms(S):
    return [S, np.rot90(S, 1), np.rot90(S, 2), np.rot90(S, 3), S.T, np.rot90(S, 1).T, np.rot90(S, 2).T, np.rot90(S, 3).T]

def canon(S): return min(tuple(g.flatten()) for g in d4forms(S))

res, log = {}, []
for n in [int(a) for a in sys.argv[1:]] or [5, 7, 9]:
    t0 = time.time(); N = n * n; Mc = n * (N + 1) // 2
    I, J = np.indices((n, n)); seen = {}
    for a1, a2, b1, b2 in itertools.product(range(n), repeat=4):
        A0 = (a1 * I + a2 * J) % n; B0 = (b1 * I + b2 * J) % n
        for al in range(n):
            A = (A0 + al) % n
            for be in range(n):
                S = n * A + (B0 + be) % n + 1
                if len(np.unique(S)) != N: continue
                if (S.sum(0) != Mc).any() or (S.sum(1) != Mc).any() or np.trace(S) != Mc or np.trace(S[:, ::-1]) != Mc: continue
                seen.setdefault(canon(S), S)
    V = {k: exact_hull(S)['f_vector'][0] for k, S in seen.items()}
    dist = Counter(V.values()); vmin = min(dist)
    sia = canon(siamese(n))
    assert sia in V and V[sia] == 12
    if n >= 7: assert vmin == 12
    res[n] = dict(classes=len(seen), V_distribution=dict(sorted(dist.items())), V_min=vmin, V_max=max(dist),
                  n_min=dist[vmin], siamese_V=V[sia], seconds=round(time.time() - t0))
    log.append(f'n={n}: {len(seen)} D4-classes of linear magic squares; V from {vmin} ({dist[vmin]} classes) to {max(dist)}; '
               f'Siamese V={V[sia]}; {res[n]["seconds"]} s')
    print(log[-1], flush=True)
# the Siamese square with its two digits exchanged: s = n<i+2j-2m> + <i+j-m> + 1
sw = {}
for n in range(5, 33, 2):
    m = (n - 1) // 2; I, J = np.indices((n, n)); S = n * ((I + 2 * J - 2 * m) % n) + ((I + J - m) % n) + 1
    N = n * n; Mc = n * (N + 1) // 2
    assert (S.sum(0) == Mc).all() and (S.sum(1) == Mc).all() and np.trace(S) == Mc and np.trace(S[:, ::-1]) == Mc
    h = exact_hull(S); assert h['f_vector'] == (12, 24, 14), n
    corners = {(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)}
    sw[n] = dict(f=list(h['f_vector']), vertices_at_corners=len(corners & {(v // n, v % n) for v in h['vertices']}))
res['digit_exchanged_square'] = sw
log.append("digit-exchanged square s' = n<i+2j-2m> + <i+j-m> + 1: magic, gem f-vector (12,24,14) for n = 5..31")
print(log[-1])
json.dump(res, open(os.path.join(HERE, 'results_linear_squares.json'), 'w'), indent=1)
open(os.path.join(HERE, 'linear_squares.log'), 'w').write('\n'.join(log) + '\n')
