"""Box + square-class analysis of the 880 order-4 gems (exact). Run from anywhere."""
import sys, os, json, csv
from fractions import Fraction
from collections import Counter, defaultdict
import numpy as np
ANC = '/Users/kylemathewson/magicGem/paper_A_gems/anc'
sys.path.insert(0, ANC)
from gem_geometry import exact_hull
OUT = os.path.dirname(os.path.abspath(__file__))
SQ = np.loadtxt(f'{ANC}/squares880.txt', dtype=int).reshape(880, 4, 4)
SYM = json.load(open(f'{ANC}/symmetry_880.json'))


def d4(S):
    o = []; T = S
    for _ in range(4):
        o += [T, T.T]; T = np.rot90(T)
    return o


def canon(S): return min(tuple(int(x) for x in V.ravel()) for V in d4(np.asarray(S)))


cidx = {canon(S): k for k, S in enumerate(SQ)}
assert len(cidx) == 880
dud = {}
for r in list(csv.reader(open(f'{ANC}/all7040_dudeney.csv'), delimiter='\t'))[1:]:
    S = np.array([int(x) for x in r[3:19]]).reshape(4, 4)
    k = cidx[canon(S)]; g = int(r[1])
    assert dud.setdefault(k, g) == g, 'Dudeney group not D4-invariant'
assert len(dud) == 880


def pandiag(S):
    return all(sum(S[t, (c+d*t) % 4] for t in range(4)) == 34 for c in range(4) for d in (1, -1))
def assoc(S): return all(S[i, j] + S[3-i, 3-j] == 17 for i in range(4) for j in range(4))
def mostperfect(S):
    if not pandiag(S): return False
    if not all(S[i, j]+S[(i+2) % 4, (j+2) % 4] == 17 for i in range(4) for j in range(4)): return False
    return all(S[i, j]+S[i, (j+1) % 4]+S[(i+1) % 4, j]+S[(i+1) % 4, (j+1) % 4] == 34 for i in range(4) for j in range(4))
def selfcomp(S): return canon(17 - S) == canon(S)


def hull2d_count(pts):
    pts = sorted(set(pts))
    def cr(o, a, b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return len(lo)+len(up)-2


box_vol = Fraction(3*3*15)
rec = []
vertex_cell_cnt = Counter(); vertex_entry_cnt = Counter()
for k, S in enumerate(SQ):
    h = exact_hull(S); P = h['P']          # doubled coordinates
    assert (np.abs(P[:, 0]) <= 3).all() and (np.abs(P[:, 1]) <= 3).all() and (np.abs(P[:, 2]) <= 15).all()
    V = set(h['vertices'])
    ent = lambda v: int(S[v//4, v % 4])
    i1 = [v for v in range(16) if ent(v) == 1][0]; i16 = [v for v in range(16) if ent(v) == 16][0]
    assert P[i1, 2] == -15 and P[i16, 2] == 15 and (P[:, 2] > -15).sum() == 15 and (P[:, 2] < 15).sum() == 15
    assert i1 in V and i16 in V
    forced = {0, 3, 12, 15}
    sides = [[(0, j) for j in range(4)], [(3, j) for j in range(4)], [(i, 0) for i in range(4)], [(i, 3) for i in range(4)]]
    for sd in sides:
        vs = sorted(sd, key=lambda c: S[c]); forced |= {vs[0][0]*4+vs[0][1], vs[-1][0]*4+vs[-1][1]}
    forced |= {i1, i16}
    assert forced <= V, (k, forced - V)
    planes = list(h['faces'].keys())
    interior = bnd_nonvert = 0
    for v in range(16):
        if v in V: continue
        vals = [a*int(P[v, 0])+b*int(P[v, 1])+c*int(P[v, 2])+d for a, b, c, d in planes]
        assert max(vals) <= 0
        if max(vals) < 0: interior += 1
        else: bnd_nonvert += 1
    vol = h['volume']; frac = vol / box_vol
    assert 0 < frac < 1
    dv = P[i1]-P[i16]; d2 = Fraction(int(dv @ dv), 4)
    contact = []
    for sd in sides:
        varying = 1 if sd[0][0] == sd[1][0] else 0   # row side: x varies... use the coordinate that varies along the side
        pts = [(int(P[a*4+b, 0] if sd[0][0] == sd[1][0] else P[a*4+b, 1]), int(P[a*4+b, 2])) for a, b in sd]
        contact.append(hull2d_count(pts))
    for v in V:
        vertex_cell_cnt[v] += 1; vertex_entry_cnt[ent(v)] += 1
    s = SYM[k]; assert s['index'] == k and s['f_vector'] == list(h['f_vector'])
    asc = assoc(S)
    assert asc == s['assoc'] and selfcomp(S) == s['self_comp']
    ents = [ent(v) for v in V]
    rec.append(dict(k=k, nv=h['f_vector'][0], f=tuple(h['f_vector']), vol=vol, frac=frac, interior=interior,
                    bnd_nonvert=bnd_nonvert, nonvert=16-len(V), d2=d2, contact=tuple(sorted(contact)),
                    pd=pandiag(S), asc=asc, sc=selfcomp(S), mp=mostperfect(S), dud=dud[k], grp=s['group'],
                    e2=2 in ents, e15=15 in ents, forced=len(forced)))
assert len(rec) == 880


def C(it): return dict(sorted(Counter(it).items(), key=lambda t: str(t[0])))


res = {}
res['n_vertices'] = C(r['nv'] for r in rec)
fr = [r['frac'] for r in rec]
res['volume_fraction'] = dict(min=str(min(fr)), max=str(max(fr)), mean=str(sum(fr)/880), mean_float=float(sum(fr)/880),
                              min_float=float(min(fr)), max_float=float(max(fr)), n_distinct=len(set(fr)))
res['volume_fraction_distinct'] = {str(f): c for f, c in sorted(Counter(fr).items())}
res['interior_points'] = C(r['interior'] for r in rec)
res['boundary_nonvertex_points'] = C(r['bnd_nonvert'] for r in rec)
res['dist2_1_16'] = {str(k): v for k, v in sorted(Counter(r['d2'] for r in rec).items())}
res['contact_side_polygon_vertex_counts'] = {str(k): v for k, v in sorted(Counter(r['contact'] for r in rec).items())}
res['forced_vertex_count_distribution'] = C(r['forced'] for r in rec)
res['min_forced_and_min_nv'] = (min(r['forced'] for r in rec), min(r['nv'] for r in rec))
res['vertex_by_grid_cell_count'] = {str(c): vertex_cell_cnt[c] for c in range(16)}
res['vertex_by_entry_count'] = {str(e): vertex_entry_cnt[e] for e in range(1, 17)}
res['entry2_nonvertex_count'] = sum(not r['e2'] for r in rec)
res['entry15_nonvertex_count'] = sum(not r['e15'] for r in rec)
res['counts'] = dict(pandiagonal=sum(r['pd'] for r in rec), associative=sum(r['asc'] for r in rec),
                     both=sum(r['pd'] and r['asc'] for r in rec), selfcomp=sum(r['sc'] for r in rec),
                     mostperfect=sum(r['mp'] for r in rec))
types = [('pandiagonal', lambda r: r['pd']), ('associative', lambda r: r['asc']), ('selfcomp', lambda r: r['sc']),
         ('mostperfect', lambda r: r['mp']), ('dudeney', lambda r: r['dud']), ('group', lambda r: r['grp']),
         ('pd_assoc', lambda r: (r['pd'], r['asc']))]
def cross(tf, valf):
    t = defaultdict(Counter)
    for r in rec: t[str(tf(r))][str(valf(r))] += 1
    return {a: dict(sorted(b.items())) for a, b in sorted(t.items())}
res['cross'] = {}
for name, tf in types:
    d = {}
    for vn, vf in [('n_vertices', lambda r: r['nv']), ('interior', lambda r: r['interior']), ('f_vector', lambda r: r['f']),
                   ('sym', lambda r: r['grp']), ('dist2_1_16', lambda r: r['d2'])]:
        d[vn] = cross(tf, vf)
    vol = {}
    for a in sorted({str(tf(r)) for r in rec}):
        m = [r['frac'] for r in rec if str(tf(r)) == a]
        vol[a] = dict(n=len(m), min=float(min(m)), mean=float(sum(m)/len(m)), max=float(max(m)))
    d['vol_fraction'] = vol
    res['cross'][name] = d
pdn = [r for r in rec if r['pd']]; asc = [r for r in rec if r['asc']]
res['test_a_pandiagonal_with_16_vertices'] = sum(r['nv'] == 16 for r in pdn)
res['test_a_pandiagonal_nv'] = C(r['nv'] for r in pdn)
res['test_b_assoc_interior'] = C(r['interior'] for r in asc)
res['test_b_assoc_nonvertex'] = C(r['nonvert'] for r in asc)
res['test_b_nonassoc_interior'] = C(r['interior'] for r in rec if not r['asc'])
res['test_b_nonassoc_nonvertex'] = C(r['nonvert'] for r in rec if not r['asc'])
res['test_b_assoc_nv_parity'] = C(r['nv'] % 2 for r in asc)
min8 = [r for r in rec if r['nv'] == 8]
res['test_c_nv8_count'] = len(min8)
res['test_c_nv8'] = [dict(k=r['k'], pd=r['pd'], asc=r['asc'], sc=r['sc'], mp=r['mp'], dud=r['dud'], grp=r['grp'], f=list(r['f']),
                          interior=r['interior'], frac=str(r['frac'])) for r in min8]
res['n_vertices_vs_mean_vol'] = {nv: float(sum(r['frac'] for r in rec if r['nv'] == nv)/sum(1 for r in rec if r['nv'] == nv)) for nv in sorted({r['nv'] for r in rec})}
json.dump(res, open(f'{OUT}/results.json', 'w'), indent=1, default=str)
skip = ('cross', 'volume_fraction_distinct')
print(json.dumps({k: res[k] for k in res if k not in skip}, indent=1, default=str))
