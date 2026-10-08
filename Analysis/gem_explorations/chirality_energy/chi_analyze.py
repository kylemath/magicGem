import json
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu
r = json.load(open('results_chi_overlap.json')); s = json.load(open('results_sigma.json'))
chi = np.array(r['chi']); grp = np.array(r['group']); part = np.array(r['partner'])
sg = np.array([g['sigma_f'] for g in s['per_gem']]); vol = np.array([float(__import__('fractions').Fraction(g['vol'])) for g in s['per_gem']])
nv = np.array([g['nverts'] for g in s['per_gem']])
out = {}
out['chi_by_group'] = {g: dict(n=int((grp==g).sum()), min=float(chi[grp==g].min()), median=float(np.median(chi[grp==g])), max=float(chi[grp==g].max())) for g in ['Ci','C2','C1']}
out['Ci_max_chi'] = float(chi[grp=='Ci'].max())
diff = np.abs(chi - chi[part]); out['partner_invariance'] = dict(max_abs_diff=float(diff.max()), median=float(np.median(diff)), n_self=int((part==np.arange(880)).sum()), frac_within_1em3=float((diff<1e-3).mean()))
out['quantiles_nonCi'] = np.percentile(chi[grp!='Ci'], [0,5,25,50,75,95,100]).tolist()
out['spearman_chi_sigma_nonCi'] = float(spearmanr(chi[grp!='Ci'], sg[grp!='Ci'])[0]); out['spearman_chi_sigma_all'] = float(spearmanr(chi, sg)[0])
out['spearman_chi_vol_nonCi'] = float(spearmanr(chi[grp!='Ci'], vol[grp!='Ci'])[0]); out['spearman_chi_nv_nonCi'] = float(spearmanr(chi[grp!='Ci'], nv[grp!='Ci'])[0])
out['mannwhitney_C2_vs_C1_p'] = float(mannwhitneyu(chi[grp=='C2'], chi[grp=='C1']).pvalue)
o = np.argsort(-chi)[:5]; out['top5_chi'] = [dict(index=int(i), chi=float(chi[i]), group=grp[i], sigma=float(sg[i])) for i in o]
o = [i for i in np.argsort(chi) if grp[i] != 'Ci'][:5]; out['bottom5_chi_nonCi'] = [dict(index=int(i), chi=float(chi[i]), group=grp[i], sigma=float(sg[i])) for i in o]
json.dump(out, open('results_chi_summary.json', 'w'), indent=1); print(json.dumps(out, indent=1))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
c = {'Ci':'g','C2':'b','C1':'orange'}
ax[0].scatter(sg, chi, s=6, c=[c[g] for g in grp]); ax[0].set_xlabel(r'$\sigma$ (Minkowski)'); ax[0].set_ylabel(r'$\chi$ (overlap, numerical)')
ax[1].scatter(chi, chi[part], s=6); ax[1].plot([0,.4],[0,.4],'k-',lw=.5); ax[1].set_xlabel(r'$\chi(S)$'); ax[1].set_ylabel(r'$\chi(17-S)$')
ax[2].scatter(vol, chi, s=6, c=[c[g] for g in grp]); ax[2].set_xlabel('volume'); ax[2].set_ylabel(r'$\chi$')
plt.tight_layout(); plt.savefig('fig_chi.png', dpi=130)
