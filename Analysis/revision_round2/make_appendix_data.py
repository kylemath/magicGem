"""Round 2: ancillary file revision_round2/appendix_data.json (and .md) holding the material removed from the
appendices: the witnesses for k*(n)=n-1 (5<=n<=13), the exact variance polynomials of eq. (var_low), and the 39
f-vectors of the 880 order-4 gems with multiplicities.  Sources: Analysis/revision/theory/results.json,
Analysis/revision/random_energy/variance_fits.json, Analysis/revision/gem_geometry/results_geometry.json (read-only)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
T = json.load(open(f'{ROOT}/Analysis/revision/theory/results.json'))
key = [k for k in T if k.startswith('permutation_threshold_search')][0]
wit = {n: T[key][str(n)]['square'] for n in range(5, 14)}
V = json.load(open(f'{ROOT}/Analysis/revision/random_energy/variance_fits.json'))
G = json.load(open(f'{ROOT}/Analysis/revision/gem_geometry/results_geometry.json'))
fv = G.get('f_vector_distribution') or G.get('f_vectors') or {k: v for k, v in G.items() if 'f_vector' in k}
out = {'description': __doc__,
       'witnesses_k_star_n_minus_1': {'note': 'rows all equal M(n); column deviations (-1)^j C(n-1,j); verified by Analysis/revision_round1/check_round1.py',
                                      'squares': wit},
       'variance_polynomials': V,
       'f_vectors_880': fv}
json.dump(out, open(f'{HERE}/appendix_data.json', 'w'), indent=1)
md = ['# Appendix data (ancillary, round 2)', '', __doc__, '', '## Witnesses for k*(n) = n-1']
for n, S in wit.items():
    md.append(f'- n = {n}: ' + ' / '.join(' '.join(map(str, r)) for r in S))
md += ['', '## Variance polynomials', '```json', json.dumps(V, indent=1), '```', '', '## f-vectors of the 880 gems', '```json', json.dumps(fv, indent=1), '```']
open(f'{HERE}/appendix_data.md', 'w').write('\n'.join(md) + '\n')
print('witnesses', list(wit), '| variance keys', list(V)[:6], '| fvec entries', len(fv))
