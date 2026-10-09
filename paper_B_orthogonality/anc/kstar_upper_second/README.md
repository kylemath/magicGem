# Second implementation of the k*(n) upper bounds (14 <= n <= 100)

Written independently of `../kstar_verify.py`: exact LLL (`lattice.py`) and enumeration with the column-feasibility
tests F1, F2 (`exact_kmax.py`), driven by `upper_scan.py` (`python3 upper_scan.py 14 100`, multi-core, many hours).
`upper_bounds_14_100.json` holds its results; `python3 compare.py` checks that they agree with `kstar_verify.json`
for every n (they do). Neither implementation produces a certificate for n > 40.
