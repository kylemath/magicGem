"""Monte Carlo for n = 3..8: sample moments of E_low / E_full vs exact theory, histograms,
and Kolmogorov distance to the Gaussian-limit weighted-chi^2 law.
Run:  python3.9 mc.py   (writes mc_results.json and mc_hist.npz)"""
import json, time, sys, os
import numpy as np
from multiprocessing import Pool
from energies import all_energies, random_arrangements
from theory import mean_energy_closed, variance_energy, weights_closed, gaussian_limit_variance

SAMPLES = {3: 100_000_000, 4: 100_000_000, 5: 100_000_000, 6: 100_000_000, 7: 100_000_000, 8: 100_000_000}
NBINS = 400
NWORK = 16
BATCH = 50_000


def hist_edges(n, key):
    # fixed edges from 0 to mean + 8 std (Gaussian-limit variance for the width)
    m = float(mean_energy_closed(n, key.split('_')[1] if key != 'E_full' else 'full'))
    return m


def worker(args):
    n, seed, nsamp, edges_low, edges_full = args
    rng = np.random.default_rng(seed)
    acc = {k: np.zeros(5) for k in ('E_low', 'E_full')}  # sum, sum^2, sum^3, sum^4, max
    hl = np.zeros(len(edges_low) - 1, dtype=np.int64)
    hf = np.zeros(len(edges_full) - 1, dtype=np.int64)
    nzero = {'E_low': 0, 'E_full': 0}
    # sorted sample subset for KS (keep 200k per worker)
    keep_l, keep_f = [], []
    done = 0
    while done < nsamp:
        B = min(BATCH, nsamp - done)
        arr = random_arrangements(n, B, rng)
        E = all_energies(arr)
        for k in ('E_low', 'E_full'):
            e = E[k]
            acc[k][0] += e.sum(); acc[k][1] += (e * e).sum(); acc[k][2] += (e ** 3).sum()
            acc[k][3] += (e ** 4).sum(); acc[k][4] = max(acc[k][4], e.max())
            nzero[k] += int((e < 1e-12).sum())
        hl += np.histogram(E['E_low'], bins=edges_low)[0]
        hf += np.histogram(E['E_full'], bins=edges_full)[0]
        if len(keep_l) * BATCH < 200_000:
            keep_l.append(E['E_low'].copy()); keep_f.append(E['E_full'].copy())
        done += B
    return acc, hl, hf, nzero, np.concatenate(keep_l), np.concatenate(keep_f)


def mixture_draws(n, which, rng, M=10_000_000):
    """Draws from the Gaussian-limit law sum_j w_j chi^2_1 (independent)."""
    out = np.zeros(M)
    for w, mult in weights_closed(n, which):
        g = rng.standard_normal((mult, M))
        out += float(w) * (g * g).sum(axis=0)
    return out


def ks_distance(a, b):
    """Two-sample Kolmogorov distance between sorted samples a, b."""
    a = np.sort(a); b = np.sort(b)
    grid = np.concatenate([a, b]); grid.sort()
    Fa = np.searchsorted(a, grid, side='right') / a.size
    Fb = np.searchsorted(b, grid, side='right') / b.size
    return float(np.abs(Fa - Fb).max())


def run_n(n, pool):
    t0 = time.time()
    nsamp = SAMPLES[n]
    res = {'n': n, 'n_samples': nsamp}
    edges = {}
    for key, which in (('E_low', 'low'), ('E_full', 'full')):
        m = float(mean_energy_closed(n, which)); s = float(gaussian_limit_variance(n, which)) ** 0.5
        edges[key] = np.linspace(0, m + 8 * s, NBINS + 1)
    per = nsamp // NWORK
    jobs = [(n, 1000 * n + w, per, edges['E_low'], edges['E_full']) for w in range(NWORK)]
    parts = pool.map(worker, jobs)
    hl = sum(p[1] for p in parts); hf = sum(p[2] for p in parts)
    keep = {'E_low': np.concatenate([p[4] for p in parts]), 'E_full': np.concatenate([p[5] for p in parts])}
    tot = per * NWORK
    rng = np.random.default_rng(777 + n)
    for key, which in (('E_low', 'low'), ('E_full', 'full')):
        S = sum(p[0][key] for p in parts)
        mean = S[0] / tot; m2 = S[1] / tot; var = m2 - mean ** 2
        m3 = S[2] / tot; m4 = S[3] / tot
        mu3 = m3 - 3 * mean * m2 + 2 * mean ** 3
        mu4 = m4 - 4 * mean * m3 + 6 * mean ** 2 * m2 - 3 * mean ** 4
        ex_mean = float(mean_energy_closed(n, which)); ex_var = float(variance_energy(n, which))
        g_var = float(gaussian_limit_variance(n, which))
        mix = mixture_draws(n, which, rng, M=4_000_000)
        ks = ks_distance(keep[key], mix)
        se_mean = (var / tot) ** 0.5
        res[key] = {
            'mc_mean': mean, 'mc_var': var, 'mc_std': var ** 0.5, 'mc_skew': mu3 / var ** 1.5,
            'mc_exkurt': mu4 / var ** 2 - 3,
            'mc_max': max(p[0][key][4] for p in parts), 'mc_n_zero': int(sum(p[3][key] for p in parts)),
            'exact_mean': ex_mean, 'exact_var': ex_var, 'gauss_limit_var': g_var,
            'rel_err_mean': mean / ex_mean - 1, 'rel_err_var': var / ex_var - 1,
            'rel_err_var_vs_gauss': var / g_var - 1,
            'mean_se': se_mean, 'mean_z': (mean - ex_mean) / se_mean,
            'ks_vs_gauss_limit': ks,
            'weights': [[float(w), int(mult)] for w, mult in weights_closed(n, which)],
            'mix_mean_check': float(mix.mean()), 'mix_var_check': float(mix.var()),
        }
    res['hist'] = {'E_low': hl, 'E_full': hf, 'edges_low': edges['E_low'], 'edges_full': edges['E_full']}
    res['runtime_s'] = time.time() - t0
    print(f"n={n}: {tot:,} samples in {res['runtime_s']:.1f}s; "
          f"E_low mean {res['E_low']['mc_mean']:.5f} vs {res['E_low']['exact_mean']:.5f}; "
          f"var {res['E_low']['mc_var']:.5f} vs {res['E_low']['exact_var']:.5f}; KS {res['E_low']['ks_vs_gauss_limit']:.4f}",
          flush=True)
    return res


if __name__ == '__main__':
    ns = [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6, 7, 8]
    out = {}
    hist = {}
    with Pool(NWORK) as pool:
        for n in ns:
            r = run_n(n, pool)
            h = r.pop('hist')
            for k, v in h.items():
                hist[f'n{n}_{k}'] = v
            out[str(n)] = r
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, 'mc_results.json'), 'w'), indent=1)
    np.savez(os.path.join(here, 'mc_hist.npz'), **hist)
    print('done')
