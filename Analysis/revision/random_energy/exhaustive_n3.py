"""Exhaustive n=3: exact distribution of E_low, E_full (symmetric), E_v4, E_asym over all 9!
arrangements, plus local-minimum counts under single swaps for each energy."""
import time
from fractions import Fraction as Fr
from itertools import permutations, combinations
import numpy as np
from collections import Counter
from energies import all_energies


def all_perms_n3():
    perms = np.fromiter((v for p in permutations(range(1, 10)) for v in p), dtype=np.int8,
                        count=9 * 362880).reshape(362880, 3, 3)
    return perms


def exact_counter(e, N2=81):
    """Energies for n=3 are rationals with denominator 81 (E*81 integer): count exactly."""
    q = np.rint(e * N2).astype(np.int64)
    assert np.allclose(q / N2, e, atol=1e-9)
    return Counter(q.tolist())


def summarize(e, name, N2=81):
    c = exact_counter(e, N2)
    mode_q, mode_cnt = max(c.items(), key=lambda kv: (kv[1], -kv[0]))
    # v4-style "peak": center of the maximal bin of a 200-bin histogram
    hist, edges = np.histogram(e, bins=200)
    peak_v4 = float(0.5 * (edges[np.argmax(hist)] + edges[np.argmax(hist) + 1]))
    return {
        'name': name,
        'count': int(e.size),
        'mean': float(e.mean()), 'mean_exact': str(Fr(int(np.rint(e.sum() * N2)), N2 * e.size)),
        'var': float(e.var()), 'std': float(e.std()),
        'var_exact': str(Fr(int(np.rint((e * e).sum() * N2 * N2)), N2 * N2 * e.size)
                         - Fr(int(np.rint(e.sum() * N2)), N2 * e.size) ** 2),
        'mode': mode_q / N2, 'mode_exact': f'{mode_q}/{N2}', 'mode_count': int(mode_cnt),
        'peak_200bin_histogram': peak_v4,
        'max': float(e.max()), 'max_exact': f'{int(np.rint(e.max() * N2))}/{N2}',
        'n_distinct_values': len(c),
        'n_zero': int((e < 1e-12).sum()),
        'median': float(np.median(e)),
    }


def local_minima(perms, energies_fn, tol=1e-12):
    """Number of arrangements for which no single swap strictly decreases the energy."""
    B = perms.shape[0]
    flat = perms.reshape(B, 9)
    e0 = energies_fn(perms)
    is_min = np.ones(B, dtype=bool)
    for a, b in combinations(range(9), 2):
        sw = flat.copy()
        sw[:, [a, b]] = sw[:, [b, a]]
        e1 = energies_fn(sw.reshape(B, 3, 3))
        is_min &= ~(e1 < e0 - tol)
    return is_min, e0


def run():
    t0 = time.time()
    perms = all_perms_n3()
    E = all_energies(perms)
    out = {'n': 3, 'n_arrangements': int(perms.shape[0])}
    for key in ('E_low', 'E_full', 'E_v4', 'E_asym'):
        out[key] = summarize(E[key], key)
    # note: for n=3 the paper's E_low and symmetric E_full are different functions; check equality?
    out['E_low_equals_E_full_pointwise'] = bool(np.allclose(E['E_low'], E['E_full']))
    out['n_lowmode_zero_but_not_full_zero'] = int(((E['E_low'] < 1e-12) & (E['E_full'] > 1e-12)).sum())
    # local minima
    lm = {}
    for key in ('E_low', 'E_full', 'E_v4', 'E_asym'):
        fn = lambda a, key=key: all_energies(a)[key]
        is_min, e0 = local_minima(perms, fn)
        n_glob = int(((e0 < 1e-12) & is_min).sum())
        vals = Counter(np.rint(e0[is_min] * 81).astype(int).tolist())
        lm[key] = {'total_local_minima': int(is_min.sum()), 'global_minima': n_glob,
                   'non_global_local_minima': int(is_min.sum()) - n_glob,
                   'local_min_energy_values_x81': {str(k): v for k, v in sorted(vals.items())}}
    out['local_minima'] = lm
    out['runtime_s'] = time.time() - t0
    return out, E


if __name__ == '__main__':
    import json
    out, E = run()
    print(json.dumps(out, indent=1))
