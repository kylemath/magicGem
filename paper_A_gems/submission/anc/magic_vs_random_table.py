"""
magic_vs_random_table.py -- writes magic_vs_random.tex (Table 4 of the paper) from magic_vs_random.json
(produced by magic_vs_random.py) and prints the order-five numbers quoted in the text of Section 5.3.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'magic_vs_random.json')))
A = R['n4']
ROWS = [('V', r'vertices $V$', 3), ('Vint', r'interior points $V^\circ$', 3), ('Vbd', r'non-vertex boundary points $V^\partial$', 3),
        ('Flow', 'lower facets', 3), ('vol', 'volume', 2),
        ('cnorm', r'distance of the solid centroid from $\mathbf 0$', 3),
        ('iso', r'fraction with $\operatorname{Iso}(\mathcal G)\ne\{\mathrm{id}\}$', 3)]
# the vertical facets and the tilt are quoted in the text only (printed below; all values are in magic_vs_random.json)
EXTRA = ['Fup', 'Fvert', 'tilt']
lines = [r'\begin{tabular}{l rrrr rr}', r'\toprule',
         r' & random & first moments $0$ & semi-magic & magic & \multicolumn{2}{c}{$d$, magic $-$ semi-magic}\\',
         r'\cmidrule(lr){6-7}',
         r'invariant & \multicolumn{3}{c}{(estimates, $10^5$ samples each)} & (exact) & all & not s.-c.\\', r'\midrule']
for k, name, dig in ROWS:
    vals = []
    for g in ('R', 'F', 'SM', 'M'):
        v = A[g][k]['mean'] - (1 if k == 'iso' else 0)        # mean of |Iso| - 1: the fraction if |Iso| <= 2, an upper bound for it in general
        vals.append(f'{v:.{dig}f}')
    if k == 'iso':
        d1 = d2 = '--'
    else:
        d1 = f"${A['M_vs_SM'][k]['d']:+.2f}$"; d2 = f"${A['Mnsc_vs_SMnsc'][k]['d']:+.2f}$"
    lines.append(f'{name} & ' + ' & '.join(vals) + f' & {d1} & {d2}\\\\')
lines += [r'\bottomrule', r'\end{tabular}']
open(os.path.join(HERE, 'magic_vs_random.tex'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
# standard errors and the uncertainty of d, for the caption
se = {k: max(A[g][k]['se'] for g in ('R', 'F', 'SM')) for k, _, _ in ROWS}
print('max SE of the sampled means:', {k: round(v, 4) for k, v in se.items()})
print('SE of d (magic - semi-magic):', round(max(A['M_vs_SM'][k]['d_se'] for k, _, _ in ROWS if k != 'iso'), 3),
      '(not s.-c.):', round(max(A['Mnsc_vs_SMnsc'][k]['d_se'] for k, _, _ in ROWS if k != 'iso'), 3))
for k in EXTRA:
    print(f'{k}: means', {g: round(A[g][k]['mean'], 3) for g in ('R', 'F', 'SM', 'M')}, 'max SE', round(max(A[g][k]['se'] for g in ('R', 'F', 'SM')), 4),
          'd(F-R)', round(A['F_vs_R'][k]['d'], 2), 'd(M-SM)', round(A['M_vs_SM'][k]['d'], 2))
print('magic - random, d:', {k: round(A['M_vs_R'][k]['d'], 2) for k, _, _ in ROWS if k != 'iso'})
print('first moments 0 - random, d:', {k: round(A['F_vs_R'][k]['d'], 2) for k, _, _ in ROWS if k != 'iso'})
print('semi-magic - first moments 0, d:', {k: round(A['SM_vs_F'][k]['d'], 2) for k, _, _ in ROWS if k != 'iso'})
print('annealed - uniform semi-magic, |z| max:', round(max(abs(A['SMa_vs_SM'][k]['z']) for k, _, _ in ROWS), 2),
      'sizes', A['SMa']['size'], A['SM']['size'])
print('mean |Iso| - 1 (fraction with nontrivial isometry, or an upper bound for it): R', A['R']['iso']['mean'] - 1, 'F', A['F']['iso']['mean'] - 1,
      'SM', A['SM']['iso']['mean'] - 1, 'self-compl. SM', A['SM']['sc']['mean'], 'M', A['M']['iso']['mean'] - 1)
print('magic - semi-magic, not s.-c.: V diff', A['Mnsc_vs_SMnsc']['V']['diff'], '+-', A['Mnsc_vs_SMnsc']['V']['se'])
# exact mean vertex counts of the magic squares by symmetry type (symmetry_880.json; D4 acts freely, so class means
# are the means over the 7040 squares), and the excess of the non-self-complementary magic squares over random arrangements
S880 = json.load(open(os.path.join(HERE, 'symmetry_880.json')))
mean = lambda L: sum(L) / len(L)
Vsc = [r['f_vector'][0] for r in S880 if r['self_comp']]
Vnsc = [r['f_vector'][0] for r in S880 if not r['self_comp']]
Vas = [r['f_vector'][0] for r in S880 if r['assoc']]
assert abs(mean(Vsc + Vnsc) - A['M']['V']['mean']) < 1e-12
print(f"magic V means: self-compl. {mean(Vsc):.3f} ({len(Vsc)}), associative {mean(Vas):.3f} ({len(Vas)}), "
      f"not self-compl. {mean(Vnsc):.3f} ({len(Vnsc)}); not s.-c. magic - random {mean(Vnsc) - A['R']['V']['mean']:+.3f} "
      f"+- {A['R']['V']['se']:.3f} = {100 * (mean(Vnsc) - A['R']['V']['mean']) / A['M_vs_R']['V']['diff']:.0f}% of the excess "
      f"{A['M_vs_R']['V']['diff']:.3f}")
if 'n5' in R:
    B = R['n5']
    for k in ('V', 'Vint', 'Vbd', 'Flow', 'Fvert', 'vol', 'cnorm', 'tilt', 'iso'):
        print(f"n=5 {k}: " + ', '.join(f"{g} {B[g][k]['mean']:.3f}+-{B[g][k]['se']:.3f}" for g in ('R5', 'F5', 'SM5', 'M5'))
              + '; M5-R5 ' + f"{B['M5_vs_R5'][k]['diff']:+.3f}+-{B['M5_vs_R5'][k]['se']:.3f} (d {B['M5_vs_R5'][k]['d']:+.2f})"
              + '; M5-SM5 ' + f"{B['M5_vs_SM5'][k]['diff']:+.3f}+-{B['M5_vs_SM5'][k]['se']:.3f} (d {B['M5_vs_SM5'][k]['d']:+.2f})")
    print('n=5 sizes', {g: B[g]['size'] for g in ('R5', 'F5', 'SM5', 'M5')})
    # n = 5 has at most four vertical facets; a gem has three or four, so the deficit of the mean counts the gems with three
    # (consistent with the stored standard deviations, which equal those of a 0/1 variable with these counts)
    three = {g: round(B[g]['size'] * (4 - B[g]['Fvert']['mean'])) for g in ('R5', 'F5', 'SM5', 'M5')}
    for g in three:
        p = three[g] / B[g]['size']; sd = (p * (1 - p) * B[g]['size'] / (B[g]['size'] - 1)) ** 0.5
        assert abs(sd - B[g]['Fvert']['sd']) < 1e-9
    print('n=5 gems with three vertical facets:', three, 'total', sum(three.values()), 'of', sum(B[g]['size'] for g in three))
