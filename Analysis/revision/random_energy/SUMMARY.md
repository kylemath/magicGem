# Random-arrangement energy: exact theory, exhaustive n=3, Monte Carlo n=3..8, search experiment

Directory: `Analysis/revision/random_energy/`. All numbers in `results.json`; LaTeX in `fragment.tex`
(bib entries in `refs.bib`); figure `fig_random_energy.pdf` (+ `.png` preview).

Conventions: N = n^2, x_ij = j-(n-1)/2, y_ij = (n-1)/2-i, z_ij = s_ij-(N+1)/2, Cov(phi,Z) = (1/N) sum (phi-mean phi) z.
E_low = Cov(X,Z)^2+Cov(Y,Z)^2+Cov(Dm,Z)^2+Cov(Da,Z)^2.
E_full (symmetric) = sum over all n rows + all n columns + 2 diagonals of Cov(L,Z)^2  (2n+2 terms).

## 1. Exact theory (theory.py, fit_variance.py)

Let sigma_n^2 := Var(Z)/(N-1) = (N+1)/12 = (n^2+1)/12. For a uniformly random permutation,
T_phi := Cov(phi,Z) is a linear permutation statistic, E[T_phi]=0 and (Wald-Wolfowitz/Hoeffding identity)

    Cov(T_phi, T_psi) = sigma_n^2 * Cov_grid(phi, psi)        (population covariance over the N cells)

Hence:
* E[Cov(X,Z)^2] = E[Cov(Y,Z)^2] = (n^4-1)/144
* E[Cov(D,Z)^2] = E[Cov(R_k,Z)^2] = (n-1)(n^2+1)/(12 n^2)   [= n(N-n)Var(Z)/((N-1)N^2)]
* **E[E_low]  = (n^2+1)(n^4 - n^2 + 12n - 12)/(72 n^2) = n^4/72 + n/6 - 13/72 + 1/(6n) - 1/(6n^2)**   (c = 1/72)
* **E[E_full] = (n^4-1)/(6 n^2)**  (= n^2/6 - 1/(6n^2))
* For n=3 both equal 40/27 = 1.4815 (Var(X) = (n^2-1)/12 equals (n-1)/n only at n=3).

Gram matrix G (Sigma_T = sigma_n^2 G):
* E_low: diag((n^2-1)/12, (n^2-1)/12, (n-1)/n^2, (n-1)/n^2); Cov(Dm,Da) = 0 (n odd) or -1/n^2 (n even); X,Y orthogonal to both diagonals and to each other.
* E_full: rows block (1/n)(I - J/n), columns block the same, all row-column / row-diagonal / column-diagonal covariances 0, diagonal 2x2 block as above.

Eigenvalues (= weights w_j of the limiting sum_j w_j chi^2_1):
* E_low:  sigma_n^2 {(n^2-1)/12 (x2), (n-1)/n^2 (x2)}  [n odd];  sigma_n^2 {(n^2-1)/12 (x2), 1/n, (n-2)/n^2}  [n even]
* E_full: sigma_n^2 {1/n (x 2n-2), (n-1)/n^2 (x2)}       [n odd];  sigma_n^2 {1/n (x 2n-1), (n-2)/n^2}           [n even]

Exact variance (fourth moments of permutation statistics via Moebius inversion over the 15 equality
patterns of a cell quadruple; falling-factorial denominators cancel; verified against exhaustive n=3
and by exact rational interpolation on n=3..45 with 5-11 held-out orders):
* Var(E_low), n odd  = (n-1)(n^2+1)(25n^11+25n^10-82n^9-82n^8-9n^7-1209n^6+3738n^5-5862n^4+2160n^3-2880n^2-4320n+4320)/(129600 n^6)
* Var(E_low), n even = (n^2+1)(25n^10-107n^8+73n^6-1200n^5+4947n^4-9600n^3+13782n^2-13680n+10080)/(129600 n^4)
* Var(E_full), n odd  = (n-1)(n^2+1)(5n^6-5n^5-17n^4+11n^3-24n^2+18n+6)/(180 n^6)
* Var(E_full), n even = (n-2)(n^2+1)(5n^5-12n^3+12n^2-23n+12)/(180 n^5)
* Leading terms: Var(E_low) ~ n^8/5184 = (n^4/72)^2, Var(E_full) ~ n^3/36; both equal the leading term of
  the Gaussian-limit variance 2 sum w_j^2, but the ratio exact/Gaussian is 0.51,0.76,0.86,0.90,0.93,0.95
  (E_low, n=3..8) and 0.24,0.45,0.56,0.64,0.69,0.73 (E_full).

CLT: Hoeffding (1951, Thm 3) applies to every fixed linear combination of T_X, T_Y, T_Dm, T_Da
(the condition ratio equals N^{1-r/2} kappa_r(a) kappa_r(z) = O(N^{1/2-r/4}) -> 0, even for the
Bernoulli(1/n) diagonal indicators); by Cramer-Wold the standardized 4-vector -> N(0, I_4)
(corr(T_Dm,T_Da) = -1/(n-1) -> 0 for even n). Hence E_low / ((n^4-1)/144) -> chi^2_2, i.e.
E_low/E[E_low] -> Exp(1). For E_full the number of statistics grows with n; the Gaussian mixture is
stated as an approximation only (KS distance to MC: 0.20 -> 0.04 for n=3..8).

## 2. Exhaustive n=3 (exhaustive_n3.py; all 9! = 362,880 arrangements; 10 s)

| energy | mean | var | std | mode (count) | max | zeros | local minima (global + non-global) |
|---|---|---|---|---|---|---|---|
| E_low (paper def.) | 40/27 = 1.4815 | 1532/2187 = 0.7005 | 0.8370 | 90/81 = 1.111 (5216) | 360/81 = 4.444 | 8 | 344 = 8 + 336 |
| E_full symmetric | 40/27 = 1.4815 | 398/2187 = 0.1820 | 0.4266 | 138/81 = 1.704 (8736) | 180/81 = 2.222 | 8 | 16 = 8 + 8 (all 8 at E = 2/81) |
| E_v4 (see below) | 40/9 = 4.444 | 6.3045 | 2.5109 | 230/81 = 2.840 (2096); 200-bin histogram peak 3.1154 | 980/81 = 12.099 | 8 | 192 = 8 + 184 |
| E_asym (v4 code's "E_full") | 10/9 = 1.111 | 0.1463 | 0.3825 | 94/81 (6076) | 180/81 | 8 | 24 = 8 + 16 |

E_low and E_full take 346 and 177 distinct values (all multiples of 1/81). For n=3 the 8 zeros of
E_low are exactly the 8 magic squares.

### The v4 discrepancy, resolved exactly
The v4 Table 3 values for n=3 (mean 4.44, std 2.51, mode 3.12, max 12.10) are reproduced *exactly*
by the energy computed in `Analysis/src/analysis.py::compute_total_energy_vectorized` /
`compute_total_magic_energy` (also used by `analyze_exhaustive_n3` and `sample_energy_landscape`):

    E_v4 = Cov(X,Z)^2 + Cov(Y,Z)^2 + (mean(main diag) - mu)^2 + (mean(anti diag) - mu)^2,   mu = (N+1)/2.

Since Cov(D,Z) = (1/N) sum_{c in D} z_c = (n/N)(mean diag - mu) = (mean diag - mu)/n, the code's
diagonal terms are n^2 times the paper's Cov(D,Z)^2 terms: E_v4 = E_xy + n^2 E_diag.
Check: E[E_v4] = 10/9 + 9*(2*5/27) = 40/9 = 4.444 (n=3); 289/24 = 12.042 (n=4; v4: 12.04); 26 (n=5; v4: 26.00).
Mean 40/9, std 2.5109, max 980/81 = 12.0988 all match; "mode 3.12" is the centre of the highest bin
of a 200-bin histogram (3.1154), not a mode (true mode of E_v4: 230/81 = 2.84).
The paper's own definition gives mean 40/27 = 1.4815, std 0.837, mode 10/9, max 40/9 = 4.444.

The "24 local minima under E_full" come from `compute_full_magic_energy`, which drops row n-1 and
column n-1 (E_asym, not D4-invariant); the symmetric E_full has 16 local minima (8 magic + 8 at
E_full = 2/81). The "344 local minima under E_low" is correct for the paper's E_low.

## 3. Monte Carlo (mc.py; 10^8 samples per order, 16 processes, 255 s total)

| n | energy | exact mean | MC mean | exact std | MC std | Gauss-limit std | rel.err mean | rel.err var | KS vs Gauss limit |
|---|---|---|---|---|---|---|---|---|---|
| 3 | E_low | 1.4815 | 1.4814 | 0.8370 | 0.8369 | 1.171 | 6e-5 | 3e-5 | 0.103 |
| 3 | E_full | 1.4815 | 1.4815 | 0.4266 | 0.4266 | 0.869 | 8e-6 | 2e-4 | 0.200 |
| 4 | E_low | 4.0729 | 4.0736 | 3.1284 | 3.1288 | 3.586 | 2e-4 | 3e-4 | 0.037 |
| 4 | E_full | 2.6562 | 2.6564 | 0.9074 | 0.9073 | 1.349 | 7e-5 | 2e-4 | 0.107 |
| 5 | E_low | 9.3600 | 9.3605 | 8.0483 | 8.0482 | 8.694 | 6e-5 | 4e-5 | 0.019 |
| 5 | E_full | 4.1600 | 4.1600 | 1.3966 | 1.3966 | 1.867 | 9e-6 | 7e-5 | 0.078 |
| 6 | E_low | 18.843 | 18.843 | 17.122 | 17.122 | 18.007 | 4e-5 | 8e-5 | 0.012 |
| 6 | E_full | 5.9954 | 5.9957 | 1.9671 | 1.9671 | 2.459 | 6e-5 | 1e-5 | 0.061 |
| 7 | E_low | 34.354 | 34.349 | 32.174 | 32.167 | 33.349 | 1e-4 | 5e-4 | 0.008 |
| 7 | E_full | 8.1633 | 8.1631 | 2.5697 | 2.5698 | 3.089 | 2e-5 | 1e-4 | 0.050 |
| 8 | E_low | 58.060 | 58.058 | 55.377 | 55.381 | 56.888 | 3e-5 | 2e-4 | 0.007 |
| 8 | E_full | 10.664 | 10.664 | 3.2352 | 3.2353 | 3.777 | 3e-5 | 3e-5 | 0.042 |

All MC means are within |z| <= 2.3 standard errors of the exact values; all relative errors <= 5e-4.
Zeros of E_low found in 10^8 samples: n=4: 61 (low-mode-balanced class ~ 6e-7 of 16!), n=5: 5, n=6: 1;
zeros of E_full: none for n >= 4 (expected 0.03 for n=4).

## 4. Search experiment on symmetric E_full (algorithms.py; 394 s)

| n | greedy success (2e5 runs) | mean swaps | stuck in non-magic local min | SA success (400 runs, 2e4 N proposals) | median proposals (successes) |
|---|---|---|---|---|---|
| 4 | 0.195 +- 0.001 | 8.1 | 80.5% | 1.000 | 1.5e5 |
| 5 | 0.0115 +- 0.0002 | 11.2 | 98.9% | 0.78 +- 0.02 | 4.2e5 |
| 6 | 0.0079 +- 0.0002 | 14.1 | 99.2% | 0.50 +- 0.03 | 6.6e5 |

Stuck descents end with N^2 E_full as small as 1 (n=5,6) or 2 (n=4): a single diagonal off by one.
SA failures also end at N^2 E_full in {1, 2}.

## 5. Figure
`fig_random_energy.pdf` (6.5 x 2.35 in, fonts 7-8 pt, vector): (a) E_low/E[E_low] for n=3 (exact), 5, 8 (MC)
with Gaussian-limit mixture densities (Imhof inversion, density.py) and the Exp(1) limit; (b) same for
E_full; (c) exact mean/std vs n (log-log, n=3..40) with MC markers. No landscape entropy anywhere.

## 6. Runtimes (16 cores)
exhaustive n=3: 10 s; variance fits (exact rationals, n=3..45): 78 s; MC (6 x 10^8 samples): 255 s;
algorithms: 394 s; figure (Imhof densities): ~90 s; assemble: 14 s. Total ~14 min.

## Files
theory.py (closed forms, Gram/covariance matrices, generic exact 2nd moment), fit_variance.py (fast
exact Var + rational interpolation -> variance_fits.json), energies.py (vectorized energies),
exhaustive_n3.py, mc.py (-> mc_results.json, mc_hist.npz), density.py (Imhof pdf/cdf),
algorithms.py (-> algo_results.json), make_figure.py, assemble.py (-> results.json), fragment.tex, refs.bib.
