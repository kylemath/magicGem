"""Numerical vertex-count and volume statistics for random arrangements and sampled magic squares (n = 3..10).
All hulls are computed with Qhull; the first AUDIT hulls of every batch are re-computed in exact integer arithmetic and the vertex sets compared.
  python3 vertex_statistics.py random  [samples=100000]   random permutations of 1..n^2, n = 3..10   -> vertex_stats_random.json
  python3 vertex_statistics.py magic   <dir> <n> ...      magic squares found by sa_magic.c (files <dir>/sa_n<n>_*.txt)  -> vertex_stats_magic.json
  python3 vertex_statistics.py volume                     n = 4: volume percentile of the 880 gems among 1e5 random arrangements,
                                                          det Cov identity                                              -> volume_stats.json
(Sampling: the annealer is seeded; the sampling distribution on magic squares of order >= 5 is unknown, see the paper.)
"""
import sys, os, json, glob
import numpy as np
from multiprocessing import Pool
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
AUDIT = 100


def grid_points(S):
    S = np.asarray(S, dtype=np.int64); n = S.shape[0]; N = n * n
    i, j = np.divmod(np.arange(N), n)
    return np.stack([2 * j - (n - 1), (n - 1) - 2 * i, 2 * S.ravel() - (N + 1)], 1)


def exact_vertices(P):
    """extreme points by exact integer arithmetic (Qhull only proposes facets)"""
    N = len(P); s = ConvexHull(P.astype(float)).simplices
    p0, p1, p2 = P[s[:, 0]], P[s[:, 1]], P[s[:, 2]]
    nrm = np.cross(p1 - p0, p2 - p0); g = np.gcd.reduce(np.abs(nrm), axis=1); ok = g > 0
    nrm = nrm[ok] // g[ok, None]; p0 = p0[ok]; d = -(nrm * p0).sum(1)
    flip = (nrm @ P.sum(0) + d * N) > 0; nrm[flip] *= -1; d[flip] *= -1
    pl = np.unique(np.concatenate([nrm, d[:, None]], 1), axis=0)
    vals = P @ pl[:, :3].T + pl[:, 3]
    assert (vals <= 0).all()
    return set(np.nonzero((vals == 0).sum(1) >= 3)[0].tolist())


def nverts(S, audit=False):
    P = grid_points(S); v = set(ConvexHull(P.astype(float)).vertices.tolist())
    S = np.asarray(S).ravel()
    assert int(np.argmin(S)) in v and int(np.argmax(S)) in v        # 1 and N are always vertices
    if audit: assert exact_vertices(P) == v, 'Qhull and exact vertex sets differ'
    return len(v)


def work_random(a):
    n, cnt, seed = a; rng = np.random.default_rng(seed); N = n * n; out = []
    for r in range(cnt):
        try: out.append(nverts((rng.permutation(N) + 1).reshape(n, n), audit=r < AUDIT))
        except Exception as e:
            if 'Qhull' in type(e).__name__ or 'QH' in str(e): continue      # exactly coplanar (n = 3 only): skipped
            raise
    return n, out


def stats(V):
    V = np.array(V); return dict(samples=len(V), mean=float(V.mean()), sd=float(V.std(ddof=1)), sem=float(V.std(ddof=1) / np.sqrt(len(V))),
                                 min=int(V.min()), max=int(V.max()), hist=np.bincount(V).tolist())


def d4canon(S):
    S = np.asarray(S); best = None; T = S
    for _ in range(4):
        for U in (T, T.T):
            t = tuple(int(x) for x in U.ravel()); best = t if best is None or t < best else best
        T = np.rot90(T)
    return best


def is_magic(S):
    n = len(S); M = n * (n * n + 1) // 2
    return (S.sum(0) == M).all() and (S.sum(1) == M).all() and np.trace(S) == M and np.trace(S[:, ::-1]) == M and sorted(S.ravel()) == list(range(1, n * n + 1))


def work_magic(S): return nverts(S, audit=False)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'random':
        tot = int(sys.argv[2]) if len(sys.argv) > 2 else 100000; chunk = 2500
        jobs = [(n, chunk, 7000 * n + c) for n in range(3, 11) for c in range(tot // chunk)]
        res = {}
        with Pool() as p:
            for n, o in p.imap_unordered(work_random, jobs): res.setdefault(n, []).extend(o)
        out = {n: stats(res[n]) for n in sorted(res)}
        for n in out: out[n]['mean_over_N'] = out[n]['mean'] / n ** 2; print(n, {k: out[n][k] for k in ('samples', 'mean', 'sd', 'sem', 'min', 'max', 'mean_over_N')})
        json.dump(out, open(os.path.join(HERE, 'vertex_stats_random.json'), 'w'))
    elif mode == 'magic':
        d = sys.argv[2]; out = {}
        for n in map(int, sys.argv[3:]):
            arr = np.concatenate([np.loadtxt(f, dtype=int, ndmin=2) for f in sorted(glob.glob(f'{d}/sa_n{n}_*.txt')) if os.path.getsize(f)]).reshape(-1, n, n)
            assert all(is_magic(S) for S in arr)
            seen = {}
            for S in arr: seen.setdefault(d4canon(S), S)
            sq = list(seen.values())
            with Pool() as p: V = p.map(work_magic, sq, chunksize=200)
            for S in sq[:200]: nverts(S, audit=True)
            out[n] = stats(V); out[n]['raw'] = len(arr); out[n]['distinct_up_to_D4'] = len(sq)
            print(n, {k: out[n][k] for k in ('raw', 'distinct_up_to_D4', 'mean', 'sd', 'sem', 'min', 'max')})
        json.dump(out, open(os.path.join(HERE, 'vertex_stats_magic.json'), 'w'))
    elif mode == 'sa4':         # sampler check at n = 4, where all 880 classes are known:  python3 vertex_statistics.py sa4 <dir>
        from collections import Counter
        from scipy.stats import chisquare
        SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4); idx = {d4canon(S): k for k, S in enumerate(SQ)}
        arr = np.concatenate([np.loadtxt(f, dtype=int, ndmin=2) for f in sorted(glob.glob(f'{sys.argv[2]}/sa_n4_*.txt')) if os.path.getsize(f)]).reshape(-1, 4, 4)
        c = Counter(idx[d4canon(S)] for S in arr); h = np.array([c[k] for k in range(880)])
        nv = np.array([g['f_vector'][0] for g in json.load(open(os.path.join(HERE, 'results_geometry.json')))['per_gem']])
        out = dict(draws=len(arr), classes_hit=len(c), hits_min=int(h.min()), hits_max=int(h.max()), hits_mean=float(h.mean()),
                   chi2_uniform_p=float(chisquare(h).pvalue), hit_weighted_mean_V=float((h * nv).sum() / h.sum()), exact_mean_V=float(nv.mean()))
        print(out); json.dump(out, open(os.path.join(HERE, 'vertex_stats_sa4.json'), 'w'))
    elif mode == 'table':       # combine the two JSON files with the exact n = 4 data into the table of the paper
        R = json.load(open(os.path.join(HERE, 'vertex_stats_random.json'))); M = json.load(open(os.path.join(HERE, 'vertex_stats_magic.json')))
        ex = json.load(open(os.path.join(HERE, 'results_box_classes.json')))['vertex_count']
        m4 = sum(int(k) * v for k, v in ex.items()) / 880; assert abs(m4 - M['4']['mean']) < 1e-12      # SA at n = 4 hit all 880 classes
        print('n=4 exact magic mean', m4, '= 269/22')
        for n in range(3, 11):
            r = R[str(n)]; line = f"n={n}: random {r['mean']:.3f} (sem {r['sem']:.3f}) V/N {r['mean_over_N']:.3f}"
            if str(n) in M and n > 4:
                m = M[str(n)]; z = (m['mean'] - r['mean']) / (m['sem'] ** 2 + r['sem'] ** 2) ** 0.5
                line += f"; magic {m['mean']:.3f} (sem {m['sem']:.3f}, {m['distinct_up_to_D4']} distinct D4-classes, min {m['min']}) z={z:.2f}"; assert abs(z) < 1.5
            print(line)
    elif mode == 'volume':
        from scipy.stats import spearmanr
        SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 16)
        geo = json.load(open(os.path.join(HERE, 'results_geometry.json')))
        from fractions import Fraction
        vol880 = np.array([float(Fraction(g['volume'])) for g in geo['per_gem']])
        xs = np.tile(np.arange(4) - 1.5, 4); ys = np.repeat(1.5 - np.arange(4), 4)

        def detcov(A):
            Z = A.astype(float) - A.mean(1, keepdims=True)
            M = np.stack([np.broadcast_to(xs, Z.shape), np.broadcast_to(ys, Z.shape), Z], 1)
            C = np.einsum('bin,bjn->bij', M, M) / 16
            return np.linalg.det(C), C
        rng = np.random.default_rng(2024); B = 100000
        A = np.argsort(rng.random((B, 16)), axis=1) + 1
        d, C = detcov(A)
        VX, VY, VZ = C[:, 0, 0], C[:, 1, 1], C[:, 2, 2]
        assert np.allclose(C[:, 0, 1], 0) and np.allclose(VZ, VZ[0]) and np.allclose(VX, VX[0]) and np.allclose(VY, VX)
        assert np.allclose(d, VX * VY * VZ - VX * C[:, 1, 2] ** 2 - VY * C[:, 0, 2] ** 2)       # the identity of the paper
        d880, C880 = detcov(SQ)
        assert np.allclose(d880, d880[0]) and np.allclose(d880[0], VX[0] * VY[0] * VZ[0]) and (d <= d880[0] + 1e-9).all()
        vol = np.empty(B)
        for b in range(B): vol[b] = ConvexHull(grid_points(A[b].reshape(4, 4)).astype(float)).volume / 8
        pct = lambda x: float((vol < x).mean() + 0.5 * (vol == x).mean())
        out = dict(samples=B, random_mean=float(vol.mean()), random_sd=float(vol.std()), magic_mean=float(vol880.mean()),
                   median_magic_volume=float(np.median(vol880)), median_magic_percentile=pct(float(np.median(vol880))),
                   min_magic_percentile=pct(float(vol880.min())), spearman_volume_detcov_random=float(spearmanr(vol, d)[0]),
                   detcov_max=float(d880[0]), detcov_random_mean=float(d.mean()), detcov_random_min=float(d.min()))
        print(out); json.dump(out, open(os.path.join(HERE, 'volume_stats.json'), 'w'))
