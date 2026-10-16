#!/usr/bin/env python3
"""Test of Conjecture 3.15 (k*(n) = U(n)) beyond n = 40.

  python3 kstar_beyond40.py              check the archived witnesses in kstar_beyond40.json and recount the feasible
                                         vectors in each ball (exact, a few seconds)
  python3 kstar_beyond40.py search 41 42 rerun the search for the given n (needs ./anneal2: cc -O3 -o anneal2 anneal2.c -lm)

U(n) is the least k such that no nonzero vector of Lambda_{n,k} satisfies (10), as computed (not certified) by
kstar_verify.py and kstar_upper_second/.  The search enumerates exactly the vectors of Lambda_{n,U(n)-1} in the ball
||gamma||^2 <= n^5(n^2-1)/12 that satisfy (10) (kstar_upper_second/lattice.py), sorts them by sup-norm and tries to
realise them as column deviations with all row sums M(n): first realise.py (steepest descent over within-row swaps)
and anneal2 from the square of Lemma 3.12, then, if that fails, a two-stage annealing (T0 = 300 for 3e9 steps,
then restarts from the final state at T0 = 3).  A success is a witness for k*(n) >= U(n), hence k*(n) = U(n)
provided the computed U(n) is correct.  Archived outcome: witnesses for 41 <= n <= 46 (n = 42 and n = 46 needed
the two-stage annealing; the ball for n = 42 holds a single feasible vector up to sign)."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'kstar_upper_second'))
from kstar_verify import feasible, vanishing_order, deviations

JS = os.path.join(HERE, 'kstar_beyond40.json')
U = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'kstar_verify.json')))['upper_bounds'].items()}


def feasible_in_ball(n):
    """all vectors of Lambda_{n,U(n)-1} (up to sign) in the ball ||gamma||^2 <= n^5(n^2-1)/12 that satisfy (10)"""
    from lattice import lll, basis, enumerate_short
    B = lll(basis(n, U[n] - 1)); R2 = -(-n ** 5 * (n * n - 1) // 12); c = []
    enumerate_short(B, R2, lambda x, v: c.append(v) if feasible(v, n) else None)
    return c


def slack(g, n):
    """min over p of the slack p n (N - p n)/2 - (sum of the p largest entries), and the minimising p (both signs)"""
    N = n * n; best = None
    for v in (g, [-x for x in g]):
        s = sorted(v, reverse=True)
        for p in range(1, n):
            sl = p * n * (N - p * n) // 2 - sum(s[:p])
            if best is None or sl < best[0]: best = (sl, p)
    return best


def check_archive():
    d = json.load(open(JS))
    for n in sorted(d, key=int):
        e = d[n]; n = int(n)
        assert e['U'] == U[n]
        c = feasible_in_ball(n); assert len(c) == e['n_candidates']
        if len(c) == 1:
            print(n, 'the ball holds a single feasible vector up to sign; its least slack in (10) is %d, at p = %d' % slack(c[0], n))
        if e['witness'] is None:
            print(n, 'U(n) = %d, %d feasible vectors in the ball, no witness found' % (e['U'], e['n_candidates'])); continue
        S = e['witness']['square']; N = n * n
        assert sorted(v for row in S for v in row) == list(range(1, N + 1))
        rho, gam = deviations(S)
        assert not any(rho) and gam == e['witness']['gamma'] and any(gam)
        assert vanishing_order(gam) >= U[n] and feasible(gam, n)
        print(n, 'U(n) = %d, %d feasible vectors in the ball (up to sign); witness verified: permutation, all row sums M(n), '
              'gamma != 0, order of vanishing %d >= U(n), max|gamma| = %d (bound %d), method %s'
              % (U[n], len(c), vanishing_order(gam), max(map(abs, gam)), n * n * (n - 1) // 2, e['witness']['method']))


def anneal(n, S, g, seed, iters, T0):
    inp = ' '.join(str(v) for row in S for v in row) + '\n' + ' '.join(map(str, g)) + '\n' + ' '.join(['0'] * n) + '\n'
    p = subprocess.run([os.path.join(HERE, 'anneal2'), str(n), str(seed), str(iters), str(T0)], input=inp,
                       capture_output=True, text=True)
    lines = p.stdout.strip().split('\n')
    E = int(lines[0].split()[1]) if lines[0].startswith('FAIL') else 0
    v = list(map(int, lines[-1].split()))
    return E, [v[i * n:(i + 1) * n] for i in range(n)]


def search(n, tmax=3600):
    from lattice import lll, basis, enumerate_short
    from realise import realise, check, start_square
    t0 = time.time(); k = U[n] - 1
    B = lll(basis(n, k)); R2 = -(-n ** 5 * (n * n - 1) // 12); cands = []
    def cb(x, vec):
        if feasible(vec, n): cands.append(vec)
        return len(cands) >= 400 or time.time() - t0 > 300
    try:
        enumerate_short(B, R2, cb)
    except RuntimeError:
        pass
    cands.sort(key=lambda v: max(map(abs, v)))
    print(n, 'U =', U[n], 'feasible vectors (up to sign):', len(cands), flush=True)
    search.n_candidates = len(cands)
    S0 = start_square(n)
    for stage in (1, 2):
        for g0 in cands[:6] if stage == 1 else cands[:4]:
            for g in (g0, [-v for v in g0]):
                for seed in range(2):
                    if stage == 1:
                        s = realise(g, seed=seed, maxit=4000)
                        if s is not None and check(s, g, [0] * n): return dict(gamma=g, square=s, method='realise')
                        E, s = anneal(n, S0, g, seed, 4 * 10 ** 8, 2000)
                        if E == 0 and check(s, g, [0] * n): return dict(gamma=g, square=s, method='anneal2')
                    else:
                        E, s = anneal(n, S0, g, 20 + seed, 3 * 10 ** 9, 300)
                        for sub in range(8):
                            if E == 0: break
                            E, s = anneal(n, s, g, 1000 * (20 + seed) + sub, 2 * 10 ** 8, 3)
                        if E == 0 and check(s, g, [0] * n): return dict(gamma=g, square=s, method='anneal2, two-stage')
                    if time.time() - t0 > tmax: return None
    return None


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'search':
        d = json.load(open(JS)) if os.path.exists(JS) else {}
        for n in map(int, sys.argv[2:]):
            res = search(n)
            print(n, 'witness found' if res else 'no witness found', flush=True)
            d[str(n)] = dict(U=U[n], n_candidates=search.n_candidates, witness=res)
            json.dump(d, open(JS, 'w'))
    else:
        check_archive()
