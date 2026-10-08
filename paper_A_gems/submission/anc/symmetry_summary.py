"""Aggregates symmetry_880.json into the numbers quoted in the paper (writes symmetry_summary.json)."""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(f'{HERE}/symmetry_880.json')); g = json.load(open(f'{HERE}/results_geometry.json'))
out = {}
for grp in ('C1', 'C2', 'Ci'):
    s = [x for x in r if x['group'] == grp]
    fixed = Counter(sum(1 for a, b in x['face_sizes_by_orbit'] if b == 1) for x in s)
    out[grp] = dict(n=len(s), n_iso_hull={str(k): v for k, v in Counter(x['n_iso_hull'] for x in s).items()},
                    V=dict(sorted(Counter(x['f_vector'][0] for x in s).items())),
                    F=dict(sorted(Counter(x['f_vector'][2] for x in s).items())),
                    fixed_facets=dict(fixed),
                    fixed_facet_sizes=dict(Counter(a for x in s for a, b in x['face_sizes_by_orbit'] if b == 1)),
                    n_orbits_size2=dict(sorted(Counter(sum(1 for a, b in x['face_sizes_by_orbit'] if b == 2) for x in s).items())))
out['all_iso_all_equals_hull'] = all(x['n_iso_hull'] == x['n_iso_all'] for x in r)
d = g['dudeney_group']
out['dudeney'] = {grp: dict(Counter(d[x['index']] for x in r if x['group'] == grp)) for grp in ('C1', 'C2', 'Ci')}
out['self_comp_total'] = sum(1 for x in r if x['self_comp']); out['assoc_total'] = sum(1 for x in r if x['assoc'])
out['assoc_subset_of_selfcomp'] = all(x['self_comp'] for x in r if x['assoc'])
out['achiral'] = sum(1 for x in r if x['n_improper'] > 0)
# compare with the complement-orbit count of congruence classes
out['congruence_classes'] = out['C1']['n'] // 2 + out['C2']['n'] + out['Ci']['n']
json.dump(out, open(f'{HERE}/symmetry_summary.json', 'w'), indent=1); print(json.dumps(out, indent=1))
