"""
magic_vs_random.py -- does the gem distinguish magic squares?  (Section 5.3 and Table 4 of the paper; Monte Carlo
estimates except for the exact magic column at n = 4.)

Groups of arrangements, n = 4:
  M    all 880 magic squares (D4-classes; every invariant below is D4-invariant, so this is the uniform distribution
       on the 7040 magic squares) -- exact
  R    uniformly random arrangements
  F    uniformly random arrangements with vanishing first moments  sum z x = sum z y = 0  (rejection sampling)
  SM   uniformly random semi-magic squares: the 549,504 semi-magic squares are the 954 orbits listed below times the
       576 row and column permutations (free action), so a uniform orbit and a uniform pair of permutations is uniform
  SMa  semi-magic squares from the annealer sa_magic.c with the 8th argument 1 (calibration of the annealer against SM)
n = 5 (all sampled):  M5 magic squares from the annealer (distinct D4-classes), R5, F5 as above, SM5 annealed
semi-magic squares.  The sampling distribution of the annealer is not known.
Invariants of the gem (exact hulls, gem_geometry.exact_hull): V, volume, V_int (interior points), V_bd (non-vertex
boundary points), numbers of lower / upper / vertical facets, |Iso(G)| (exact, isolib on the vertex set), the solid
centroid c (distance from the origin) and the solid covariance C (its vertical variance C_zz and its tilt
sqrt(C_xz^2 + C_yz^2)); and, for reference, the square's own self-complementarity.
Effect sizes: difference of means with its standard error (the n = 4 magic column is a population, without error),
z = difference / SE and Cohen's d = difference / pooled sd.
  python3 magic_vs_random.py [K4=100000] [K5=20000]   -> magic_vs_random.json, magic_vs_random.log  (about 15 min, 4 cores)
Seeds: 4040 + group index (n = 4), 5050 + group index (n = 5); annealer seeds 9000 s + n.
"""
import os, sys, json, itertools, subprocess, tempfile, time
from multiprocessing import Pool
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull, classify_points
from isolib import isometries

K4 = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
K5 = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
LOG = []


def log(s):
    print(s, flush=True); LOG.append(s)


# ---------------------------------------------------------------- invariants of one gem
def d4(S):
    return [S, np.rot90(S, 1), np.rot90(S, 2), np.rot90(S, 3), S.T, np.rot90(S, 1).T, np.rot90(S, 2).T, np.rot90(S, 3).T]


def d4canon(S):
    return min(tuple(int(v) for v in g.ravel()) for g in d4(S))


def self_complementary(S):
    N = S.size; C = N + 1 - S
    return any((g == C).all() for g in d4(S))


def invariants(S):
    S = np.asarray(S); h = exact_hull(S); P = h['P']
    V, I, B = classify_points(h)
    low = sum(1 for k in h['faces'] if k[2] < 0); up = sum(1 for k in h['faces'] if k[2] > 0)
    vert = sum(1 for k in h['faces'] if k[2] == 0)
    iso = len(isometries(P[h['vertices']]))
    # solid moments: tetrahedra from the origin (an interior point) over a triangulation of the boundary
    X = P.astype(float) / 2.0; hull = ConvexHull(X)
    vol = 0.0; m1 = np.zeros(3); m2 = np.zeros((3, 3))
    for s in hull.simplices:
        A = X[s]; v = abs(np.linalg.det(A)) / 6.0; sm = A.sum(0)
        vol += v; m1 += v * sm / 4.0; m2 += v / 20.0 * (A.T @ A + np.outer(sm, sm))
    c = m1 / vol; C = m2 / vol - np.outer(c, c)
    assert abs(vol - float(h['volume'])) < 1e-9
    return dict(V=len(V), vol=float(h['volume']), Vint=len(I), Vbd=len(B), Flow=low, Fup=up, Fvert=vert, iso=iso,
                cnorm=float(np.linalg.norm(c)), Czz=float(C[2, 2]), tilt=float(np.hypot(C[0, 2], C[1, 2])),
                sc=int(self_complementary(S)))


KEYS = ['V', 'vol', 'Vint', 'Vbd', 'Flow', 'Fup', 'Fvert', 'iso', 'cnorm', 'Czz', 'tilt', 'sc']


def run(squares):
    with Pool() as p:
        out = p.map(invariants, squares, chunksize=200)
    return {k: np.array([o[k] for o in out], dtype=float) for k in KEYS}


# ---------------------------------------------------------------- samplers
def random_arrangements(n, K, seed):
    rng = np.random.default_rng(seed)
    return [(rng.permutation(n * n) + 1).reshape(n, n) for _ in range(K)]


def first_moment_free(n, K, seed):
    """uniform arrangements conditioned on sum s x = sum s y = 0 (equivalently sum z x = sum z y = 0), by rejection"""
    rng = np.random.default_rng(seed); N = n * n
    i, j = np.divmod(np.arange(N), n); X2 = 2 * j - (n - 1); Y2 = (n - 1) - 2 * i
    out, draws = [], 0
    while len(out) < K:
        A = np.argsort(rng.random((500000, N)), axis=1) + 1; draws += len(A)
        ok = ((A @ X2) == 0) & ((A @ Y2) == 0)
        out.extend(A[ok][:K - len(out)])
    return [a.reshape(n, n) for a in out], draws


def semimagic4_orbits():
    R = [frozenset(c) for c in itertools.combinations(range(1, 17), 4) if sum(c) == 34]
    parts = []

    def rec(rem, acc):
        if not rem:
            parts.append(acc); return
        mn = min(rem)
        for r in R:
            if mn in r and r <= rem:
                rec(rem - r, acc + [r])
    rec(frozenset(range(1, 17)), [])
    reps = []
    for P in parts:                 # rows ordered by their smallest entry, first row increasing: one square per orbit
        r1 = sorted(P[0]); s4 = sorted(P[3])
        for p in itertools.permutations(sorted(P[1])):
            for q in itertools.permutations(sorted(P[2])):
                r4 = [34 - r1[c] - p[c] - q[c] for c in range(4)]
                if sorted(r4) == s4:
                    reps.append(np.array(r1 + list(p) + list(q) + r4).reshape(4, 4))
    return reps


def semimagic4(K, seed, reps):
    rng = np.random.default_rng(seed)
    return [reps[rng.integers(len(reps))][rng.permutation(4)][:, rng.permutation(4)] for _ in range(K)]


def anneal(n, K, semi, params):
    """distinct squares (D4-classes) from the annealer, seeds 9000 s + n, s = 1..8"""
    steps, T0, T1 = params
    d = tempfile.mkdtemp(); exe = os.path.join(d, 'sa')
    subprocess.check_call(['cc', '-O2', os.path.join(HERE, 'sa_magic.c'), '-o', exe, '-lm'])
    per = (int(K * 1.02) + 7) // 8
    procs = [subprocess.Popen([exe, str(n), str(per), str(9000 * s + n), str(steps), str(T0), str(T1), '100', str(int(semi))],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) for s in range(1, 9)]
    seen = {}
    for p in procs:
        for line in p.communicate()[0].split('\n'):
            if line.strip():
                S = np.array(list(map(int, line.split()))).reshape(n, n); seen.setdefault(d4canon(S), S)
    sq = list(seen.values())[:K]
    M = n * (n * n + 1) // 2
    for S in sq:
        assert sorted(S.ravel()) == list(range(1, n * n + 1)) and (S.sum(0) == M).all() and (S.sum(1) == M).all()
        if not semi:
            assert np.trace(S) == M and np.trace(S[:, ::-1]) == M
    return sq


# ---------------------------------------------------------------- statistics
def summary(D):
    return {k: dict(mean=float(D[k].mean()), sd=float(D[k].std(ddof=1)), se=float(D[k].std(ddof=1) / np.sqrt(len(D[k]))))
            for k in KEYS} | {'size': len(D['V'])}


def compare(A, B, exactA=False):
    """A - B: difference, SE, z, Cohen's d (pooled sd) and its approximate SE"""
    out = {}
    for k in KEYS:
        a, b = A[k], B[k]; na, nb = len(a), len(b)
        diff = a.mean() - b.mean()
        se = np.sqrt((0 if exactA else a.var(ddof=1) / na) + b.var(ddof=1) / nb)
        sp_ = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
        dd = diff / sp_ if sp_ > 0 else 0.0
        out[k] = dict(diff=float(diff), se=float(se), z=float(diff / se) if se > 0 else 0.0, d=float(dd),
                      d_se=float(np.sqrt(1 / na + 1 / nb + dd ** 2 / (2 * (na + nb)))))
    return out


def fmt_cmp(name, c, keys=KEYS):
    return name + ': ' + '; '.join(f"{k} {c[k]['diff']:+.3f}+-{c[k]['se']:.3f} (z {c[k]['z']:+.1f}, d {c[k]['d']:+.2f})" for k in keys)


if __name__ == '__main__':
    t0 = time.time(); RES = {}
    # ---------------- n = 4
    M = [np.array(list(map(int, l.split()))).reshape(4, 4) for l in open(os.path.join(HERE, 'squares880.txt')) if l.strip()]
    reps = semimagic4_orbits()
    assert len(reps) * 576 == 549504                            # the number of semi-magic squares of order 4
    orbit = {}
    for r in reps:
        orbit[tuple(r.ravel())] = 1

    def orbit_rep(S):                                           # the listed orbit representative of a semi-magic square
        rows = sorted(S.tolist(), key=min); order = np.argsort(rows[0])
        return tuple(np.array(rows)[:, order].ravel())
    assert all(orbit_rep(g) in orbit for S in M for g in d4(S))   # every magic square is in a listed orbit
    G4 = {'M': M}
    G4['R'] = random_arrangements(4, K4, 4041)
    G4['F'], draws = first_moment_free(4, K4, 4042)
    log(f'n=4: first-moment-free sample: {K4} accepted of {draws} uniform draws (rate {K4 / draws:.2e})')
    G4['SM'] = semimagic4(K4, 4043, reps)
    G4['SMa'] = anneal(4, min(K4, 20000), True, (200000, 20, 0.5))
    D4_ = {g: run(sq) for g, sq in G4.items()}
    RES['n4'] = {g: summary(D) for g, D in D4_.items()}
    RES['n4']['M_vs_R'] = compare(D4_['M'], D4_['R'], exactA=True)
    RES['n4']['M_vs_F'] = compare(D4_['M'], D4_['F'], exactA=True)
    RES['n4']['M_vs_SM'] = compare(D4_['M'], D4_['SM'], exactA=True)
    RES['n4']['F_vs_R'] = compare(D4_['F'], D4_['R'])
    RES['n4']['SM_vs_F'] = compare(D4_['SM'], D4_['F'])
    RES['n4']['SMa_vs_SM'] = compare(D4_['SMa'], D4_['SM'])
    # magic squares that are not self-complementary, against semi-magic squares that are not
    nsc = lambda D: {k: D[k][D['sc'] == 0] for k in KEYS}
    RES['n4']['Mnsc_vs_SMnsc'] = compare(nsc(D4_['M']), nsc(D4_['SM']), exactA=True)
    RES['n4']['V_hist'] = {g: np.bincount(D['V'].astype(int), minlength=17).tolist() for g, D in D4_.items()}
    for g in G4:
        s = RES['n4'][g]
        log(f"n=4 {g} ({s['size']}): " + '; '.join(f"{k} {s[k]['mean']:.3f}+-{s[k]['se']:.3f}" for k in KEYS))
    for c in ('M_vs_R', 'M_vs_F', 'M_vs_SM', 'F_vs_R', 'SM_vs_F', 'SMa_vs_SM', 'Mnsc_vs_SMnsc'):
        log(fmt_cmp('n=4 ' + c, RES['n4'][c]))
    for g in G4:
        log(f"n=4 {g} V histogram (V = 0..16): {RES['n4']['V_hist'][g]}")
    log(f'n=4 done ({time.time() - t0:.0f} s)')
    # ---------------- n = 5
    G5 = {'M5': anneal(5, K5, False, (400000, 30, 0.5)), 'R5': random_arrangements(5, K5, 5051)}
    G5['F5'], draws = first_moment_free(5, K5, 5052)
    log(f'n=5: first-moment-free sample: {K5} accepted of {draws} uniform draws (rate {K5 / draws:.2e})')
    G5['SM5'] = anneal(5, K5, True, (400000, 30, 0.5))
    D5 = {g: run(sq) for g, sq in G5.items()}
    RES['n5'] = {g: summary(D) for g, D in D5.items()}
    RES['n5']['M5_vs_R5'] = compare(D5['M5'], D5['R5'])
    RES['n5']['M5_vs_F5'] = compare(D5['M5'], D5['F5'])
    RES['n5']['M5_vs_SM5'] = compare(D5['M5'], D5['SM5'])
    RES['n5']['F5_vs_R5'] = compare(D5['F5'], D5['R5'])
    RES['n5']['SM5_vs_F5'] = compare(D5['SM5'], D5['F5'])
    RES['n5']['V_hist'] = {g: np.bincount(D['V'].astype(int), minlength=26).tolist() for g, D in D5.items()}
    for g in G5:
        s = RES['n5'][g]
        log(f"n=5 {g} ({s['size']}): " + '; '.join(f"{k} {s[k]['mean']:.3f}+-{s[k]['se']:.3f}" for k in KEYS))
    for c in ('M5_vs_R5', 'M5_vs_F5', 'M5_vs_SM5', 'F5_vs_R5', 'SM5_vs_F5'):
        log(fmt_cmp('n=5 ' + c, RES['n5'][c]))
    log(f'done ({time.time() - t0:.0f} s)')
    json.dump(RES, open(os.path.join(HERE, 'magic_vs_random.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'magic_vs_random.log'), 'w').write('\n'.join(LOG) + '\n')
