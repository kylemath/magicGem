"""
Computer-assisted proof that the Siamese (de la Loubere) gem of odd order
n = 2m+1 >= 5 has exactly 12 hull vertices, with f-vector (12, 26, 16).

All checks are polynomial identities / inequalities in m, verified exactly
with integer polynomial arithmetic, valid for every integer m >= 2.

Setup (see fragment.tex):
  closed form   s(i,j) = n*((i+j-m) mod n) + ((i+2j-2m) mod n) + 1
  gem coords    x = j-m, y = m-i, z = s - (n^2+1)/2
  identity      z = L(x,y) + n * zeta(x,y),   L affine,
                zeta = -n*floor((x-y+m)/n) - floor((2x-y+m)/n)
  The affine bijection (x,y,z) -> (x,y,zeta) preserves hull combinatorics.
  zeta takes 5 values on 5 lattice polygons:
      T (zeta=n+1): triangle (-m,m), (-1,m), (-m,1)
      U (zeta=1)  : triangle (-m,-m+1), (-m,0), (-1,m-1)
      M (zeta=0)  : parallelogram (-m,-m), (0,m), (m,m), (0,-m)
      D = -U (zeta=-1),  B = -T (zeta=-(n+1))
"""
import json, os, sys
from fractions import Fraction
from itertools import combinations
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from siamese_util import siamese, siamese_closed_form, zeta_points

# ---------------------------------------------------------------- polynomials in m
class Poly:
    """integer polynomial in m, coefficient list c[0] + c[1] m + ..."""
    def __init__(self, c):
        c = [int(x) for x in c]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = c or [0]
    @staticmethod
    def const(a): return Poly([a])
    def __add__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        n = max(len(self.c), len(o.c))
        return Poly([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)])
    __radd__ = __add__
    def __neg__(self): return Poly([-a for a in self.c])
    def __sub__(self, o): return self + (-(o if isinstance(o, Poly) else Poly.const(o)))
    def __rsub__(self, o): return Poly.const(o) - self
    def __mul__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        r = [0] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                r[i + j] += a * b
        return Poly(r)
    __rmul__ = __mul__
    def __call__(self, m): return sum(a * m ** i for i, a in enumerate(self.c))
    def is_zero(self): return self.c == [0]
    def deg(self): return len(self.c) - 1
    def __repr__(self):
        terms = []
        for i, a in enumerate(self.c):
            if a == 0: continue
            if i == 0: terms.append(f"{a}")
            elif i == 1: terms.append(f"{a}m")
            else: terms.append(f"{a}m^{i}")
        return " + ".join(terms) if terms else "0"
    def shift(self, s):
        """coefficients of p(s + t) in t"""
        from math import comb
        r = [0] * len(self.c)
        for i, a in enumerate(self.c):
            for k in range(i + 1):
                r[k] += a * comb(i, k) * s ** (i - k)
        return Poly(r)
    def sign_for_m_ge(self, m0=2):
        """Rigorous sign of p(m) for all integers m >= m0:
        returns +1, -1, 0 (identically zero) or None (sign changes)."""
        if self.is_zero():
            return 0
        q = self.shift(m0)        # q(t) = p(m0 + t), t >= 0 integer
        lead = q.c[-1]
        if all(a >= 0 for a in q.c) and q.c[0] > 0: return +1
        if all(a <= 0 for a in q.c) and q.c[0] < 0: return -1
        # Cauchy bound: all real roots of q have |t| <= R
        R = 1 + max(abs(Fraction(a, lead)) for a in q.c[:-1]) if len(q.c) > 1 else 0
        s = 1 if lead > 0 else -1          # sign beyond the root bound
        for t in range(0, int(R) + 2):
            v = q(t)
            if v == 0 or (v > 0) != (s > 0):
                return None
        return s

M = Poly([0, 1])

def P3(x, y, z):
    return tuple(v if isinstance(v, Poly) else Poly.const(v) for v in (x, y, z))

def sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def det3(a, b, c): return dot(a, cross(b, c))

# ---------------------------------------------------------------- the 12 claimed vertices (symbolic)
n_ = 2 * M + 1
VERTS = {
    'v1': P3(-M, M, n_ + 1), 'v2': P3(-1, M, n_ + 1), 'v3': P3(-M, 1, n_ + 1),          # T
    'v4': P3(-M, 0, 1),                                                                  # U
    'v5': P3(-M, -M, 0), 'v6': P3(0, -M, 0), 'v7': P3(0, M, 0), 'v8': P3(M, M, 0),     # M
    'v9': P3(M, 0, -1),                                                                  # D
    'v10': P3(M, -M, -(n_ + 1)), 'v11': P3(M, -1, -(n_ + 1)), 'v12': P3(1, -M, -(n_ + 1)),  # B
}
# polygon vertices of the five layers (all lattice points of a layer are convex combinations of these)
LAYER_POLY = {
    'T': [P3(-M, M, n_ + 1), P3(-1, M, n_ + 1), P3(-M, 1, n_ + 1)],
    'U': [P3(-M, 1 - M, 1), P3(-M, 0, 1), P3(-1, M - 1, 1)],
    'M': [P3(-M, -M, 0), P3(0, M, 0), P3(M, M, 0), P3(0, -M, 0)],
    'D': [P3(M, M - 1, -1), P3(M, 0, -1), P3(1, 1 - M, -1)],
    'B': [P3(M, -M, -(n_ + 1)), P3(1, -M, -(n_ + 1)), P3(M, -1, -(n_ + 1))],
}


def check_layers(n):
    """Lemma: the lattice points of the transformed gem are exactly the lattice
    points of the five polygons at the five heights (checked numerically for this n)."""
    m = (n - 1) // 2
    P = zeta_points(n)
    pts = {tuple(int(v) for v in p) for p in P}
    def lattice_pts_in_polygon(poly):
        poly = [(int(p[0](m)), int(p[1](m)), int(p[2](m))) for p in poly]
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]; z = poly[0][2]
        out = set()
        # integer points inside convex polygon: all orientation tests >= 0 (polygon ccw or cw)
        k = len(poly)
        for x in range(min(xs), max(xs) + 1):
            for y in range(min(ys), max(ys) + 1):
                signs = []
                for a in range(k):
                    p, q = poly[a], poly[(a + 1) % k]
                    signs.append((q[0] - p[0]) * (y - p[1]) - (q[1] - p[1]) * (x - p[0]))
                if all(s >= 0 for s in signs) or all(s <= 0 for s in signs):
                    out.add((x, y, z))
        return out
    union = set()
    for name, poly in LAYER_POLY.items():
        union |= lattice_pts_in_polygon(poly)
    return union == pts


# ---------------------------------------------------------------- facets found numerically at a reference m
def numeric_facets(n):
    from scipy.spatial import ConvexHull
    from gem_geometry import _plane
    m = (n - 1) // 2
    P = zeta_points(n)
    h = ConvexHull(P.astype(float))
    name_of = {tuple(int(c(m)) for c in v): k for k, v in VERTS.items()}
    assert sorted(name_of) == sorted(tuple(int(c) for c in P[v]) for v in h.vertices), 'vertex list mismatch'
    facets = {}
    for s in h.simplices:
        a, b, c, d = _plane(P[s[0]], P[s[1]], P[s[2]])
        if a * P[:, 0].sum() + b * P[:, 1].sum() + c * P[:, 2].sum() + d * len(P) > 0:
            a, b, c, d = -a, -b, -c, -d
        facets.setdefault((a, b, c, d), set())
    out = []
    for (a, b, c, d) in facets:
        vals = a * P[:, 0] + b * P[:, 1] + c * P[:, 2] + d
        on = [name_of[tuple(int(x) for x in P[t])] for t in np.nonzero(vals == 0)[0] if tuple(int(x) for x in P[t]) in name_of]
        out.append(sorted(on, key=lambda s: int(s[1:])))
    return sorted(out)


def main():
    report = {}
    # (0) closed form and layer lemma, numerically for n = 3..41
    for n in range(3, 43, 2):
        assert (siamese(n) == siamese_closed_form(n)).all()
        assert check_layers(n), n
    report['closed_form_and_layers_checked_n'] = list(range(3, 43, 2))

    # (1) combinatorial facet structure, same for all reference orders
    ref = numeric_facets(11)
    for n in (5, 7, 9, 13, 15, 21):
        assert numeric_facets(n) == ref, n
    assert len(ref) == 16
    report['facets_vertex_sets'] = ref

    # (2) symbolic planes from the first three vertices of each facet, oriented so that
    #     the centroid of the 12 vertices is strictly inside (sign fixed at m=5, then proven)
    centroid_num = tuple(sum(VERTS[k][i](5) for k in VERTS) for i in range(3))  # 12 * centroid
    planes = []
    for F in ref:
        p0, p1, p2 = VERTS[F[0]], VERTS[F[1]], VERTS[F[2]]
        nrm = cross(sub(p1, p0), sub(p2, p0))
        d = -dot(nrm, p0)
        val = sum(nrm[i](5) * centroid_num[i] for i in range(3)) + 12 * d(5)
        if val > 0:
            nrm = tuple(-c for c in nrm); d = -d
        planes.append((nrm, d, F))

    # (3a) every claimed vertex lies on the plane identically; all other vertices strictly inside for all m>=2
    strict_polys = []
    for nrm, d, F in planes:
        for k, v in VERTS.items():
            val = dot(nrm, v) + d
            if k in F:
                assert val.is_zero(), (F, k, val)
            else:
                s = val.sign_for_m_ge(2)
                assert s == -1, (F, k, val, s)
                strict_polys.append(str(val))
    # (3b) all layer-polygon vertices satisfy every inequality for all m>=2 (hence all N points do)
    layer_polys = []
    for nrm, d, F in planes:
        for name, poly in LAYER_POLY.items():
            for p in poly:
                val = dot(nrm, p) + d
                s = val.sign_for_m_ge(2)
                assert s in (-1, 0), (F, name, val, s)
                layer_polys.append(str(val))
    # (3c) each facet polygon: convex position & cyclic order; collect edges
    edges = Counter()
    facet_cycles = []
    for nrm, d, F in planes:
        pts = [VERTS[k] for k in F]
        if len(F) == 3:
            cyc = F
        else:
            # order cyclically by angle at m=5, then prove convex position for all m>=2
            c5 = [tuple(float(c(5)) for c in p) for p in pts]
            cen = np.mean(c5, axis=0)
            nn = np.array([float(c(5)) for c in nrm])
            e1 = np.array(c5[0]) - cen; e1 -= nn * (e1 @ nn) / (nn @ nn); e1 /= np.linalg.norm(e1)
            e2 = np.cross(nn / np.linalg.norm(nn), e1)
            ang = [np.arctan2((np.array(q) - cen) @ e2, (np.array(q) - cen) @ e1) for q in c5]
            order = np.argsort(ang)
            cyc = [F[i] for i in order]
            # convexity: orientation of consecutive triples (w.r.t. the outward normal) has constant sign
            signs = set()
            k = len(cyc)
            for a in range(k):
                p, q, r = VERTS[cyc[a]], VERTS[cyc[(a + 1) % k]], VERTS[cyc[(a + 2) % k]]
                t = det3(nrm, sub(q, p), sub(r, q))
                s = t.sign_for_m_ge(2)
                assert s in (1, -1), (F, t, s)
                signs.add(s)
            assert len(signs) == 1, (F, signs)
        facet_cycles.append(cyc)
        for a in range(len(cyc)):
            e = frozenset((cyc[a], cyc[(a + 1) % len(cyc)]))
            edges[e] += 1
    assert all(c == 2 for c in edges.values()), edges
    V, E, Fc = len(VERTS), len(edges), len(planes)
    assert (V, E, Fc) == (12, 26, 16) and V - E + Fc == 2
    # (3d) every claimed vertex is on >= 3 facets with linearly independent normals (so it is a vertex of Q)
    for k in VERTS:
        inc = [nrm for nrm, d, F in planes if k in F]
        assert len(inc) >= 3
        ok = False
        for a, b, c in combinations(inc, 3):
            if det3(a, b, c).sign_for_m_ge(2) in (1, -1):
                ok = True; break
        assert ok, k
    report['proof_checks'] = dict(
        n_planes=16, n_strict_inequalities_vertices=len(strict_polys),
        n_layer_vertex_inequalities=len(layer_polys),
        edges=26, euler=V - E + Fc, face_sizes=sorted(len(c) for c in facet_cycles),
        valid_for='all integers m >= 2, i.e. all odd n >= 5')
    report['planes'] = [dict(normal=[str(c) for c in nrm], offset=str(d), vertices=F, cycle=cyc)
                        for (nrm, d, F), cyc in zip(planes, facet_cycles)]
    # (4) the 12 cells and values in the original square, symbolic in m, cross-checked numerically
    cells = {}
    for k, v in VERTS.items():
        x, y = v[0], v[1]
        i, j = M - y, x + M
        cells[k] = dict(x=str(x), y=str(y), zeta=str(v[2]), i=str(i), j=str(j))
    for n in (5, 7, 9, 11, 21):
        m = (n - 1) // 2; S = siamese(n)
        from gem_geometry import exact_hull
        h = exact_hull(S)
        hv = sorted((v // n, v % n) for v in h['vertices'])
        pred = sorted((int((M - VERTS[k][1])(m)), int((VERTS[k][0] + M)(m))) for k in VERTS)
        assert hv == pred, n
        for k in VERTS:
            i, j = int((M - VERTS[k][1])(m)), int((VERTS[k][0] + M)(m))
            cells[k].setdefault('values', {})[n] = int(S[i, j])
    report['vertex_cells'] = cells
    with open(f'{HERE}/results_siamese_proof.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('Siamese 12-vertex proof: all symbolic checks passed for all m >= 2.')
    for pl in report['planes']:
        print('  plane', pl['normal'], pl['offset'], pl['cycle'])
    for k, c in cells.items():
        print(' ', k, c)


if __name__ == '__main__':
    main()
