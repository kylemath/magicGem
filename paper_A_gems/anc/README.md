# Ancillary files for "Magic Gems: A Polyhedral Framework for Magic Squares"

Python 3.9, NumPy, SciPy, NetworkX, matplotlib. Run every command from inside this directory.
Squares are numbered 0..879 in the order of `squares880.txt` (one square per line, row by row);
`all7040_dudeney.csv` lists the 7040 order-4 squares with Dudeney's group (column `Gr.`).

| command | produces |
|---|---|
| `python3 run_geometry_880.py` | exact hulls, f-vectors, volumes, types, congruence classes of the 880 gems -> `results_geometry.json`, `run_geometry_880.log` |
| `python3 symmetry_880.py` | exact isometry groups and facet orbits of the 880 gems -> `symmetry_880.json` (uses `isolib.py`) |
| `python3 symmetry_summary.py` | aggregated counts quoted in Section 4 -> `symmetry_summary.json` |
| `python3 siamese_proof.py` | symbolic verification of the Siamese theorem for all m >= 2 -> `results_siamese_proof.json` |
| `python3 verify_numbers.py` | re-derives the other numbers in the paper (Table 2, Dudeney cross-tabulation, named squares, Siamese f-vectors n=3..21) -> `verify_numbers.json` |
| `python3 solid_centroid.py` | number of gems whose solid centroid is not the origin (829) |
| `python3 make_fig_vectors.py` (Fig. 1, `fig_vectors.pdf`: heat map, vectors, hull), `make_fig_lines.py` (Fig. 2, `fig_lines.pdf`), `make_fig_moments.py` (Fig. 4, `fig_moments.pdf`: piles of checkers, heights, lever, mixed moment; checks pile counts (34 per row and column), centre of mass of the checkers, sum z x y = 0 and 60), `make_fig_weighted_sum.py` (Fig. 5, `fig_weighted_sum.pdf`: closed chain of the moment arms z(x,y); asserts sum z x = sum z y = 0, quadrant totals 0 and 60), `make_fig_pointsets.py` (Fig. 7, `fig_pointsets.pdf`: point sets with antipodal / half-turn pairings; asserts the pairings), `make_fig_construction_d4.py`, `make_fig_symmetry.py`, `make_fig_geometry_880.py`, `make_fig_siamese_layers.py` | the figures (PDF, written to `../figures`) |

`gem_geometry.py` (exact hull, congruence), `isolib.py` (isometry groups), `siamese_util.py`, `gemfig.py`, `vecfig.py` are libraries.
