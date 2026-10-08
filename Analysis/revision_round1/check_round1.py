"""Round-1 referee checks (author's verification).

1. n=3 exhaustive: number of arrangements with Loly's I = 60 (RefB: 24,192), number
   satisfying the degree-2 conditions (72 = semi-magic), mean and variance of I.
2. Null distribution of Loly's I for a uniformly random arrangement:
   E[I] = n^2(n^4-1)/12,  Var(I) = N^2 sigma_n^2 Var_grid(x^2+y^2) = n^4(n^4-1)(n^2-4)/1080.
   Checked exactly (Wald-Wolfowitz identity as rational arithmetic) for n=3..12, against the
   exhaustive n=3 values, and by Monte Carlo for n=4,5.
3. The witnesses for k*(n) = n-1, 4 <= n <= 13 (from Analysis/revision/theory/results.json):
   permutation of 1..N, all row sums M(n), column deviations (-1)^j C(n-1,j); hence the
   degree-(n-2) conditions hold (checked exactly for all m <= n-2) and the square is not semi-magic.
4. The v4 sampling question: what the archived data file and the v4 code actually contain.
5. Correlation of the two diagonal statistics for even n: -1/(n-1) (not -1/(n^2-1)).

Writes results_round1.json next to this file.  Runtime ~2 min.
"""
import itertools, json, os, sys, time
from fractions import Fraction
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
out = {}


def grid(n):
    x = np.array([j - (n - 1) / 2 for i in range(n) for j in range(n)])
    y = np.array([(n - 1) / 2 - i for i in range(n) for j in range(n)])
    return x, y


# ---------------------------------------------------------------- 1. n=3 exhaustive
t0 = time.time()
n = 3; N = 9
x, y = grid(n); r2 = x ** 2 + y ** 2
x2 = (2 * x).astype(int); y2 = (2 * y).astype(int)  # doubled integer coordinates
r2i = (x2 ** 2 + y2 ** 2)  # 4*(x^2+y^2), integer
perms = np.array(list(itertools.permutations(range(1, 10))), dtype=np.int64)  # (362880, 9)
z = perms - 5
I = (perms * r2i).sum(1) // 4  # exact integer: r2 is integer for n=3
cnt_I60 = int((I == 60).sum())
deg1 = ((z * x2).sum(1) == 0) & ((z * y2).sum(1) == 0)
deg2 = deg1 & ((z * x2 ** 2).sum(1) == 0) & ((z * y2 ** 2).sum(1) == 0)
S = perms.reshape(-1, 3, 3)
semi = (S.sum(1) == 15).all(1) & (S.sum(2) == 15).all(1)
meanI = Fraction(int(I.sum()), len(I))
varI = Fraction(int((I * I).sum()), len(I)) - meanI ** 2
out['n3_exhaustive'] = dict(arrangements=len(I), I_equals_60=cnt_I60, degree2=int(deg2.sum()),
                            semi_magic=int(semi.sum()), degree1=int(deg1.sum()),
                            I_mean=str(meanI), I_var=str(varI), I_min=int(I.min()), I_max=int(I.max()),
                            I_distinct=int(len(np.unique(I))),
                            fraction_I60=cnt_I60 / len(I))
print('n=3: I=60 count', cnt_I60, '(%.2f%%)' % (100 * cnt_I60 / len(I)), '| degree-2:', int(deg2.sum()),
      '| semi-magic:', int(semi.sum()), '| mean I', meanI, '| var I', varI,
      '| distinct', len(np.unique(I)), 'range', I.min(), I.max(), '(%.0fs)' % (time.time() - t0))
assert cnt_I60 == 24192 and int(deg2.sum()) == 72 and meanI == 60 and varI == 30


# ---------------------------------------------------------------- 2. null distribution of I, general n
def loly_value(n):
    return Fraction(n ** 2 * (n ** 4 - 1), 12)


def var_I_formula(n):
    return Fraction(n ** 4 * (n ** 4 - 1) * (n ** 2 - 4), 1080)


def var_I_ww(n):
    """Wald-Wolfowitz: Var(sum_c a_c b_pi(c)) = (1/(N-1)) sum(a-abar)^2 sum(b-bbar)^2, a = x^2+y^2, b = s."""
    N = n * n
    xs = [Fraction(2 * j - (n - 1), 2) for j in range(n)]
    r2 = [xi ** 2 + yi ** 2 for xi in xs for yi in xs]
    abar = sum(r2) / N
    sa = sum((a - abar) ** 2 for a in r2)
    sb = sum((Fraction(v) - Fraction(N + 1, 2)) ** 2 for v in range(1, N + 1))
    return sa * sb / (N - 1)


tbl = {}
for n in range(3, 13):
    vw, vf = var_I_ww(n), var_I_formula(n)
    assert vw == vf, (n, vw, vf)
    tbl[n] = dict(E_I=str(loly_value(n)), Var_I=str(vf), sd_I=float(vf) ** 0.5)
    print(f'n={n}: E[I]={loly_value(n)}  Var(I)={vf} = {float(vf):.4f}  sd={float(vf)**0.5:.4f}')
out['null_I_exact'] = tbl
assert var_I_formula(3) == 30

rng = np.random.default_rng(20261007)
mc = {}
for n, nsamp in ((4, 20_000_000), (5, 10_000_000)):
    N = n * n
    x, y = grid(n); r2 = x ** 2 + y ** 2
    tot = 0.0; tot2 = 0.0; hit = 0
    batch = 1_000_000
    for _ in range(nsamp // batch):
        P = rng.permuted(np.tile(np.arange(1, N + 1), (batch, 1)), axis=1)
        Ib = (P * r2).sum(1)
        tot += Ib.sum(); tot2 += (Ib * Ib).sum()
        hit += int(np.isclose(Ib, float(loly_value(n))).sum())
    m = tot / nsamp; v = tot2 / nsamp - m * m
    mc[n] = dict(samples=nsamp, mean=m, var=v, exact_mean=float(loly_value(n)), exact_var=float(var_I_formula(n)),
                 frac_at_loly_value=hit / nsamp, se_mean=float(var_I_formula(n) ** Fraction(1, 2)) / nsamp ** 0.5)
    print(f'n={n} MC ({nsamp:.0e}): mean I={m:.4f} (exact {float(loly_value(n))}), var={v:.3f} '
          f'(exact {float(var_I_formula(n)):.3f}); fraction with I = Loly value: {hit/nsamp:.5f}')
out['null_I_mc'] = mc


# ---------------------------------------------------------------- 3. witnesses for k*(n)=n-1, n<=13
R = json.load(open(f'{ROOT}/Analysis/revision/theory/results.json'))
key = [k for k in R if k.startswith('permutation_threshold_search')][0]
wit = {}
for n in range(4, 14):
    S = np.array(R[key][str(n)]['square'], dtype=np.int64)
    N = n * n
    assert S.shape == (n, n) and sorted(S.ravel().tolist()) == list(range(1, N + 1))
    M = n * (N + 1) // 2
    rows = S.sum(1) - M
    cols = S.sum(0) - M
    v = np.array([(-1) ** j * comb(n - 1, j) for j in range(n)])
    assert (rows == 0).all(), (n, rows)
    assert (cols == v).all(), (n, cols, v)
    # degree-(n-2) conditions, exact: sum_j (2x_j)^m gamma_j = 0 for m=1..n-2 (doubled nodes)
    X2 = np.array([2 * j - (n - 1) for j in range(n)], dtype=object)
    moms = [int(sum(X2[j] ** m * int(cols[j]) for j in range(n))) for m in range(1, n)]
    assert all(mm == 0 for mm in moms[:n - 2]) and moms[n - 2] != 0, (n, moms)
    wit[n] = dict(square=S.tolist(), col_devs=cols.tolist(), ok=True, moment_n_minus_1_doubled=moms[n - 2])
    print(f'n={n}: witness ok; rows all {M}; gamma = {cols.tolist()}; <x^(n-1),z>*N*2^(n-1) = {moms[n-2]}')
out['witnesses'] = wit

# ---------------------------------------------------------------- 4. the v4 sampling data and code
sys.path.insert(0, f'{ROOT}/Analysis')
from src.analysis import compute_total_energy_vectorized  # the v4 sampler's energy
D = json.load(open(f'{ROOT}/Analysis/data/large_scale_landscape.json'))
v4 = {}
pL = {4: 14639440 / 20922789888000.0}  # |L_4| / 16!
for k in ('4', '5'):
    d = D[k]
    v4[k] = dict(n_samples=d['n_samples'], magic_count=d['magic_count'], min_energy=d['stats']['min'],
                 zero_fraction=d['stats']['zero_fraction'])
v4['expected_L4_members_in_archived_run'] = D['4']['n_samples'] * pL[4]
v4['expected_L4_members_in_6e7'] = 6e7 * pL[4]
W = np.array([[9, 4, 12, 3], [16, 1, 14, 7], [10, 15, 11, 8], [2, 5, 6, 13]])
e = compute_total_energy_vectorized(W[None])[0]
v4['E_v4_on_L4_witness'] = float(e)
v4['E_v4_on_L4_witness_is_exact_zero'] = bool(e == 0.0)
# how often is a member of L_4 missed by the 1e-10 tolerance? never, if the energy is exactly 0:
# cov terms are means of products of half-integers and integers -> exact in binary floating point.
print('v4 archived run: n=4 samples', D['4']['n_samples'], 'min E_v4', D['4']['stats']['min'],
      '; n=5 samples', D['5']['n_samples'], '; expected L_4 members in archived run',
      round(v4['expected_L4_members_in_archived_run'], 3), '; in 6e7 samples', round(v4['expected_L4_members_in_6e7'], 1))
print('E_v4 on the 4x4 member of L_4 (Remark 4.3):', e, '(exact zero:', e == 0.0, ')')
out['v4_sampling'] = v4

# ---------------------------------------------------------------- 4b. product of inertia over the 880 (RefB point 5)
SQ = np.load(f'{ROOT}/Analysis/data/magic_squares_880 (1).npy')
x4, y4 = grid(4)
Ixy = np.array([-(S.ravel() * x4 * y4).sum() for S in SQ])   # I_xy = -sum s_ij x_ij y_ij (planar, value-weighted)
Ixy4 = np.rint(4 * Ixy).astype(int)  # x*y is a multiple of 1/4
vals, cnts = np.unique(Ixy4, return_counts=True)
out['product_of_inertia_880'] = dict(distinct=int(len(vals)), min=float(vals.min() / 4), max=float(vals.max() / 4),
                                     n_zero=int(cnts[vals == 0][0]) if (vals == 0).any() else 0,
                                     values_over_4=vals.tolist(), counts=cnts.tolist())
absv = np.unique(np.abs(Ixy4))
out['product_of_inertia_880'].update(abs_distinct=int(len(absv)), abs_max=float(absv.max() / 4))
print('I_xy over the 880 order-4 squares: distinct values', len(vals), 'range', vals.min() / 4, '..', vals.max() / 4,
      '; squares with I_xy = 0:', out['product_of_inertia_880']['n_zero'], '; distinct |I_xy|:', len(absv), 'max', absv.max() / 4)

# ---------------------------------------------------------------- 5. diagonal correlation, even n
corr = {}
for n in (4, 6, 8):
    N = n * n
    dm = np.zeros(N); da = np.zeros(N)
    for i in range(n):
        dm[i * n + i] = 1; da[i * n + (n - 1 - i)] = 1
    c = np.corrcoef(dm, da)[0, 1]
    corr[n] = dict(empirical=float(c), minus_1_over_n_minus_1=-1 / (n - 1), minus_1_over_n2_minus_1=-1 / (n * n - 1))
    assert abs(c + 1 / (n - 1)) < 1e-12
    print(f'n={n}: corr(D_m, D_a) = {c:.6f} = -1/(n-1) = {-1/(n-1):.6f}  (not -1/(n^2-1) = {-1/(n*n-1):.6f})')
out['diag_corr'] = corr

json.dump(out, open(f'{HERE}/results_round1.json', 'w'), indent=1)
print('wrote results_round1.json')
