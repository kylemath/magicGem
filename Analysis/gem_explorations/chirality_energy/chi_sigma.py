"""Task 4a: exact Minkowski central-symmetry measure sigma(P)=vol((P-P)/2)/vol(P) for all 880 gems."""
import json
from common import *
from scipy.stats import spearmanr, mannwhitneyu
sym = json.load(open('/Users/kylemathewson/magicGem/paper_A_gems/anc/symmetry_880.json'))
res = []
for k in range(880):
    P = scaled_points(SQ[k])
    v6, nv = hull_int(P)
    # (P-P): pairwise differences (doubled coords of 2*(p-q)/... ) ; (P-P)/2 has volume vol(P-P)/8 ; do it in integers
    D = (P[:, None, :] - P[None, :, :]).reshape(-1, 3)
    d6, _ = hull_int(D)
    sigma = Fraction(d6, 8 * v6)         # vol(P-P)/(8 vol P)
    # sanity: P-P is centrally symmetric
    assert d6 >= 8 * v6 if True else None
    # self-check complement invariance: complement gem = z-reflection
    Pc = P.copy(); Pc[:, 2] *= -1
    Dc = (Pc[:, None, :] - Pc[None, :, :]).reshape(-1, 3)
    v6c, _ = hull_int(Pc); d6c, _ = hull_int(Dc)
    assert v6c == v6 and d6c == d6
    res.append(dict(index=k, vol=str(vol_real(v6)), nverts=nv, sigma=str(sigma), sigma_f=float(sigma),
                    group=sym[k]['group'], assoc=sym[k]['assoc'], self_comp=sym[k]['self_comp']))
sg = np.array([r['sigma_f'] for r in res]); grp = np.array([r['group'] for r in res])
vol = np.array([float(Fraction(r['vol'])) for r in res]); nv = np.array([r['nverts'] for r in res])
exact1 = [r['sigma'] == '1' for r in res]
assert all(e == (r['group'] == 'Ci') for e, r in zip(exact1, res))
assert sum(exact1) == 48 and (sg[grp != 'Ci'] > 1).all()
out = dict(n_sigma_exactly_1=sum(exact1), min_nonassoc=float(sg[grp!='Ci'].min()), max=float(sg.max()),
  mean_by_group={g: float(sg[grp==g].mean()) for g in ['Ci','C2','C1']},
  median_by_group={g: float(np.median(sg[grp==g])) for g in ['Ci','C2','C1']},
  quantiles_all=dict(zip(['0','5','25','50','75','95','100'], np.percentile(sg,[0,5,25,50,75,95,100]).tolist())),
  mannwhitney_C2_vs_C1_p=float(mannwhitneyu(sg[grp=='C2'], sg[grp=='C1']).pvalue),
  spearman_sigma_nverts_nonassoc=float(spearmanr(sg[grp!='Ci'], nv[grp!='Ci'])[0]),
  spearman_sigma_vol_nonassoc=float(spearmanr(sg[grp!='Ci'], vol[grp!='Ci'])[0]),
  spearman_sigma_nverts_all=float(spearmanr(sg, nv)[0]), spearman_sigma_vol_all=float(spearmanr(sg, vol)[0]))
# pairs (S,17-S): index of complement gem congruent class -> by mirror: sigma equal (asserted above on the reflected point set)
order = np.argsort(-sg)
out['top10_most_asymmetric'] = [dict(index=int(i), sigma=float(sg[i]), nverts=int(nv[i]), vol=float(vol[i]), group=grp[i], square=SQ[i].tolist()) for i in order[:10]]
nz = [i for i in np.argsort(sg) if grp[i] != 'Ci'][:10]
out['top10_least_asymmetric_nonassoc'] = [dict(index=int(i), sigma=float(sg[i]), nverts=int(nv[i]), group=grp[i], square=SQ[i].tolist()) for i in nz]
json.dump(dict(summary=out, per_gem=res), open('results_sigma.json', 'w'), indent=1)
print(json.dumps(out, indent=1)[:3500])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
bins = np.linspace(1, sg.max()*1.01, 40)
for g, c in [('Ci','tab:green'),('C2','tab:blue'),('C1','tab:orange')]:
    ax[0].hist(sg[grp==g], bins=bins, alpha=.7, label=f'{g} ({(grp==g).sum()})', color=c)
ax[0].set_xlabel(r'$\sigma=\mathrm{vol}((P-P)/2)/\mathrm{vol}(P)$'); ax[0].set_ylabel('gems'); ax[0].legend()
ax[1].scatter(nv + np.random.default_rng(0).uniform(-.2,.2,880), sg, s=6); ax[1].set_xlabel('vertex count'); ax[1].set_ylabel(r'$\sigma$')
ax[2].scatter(vol, sg, s=6, c=[{'Ci':'g','C2':'b','C1':'orange'}[g] for g in grp]); ax[2].set_xlabel('volume'); ax[2].set_ylabel(r'$\sigma$')
plt.tight_layout(); plt.savefig('fig_sigma.png', dpi=130)
