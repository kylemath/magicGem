"""Task 6a: single swaps of magic squares: gem volume change vs d^2 m (energy), d, cell positions."""
import json, itertools
from common import *
from scipy.stats import spearmanr, pearsonr
n = 4; N = 16
# lines: 4 rows,4 cols,2 diags as lists of cell indices
lines = [[4*i+j for j in range(4)] for i in range(4)] + [[4*i+j for i in range(4)] for j in range(4)] \
      + [[5*i for i in range(4)], [3*(i+1) for i in range(4)]]
Lmat = np.zeros((10, 16), int)
for l, L in enumerate(lines): Lmat[l, L] = 1
def F(flat): return int(((Lmat @ flat - 34) ** 2).sum())
cell_pts = scaled_points(np.arange(1, 17).reshape(4, 4))  # x,y per cell; z replaced
XY = cell_pts[:, :2]
rng = np.random.default_rng(1)
idx = np.sort(rng.choice(880, 100, replace=False))
rows = []
for k in idx:
    flat = SQ[k].ravel().copy()
    P0 = np.c_[XY, 2 * flat - 17]
    v0, nv0 = hull_int(P0)
    assert F(flat) == 0
    for a, b in itertools.combinations(range(16), 2):
        f2 = flat.copy(); f2[a], f2[b] = f2[b], f2[a]
        P = np.c_[XY, 2 * f2 - 17]
        v, nv = hull_int(P)
        d = int(flat[b] - flat[a])
        dF = F(f2)
        m = int(((Lmat[:, a] + Lmat[:, b]) == 1).sum())
        assert dF == d * d * m   # swap formula (u=0 for magic)
        rows.append((k, a, b, d, m, dF, v - v0, nv - nv0, int(v0), int(nv0)))
R = np.array(rows)
np.save('swaps_raw.npy', R)
dV = R[:, 6] / 48.0  # volume change in real units
dF = R[:, 5]; d = np.abs(R[:, 3]); m = R[:, 4]; dnv = R[:, 7]
out = dict(n_squares=100, n_swaps=len(R), sample_indices=idx.tolist(),
  frac_swaps_volume_decreases=float((R[:,6] < 0).mean()), frac_volume_increases=float((R[:,6] > 0).mean()), frac_zero=float((R[:,6]==0).mean()),
  mean_dV=float(dV.mean()), sd_dV=float(dV.std()),
  spearman_dV_dF=float(spearmanr(dV, dF)[0]), spearman_dV_d2m_pearson=float(pearsonr(dV, dF)[0]),
  spearman_absdV_dF=float(spearmanr(np.abs(dV), dF)[0]),
  spearman_dV_absd=float(spearmanr(dV, d)[0]), spearman_absdV_absd=float(spearmanr(np.abs(dV), d)[0]),
  spearman_dV_m=float(spearmanr(dV, m)[0]),
  spearman_dnv_dF=float(spearmanr(dnv, dF)[0]),
  mean_dnv=float(dnv.mean()), frac_dnv_pos=float((dnv>0).mean()), frac_dnv_neg=float((dnv<0).mean()))
# partial: within fixed m
out['spearman_dV_dF_within_m'] = {int(mm): float(spearmanr(dV[m==mm], dF[m==mm])[0]) for mm in np.unique(m) if (m==mm).sum() > 50}
# position dependence: dV by cell-pair radial distance and by whether swap involves corners/centre
r2 = (XY[:,0]**2 + XY[:,1]**2)
rad_a = r2[R[:,1].astype(int)]; rad_b = r2[R[:,2].astype(int)]
out['spearman_dV_vs_zdiff_times_radialdiff'] = float(spearmanr(dV, (R[:,3]) * (rad_a - rad_b))[0])
# a signed model: moving big value outward (to larger radius) enlarges the hull
sgn = R[:,3] * (rad_b - rad_a)   # value d=s_b-s_a: if b is farther out, it gains d
out['spearman_dV_vs_d_times_radius_gain'] = float(spearmanr(dV, sgn)[0])
# linear regression dV ~ d^2 m, |d|, d*(r2b-r2a)
X = np.c_[np.ones(len(R)), dF, d, sgn, R[:,3]*0+1*(m)]
beta, res, *_ = np.linalg.lstsq(X[:, :4], dV, rcond=None)
pred = (X[:, :4] * beta).sum(1)
out['ols_dV_on_[1,d2m,|d|,d*radialgain]'] = dict(beta=beta.tolist(), R2=float(1 - ((dV-pred)**2).sum() / ((dV-dV.mean())**2).sum()))
dd = R[:,3].astype(int); ad = np.abs(dd)
out['spearman_dV_dF_within_absd'] = {int(x): float(spearmanr(dV[ad==x], dF[ad==x])[0]) for x in np.unique(ad) if (ad==x).sum()>200 and len(np.unique(dF[ad==x]))>1}
out['mean_dV_by_absd'] = {int(x): float(dV[ad==x].mean()) for x in np.unique(ad)}
out['mean_dV_by_m'] = {int(x): float(dV[m==x].mean()) for x in np.unique(m)}
# by cell-class of the swap: vertex-count change by pair type
json.dump(out, open('results_swaps.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
j = np.random.default_rng(0).uniform(-.3,.3,len(R))
ax[0].scatter(dF, dV, s=2, alpha=.3); ax[0].set_xlabel(r'$N^2\Delta E=d^2m$'); ax[0].set_ylabel(r'$\Delta$ hull volume')
ax[1].scatter(d + j, dV, s=2, alpha=.3); ax[1].set_xlabel('|d|'); ax[1].set_ylabel(r'$\Delta$ hull volume')
ax[2].scatter(sgn, dV, s=2, alpha=.3); ax[2].set_xlabel(r'$d\,(r_b^2-r_a^2)$ (doubled coords)'); ax[2].set_ylabel(r'$\Delta$ hull volume')
plt.tight_layout(); plt.savefig('fig_swaps.png', dpi=130)
