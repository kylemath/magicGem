"""
linear_census.py -- vertex counts of the gems of all linear magic squares of odd order n, up to D4 (Remark rem:linear):
    s(i,j) = n*<u1 i + u2 j + alpha> + <w1 i + w2 j + beta> + 1.
Faster than linear_squares.py, for 5 <= n <= 21: the admissible parameters come from Proposition prop:linear-magic
(checked against the actual line sums on a sample), D4 acts on the parameters (transpose swaps u1,u2 and w1,w2; the
row flip i -> n-1-i sends (u1, alpha) to (-u1, alpha-u1), likewise for w), and one parameter tuple per class is kept.
The class count is compared with the formula of Proposition prop:linear-magic.
Vertex counts by qhull; every class with at most 13 vertices and every class with the largest count is then
certified with the exact hull (gem_geometry.exact_hull). The minimum, the classes attaining it and the maximum are
therefore exact provided the Quickhull counts of the remaining classes are right (for n <= 11 the Quickhull vertex sets
agree with the exact ones for every class; see linear_squares.py).  Usage: python3 linear_census.py 13 15 17 19 21  (n = 19 takes about 15 min on 4 cores)
Writes results_linear_census.json and linear_census.log.
"""
import sys, os, json, time, itertools
from math import gcd
from collections import Counter
from multiprocessing import Pool
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import scaled_points, exact_hull


def square(n, p):
    u1, u2, w1, w2, al, be = p
    I, J = np.indices((n, n))
    return n * ((u1 * I + u2 * J + al) % n) + (w1 * I + w2 * J + be) % n + 1


def is_magic(S):
    n = S.shape[0]; N = n * n; M = n * (N + 1) // 2
    return (len(np.unique(S)) == N and (S.sum(0) == M).all() and (S.sum(1) == M).all()
            and int(np.trace(S)) == M and int(np.trace(S[:, ::-1])) == M)


def d4_images(n, p):
    u1, u2, w1, w2, al, be = p
    out = []
    for t in (False, True):
        a1, a2, b1, b2 = (u2, u1, w2, w1) if t else (u1, u2, w1, w2)
        for fr in (False, True):
            for fc in (False, True):
                c1, c2, d1, d2, g, h = a1, a2, b1, b2, al, be
                if fr: g, h, c1, d1 = g - c1, h - d1, -c1, -d1
                if fc: g, h, c2, d2 = g - c2, h - d2, -c2, -d2
                out.append((c1 % n, c2 % n, d1 % n, d2 % n, g % n, h % n))
    return out


def ok_digit(n, a1, a2, g):
    for s, t in ((a1 + a2, g), (a1 - a2, g - a2)):
        d = gcd(s % n, n)
        if d > 1 and (t - (d - 1) // 2) % d:
            return False
    return True


def work(args):
    n, u1 = args
    units = [r for r in range(1, n) if gcd(r, n) == 1]
    reps, V = [], []
    for u2, w1, w2 in itertools.product(units, repeat=3):
        if gcd((u1 * w2 - u2 * w1) % n, n) != 1:
            continue
        als = [a for a in range(n) if ok_digit(n, u1, u2, a)]
        bes = [b for b in range(n) if ok_digit(n, w1, w2, b)]
        for al in als:
            for be in bes:
                p = (u1, u2, w1, w2, al, be)
                if min(d4_images(n, p)) != p:
                    continue
                reps.append(p)
                V.append(len(ConvexHull(scaled_points(square(n, p)).astype(float)).vertices))
    return reps, V


def formula_classes(n):
    units = [r for r in range(1, n) if gcd(r, n) == 1]
    f = lambda r: n // (gcd(r + 1, n) * gcd(r - 1, n))
    tot = len(units) ** 2 * sum(f(r) * f(rp) for r in units for rp in units if gcd((r - rp) % n, n) == 1)
    assert tot % 8 == 0
    return tot // 8


def main(ns):
    res, log = {}, []
    rng = np.random.default_rng(1)
    for n in ns:
        t0 = time.time(); m = (n - 1) // 2
        # criterion check on random parameters (the full check is linear_magic_count.py)
        for _ in range(2000):
            p = tuple(int(x) for x in rng.integers(0, n, 6))
            u1, u2, w1, w2 = p[:4]
            crit = (all(gcd(x, n) == 1 for x in (u1, u2, w1, w2, (u1 * w2 - u2 * w1) % n))
                    and ok_digit(n, u1, u2, p[4]) and ok_digit(n, w1, w2, p[5]))
            assert crit == is_magic(square(n, p)), (n, p)
        units = [r for r in range(1, n) if gcd(r, n) == 1]
        with Pool(4) as pool:
            parts = pool.map(work, [(n, u1) for u1 in units])
        reps = [p for r, _ in parts for p in r]; V = [v for _, vs in parts for v in vs]
        assert len(reps) == formula_classes(n), (len(reps), formula_classes(n))
        dist = Counter(V); vmax = max(dist)
        cert = {}
        for p, v in zip(reps, V):
            if v <= 13 or v == vmax:
                S = square(n, p); assert is_magic(S)
                h = exact_hull(S); assert h['f_vector'][0] == v, (n, p, v, h['f_vector'])
                cert.setdefault(v, []).append(dict(params=p, f=list(h['f_vector'])))
        vmin = min(dist)
        sia = min(d4_images(n, (1, 1, 1, 2, -m % n, -2 * m % n)))
        exch = min(d4_images(n, (1, 2, 1, 1, -2 * m % n, -m % n)))
        if n >= 7:
            assert vmin == 12 and sorted(c['params'] for c in cert[12]) == sorted([sia, exch]), (n, cert.get(12))
        res[n] = dict(classes=len(reps), V_distribution=dict(sorted(dist.items())), V_min=vmin, n_min=dist[vmin],
                      V_max=vmax, n_max=dist[vmax], certified=cert, seconds=round(time.time() - t0))
        line = (f'n={n}: {len(reps)} D4-classes (= formula); V from {vmin} ({dist[vmin]} classes) to {vmax} '
                f'({dist[vmax]} classes); classes with V<=13 and V={vmax} certified exactly')
        if n >= 7:
            line += '; the V=12 classes are the Siamese and the digit-exchanged square'
        log.append(line + f'; {res[n]["seconds"]} s')
        print(log[-1], flush=True)
        json.dump(res, open(os.path.join(HERE, 'results_linear_census.json'), 'w'), indent=1)
        open(os.path.join(HERE, 'linear_census.log'), 'w').write('\n'.join(log) + '\n')


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]] or [5, 7, 9, 11, 13])
