"""Bounding box, forced vertices, interior / boundary non-vertex points and square classes of the
880 order-4 gems (exact integer arithmetic).  Every statement quoted in the paper is asserted below.
Run from this directory:  python3 box_and_classes.py   ->  results_box_classes.json, box_and_classes.log
"""
import os, json, csv
from fractions import Fraction
from collections import Counter
import numpy as np
from gem_geometry import exact_hull

HERE = os.path.dirname(os.path.abspath(__file__))
SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
SYM = json.load(open(os.path.join(HERE, 'symmetry_880.json')))


def d4(S):
    o, T = [], S
    for _ in range(4):
        o += [T, T.T]; T = np.rot90(T)
    return o


def canon(S):
    return min(tuple(int(x) for x in V.ravel()) for V in d4(np.asarray(S)))


# Dudeney groups (column Gr. of all7040_dudeney.csv); checked to be constant on D4-classes
cidx = {canon(S): k for k, S in enumerate(SQ)}
assert len(cidx) == 880
dud = {}
for r in list(csv.reader(open(os.path.join(HERE, 'all7040_dudeney.csv')), delimiter='\t'))[1:]:
    S = np.array([int(x) for x in r[3:19]]).reshape(4, 4)
    k = cidx[canon(S)]
    assert dud.setdefault(k, int(r[1])) == int(r[1])
assert len(dud) == 880


def pandiagonal(S):
    return all(sum(S[t, (c + d * t) % 4] for t in range(4)) == 34 for c in range(4) for d in (1, -1))


def associative(S):
    return all(S[i, j] + S[3 - i, 3 - j] == 17 for i in range(4) for j in range(4))


BOX = Fraction(3 * 3 * 15)          # (n-1)^2 (N-1) for n = 4
sides = [[(0, j) for j in range(4)], [(3, j) for j in range(4)], [(i, 0) for i in range(4)], [(i, 3) for i in range(4)]]
rec = []
cell_vertex = Counter(); entry_vertex = Counter()
for k, S in enumerate(SQ):
    h = exact_hull(S); P = h['P']                      # doubled coordinates 2p
    V = set(h['vertices']); planes = list(h['faces'].keys())
    # (1) bounding box, 1 and N are the unique z-extremes and vertices
    assert (np.abs(P[:, 0]) <= 3).all() and (np.abs(P[:, 1]) <= 3).all() and (np.abs(P[:, 2]) <= 15).all()
    cell = {int(S[v // 4, v % 4]): v for v in range(16)}
    assert P[cell[1], 2] == -15 and P[cell[16], 2] == 15 and sorted(P[:, 2])[1] > -15 and sorted(P[:, 2])[-2] < 15
    assert cell[1] in V and cell[16] in V
    # (2) forced vertices: 4 corners, min and max entry on each side line, entries 1 and N
    forced = {0, 3, 12, 15, cell[1], cell[16]}
    for sd in sides:
        vs = sorted(sd, key=lambda c: S[c]); forced |= {vs[0][0] * 4 + vs[0][1], vs[-1][0] * 4 + vs[-1][1]}
    assert forced <= V
    # (3) strictly interior vs boundary non-vertex points (exact: slack against all facet planes)
    interior = bnd = 0
    for v in range(16):
        if v in V: continue
        slack = max(a * int(P[v, 0]) + b * int(P[v, 1]) + c * int(P[v, 2]) + d for a, b, c, d in planes)
        assert slack <= 0
        if slack < 0: interior += 1
        else: bnd += 1
    assert interior + bnd + len(V) == 16
    frac = h['volume'] / BOX; assert 0 < frac < 1
    for v in V:
        cell_vertex[v] += 1; entry_vertex[int(S[v // 4, v % 4])] += 1
    sy = SYM[k]; assert sy['index'] == k and sy['f_vector'] == list(h['f_vector'])
    asc = associative(S); assert asc == sy['assoc']
    rec.append(dict(k=k, nv=len(V), vol=h['volume'], frac=frac, interior=interior, bnd=bnd, pd=pandiagonal(S), asc=asc,
                    dud=dud[k], grp=sy['group'], forced=len(forced), e2=cell[2] in V, e15=cell[15] in V,
                    f=tuple(h['f_vector'])))

C = lambda it: {str(a): b for a, b in sorted(Counter(it).items())}
out = {}
out['vertex_count'] = C(r['nv'] for r in rec)
assert out['vertex_count'] == {'8': 7, '9': 10, '10': 103, '11': 80, '12': 380, '13': 106, '14': 162, '15': 14, '16': 18}
fr = [r['frac'] for r in rec]
out['volume_fraction'] = dict(min=str(min(fr)), mean=str(sum(fr) / 880), max=str(max(fr)), n_distinct=len(set(fr)))
assert (min(fr), sum(fr) / 880, max(fr)) == (Fraction(58, 135), Fraction(2219, 3564), Fraction(292, 405)) and len(set(fr)) == 155
out['volume_fraction_by_V'] = {str(v): dict(n=sum(r['nv'] == v for r in rec),
                                            min=float(min(r['frac'] for r in rec if r['nv'] == v)),
                                            mean=float(sum(r['frac'] for r in rec if r['nv'] == v) / sum(r['nv'] == v for r in rec)),
                                            max=float(max(r['frac'] for r in rec if r['nv'] == v)))
                               for v in range(8, 17)}
out['interior_points'] = C(r['interior'] for r in rec)
out['boundary_nonvertex_points'] = C(r['bnd'] for r in rec)
out['interior_boundary_joint'] = C((r['interior'], r['bnd']) for r in rec)
assert max(r['interior'] for r in rec) == 4
assert out['interior_points'] == {'0': 37, '1': 32, '2': 353, '3': 178, '4': 280}
assert out['boundary_nonvertex_points'] == {'0': 357, '1': 204, '2': 257, '3': 40, '4': 21, '6': 1}
out['forced_set_size'] = C(r['forced'] for r in rec); assert min(r['forced'] for r in rec) == 4 and max(r['forced'] for r in rec) == 13
# cells / entries that are vertices in every gem
out['cells_always_vertex'] = [c for c in range(16) if cell_vertex[c] == 880]; assert out['cells_always_vertex'] == [0, 3, 12, 15]
out['entries_always_vertex'] = [e for e in range(1, 17) if entry_vertex[e] == 880]; assert out['entries_always_vertex'] == [1, 16]
out['max_other_cell_count'] = max(cell_vertex[c] for c in range(16) if c not in (0, 3, 12, 15)); assert out['max_other_cell_count'] < 880
no2 = [r['k'] for r in rec if not r['e2']]; no15 = [r['k'] for r in rec if not r['e15']]
assert len(no2) == 8 and len(no15) == 8
from gem_geometry import classify_points
for k in no2:      # in every one of the eight gems the point carrying 2 lies on the boundary of the gem (on a face), not in the interior
    h = exact_hull(SQ[k]); _, I, B = classify_points(h); c2 = [v for v in range(16) if SQ[k][v // 4, v % 4] == 2][0]
    assert c2 in B and c2 not in I
out['entry2_nonvertex_indices'] = no2
out['entry2_nonvertex'] = [SQ[k].tolist() for k in no2]
out['entry15_nonvertex'] = [SQ[k].tolist() for k in no15]
# the complement 17-S of a square with 2 non-extreme has 15 non-extreme (mirror image): same classes
# (D4-class of 17-S is the complement-partner class)
# (4) square classes
nrow = lambda f: [r for r in rec if f(r)]
pd_ = nrow(lambda r: r['pd']); as_ = nrow(lambda r: r['asc'])
assert len(pd_) == 48 and len(as_) == 48 and not nrow(lambda r: r['pd'] and r['asc'])
assert {r['k'] for r in pd_} == {r['k'] for r in rec if r['dud'] == 1}          # Dudeney I   = pandiagonal
assert {r['k'] for r in as_} == {r['k'] for r in rec if r['dud'] == 3}          # Dudeney III = associative
assert {r['k'] for r in rec if r['grp'] == 'C2'} == {r['k'] for r in rec if r['dud'] == 6}   # Dudeney VI = C2 gems
assert sum(r['grp'] == 'C2' for r in rec) == 304
out['pandiagonal_vertex_count'] = C(r['nv'] for r in pd_); assert set(r['nv'] for r in pd_) <= set(range(11, 16))
out['pandiagonal_interior'] = C(r['interior'] for r in pd_); assert min(r['interior'] for r in pd_) >= 1
assert out['pandiagonal_vertex_count'] == {'11': 10, '12': 20, '13': 12, '14': 4, '15': 2}
assert out['pandiagonal_interior'] == {'1': 4, '2': 12, '3': 28, '4': 4}
out['associative_vertex_count'] = C(r['nv'] for r in as_)
out['associative_interior'] = C(r['interior'] for r in as_); out['associative_boundary_nonvertex'] = C(r['bnd'] for r in as_)
assert out['associative_interior'] == {'0': 4, '2': 23, '4': 21}
for r in as_:      # central-symmetry parity (Proposition): all three counts even
    assert r['nv'] % 2 == 0 and r['interior'] % 2 == 0 and r['bnd'] % 2 == 0
v8 = nrow(lambda r: r['nv'] == 8)
out['eight_vertex_gems'] = [dict(k=r['k'], dudeney=r['dud'], group=r['grp'], f=list(r['f']), interior=r['interior'],
                                 boundary_nonvertex=r['bnd'], pandiagonal=r['pd'], associative=r['asc']) for r in v8]
assert [r['k'] for r in v8] == [50, 54, 276, 277, 494, 496, 672]
assert all(not r['pd'] and not r['asc'] and r['interior'] == 4 and r['bnd'] == 4 for r in v8)
assert [r['dud'] for r in v8] == [6, 6, 8, 8, 8, 8, 6]
# named squares
DURER = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
kd = cidx[canon(DURER)]
out['durer'] = dict(k=kd, nv=rec[kd]['nv'], interior=rec[kd]['interior'], boundary_nonvertex=rec[kd]['bnd'])
out['square_54'] = dict(nv=rec[54]['nv'], interior=rec[54]['interior'], boundary_nonvertex=rec[54]['bnd'])
for k in (102, 124, 802, 379):
    out[f'square_{k}'] = dict(nv=rec[k]['nv'], interior=rec[k]['interior'], boundary_nonvertex=rec[k]['bnd'])
# Siamese gems: the vertex set equals the forced set (corners, side extremes) for odd n = 5..21
from siamese_util import siamese
for n in range(5, 22, 2):
    S = siamese(n); h = exact_hull(S); sd = [[(0, j) for j in range(n)], [(n - 1, j) for j in range(n)], [(i, 0) for i in range(n)], [(i, n - 1) for i in range(n)]]
    F = {0, n - 1, n * (n - 1), n * n - 1}
    for c in sd:
        vs = sorted(c, key=lambda t: S[t]); F |= {vs[0][0] * n + vs[0][1], vs[-1][0] * n + vs[-1][1]}
    assert F == set(h['vertices']) and len(F) == 12, n
out['siamese_vertices_equal_forced_n5_to_21'] = True
json.dump(out, open(os.path.join(HERE, 'results_box_classes.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
print('all assertions passed')
