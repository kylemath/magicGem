#!/usr/bin/env python3
"""Independent exact re-verification of the numerical statements of the paper.

Run:  python3 verify_numbers.py            (about 1-2 minutes)
Writes verify_numbers.json and prints a log.  Everything is exact integer / rational arithmetic
except where explicitly marked (float comparisons with tolerances).

Conventions: N=n^2, x=j-(n-1)/2, y=(n-1)/2-i, z=s-(N+1)/2, F(S):=N^2*E_full(S)=sum over the
2n+2 lines of (line sum - M)^2 (a non-negative integer).
"""
import itertools, json, math, os, sys
from collections import Counter
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}


def lines(n):
    """List of 2n+2 index arrays (cells flattened row-major)."""
    L = []
    for k in range(n):
        L.append([k * n + j for j in range(n)])
    for k in range(n):
        L.append([i * n + k for i in range(n)])
    L.append([i * n + i for i in range(n)])
    L.append([i * n + n - 1 - i for i in range(n)])
    return L


def incidence(n):
    N = n * n
    A = np.zeros((2 * n + 2, N), dtype=np.int64)
    for r, cells in enumerate(lines(n)):
        A[r, cells] = 1
    return A


def F_of(S, n):
    """N^2 E_full for an array of arrangements S (B, N)."""
    N = n * n
    A = incidence(n)
    M = n * (N + 1) // 2
    dev = S @ A.T - M
    return (dev ** 2).sum(axis=1)


# ---------------------------------------------------------------- n = 3 exhaustive
def check_n3():
    n, N = 3, 9
    P = np.array(list(itertools.permutations(range(1, 10))), dtype=np.int64)
    A = incidence(n)
    M = 15
    dev = P @ A.T - M
    F = (dev ** 2).sum(axis=1)               # N^2 E_full = 81 E_full
    # E_low*81*4 integer:
    j = np.tile(np.arange(3), 3); i = np.repeat(np.arange(3), 3)
    x2 = 2 * j - 2; y2 = 2 - 2 * i            # 2x, 2y
    z = P - 5
    cx = z @ x2; cy = z @ y2                  # 2*sum z x, 2*sum z y
    G = (cx ** 2 + cy ** 2) + 4 * (dev[:, 6] ** 2 + dev[:, 7] ** 2)   # 4*81*E_low
    res = {}
    res['n_perm'] = len(P)
    res['magic'] = int((F == 0).sum())
    res['elow_zero'] = int((G == 0).sum())
    res['elow_zero_equals_magic'] = bool(np.array_equal(F == 0, G == 0))
    semi = (dev[:, :6] == 0).all(axis=1)
    res['semi_magic'] = int(semi.sum())
    res['both_diagonals'] = int(((dev[:, 6] == 0) & (dev[:, 7] == 0)).sum())
    res['degree1'] = int(((cx == 0) & (cy == 0)).sum())
    res['degree1_and_diag'] = int(((cx == 0) & (cy == 0) & (dev[:, 6] == 0) & (dev[:, 7] == 0)).sum())
    EF = F / 81.0; EL = G / 324.0
    res['mean_full'] = EF.mean(); res['mean_low'] = EL.mean()
    res['std_full'] = EF.std(); res['std_low'] = EL.std()
    res['var_full_exact'] = str(Fr(int((F ** 2).sum()), len(P) * 81 ** 2) - Fr(int(F.sum()), len(P) * 81) ** 2)
    res['var_low_exact'] = str(Fr(int((G ** 2).sum()), len(P) * 324 ** 2) - Fr(int(G.sum()), len(P) * 324) ** 2)
    res['max_full_times81'] = int(F.max()); res['max_low_times81'] = float(G.max() / 4)
    res['distinct_full'] = int(len(np.unique(F))); res['distinct_low'] = int(len(np.unique(G)))
    cF = Counter(F.tolist()); cG = Counter(G.tolist())
    res['mode_full_times81'] = max(cF.items(), key=lambda kv: kv[1])[0]
    res['mode_low_times81'] = max(cG.items(), key=lambda kv: kv[1])[0] / 4
    # local minima under single swaps: no swap with strictly smaller energy
    minF = np.ones(len(P), bool); minG = np.ones(len(P), bool)
    sminF = np.ones(len(P), bool); sminG = np.ones(len(P), bool)  # strict: every swap raises the energy
    for a, b in itertools.combinations(range(9), 2):
        Q = P.copy(); Q[:, [a, b]] = Q[:, [b, a]]
        devq = Q @ A.T - M
        Fq = (devq ** 2).sum(axis=1)
        zq = Q - 5
        Gq = ((zq @ x2) ** 2 + (zq @ y2) ** 2) + 4 * (devq[:, 6] ** 2 + devq[:, 7] ** 2)
        minF &= (Fq >= F); minG &= (Gq >= G)
        sminF &= (Fq > F); sminG &= (Gq > G)
    res['localmin_full'] = int(minF.sum()); res['localmin_full_magic'] = int((minF & (F == 0)).sum())
    res['localmin_full_values'] = sorted(set((F[minF] / 81).round(6).tolist()))
    res['localmin_low'] = int(minG.sum()); res['localmin_low_nonmagic'] = int((minG & (F != 0)).sum())
    res['strict_localmin_full'] = int(sminF.sum()); res['strict_localmin_low'] = int(sminG.sum()); res['strict_localmin_low_nonmagic'] = int((sminG & (F != 0)).sum())
    # Loly's invariant, n=3: I = sum s (x^2+y^2); 9 cells
    w = (j - 1) ** 2 + (1 - i) ** 2
    I = P @ w
    res['I_equals_60'] = int((I == 60).sum())
    res['I_var'] = float(I.var()); res['I_min'] = int(I.min()); res['I_max'] = int(I.max())
    res['I_distinct'] = int(len(np.unique(I)))
    res['deg2_conditions'] = int(((dev[:, :6] == 0).all(axis=1)).sum())
    OUT['n3'] = res
    for k, v in res.items():
        print('  n3', k, v)


# ---------------------------------------------------------------- exact moments of random energies
def pattern_moments(N):
    """Exact E[z_a^{k1} z_b^{k2} ...] for distinct cells under a uniform permutation."""
    p2 = Fr(sum((2 * v - N - 1) ** 2 for v in range(1, N + 1)), 4)    # sum of squares of centred values
    p4 = Fr(sum((2 * v - N - 1) ** 4 for v in range(1, N + 1)), 16)
    ff = lambda t: math.prod(N - r for r in range(t))
    return {
        'p2': p2, 'p4': p4,
        '2': p2 / N,
        '11': -p2 / (N * (N - 1)),
        '4': p4 / N,
        '31': -p4 / (N * (N - 1)),
        '22': (p2 * p2 - p4) / (N * (N - 1)),
        '211': (2 * p4 - p2 * p2) / ff(3),
        '1111': (3 * p2 * p2 - 6 * p4) / ff(4),
    }


def quad_form_moments(U, n):
    """U: integer symmetric (N,N) matrix of the form q(z)=z^T U z.  Returns exact (E q, E q^2)."""
    N = n * n
    m = pattern_moments(N)
    d = np.diag(U).astype(object); tot = int(U.sum()); trace = int(np.trace(U))
    Eq = m['2'] * trace + m['11'] * (tot - trace)
    # E q^2 = sum_{c1c2c3c4} U[c1c2] U[c3c4] E[z1 z2 z3 z4], pattern classification by exact integer sums
    Ui = U.astype(np.int64)
    idx = np.arange(N)
    c1, c2, c3, c4 = np.meshgrid(idx, idx, idx, idx, indexing='ij', sparse=False)
    W = Ui[c1, c2] * Ui[c3, c4]
    eq12 = c1 == c2; eq34 = c3 == c4; eq13 = c1 == c3; eq14 = c1 == c4; eq23 = c2 == c3; eq24 = c2 == c4
    # pattern id via canonical labelling
    lab = np.zeros(c1.shape + (4,), dtype=np.int8)
    stack = [c1, c2, c3, c4]
    pid = np.zeros(c1.shape, dtype=np.int64)
    # labels: first-occurrence indexing
    L1 = np.zeros(c1.shape, np.int64)
    L2 = np.where(eq12, 0, 1)
    L3 = np.where(eq13, 0, np.where(eq23, L2, np.maximum(L1, L2) + 1))
    # label for 4: equal to 1,2,3 else new
    nextnew = np.maximum(np.maximum(L1, L2), L3) + 1
    L4 = np.where(eq14, 0, np.where(eq24, L2, np.where(c3 == c4, L3, nextnew)))
    pid = L1 + 5 * L2 + 25 * L3 + 125 * L4
    sums = {}
    flat_pid = pid.ravel(); flat_W = W.ravel()
    for key in np.unique(flat_pid):
        sums[int(key)] = int(flat_W[flat_pid == key].sum())
    Eq2 = Fr(0)
    for key, S in sums.items():
        labs = [key % 5, (key // 5) % 5, (key // 25) % 5, (key // 125) % 5]
        cnt = sorted(Counter(labs).values(), reverse=True)
        typ = {(4,): '4', (3, 1): '31', (2, 2): '22', (2, 1, 1): '211', (1, 1, 1, 1): '1111'}[tuple(cnt)]
        Eq2 += S * m[typ]
    return Eq, Eq2


def quad_forms(n):
    """Integer matrices U_full (for N^2 E_full) and U_low (for 4 N^2 E_low)."""
    N = n * n
    A = incidence(n)
    Uf = A.T @ A
    j = np.tile(np.arange(n), n); i = np.repeat(np.arange(n), n)
    x2 = (2 * j - (n - 1)); y2 = ((n - 1) - 2 * i)          # 2x, 2y
    Ul = np.outer(x2, x2) + np.outer(y2, y2) + 4 * (np.outer(A[2 * n], A[2 * n]) + np.outer(A[2 * n + 1], A[2 * n + 1]))
    return Uf, Ul


def check_variances(ns=(3, 4, 5, 6)):
    import sympy as sp
    d = json.load(open(os.path.join(HERE, 'data_witnesses_variances.json')))['variance_polynomials']
    nsym = sp.symbols('n')
    res = {}
    for n in ns:
        N = n * n
        Uf, Ul = quad_forms(n)
        Ef, Ef2 = quad_form_moments(Uf, n)
        El, El2 = quad_form_moments(Ul, n)
        mean_full = Ef / N ** 2; var_full = (Ef2 - Ef ** 2) / N ** 4
        mean_low = El / (4 * N ** 2); var_low = (El2 - El ** 2) / (16 * N ** 4)
        par = 'odd' if n % 2 else 'even'
        pol_low = sp.sympify(d['low'][par]['expr']).subs(nsym, n)
        pol_full = sp.sympify(d['full'][par]['expr']).subs(nsym, n)
        r = {'mean_full': str(mean_full), 'var_full': str(var_full), 'mean_low': str(mean_low), 'var_low': str(var_low),
             'closed_mean_full': str(Fr(n ** 4 - 1, 6 * n * n)),
             'closed_mean_low': str(Fr((n * n + 1) * (n ** 4 - n * n + 12 * n - 12), 72 * n * n)),
             'poly_var_low_match': bool(sp.Rational(var_low.numerator, var_low.denominator) == sp.nsimplify(pol_low)),
             'poly_var_full_match': bool(sp.Rational(var_full.numerator, var_full.denominator) == sp.nsimplify(pol_full)),
             'std_full': math.sqrt(var_full), 'std_low': math.sqrt(var_low)}
        assert str(mean_full) == r['closed_mean_full'] and str(mean_low) == r['closed_mean_low'], (n, r)
        # Gaussian-mixture std (sum_j w_j chi2_1):  std = sqrt(2 sum w^2)
        s2 = Fr(N + 1, 12)
        if n % 2:
            wl = [s2 * Fr(n * n - 1, 12)] * 2 + [s2 * Fr(n - 1, n * n)] * 2
            wf = [s2 / n] * (2 * n - 2) + [s2 * Fr(n - 1, n * n)] * 2
        else:
            wl = [s2 * Fr(n * n - 1, 12)] * 2 + [s2 * Fr(1, n), s2 * Fr(n - 2, n * n)]
            wf = [s2 / n] * (2 * n - 2) + [s2 / n, s2 * Fr(n - 2, n * n)]
        r['gauss_std_low'] = math.sqrt(2 * sum(float(w) ** 2 for w in wl))
        r['gauss_std_full'] = math.sqrt(2 * sum(float(w) ** 2 for w in wf))
        res[n] = r
        print('  n=%d  E_low mean %s std %.4f (gauss %.3f)  E_full mean %s std %.4f (gauss %.3f)  polymatch %s %s'
              % (n, mean_low, r['std_low'], r['gauss_std_low'], mean_full, r['std_full'], r['gauss_std_full'],
                 r['poly_var_low_match'], r['poly_var_full_match']))
        if n == 3:
            print('     var_low', var_low, ' var_full', var_full)
        if n == 4:
            print('     var_low', var_low, ' var_full', var_full)
    OUT['variances'] = res


# ---------------------------------------------------------------- Loly invariant variance and n=4 distribution (exact)
def check_loly_n4():
    n, N = 4, 16
    # cells grouped by w=x^2+y^2 in {1/2,5/2,9/2}; I = sum s*w ; use 2I integer
    cnt = Counter()
    vals = list(range(1, 17))
    for inner in itertools.combinations(vals, 4):
        rest = [v for v in vals if v not in inner]
        for edge in itertools.combinations(rest, 8):
            corner_sum = sum(rest) - sum(edge)
            twoI = sum(inner) * 1 + sum(edge) * 5 + corner_sum * 9
            cnt[twoI] += 1
    tot = sum(cnt.values()) ; assert tot == math.comb(16, 4) * math.comb(12, 8)
    # multiplicity 4! 8! 4! uniform -> probabilities proportional to cnt
    mean = Fr(sum(k * v for k, v in cnt.items()), tot * 2)
    var = Fr(sum(k * k * v for k, v in cnt.items()), tot * 4) - mean ** 2
    p340 = Fr(cnt[680], tot)
    res = {'mean': str(mean), 'var': str(var), 'P_I_eq_340': float(p340), 'std': math.sqrt(var)}
    print('  n=4 Loly I: mean', mean, 'var', var, 'P(I=340)=%.4f' % float(p340), 'std %.2f' % math.sqrt(var))
    # null variance formula n^4 (n^4-1)(n^2-4)/1080
    for nn in (3, 4):
        print('   formula Var(I) n=%d:' % nn, Fr(nn ** 4 * (nn ** 4 - 1) * (nn * nn - 4), 1080))
    OUT['loly_n4'] = res


# ---------------------------------------------------------------- magic squares of order 4
def load_magic4():
    A = np.loadtxt(os.path.join(HERE, 'magic4_all7040.txt'), dtype=np.int64)
    assert A.shape == (7040, 16)
    assert len({tuple(a) for a in A}) == 7040
    assert (F_of(A, 4) == 0).all() and (np.sort(A, axis=1) == np.arange(1, 17)).all()
    # essentially different: D4 orbits
    seen = {}
    for a in A:
        g = a.reshape(4, 4); forms = []
        for k in range(4):
            r = np.rot90(g, k); forms += [tuple(r.ravel()), tuple(r.T.ravel())]
        seen.setdefault(min(forms), 0); seen[min(forms)] += 1
    assert len(seen) == 880 and set(seen.values()) == {8}
    reps = np.array(sorted(seen.keys()), dtype=np.int64)
    return A, reps


def check_swaps():
    res = {}
    for n, S in ((3, None), (4, None)):
        pass
    A4, reps4 = load_magic4()
    n = 4; N = 16
    A = incidence(n)
    cells = [(i, j) for i in range(n) for j in range(n)]
    # m(a,b) from incidence
    m_ab = {}
    for a, b in itertools.combinations(range(N), 2):
        m_ab[(a, b)] = int(((A[:, a] - A[:, b]) != 0).sum())
    gaps = Counter(); mins = Counter(); allvals = Counter(); bad = 0
    for S in reps4:
        best = None
        for (a, b), m in m_ab.items():
            T = S.copy(); T[a], T[b] = T[b], T[a]
            F = int(F_of(T[None, :], n)[0])
            d = abs(int(S[a]) - int(S[b]))
            if F != d * d * m:
                bad += 1
            allvals[F] += 1
            best = F if best is None else min(best, F)
        mins[best] += 1
    res['n4_swaps'] = sum(allvals.values()); res['n4_formula_failures'] = bad
    res['n4_distinct_gap_values'] = len(allvals); res['n4_min_gap_value'] = min(allvals); res['n4_max_gap_value'] = max(allvals)
    res['n4_min_gap_multiset'] = dict(sorted(mins.items()))
    res['n4_gap_spectrum'] = dict(sorted(allvals.items()))
    # n=3: 8 squares
    n = 3; A3 = incidence(3)
    sq3 = []
    for p in itertools.permutations(range(1, 10)):
        if F_of(np.array([p]), 3)[0] == 0:
            sq3.append(np.array(p))
    mins3 = Counter(); bad3 = 0; ns3 = 0
    for S in sq3:
        best = None
        for a, b in itertools.combinations(range(9), 2):
            m = int(((A3[:, a] - A3[:, b]) != 0).sum())
            T = S.copy(); T[a], T[b] = T[b], T[a]
            F = int(F_of(T[None, :], 3)[0]); d = abs(int(S[a]) - int(S[b]))
            bad3 += (F != d * d * m); ns3 += 1
            best = F if best is None else min(best, F)
        mins3[best] += 1
    res['n3_swaps'] = ns3; res['n3_formula_failures'] = bad3; res['n3_min_gap_multiset'] = dict(mins3)
    # Siamese squares
    def siamese(n):
        S = np.zeros((n, n), int); i, j = 0, n // 2
        for v in range(1, n * n + 1):
            S[i, j] = v
            ni, nj = (i - 1) % n, (j + 1) % n
            if S[ni, nj]:
                ni, nj = (i + 1) % n, j
            i, j = ni, nj
        return S.ravel()
    sm = {}
    for n in (5, 7, 9):
        S = siamese(n); assert F_of(S[None, :], n)[0] == 0
        A_ = incidence(n); best = None; bad = 0
        for a, b in itertools.combinations(range(n * n), 2):
            m = int(((A_[:, a] - A_[:, b]) != 0).sum())
            T = S.copy(); T[a], T[b] = T[b], T[a]
            F = int(F_of(T[None, :], n)[0]); d = abs(int(S[a]) - int(S[b]))
            bad += (F != d * d * m)
            best = F if best is None else min(best, F)
        sm[n] = {'min_gap_N2E': best, 'formula_failures': bad}
    res['siamese'] = sm
    OUT['swaps'] = res
    for k, v in res.items():
        if k != 'n4_gap_spectrum':
            print('  swaps', k, v)
    return reps4


def check_product_inertia(reps4):
    n = 4
    j = np.tile(np.arange(n), n); i = np.repeat(np.arange(n), n)
    xy4 = (2 * j - 3) * (3 - 2 * i)          # 4xy
    P = np.abs(reps4 @ xy4) / 4.0           # |sum s x y|  (same for z since sum xy = 0)
    vals = sorted(set(P.tolist()))
    OUT['product_inertia'] = {'distinct': len(vals), 'min': vals[0], 'max': vals[-1], 'n_zero': int((P == 0).sum())}
    print('  product of inertia |P_xy| over 880: distinct', len(vals), 'range', vals[0], vals[-1], 'zero for', int((P == 0).sum()))


def check_witnesses():
    d = json.load(open(os.path.join(HERE, 'data_witnesses_variances.json')))['witnesses_k_star_n_minus_1']['squares']
    out = {}
    for ns, S in d.items():
        n = int(ns); S = np.array(S); N = n * n; M = n * (N + 1) // 2
        assert sorted(S.ravel()) == list(range(1, N + 1))
        rho = S.sum(axis=1) - M; gam = S.sum(axis=0) - M
        want = np.array([(-1) ** jj * math.comb(n - 1, jj) for jj in range(n)])
        x = np.arange(n) - (n - 1) / 2
        ok = (rho == 0).all() and (gam == want).all()
        # degree-(n-2) conditions
        deg = all(abs(sum(x[jj] ** m * gam[jj] for jj in range(n))) < 1e-6 for m in range(0, n - 1))
        out[n] = bool(ok and deg)
    # n=3,4 theorem witnesses
    W3 = np.array([[1, 3, 9], [8, 6, 5], [7, 4, 2]]); W4 = np.array([[14, 2, 5, 13], [8, 15, 7, 4], [12, 3, 9, 10], [1, 11, 16, 6]])
    r3 = (W3.sum(0) - 15, W3.sum(1) - 15); r4 = (W4.sum(0) - 34, W4.sum(1) - 34)
    out['W3 (gamma,rho)'] = (r3[0].tolist(), r3[1].tolist()); out['W4 (gamma,rho)'] = (r4[0].tolist(), r4[1].tolist())
    # four-term witness
    S = np.array([[9, 4, 12, 3], [16, 1, 14, 7], [10, 15, 11, 8], [2, 5, 6, 13]])
    out['four-term witness rows'] = (S.sum(1)).tolist(); out['cols'] = S.sum(0).tolist()
    out['diag'] = (int(np.trace(S)), int(np.trace(S[:, ::-1])))
    out['N2Efull'] = int(F_of(S.ravel()[None, :], 4)[0])
    x2 = (2 * np.tile(np.arange(4), 4) - 3); y2 = (3 - 2 * np.repeat(np.arange(4), 4))
    z = S.ravel() - 8.5
    out['Cov X,Y numerators'] = (float(z @ x2), float(z @ y2))
    # gamma, rho of that witness and sum y^2 rho
    rho = S.sum(1) - 34; gam = S.sum(0) - 34
    y = np.array([1.5, .5, -.5, -1.5])
    out['four-term gamma,rho'] = (gam.tolist(), rho.tolist(), float((y ** 2 * rho).sum()))
    # Table: witness condition k*(3)=2? degree1 for W3
    OUT['witnesses'] = out
    print('  witnesses', out)


# ---------------------------------------------------------------- L4 etc
def check_L4():
    for fn in ('enum_n3.jsonl', 'enum_n4.jsonl'):
        for line in open(os.path.join(HERE, fn)):
            print('  ', fn, line.strip()[:240])
    s = 0
    for line in open(os.path.join(HERE, 'mc_n4.jsonl')):
        d = json.loads(line); s += d['hits_L']
    print('  MC n=4 total hits_L', s, 'of 2e9; |L4|/16! =', 14639440 / math.factorial(16), 'expected hits', 2e9 * 14639440 / math.factorial(16))
    # diagonal-only class by direct combinatorics: ordered pairs of disjoint 4-subsets of 1..16 with sum 34
    subs = [frozenset(c) for c in itertools.combinations(range(1, 17), 4) if sum(c) == 34]
    pairs = sum(1 for a in subs for b in subs if not (a & b))
    diag = pairs * math.factorial(4) ** 2 * math.factorial(8)
    print('  diagonal-only class by direct combinatorics:', len(subs), 'subsets,', pairs, 'disjoint ordered pairs ->', diag, '(enumerator: 49932288000)')
    assert diag == 49932288000
    OUT['L4'] = {'p': 14639440 / math.factorial(16), 'mc_hits': s, 'diag_only': diag}


def main():
    print('[n=3 exhaustive]'); check_n3()
    print('[exact moments]'); check_variances()
    print('[Loly n=4]'); check_loly_n4()
    print('[swaps]'); reps4 = check_swaps()
    print('[product of inertia]'); check_product_inertia(reps4)
    print('[witnesses]'); check_witnesses()
    print('[L4]'); check_L4()
    json.dump(OUT, open(os.path.join(HERE, 'verify_numbers.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
