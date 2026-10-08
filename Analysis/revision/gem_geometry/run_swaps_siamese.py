"""Parts B and C: exact swap-gap verification and Siamese-square gems."""
import json, sys, os
from fractions import Fraction
from itertools import combinations
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gem_geometry import exact_hull

ROOT = '/Users/kylemathewson/magicGem'
SQ880 = np.load(f'{ROOT}/Analysis/data/magic_squares_880 (1).npy')


# ------------------------------------------------------------- exact symmetric energy
def lines(n):
    L = []
    for i in range(n):
        L.append([(i, j) for j in range(n)])          # rows
    for j in range(n):
        L.append([(i, j) for i in range(n)])          # columns
    L.append([(i, i) for i in range(n)])              # main diagonal
    L.append([(i, n - 1 - i) for i in range(n)])      # anti-diagonal
    return L


def E_full_exact(S):
    """Symmetric E_full = sum over 2n+2 lines of Cov(phi_L, Z)^2, exact Fraction.
    Cov(phi,Z) = (1/N) sum_cells (phi - mean phi) z,  z = s - (N+1)/2."""
    S = np.asarray(S); n = S.shape[0]; N = n * n
    z = {(i, j): Fraction(2 * int(S[i, j]) - (N + 1), 2) for i in range(n) for j in range(n)}
    mean_phi = Fraction(n, N)
    E = Fraction(0)
    for L in lines(n):
        Ls = set(L)
        cov = sum(((Fraction(1) if c in Ls else Fraction(0)) - mean_phi) * z[c] for c in z) / N
        E += cov * cov
    return E


def m_lines(n, a, b):
    """number of the 2n+2 lines containing exactly one of the cells a, b"""
    return sum(1 for L in lines(n) if (a in L) != (b in L))


def swap_check(S):
    S = np.asarray(S); n = S.shape[0]; N = n * n
    E0 = E_full_exact(S)
    cells = [(i, j) for i in range(n) for j in range(n)]
    gaps = []; ok = True; bad = []
    for a, b in combinations(cells, 2):
        T = S.copy(); T[a], T[b] = S[b], S[a]
        dE = E_full_exact(T) - E0
        d = abs(int(S[a]) - int(S[b]))
        pred = Fraction(d * d * m_lines(n, a, b), N * N)
        if dE != pred:
            ok = False; bad.append((a, b, str(dE), str(pred)))
        gaps.append(dE)
    return E0, ok, bad, gaps


def lo_shu_variants():
    L = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
    out = []; T = L
    for _ in range(4):
        out.append(T.copy()); out.append(T.T.copy()); T = np.rot90(T)
    return out


def siamese(n):
    assert n % 2 == 1
    S = np.zeros((n, n), dtype=int)
    i, j = 0, n // 2
    for k in range(1, n * n + 1):
        S[i, j] = k
        ni, nj = (i - 1) % n, (j + 1) % n
        if S[ni, nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return S


def is_magic(S):
    S = np.asarray(S); n = S.shape[0]; M = n * (n * n + 1) // 2
    return (S.sum(0) == M).all() and (S.sum(1) == M).all() and \
        np.trace(S) == M and np.trace(np.fliplr(S)) == M and sorted(S.ravel()) == list(range(1, n * n + 1))


results = {}
# ---- n = 4, 880 squares
total_swaps = 0; all_ok = True; counterexamples = []; mingaps = Counter(); E0s = set()
for k, S in enumerate(SQ880):
    E0, ok, bad, gaps = swap_check(S)
    E0s.add(E0); total_swaps += len(gaps); all_ok &= ok; counterexamples += [(k,) + b for b in bad]
    mingaps[min(gaps) * 256] += 1
print('n=4: swaps checked', total_swaps, 'formula ok:', all_ok, 'E0 values:', E0s)
print('n=4 min-gap multiset (x256):', sorted(mingaps.items()))
results['n4'] = dict(n_squares=880, swaps_checked=total_swaps, formula_agrees=all_ok,
                     counterexamples=counterexamples, E0_all_zero=(E0s == {0}),
                     min_gap_times_N2_distribution={str(k): v for k, v in sorted(mingaps.items())})

# ---- n = 3, 8 squares
total3 = 0; ok3 = True; bad3 = []; mingaps3 = Counter(); allgaps3 = Counter()
for S in lo_shu_variants():
    assert is_magic(S)
    E0, ok, bad, gaps = swap_check(S)
    assert E0 == 0
    total3 += len(gaps); ok3 &= ok; bad3 += bad
    mingaps3[min(gaps) * 81] += 1
    for g in gaps: allgaps3[g * 81] += 1
print('n=3: swaps checked', total3, 'formula ok:', ok3, 'min gaps (x81):', sorted(mingaps3.items()))
print('n=3 all gaps (x81):', sorted(allgaps3.items()))
results['n3'] = dict(n_squares=8, swaps_checked=total3, formula_agrees=ok3, counterexamples=bad3,
                     min_gap_times_N2_distribution={str(k): v for k, v in sorted(mingaps3.items())},
                     all_gap_times_N2_distribution={str(k): v for k, v in sorted(allgaps3.items())})

# ---- all-gap distribution for n=4 (first pass only values, cheap):
allgaps4 = Counter()
for k, S in enumerate(SQ880):
    n = 4; N = 16
    for a, b in combinations([(i, j) for i in range(4) for j in range(4)], 2):
        d = abs(int(S[a]) - int(S[b])); allgaps4[d * d * m_lines(4, a, b)] += 1
results['n4']['all_gap_times_N2_distribution_from_formula'] = {str(k): v for k, v in sorted(allgaps4.items())}
results['n4']['n_distinct_gap_values'] = len(allgaps4)

# ---- Siamese squares n=5,7,9: swap min gap
results['siamese_swaps'] = {}
for n in (5, 7, 9):
    S = siamese(n); assert is_magic(S)
    E0, ok, bad, gaps = swap_check(S)
    N = n * n
    mg = min(gaps)
    print(f'Siamese n={n}: formula ok {ok}, E0={E0}, min gap = {mg} = {mg * N * N}/{N * N}')
    results['siamese_swaps'][n] = dict(formula_agrees=ok, min_gap=str(mg), min_gap_times_N2=int(mg * N * N),
                                        swaps_checked=len(gaps))

# ---- Siamese hulls n = 3..21
results['siamese_hulls'] = {}
for n in range(3, 23, 2):
    S = siamese(n); assert is_magic(S)
    h = exact_hull(S)
    cells = [(v // n, v % n) for v in h['vertices']]
    vals = [int(S[c]) for c in cells]
    print(f'Siamese n={n}: V,E,F={h["f_vector"]}, face sizes={h["face_sizes"]}, vol={h["volume"]}')
    print('   hull cells (i,j,value):', [(c[0], c[1], v) for c, v in zip(cells, vals)])
    results['siamese_hulls'][n] = dict(f_vector=h['f_vector'], face_sizes=h['face_sizes'], volume=str(h['volume']),
                                       hull_cells=[[int(c[0]), int(c[1]), int(v)] for c, v in zip(cells, vals)],
                                       hull_fraction=h['f_vector'][0] / (n * n))
# check predicted 12 cells for n>=5 (see siamese_proof.py for the structural description)
with open(f'{HERE}/results_swaps_siamese.json', 'w') as f:
    json.dump(results, f, indent=1, default=str)
print('saved results_swaps_siamese.json')
