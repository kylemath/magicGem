"""Merge the three result files into results.json and emit LaTeX table rows."""
import json, os
from math import gcd
from functools import reduce
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(f'{HERE}/results_geometry.json'))
S = json.load(open(f'{HERE}/results_swaps_siamese.json'))
P = json.load(open(f'{HERE}/results_siamese_proof.json'))

# per-V summary table
byV = defaultdict(lambda: dict(n=0, fvecs=Counter(), types=set(), vols=set()))
for g in G['per_gem']:
    V, E, F = g['f_vector']
    r = byV[V]; r['n'] += 1; r['fvecs'][(E, F)] += 1; r['types'].add(g['combinatorial_type']); r['vols'].add(g['volume'])
summary_by_V = {V: dict(n_squares=r['n'], f_vectors={f'({V},{E},{F})': c for (E, F), c in sorted(r['fvecs'].items())},
                        n_combinatorial_types=len(r['types']), n_distinct_volumes=len(r['vols'])) for V, r in sorted(byV.items())}

out = dict(
    description='Geometry of the 880 essentially different 4x4 Magic Gems, exact swap-gap verification, Siamese gems.',
    conventions='x=j-(n-1)/2, y=(n-1)/2-i, z=s_ij-(N+1)/2; symmetric E_full over all 2n+2 lines; exact rational arithmetic.',
    geometry_880={k: v for k, v in G.items() if k != 'per_gem'},
    summary_by_vertex_count=summary_by_V,
    swap_gaps=S,
    siamese_proof=P,
)
with open(f'{HERE}/results.json', 'w') as f:
    json.dump(out, f, indent=1)

# ---- LaTeX helpers
def poly_tex(s):
    """'1 + -2m + 1m^2' -> '1-2m+m^2'"""
    s = s.replace(' + -', '-').replace(' + ', '+')
    s = s.replace('+1m', '+m').replace('-1m', '-m')
    if s.startswith('1m'): s = s[1:]
    return s

print('% per-V table')
for V, r in summary_by_V.items():
    fv = ', '.join(f'{k}:{c}' for k, c in r['f_vectors'].items())
    print(f"{V} & {r['n_squares']} & {r['n_combinatorial_types']} & {r['n_distinct_volumes']} & {fv} \\\\")
print('% Dudeney table')
for g in range(1, 13):
    c = G['dudeney_vs_vertex_count'][str(g)]
    row = ' & '.join(str(c.get(str(V), '')) for V in range(8, 17))
    print(f"{g} & {G['dudeney_group_sizes'][str(g)]} & {row} & {G['dudeney_n_types'][str(g)]} \\\\")
print('% plane table')
for pl in P['planes']:
    print(f"${poly_tex(pl['normal'][0])}$ & ${poly_tex(pl['normal'][1])}$ & ${poly_tex(pl['normal'][2])}$ & ${poly_tex(pl['offset'])}$ & {', '.join(pl['cycle']).replace('v','v_')} \\\\")
print('% vertex table')
for k, c in P['vertex_cells'].items():
    print(k, c['i'], c['j'], c['x'], c['y'], c['zeta'], c['values'])
