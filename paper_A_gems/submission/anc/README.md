# Ancillary files for "Magic Gems: Convex Hulls of Lifted Magic Squares"

Python 3.9, NumPy 2.0, SciPy 1.13, SymPy 1.13, NetworkX 3.2, matplotlib. Run every command from inside this directory.
Squares are numbered #0..#879 in the lexicographic order of their Frenicle standard forms, one square per line (row by row)
in `squares880.txt`; `all7040_dudeney.tsv` (tab-separated; the same table as comma-separated values in `all7040_dudeney.csv`) lists the 7040 order-4 squares with the Dudeney group labels used
in the paper (column `Gr.`) and the paper's 0-based class number # (column `paper_no`).
`sa_n5_V10.txt` lists, one square per line (row by row), the 15 D4-classes of order-5 magic squares found by the annealer
(Appendix B) whose gems have 10 vertices (Remark 6.6); 14 have f-vector (10,22,14) and one (10,23,15).

## Exact computations (all statements asserted; times on a laptop)

| command | produces | time |
|---|---|---|
| `python3 verify_structure.py` | the structural statements: coplanar arrangements (Prop. 2.3; exhaustive for n = 2, 3), covariance diag(a,a,b) (Lemma 3.1), isometry groups of point sets and vertex sets (Props 4.2, 4.3), D4-injectivity of vertex sets (Remark 5.5), the 616 distinct squared-distance multisets and the 616 congruence classes (Prop. 5.4), parity (Lemma 4.4: V, V_int, V_bd even for all 352 self-complementary squares, E and F even for the 48 associative ones; Remark 4.5: odd F for 18 of the 304 half-turn gems), hull certification in exact integer arithmetic (pairwise distinct facet planes, every point satisfies every facet inequality, each facet 2-dimensional and equal to the exact 2D hull of the points on its plane, every facet edge in exactly two facets, strict convexity at every edge), regular subdivisions and vertical facets (Prop. 5.2), types as unions of complement orbits, Siamese vertices = forced vertices for n = 3..41 (a cross-check of Thm 6.4), interior / boundary counts (Table 3), mixed moments (Appendix C) -> `verify_structure.json`, `verify_structure.log` | 20 s |
| `python3 siamese_slacks.py` | the slack polynomials of Table 5 (proof of Thm 6.4) at the points q1..q16 (written to `siamese_slacks.tex`, which the paper includes), positivity for all m >= 2, closure of the facet list, distinct facet planes, each facet the strictly convex polygon of its incident points, strict convexity across all 26 edges, isometry group {id, -id} of the Siamese gem for all m >= 2 -> `siamese_slacks.log` | 3 s |
| `python3 linear_squares.py 5 7 9 11` | vertex counts of all linear magic squares of orders 5..11 (Remark 6.6) and, as a cross-check of Prop. 6.5, the f-vector (12,24,14) of the digit-exchanged square s' (Corollary 6.2) for n = 5..31 -> `results_linear_squares.json`, `linear_squares.log` | 8 min |
| `python3 digit_exchanged_slacks.py` | proof data for Prop. 6.5 (digit-exchanged square s'): the slack polynomials of Table 6 (written to `digit_exchanged_slacks.tex`, which the paper includes), positivity for all m >= 2, closure of the 14 facets, distinct planes, strictly convex facets and edges, the turns of the quadrilaterals, isometry group {id, -id}; the same generic certificate re-applied to the Siamese square; numerical checks of the level sets, entries and forced vertices for n = 5..61 -> `digit_exchanged_slacks.log` | 5 s |
| `python3 linear_magic_count.py` | the magic criterion and the count of linear magic squares (Prop. 6.1), checked against the actual line sums of all n^6 parameter choices for n = 3..25, and against `results_linear_squares.json` -> `linear_magic_count.log` | 6 min |
| `python3 linear_census.py 5 7 9 11 13 15 17 19 21` | vertex counts of all linear magic squares of odd orders 5..21 up to D4 (Remark 6.6): one parameter tuple per D4-class (D4 acts on the parameters), class counts compared with the formula of Prop. 6.1, vertex counts by Quickhull, and every class with at most 13 vertices or with the largest count certified with the exact hull; asserts that for n >= 7 the only 12-vertex classes are the Siamese and the digit-exchanged square -> `results_linear_census.json`, `linear_census.log` | 25 min on 4 cores |
| `python3 linear_fixed_steps.py` | Section 6.4: Rubin's triangle (Lemma 6.8, k <= 15), the squares of Prop. 6.9 at n = 7, 29, 173 and of Cor. 6.10 at every prime 7 <= n < 120 (exact hulls), and the periodicity examples after Prop. 6.7 (exact hulls of all n^2 points) -> `linear_fixed_steps.log` | 2 min |
| `python3 vertex_determination.py` | Remark 5.5: rank of the line equations on the non-vertex cells (871 of 880 classes full rank), all magic completions of the vertex data of the other 9, and their different vertex sets -> `vertex_determination.log` | 3 s |
| `python3 run_geometry_880.py` | exact hulls, f-vectors, volumes, combinatorial types, congruence classes of the 880 gems -> `results_geometry.json`, `run_geometry_880.log` | 5 s |
| `python3 symmetry_880.py`, `python3 symmetry_summary.py` | isometry groups and facet orbits of the 880 gems -> `symmetry_880.json`, `symmetry_880.log`, `symmetry_summary.json` (uses `isolib.py`) | 1 s |
| `python3 siamese_proof.py` | the earlier symbolic verification of the Siamese theorem (facet planes derived from the hull) -> `results_siamese_proof.json`, `siamese_proof.log` | 1 s |
| `python3 box_and_classes.py` | box, forced vertices, interior / boundary counts, volume fractions, pandiagonal / associative / Dudeney classes -> `results_box_classes.json`, `box_and_classes.log` | 1 s |
| `python3 difference_body_ratio.py` | exact difference-body ratio sigma (Appendix C) -> `results_sigma.json`, `difference_body_ratio.log` | 1 s |
| `python3 ehrhart_880.py` | Ehrhart polynomials and h*-vectors of the lattice translates G + (1/2,1/2,1/2) of the 880 gems, and of the Lo Shu (Appendix B) -> `results_ehrhart.json`, `ehrhart_880.log` | 5 s |
| `python3 verify_numbers.py` | further numbers (Dudeney cross-tabulation of Appendix C, named squares) -> `verify_numbers.json`, `verify_numbers.log` | 1 s |
| `python3 solid_centroid.py` | the 829 order-four gems whose solid centre of mass is not the origin (Appendix C; prints the count) | 5 s |
| `python3 independent_hull_check.py` | an independent exact recomputation of the hulls without Quickhull (all supporting planes through triples of points, exact 2D hulls of the facets): vertex sets, f-vectors, volumes and interior / boundary counts of the 880 gems, Duerer, the Siamese squares n = 3..21, the 15 squares of `sa_n5_V10.txt` and the two order-5 squares of Remark 6.6, compared with the stored results -> `independent_hull_check.log` | 12 s |

## Which invariants see the line conditions (Section 5.3, Table 4; Monte Carlo estimates except the exact n = 4 magic column)

`python3 magic_vs_random.py 100000 20000` compares, at n = 4, the 880 magic squares (exact) with 10^5 uniformly random arrangements, 10^5 uniform arrangements with vanishing first moments (rejection sampling), 10^5 uniformly random semi-magic squares (the 549,504 semi-magic squares of order 4 are the 954 listed orbits times the 576 row and column permutations; `semimagic4_count.c` counts them independently by depth-first search), and annealed semi-magic squares (a check of the annealer); and at n = 5 annealed magic squares, random arrangements, arrangements with vanishing first moments and annealed semi-magic squares (2 x 10^4 each). Invariants: V, V_int, V_bd, numbers of lower / upper / vertical facets, volume, |Iso|, solid centroid, solid covariance; effect sizes (difference, SE, z, Cohen's d). It compiles `sa_magic.c` itself. -> `magic_vs_random.json`, `magic_vs_random.log` (about 20 min on 4 cores). `python3 magic_vs_random_table.py` writes Table 4 (`magic_vs_random.tex`, included by the paper) and prints the other numbers of Section 5.3 (upper and vertical facets, tilt, the exact vertex means of the magic squares by symmetry type from `symmetry_880.json`, the order-five numbers, and the 16 order-five gems with three vertical facets) to `magic_vs_random_table.log`.

## Sampling (Appendix B, Table 7, and Section 7, question 2; Monte Carlo estimates, not results)

`python3 vertex_statistics.py random` / `magic <dir> 4 5 6 7 8` / `sa4 <dir>` / `table` / `volume`: numerical vertex-count
statistics; `<dir>` holds the output of `run_sa.sh`, which runs the annealer `sa_magic.c` (an optional 8th argument 1 restricts it to rows and columns, i.e. semi-magic squares; the default, used for all magic samples, is unchanged; compile with
`cc -O2 sa_magic.c -o sa_magic -lm`; parameters n=4: `20000 200000 20 0.5`, n=5: `60000 400000 30 0.5`,
n=6: `24000 1000000 40 0.5`, n=7: `8000 1500000 60 0.5`, n=8: `2400 2500000 80 0.5` as total squares, steps, T0, T1)
-> `vertex_stats_random.json`, `vertex_stats_magic.json`, `vertex_stats_sa4.json` (with the logs `vertex_stats_random.log`, `vertex_stats_magic.log`, `vertex_stats_sa4.log`), `volume_stats.json`, `volume_stats.log`, and `vertex_stats_table.log` (the numbers of Table 7; counts are distinct D4-classes). Seeds: random arrangements
`7000 n + c` (`vertex_statistics.py`); annealer `1000 s + n`, s = 1..16 (`run_sa.sh`). The sampled squares themselves are
not included, except the 15 ten-vertex squares of order 5 in `sa_n5_V10.txt`.

## Figures (PDF, written to `../figures`)

`make_fig_vectors.py` (Fig. 1), `make_fig_lines.py` (Fig. 2), `make_fig_construction.py` (Fig. 3; panel (e) draws the regular subdivisions S(z), S(-z) of the Lo Shu and asserts the cells and vertical facets of Example 5.3),
`make_fig_moments.py` (Fig. 4: checkers on a checkerboard), `make_fig_weighted_sum.py`
(Fig. 5; asserts the closed chains and the mixed-moment totals 0 and 60), `make_fig_symmetry.py` and `make_fig_pointsets.py` (Fig. 6, top and bottom; asserts the
pairings), `make_fig_geometry_880.py` (Fig. 7), `make_fig_siamese_layers.py` (Fig. 8).

`gem_geometry.py` (exact hull with an integer-arithmetic certificate applied to every hull, congruence), `isolib.py` (isometry groups), `siamese_util.py`, `gemfig.py`, `vecfig.py` are
libraries. `siamese_slacks.tex`, `digit_exchanged_slacks.tex` and `magic_vs_random.tex` are generated by the scripts of the same names and included in the paper as Tables 5, 6 and 4.

`v4_sampling_recheck.py` re-runs the order-4 sampling of Table 3 of version 4 (6*10^7 uniform arrangements, seed 20261014, about one minute with NumPy) and counts the zeros of the four-term energy; output in `v4_sampling_recheck.log` (45 found, about 42 expected). It supports item (v) of "Changes from earlier versions".
