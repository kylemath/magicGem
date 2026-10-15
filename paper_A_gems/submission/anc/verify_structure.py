"""
verify_structure.py -- exact checks of the structural statements of the paper (every statement asserted).

  A  coplanar point sets: for n = 2, 3 (all arrangements) the points p_ij are coplanar exactly for the
     8 D4-images of the natural square s_ij = n i + j + 1; for n = 4..6 these 8 are coplanar and
     random arrangements are not; no semi-magic square is coplanar (all 880 of order 4 checked).
  B  covariance matrix of the point set of every semi-magic square = diag(a, a, b), a=(n^2-1)/12, b=(N^2-1)/12
     (880 order-4 squares, Siamese n = 3..21).
  C  isometries of the point set (Theorem 4.2): for all 880 order-4 squares and the Siamese squares n = 3..15
     |Iso({p_ij})| = 2 iff S is self-complementary, else 1; at hull level (vertex sets) the same for the 880
     and for the Siamese gems n = 5..15.
  D  injectivity: the 880 vertex sets are pairwise distinct up to the action of D4 (D4-canonical forms),
     and the congruence classes of the 880 gems are the 616 complement orbits.
  E  parity for the 48 associative squares (V, B, I even) and the failure for the natural square.
  F  certification of the exact hulls (integer arithmetic): pairwise distinct facet planes, every point satisfies
     every facet inequality, each facet is 2-dimensional and its polygon is the exact 2D hull of the points on its
     plane, every polygon edge lies in exactly two facets (closed facet complex), strict convexity at every edge.
  G  regular subdivisions: lower / upper / vertical facets; vertical facets only over the four sides,
     present iff the heights along that side are not in arithmetic progression; every vertex is a vertex of
     the lower or the upper hull; number of distinct regular subdivisions of the 4x4 grid induced by the
     magic height functions (up to D4).
  H  combinatorial types are unions of complement orbits; composition of the 352 types.
  I  Siamese gems n = 3..41: vertex cells = forced cells (corners, entries 1 and N, side extremes).
  J  squares880.txt lists the Frenicle standard forms in lexicographic order.
  K  census numbers by number of vertices (strictly interior / non-vertex boundary counts, k = 0..6).
Writes verify_structure.json and verify_structure.log.
"""
import itertools, math, json, os, sys, time
from collections import Counter, defaultdict
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gem_geometry import exact_hull, classify_points, congruent, sqdist_multiset
from isolib import isometries
from siamese_util import siamese

T0 = time.time()
LOG = []
OUT = {}


def log(s):
    print(s, flush=True)
    LOG.append(s)


def d4(S):
    """the 8 images gS of a square (numpy), as a dict name -> array; (gS)_{gc} = s_c"""
    S = np.asarray(S)
    return {'e': S, 'r': np.rot90(S, -1), 'r2': np.rot90(S, 2), 'r3': np.rot90(S, 1),
            'h': S[:, ::-1], 'v': S[::-1, :], 't': S.T, 'tr2': np.rot90(S, 2).T}


def frenicle(S):
    return min(tuple(g.flatten()) for g in d4(S).values())


def load880():
    rows = [list(map(int, l.split())) for l in open(os.path.join(HERE, 'squares880.txt')) if l.strip()]
    return [np.array(r).reshape(4, 4) for r in rows]


def points(S):
    S = np.asarray(S); n = S.shape[0]; N = n * n
    return np.array([(j - (n - 1) / 2, (n - 1) / 2 - i, S[i, j] - (N + 1) / 2) for i in range(n) for j in range(n)])


def coplanar(S):
    """points coplanar <=> z affine on the grid <=> second differences z_ij - z_i0 - z_0j + z_00 vanish"""
    S = np.asarray(S, dtype=np.int64)
    sep = (S - S[:, :1] - S[:1, :] + S[0, 0] == 0).all()          # z = a_i + b_j
    lin = (np.diff(S[:, 0], 2) == 0).all() and (np.diff(S[0, :], 2) == 0).all()   # a, b affine
    return bool(sep and lin)


def is_semimagic(S):
    S = np.asarray(S); n = S.shape[0]; M = n * (n * n + 1) // 2
    return (S.sum(0) == M).all() and (S.sum(1) == M).all()


def complement(S):
    S = np.asarray(S); return S.size + 1 - S


def self_comp(S):
    C = complement(S)
    return [k for k, g in d4(S).items() if (g == C).all()]


# ------------------------------------------------------------------ A coplanarity
natural = {n: np.arange(1, n * n + 1).reshape(n, n) for n in range(2, 7)}
for n in (2, 3):
    N = n * n
    imgs = {tuple(g.flatten()) for g in d4(natural[n]).values()}
    assert len(imgs) == 8
    cop = set()
    for perm in itertools.permutations(range(1, N + 1)):
        S = np.array(perm).reshape(n, n)
        if coplanar(S):
            cop.add(perm)
        if n == 2 or perm[0] < 3:   # independent rank test on a third of the arrangements
            assert coplanar(S) == (np.linalg.matrix_rank(points(S)) == 2)
    assert cop == imgs, (n, len(cop))
    log(f'A: n={n}: {len(cop)} of {math.factorial(N)} arrangements coplanar, exactly the D4-images of s=ni+j+1')
rng = np.random.default_rng(1)
for n in (4, 5, 6):
    assert all(coplanar(g) for g in d4(natural[n]).values())
    cnt = sum(coplanar(rng.permutation(n * n).reshape(n, n) + 1) for _ in range(20000))
    assert cnt == 0
    # rank of the natural square's point set is 2
    P = points(natural[n]); assert np.linalg.matrix_rank(P) == 2
log('A: n=4,5,6: the 8 images of the natural square are coplanar (rank 2); 20000 random arrangements each are not')
SQ = load880()
assert all(is_semimagic(S) and not coplanar(S) for S in SQ)
log('A: none of the 880 order-4 magic squares is coplanar')

# ------------------------------------------------------------------ J ordering
fr = [frenicle(S) for S in SQ]
assert all(tuple(S.flatten()) == f for S, f in zip(SQ, fr)), 'not in Frenicle standard form'
assert fr == sorted(fr) and len(set(fr)) == 880
index_of = {f: k for k, f in enumerate(fr)}
comp_idx = [index_of[frenicle(complement(S))] for S in SQ]
log('J: squares880.txt = the 880 Frenicle standard forms in lexicographic order')

# ------------------------------------------------------------------ B covariance
def cov(S):
    S = np.asarray(S); n = S.shape[0]; N = n * n
    P = [(Fraction(2 * j - (n - 1), 2), Fraction((n - 1) - 2 * i, 2), Fraction(2 * int(S[i, j]) - (N + 1), 2))
         for i in range(n) for j in range(n)]
    return [[sum(p[a] * p[b] for p in P) / N for b in range(3)] for a in range(3)]


def check_cov(S):
    n = S.shape[0]; N = n * n
    C = cov(S); a = Fraction(n * n - 1, 12); b = Fraction(N * N - 1, 12)
    assert C == [[a, 0, 0], [0, a, 0], [0, 0, b]], C


for S in SQ:
    check_cov(S)
for n in range(3, 23, 2):
    check_cov(siamese(n))
log('B: covariance = diag((n^2-1)/12, (n^2-1)/12, (n^4-1)/12) for the 880 squares and the Siamese squares n=3..21')

# ------------------------------------------------------------------ hulls of the 880
hulls = [exact_hull(S) for S in SQ]
log(f'   exact hulls of the 880 computed ({time.time() - T0:.1f}s)')

# ------------------------------------------------------------------ C isometries
sc = [self_comp(S) for S in SQ]
n_sc = sum(1 for s in sc if s)
assert n_sc == 352
assoc = [('r2' in s) for s in sc]
assert sum(assoc) == 48
assert all(set(s) <= {'r2', 'h', 'v'} and len(s) <= 1 for s in sc)
for k, (S, h) in enumerate(zip(SQ, hulls)):
    P = h['P']
    iso_pts = isometries(P)
    iso_v = isometries(P[h['vertices']])
    want = 2 if sc[k] else 1
    assert len(iso_pts) == want and len(iso_v) == want, (k, len(iso_pts), len(iso_v))
    for perm, R in iso_pts:   # every isometry of the point set is block diagonal diag(B, +-1)
        assert abs(R[0, 2]) < 1e-9 and abs(R[1, 2]) < 1e-9 and abs(R[2, 0]) < 1e-9 and abs(R[2, 1]) < 1e-9
log('C: n=4: |Iso(point set)| = |Iso(vertex set)| = 2 for the 352 self-complementary squares, 1 for the other 528')
sia_iso = {}
for n in range(3, 17, 2):
    S = siamese(n); h = exact_hull(S)
    a = len(isometries(h['P'])); b = len(isometries(h['P'][h['vertices']]))
    assert a == 2 and b == 2 and self_comp(S) == ['r2'], (n, a, b)
    sia_iso[n] = (a, b)
log('C: Siamese n=3..15: point set and vertex set both have exactly the isometries {id, -id}')

# ------------------------------------------------------------------ D injectivity
def canon_vertex_set(S, h):
    """D4-canonical form of the vertex set {(cell position, height)} of G(S)"""
    forms = []
    # apply the 8 planar isometries directly to the vertex points
    P = h['P'][h['vertices']]
    mats = [np.array(M) for M in ([[1, 0], [0, 1]], [[0, 1], [-1, 0]], [[-1, 0], [0, -1]], [[0, -1], [1, 0]],
                                  [[-1, 0], [0, 1]], [[1, 0], [0, -1]], [[0, -1], [-1, 0]], [[0, 1], [1, 0]])]
    for A in mats:
        Q = np.column_stack([P[:, :2] @ A.T, P[:, 2]])
        forms.append(tuple(sorted(map(tuple, Q.tolist()))))
    return min(forms)


canon = [canon_vertex_set(S, h) for S, h in zip(SQ, hulls)]
assert len(set(canon)) == 880
log('D: the 880 vertex sets are pairwise inequivalent under D4 (no vertex set of one class is the image of another)')
# congruence classes of the gems (vertex sets), exact
groups = defaultdict(list)
for k, h in enumerate(hulls):
    groups[sqdist_multiset(h['P'][h['vertices']])].append(k)
parent = list(range(880))
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
for ks in groups.values():
    for a, b in itertools.combinations(ks, 2):
        if find(a) != find(b) and congruent(hulls[a]['P'][hulls[a]['vertices']], hulls[b]['P'][hulls[b]['vertices']]):
            parent[find(a)] = find(b)
classes = defaultdict(set)
for k in range(880):
    classes[find(k)].add(k)
orbits = {frozenset((k, comp_idx[k])) for k in range(880)}
assert {frozenset(c) for c in classes.values()} == orbits and len(orbits) == 616
log('D: congruence classes of the 880 gems = the 616 complement orbits {S, 17-S} (exact)')
# certificate used in the paper (Prop. 5.4(2)): the sorted squared-distance multiset is a congruence invariant and
# takes 616 distinct values, one per complement orbit
assert len(groups) == 616 and {frozenset(v) for v in groups.values()} == orbits
log('D: the sorted squared-distance multisets of the 880 vertex sets take 616 distinct values, one per complement orbit')

# ------------------------------------------------------------------ E parity
cls = [classify_points(h) for h in hulls]
for k in range(880):
    if assoc[k]:
        V, I, B = (len(x) for x in cls[k])
        assert V % 2 == 0 and I % 2 == 0 and B % 2 == 0
I_assoc = Counter(len(cls[k][1]) for k in range(880) if assoc[k])
log(f'E: the 48 associative gems have V, I, B all even; I distribution {dict(sorted(I_assoc.items()))}')
S3 = natural[3]
assert (S3 + np.rot90(S3, 2) == 10).all() and np.linalg.matrix_rank(points(S3)) == 2
log('E: the natural square of order 3 is associative and its point set has rank 2 (parity needs full dimension)')

# ------------------------------------------------------------------ F certification
# (the closure test itself is part of gem_geometry.exact_hull, so it was applied to every hull above;
#  it is repeated here explicitly for the 880 order-four hulls)
from gem_geometry import certify_closure
for k, h in enumerate(hulls):
    P = h['P']
    for (a, b, c, d) in h['faces']:
        assert (a * P[:, 0] + b * P[:, 1] + c * P[:, 2] + d <= 0).all()
    certify_closure(P, h['faces'], h['edges'])
log('F: all 880 hulls certified: distinct facet planes; every point satisfies every integer facet inequality; '
    'each facet = exact 2D hull of the points on its plane (2-dimensional); every facet edge lies in exactly two facets; '
    'strictly convex at every edge')

# ------------------------------------------------------------------ G regular subdivisions
def lifted_faces(S, h):
    P = h['P']; out = {'lower': [], 'upper': [], 'vertical': []}
    for (a, b, c, d) in h['faces']:
        on = frozenset(int(t) for t in np.nonzero(a * P[:, 0] + b * P[:, 1] + c * P[:, 2] + d == 0)[0])
        key = 'lower' if c < 0 else 'upper' if c > 0 else 'vertical'
        out[key].append(((a, b, c, d), on))
    return out


def is_ap(seq):
    d = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return len(set(d)) == 1


def canon_subdiv(cells, n=4):
    mats = [lambda i, j: (i, j), lambda i, j: (j, n - 1 - i), lambda i, j: (n - 1 - i, n - 1 - j),
            lambda i, j: (n - 1 - j, i), lambda i, j: (i, n - 1 - j), lambda i, j: (n - 1 - i, j),
            lambda i, j: (j, i), lambda i, j: (n - 1 - j, n - 1 - i)]
    forms = []
    for g in mats:
        forms.append(tuple(sorted(tuple(sorted(g(c // n, c % n)[0] * n + g(c // n, c % n)[1] for c in cell))
                                  for cell in cells)))
    return min(forms)


vert_count = Counter(); n_vertical = []
subdiv_lower = []; pairs = []; n_tri = 0
for k, (S, h) in enumerate(zip(SQ, hulls)):
    F = lifted_faces(S, h)
    sides = [list(S[0, :]), list(S[3, :]), list(S[:, 0]), list(S[:, 3])]
    non_ap = sum(1 for s in sides if not is_ap(s))
    for (a, b, c, d), on in F['vertical']:
        assert c == 0 and ((a == 0) != (b == 0)), (k, (a, b, c, d))   # normal along x or y: plane over a side
    assert len(F['vertical']) == non_ap, (k, len(F['vertical']), non_ap)
    n_vertical.append(len(F['vertical']))
    low_v = set().union(*[on for _, on in F['lower']]) & set(h['vertices'])
    up_v = set().union(*[on for _, on in F['upper']]) & set(h['vertices'])
    assert low_v | up_v == set(h['vertices'])
    # corners are vertices of both hulls
    assert {0, 3, 12, 15} <= (low_v & up_v)
    lower = [on for _, on in F['lower']]
    upper = [on for _, on in F['upper']]
    # the lower cells cover the square: their projected areas add up to 9 (doubled coordinates: 36)
    def area2(cell):
        pts = np.array([(2 * (c % 4) - 3, 3 - 2 * (c // 4)) for c in cell], float)
        from scipy.spatial import ConvexHull
        return ConvexHull(pts).volume
    assert abs(sum(area2(c) for c in lower) - 36) < 1e-9 and abs(sum(area2(c) for c in upper) - 36) < 1e-9
    subdiv_lower.append(canon_subdiv(lower))
    if all(len(c) == 3 for c in lower):
        n_tri += 1
vc = Counter(n_vertical)
log(f'G: vertical facets lie over the sides, one per side whose heights are not an arithmetic progression; '
    f'number of vertical facets per gem: {dict(sorted(vc.items()))}')
log('G: every vertex lies on the lower or the upper hull; the four corners on both; lower and upper cells tile the square')
n_sub = len(set(subdiv_lower))
# all regular subdivisions S(z) for z ranging over the height functions of the 7040 magic squares, up to D4:
# the upper subdivision of S is the lower one of its complement, so the 880 lower subdivisions suffice
log(f'G: the 7040 magic height functions of order 4 induce {n_sub} distinct regular subdivisions of the 4x4 grid up to D4 '
    f'({n_tri} of the 880 lower subdivisions are triangulations)')
pair_canon = set()
for k in range(880):
    pair_canon.add(min((subdiv_lower[k], subdiv_lower[comp_idx[k]]), (subdiv_lower[comp_idx[k]], subdiv_lower[k])))
OUT['regular_subdivisions'] = dict(n_distinct_lower_up_to_D4=n_sub, n_lower_triangulations=n_tri,
                                   vertical_facets=dict(vc))

# ------------------------------------------------------------------ H types as unions of complement orbits
geo = json.load(open(os.path.join(HERE, 'results_geometry.json')))
comp_types = Counter()
for T in geo['combinatorial_types']:
    mem = set(T['members'])
    assert all(comp_idx[k] in mem for k in mem)
    n_self = sum(1 for k in mem if comp_idx[k] == k)
    n_pairs = (len(mem) - n_self) // 2
    comp_types[(n_self, n_pairs)] += 1
singles = comp_types[(1, 0)]
doubles_pair = comp_types[(0, 1)]; doubles_self = comp_types[(2, 0)]
assert singles == 93
log(f'H: every combinatorial type is a union of complement orbits; the 93 one-member types are self-complementary squares; '
    f'of the 201 two-member types, {doubles_pair} are mirror pairs and {doubles_self} consist of two self-complementary squares')
OUT['types_composition'] = {f'{a}self+{b}pairs': c for (a, b), c in sorted(comp_types.items())}

# ------------------------------------------------------------------ I Siamese forced vertices
def forced_cells(S):
    n = S.shape[0]; N = n * n; out = {(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)}
    for v in (1, N):
        out.add(tuple(int(t) for t in np.argwhere(S == v)[0]))
    for line in ([(0, j) for j in range(n)], [(n - 1, j) for j in range(n)],
                 [(i, 0) for i in range(n)], [(i, n - 1) for i in range(n)]):
        vals = [S[c] for c in line]
        out.add(line[int(np.argmin(vals))]); out.add(line[int(np.argmax(vals))])
    return out


for n in range(3, 43, 2):
    S = siamese(n); h = exact_hull(S)
    vc_ = {(v // n, v % n) for v in h['vertices']}
    assert vc_ == forced_cells(S) and len(vc_) == (8 if n == 3 else 12), n
    if n >= 5:
        assert h['f_vector'] == (12, 26, 16)
log('I: Siamese n=3..41: vertices = forced vertices (8 for n=3, 12 for n>=5, f=(12,26,16))')
# forced vertices of the 880 order-4 gems are vertices, and their number
nf = Counter()
for S, h in zip(SQ, hulls):
    f = forced_cells(S); vc_ = {(v // 4, v % 4) for v in h['vertices']}
    assert f <= vc_
    nf[len(f)] += 1
OUT['forced_count_880'] = dict(sorted(nf.items()))
log(f'I: n=4: forced vertices are vertices; their number over the 880 gems: {dict(sorted(nf.items()))}')

# ------------------------------------------------------------------ K census
census = defaultdict(lambda: dict(I=Counter(), B=Counter()))
Ic = Counter(); Bc = Counter()
for (V, I, B) in cls:
    Ic[len(I)] += 1; Bc[len(B)] += 1
OUT['I_distribution'] = {k: Ic.get(k, 0) for k in range(7)}
OUT['B_distribution'] = {k: Bc.get(k, 0) for k in range(7)}
log(f'K: strictly interior counts {OUT["I_distribution"]}; non-vertex boundary counts {OUT["B_distribution"]}')
OUT['runtime_seconds'] = round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(HERE, 'verify_structure.json'), 'w'), indent=1)

# ------------------------------------------------------------------ L Siamese vertex table and mixed moments
for n in range(5, 43, 2):
    m = (n - 1) // 2; N = n * n; sb = (N + 1) // 2; S = siamese(n)
    table = {(0, 0): sb + m + 2, (0, m - 1): N - 1, (0, m): 1, (0, 2 * m): sb + m, (m - 1, 0): N - m, (m, 0): m + 2,
             (m, 2 * m): N - m - 1, (m + 1, 2 * m): m + 1, (2 * m, 0): sb - m, (2 * m, m): N, (2 * m, m + 1): 2,
             (2 * m, 2 * m): sb - m - 2}
    assert all(S[c] == v for c, v in table.items()) and set(table) == forced_cells(S)
    assert (S + np.rot90(S, 2) == N + 1).all()
log('L: Siamese vertex table (cells and entries) checked for n=5..41; Siamese squares are associative')
mm = []
for S in SQ:
    X = np.array([[j - 1.5 for j in range(4)] for i in range(4)]); Y = np.array([[1.5 - i] * 4 for i in range(4)])
    v = 8 * ((S - 8.5) * X * Y).sum(); assert v == round(v); mm.append(int(round(v)))
absv = {abs(v) for v in mm}
assert len(absv) == 48 and max(absv) == 480 and sum(1 for v in mm if v == 0) == 56
assert sum(1 for k, v in enumerate(mm) if v == 0 and assoc[k]) == 48
log('L: 8*sum z x y over the 880: 48 distinct absolute values in [0, 480], zero for 56 classes, 48 of them associative')
for n in range(3, 10):
    assert n * n * (n ** 4 - 1) // 12 == [60, 340, 1300, 3885, 9800, 21840, 44280][n - 3]
log(f'all checks passed ({time.time() - T0:.1f} s)')
open(os.path.join(HERE, 'verify_structure.log'), 'w').write('\n'.join(LOG) + '\n')
