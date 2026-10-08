# Chirality and energy-vs-shape explorations (order-4 gems)

All scripts here; run from this directory (`python3 <script>`): `chi_sigma.py`, `chi_overlap.py` + `chi_analyze.py`,
`swaps.py`, `n3_random4.py`, `inertia_control.py`; shared helper `common.py`. Results: `results_*.json`; plots `fig_*.png`.
Volumes are in the paper's units (doubled-lattice integer volume/48, cross-checked: my fast volume and vertex counts equal the
paper's exact values for all 880 gems, asserted in `n3_random4.py`).

## Setup facts used (from Paper A data, re-read not recomputed)
- The 880 squares are D4-classes, and D4 includes transposition, i.e. a mirror of the gem in the plane. So a "gem" is defined up to
  a mirror anyway; shape invariants below are unaffected.
- The complement S -> 17-S is the reflection z -> -z. Self-complementary = the 352 gems = 304 (group C2, proper half-turn) + 48 (Ci, associative).
- No gem among the 880 has an improper symmetry except the inversion of the 48 Ci gems. Hence the 832 others are geometrically chiral
  (no reflection, rotoreflection or inversion maps them to themselves).

## Task 4. Chirality / asymmetry measures

### 4a. Minkowski measure (exact) sigma(P) = vol((P-P)/2)/vol(P)  [chi_sigma.py -> results_sigma.json, fig_sigma.png]
VERIFIED (exact rational arithmetic, hull of all 256 pairwise differences):
- sigma = 1 exactly for the 48 associative (Ci) gems and for no others; sigma > 1 for all 832 others (asserted). Min over non-Ci = 1.0383, max = 1.6477 (= 145/88, gem 218); all exact rationals are in the JSON.
- Distribution (all 880): quantiles 0/5/25/50/75/95/100% = 1 / 1 / 1.106 / 1.158 / 1.228 / 1.420 / 1.648.
- Mean sigma: Ci 1.000, half-turn C2 (304) 1.2125, trivial C1 (528) 1.1762 (medians 1.176 vs 1.153); Mann-Whitney C2 vs C1 p = 1.9e-6, i.e. half-turn gems are *more* asymmetric by this measure.
- Correlations (non-Ci, Spearman): with volume -0.667 (small gems are more asymmetric), with vertex count +0.150 (weak).
- Most asymmetric (index: sigma): 218: 1.648, 219: 1.639, 252: 1.633, 43: 1.621, 12: 1.618 (squares listed in JSON `top10_most_asymmetric`; 8 of top 10 are C2). Least asymmetric non-Ci: sigma 1.038 upward.
- Complement invariance: sigma is the same for S and 17-S (asserted exactly for all 880 on the reflected point set; trivially true, sigma is
  an isometry invariant including reflections).
CAVEAT (plainly): sigma measures *failure of central symmetry*, not chirality. A gem with a mirror plane but no centre also has sigma>1. It is
exact and a clean characterisation of the 48 associative gems ("sigma = 1 iff associative", empirically for n=4 only; the direction
associative => sigma=1 is trivial since S -> 17-S composed with a half-turn is the inversion).

### 4b. Overlap chirality chi(P) = 1 - max_{R in SO(3), t} vol(P ∩ (R·M P + t))/vol(P), M = z-reflection  [chi_overlap.py, chi_analyze.py]
NUMERICAL (qhull halfspace intersection; Nelder-Mead from the 24 octahedral starts, top 3 refined). The optimum is a lower
bound on overlap, so chi_hat is an upper bound on chi. NOT exact.
- Ci gems (48): chi = 0 to 7e-16 (consistent with achirality). Others: chi in [0.036, 0.207]; median 0.097; quartiles 0.082/0.114.
  Half-turn C2: median 0.104; trivial C1: median 0.092 (p = 2.5e-9). Most chiral: indices 15 (0.207), 17 (0.204), 237 and 239 (0.203), 51 (0.201). Least chiral non-Ci: 191 (0.0357), 399, 386.
- chi vs sigma: Spearman 0.655 (non-Ci), 0.708 (all). chi vs volume -0.557; vs vertex count 0.003.
- Complement invariance chi(S) = chi(17-S): median |difference| 1.0e-10, 99.5% (875/880 gems) agree to 1e-3, max difference 0.028
  (optimiser stuck in a local optimum for a few gems, so chi_hat is not guaranteed minimal there). Invariance is structural (conjugate the optimiser: if g aligns P with M P' then g^-1 aligns P' with M P),
  the numerics confirm it up to optimiser failures.
- Note: chi is the same measure for both members of a mirror pair by construction (mirror image of P is the gem of 17-S up to a proper motion);
  chi cannot distinguish "left" from "right" gem. A handedness label would need e.g. sign of a pseudo-scalar such as the triple product of
  inertia axes with z-asymmetry; not attempted.

## Task 6. Energy and gem shape

### 6a. Single swaps of magic squares (100 random magic squares x 120 swaps = 12,000)  [swaps.py -> results_swaps.json, fig_swaps.png]
VERIFIED: N^2 dE = d^2 m for every swap (m = number of the 10 lines containing exactly one of the two cells), asserted on all 12,000 (u=0 for magic squares).
Volume change dV (new hull volume - old):
- 61.1% of swaps decrease volume, 32.7% increase, 6.2% unchanged. Mean dV = -1.72 (sd 4.26) on a base volume ~84.
- dV vs d^2 m: Spearman -0.39 (Pearson -0.48). Spearman |dV| vs d^2 m: +0.55.
- The link is mostly mediated by |d| (size of the swapped values): Spearman(dV, |d|) = -0.38; mean dV by |d|: -0.02 (|d|=1), -0.79 (4), -3.0 (8), -6.7 (12), -8.0 (15). Holding |d| fixed the dV-d^2m correlation drops to between 0 and -0.17 for |d| <= 9 (and -0.26/-0.42 at |d| = 10, 12, where m and extremal values coincide).
  Holding m fixed the correlation with dE is -0.34..-0.46, but that is the same |d| effect.
- No dependence on cell positions in the sign sense: Spearman(dV, d*(r_b^2 - r_a^2)) = 0.006. OLS dV ~ d^2 m, |d|, d*radial gain gives R^2 = 0.23 (coefficient on |d| dominates). Vertex-count change is unrelated to dE (Spearman -0.06; mean change -0.002).
- Reading: moving the squares away from magic mostly shrinks volume, because magic squares are tilt-free (see 6c); but the effect size is driven by how far values move,
  not by the energy increment per se.

### 6b. n=3 exhaustive (all 9! = 362,880)  [n3_random4.py -> results_n3_random4.json]
- 8 magic squares (all volume 18, the near-top: 99.4th percentile; 99% quantile of all arrangements is 17.67). 8 arrangements are flat (volume 0); none is magic.
- Spearman(volume, E_full) = -0.578 (Pearson -0.596); Spearman(volume, E_low) = -0.817; vertex count vs E_full -0.011.
- Mean volume by E_full decile (low to high): 16.0, 14.9, 14.2, 13.8, 13.4, 13.1, 12.8, 12.4, 11.8, 11.0 (monotone).

### 6c. Random order-4 permutations (1e5) vs the 880 magic gems
- Random: volume mean 75.7, sd 7.6, quartiles 71.2/76.5/81.0. Magic 880: mean 84.05, sd 7.14, quartiles 80.3/85.2/89.0. The median magic gem sits at the 91st percentile of random volume (range 2nd to 99.999th); 16% of magic gems are below the random median.
- Vertex count: random mean 12.06 (mode 12), magic 12.23 (mode 12); distributions nearly equal (magic slightly fatter at 16 vertices: 2% vs 0.17%, and at 8: 0.8% vs 0.2%).
- Correlation with random-perm volume: Spearman vs E_full -0.455, vs E_low -0.671; vertex count vs E_full +0.014. Mean volume by E_full decile: 81.2 (lowest) falling to 68.9.
- REAL EXPLANATION, EXACT (inertia_control.py; identity asserted numerically on 2000 arrangements): on the grid X,Y are uncorrelated with equal variance, so
  det Cov(X,Y,Z) = VX VY VZ - VY Cov(X,Z)^2 - VX Cov(Y,Z)^2 = const - V_X * E_xy,
  where E_xy = Cov(X,Z)^2 + Cov(Y,Z)^2 is the first-order part of E_low and VZ is constant for permutations. So the determinant of the covariance (the volume of the
  inertia ellipsoid) is maximal exactly when the height function is orthogonal to x and y, i.e. for every magic square (all 880 have the same det Cov, asserted).
  Hull volume vs det Cov in random perms: Spearman +0.659 (vs E_xy -0.659; vs the diagonal part of the energy +0.03).
- Control: among random perms with Cov(X,Z)=Cov(Y,Z)=0 (3,897 found in 1.2e7), mean volume is 81.5 (sd 5.5); magic gems (84.05) sit at the 74th percentile (median) of that control. So about 2/3 of the "magic gems are voluminous" excess
  (75.7 -> 81.5 of the 8.3 gap) is the tilt-freeness already contained in E_xy=0; the remaining +2.5 (about 0.45 sd) is real but modest, attributable to the row/column/diagonal
  balance (within the tilt-free control, Spearman(volume, E_full) = -0.22). The control with E_low = 0 had only 6 samples: inconclusive.
- Swaps: Spearman(dV, d det Cov) = 0.41 (Pearson 0.59), 12,000 swaps; so tilt explains part of the swap effect too.

## Recommendation
- Paper A (chirality): include the exact sigma statement (sigma = 1 iff associative, for the 880: 48 gems; ranking of asymmetric gems) as a short remark, with the caveat that it measures central symmetry. The overlap chi is numerical and optimiser-limited; if included, flag it as numerical (a figure or one sentence: "832 of 880 gems are chiral, chi in [0.036, 0.207]"). The structural statement that only the 48 associative gems have an improper symmetry is already exact in the symmetry data and is the cleaner chirality claim.
- Paper B (energy-volume link): the covariance-determinant identity det Cov = const - V_X E_xy is exact, one line, and explains why low energy goes with large gem "volume" (mean-field/inertia sense). Hull volume itself is only correlated (Spearman -0.45 vs E_full at n=4, -0.58 at n=3; -0.67/-0.82 vs E_low); mention as an empirical remark at most. 
- Omit: swap-volume results (the dV~d^2 m relation is mediated by |d| and tilt, no clean law found), vertex-count relationships (null), C2-vs-C1 shape differences.
- Speculative / not supported: any claim that magic gems are "round" (not tested: only volume and vertex count); the C2-more-chiral difference is statistically significant but small and not interpreted.
