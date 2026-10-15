"""Independent exact hull checker for Magic Gems (referee cross-check).

Does NOT use scipy/qhull or gem_geometry.exact_hull.  Everything is integer arithmetic
(NumPy int64 with explicit overflow bounds, Python ints, Fractions):

  points   p_ij = 2*(x, y, z), x = j-(n-1)/2, y = (n-1)/2-i, z = s_ij-(N+1)/2  (integers)
  facets   for every triple of non-collinear (candidate) points, the primitive integer plane
           through them; kept iff all N points lie on one side; deduplicated.  Every such plane
           contains three non-collinear points, so its on-plane point set is 2-dimensional and
           it is a facet plane; conversely every facet plane contains three non-collinear
           points, so the list is complete.
  vertices the vertices of the exact 2D hulls (strict, collinear points dropped) of the
           on-plane point sets of the facets
  edges    consecutive vertex pairs of the facet polygons; checked: each edge lies in exactly
           two facets, V - E + F = 2
  volume   sum over facet fans of |det|/6 with apex the origin (the centroid of the points,
           hence in the hull), divided by 8 for the doubling
  counts   interior = strictly inside every facet; boundary non-vertex = on some facet, not a vertex

Optional exact pruning for large n (prune=True): K = set of points that are the UNIQUE maximiser
of some integer linear functional (hence vertices).  Points strictly inside conv(K) (decided by the
same brute-force facet enumeration applied to K) are not vertices and cannot be needed to span a
facet plane, so triples are drawn only from the remaining candidates; the support test and all
counts still use all N points.  For n <= 15 the pruned and unpruned runs are compared.

Run:  python3 independent_hull_check.py      -> independent_hull_check.log
"""
import os, sys, time, json, itertools
from math import gcd
from fractions import Fraction
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = []


def log(s=''):
    print(s, flush=True)
    LOG.append(str(s))


def points(S):
    S = [[int(v) for v in row] for row in S]
    n = len(S); N = n * n
    return np.array([(2 * j - (n - 1), (n - 1) - 2 * i, 2 * S[i][j] - (N + 1))
                     for i in range(n) for j in range(n)], dtype=np.int64)


def primitive(a, b, c, d):
    g = gcd(gcd(abs(a), abs(b)), gcd(abs(c), abs(d)))
    return (a // g, b // g, c // g, d // g)


def supporting_planes(P, cand):
    """All facet planes (a,b,c,d) with a x + b y + c z <= d for all points, primitive,
    from triples of indices in cand.  Brute force over triples, vectorised per first index."""
    P = np.asarray(P, dtype=np.int64)
    # overflow guard: |coords| <= M, normals <= 2*(2M)^2, dot <= 3*M*that
    M = int(np.abs(P).max())
    assert 3 * M * 2 * (2 * M) ** 2 * 2 < 2 ** 62
    cand = np.asarray(cand)
    m = len(cand)
    planes = set()
    for a in range(m - 2):
        i = cand[a]
        rest = cand[a + 1:]
        J, K = np.triu_indices(len(rest), 1)
        J = rest[J]; K = rest[K]
        u = P[J] - P[i]; v = P[K] - P[i]
        nr = np.cross(u, v)
        ok = np.any(nr != 0, axis=1)
        nr = nr[ok]
        if len(nr) == 0:
            continue
        vals = nr @ P.T - (nr @ P[i])[:, None]
        le = np.all(vals <= 0, axis=1)
        ge = np.all(vals >= 0, axis=1)
        for row, s in ((nr[le], 1), (nr[ge], -1)):
            for nv in row:
                A, B, C = (int(nv[0]) * s, int(nv[1]) * s, int(nv[2]) * s)
                D = A * int(P[i][0]) + B * int(P[i][1]) + C * int(P[i][2])
                planes.add(primitive(A, B, C, D))
    return sorted(planes)


def hull2d(pts2, idx):
    """Strict convex hull (CCW, collinear points dropped) of integer 2D points; returns indices."""
    order = sorted(range(len(pts2)), key=lambda k: pts2[k])
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for k in order:
        while len(lower) >= 2 and cr(pts2[lower[-2]], pts2[lower[-1]], pts2[k]) <= 0:
            lower.pop()
        lower.append(k)
    for k in reversed(order):
        while len(upper) >= 2 and cr(pts2[upper[-2]], pts2[upper[-1]], pts2[k]) <= 0:
            upper.pop()
        upper.append(k)
    h = lower[:-1] + upper[:-1]
    return [idx[k] for k in h]


def polytope(P, planes):
    P = np.asarray(P, dtype=np.int64)
    Pl = [tuple(int(t) for t in p) for p in P]
    N = len(Pl)
    slack = np.array([[d - (a * x + b * y + c * z) for (x, y, z) in Pl] for (a, b, c, d) in planes],
                     dtype=object)  # exact, >= 0
    assert (slack >= 0).all()
    polys = []
    for f, (a, b, c, d) in enumerate(planes):
        on = [k for k in range(N) if slack[f, k] == 0]
        drop = max(range(3), key=lambda t: abs((a, b, c)[t]))
        keep = [t for t in range(3) if t != drop]
        pts2 = [(Pl[k][keep[0]], Pl[k][keep[1]]) for k in on]
        poly = hull2d(pts2, on)
        assert len(poly) >= 3
        polys.append(poly)
    verts = sorted({v for poly in polys for v in poly})
    edges = Counter()
    for poly in polys:
        for t in range(len(poly)):
            e = tuple(sorted((poly[t], poly[(t + 1) % len(poly)])))
            edges[e] += 1
    assert all(c == 2 for c in edges.values()), 'edge not in exactly two facets'
    V, E, F = len(verts), len(edges), len(planes)
    assert V - E + F == 2, (V, E, F)
    vol6 = 0
    for poly in polys:
        p0 = Pl[poly[0]]
        for t in range(1, len(poly) - 1):
            p1, p2 = Pl[poly[t]], Pl[poly[t + 1]]
            det = (p0[0] * (p1[1] * p2[2] - p1[2] * p2[1]) - p0[1] * (p1[0] * p2[2] - p1[2] * p2[0])
                   + p0[2] * (p1[0] * p2[1] - p1[1] * p2[0]))
            vol6 += abs(det)
    volume = Fraction(vol6, 6 * 8)
    vset = set(verts)
    on_any = [k for k in range(N) if any(slack[f, k] == 0 for f in range(F))]
    interior = N - len(on_any)
    bnv = sum(1 for k in on_any if k not in vset)
    return dict(f=(V, E, F), vertices=verts, volume=volume, interior=interior, bnv=bnv,
                face_sizes=sorted(len(p) for p in polys), planes=planes)


def known_vertices(P):
    """Indices that are the unique maximiser of some small integer functional (exact)."""
    P = np.asarray(P, dtype=np.int64)
    K = set()
    rng = range(-3, 4)
    for w in itertools.product(rng, rng, rng):
        if w == (0, 0, 0):
            continue
        vals = P @ np.array(w, dtype=np.int64)
        mx = vals.max()
        hit = np.flatnonzero(vals == mx)
        if len(hit) == 1:
            K.add(int(hit[0]))
    return sorted(K)


def gem(S, prune=False):
    P = points(S)
    N = len(P)
    cand = np.arange(N)
    if prune:
        K = known_vertices(P)
        PK = P[K]
        planesK = supporting_planes(PK, np.arange(len(K)))
        A = np.array([pl[:3] for pl in planesK], dtype=np.int64)
        d = np.array([pl[3] for pl in planesK], dtype=np.int64)
        strict_in = np.all(P @ A.T < d, axis=1)
        cand = np.flatnonzero(~strict_in)
    planes = supporting_planes(P, cand)
    h = polytope(P, planes)
    h['n_cand'] = len(cand)
    return h


# ------------------------------------------------------------------ helpers on squares
def is_magic(S):
    S = np.asarray(S); n = S.shape[0]; M = n * (n * n + 1) // 2
    return ((S.sum(0) == M).all() and (S.sum(1) == M).all() and np.trace(S) == M
            and np.trace(np.fliplr(S)) == M and sorted(S.ravel().tolist()) == list(range(1, n * n + 1)))


def siamese(n):
    S = [[0] * n for _ in range(n)]
    i, j = 0, n // 2
    for k in range(1, n * n + 1):
        S[i][j] = k
        ni, nj = (i - 1) % n, (j + 1) % n
        if S[ni][nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return np.array(S)


def forced_cells(S):
    """Lemma 'forced vertices', implemented from its statement."""
    S = np.asarray(S); n = S.shape[0]; N = n * n
    F = {(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)}
    for v in (1, N):
        i, j = np.argwhere(S == v)[0]; F.add((int(i), int(j)))
    sides = [[(0, j) for j in range(n)], [(n - 1, j) for j in range(n)],
             [(i, 0) for i in range(n)], [(i, n - 1) for i in range(n)]]
    for side in sides:
        vals = [S[c] for c in side]
        F.add(side[int(np.argmin(vals))]); F.add(side[int(np.argmax(vals))])
    return F


def cells(h, n):
    return {(v // n, v % n) for v in h['vertices']}


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    log('Independent exact hull check (pure integer brute force, no qhull, no gem_geometry)')
    tot_ok = Counter(); tot_bad = []

    # ---------------- 880 order-4 squares
    t = time.time()
    SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
    RG = json.load(open(os.path.join(HERE, 'results_geometry.json')))
    BX = json.load(open(os.path.join(HERE, 'results_box_classes.json')))
    VS = json.load(open(os.path.join(HERE, 'verify_structure.json')))
    H = []
    agree = Counter()
    for k, S in enumerate(SQ):
        assert is_magic(S)
        h = gem(S)
        H.append(h)
        g = RG['per_gem'][k]
        assert g['index'] == k and np.array_equal(np.array(g['square']), S)
        checks = {
            'f_vector': tuple(g['f_vector']) == h['f'],
            'face_sizes': sorted(g['face_sizes']) == h['face_sizes'],
            'vertex_set': {tuple(c) for c in g['hull_vertex_cells']} == cells(h, 4),
            'volume': Fraction(g['volume']) == h['volume'],
            'forced_subset_of_vertices': forced_cells(S) <= cells(h, 4),
        }
        for key, ok in checks.items():
            if ok:
                agree[key] += 1
            else:
                tot_bad.append(('880', k, key))
    log(f'\n[880 order-4 squares]  ({time.time() - t:.1f} s)')
    for key in ['f_vector', 'face_sizes', 'vertex_set', 'volume', 'forced_subset_of_vertices']:
        log(f'  {key:28s} agree {agree[key]}/880')
    # distributions
    fdist = Counter(str(h['f']) for h in H)
    ok = dict(fdist) == RG['f_vector_distribution']; log(f'  f-vector distribution (39 classes) equal: {ok}'); tot_ok['880 fdist'] = ok
    vdist = Counter(str(h['volume']) for h in H)
    ok = {Fraction(a): b for a, b in vdist.items()} == {Fraction(a): b for a, b in RG['volume_distribution'].items()}
    log(f'  volume distribution ({len(vdist)} distinct) equal: {ok};  min {min(h["volume"] for h in H)}, max {max(h["volume"] for h in H)}'
        f' (stored {RG["volume_min"]}, {RG["volume_max"]})'); tot_ok['880 vdist'] = ok
    Idist = Counter(h['interior'] for h in H); Bdist = Counter(h['bnv'] for h in H)
    okI = all(Idist.get(int(a), 0) == b for a, b in VS['I_distribution'].items()) and sum(VS['I_distribution'].values()) == 880
    okB = all(Bdist.get(int(a), 0) == b for a, b in VS['B_distribution'].items()) and sum(VS['B_distribution'].values()) == 880
    okI2 = {str(a): b for a, b in Idist.items()} == BX['interior_points']
    okB2 = {str(a): b for a, b in Bdist.items()} == BX['boundary_nonvertex_points']
    joint = Counter(str((h['interior'], h['bnv'])) for h in H)
    okJ = dict(joint) == BX['interior_boundary_joint']
    log(f'  interior distribution {dict(sorted(Idist.items()))}: = verify_structure {okI}, = box_classes {okI2}')
    log(f'  boundary-nonvertex distribution {dict(sorted(Bdist.items()))}: = verify_structure {okB}, = box_classes {okB2}')
    log(f'  joint (interior, bnv) distribution (21 cells) = box_classes: {okJ}')
    tot_ok.update({'880 I': okI and okI2, '880 B': okB and okB2, '880 joint': okJ})
    for e in BX['eight_vertex_gems']:
        h = H[e['k']]
        ok = (h['f'] == tuple(e['f']) and h['interior'] == e['interior'] and h['bnv'] == e['boundary_nonvertex'])
        tot_ok['8-vertex #%d' % e['k']] = ok
    ok8 = all(tot_ok['8-vertex #%d' % e['k']] for e in BX['eight_vertex_gems'])
    log(f'  the 7 eight-vertex gems (f, interior, bnv) agree: {ok8}')
    for key in ['square_54', 'square_802', 'square_379']:
        e = BX[key]; h = H[int(key.split('_')[1])]
        ok = (len(h['vertices']) == e['nv'] and h['interior'] == e['interior'] and h['bnv'] == e['boundary_nonvertex'])
        tot_ok[key] = ok
        log(f'  {key}: V={len(h["vertices"])} interior={h["interior"]} bnv={h["bnv"]} f={h["f"]} vol={h["volume"]}  agree: {ok}')

    # ---------------- Duerer
    D = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
    assert is_magic(D)
    h = gem(D)
    e = BX['durer']
    ok = (len(h['vertices']) == 12 == e['nv'] and h['interior'] == 4 == e['interior']
          and h['bnv'] == e['boundary_nonvertex'] and h['volume'] == 92)
    # its index among the 880 (D4 image)
    def d4(S):
        out = []; T = S
        for _ in range(4):
            out += [T, T.T]; T = np.rot90(T)
        return out
    idx = [k for k, S in enumerate(SQ) if any(np.array_equal(S, T) for T in d4(D))]
    ok = ok and idx == [e['k']] and H[e['k']]['volume'] == h['volume'] and H[e['k']]['f'] == h['f']
    tot_ok['Duerer'] = ok
    log(f'\n[Duerer]  #{idx}  f={h["f"]} V={len(h["vertices"])} interior={h["interior"]} bnv={h["bnv"]} vol={h["volume"]}'
        f'  (paper: 12 vertices, 4 interior, volume 92)  agree: {ok}')

    # ---------------- Siamese
    log('\n[Siamese squares]  claims: n=3 f=(8,16,10) vol 18 (1 interior); n>=5 f=(12,26,16), 12 triangles + 4 quads,'
        ' vertices = forced; n=5 vol 830/3')
    for n in range(3, 22, 2):
        t = time.time()
        S = siamese(n)
        assert is_magic(S)
        m = (n - 1) // 2
        cf = np.array([[n * ((i + j - m) % n) + ((i + 2 * j - 2 * m) % n) + 1 for j in range(n)] for i in range(n)])
        assert np.array_equal(cf, S)
        brute = n <= 15
        hp = gem(S, prune=True)
        if brute:
            h = gem(S)
            same = (h['planes'] == hp['planes'])
            assert same, f'pruned != unpruned at n={n}'
        else:
            h = hp
        exp_f = (8, 16, 10) if n == 3 else (12, 26, 16)
        exp_fs = [3] * 8 + [4] * 2 if n == 3 else [3] * 12 + [4] * 4
        ok = (h['f'] == exp_f and h['face_sizes'] == exp_fs and cells(h, n) == forced_cells(S))
        if n == 3:
            ok = ok and h['volume'] == 18 and h['interior'] == 1
        if n == 5:
            ok = ok and h['volume'] == Fraction(830, 3)
        tot_ok[f'Siamese n={n}'] = ok
        log(f'  n={n:2d}: f={h["f"]} faces={dict(Counter(h["face_sizes"]))} vertices=forced:{cells(h, n) == forced_cells(S)}'
            f' vol={h["volume"]} interior={h["interior"]} bnv={h["bnv"]}'
            f'  [{"brute force + pruned identical" if brute else "pruned only"}, {hp["n_cand"]}/{n*n} cand, {time.time() - t:.1f} s]  agree: {ok}')

    # ---------------- order-5 SA squares
    t = time.time()
    A = np.loadtxt(os.path.join(HERE, 'sa_n5_V10.txt'), dtype=int).reshape(-1, 5, 5)
    fs = []
    for S in A:
        assert is_magic(S)
        fs.append(gem(S)['f'])
    c = Counter(fs)
    ok = len(A) == 15 and c == Counter({(10, 22, 14): 14, (10, 23, 15): 1})
    tot_ok['sa_n5_V10'] = ok
    log(f'\n[sa_n5_V10.txt] {len(A)} squares, f-vectors {dict(c)}  (claim 14 x (10,22,14), 1 x (10,23,15))  agree: {ok}  ({time.time() - t:.1f} s)')

    # ---------------- Remark 6.3 examples
    R1 = np.array([[1, 18, 10, 22, 14], [25, 12, 4, 16, 8], [19, 6, 23, 15, 2], [13, 5, 17, 9, 21], [7, 24, 11, 3, 20]])
    R2 = np.array([[1, 19, 15, 13, 17], [23, 5, 14, 20, 3], [10, 21, 12, 4, 18], [24, 9, 8, 22, 2], [7, 11, 16, 6, 25]])
    assert is_magic(R1) and is_magic(R2)
    # R1 is the linear square 5<4i+3j>+<4i+2j>+1
    assert all(R1[i, j] == 5 * ((4 * i + 3 * j) % 5) + ((4 * i + 2 * j) % 5) + 1 for i in range(5) for j in range(5))
    h1, h2 = gem(R1), gem(R2)
    ok1 = h1['f'] == (11, 23, 14)
    ok2 = h2['f'] == (10, 22, 14) and h2['volume'] == Fraction(845, 3) and h2['interior'] == 8
    in_sa = any(any(np.array_equal(T, R2) for T in d4(S)) for S in A)
    tot_ok['Remark 6.3 first'] = ok1; tot_ok['Remark 6.3 second'] = ok2
    log(f'\n[Remark 6.3] first : f={h1["f"]} vol={h1["volume"]} interior={h1["interior"]} bnv={h1["bnv"]}  (claim (11,23,14))  agree: {ok1}')
    log(f'[Remark 6.3] second: f={h2["f"]} vol={h2["volume"]} interior={h2["interior"]} bnv={h2["bnv"]}'
        f'  (claim (10,22,14), 845/3, 8 interior)  agree: {ok2};  D4-class listed in sa_n5_V10.txt: {in_sa}')

    log('\n[summary]')
    log(f'  per-gem disagreements among the 880: {len(tot_bad)} {tot_bad[:10]}')
    bad = [k for k, v in tot_ok.items() if not v]
    log(f'  other checks: {sum(tot_ok.values())}/{len(tot_ok)} agree; failures: {bad}')
    log(f'  total runtime {time.time() - t0:.1f} s')
    with open(os.path.join(HERE, 'independent_hull_check.log'), 'w') as fh:
        fh.write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
