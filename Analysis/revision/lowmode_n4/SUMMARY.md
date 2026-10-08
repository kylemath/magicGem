# Low-mode balanced class for n = 4: exact enumeration

Directory: `Analysis/revision/lowmode_n4/`. Reproduce everything with `bash run_all.sh`
(about 3 minutes; `bash run_all.sh mc` also reruns the Monte Carlo, about 15 minutes on 16 cores).
Machine: Apple M4 Max, 16 cores, 128 GB, Apple clang 17, Python 3.9 / numpy 2.0.

## Definitions

n x n arrangement of {1..N}, N = n^2, cells (i, j) 0-indexed.
T1 = sum j s_ij, T2 = sum i s_ij (targets (n-1)N(N+1)/4 = 45 for n=3, 204 for n=4);
T3 = main diagonal sum, T4 = anti-diagonal sum (target M(n) = n(N+1)/2).
L_n = {T1 = T2 = target, T3 = T4 = M} = {E_low = 0}. XY = first two conditions only; DIAG = last two only.

## Main results (exact)

| quantity | n = 3 | n = 4 |
|---|---|---|
| \|L_n\| | 8 | **14,639,440** |
| magic squares in L_n | 8 | 7,040 |
| D4 orbits of L_n | 1 | 1,829,930 (free action: 8 x 1,829,930) |
| \|XY\| | 760 | 6,697,177,424 |
| \|DIAG\| | 4,224 | 49,932,288,000 |
| semi-magic (all rows and cols = M) | 72 | 549,504 = 8 x 68,688 |
| \|L_n\| / N! | 2.2e-5 | 6.997e-7 (1 in 1.43 million) |

Breakdown of L_4 by (#row sums = 34, #column sums = 34):

| rows \ cols | 0 | 1 | 4 |
|---|---|---|---|
| 0 | 9,637,312 | 2,172,824 | 100,728 |
| 1 | 2,172,824 | 429,312 | 9,336 |
| 4 | 100,728 | 9,336 | **7,040** (magic) |

Coarse: magic 7,040; all rows = 34 but not all columns 110,064; all columns but not all rows 110,064;
neither 14,412,272 (of which 9,637,312 have no line sum equal to 34 at all).
Exactly 2 or 3 equal rows (or columns) never occur: with R_i = 34 + e_i the conditions sum e_i = 0 and
sum i e_i = 0 (this is T2) cannot hold with only one or two nonzero e_i.
The paper's counterexample [[9,4,12,3],[16,1,14,7],[10,15,11,8],[2,5,6,13]] is in L_4 (class (0,0)).
Among non-magic members the symmetric E_full ranges from 1/64 to 5.3125 (mean 1.91).

## Validation

* n = 3: all seven modes of the enumerator agree with brute force over 9! (8, 760, 4224, 8 magic, 72 semi-magic, 8, 8).
* n = 4: the magic count 7,040 is reproduced by an independent 8-statistic key (rows, columns, diagonals);
  semi-magic 549,504 = 8 x 68,688 (known count of 4x4 semi-magic squares up to D4);
  DIAG = 49,932,288,000 reproduced by direct combinatorics (ordered pairs of disjoint 4-sets summing to 34, times 8!);
  ROWSL = COLSL = 117,104 equals 100,728 + 9,336 + 7,040 from the explicit member list;
  Monte Carlo with 2e9 samples: P(L) = 6.865e-7 +/- 2.7 % vs exact 6.997e-7; P(XY) and P(DIAG) agree to 0.1 %.
* The L_4 member list is D4-closed with 8 x (number of orbits) = |L_4|.

## Gaussian local-limit estimate

(T1..T4) under a uniform permutation has mean = target and covariance
Sigma_mk = (1/(N-1)) sum_c (a_m,c - abar_m)(a_k,c - abar_k) sum_v (v - vbar)^2. T1, T2, diagonals are mutually
uncorrelated except corr(T3, T4) = -1/(N-1) for even n (0 for odd n). The step lattice is Z^4 (Smith normal form, n = 3..8),
so estimate = N! (2 pi)^-2 det(Sigma)^-1/2.

| n | Gaussian \|L_n\| | exact / MC | ratio |
|---|---|---|---|
| 3 | 13.6 | 8 | 0.59 |
| 4 | 1.8235e7 | 14,639,440 | 0.803 |
| 5 | 6.70e17 | 5.09e17 (MC, 1e10 samples, 328 hits, +/-5.5 %) | 0.76 |
| 6 | 1.49e33 | 1.15e33 (MC, 2e10 samples, 62 hits, +/-13 %) | 0.78 |

Two-condition classes: XY ratio 0.59 (n=3), 0.91 (n=4), 0.93 (n=5 MC), 0.96 (n=6 MC); DIAG ratio 1.10 (n=3), 0.96 (n=4), 0.92 (n=5 MC), 0.94 (n=6 MC).
The four-condition ratio is below the product of the two-condition ratios (0.80 vs 0.88 at n=4): the discrete
joint distribution carries a small negative dependence that the Gaussian misses.

**Conjectural estimates:** |L_5| ~ 5-7 x 10^17 (of 25! = 1.55e25), |L_6| ~ 1-1.5 x 10^33 (of 36! = 3.7e41).
Scaling: det(Sigma)^1/2 grows like n^13, so |L_n|/N! ~ c n^-13.

## Surprises / things the paper text must change

1. v4 says the probability of E_low = 0 is "estimated below 1e-8 for n = 4"; it is 7.0e-7, so 460 million
   uniform samples should contain about 320 non-magic members of L_4. The earlier sampling failure is not explained
   by rarity; the v5 text should say so (or drop the claim).
2. Row/column equality counts in L_4 are only 0, 1 or 4 (never 2 or 3), a one-line consequence of the T2 condition.
3. L_4 is 2080 times larger than the magic squares; "all rows equal but not columns" (110,064) is itself 15.6 times larger.
4. The Gaussian local limit is already within 20 % at n = 4 and the ratio appears to approach 1 slowly from below.

## Files

* `lowmode_enum.c` - meet-in-the-middle enumerator (modes L, XY, DIAG, MAGIC, SEMI, ROWSL, COLSL), pthreads.
* `lowmode_mc.c` - Monte Carlo hit counter (xoshiro256**).
* `gaussian_estimate.py` - covariance matrices, lattice index, Gaussian estimates (-> gaussian_estimates.json).
* `analyze_members.py` - breakdown, D4 orbits, gallery, figures (-> members_analysis.json, fig_lowmode_gallery.pdf, fig_lowmode_vs_full_n4.pdf).
* `assemble_results.py` - -> results.json. `raw_outputs/` holds the raw JSON lines of every run.
* `fragment.tex` - LaTeX for Section 4.4 (proposition, computation paragraph, table, estimate, figure).
* The explicit list of the 14,639,440 members (234 MB, uint8 16 bytes each) is regenerated into `work/` by run_all.sh and not committed.
