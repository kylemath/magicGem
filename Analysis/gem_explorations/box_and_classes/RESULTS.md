# Bounding box and square classes for the 880 order-4 gems

Script: `box_and_classes.py` (uses `paper_A_gems/anc/gem_geometry.py`, `squares880.txt`, `symmetry_880.json`, `all7040_dudeney.csv`; exact integer hulls; every statement below marked VERIFIED is asserted in the script). Full tables: `results.json`.
Dudeney group is checked D4-invariant (each of the 7040 squares maps to its D4 class, no clashes).
Flags: **PROVED** (general n, proof given) / **VERIFIED-n4** (exhaustive over the 880, no proof) / **OBSERVED** (n=4 only).

## 1. Bounding box

**PROVED (all n).** With x = j-(n-1)/2, y = (n-1)/2-i, z = s_ij-(N+1)/2, every point lies in B = [-(n-1)/2,(n-1)/2]^2 x [-(N-1)/2,(N-1)/2] since |x|,|y| <= (n-1)/2 and 1 <= s <= N. B is convex, so every gem is inside B; B is the same for all squares of order n. Volume of B = (n-1)^2 (N-1); n=4: 135.
**PROVED.** The points carrying 1 and N are the unique minimiser/maximiser of z (entries are distinct), so they are vertices (supporting plane touching in one point), and they are the only points on the planes z = -+(N-1)/2.
**PROVED (new, general n >= 2): forced vertices.** (i) the 4 grid corners (unique maximisers of +-x+-y); (ii) on each of the 4 side lines of the grid, the points with min and max entry (maximise x (or y, -x, -y) with a tiny z perturbation: the supporting face of the grid projection is the side line, and the z-extremes of a collinear point set are extreme); (iii) 1 and N. Up to 4 + 8 + 2 forced points; as few as 4 distinct when these coincide (VERIFIED-n4: forced set size ranges 4..13, always contained in the vertex set, asserted for all 880).
**Not forced (VERIFIED-n4, counterexamples).** Over the 880, the only grid cells that are vertices in every gem are the 4 corners (cells 0,3,12,15); the only entries that are vertices in every gem are 1 and 16. Entries 2 and 15 are NOT forced: each is a non-vertex in 8 of 880 classes (872 vertices each). No other forced-vertex statement holds for n=4 (all other cell counts <= 834/880).
**Contact pattern is trivial.** Every gem touches all six faces of B: z-faces at the single points of 1 and N; x- and y-faces along the hull of the 4 points of the corresponding grid side line (a polygon with 2,3 or 4 vertices). So "which faces are touched" is a constant (PROVED, all n). Nontrivial contact invariant (VERIFIED-n4): the sorted vertex counts of the four side-contact polygons: (4,4,4,4):383, (3,4,4,4):194, (3,3,4,4):241, (3,3,3,4):32, (3,3,3,3):6, (2,4,4,4):15, (2,3,3,4):5, (2,2,4,4):4 (2 = three or more of the side's points collinear in a vertical plane, impossible to be a quad).

**Volume fraction (VERIFIED-n4, exact).** vol/135: min 58/135 = 0.4296, mean 2219/3564 = 0.6226, max 292/405 = 0.7210; 155 distinct values (matches the published 155 distinct volumes). The full list of the 155 fractions with multiplicities is in `results.json` -> `volume_fraction_distinct`. Mean fraction by vertex count: 8: 0.642, 10: 0.631, 12: 0.634, 14: 0.608, 15: 0.560, 16: 0.536 (more vertices <-> smaller volume fraction, mildly).

**Vertex count (VERIFIED-n4).** nv: 8:7, 9:10, 10:103, 11:80, 12:380, 13:106, 14:162, 15:14, 16:18 (sum 880).
**Non-vertex points** (16-nv) split into strictly interior and boundary-non-vertex: interior 0:37, 1:32, 2:353, 3:178, 4:280 (never more than 4). Boundary non-vertex 0:357, 1:204, 2:257, 3:40, 4:21, 6:1.

**Distance between points of 1 and 16** (squared, original units; = 225 + dx^2 + dy^2): 226:368, 227:60, 229:168, 233:48, 234:200, 235:24, 243:12. 7 distinct values; minimum 226 (cells adjacent, offset (1,0) or (0,1)); 225 never occurs (same cell impossible); max 243 (offset (3,3)... 225+18) in 12 classes. OBSERVED only.

## 2. Square classes vs geometry

Counts among the 880 classes: pandiagonal 48, associative 48, both 0, self-complementary 352, most-perfect 48 (= exactly the pandiagonal ones; VERIFIED-n4). Dudeney group 1 = exactly the 48 pandiagonal classes, group 3 = exactly the 48 associative classes, group 6 = exactly the 304 classes with hull symmetry C2 (VERIFIED-n4; checked equal). Self-complementary here = equal to its complement 17-s up to D4 (agrees with `symmetry_880.json`).

Vertex count by class (rows: type; entries are nv: #classes):

| type | #classes | vertex counts |
|---|---|---|
| pandiagonal (= Dudeney 1 = most-perfect) | 48 | 11:10, 12:20, 13:12, 14:4, 15:2 |
| associative (= Dudeney 3, group Ci) | 48 | 10:13, 12:28, 14:4, 16:3 |
| self-complementary | 352 | 8:3, 10:53, 12:178, 14:102, 16:16 |
| not self-compl. | 528 | 8:4, 9:10, 10:50, 11:80, 12:202, 13:106, 14:60, 15:14, 16:2 |
| Dudeney 2 | 48 | 10:4, 11:14, 12:14, 13:6, 14:6, 15:2, 16:2 |
| Dudeney 4 | 96 | 10:12, 11:20, 12:40, 13:14, 14:10 |
| Dudeney 5 | 96 | 10:12, 11:10, 12:34, 13:20, 14:16, 15:4 |
| Dudeney 6 (C2) | 304 | 8:3, 10:40, 12:150, 14:98, 16:13 |
| Dudeney 7 | 56 | 11:4, 12:20, 13:22, 14:4, 15:6 |
| Dudeney 8 | 56 | 8:4, 9:0..: 8:4, 9:8, 10:10, 11:4, 12:24, 13:6 |
| Dudeney 9 | 56 | 9:2, 10:10, 11:18, 12:12, 13:10, 14:4 |
| Dudeney 10 | 56 | 12:32, 13:8, 14:16 |
| Dudeney 11 | 8 | 12:4, 13:4 |
| Dudeney 12 | 8 | 10:2, 12:2, 13:4 |

Every Dudeney group has a single hull symmetry type: 3 -> Ci, 6 -> C2, all others C1.  Self-complementary classes: nv always even (8,10,...,16), OBSERVED (the 352 = 304 C2 + 48 Ci hulls; the 48 Ci ones are the associative ones, covered by the proof in (b); evenness for the 304 C2 ones is not proved here).

Interior points by type: pandiagonal 1:4, 2:12, 3:28, 4:4 (never 0); associative 0:4, 2:23, 4:21; Dudeney 6: 0:29, 2:148, 4:127; Dudeney 11,12: only 2 or 3 interior.
Volume fraction mean by type: pandiagonal 0.643 (0.543..0.690); associative 0.646 (0.570..0.719); all others 0.621.

### Specific tests
- **(a) Pandiagonal with 16 vertices: NO.** 0 of 48; vertex counts 11-15 only. OBSERVED (n=4 exhaustive over the 48 classes); no proof. Note pandiagonal squares also never have 8,9,10 vertices; they have >=1 interior point always. Mild/odd-looking and unexplained; would be a clean table row but not a theorem.
- **(b) Associative squares: all non-vertex counts even.** YES, **PROVED for every even n**: associative means s(i,j)+s(n-1-i,n-1-j)=N+1, i.e. the point set is invariant under the point reflection p -> -p; this is a fixed-point-free involution (the only fixed point of -I is the origin, not a point for even n), and it maps vertices to vertices, strictly interior to strictly interior, boundary-non-vertex to the same. Hence nv, #interior, #boundary-non-vertex are all even (VERIFIED-n4: interior 0:4, 2:23, 4:21; nv in {10,12,14,16}). For odd n the centre point (value (N+1)/2) is fixed, so parities of interior count change (it is interior). Non-associative squares have all parities (odd interior counts 1 and 3 occur: 32+178 classes). Also the hull is centrally symmetric (group contains -I, the Ci row).
- **(c) Minimal vertex count 8:** 7 classes, k = 50, 54, 672 (Dudeney 6, C2, self-complementary, f = (8,16,10), (8,14,8), (8,17,11)) and 276, 277, 494, 496 (Dudeney 8, C1, not self-compl., f = (8,18,12)). None is pandiagonal or associative; all have 4 interior points (so 8 vertices + 4 interior + 4 boundary non-vertex). Volume fractions 29/45, 28/45, 257/405, 35/54 (x4). Min forced vertices is 4, but nv>=8 observed only (no lower-bound proof; the trivial bound from forced vertices gives 4).

## Recommendation for Paper A
Include (short proposition, proof one paragraph): the bounding-box statement (same box for all squares of order n; volume (n-1)^2(N-1)), 1 and N are vertices and touch the z-faces, corners always vertices and side-extreme entries are vertices; plus the one-line remark that the vertex-count/interior-count of associative squares are even (central symmetry, even n) -- this ties to existing C_i table. Include one table: volume fraction min/mean/max (58/135, 2219/3564, 292/405) and nv distribution. Optional one-sentence observations: no pandiagonal gem has 16 (or <=10) vertices; the 8-vertex gems are not pandiagonal/associative (7 classes, Dudeney 6 and 8); Dudeney groups 1, 3, 6 coincide with pandiagonal, associative (Ci), C2. Omit: 1-16 distance distribution, face-contact polygon patterns, forced-entry-2/15 negative result (at most one clause: "2 and N-1 are not forced").
