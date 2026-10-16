#!/bin/bash
# Reproduces every number and figure of the paper from this directory (about 4 minutes, excluding the optional long runs).
set -e
cd "$(dirname "$0")"
python3 verify_numbers.py > verify_numbers.log      # exact re-verification of the quoted numbers
python3 n3_lowmode_proof.py > n3_lowmode_proof.log  # n=3: E_4=0 iff magic (Proposition 5.1), each proof step against all 9! arrangements
python3 balance_check.py  > balance_check.log       # functionals of Remark 2.6 (nonlinear examples supplementary) -> balance_results.json
python3 variance_proof.py > variance_proof.log      # symbolic proof of the variance formulas (~2 min)
python3 make_figures.py                              # figures -> ../figures/ (fig_kstar needs kstar_verify.json)
# exact count of the class L_4 (Proposition 5.3; 16 threads, ~10 s)
cc -O3 -march=native -o lowmode_enum lowmode_enum.c -lpthread
./lowmode_enum 3 L - 16 ; ./lowmode_enum 4 L - 16
python3 gaussian_estimate.py                         # Gaussian local-limit estimates
python3 search_reduced.py                            # reduced-scale local-search experiment (~30 s)
python3 kstar_enum_independent.py --certificate > kstar_enum_independent.log   # second enumeration + certificate (~1 min)
python3 kstar_check_certificates.py                  # check the certificate (<1 s)
python3 kstar_subset_sums.py > kstar_subset_sums.log # Proposition 3.14 checks and the subset-sum lower bounds (~10 s)
python3 kstar_beyond40.py > kstar_beyond40.log       # check the witnesses for 41 <= n <= 46 (Conjecture 3.15; <1 s)
# Optional long runs (the archived outputs are provided):
#   python3 kstar_verify.py 100 > kstar_verify.log   # permutation threshold: witnesses, lattice enumeration (a few hours)
#   cc -O3 -o anneal2 anneal2.c -lm; python3 kstar_beyond40.py search 41 42 43 44 45 46   # witness search beyond n = 40 (up to about an hour per n)
#   python3 twin_squares.py                          # independent check of the squares with complementary rows
#   python3 lowmode_recount.py ROW4; python3 lowmode_recount.py L; python3 lowmode_recount.py XY   # recount of L_4 (~6 min)
#   python3 table4_recount.py                        # recount of Table 4, cell (1,1) (~17 min)
#   python3 algorithms.py                            # full local-search experiment (steepest descent / annealing)
#   python3 mc.py                                    # 10^8-sample Monte Carlo of the random energies (hours)
#   cc -O3 -o lowmode_mc lowmode_mc.c ; ./lowmode_mc 4 125000000 SEED   # Monte Carlo frequency of L_n
#   python3 fit_variance.py                          # exact variances for n<=45 by direct summation (variance_fits.json)
