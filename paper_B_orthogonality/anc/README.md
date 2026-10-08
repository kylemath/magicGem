# Ancillary files for "Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies"

Python 3.9+ with NumPy, SciPy, SymPy, Matplotlib (and mpmath, which ships with SymPy); a C compiler for the enumerator and the annealer.
`bash run_all.sh` regenerates the quick items below; every script is run from this directory.

| file | purpose | output / archived data |
|---|---|---|
| `kstar_verify.py` | permutation threshold k*(n) (Theorem 3.7): exact check of all witnesses (5 <= n <= 40), exact LLL + Fincke-Pohst enumeration of the lattices Lambda_{n,k} giving the upper bounds U(n) for 14 <= n <= 100, rank-2 check of level n-3 for 14 <= n <= 400, numerical range of Theorem 3.7(a). `python3 kstar_verify.py 100` (a few hours; `--resume LOG` reuses the U(n) of an earlier log) | `kstar_verify.json`, `kstar_verify.log` |
| `kstar_crosscheck/` | independent cross-checks of the k*(n) material: `wit.py` (witnesses), `rank2.py` (level n-3, 18 <= n <= 170), `thA.py` (range of Theorem 3.7(a)), `cons.py` (twin-row squares), `milp_ub.py` (upper bounds by floating-point MILP with HiGHS; reproduces 14 <= n <= 33) | |
| `kstar_witnesses.json` | witness arrangements for 14 <= n <= 40: all row sums M(n), column deviations gamma with (t-1)^{k*(n)} dividing P_gamma | |
| `data_witnesses_variances.json` | witness arrangements for 5 <= n <= 13 (gamma_j = (-1)^j C(n-1,j)) and the variance polynomials | |
| `constructions.py`, `twin_squares.py` | the semi-magic squares with twin rows of Lemma 3.12 (two independent implementations, each verified exactly) | |
| `realise.py`, `anneal2.c` | witness search: steepest descent over within-row swaps, and simulated annealing over arbitrary swaps (`cc -O3 -o anneal2 anneal2.c -lm`) | |
| `variance_proof.py` | symbolic proof of Theorems 4.3-4.4: Moebius inversion over set partitions, invariants of the energy matrices, checks against full permutation enumeration (N <= 7), explicit matrices (n <= 25) and all 9! arrangements for n = 3; asymptotics and Gaussian variance ratios | `variance_proof.log`, `variance_proof_results.json` |
| `verify_numbers.py` | exact integer/rational recheck: n=3 enumeration, exact means and variances (n=3..6), swap gaps of the 880+8 magic squares, Loly invariant (n=3,4), mixed moments of the 880 squares, k*(n) witnesses for n <= 13 | `verify_numbers.log`, `verify_numbers.json` |
| `n3_lowmode_proof.py` | Proposition 3.14 (n = 3: E_low = 0 iff magic): counts of all 9! arrangements (760 degree-1, 4224 both diagonals, 72 semi-magic, 8 with E_low = 0), symbolic check of the parametrisation and of the sum-of-squares identity used in the proof, and the integer solutions of 4k^2+3(P^2+Q^2)+T^2+U^2 = 30 (under 1 s) | `n3_lowmode_proof.log` |
| `balance_lib.py`, `balance_check.py` | balance functionals of Section 3.7 (linear, ring, 3D unit vector) for n=3 and n=4 | `balance_results.json` |
| `make_figures.py`, `figstyle.py` | the four figures (writes `../figures/*.pdf`; `fig_kstar` reads `kstar_verify.json`) | |
| `lowmode_enum.c` | meet-in-the-middle enumeration of the low-order class (`./lowmode_enum 4 L - 16`; modes L, XY, DIAG, MAGIC, SEMI, ROWSL, COLSL) | `enum_n3.jsonl`, `enum_n4.jsonl` |
| `lowmode_mc.c` | Monte Carlo frequency of the low-order class | `mc_n4.jsonl`, `mc_n5.jsonl`, `mc_n6.jsonl` |
| `gaussian_estimate.py` | Gaussian local-limit estimates of the size of L_n | `gaussian_estimates.json` |
| `theory.py`, `energies.py`, `density.py`, `exhaustive_n3.py`, `mc.py` | exact means, Gaussian-approximation densities, 10^8-sample Monte Carlo of the random energies (sanity check of the exact moments) | `mc_results.json`, `mc_hist.npz` |
| `fit_variance.py` | exact variances for n <= 45 by direct summation over equality patterns, and their rational interpolation (superseded by `variance_proof.py`, which agrees) | `variance_fits.json` |
| `algorithms.py`, `search_reduced.py` | steepest swap descent and simulated annealing on E_full for n = 4, 5, 6 (full scale: 2x10^5 descents and 400 annealing runs per order; reduced scale: 2x10^4 and 64) | `algo_results.json`, `search_reduced.json` |
| `magic4_all7040.txt` | all 7,040 magic squares of order 4 (one per line, row-major) | |

Local search (Section 5.2): steepest descent reaches a magic square from 19.5%, 1.2%, 0.8% of random starts for n = 4, 5, 6; simulated annealing (geometric cooling over 2x10^4 N proposals) succeeds in 100%, 78%, 50% of runs. The reduced-scale rerun gives 0.193, 0.011, 0.008 and 1.00, 0.81, 0.45.
