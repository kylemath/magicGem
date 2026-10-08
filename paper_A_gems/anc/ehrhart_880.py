"""Ehrhart polynomials of the 880 order-4 gems (exact integer arithmetic).
Q = G + (1/2,1/2,1/2) is a lattice polytope (all coordinates of the points of G are half-odd integers); L_Q(t) = #(tQ cap Z^3)
is counted directly for t = 0..6, the cubic L(t) = 1 + c1 t + c2 t^2 + vol t^3 is interpolated from t = 0..3 and checked at t = 4,5,6;
h* is read off from  (1-t)^4 sum_k L(k) t^k, with  h*_3 = #interior lattice points (Ehrhart-Macdonald) and  sum h* = 6 vol  checked.
Also the Lo Shu (n = 3, G itself a lattice polytope).   Run from this directory:  python3 ehrhart_880.py -> results_ehrhart.json
"""
import os, json
from fractions import Fraction
from math import comb
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import ConvexHull
from gem_geometry import scaled_points, exact_hull, _plane

HERE = os.path.dirname(os.path.abspath(__file__))
SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
GEO = json.load(open(os.path.join(HERE, 'results_geometry.json')))


def analyse(S):
    S = np.asarray(S); n = S.shape[0]
    P = scaled_points(S)                                         # 2p
    if n % 2 == 0:
        assert (P % 2 == 1).all(); Q = (P + 1) // 2              # Q = G + (1/2,1/2,1/2)
    else:
        assert (P % 2 == 0).all(); Q = P // 2                    # Q = G
    h = exact_hull(S)
    planes = set()
    for s in ConvexHull(Q.astype(float)).simplices:
        a, b, c, d = _plane(Q[s[0]], Q[s[1]], Q[s[2]])
        if a * int(Q[:, 0].sum()) + b * int(Q[:, 1].sum()) + c * int(Q[:, 2].sum()) + d * len(Q) > 0: a, b, c, d = -a, -b, -c, -d
        planes.add((a, b, c, d))
    A = np.array([p[:3] for p in planes], dtype=np.int64); hh = np.array([-p[3] for p in planes], dtype=np.int64)
    assert all((A @ q <= hh).all() for q in Q)
    lo, hi = Q.min(0), Q.max(0)

    def count(t, strict=False):
        if t == 0: return 0 if strict else 1
        X, Y, Z = np.meshgrid(*[np.arange(t * lo[i], t * hi[i] + 1) for i in range(3)], indexing='ij')
        pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1); v = pts @ A.T
        return int(((v < t * hh).all(1) if strict else (v <= t * hh).all(1)).sum())

    L = [count(t) for t in range(7)]; assert L[0] == 1
    d1 = L[1] - 1; d2 = L[2] - 1; d3 = L[3] - 1                 # solve c1 t + c2 t^2 + c3 t^3 = L(t) - 1 for t = 1, 2, 3
    M = [[Fraction(t ** k) for k in (1, 2, 3)] for t in (1, 2, 3)]
    rhs = [Fraction(d1), Fraction(d2), Fraction(d3)]
    # Gaussian elimination over Q
    for i in range(3):
        piv = next(r for r in range(i, 3) if M[r][i] != 0); M[i], M[piv] = M[piv], M[i]; rhs[i], rhs[piv] = rhs[piv], rhs[i]
        for r in range(3):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]; M[r] = [a - f * b for a, b in zip(M[r], M[i])]; rhs[r] -= f * rhs[i]
    c1, c2, c3 = [rhs[i] / M[i][i] for i in range(3)]
    for t in range(4, 7): assert 1 + c1 * t + c2 * t ** 2 + c3 * t ** 3 == L[t], 'not a cubic'
    assert c3 == h['volume']                                     # leading coefficient = volume
    inter = count(1, strict=True)
    hs = [sum((-1) ** j * comb(4, j) * L[i - j] for j in range(i + 1)) for i in range(4)]
    assert hs[3] == inter and sum(hs) == 6 * c3 and -(1 - c1 + c2 - c3) == inter     # h*_3 = interior; L(-1) = -interior
    assert all(x >= 0 for x in hs)
    return dict(coef=(c1, c2, c3), h=tuple(hs), L1=L[1], inter=inter, vol=c3, f=tuple(h['f_vector']))


# Lo Shu and Duerer
LOSHU = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
r = analyse(LOSHU)
assert (r['coef'], r['h']) == ((1, 13, 18), (1, 29, 73, 5)) and r['L1'] == 33 and r['inter'] == 5
print('Lo Shu: L(t) = 1 + %s t + %s t^2 + %s t^3, h* = %s' % (r['coef'][0], r['coef'][1], r['coef'][2], r['h']))
res = [analyse(S) for S in SQ]
cp = GEO['complement_partner']
typ = [GEO['per_gem'][k]['combinatorial_type'] for k in range(880)]
poly = [(r['coef'], r['h']) for r in res]
fv = [r['f'] for r in res]; vol = [r['vol'] for r in res]; hv = [r['h'] for r in res]
ST = dict(
    all_hstar_nonnegative_integers=True,
    h1_range=(min(h[1] for h in hv), max(h[1] for h in hv)), h2_range=(min(h[2] for h in hv), max(h[2] for h in hv)),
    h3_range=(min(h[3] for h in hv), max(h[3] for h in hv)),
    distinct_polynomials=len(set(poly)), distinct_hstar=len(set(hv)), distinct_f=len(set(fv)), distinct_types=len(set(typ)),
    distinct_volumes=len(set(vol)), complement_same_polynomial=all(poly[k] == poly[cp[k]] for k in range(880)),
    n_classes=len({min(k, cp[k]) for k in range(880)}),
    c2_denominators=dict(Counter(Fraction(r['coef'][1]).denominator for r in res)),
    vol_denominators=dict(Counter(Fraction(v).denominator for v in vol)),
    L1_range=(min(r['L1'] for r in res), max(r['L1'] for r in res)),
)
def n_multi(key):
    d = defaultdict(set)
    for k in range(880): d[key[k]].add(poly[k])
    return sum(len(s) > 1 for s in d.values()), len(d)
ST['f_vectors_with_several_polynomials'] = n_multi(fv); ST['types_with_several_polynomials'] = n_multi(typ); ST['volumes_with_several_polynomials'] = n_multi(vol)
assert ST['complement_same_polynomial'] and ST['n_classes'] == 616 and ST['distinct_types'] == 352 and ST['distinct_f'] == 39 and ST['distinct_volumes'] == 155
assert ST['h1_range'] == (70, 136) and ST['h3_range'] == (34, 52) and ST['distinct_polynomials'] == 554
assert ST['distinct_polynomials'] == ST['distinct_hstar']
dur = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
rd = analyse(dur)
assert (rd['coef'], rd['h']) == ((-3, 44, 92), (1, 130, 377, 44))
print('Duerer: L(t) = 1 + %s t + %s t^2 + %s t^3, h* = %s' % (rd['coef'][0], rd['coef'][1], rd['coef'][2], rd['h']))
for k, v in ST.items(): print(k, v)
json.dump(dict(stats=ST, loshu=dict(coef=[str(c) for c in r['coef']], h=r['h']), durer=dict(coef=[str(c) for c in rd['coef']], h=rd['h']),
               per_gem=[dict(index=k, coef=[str(c) for c in res[k]['coef']], h=list(res[k]['h']), L1=res[k]['L1'], interior=res[k]['inter']) for k in range(880)]),
          open(os.path.join(HERE, 'results_ehrhart.json'), 'w'), default=str)
