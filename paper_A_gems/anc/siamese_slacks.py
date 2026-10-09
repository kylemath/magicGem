"""
siamese_slacks.py -- the hand-checkable form of the Siamese theorem (Section 6, Table 3 of the paper).

For n = 2m+1, after the shear (x,y,z) -> (x,y,zeta) the lifted points lie on five level
polygons Lambda_{+2}, Lambda_{+1}, Lambda_0, Lambda_{-1}, Lambda_{-2} with 16 polygon vertices q1..q16 in total.
For the eight inequalities a.(x,y,zeta) <= b printed in the paper we compute the slack b - a.p
at each of the 16 level-polygon vertices p as a polynomial in m (sympy, exact), and assert:
  * the slack is identically 0 exactly for the incidences listed in the paper,
  * every other slack is a polynomial that is > 0 for all integers m >= 2
    (certified by non-negative coefficients after the substitution m = 2 + t, constant term > 0),
  * the 16 facets (8 listed + their images under -id) form a closed surface: every edge of every
    facet polygon lies in exactly two facets, (V,E,F) = (12,26,16).
By central symmetry of the set of level-polygon vertices, checking (k) at all 16 points also checks (k') = -(k).
Writes siamese_slacks.tex (the table printed in the paper) and siamese_slacks.log.
"""
import os, itertools
from collections import Counter
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
m, t = sp.symbols('m t')
n = 2 * m + 1

# the 16 vertices of the level polygons (x, y, zeta); q1..q12 are the forced vertices (the claimed gem vertices),
# q13..q16 are the other four polygon vertices
P = {
    'q1': (-m, m, n + 1), 'q2': (-1, m, n + 1), 'q3': (-m, 1, n + 1),       # Lambda_{+2}
    'q4': (-m, 0, 1), 'q13': (-m, 1 - m, 1), 'q14': (-1, m - 1, 1),            # Lambda_{+1}
    'q5': (-m, -m, 0), 'q6': (0, -m, 0), 'q7': (0, m, 0), 'q8': (m, m, 0),  # Lambda_0
    'q9': (m, 0, -1), 'q15': (m, m - 1, -1), 'q16': (1, 1 - m, -1),            # Lambda_{-1} = -Lambda_{+1}
    'q10': (m, -m, -(n + 1)), 'q11': (m, -1, -(n + 1)), 'q12': (1, -m, -(n + 1)),  # Lambda_{-2}
}
ORDER = ['q1', 'q2', 'q3', 'q4', 'q13', 'q14', 'q5', 'q6', 'q7', 'q8', 'q9', 'q15', 'q16', 'q10', 'q11', 'q12']
NEG = {'q1': 'q10', 'q2': 'q12', 'q3': 'q11', 'q4': 'q9', 'q13': 'q15', 'q14': 'q16',
       'q5': 'q8', 'q6': 'q7'}
NEG.update({b: a for a, b in list(NEG.items())})
for a, b in NEG.items():
    assert all(sp.expand(P[a][k] + P[b][k]) == 0 for k in range(3)), (a, b)

# the eight inequalities (normal a, right-hand side b): a . (x,y,zeta) <= b
INEQ = {
    1: ((0, 0, 1), 2 * m + 2),
    2: ((0, 1, 0), m),
    3: ((-1, 0, 0), m),
    4: ((-2 * (m + 1), 2 * m + 1, -m), m * (2 * m + 1)),
    5: ((2 * (m + 1), -2 * (m + 1), 2 * m + 1), 2 * m * (m + 1)),
    6: ((2 * m * (m + 2), -(2 * m**2 + 2 * m - 1), m * (2 * m + 1)), m * (2 * m**2 + 2 * m - 1)),
    7: ((2 * m, -1, m), m * (2 * m - 1)),
    8: ((0, -2, 1), 2 * m),
}
# claimed incidences (facet vertex cycles, in cyclic order)
FACETS = {1: ['q1', 'q2', 'q3'], 2: ['q1', 'q2', 'q8', 'q7'], 3: ['q1', 'q3', 'q5', 'q4'],
          4: ['q1', 'q4', 'q7'], 5: ['q2', 'q3', 'q6'], 6: ['q2', 'q6', 'q9'],
          7: ['q2', 'q8', 'q9'], 8: ['q3', 'q5', 'q6']}


def positive_for_m_ge_2(p):
    q = sp.Poly(sp.expand(p.subs(m, 2 + t)), t)
    cs = q.all_coeffs()
    return all(c >= 0 for c in cs) and q.eval(0) > 0


def fmt(p):
    p = sp.expand(p)
    if p == 0:
        return r'\mathbf{0}'
    return sp.latex(sp.factor(p)).replace(r'\left(', '(').replace(r'\right)', ')').replace(' ', '')


log = []
rows = {k: [] for k in ORDER}
for k, (a, b) in INEQ.items():
    on = []
    for name in ORDER:
        p = P[name]
        s = sp.expand(b - sum(a[i] * p[i] for i in range(3)))
        if s == 0:
            on.append(name)
        else:
            assert positive_for_m_ge_2(s), (k, name, s)
        rows[name].append(s)
    assert sorted(v for v in on if int(v[1:]) <= 12) == sorted(FACETS[k]), (k, on)
    log.append(f'({k}) tight at {on}')

# facets (k') = images under -id
all_facets = list(FACETS.values()) + [[NEG[v] for v in c] for c in FACETS.values()]
edges = Counter()
for c in all_facets:
    for i in range(len(c)):
        edges[frozenset((c[i], c[(i + 1) % len(c)]))] += 1
assert all(v == 2 for v in edges.values())
verts = {v for c in all_facets for v in c}
V, E, F = len(verts), len(edges), len(all_facets)
assert (V, E, F) == (12, 26, 16)
sizes = Counter(len(c) for c in all_facets)
assert sizes == Counter({3: 12, 4: 4})
log.append(f'closed surface: (V,E,F) = {(V, E, F)}, facet sizes {dict(sizes)}; all nonzero slacks > 0 for every integer m >= 2')

# numerical cross-check of the inequalities against the actual reduced point sets
import sys
import numpy as np
sys.path.insert(0, HERE)
from siamese_util import zeta_points
for nn_ in range(5, 43, 2):
    mm = (nn_ - 1) // 2
    Z = zeta_points(nn_)
    for k, (a, b) in INEQ.items():
        av = [int(sp.sympify(c).subs(m, mm)) for c in a]
        bv = int(sp.sympify(b).subs(m, mm))
        assert (Z @ np.array(av) <= bv).all() and (-Z @ np.array(av) <= bv).all(), (nn_, k)
log.append('all lattice points of the reduced Siamese gems for n = 5..41 satisfy the 16 inequalities')

# LaTeX table: rows = level-polygon vertices, columns = inequalities (1)..(8)
names = {f'q{k}': f'q_{{{k}}}' for k in range(1, 17)}
lines = [r'\begin{tabular}{l l cccccccc}', r'\toprule',
         r'point & $(x,y,\zeta)$ & (1) & (2) & (3) & (4) & (5) & (6) & (7) & (8)\\', r'\midrule']

for name in ORDER:
    p = P[name]
    coords = '(' + ','.join(sp.latex(sp.expand(c)).replace(' ', '') for c in p) + ')'
    cells = ' & '.join('$' + fmt(s) + '$' for s in rows[name])
    lines.append(f'${names[name]}$ & ${coords}$ & {cells}\\\\')
    if name in ('q14', 'q8', 'q16'):
        lines.append(r'\addlinespace[2pt]')
    if name == 'q3':
        lines.append(r'\addlinespace[2pt]')
lines += [r'\bottomrule', r'\end{tabular}']
with open(os.path.join(HERE, 'siamese_slacks.tex'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
with open(os.path.join(HERE, 'siamese_slacks.log'), 'w') as f:
    f.write('\n'.join(log) + '\n')
print('\n'.join(log))

# ---------------------------------------------------------------- isometry group of the Siamese gem, all m >= 2
# A symmetry of the gem permutes its vertices and preserves the face lattice; the face lattice has 8
# automorphisms (computed from the facet list above).  In the original coordinates
# z = lambda(x,y) + n zeta, lambda(x,y) = n(x-y+m) + (2x-y+m) + 1 - (n^2+1)/2, we show that the only
# automorphisms preserving all squared distances, as polynomials in m, are id and -id, and that for each of
# the other six some squared distance differs by a polynomial with no integer root m >= 2.
import networkx as nx
G = nx.Graph()
for i, c in enumerate(all_facets):
    G.add_node(('f', i), kind=1)
    for v in c:
        G.add_node(('v', v), kind=0); G.add_edge(('f', i), ('v', v))
gm = nx.algorithms.isomorphism.GraphMatcher(G, G, node_match=lambda a, b: a['kind'] == b['kind'])
autos = [{a[1]: b[1] for a, b in iso.items() if a[0] == 'v'} for iso in gm.isomorphisms_iter()]
assert len(autos) == 8
lam = lambda x, y: n * (x - y + m) + (2 * x - y + m) + 1 - (n**2 + 1) / sp.Integer(2)
Z = {v: (P[v][0], P[v][1], sp.expand(lam(P[v][0], P[v][1]) + n * P[v][2])) for v in verts}
d2 = lambda a, b: sp.expand(sum((Z[a][k] - Z[b][k])**2 for k in range(3)))
VL = sorted(verts, key=lambda s: int(s[1:]))
n_iso = 0
for pi in autos:
    bad = None
    for a in VL:
        for b in VL:
            if a < b:
                dlt = sp.expand(d2(a, b) - d2(pi[a], pi[b]))
                if dlt != 0:
                    roots = [r for r in sp.Poly(dlt, m).all_roots() if r.is_integer and r >= 2]
                    if not roots:
                        bad = (a, b, dlt); break
        if bad: break
    if bad is None:
        assert all(sp.expand(d2(a, b) - d2(pi[a], pi[b])) == 0 for a in VL for b in VL)
        n_iso += 1
        assert all(pi[v] == v for v in VL) or all(pi[v] == NEG[v] for v in VL)
assert n_iso == 2
log.append('isometry group of the Siamese gem for every m >= 2: {id, -id} (8 combinatorial automorphisms, 6 not isometric)')
with open(os.path.join(HERE, 'siamese_slacks.log'), 'w') as f:
    f.write('\n'.join(log) + '\n')
print(log[-1])

# hand-checkable form of the same fact: the six antipodal pairs {v, -v} have distinct squared norms for m >= 2,
# and q1 is orthogonal to no other vertex; an isometry of the gem fixes the centroid 0 of its vertex set.
reps = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
assert all(NEG[NEG[v]] == v for v in reps) and set(reps) | {NEG[v] for v in reps} == verts
norms = {v: sp.expand(sum(c**2 for c in Z[v])) for v in reps}
for a, b in itertools.combinations(reps, 2):
    dlt = sp.Poly(norms[a] - norms[b], m)
    assert not [r for r in dlt.all_roots() if r.is_integer and r >= 2], (a, b)
for v in reps[1:]:
    dot = sp.Poly(sp.expand(sum(p * q for p, q in zip(Z['q1'], Z[v]))), m)
    assert not [r for r in dot.all_roots() if r.is_integer and r >= 2], v
print('norms', {v: str(sp.factor(norms[v])) for v in reps})
