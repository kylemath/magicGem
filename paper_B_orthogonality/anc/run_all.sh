#!/bin/bash
# Reproduces every number and figure of the paper from this directory (about 2 minutes, excluding the optional long runs).
set -e
cd "$(dirname "$0")"
python3 verify_numbers.py > verify_numbers.log      # exact re-verification of the quoted numbers
python3 balance_check.py  > balance_check.log       # Section 4 numbers -> balance_results.json
python3 make_figures.py                              # figures -> ../figures/
# exact count of the low-mode class (Proposition on |L_4|; 16 threads, ~10 s)
cc -O3 -march=native -o lowmode_enum lowmode_enum.c -lpthread
./lowmode_enum 3 L - 16 ; ./lowmode_enum 4 L - 16
python3 gaussian_estimate.py                         # Gaussian local-limit estimates
python3 search_reduced.py                            # reduced-scale local-search experiment (~30 s)
# Optional long runs (the archived outputs are provided):
#   python3 algorithms.py                            # full local-search experiment (Table of Section 6.2)
#   python3 mc.py                                    # 10^8-sample Monte Carlo of the random energies (hours)
#   cc -O3 -o lowmode_mc lowmode_mc.c ; ./lowmode_mc 4 125000000 SEED   # Monte Carlo frequency of L_n
#   python3 fit_variance.py                          # exact variance polynomials (variance_fits.json)
