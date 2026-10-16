"""
digit_exchanged_slacks.py -- proof data for the gem of the digit-exchanged square (Proposition 6.5 of the paper)
    s'(i,j) = n<i+2j-2m> + <i+j-m> + 1,   n = 2m+1,
by the five-level shear of the Siamese theorem (Theorem 6.4), with a generic slack certificate that is also re-applied
to the Siamese square as a cross-check of siamese_slacks.py.

With x = j-m, y = m-i, l1 = x-y+m, l2 = 2x-y+m:  s' = n<l2> + <l1> + 1, so z = lambda'(x,y) + n zeta' with the affine
lambda' = n l2 + l1 + 1 - (N+1)/2 and zeta' = -n floor(l2/n) - floor(l1/n).  The floors are those of the Siamese
proof with l1, l2 exchanged, so zeta' is constant on the same five level polygons Lambda_{+2}, ..., Lambda_{-2}, now
with heights n+1, n, 0, -n, -(n+1) (Siamese: n+1, 1, 0, -1, -(n+1)).  The hull of the sheared points is the hull of
the 16 polygon vertices q1..q16.  For the 7 inequalities below and their images under -id we assert, as
polynomials in m (sympy, exact):
  * every slack at q1..q16 is identically 0 or positive for all integers m >= 2 (non-negative coefficients of
    p(2+t) and p(2) > 0);
  * the 14 facets (7 listed + antipodes) form a closed surface, (V,E,F) = (12,24,14), 8 triangles + 6 quadrilaterals;
  * the 14 planes are pairwise distinct; each facet is 2-dimensional and its listed cycle is the strictly convex
    polygon of all incident points; the surface is strictly convex across all 24 edges;
  * the isometry group of the gem is {id, -id} for every m >= 2 (distinct squared norms of the six antipodal vertex
    pairs, and non-zero inner products with one vertex);
  * numerically, for n = 5..61, the sheared point set of s' has exactly the five level sets claimed, and all its
    points satisfy the 14 inequalities.
Writes digit_exchanged_slacks.tex (table in Appendix A of the paper) and digit_exchanged_slacks.log.
"""
import os, itertools
from collections import Counter
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
m, t = sp.symbols('m t')
n = 2 * m + 1
LOG = []


def log(s):
    print(s, flush=True); LOG.append(s)


def level_points(h1):
    """the 16 vertices of the five level polygons, with heights n+1, h1, 0, -h1, -(n+1)"""
    return {
        'q1': (-m, m, n + 1), 'q2': (-1, m, n + 1), 'q3': (-m, 1, n + 1),            # Lambda_{+2}
        'q4': (-m, 0, h1), 'q13': (-m, 1 - m, h1), 'q14': (-1, m - 1, h1),            # Lambda_{+1}
        'q5': (-m, -m, 0), 'q6': (0, -m, 0), 'q7': (0, m, 0), 'q8': (m, m, 0),       # Lambda_0
        'q9': (m, 0, -h1), 'q15': (m, m - 1, -h1), 'q16': (1, 1 - m, -h1),            # Lambda_{-1}
        'q10': (m, -m, -(n + 1)), 'q11': (m, -1, -(n + 1)), 'q12': (1, -m, -(n + 1)),  # Lambda_{-2}
    }


ORDER = ['q1', 'q2', 'q3', 'q4', 'q13', 'q14', 'q5', 'q6', 'q7', 'q8', 'q9', 'q15', 'q16', 'q10', 'q11', 'q12']
NEG = {'q1': 'q10', 'q2': 'q12', 'q3': 'q11', 'q4': 'q9', 'q13': 'q15', 'q14': 'q16', 'q5': 'q8', 'q6': 'q7'}
NEG.update({b: a for a, b in list(NEG.items())})


def pos(p):
    """p is a polynomial in m that is > 0 for every integer m >= 2 (certificate: coefficients of p(2+t) >= 0, p(2) > 0)"""
    p = sp.expand(p)
    if p == 0:
        return False
    q = sp.Poly(sp.expand(p.subs(m, 2 + t)), t)
    return all(c >= 0 for c in q.all_coeffs()) and q.eval(0) > 0


def certify(P, INEQ, FACETS, fvec, nsizes):
    """generic version of the certificate of siamese_slacks.py; returns (slack table rows, vertex names, all facets)"""
    for a, b in NEG.items():
        assert all(sp.expand(P[a][k] + P[b][k]) == 0 for k in range(3)), (a, b)
    FAC = {str(k): (a, b, FACETS[k]) for k, (a, b) in INEQ.items()}
    FAC.update({f"{k}'": (tuple(-c for c in a), b, [NEG[v] for v in FACETS[k]]) for k, (a, b) in INEQ.items()})
    slack = lambda f, q: sp.expand(FAC[f][1] - sum(FAC[f][0][i] * P[q][i] for i in range(3)))
    rows = {q: [slack(str(k), q) for k in INEQ] for q in ORDER}
    # every slack is 0 or positive for all m >= 2 (for (k') this is (k) at -q)
    for f in FAC:
        assert all(slack(f, q) == 0 or pos(slack(f, q)) for q in ORDER), f
    verts = {v for c in FAC.values() for v in c[2]}
    # closed surface
    EF = {}
    for f, (a, b, cyc) in FAC.items():
        for i in range(len(cyc)):
            EF.setdefault(frozenset((cyc[i], cyc[(i + 1) % len(cyc)])), []).append(f)
    assert all(len(x) == 2 for x in EF.values())
    assert (len(verts), len(EF), len(FAC)) == fvec, (len(verts), len(EF), len(FAC))
    assert Counter(len(c[2]) for c in FAC.values()) == Counter(nsizes)
    INC = {f: [q for q in ORDER if slack(f, q) == 0] for f in FAC}
    sub = lambda u, v: [sp.expand(u[i] - v[i]) for i in range(3)]
    cross = lambda u, v: [sp.expand(u[1] * v[2] - u[2] * v[1]), sp.expand(u[2] * v[0] - u[0] * v[2]),
                          sp.expand(u[0] * v[1] - u[1] * v[0])]
    dot = lambda u, v: sp.expand(sum(u[i] * v[i] for i in range(3)))
    # pairwise distinct planes
    for f, g in itertools.combinations(FAC, 2):
        assert any(slack(f, q) == 0 and pos(slack(g, q)) for q in ORDER), (f, g)
    # each facet 2-dimensional; listed cycle = strictly convex polygon of all incident level-polygon vertices
    nonvert = set()
    for f, (a, b, cyc) in FAC.items():
        assert set(cyc) <= set(INC[f]) and not (set(INC[f]) - set(cyc)) & verts, f
        c0 = cross(sub(P[cyc[1]], P[cyc[0]]), sub(P[cyc[2]], P[cyc[0]]))
        assert any(pos(c) or pos(-c) for c in c0), f
        sgn = 1 if pos(dot(a, c0)) else -1
        assert pos(sgn * dot(a, c0)), f
        for i in range(len(cyc)):
            u, v = P[cyc[i]], P[cyc[(i + 1) % len(cyc)]]
            for w in INC[f]:
                if w in (cyc[i], cyc[(i + 1) % len(cyc)]):
                    continue
                o = dot(a, cross(sub(v, u), sub(P[w], u)))
                if w in cyc or o != 0:
                    assert pos(sgn * o), (f, cyc[i], w, o)
                else:
                    assert pos(dot(sub(P[w], u), sub(v, u))) and pos(dot(sub(P[w], v), sub(u, v))), (f, w)
        nonvert |= {(f, w) for w in set(INC[f]) - set(cyc)}
    # strict convexity across every edge
    for e, (f, g) in EF.items():
        for f1, g1 in ((f, g), (g, f)):
            assert all(pos(slack(g1, q)) for q in FAC[f1][2] if q not in e), (e, f1, g1)
    return rows, verts, FAC, sorted(nonvert)


def zeta_points(nn, exchanged):
    mm = (nn - 1) // 2; out = []
    for i in range(nn):
        for j in range(nn):
            x, y = j - mm, mm - i; l1, l2 = x - y + mm, 2 * x - y + mm
            out.append((x, y, -nn * (l2 // nn) - (l1 // nn)) if exchanged else (x, y, -nn * (l1 // nn) - (l2 // nn)))
    return np.array(out)


# ---------------------------------------------------------------- cross-check: the Siamese square (Table 5)
INEQ_S = {
    1: ((0, 0, 1), 2 * m + 2), 2: ((0, 1, 0), m), 3: ((-1, 0, 0), m),
    4: ((-2 * (m + 1), 2 * m + 1, -m), m * (2 * m + 1)),
    5: ((2 * (m + 1), -2 * (m + 1), 2 * m + 1), 2 * m * (m + 1)),
    6: ((2 * m * (m + 2), -(2 * m**2 + 2 * m - 1), m * (2 * m + 1)), m * (2 * m**2 + 2 * m - 1)),
    7: ((2 * m, -1, m), m * (2 * m - 1)), 8: ((0, -2, 1), 2 * m)}
FACETS_S = {1: ['q1', 'q2', 'q3'], 2: ['q1', 'q2', 'q8', 'q7'], 3: ['q1', 'q3', 'q5', 'q4'], 4: ['q1', 'q4', 'q7'],
            5: ['q2', 'q3', 'q6'], 6: ['q2', 'q6', 'q9'], 7: ['q2', 'q8', 'q9'], 8: ['q3', 'q5', 'q6']}
certify(level_points(sp.Integer(1)), INEQ_S, FACETS_S, (12, 26, 16), {3: 12, 4: 4})
log('Siamese square: the generic certificate reproduces Theorem 6.4 (f = (12,26,16)) for every m >= 2')

# ---------------------------------------------------------------- the digit-exchanged square
P = level_points(n)
INEQ = {
    1: ((0, 0, 1), 2 * m + 2),                                   # top level
    2: ((0, 1, 0), m),                                           # vertical, over the top row
    3: ((-1, 0, 0), m),                                          # vertical, over the left column
    4: ((-2 * (m + 1), m + 1, -m), m * (m + 1)),
    5: ((1, -1, m), (2 * m - 1) * (m + 1)),
    6: ((2, -1, 1), m),
    7: ((0, -(2 * m + 1), 1), m * (2 * m + 1)),
}
FACETS = {1: ['q1', 'q2', 'q3'], 2: ['q1', 'q2', 'q8', 'q7'], 3: ['q1', 'q3', 'q13', 'q5'], 4: ['q1', 'q5', 'q7'],
          5: ['q2', 'q3', 'q13'], 6: ['q2', 'q13', 'q6', 'q8'], 7: ['q13', 'q5', 'q6']}
rows, verts, FAC, nonvert = certify(P, INEQ, FACETS, (12, 24, 14), {3: 8, 4: 6})
VERTS = ['q1', 'q2', 'q3', 'q13', 'q5', 'q6', 'q7', 'q8', 'q15', 'q10', 'q11', 'q12']
assert verts == set(VERTS)
log("digit-exchanged square s': 14 facets (7 listed and their antipodes), f = (12,24,14), 8 triangles and 6 "
    "quadrilaterals; all non-zero slacks > 0 for every integer m >= 2; planes pairwise distinct, facets 2-dimensional "
    "and strictly convex, surface strictly convex across all 24 edges")
log(f'  non-vertex incidences (point on a facet plane, not a vertex): {nonvert}')
for k in INEQ:
    log(f'  ({k}) {INEQ[k][0]} . (x,y,zeta) <= {INEQ[k][1]}: tight at {[q for q in ORDER if rows[q][k - 1] == 0]}')

# hand-checkable cyclic order of the quadrilaterals (3) and (6) quoted in the paper: the turns
# (b-a) x (c-b) of consecutive triples, in the coordinates (y, zeta') on the plane x = -m and (x, y) for (6)
def turns(pts):
    k = len(pts)
    return [sp.factor(sp.expand((pts[(i + 1) % k][0] - pts[i][0]) * (pts[(i + 2) % k][1] - pts[(i + 1) % k][1])
                                - (pts[(i + 1) % k][1] - pts[i][1]) * (pts[(i + 2) % k][0] - pts[(i + 1) % k][0])))
            for i in range(k)]
T3 = turns([(P[q][1], P[q][2]) for q in ['q1', 'q3', 'q13', 'q5']])
T6 = turns([(P[q][0], P[q][1]) for q in ['q2', 'q13', 'q6', 'q8']])
assert all(pos(-t) for t in T3) or all(pos(t) for t in T3)
assert all(pos(t) for t in T6)
log(f'  turns of (3) q1 q3 q13 q5 in (y, zeta): {T3}; of (6) q2 q13 q6 q8 in (x, y): {T6}')

# vertex cells and entries in the original square: cell (i,j) = (m-y, x+m)
cell = {q: (sp.expand(m - P[q][1]), sp.expand(P[q][0] + m)) for q in VERTS}
log('  vertex cells (i,j): ' + ', '.join(f'{q}:{cell[q]}' for q in VERTS))

# ---------------------------------------------------------------- isometry group {id, -id}, all m >= 2
# original coordinates: z = lambda'(x,y) + n zeta', lambda' = n l2 + l1 + 1 - (N+1)/2
lam = lambda x, y: n * (2 * x - y + m) + (x - y + m) + 1 - (n**2 + 1) / sp.Integer(2)
Z = {v: (P[v][0], P[v][1], sp.expand(lam(P[v][0], P[v][1]) + n * P[v][2])) for v in VERTS}
for v in VERTS:
    assert all(sp.expand(Z[v][k] + Z[NEG[v]][k]) == 0 for k in range(3))      # the vertex set is centrally symmetric
reps = ['q1', 'q2', 'q3', 'q13', 'q5', 'q6']
norms = {v: sp.expand(sum(c**2 for c in Z[v])) for v in reps}
for a, b in itertools.combinations(reps, 2):
    d = sp.Poly(norms[a] - norms[b], m)
    assert not [r for r in d.all_roots() if r.is_integer and r >= 2], (a, b)
for v in reps[1:]:
    d = sp.Poly(sp.expand(sum(p * q for p, q in zip(Z['q1'], Z[v]))), m)
    assert not [r for r in d.all_roots() if r.is_integer and r >= 2], v
log('  isometry group {id, -id} for every m >= 2: squared norms of the six antipodal vertex pairs ' +
    ', '.join(f'{v}: {sp.factor(norms[v])}' for v in reps) +
    '; inner products with q1 ' + ', '.join(str(sp.factor(sp.expand(sum(p * q for p, q in zip(Z['q1'], Z[v]))))) for v in reps[1:]))

# ---------------------------------------------------------------- numerical cross-checks on the actual squares
import sys
sys.path.insert(0, HERE)
for nn in range(5, 63, 2):
    mm = (nn - 1) // 2
    I, J = np.indices((nn, nn))
    S = nn * ((I + 2 * J - 2 * mm) % nn) + ((I + J - mm) % nn) + 1
    N = nn * nn; M = nn * (N + 1) // 2
    assert sorted(S.ravel()) == list(range(1, N + 1)) and (S.sum(0) == M).all() and (S.sum(1) == M).all() \
        and np.trace(S) == M and np.trace(S[:, ::-1]) == M
    Zp = zeta_points(nn, exchanged=True)
    # z = lambda' + n zeta' exactly
    x, y = Zp[:, 0], Zp[:, 1]
    lamv = nn * (2 * x - y + mm) + (x - y + mm) + 1
    assert (2 * (lamv + nn * Zp[:, 2]) == 2 * S[mm - y, x + mm]).all()
    # level sets = lattice points of the five polygons
    lev = {nn + 1: lambda x, y: y >= x + mm + 1, nn: lambda x, y: (2 * x + mm + 1 <= y) & (y <= x + mm),
           0: lambda x, y: abs(y - 2 * x) <= mm, -nn: lambda x, y: (2 * x - mm - 1 >= y) & (y >= x - mm),
           -(nn + 1): lambda x, y: y <= x - mm - 1}
    for h, f in lev.items():
        assert ((Zp[:, 2] == h) == f(x, y)).all(), (nn, h)
    for f, (a, b, cyc) in FAC.items():
        av = np.array([int(sp.sympify(c).subs(m, mm)) for c in a]); bv = int(sp.sympify(b).subs(m, mm))
        assert (Zp @ av <= bv).all(), (nn, f)
    # the entries at the twelve vertex cells quoted in the paper, and which of these cells are forced vertices
    ent = {(0, 0): nn + mm + 2, (0, mm - 1): N - nn, (0, mm): 1, (0, 2 * mm): N - nn + mm + 1, (1, 2 * mm): mm + 2,
           (mm - 1, 0): nn * (mm + 1), (mm + 1, 2 * mm): nn * mm + 1, (2 * mm - 1, 0): N - nn + mm, (2 * mm, 0): mm + 1,
           (2 * mm, mm): N, (2 * mm, mm + 1): nn + 1, (2 * mm, 2 * mm): N - 2 * nn + mm}
    assert set(ent) == {(int(sp.sympify(cell[q][0]).subs(m, mm)), int(sp.sympify(cell[q][1]).subs(m, mm))) for q in VERTS}
    assert all(S[c] == v for c, v in ent.items()), nn
    sides = [[(0, j) for j in range(nn)], [(nn - 1, j) for j in range(nn)], [(i, 0) for i in range(nn)], [(i, nn - 1) for i in range(nn)]]
    forced = {(0, 0), (0, nn - 1), (nn - 1, 0), (nn - 1, nn - 1)} | {min(e, key=lambda c: S[c]) for e in sides} \
        | {max(e, key=lambda c: S[c]) for e in sides}
    assert forced == {(0, 0), (0, 2 * mm), (2 * mm, 0), (2 * mm, 2 * mm), (0, mm), (2 * mm, mm), (1, 2 * mm), (2 * mm - 1, 0)}, nn
log("numerical: for n = 5..61, s' is magic, z = lambda' + n zeta' with the five claimed level sets, every point "
    "satisfies the 14 inequalities, the entries at the twelve vertex cells are those of the paper, and the forced "
    "vertices are the corners and the cells (0,m), (2m,m), (1,2m), (2m-1,0)")

# ---------------------------------------------------------------- LaTeX table (Appendix A)
def fmt(p):
    p = sp.expand(p)
    if p == 0:
        return r'\mathbf{0}'
    return sp.latex(sp.factor(p)).replace(r'\left(', '(').replace(r'\right)', ')').replace(' ', '')


lines = [r'\begin{tabular}{l l ccccccc}', r'\toprule',
         r'point & $(x,y,\zeta^\prime)$ & (1) & (2) & (3) & (4) & (5) & (6) & (7)\\', r'\midrule']
for name in ORDER:
    p = P[name]
    coords = '(' + ','.join(sp.latex(sp.expand(c)).replace(' ', '') for c in p) + ')'
    cells = ' & '.join('$' + fmt(s) + '$' for s in rows[name])
    lines.append(f'$q_{{{name[1:]}}}$ & ${coords}$ & {cells}\\\\')
    if name in ('q3', 'q14', 'q8', 'q16'):
        lines.append(r'\addlinespace[2pt]')
lines += [r'\bottomrule', r'\end{tabular}']
with open(os.path.join(HERE, 'digit_exchanged_slacks.tex'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
with open(os.path.join(HERE, 'digit_exchanged_slacks.log'), 'w') as f:
    f.write('\n'.join(LOG) + '\n')
