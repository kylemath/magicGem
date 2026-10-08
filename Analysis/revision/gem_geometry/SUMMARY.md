# Gem geometry of the 880 order-4 squares, swap-gap verification, Siamese gems

Subagent D of `REVISION_PLAN_V5.md` (items 4.3, 4.5, 4.6). Everything is computed in
exact arithmetic (doubled integer coordinates, `Fraction`s, integer plane equations).
Runtime: ~5 s (geometry), ~60 s (swaps), ~2 s (proof), ~10 s (figures).

## Files

| file | purpose |
|---|---|
| `gem_geometry.py` | exact hull: merged facets, vertices, edges, f-vector, rational volume; WL hash + isomorphism for combinatorial type; exact congruence test |
| `run_geometry_880.py` | Part A: all tables for the 880 gems, Dudeney mapping -> `results_geometry.json` |
| `run_swaps_siamese.py` | Parts B/C: exact swap gaps (symmetric E_full), Siamese hulls n=3..21 -> `results_swaps_siamese.json` |
| `siamese_util.py` | Siamese generator, closed form, affine (zeta) coordinates |
| `siamese_proof.py` | Part C: computer-assisted proof of the 12-vertex theorem, symbolic in m=(n-1)/2 -> `results_siamese_proof.json` |
| `make_figures.py` | `fig_gem_geometry_880.pdf`, `fig_gems_cross_order.pdf` (vector, 6.5 in wide, 8 pt fonts) |
| `merge_results.py` | merges everything into `results.json`, prints the LaTeX table rows |
| `fragment.tex` | LaTeX for Sections 4.3, 4.5, 4.6 (+ Siamese proposition with proof); compiles cleanly in a wrapper with the paper's preamble, 0 overfull boxes, 8 pages |

## Headline results

**A. Geometry of the 880 gems**
- Hull vertex counts 8:7, 9:10, 10:103, 11:80, 12:380, 13:106, 14:162, 15:14, 16:18.
- Euler V-E+F=2 holds for all 880 after merging coplanar triangles. 39 distinct f-vectors; the facet-size profile is determined by the f-vector.
- Exact volumes: 155 distinct values, min 58 (square #427), max 292/3 (#379), mean 84.05; denominators 1,2,3,6. Surface area 116.5-148.6.
- **352 combinatorial types** (face lattices up to isomorphism). The WL hash already separated them; explicit isomorphism confirmed every class (0 splits). Sizes: 93 singletons, 201 pairs, 8x3, 20x4, ..., largest type 32 squares (f=(10,22,14)), second 26 (f=(12,24,14)).
- **Congruence: 616 classes** = 352 singletons + 264 pairs. All 880 hull-vertex point sets are distinct (class -> gem injective as point sets). The congruence classes are *exactly* the orbits of the complement map S -> 17-S (the reflection z -> -z): 352 self-complementary squares + 264 mirror pairs. No other coincidences, neither for hull-vertex sets nor for the full 16-point configurations. Kabsch cross-check max RMSD 2e-14.
- Self-complementary squares = all of Dudeney III (48, associated) + all of Dudeney VI (304). The complement map preserves every Dudeney group.
- Dudeney cross-tab (V vs group) from `all7040CategoriesData.csv` (7040 = 880 x 8 D4 variants; mapping unambiguous). Geometry is only loosely tied to the group; 8-vertex gems occur only in VI and VIII; the self-complementary groups have only even V (explained by a remark in the fragment).
- Coincidence to flag: 352 = #types = #self-complementary squares. Checked: different partitions; purely numerical.

**B. Swap gaps**
- Delta E_full = d^2 m(a,b)/N^2 verified exactly on all 105,600 (n=4) + 288 (n=3) swaps and all swaps of the Siamese n=5,7,9: 100% agreement, 0 counterexamples. E_full(S)=0 exactly for every magic square (sanity).
- Min-gap multiset over the 880 (x256): {2: 432, 3: 420, 4: 28}. Over the 8 Lo Shu variants (x81): {3: 8}. Siamese: n=5 -> 3/625, n=7 -> 2/2401, n=9 -> 2/6561.
- Over all 105,600 swaps N^2 Delta E takes 70 distinct integer values (2..980): the v4 "trimodal bands" are an arithmetic artifact.

**C. Siamese gems: PROVED (computer-assisted, all odd n >= 5)**
- Closed form s(i,j) = n<i+j-m> + <i+2j-2m> + 1, m=(n-1)/2, <.> = mod n (3-line induction; verified n=3..41).
- Key idea: z = L(x,y) + n*zeta(x,y), L affine, zeta = -n floor((x-y+m)/n) - floor((2x-y+m)/n) takes only 5 values; affine maps preserve the face lattice, so the gem is affinely the hull of 5 parallel lattice polygons (triangles T, U, D, B and a parallelogram M). The 12 vertices: the 3 vertices of T and of B, one vertex of U and of D, the 4 vertices of M.
- `siamese_proof.py` verifies, as polynomial identities/inequalities in m valid for all m >= 2: 16 explicit planes (8 + central-symmetric images) support conv(12 points) in exactly the claimed faces, the faces close into a surface with (V,E,F)=(12,26,16), every vertex lies on 3 independent planes, and all layer-polygon vertices satisfy every inequality. The fragment gives the full proof with the 8 inequalities in simplified form (checked against the computed planes for m=2,3,5,8).
- Vertex cells: the 4 corners plus, on each side, the two cells holding that side's max and min (top row: n^2-1 and 1, etc.). Hull fraction 12/n^2 -> 0. n=3 degenerates to the 8-vertex Lo Shu gem.

**D. Figures**: `fig_gem_geometry_880.pdf` (a: V histogram; b: volume histogram; c: type-size bar chart; d-f: 3D renders of the (8,14,8) gem #54, the 16-vertex gem #802 (a row-permuted Durer square), the max-volume gem #379). `fig_gems_cross_order.pdf` (Lo Shu, Durer, Siamese 5 with hull fractions and volumes). Both inspected visually.

## Notes for the integrator
- `fragment.tex` references `\ref{sec:swap-formula}` (the theory section proving the swap formula): adjust the label.
- Figures are referenced as `figures/fig_gem_geometry_880.pdf` and `figures/fig_gems_cross_order.pdf`; copy from this directory.
- Uses the paper's `proposition`/`remark` environments and `\Cov`.
- `Analysis/src/analysis.py::compute_full_magic_energy` was NOT used (asymmetric bug); `E_full_exact` in `run_swaps_siamese.py` implements the symmetric definition.
- Sentences worth keeping: (i) congruence classes = complement orbits; (ii) Durer's own gem has V=12 but swapping its row pairs gives a 16-vertex gem; (iii) Siamese gems are affinely "five stacked lattice polygons", which is why their type is constant in n.
