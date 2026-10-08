#!/usr/bin/env python3
"""Numerical checks for Section `Balance of the signed mass`.  Writes balance_results.json.
Run: python3 balance_check.py    (about 20 s)"""
import itertools, json, math, os
import numpy as np
from balance_lib import functionals, magic4_reps

HERE = os.path.dirname(os.path.abspath(__file__))
res = {}

# ---- n=3 exhaustive
P = np.array(list(itertools.permutations(range(1, 10))), float)
f3 = functionals(P, 3)
mag = f3['E_full'] < 1e-12
res['n3'] = {'n_magic': int(mag.sum())}
for k in ('B_lin', 'B_ring', 'B_3D_xy', 'V_3D', 'B_3D', 'P_xy', 'I_dev'):
    v = f3[k][mag]
    res['n3'][k] = {'min': float(v.min()), 'max': float(v.max())}
res['n3']['closed_form_B_ring'] = 2 * (2 - math.sqrt(2)) * math.sqrt(5)
# T2 bound exhaustively
viol = int((f3['T2_lhs'] > f3['T2_rhs'] + 1e-9).sum())
ratio = f3['T2_lhs'] / np.maximum(f3['T2_rhs'], 1e-12)
res['n3']['T2_violations'] = viol; res['n3']['T2_max_ratio'] = float(ratio[f3['T2_rhs'] > 0].max())
# ring balance over all arrangements: minimum
res['n3']['B_ring_min_over_all'] = float(f3['B_ring'].min())
res['n3']['B_ring_frac_below_magic'] = float((f3['B_ring'] < f3['B_ring'][mag].min() - 1e-12).mean())

# ---- n=4
reps, allm = magic4_reps(os.path.join(HERE, 'magic4_all7040.txt'))
rng = np.random.default_rng(20240607)
R = np.array([rng.permutation(16) + 1 for _ in range(300000)], float)
fm = functionals(reps, 4); fr = functionals(R, 4)
res['n4'] = {'n_magic_classes': len(reps), 'n_random': len(R), 'seed': 20240607}
res['n4']['random_E_full_mean'] = float(fr['E_full'].mean())
res['n4']['random_E_full_zero'] = int((fr['E_full'] < 1e-12).sum())
for k in ('B_lin', 'B_ring', 'B_3D_xy', 'V_3D', 'P_xy'):
    a, b = fm[k], fr[k]
    res['n4'][k] = {'magic_mean': float(a.mean()), 'magic_median': float(np.median(a)), 'magic_min': float(a.min()),
                    'magic_max': float(a.max()), 'random_mean': float(b.mean()), 'random_median': float(np.median(b)),
                    'random_p5': float(np.percentile(b, 5)),
                    'pct_rank_of_magic_mean': float((b <= a.mean()).mean() * 100),
                    'pct_rank_of_magic_median': float((b <= np.median(a)).mean() * 100),
                    'pct_rank_of_magic_max': float((b <= a.max()).mean() * 100)}
res['n4']['B_lin_random_zero_fraction'] = float((fr['B_lin'] < 1e-9).mean())
res['n4']['magic_with_B_ring_zero'] = int((fm['B_ring'] < 1e-9).sum())
viol = int((fr['T2_lhs'] > fr['T2_rhs'] + 1e-9).sum())
res['n4']['T2_violations'] = viol; res['n4']['T2_max_ratio'] = float((fr['T2_lhs'] / np.maximum(fr['T2_rhs'], 1e-12)).max())
res['n4']['spearman_E_vs'] = {}
from scipy.stats import spearmanr
for k in ('B_lin', 'B_ring', 'B_3D_xy', 'P_xy'):
    res['n4']['spearman_E_vs'][k] = float(spearmanr(fr['E_full'], fr[k])[0])
# explicit sharp T2 example (real-valued height): z=a(x)+b(y) with a=x, b=y
x = np.arange(4) - 1.5
zz = (np.tile(x, 4) + np.repeat(x[::-1], 4)) # z_ij = x_j + y_i
ex = functionals(zz[None, :] + 8.5, 4)
res['T2_sharp_real_example'] = float(ex['T2_lhs'][0] / ex['T2_rhs'][0])
# n=5,6 random: T2 check
for n in (5, 6, 7):
    Rn = np.array([rng.permutation(n * n) + 1 for _ in range(100000)], float)
    fn = functionals(Rn, n)
    res['T2_n%d' % n] = {'violations': int((fn['T2_lhs'] > fn['T2_rhs'] + 1e-9).sum()), 'max_ratio': float((fn['T2_lhs'] / np.maximum(fn['T2_rhs'], 1e-12)).max())}
# ---- extra checks: mixed moments, projection bound, relaxed gradient flow limit
x4 = np.tile(np.arange(4), 4) - 1.5; y4 = 1.5 - np.repeat(np.arange(4), 4)
Z = reps - 8.5
res['n4']['mixed_moments_over_880'] = {
    'xy': {'distinct_abs': int(len(np.unique(np.abs(Z @ (x4 * y4))))), 'nonzero': int((np.abs(Z @ (x4 * y4)) > 1e-9).sum())},
    'x2y': {'nonzero': int((np.abs(Z @ (x4 ** 2 * y4)) > 1e-9).sum())},
    'xy2': {'nonzero': int((np.abs(Z @ (x4 * y4 ** 2)) > 1e-9).sum())}}
DUR = np.array([16, 3, 2, 13, 5, 10, 11, 8, 9, 6, 7, 12, 4, 15, 14, 1], float)
res['durer'] = {'P_xy_sum_z_xy': float((DUR - 8.5) @ (x4 * y4)), 'B_ring': float(functionals(DUR[None, :], 4)['B_ring'][0]),
                'B_3D_xy': float(functionals(DUR[None, :], 4)['B_3D_xy'][0]), 'V_3D': float(functionals(DUR[None, :], 4)['V_3D'][0])}
# projection bound ||P_W z||^2 <= n^2/(n-2) E_full  (normalised inner product (1/N) sum), and relaxed gradient-flow limit
from balance_lib import geometry
for n in (3, 4, 5):
    N = n * n; xg, yg, Lg = geometry(n)
    Lc = Lg - Lg.mean(1, keepdims=True)
    Q, _ = np.linalg.qr(Lc.T)           # orthonormal basis of W (rank 2n; QR keeps 2n+2 columns, drop null ones)
    U, sv, _ = np.linalg.svd(Lc.T, full_matrices=False)
    Wb = U[:, sv > 1e-9]; assert Wb.shape[1] == 2 * n
    Rn = np.array([rng.permutation(N) + 1 for _ in range(20000)], float)
    z = Rn - (N + 1) / 2
    PW = z @ Wb @ Wb.T
    pn = (PW ** 2).sum(1) / N
    Ef = functionals(Rn, n)['E_full']
    res['projection_bound_n%d' % n] = {'max_ratio_PWz2_over_Efull': float((pn / Ef).max()), 'min_ratio': float((pn / Ef).min()), 'bound_n2_over_n_minus_2': n * n / (n - 2)}
    if n == 4:
        zinf = z - PW                                  # limit of the gradient flow  dz/dt = -grad E_full  (linear flow)
        fi = functionals(zinf + (N + 1) / 2, n)
        fz = functionals(Rn, n)
        res['flow_limit_n4'] = {'E_full': float(fi['E_full'].max()), 'B_lin': float(fi['B_lin'].max()),
                                'B_ring_start_mean': float(fz['B_ring'].mean()), 'B_ring_end_mean': float(fi['B_ring'].mean()),
                                'B_3D_xy_start_mean': float(fz['B_3D_xy'].mean()), 'B_3D_xy_end_mean': float(fi['B_3D_xy'].mean()),
                                'norm_ratio_z_end_over_start_mean': float(np.sqrt(((zinf ** 2).sum(1) / (z ** 2).sum(1))).mean())}
json.dump(res, open(os.path.join(HERE, 'balance_results.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
