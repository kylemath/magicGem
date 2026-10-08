"""Assemble results.json from: theory.py (closed forms, Gram/covariance matrices, weights),
exhaustive_n3.py, mc_results.json, algo_results.json, variance_fits.json."""
import json, os, time
from fractions import Fraction as Fr
import numpy as np
from theory import (mean_energy, mean_energy_closed, covariance_matrix_T, weights_closed,
                    weights_numeric, gaussian_limit_variance)
from fit_variance import exact_var
from exhaustive_n3 import run as run_n3

HERE = os.path.dirname(os.path.abspath(__file__))


def fr(x):
    return {'exact': str(x), 'float': float(x)}


def main():
    t0 = time.time()
    out = {'conventions': {
        'N': 'n^2', 'x_ij': 'j-(n-1)/2', 'y_ij': '(n-1)/2-i', 'z_ij': 's_ij-(N+1)/2',
        'Cov(phi,Z)': '(1/N) sum_c (phi_c - mean phi) z_c',
        'E_low': 'Cov(X,Z)^2+Cov(Y,Z)^2+Cov(Dm,Z)^2+Cov(Da,Z)^2',
        'E_full': 'sum_{k=0}^{n-1} Cov(R_k,Z)^2 + sum_{l=0}^{n-1} Cov(C_l,Z)^2 + Cov(Dm,Z)^2 + Cov(Da,Z)^2 (symmetric, 2n+2 terms)',
        'E_v4': 'Cov(X,Z)^2+Cov(Y,Z)^2+(mean diag - mu)^2+(mean antidiag - mu)^2 = E_xy + n^2 E_diag (v4 code: compute_total_energy_vectorized)',
        'E_asym': 'E_full with row n-1 and column n-1 omitted (v4 code: compute_full_magic_energy)'}}
    # ---- closed forms
    out['closed_forms'] = {
        'Var(Z)': '(N^2-1)/12', 'sigma2 := Var(Z)/(N-1)': '(N+1)/12',
        'E[Cov(phi,Z)^2]': 'Var_grid(phi) Var(Z)/(N-1) = Var_grid(phi) (N+1)/12',
        'Cov(Cov(phi,Z),Cov(psi,Z))': 'Cov_grid(phi,psi) (N+1)/12',
        'E[Cov(X,Z)^2]': '(n^4-1)/144',
        'E[Cov(D,Z)^2]': '(n-1)(n^2+1)/(12 n^2)  [= n(N-n)Var(Z)/((N-1)N^2)]',
        'E[Cov(R_k,Z)^2]': '(n-1)(n^2+1)/(12 n^2)',
        'E[E_low]': '(n^2+1)/12 * [ (n^2-1)/6 + 2(n-1)/n^2 ] = (n^2+1)(n^4 - n^2 + 12 n - 12)/(72 n^2)',
        'E[E_full]': '(n^4-1)/(6 n^2)',
        'E[E_v4]': '(n^2+1)/12 * [ (n^2-1)/6 + 2(n-1) ]',
        'E[E_asym]': '(n^2+1)(n-1)/(6 n)',
        'E_low_leading': 'n^4/72', 'E_full_leading': 'n^2/6',
        'Gram_low': 'diag(Var X, Var Y, Var D, Var D) with Var X = Var Y = (n^2-1)/12, Var D = (n-1)/n^2; '
                    'Cov_grid(Dm,Da) = 0 (n odd) or -1/n^2 (n even); all other cross terms 0',
        'Gram_full': 'rows block (1/n)(I - J/n), cols block (1/n)(I - J/n), zero cross terms between rows/cols/diagonals, '
                     'diagonal 2x2 block [[(n-1)/n^2, c],[c,(n-1)/n^2]] with c = 0 (n odd), -1/n^2 (n even)',
        'weights_low': 'sigma2 * {(n^2-1)/12 (x2), (n-1)/n^2 (x2)} for n odd; sigma2 * {(n^2-1)/12 (x2), 1/n, (n-2)/n^2} for n even',
        'weights_full': 'sigma2 * {1/n (x 2(n-1)), (n-1)/n^2 (x2)} for n odd; sigma2 * {1/n (x 2n-1), (n-2)/n^2} for n even',
        'gaussian_limit_var': '2 sum_j w_j^2 (multiplicity-weighted)',
    }
    vf = json.load(open(os.path.join(HERE, 'variance_fits.json')))
    out['exact_variance_rational_functions'] = {w: {p: {'expr': vf[w][p]['expr'], 'latex': vf[w][p]['latex'],
                                                         'leading_order_in_n': vf[w][p]['leading_order'],
                                                         'leading_coeff': vf[w][p]['leading_coeff'],
                                                         'verified_on_extra_orders': vf[w][p]['verified_on_extra_points']}
                                                     for p in ('odd', 'even')} for w in ('low', 'full')}
    # ---- per-n exact table
    tab = {}
    for n in range(3, 13):
        d = {}
        for which in ('low', 'full', 'v4', 'asym'):
            m = mean_energy_closed(n, which)
            if which != 'v4':
                assert m == mean_energy(n, which), (n, which)
            d[which] = {'mean': fr(m)}
            if which in ('low', 'full'):
                v = exact_var(n, which)
                d[which]['var'] = fr(v)
                d[which]['std'] = float(v) ** 0.5
                d[which]['gauss_limit_var'] = fr(gaussian_limit_variance(n, which))
                d[which]['var_over_gauss_limit_var'] = float(v / gaussian_limit_variance(n, which))
                wc = weights_closed(n, which)
                wn = weights_numeric(n, which)
                wc_flat = sorted([float(w) for w, mult in wc for _ in range(mult)], reverse=True)
                assert np.allclose(wc_flat, wn[:len(wc_flat)]) and np.allclose(wn[len(wc_flat):], 0, atol=1e-12)
                d[which]['weights'] = [[str(w), mult] for w, mult in wc]
        tab[str(n)] = d
    out['exact_moments_by_n'] = tab
    # exact covariance matrix for E_low, n=3..6
    out['covariance_matrix_T_low'] = {}
    for n in (3, 4, 5, 6):
        names, S = covariance_matrix_T(n, 'low')
        out['covariance_matrix_T_low'][str(n)] = {'names': names, 'matrix': [[str(x) for x in row] for row in S]}
    # ---- exhaustive n=3
    n3, _ = run_n3()
    out['exhaustive_n3'] = n3
    out['v4_discrepancy'] = {
        'v4_reported': {'mean': 4.44, 'std': 2.51, 'mode': 3.12, 'max': 12.10,
                        'local_minima_E_full': 24, 'local_minima_E_low': 344},
        'reproduced_by': {
            'mean 4.44 = 40/9, std 2.51, max 12.10 = 980/81': 'E_v4 (diagonal terms (mean diag - mu)^2 = n^2 Cov(D,Z)^2)',
            'mode 3.12': 'E_v4, center of the maximal bin of a 200-bin histogram (exact mode of E_v4 is 230/81 = 2.840)',
            '24 local minima': 'E_asym (rows/cols n-1 dropped), not D4-invariant',
            '344 local minima': 'E_low as defined in the paper (Cov(D,Z)^2 terms)'},
        'correct_values_paper_definition': {
            'E_low': {'mean': '40/27 = 1.4815', 'std': n3['E_low']['std'], 'var': '1532/2187', 'mode': '90/81 = 1.111 (5216 arrangements)',
                      'max': '360/81 = 4.444', 'zeros': 8, 'local_minima': 344, 'non_global_local_minima': 336},
            'E_full_symmetric': {'mean': '40/27 = 1.4815', 'std': n3['E_full']['std'], 'var': '398/2187', 'mode': '138/81 = 1.704 (8736 arrangements)',
                                 'max': '180/81 = 2.222', 'zeros': 8, 'local_minima': 16, 'non_global_local_minima': 8,
                                 'non_global_local_min_energy': '2/81 (all 8)'}}}
    # ---- MC and algorithms
    mc = json.load(open(os.path.join(HERE, 'mc_results.json')))
    out['monte_carlo'] = mc
    out['algorithms'] = json.load(open(os.path.join(HERE, 'algo_results.json')))
    out['runtimes_s'] = {'exhaustive_n3': n3['runtime_s'],
                         'monte_carlo_total': sum(mc[k]['runtime_s'] for k in mc),
                         'algorithms_total': out['algorithms']['total_runtime_s'],
                         'variance_fits': vf['runtime_s'], 'assemble': time.time() - t0}
    json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
    print('results.json written', time.time() - t0)


if __name__ == '__main__':
    main()
