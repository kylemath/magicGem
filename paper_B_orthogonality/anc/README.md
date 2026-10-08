# Ancillary files for "Magic squares as orthogonality conditions on a height function"

Python 3.9+ with NumPy, SciPy, SymPy, Matplotlib; a C compiler for the enumerator.
`bash run_all.sh` regenerates the quick items below; every script is run from this directory.

| file | purpose | output / archived data |
|---|---|---|
| `verify_numbers.py` | exact integer/rational recheck: n=3 enumeration, exact means and variances (n=3..6) against the closed forms, swap formula on all 105,888 swaps of the 880+8 magic squares and Siamese squares, k*(n) witnesses, Loly invariant (n=3,4), product of inertia, |L_n| files | `verify_numbers.log`, `verify_numbers.json` |
| `balance_lib.py`, `balance_check.py` | balance functionals of Section 4 (linear, ring, 3D unit vector), bound check, comparison n=3, n=4 | `balance_results.json` |
| `make_figures.py`, `figstyle.py` | the four figures (writes `../figures/*.pdf`) | |
| `lowmode_enum.c` | meet-in-the-middle enumeration of the low-mode class (`./lowmode_enum 4 L - 16`; modes L, XY, DIAG, MAGIC, SEMI, ROWSL, COLSL) | `enum_n3.jsonl`, `enum_n4.jsonl` |
| `lowmode_mc.c` | Monte Carlo frequency of the low-mode class | `mc_n4.jsonl`, `mc_n5.jsonl`, `mc_n6.jsonl` |
| `gaussian_estimate.py` | Gaussian local-limit estimates of |L_n| | `gaussian_estimates.json` |
| `theory.py`, `energies.py`, `fit_variance.py`, `density.py`, `exhaustive_n3.py`, `mc.py` | exact moments of the random energies, variance polynomials, Imhof-type densities, Monte Carlo | `variance_fits.json`, `mc_results.json`, `mc_hist.npz`, `data_witnesses_variances.json` |
| `algorithms.py`, `search_reduced.py` | steepest descent and annealing on E_full (full and reduced scale) | `algo_results.json`, `search_reduced.json` |
| `magic4_all7040.txt` | all 7,040 magic squares of order 4 (one per line, row-major) | |
