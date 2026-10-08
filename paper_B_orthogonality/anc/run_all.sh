#!/bin/bash
# Reproduces every number and figure of the paper from this directory (about 4 minutes, excluding the optional long runs).
set -e
cd "$(dirname "$0")"
python3 verify_numbers.py > verify_numbers.log      # exact re-verification of the quoted numbers
python3 n3_lowmode_proof.py > n3_lowmode_proof.log  # n=3: E_low=0 iff magic (Proposition 3.14), each proof step against all 9! arrangements
python3 balance_check.py  > balance_check.log       # balance numbers of Section 3.7 -> balance_results.json
python3 variance_proof.py > variance_proof.log      # symbolic proof of the variance formulas (~2 min)
python3 make_figures.py                              # figures -> ../figures/ (fig_kstar needs kstar_verify.json)
# exact count of the low-mode class (Proposition on |L_4|; 16 threads, ~10 s)
cc -O3 -march=native -o lowmode_enum lowmode_enum.c -lpthread
./lowmode_enum 3 L - 16 ; ./lowmode_enum 4 L - 16
python3 gaussian_estimate.py                         # Gaussian local-limit estimates
python3 search_reduced.py                            # reduced-scale local-search experiment (~30 s)
# Optional long runs (the archived outputs are provided):
#   python3 kstar_verify.py 100 > kstar_verify.log   # permutation threshold: witnesses, lattice enumeration (a few hours)
#   python3 twin_squares.py                          # independent check of the twin-row squares
#   python3 algorithms.py                            # full local-search experiment (steepest descent / annealing)
#   python3 mc.py                                    # 10^8-sample Monte Carlo of the random energies (hours)
#   cc -O3 -o lowmode_mc lowmode_mc.c ; ./lowmode_mc 4 125000000 SEED   # Monte Carlo frequency of L_n
#   python3 fit_variance.py                          # exact variances for n<=45 by direct summation (variance_fits.json)
