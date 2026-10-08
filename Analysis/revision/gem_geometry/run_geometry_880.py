"""Part A: geometry of the 880 essentially different 4x4 Magic Gems."""
import json, sys, os, csv
from collections import Counter, defaultdict
from fractions import Fraction
import numpy as np
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gem_geometry import (exact_hull, bipartite_graph, combinatorial_hash,
                          same_combinatorial_type, sqdist_multiset, congruent, kabsch_check)

ROOT = '/Users/kylemathewson/magicGem'
SQ = np.load(f'{ROOT}/Analysis/data/magic_squares_880 (1).npy')
assert SQ.shape == (880, 4, 4)
n = 4; N = 16


def d4_variants(S):
    out = []
    T = S
    for _ in range(4):
        out.append(T); out.append(T.T)
        T = np.rot90(T)
    return out


def canon(S):
    return min(tuple(int(x) for x in V.ravel()) for V in d4_variants(np.asarray(S)))


def is_magic(S):
    S = np.asarray(S); n = S.shape[0]; M = n * (n * n + 1) // 2
    return (S.sum(0) == M).all() and (S.sum(1) == M).all() and \
        np.trace(S) == M and np.trace(np.fliplr(S)) == M and sorted(S.ravel()) == list(range(1, n * n + 1))


assert all(is_magic(S) for S in SQ)
canon_index = {canon(S): k for k, S in enumerate(SQ)}
assert len(canon_index) == 880

# ------------------------------------------------------------- hull data
hulls = []
for k, S in enumerate(SQ):
    h = exact_hull(S)
    h['G'] = bipartite_graph(h)
    h['wl'] = combinatorial_hash(h, h['G'])
    h['vertex_cells'] = [(v // n, v % n) for v in h['vertices']]
    hulls.append(h)

vcount = Counter(h['f_vector'][0] for h in hulls)
fvec = Counter(h['f_vector'] for h in hulls)
vols = Counter(h['volume'] for h in hulls)
face_size_profiles = Counter(tuple(h['face_sizes']) for h in hulls)
print('vertex counts:', sorted(vcount.items()))
print('distinct f-vectors:', len(fvec))
print('distinct volumes:', len(vols))
print('distinct face-size profiles:', len(face_size_profiles))

# ------------------------------------------------------------- combinatorial types
by_hash = defaultdict(list)
for k, h in enumerate(hulls):
    by_hash[h['wl']].append(k)
types = []  # list of lists of indices
hash_splits = 0
for hsh, members in by_hash.items():
    reps = []  # (rep_index, [members])
    for k in members:
        for r in reps:
            if same_combinatorial_type(hulls[k]['G'], hulls[r[0]]['G']):
                r[1].append(k); break
        else:
            reps.append((k, [k]))
    if len(reps) > 1:
        hash_splits += 1
    types.extend(m for _, m in reps)
types.sort(key=lambda m: (-len(m), m[0]))
print('combinatorial types:', len(types), ' (WL hash groups:', len(by_hash), ', split groups:', hash_splits, ')')
# check: f-vector constant within a type
for m in types:
    assert len({hulls[k]['f_vector'] for k in m}) == 1
    assert len({tuple(hulls[k]['face_sizes']) for k in m}) == 1
type_size_dist = Counter(len(m) for m in types)
print('type size distribution (size: #types):', sorted(type_size_dist.items()))
# compare: how many types per f-vector
types_per_fvec = Counter(hulls[m[0]]['f_vector'] for m in types)

# ------------------------------------------------------------- identical hull-vertex sets
vset_groups = defaultdict(list)
for k, h in enumerate(hulls):
    key = tuple(sorted(tuple(int(c) for c in h['P'][v]) for v in h['vertices']))
    vset_groups[key].append(k)
print('distinct hull-vertex point sets:', len(vset_groups), ' (identical-gem groups of size>1:',
      sum(1 for g in vset_groups.values() if len(g) > 1), ')')

# ------------------------------------------------------------- congruence classes (hull vertices)
def congruence_classes(point_lists):
    sig_groups = defaultdict(list)
    for k, P in enumerate(point_lists):
        sig_groups[(len(P), sqdist_multiset(P))].append(k)
    classes = []
    sig_splits = 0
    for sig, members in sig_groups.items():
        reps = []
        for k in members:
            for r in reps:
                if congruent(point_lists[k], point_lists[r[0]]):
                    r[1].append(k); break
            else:
                reps.append((k, [k]))
        if len(reps) > 1:
            sig_splits += 1
        classes.extend(m for _, m in reps)
    classes.sort(key=lambda m: (-len(m), m[0]))
    return classes, len(sig_groups), sig_splits

hull_pts = [h['P'][h['vertices']] for h in hulls]
cong_hull, nsig_hull, splits_hull = congruence_classes(hull_pts)
print('congruence classes of gems (hull vertex sets):', len(cong_hull),
      ' signature groups:', nsig_hull, ' signature splits:', splits_hull)
print('congruence class size distribution:', sorted(Counter(len(m) for m in cong_hull).items()))
# Kabsch numerical confirmation for every non-trivial class
max_rmsd = 0.0
for m in cong_hull:
    for k in m[1:]:
        max_rmsd = max(max_rmsd, kabsch_check(hull_pts[m[0]], hull_pts[k]))
print('max Kabsch RMSD within congruence classes:', max_rmsd)

# all 16 points (congruence of the full point configuration)
all_pts = [h['P'] for h in hulls]
cong_all, nsig_all, splits_all = congruence_classes(all_pts)
print('congruence classes of full 16-point configurations:', len(cong_all))

# explanation: complement S -> 17 - S is the reflection z -> -z
comp_pairs = 0; self_comp = 0
comp_partner = {}
for k, S in enumerate(SQ):
    kc = canon_index[canon(17 - S)]
    comp_partner[k] = kc
    if kc == k:
        self_comp += 1
    elif kc > k:
        comp_pairs += 1
print('self-complementary squares:', self_comp, ' complement pairs:', comp_pairs)
# are the congruence classes exactly the complement orbits?
comp_orbits = {frozenset({k, comp_partner[k]}) for k in range(880)}
cong_all_sets = {frozenset(m) for m in cong_all}
print('full-config congruence classes == complement orbits:', comp_orbits == cong_all_sets)
# hull classes beyond complement
extra = [m for m in cong_hull if frozenset(m) not in comp_orbits]
print('hull-congruence classes that are NOT complement orbits:', len(extra))

# ------------------------------------------------------------- Dudeney groups
dud = {}
with open(f'{ROOT}/Analysis/data/all7040CategoriesData.csv') as f:
    rd = csv.reader(f, delimiter='\t')
    next(rd)
    for row in rd:
        g = int(row[1]); vals = [int(x) for x in row[3:19]]
        S = np.array(vals).reshape(4, 4)
        c = canon(S)
        k = canon_index.get(c)
        if k is None:
            raise RuntimeError('CSV square not found among the 880')
        dud.setdefault(k, set()).add(g)
assert len(dud) == 880 and all(len(v) == 1 for v in dud.values())
dudeney = [next(iter(dud[k])) for k in range(880)]
dud_counts = Counter(dudeney)
print('Dudeney group sizes:', sorted(dud_counts.items()))
dud_vs_V = defaultdict(Counter)
for k in range(880):
    dud_vs_V[dudeney[k]][hulls[k]['f_vector'][0]] += 1
dud_vs_types = defaultdict(set)
type_of = {}
for t, m in enumerate(types):
    for k in m:
        type_of[k] = t
for k in range(880):
    dud_vs_types[dudeney[k]].add(type_of[k])
dud_vol = {g: sorted({float(hulls[k]['volume']) for k in range(880) if dudeney[k] == g}) for g in range(1, 13)}

# ------------------------------------------------------------- extremes
def sq_list(S):
    return [[int(x) for x in r] for r in S]

vol_list = [h['volume'] for h in hulls]
kmin = int(np.argmin([float(v) for v in vol_list])); kmax = int(np.argmax([float(v) for v in vol_list]))
k8 = [k for k, h in enumerate(hulls) if h['f_vector'][0] == 8]
k16 = [k for k, h in enumerate(hulls) if h['f_vector'][0] == 16]
print('min volume', vol_list[kmin], 'square', kmin); print(SQ[kmin])
print('max volume', vol_list[kmax], 'square', kmax); print(SQ[kmax])
print('8-vertex gems:', k8); print('16-vertex gems:', k16)
for k in k8: print(SQ[k], hulls[k]['volume'], hulls[k]['f_vector'], dudeney[k])

# ------------------------------------------------------------- save
results = dict(
    n_squares=880,
    vertex_count_distribution={int(k): int(v) for k, v in sorted(vcount.items())},
    f_vector_distribution={str(k): int(v) for k, v in sorted(fvec.items())},
    n_distinct_f_vectors=len(fvec),
    face_size_profile_count=len(face_size_profiles),
    volume_distribution={str(k): int(v) for k, v in sorted(vols.items(), key=lambda kv: kv[0])},
    n_distinct_volumes=len(vols),
    volume_min=str(vol_list[kmin]), volume_max=str(vol_list[kmax]),
    volume_mean=float(np.mean([float(v) for v in vol_list])),
    area_min=float(min(h['area'] for h in hulls)), area_max=float(max(h['area'] for h in hulls)),
    n_combinatorial_types=len(types),
    n_wl_hash_groups=len(by_hash), n_wl_groups_split_by_isomorphism=hash_splits,
    combinatorial_type_size_distribution={int(k): int(v) for k, v in sorted(type_size_dist.items())},
    combinatorial_types=[dict(size=len(m), f_vector=hulls[m[0]]['f_vector'],
                              face_sizes=hulls[m[0]]['face_sizes'],
                              representative_index=m[0], representative_square=sq_list(SQ[m[0]]),
                              members=m) for m in types],
    types_per_f_vector={str(k): int(v) for k, v in sorted(types_per_fvec.items())},
    n_distinct_hull_vertex_sets=len(vset_groups),
    identical_gem_groups=[g for g in vset_groups.values() if len(g) > 1],
    n_congruence_classes_hull=len(cong_hull),
    congruence_class_size_distribution_hull={int(k): int(v) for k, v in sorted(Counter(len(m) for m in cong_hull).items())},
    n_signature_groups_hull=nsig_hull, n_signature_groups_split=splits_hull,
    max_kabsch_rmsd=max_rmsd,
    n_congruence_classes_full16=len(cong_all),
    n_self_complementary=self_comp, n_complement_pairs=comp_pairs,
    full16_classes_equal_complement_orbits=(comp_orbits == cong_all_sets),
    hull_classes_not_complement_orbits=extra,
    complement_partner=[int(comp_partner[k]) for k in range(880)],
    dudeney_group=[int(g) for g in dudeney],
    dudeney_group_sizes={int(k): int(v) for k, v in sorted(dud_counts.items())},
    dudeney_vs_vertex_count={int(g): {int(k): int(v) for k, v in sorted(c.items())} for g, c in sorted(dud_vs_V.items())},
    dudeney_n_types={int(g): len(s) for g, s in sorted(dud_vs_types.items())},
    dudeney_n_volumes={int(g): len(v) for g, v in dud_vol.items()},
    extremes=dict(min_volume=dict(index=kmin, square=sq_list(SQ[kmin]), volume=str(vol_list[kmin]), f_vector=hulls[kmin]['f_vector']),
                  max_volume=dict(index=kmax, square=sq_list(SQ[kmax]), volume=str(vol_list[kmax]), f_vector=hulls[kmax]['f_vector']),
                  eight_vertex=[dict(index=k, square=sq_list(SQ[k]), volume=str(hulls[k]['volume']), f_vector=hulls[k]['f_vector'],
                                     face_sizes=hulls[k]['face_sizes'], dudeney=dudeney[k], vertex_cells=hulls[k]['vertex_cells']) for k in k8],
                  sixteen_vertex=[dict(index=k, square=sq_list(SQ[k]), volume=str(hulls[k]['volume']), f_vector=hulls[k]['f_vector'],
                                       face_sizes=hulls[k]['face_sizes'], dudeney=dudeney[k]) for k in k16]),
    per_gem=[dict(index=k, square=sq_list(SQ[k]), f_vector=hulls[k]['f_vector'], face_sizes=hulls[k]['face_sizes'],
                  volume=str(hulls[k]['volume']), area=hulls[k]['area'], hull_vertex_cells=hulls[k]['vertex_cells'],
                  combinatorial_type=type_of[k], dudeney=dudeney[k]) for k in range(880)],
)
with open(f'{HERE}/results_geometry.json', 'w') as f:
    json.dump(results, f, indent=1)
print('saved results_geometry.json')
