"""Difference-body ratio sigma(G) = vol(G-G) / (8 vol(G)) = vol((G-G)/2) / vol(G) of the 880 order-4 gems (exact rational
arithmetic).  G-G is the convex hull of the 256 pairwise differences of the 16 points.  sigma >= 1 (Brunn-Minkowski), with
equality iff G is centrally symmetric; sigma <= 5/2 (Rogers-Shephard).
Run from this directory:  python3 difference_body_ratio.py > difference_body_ratio.log -> results_sigma.json
"""
import os, json
from fractions import Fraction
import numpy as np
from scipy.spatial import ConvexHull
from gem_geometry import scaled_points

HERE = os.path.dirname(os.path.abspath(__file__))
SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
SYM = json.load(open(os.path.join(HERE, 'symmetry_880.json')))


def vol6(P):
    """6 * volume of conv(P) for an integer point set (exact: sum of |det| of the qhull triangulation, cross-checked)"""
    P = np.asarray(P, dtype=np.int64)
    h = ConvexHull(P.astype(float)); ref = P[h.vertices[0]]
    A = P[h.simplices] - ref
    det = (A[:, 0, 0] * (A[:, 1, 1] * A[:, 2, 2] - A[:, 1, 2] * A[:, 2, 1])
           - A[:, 0, 1] * (A[:, 1, 0] * A[:, 2, 2] - A[:, 1, 2] * A[:, 2, 0])
           + A[:, 0, 2] * (A[:, 1, 0] * A[:, 2, 1] - A[:, 1, 1] * A[:, 2, 0]))
    v = int(np.abs(det).sum()); assert abs(v / 6 - h.volume) < 1e-6 * max(1.0, h.volume)
    return v


res = []
for k in range(880):
    P = scaled_points(SQ[k])                                    # doubled coordinates 2p
    D = (P[:, None, :] - P[None, :, :]).reshape(-1, 3)          # 2(p-q); (G-G)/2 has doubled-coordinates D/2
    sigma = Fraction(vol6(D), 8 * vol6(P))                      # vol((G-G)/2)/vol(G) = vol6(D)/8 / vol6(P)... (D = 2*(p-q))
    Pm = P * np.array([1, 1, -1]); Dm = (Pm[:, None, :] - Pm[None, :, :]).reshape(-1, 3)
    assert Fraction(vol6(Dm), 8 * vol6(Pm)) == sigma              # mirror image / complement: same sigma
    assert sigma >= 1
    res.append(sigma)
asc = [SYM[k]['assoc'] for k in range(880)]
assert all((s == 1) == a for s, a in zip(res, asc)) and sum(asc) == 48
non = [(s, k) for k, s in enumerate(res) if not asc[k]]
smin, kmin = min(non); smax, kmax = max(non)
print('sigma=1 for', sum(s == 1 for s in res), 'gems; min over the other 832:', smin, float(smin), '(square #%d)' % kmin,
      '; max:', smax, float(smax), '(square #%d)' % kmax)
assert smax == Fraction(145, 88) and kmax == 218 and abs(float(smin) - 1.0383) < 5e-5
json.dump(dict(n_sigma_one=sum(s == 1 for s in res), min_nonassociative=str(smin), min_index=kmin, max=str(smax), max_index=kmax,
               sigma=[str(s) for s in res]), open(os.path.join(HERE, 'results_sigma.json'), 'w'))
