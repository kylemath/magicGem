"""Symmetry classification of the 880 order-4 Magic Gems (Section 'Symmetry' of the paper).

For each essentially different order-4 magic square S we compute, exactly,
  * the full isometry group of the hull-vertex set of G(S) (and of the full 16-point set),
  * the face orbits of the hull under that group,
  * whether S is self-complementary (17-S in the D4-orbit of S) / associative (S + rot180 S = 17).
Output: symmetry_880.json, symmetry_880.log.  Needs only numpy, scipy, networkx.
"""
import json, os, sys
from collections import Counter, defaultdict
from itertools import product
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull
from isolib import isometries, element_type, group_name

SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)

def d4(S):
    out = []; T = S
    for _ in range(4):
        out.append(T); out.append(T.T); T = np.rot90(T)
    return out
def canon(S): return min(tuple(int(x) for x in V.ravel()) for V in d4(S))
cidx = {canon(S): k for k, S in enumerate(SQ)}

res = []
for k, S in enumerate(SQ):
    h = exact_hull(S); P = h['P']; V = h['vertices']
    isoV = isometries(P[V]); isoA = isometries(P)
    types = [element_type(R) for _, R in isoV]
    # faces of the hull as frozensets of hull-vertex positions (indices into V)
    pos = {v: t for t, v in enumerate(V)}
    faces = [frozenset(pos[v] for v in f) for f in h['faces'].values()]
    fset = set(faces)
    # orbits of faces under the group
    orb = []; seen = set()
    for f in faces:
        if f in seen: continue
        o = {frozenset(int(p[v]) for v in f) for p, _ in isoV}
        assert o <= fset
        seen |= o; orb.append(sorted(len(x) for x in [f]) + [len(o)])
    # complementary / associative status
    comp = canon(17 - S) == canon(S)
    assoc = bool((S + np.rot90(S, 2) == 17).all())
    # which D4 element g gives g S = 17 - S ?
    gcomp = None
    if comp:
        names = ['e', 'T', 'r', 'rT', 'r2', 'r2T', 'r3', 'r3T']
        for nm, V4 in zip(names, d4(S)):
            if (V4 == 17 - S).all(): gcomp = nm
    # does the full 16-point set have the same group order?
    res.append(dict(index=k, f_vector=h['f_vector'], n_iso_hull=len(isoV), n_iso_all=len(isoA),
                    group=group_name(types), types=dict(Counter(types)), self_comp=bool(comp),
                    assoc=assoc, g_comp=gcomp, n_proper=sum(1 for t in types if t in ('E', 'C2', 'C3', 'C4', 'C6')),
                    n_improper=sum(1 for t in types if t not in ('E', 'C2', 'C3', 'C4', 'C6')),
                    face_orbit_sizes=sorted(Counter(o[-1] for o in orb).items()),
                    face_sizes_by_orbit=[(o[0], o[1]) for o in orb]))
    if k % 100 == 0: print(k, res[-1]['group'], flush=True)

summary = Counter((r['group'], r['self_comp'], r['assoc'], r['g_comp'], r['n_iso_hull'], r['n_iso_all']) for r in res)
for key, v in sorted(summary.items(), key=lambda kv: -kv[1]): print(v, key)
json.dump(res, open(os.path.join(HERE, 'symmetry_880.json'), 'w'))
