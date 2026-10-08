"""Small algorithmic experiment: greedy (steepest) swap descent and simulated annealing on the
symmetric E_full, starting from uniformly random arrangements, n = 4, 5, 6.
F := N^2 E_full = sum over the 2n+2 lines of (line sum - M)^2, an integer; F = 0 iff magic.
Run: python3.9 algorithms.py  (writes algo_results.json)"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool

RUNS_GREEDY = 200000
RUNS_SA = 400
NWORK = 16


def line_membership(n):
    N = n * n
    L = np.zeros((N, 2 * n + 2), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            c = i * n + j
            L[c, i] = 1
            L[c, n + j] = 1
            if i == j:
                L[c, 2 * n] = 1
            if i + j == n - 1:
                L[c, 2 * n + 1] = 1
    return L


def setup(n):
    N = n * n
    L = line_membership(n)
    M = n * (N + 1) // 2
    a, b = np.triu_indices(N, 1)
    D = L[a] - L[b]                  # (P, lines)
    q = (D * D).sum(axis=1)          # |D|^2
    return N, L, M, a, b, D, q


def greedy_run(n, rng, ctx):
    N, L, M, a, b, D, q = ctx
    v = rng.permutation(N) + 1
    s = v @ L - M                    # centered line sums
    F = int((s * s).sum())
    swaps = 0
    while F > 0:
        d = v[b] - v[a]              # swap a<->b: cell a gets v[b]: lines of a change by +d, lines of b by -d
        dF = 2 * d * (D @ s) + d * d * q
        k = int(np.argmin(dF))
        if dF[k] >= 0:
            break
        va, vb = a[k], b[k]
        v[va], v[vb] = v[vb], v[va]
        s = s + d[k] * D[k]
        F += int(dF[k])
        swaps += 1
    return F == 0, swaps, F


def sa_run(n, rng, ctx, steps, T0, T1):
    N, L, M, a, b, D, q = ctx
    v = rng.permutation(N) + 1
    s = v @ L - M
    F = int((s * s).sum())
    best = F
    if F == 0:
        return True, 0, 0, 0
    alpha = (T1 / T0) ** (1.0 / steps)
    T = T0
    P = a.size
    ks = rng.integers(0, P, size=steps)
    us = rng.random(steps)
    accepted = 0
    for t in range(steps):
        k = ks[t]
        va, vb = a[k], b[k]
        d = v[vb] - v[va]
        Dk = D[k]
        dF = 2 * d * int(Dk @ s) + d * d * q[k]
        if dF <= 0 or us[t] < np.exp(-dF / T):
            v[va], v[vb] = v[vb], v[va]
            s += d * Dk
            F += dF
            accepted += 1
            if F < best:
                best = F
            if F == 0:
                return True, t + 1, accepted, 0
        T *= alpha
    return False, steps, accepted, best


def calibrate_T0(n, ctx, rng, m=2000):
    """Median uphill |dF| of random swaps from random arrangements."""
    N, L, M, a, b, D, q = ctx
    vals = []
    for _ in range(m):
        v = rng.permutation(N) + 1
        s = v @ L - M
        k = rng.integers(0, a.size)
        d = v[b[k]] - v[a[k]]
        dF = 2 * d * (D[k] @ s) + d * d * q[k]
        if dF > 0:
            vals.append(dF)
    return float(np.median(vals))


def worker(args):
    kind, n, seed, runs, steps, T0, T1 = args
    rng = np.random.default_rng(seed)
    ctx = setup(n)
    out = []
    for _ in range(runs):
        if kind == 'greedy':
            out.append(greedy_run(n, rng, ctx))
        else:
            out.append(sa_run(n, rng, ctx, steps, T0, T1))
    return out


def run_all(ns=(4, 5, 6)):
    res = {}
    t_all = time.time()
    with Pool(NWORK) as pool:
        for n in ns:
            t0 = time.time()
            ctx = setup(n)
            rng = np.random.default_rng(99 + n)
            T0 = calibrate_T0(n, ctx, rng)
            T1 = 0.5
            steps = 20000 * n * n          # 320k (n=4) .. 720k (n=6) proposals
            g = pool.map(worker, [('greedy', n, 10 * n + w, RUNS_GREEDY // NWORK, 0, 0, 0) for w in range(NWORK)])
            g = [r for part in g for r in part]
            succ = np.array([r[0] for r in g]); sw = np.array([r[1] for r in g]); fin = np.array([r[2] for r in g])
            greedy = {'runs': len(g), 'success_prob': float(succ.mean()),
                      'success_se': float((succ.mean() * (1 - succ.mean()) / len(g)) ** 0.5),
                      'n_success': int(succ.sum()),
                      'mean_swaps_all': float(sw.mean()),
                      'mean_swaps_success': float(sw[succ].mean()) if succ.any() else None,
                      'mean_swaps_stuck': float(sw[~succ].mean()) if (~succ).any() else None,
                      'stuck_in_nonmagic_local_min': float(1 - succ.mean()),
                      'stuck_final_F_mean': float(fin[~succ].mean()) if (~succ).any() else None,
                      'stuck_final_F_min': int(fin[~succ].min()) if (~succ).any() else None,
                      'stuck_final_E_full_mean': float(fin[~succ].mean()) / n ** 4 if (~succ).any() else None,
                      'expected_restarts_to_success': float(1 / succ.mean()) if succ.any() else None}
            s = pool.map(worker, [('sa', n, 500 * n + w, RUNS_SA // NWORK, steps, T0, T1) for w in range(NWORK)])
            s = [r for part in s for r in part]
            succ = np.array([r[0] for r in s]); st = np.array([r[1] for r in s]); acc = np.array([r[2] for r in s])
            best = np.array([r[3] for r in s])
            sa = {'runs': len(s), 'steps_budget': steps, 'T0': T0, 'T1': T1,
                  'success_prob': float(succ.mean()),
                  'success_se': float((succ.mean() * (1 - succ.mean()) / len(s)) ** 0.5),
                  'n_success': int(succ.sum()),
                  'mean_proposals_success': float(st[succ].mean()) if succ.any() else None,
                  'median_proposals_success': float(np.median(st[succ])) if succ.any() else None,
                  'mean_accepted_swaps_success': float(acc[succ].mean()) if succ.any() else None,
                  'fail_best_F_mean': float(best[~succ].mean()) if (~succ).any() else None}
            res[str(n)] = {'n': n, 'greedy': greedy, 'sa': sa, 'runtime_s': time.time() - t0}
            print(f"n={n}: greedy p={greedy['success_prob']:.4f} swaps={greedy['mean_swaps_all']:.1f}; "
                  f"SA p={sa['success_prob']:.3f} proposals={sa['mean_proposals_success']}; {time.time()-t0:.0f}s", flush=True)
    res['total_runtime_s'] = time.time() - t_all
    return res


if __name__ == '__main__':
    r = run_all()
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(r, open(os.path.join(here, 'algo_results.json'), 'w'), indent=1)
