# Ancillary files for "Magic Gems: A Polyhedral Framework for Magic Squares"

Python 3.9, NumPy 2.0, SciPy 1.13, SymPy 1.13, NetworkX 3.2, matplotlib. Run every command from inside this directory.
Squares are numbered #0..#879 in the lexicographic order of their Frenicle standard forms, one square per line (row by row)
in `squares880.txt`; `all7040_dudeney.tsv` (tab-separated; the same table as comma-separated values in `all7040_dudeney.csv`) lists the 7040 order-4 squares with the Dudeney group labels used
in the paper (column `Gr.`) and the paper's 0-based class number # (column `paper_no`).
`sa_n5_V10.txt` lists, one square per line (row by row), the 15 D4-classes of order-5 magic squares found by the annealer
(Appendix B) whose gems have 10 vertices (Remark 6.3); 14 have f-vector (10,22,14) and one (10,23,15).

## Exact computations (all statements asserted; times on a laptop)

| command | produces | time |
|---|---|---|
| `python3 verify_structure.py` | the structural statements: coplanar arrangements (Prop. 2.3; exhaustive for n = 2, 3), covariance diag(a,a,b) (Lemma 3.2), isometry groups of point sets and vertex sets (Thms 4.2, 4.3), D4-injectivity of vertex sets, the 616 distinct squared-distance multisets and the 616 congruence classes (Prop. 5.4), parity (Lemma 4.4), hull certification (every point satisfies every facet inequality, every facet edge in exactly two facets), regular subdivisions and vertical facets (Prop. 5.2), types as unions of complement orbits, Siamese vertices = forced vertices for n = 3..41 (a cross-check of Thm 6.2), interior / boundary counts (Table 2), mixed moments (Section 3) -> `verify_structure.json`, `verify_structure.log` | 20 s |
| `python3 siamese_slacks.py` | the slack polynomials of Table 3 (proof of Thm 6.2) at the points q1..q16 (written to `siamese_slacks.tex`, which the paper includes), positivity for all m >= 2, closure of the facet list, isometry group {id, -id} of the Siamese gem for all m >= 2 -> `siamese_slacks.log` | 3 s |
| `python3 linear_squares.py 5 7 9 11` | vertex counts of all linear magic squares of orders 5..11 (Remark 6.3) and the digit-exchanged square s' (Lemma 6.1) for n = 5..31 -> `results_linear_squares.json`, `linear_squares.log` | 8 min |
| `python3 run_geometry_880.py` | exact hulls, f-vectors, volumes, combinatorial types, congruence classes of the 880 gems -> `results_geometry.json`, `run_geometry_880.log` | 5 s |
| `python3 symmetry_880.py`, `python3 symmetry_summary.py` | isometry groups and facet orbits of the 880 gems -> `symmetry_880.json`, `symmetry_880.log`, `symmetry_summary.json` (uses `isolib.py`) | 1 s |
| `python3 siamese_proof.py` | the earlier symbolic verification of the Siamese theorem (facet planes derived from the hull) -> `results_siamese_proof.json`, `siamese_proof.log` | 1 s |
| `python3 box_and_classes.py` | box, forced vertices, interior / boundary counts, volume fractions, pandiagonal / associative / Dudeney classes -> `results_box_classes.json`, `box_and_classes.log` | 1 s |
| `python3 difference_body_ratio.py` | exact difference-body ratio sigma (Remark 4.6) -> `results_sigma.json`, `difference_body_ratio.log` | 1 s |
| `python3 ehrhart_880.py` | Ehrhart polynomials and h*-vectors of the lattice translates G + (1/2,1/2,1/2) of the 880 gems, and of the Lo Shu (Appendix B) -> `results_ehrhart.json`, `ehrhart_880.log` | 5 s |
| `python3 verify_numbers.py` | further numbers (Dudeney cross-tabulation, named squares) -> `verify_numbers.json`, `verify_numbers.log` | 1 s |
| `python3 solid_centroid.py` | the 829 order-four gems whose solid centre of mass is not the origin (Section 3; prints the count) | 5 s |

## Sampling (Appendix B, Table 4, and Section 7, question 3; Monte Carlo estimates, not results)

`python3 vertex_statistics.py random` / `magic <dir> 4 5 6 7 8` / `sa4 <dir>` / `table` / `volume`: numerical vertex-count
statistics; `<dir>` holds the output of `run_sa.sh`, which runs the annealer `sa_magic.c` (compile with
`cc -O2 sa_magic.c -o sa_magic -lm`; parameters n=4: `20000 200000 20 0.5`, n=5: `60000 400000 30 0.5`,
n=6: `24000 1000000 40 0.5`, n=7: `8000 1500000 60 0.5`, n=8: `2400 2500000 80 0.5` as total squares, steps, T0, T1)
-> `vertex_stats_random.json`, `vertex_stats_magic.json`, `vertex_stats_sa4.json` (with the logs `vertex_stats_random.log`, `vertex_stats_magic.log`, `vertex_stats_sa4.log`), `volume_stats.json`, `volume_stats.log`, and `vertex_stats_table.log` (the numbers of Table 4; counts are distinct D4-classes). Seeds: random arrangements
`7000 n + c` (`vertex_statistics.py`); annealer `1000 s + n`, s = 1..16 (`run_sa.sh`). The sampled squares themselves are
not included, except the 15 ten-vertex squares of order 5 in `sa_n5_V10.txt`.

## Figures (PDF, written to `../figures`)

`make_fig_vectors.py` (Fig. 1), `make_fig_lines.py` (Fig. 2), `make_fig_construction.py` (Fig. 3; panel (e) draws the regular subdivisions S(z), S(-z) of the Lo Shu and asserts the cells and vertical facets of Example 5.3),
`make_fig_moments.py` (Fig. 4: checkers on a checkerboard), `make_fig_weighted_sum.py`
(Fig. 5; asserts the closed chains and the mixed-moment totals 0 and 60), `make_fig_symmetry.py` and `make_fig_pointsets.py` (Fig. 6, top and bottom; asserts the
pairings), `make_fig_geometry_880.py` (Fig. 7), `make_fig_siamese_layers.py` (Fig. 8).

`gem_geometry.py` (certified exact hull, congruence), `isolib.py` (isometry groups), `siamese_util.py`, `gemfig.py`, `vecfig.py` are
libraries. `siamese_slacks.tex` is generated by `siamese_slacks.py` and included in the paper as Table 3.
