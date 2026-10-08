"""Ehrhart analysis of Magic Gems (exact integer arithmetic).
Lattice polytope used:  Q = conv{ (j, n-1-i, s_ij - (N+1)/2 + shift) } with half-odd offsets removed,
i.e. for even n  Q = gem + (1/2,1/2,1/2)  (gem = conv of p_ij in paper coords); for odd n Q = gem.
Explicitly Q = conv{(j, n-1-i, s_ij - ceil(N/2))}  hmm -> we build via doubled coords P=2p: Q=(P+1)/2 (even n) or P/2 (odd n).
"""
import sys, os, json, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/kylemathewson/magicGem/paper_A_gems/anc')
from fractions import Fraction
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import ConvexHull
from gem_geometry import scaled_points, exact_hull, _plane
from math import gcd

ANC = '/Users/kylemathewson/magicGem/paper_A_gems/anc'

def lattice_Q(S):
    """integer vertex candidates of Q and exact facet inequalities  A q <= h  (A primitive int)"""
    S = np.asarray(S); n = S.shape[0]
    P = scaled_points(S)               # doubled coords, parity of (n-1) in x,y and of N+1 in z
    if n % 2 == 0:
        assert (P % 2 == 1).all()
        Q = (P + 1) // 2
    else:
        assert (P % 2 == 0).all()
        Q = P // 2
    h = exact_hull(S)
    verts = h['vertices']
    # facets in Q coordinates: recompute planes from hull of Q directly (exact)
    H = ConvexHull(Q.astype(float))
    planes = {}
    for s in H.simplices:
        a, b, c, d = _plane(Q[s[0]], Q[s[1]], Q[s[2]])
        val = a*int(Q[:,0].sum()) + b*int(Q[:,1].sum()) + c*int(Q[:,2].sum()) + d*len(Q)
        if val > 0: a, b, c, d = -a, -b, -c, -d
        planes[(a, b, c, d)] = 1
    A = np.array([[a, b, c] for a, b, c, d in planes], dtype=np.int64)
    hh = np.array([-d for a, b, c, d in planes], dtype=np.int64)   # A q <= hh
    for k in range(len(Q)):
        assert (A @ Q[k] <= hh).all()
    vq = Q[verts]
    # every vertex is integral by construction; check that facets are tight on >=3 vertices
    for r in range(len(A)):
        assert ((vq @ A[r]) == hh[r]).sum() >= 3
    return Q, verts, A, hh, h

def count_points(A, hh, t, strict=False):
    """# integer points q with A q <= t*hh (strict: A q < t*hh), exact int arithmetic."""
    # bounding box via vertices is implied; use generous box from LP-free bound: use hull vertex extents passed in
    raise NotImplementedError

def make_counter(Q, verts, A, hh):
    V = Q[verts]
    lo = V.min(0); hi = V.max(0)
    def count(t, strict=False):
        if t == 0 and strict: return 0
        rng = [np.arange(t*lo[k], t*hi[k]+1) for k in range(3)]
        X, Y, Z = np.meshgrid(*rng, indexing='ij')
        pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
        vals = pts @ A.T
        lim = t * hh
        ok = (vals < lim).all(1) if strict else (vals <= lim).all(1)
        return int(ok.sum())
    return count

def interp(vals):
    """exact Lagrange/Newton interpolation through (t, vals[t]), t=0..3 -> coefficients c0..c3 (Fractions)"""
    import sympy as sp
    t = sp.symbols('t')
    poly = sp.interpolate([(k, sp.Integer(v)) for k, v in enumerate(vals)], t)
    p = sp.Poly(sp.expand(poly), t)
    co = [Fraction(int(c.p), int(c.q)) for c in [p.coeff_monomial(t**k) for k in range(4)]]
    return co

def analyse(S, tmax=6):
    Q, verts, A, hh, h = lattice_Q(S)
    cnt = make_counter(Q, verts, A, hh)
    L = [cnt(t) for t in range(tmax+1)]
    assert L[0] == 1
    co = interp(L[:4])
    for t in range(4, tmax+1):
        assert sum(co[k]*t**k for k in range(4)) == L[t], 'Ehrhart interpolation failed'
    vol = co[3]
    assert vol == h['volume']*Fraction(1)/1 * 1 or True
    # reciprocity: interior points
    inter = cnt(1, strict=True)
    # h*: (1-t)^4 sum L(k)t^k  truncated to degree 3
    Ls = L[:4]
    hs = []
    for i in range(4):
        # coefficient of t^i in (1-t)^4 * sum_k L_k t^k : sum_j (-1)^j C(4,j) L_{i-j}
        from math import comb
        hs.append(sum((-1)**j * comb(4, j) * Ls[i-j] for j in range(i+1)))
    assert hs[3] == inter, (hs, inter)             # h*_3 = #interior points (Ehrhart-Macdonald reciprocity)
    assert sum(hs) == 6*vol
    # also check L(-1) = -interior  (reciprocity) from polynomial: (-1)^3 L(-1)=interior
    assert -sum(co[k]*(-1)**k for k in range(4)) == inter
    bd = L[1] - inter
    # lattice width (directions with |u_i|<=W)
    V = Q[verts]
    return dict(L=L, coef=co, h=hs, inter=inter, bd=bd, vol_Q=vol, nverts=len(verts), Q=Q, verts=verts, V=V, h_exact=h)

def lattice_width(V, R=8):
    best = None
    rng = range(-R, R+1)
    U = np.array([u for u in itertools.product(rng, rng, rng) if u != (0,0,0) and
                  next(c for c in u if c != 0) > 0 and gcd(gcd(abs(u[0]), abs(u[1])), abs(u[2])) == 1], dtype=np.int64)
    vals = V @ U.T
    w = vals.max(0) - vals.min(0)
    k = int(np.argmin(w))
    return int(w[k]), tuple(int(x) for x in U[k]), int((w == w[k]).sum())

if __name__ == '__main__':
    SQ = np.loadtxt(os.path.join(ANC, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
    G = json.load(open(os.path.join(ANC, 'results_geometry.json')))
    out = []
    for k, S in enumerate(SQ):
        r = analyse(S)
        h = r['h_exact']
        # volume of gem equals volume of Q (translation)
        assert r['vol_Q'] == h['volume'], (k, r['vol_Q'], h['volume'])
        assert Fraction(G['per_gem'][k]['volume']) == r['vol_Q'] if isinstance(G['per_gem'][k].get('volume'), str) else True
        w, u, mult = lattice_width(r['V'])
        out.append(dict(idx=k, square=S.tolist(), L=r['L'], coef=[str(c) for c in r['coef']], h=r['h'],
                        inter=r['inter'], bd=r['bd'], vol=str(r['vol_Q']), f=list(h['f_vector']),
                        width=w, width_dir=u, width_mult=mult,
                        wl=G['per_gem'][k].get('wl', None)))
        if k % 100 == 0: print(k, out[-1]['coef'], out[-1]['h'], flush=True)
    json.dump(out, open('ehrhart_880.json', 'w'))
