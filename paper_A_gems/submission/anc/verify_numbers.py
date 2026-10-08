"""Re-derives every number quoted in the paper from the data files / exact hull code. Prints a report; writes verify_numbers.json."""
import json, os, sys
from collections import Counter, defaultdict
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull
from siamese_util import siamese
out = {}
g = json.load(open(f'{HERE}/results_geometry.json')); per = g['per_gem']
types = g['combinatorial_types']; type_of = {k: t for t, ty in enumerate(types) for k in ty['members']}
# Table: per vertex count
tab = {}
for V in range(8, 17):
    ks = [p for p in per if p['f_vector'][0] == V]
    tab[V] = dict(squares=len(ks), types=len({p['combinatorial_type'] for p in ks}),
                  volumes=len({p['volume'] for p in ks}), fvectors=len({tuple(p['f_vector']) for p in ks}))
out['table_by_V'] = tab; print(tab)
den = Counter(Fraction(p['volume']).denominator for p in per); print('volume denominators', den)
fv = Counter(tuple(p['f_vector']) for p in per); print('modal f', fv.most_common(2), 'min/max fvec', min(fv), max(fv))
print('(8,14,8)', fv[(8,14,8)], '(8,16,10)', fv[(8,16,10)], '(16,36,22)', fv[(16,36,22)], '(8,18,12)', fv[(8,18,12)])
print('type sizes', sorted(Counter(len(t['members']) for t in types).items()))
big = sorted(types, key=lambda t: -len(t['members']))[:2]; print([(t['f_vector'], len(t['members']), Counter(t['face_sizes'])) for t in big])
print('8-vertex types', len({p['combinatorial_type'] for p in per if p['f_vector'][0]==8}), '16-vertex types', len({p['combinatorial_type'] for p in per if p['f_vector'][0]==16}))
# Dudeney vs V
d = g['dudeney_group']
for grp in range(1, 13):
    ks = [k for k in range(880) if d[k] == grp]
    print('Dud', grp, len(ks), 'Vcounts', len({per[k]['f_vector'][0] for k in ks}), 'types', len({per[k]['combinatorial_type'] for k in ks}),
          '8-vertex', sum(1 for k in ks if per[k]['f_vector'][0]==8), 'all-even-V', all(per[k]['f_vector'][0]%2==0 for k in ks))
# named squares
dur = np.array([[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]); loshu = np.array([[2,7,6],[9,5,1],[4,3,8]])
for nm, S in [('Loshu', loshu), ('Durer', dur), ('Siamese5', siamese(5))]:
    h = exact_hull(S); print(nm, h['f_vector'], h['volume'], 'hull fraction', len(h['vertices']), S.size)
sq = np.loadtxt(f'{HERE}/squares880.txt', dtype=int).reshape(880,4,4)
def canon(S): 
    L=[];T=S
    for _ in range(4):
        L += [tuple(T.ravel()), tuple(T.T.ravel())]; T=np.rot90(T)
    return min(L)
c = {canon(S): k for k, S in enumerate(sq)}
print('Durer class', c[canon(dur)], per[c[canon(dur)]]['f_vector'], 'swapped', c[canon(dur[[1,0,3,2]])], per[c[canon(dur[[1,0,3,2]])]]['f_vector'])
# Siamese f-vectors n=3..21
sf = {}
for n in range(3, 22, 2):
    h = exact_hull(siamese(n)); sf[n] = (h['f_vector'], Counter(h['face_sizes']).most_common()); 
print(sf)
out['siamese'] = {str(k): [list(v[0]), v[1]] for k, v in sf.items()}
# Loly invariant & mixed moment
for n in range(3, 10): print(n, n*n*(n**4-1)//12, end='; ')
print()
json.dump(out, open(f'{HERE}/verify_numbers.json', 'w'), default=str)
