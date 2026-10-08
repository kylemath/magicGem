# Ehrhart theory and large-n hull growth for Magic Gems (exploration, nothing edited in paper dirs)

All code in this directory; every number below was produced by it. Source pipeline: `paper_A_gems/anc/gem_geometry.py` (imported read-only).

## Part 3. Ehrhart polynomials

### Which polytope
Paper coordinates p_ij=(x,y,z), x=j-(n-1)/2, y=(n-1)/2-i, z=s_ij-(N+1)/2. For n=4 all three coordinates are half-odd (2p has all-odd entries; asserted for all 880).
* Gem + (1/2,1/2,1/2) has integer vertices (asserted): this is the lattice polytope **Q = gem + (1/2,1/2,1/2)** used throughout. Equivalently Q=(2p+1)/2; also 2*gem+(1,1,1)=2Q has even coordinates. Q is the smallest scaling (no scaling needed, just the half-translation); any other lattice translate of Q gives the same Ehrhart polynomial. A translation by only (1/2,1/2,0) does NOT give a lattice polytope (z is half-odd too).
* The paper's statement "volumes in (1/6)Z" is confirmed: the volume denominators over the 880 gems are 1 (261), 2 (80), 3 (407), 6 (132); volume of Q equals the exact gem volume from `exact_hull` for all 880 (asserted).
* For odd n (Lo Shu, Siamese) the gem itself is a lattice polytope (x,y,z integers).

### Method (exact)
For each gem: facet inequalities A q <= h (primitive integer A, exact via `_plane`), L(t)=#(tQ cap Z^3) counted on the integer box by integer matrix products, t=0..6. Newton interpolation (sympy, exact rationals) from t=0..3; **t=4,5,6 verified exactly** for every gem; L(0)=1; Ehrhart-Macdonald reciprocity (-L(-1) = #strict interior, counted directly) verified for every gem; h*_3 = #interior points and sum h* = 6 vol verified. Files: `ehrhart.py`, `ehrhart_880.json`, `ehrhart_analysis.py`, `ehrhart_summary.json`, `ehrhart_hstar.png`.

### Results over the 880 order-4 gems
L(t)=vol t^3 + c2 t^2 + c1 t + 1 with vol in (1/6)Z, c2 in (1/2)Z (denominators 1 or 2 only: 634 / 246), c1 in (1/6)Z.
* L(1) (lattice points of Q) ranges 74..140; interior points (=h*_3) 34..52 (17 values, never 0); boundary lattice points 28..96.
* h*-vector (1,h1,h2,h3): h1=70..136, h2=233..403, h3=34..52. **All h* are non-negative integers (Stanley non-negativity holds, as it must for lattice polytopes), also Hibi's inequalities h1<=h2 and h3<=h1 hold in every case.** (Stanley's chain h3<=h1 is a theorem here; this is a consistency check, not new.)
* Distinct objects among 880 gems: **554 distinct Ehrhart polynomials** (= 554 distinct h*-vectors), vs 616 congruence classes (= complement orbits), 352 combinatorial types, 39 f-vectors, 155 volumes. Pairs: (volume,f-vector) 424 classes, (volume,type) 570, (volume, boundary pts) 490, (volume, L(1)) 471. So the Ehrhart polynomial is NOT a function of the f-vector (29 of 39 f-vectors carry >1 h*), NOT a function of the combinatorial type (81 of 352 types carry >1), NOT of the volume (104 of 155 volumes carry >1). Conversely it is far from injective on congruence classes.
* Complement partners (z -> -z reflection) always have equal Ehrhart polynomials (checked all 880): trivially expected.
* **Ehrhart-equivalent but non-congruent gems:** 55 Ehrhart polynomials are shared by >1 congruence class (class counts per polynomial: 1:499, 2:49, 3:5, 4:1). 44 of the shared polynomials even occur with different combinatorial types and 35 with different f-vectors. Examples (square indices): polynomial 1 - 8/3 t + 28 t^2 + 239/3 t^3 shared by #13 and #358; #66 & #318; #73 & #455. Caveat: this only says the Ehrhart polynomials coincide; I did not test unimodular equivalence of the lattice polytopes (it would be a stronger and more interesting statement if it failed).
* Correlation: h*_3 vs volume 0.72, c2 vs volume 0.81: strong but far from determined.
* Lattice width: **every one of the 880 gems has lattice width 3** (min over primitive directions with |u_i|<=8; the x- and y-extents give the upper bound 3, so width<=3 is rigorous; "=3" rests on the search box, directions with larger entries have huge z-extent). Not a discriminating invariant.
* Dürer (square #174 in the 880 numbering): L(t)=1 - 3t + 44t^2 + 92 t^3, h*=(1,130,377,44), 90 boundary / 44 interior points, volume 92, f=(12,24,14), width 3.
* Lo Shu (n=3, gem itself lattice): L(t)=1 + t + 13 t^2 + 18 t^3, h*=(1,29,73,5), 28 boundary / 5 interior points, f=(8,16,10), width 2 (verified with t up to 5).

### Siamese gems of order n=5,7,...,17 (lattice polytopes, 12 vertices)
Exact Ehrhart data in `ehrhart_named.json`. Interpolating in n over n=5,7,...,17 (7 data points) found, with at least 2 independent checks each:
* c3 = volume = n(5n^3-12n^2-n+12)/6  (degree 4 in n; fitted with 5 points and confirmed on n=15,17). Also holds at n=3 (=18, the Lo Shu), though the Lo Shu gem has 8 not 12 vertices.
* c2 = n^3-n^2-2n+1 (confirmed on 7 points; also gives 13 at n=3).
* number of boundary lattice points = 2(n-1)(n^2-2) (confirmed on 7 points; gives 28 at n=3).
* c1 and the interior point count are NOT polynomial in n of degree <=5 on these 7 points (c1 values 1,-11/3,-41/3,-27,-137/3,-203/3,-95,-377/3 at n=3,5,..; arithmetic fluctuation, likely gcd/lattice-length quasi-polynomial effects).
These closed forms are empirical fits (not proved); the volume formula could be proved from the affine reduction in Prop. Siamese, which I did not attempt. Flag as **speculation until proven** if used.

## Part 5. Hull vertices for larger n

### (a) Random permutations on the n x n grid, exact check
`random_perm_hulls.py`; scipy ConvexHull vertex count; for the first 100 samples per batch (4000 per n <=10, 800 for n>10) the vertex set was compared with an exact integer-plane computation (`hulllib.exact_vertices`): **0 mismatches** in all audits. 2 of the n=3 samples were exactly coplanar (hull degenerate) and dropped.

| n | N | samples | E[V] | sd | range | E[V]/N |
|---|---|---|---|---|---|---|
| 3 | 9 | 99998 | 8.212 | 0.668 | 5-9 | 0.912 |
| 4 | 16 | 100000 | 12.056 | 1.277 | 7-16 | 0.753 |
| 5 | 25 | 100000 | 15.397 | 1.695 | 8-23 | 0.616 |
| 6 | 36 | 100000 | 18.394 | 2.060 | 11-28 | 0.511 |
| 7 | 49 | 100000 | 21.063 | 2.363 | 13-33 | 0.430 |
| 8 | 64 | 100000 | 23.541 | 2.636 | 13-36 | 0.368 |
| 9 | 81 | 100000 | 25.798 | 2.903 | 14-38 | 0.318 |
| 10 | 100 | 100000 | 27.902 | 3.157 | 16-42 | 0.279 |
| 11 | 121 | 20000 | 29.848 | 3.387 | 18-44 | 0.247 |
| 12 | 144 | 20000 | 31.733 | 3.541 | 19-47 | 0.220 |
| 13 | 169 | 20000 | 33.470 | 3.771 | 20-48 | 0.198 |
| 14 | 196 | 20000 | 35.046 | 3.912 | 20-53 | 0.179 |
| 15 | 225 | 20000 | 36.595 | 4.121 | 21-54 | 0.163 |
| 16 | 256 | 20000 | 38.070 | 4.235 | 23-56 | 0.149 |

Growth: standard error of E[V] is <=0.03 everywhere. The fit a ln^2 N + b ln N + c (a=0.81, b=2.63, c=-1.50) has chi^2=24.7 on 11 dof (acceptable given the model is only asymptotic); a pure a ln N + b and a ln^2N + b fit are rejected (chi^2>10^4), as is a pure power law (local exponent d ln E[V]/d ln N falls monotonically from 0.67 at n=3-4 to 0.31 at n=15-16, i.e. clearly sub-polynomial). So growth is slow, consistent with polylogarithmic (the known random-points-in-a-cube behaviour (ln N)^2 in 3D); with n<=16 this cannot distinguish polylog scalings rigorously. Hull fraction falls from 0.91 (n=3) to 0.15 (n=16). Plot: `largen_growth.png`.

### (b) Magic squares: sources and bias
* `sa_magic.c`: simulated annealing on F = sum over 2n+2 lines (line sum - M)^2 from random permutations, swap moves, geometric cooling, stop at the first F=0, fresh random restart per square. Raw output distinct up to D4 (and complement not quotiented): n=4: 20000 draws hit **all 880** classes; n=5: 60000 raw -> 59993 distinct; n=6: 24000; n=7: 8000; n=8: 2400 (all distinct).
* **Bias test at n=4 (ground truth available):** class hit counts range 10..41 (mean 22.7), coefficient of variation 0.217 vs 0.21 expected for uniform Poisson; chi^2 uniformity p=0.078; V-mean weighted by hit counts 12.240 vs uniform 12.227. So the sampler is close to uniform at n=4. No evidence at n>=5 (no ground truth; the 275 305 224 order-5 classes cannot be enumerated here), and there SA could be biased toward "easy-to-reach" squares. Samples are small fractions of the space (n=5: 60000/2.75e8).
* Constructions (`constructions.py`): all generalised de la Loubere (start cell, step vector, break vector) fills that are magic: n=5: 12000 valid fills -> 184 classes up to D4; n=7: 98784 valid fills -> 3159 classes (counts of valid ones computed from all start/step/break choices, mod n). n=6: Strachey-type (4 copies of an oriented Lo Shu with offsets 0,9,18,27, any left-block swap) 16 classes + Conway LUX 8 classes, 24 distinct up to D4 in total (a modest set; the full Strachey/LUX families are small). n=3: Lo Shu only.

### Table (V = number of hull vertices; "magic" = SA sample mean +- sem)
n=4 magic is exact over all 880.

| n | random perm E[V] | magic E[V] | magic sd (random sd) | z (magic-random) | KS p | constructions mean (count) | min-max magic |
|---|---|---|---|---|---|---|---|
| 3 | 8.212 | 8 (Lo Shu, unique) | | | | | |
| 4 | 12.056 | 12.227 (all 880) | 1.438 (1.277) | significant (exact) | 0 | - | 8-16 |
| 5 | 15.397 | 15.384 +- 0.007 (59993) | 1.617 (1.695) | -1.6 | ~0 | 14.36 (184) | 10-23 |
| 6 | 18.394 | 18.407 +- 0.013 (24000) | 1.990 (2.060) | +0.9 | 0.085 | 18.08 (24) | 12-27 |
| 7 | 21.063 | 21.085 +- 0.026 (8000) | 2.280 (2.363) | +0.8 | 0.25 | 18.77 (3159) | 14-30 |
| 8 | 23.541 | 23.563 +- 0.054 (2400) | 2.661 (2.636) | +0.4 | 1.0 | - | 16-34 |

Findings:
* **The magic constraint does not change vertex-count growth**: SA magic means agree with random-permutation means within ~1.6 sigma for n=5..8. At n=4 the magic ones have slightly more vertices (12.23 vs 12.06, exact). At n=5 the magic V distribution is slightly narrower (sd 1.62 vs 1.70, total-variation distance 0.025, KS p~0) with fewer very low and very high V; at n>=6 differences are within noise-ish (TV 0.016-0.026). Plot `largen_Vhist.png`.
* **Classical constructions are not typical**: Siamese-type n=5 fills average 14.4 vertices (range 11-18; 12 is the Siamese square itself) and n=7 fills average 18.8 vs 21.1 for SA; only the exact original Siamese squares have V=12 for all odd n up to 21 (checked n=3..21: 8,12,12,...). So the "constant 12" of the Siamese family is a property of that single highly structured family, not of magic squares. Order-6 constructions (24 squares) average 18.1, near the typical value.
* The Siamese V=12 is in the lower tail but not exceptional at n=5 (SA magic min 10), and far below typical at n>=7 (n=7: SA min 14; n=8 min 16): by n~7 a V=12 gem is atypical.

### Constant-box / extreme-value statement
Verified (asserted in code for every random and magic sample): the cell with s=1 and the cell with s=N are always vertices (they are the unique points attaining min and max z). Also measured: the cells with s=2 (or N-1) are vertices in 99.1% (n=4), 97.8% (n=5), 97.7% (n=6,7,8) of magic samples (Siamese-type fills lower: 88% n=5, 84% n=7), so "extreme z values" beyond the unique extremes are not guaranteed. Hence V>=2 trivially and the lower bound V>=? is empirical only (min over 59993 SA squares at n=5 is 10, over random perms 8).

## Recommendation for Paper A
1. A short remark/subsection (and perhaps one row of a table) on Ehrhart: the order-4 gems are lattice polytopes after the half-integer translation, 554 distinct Ehrhart polynomials among the 880 gems, h* nonnegative, widths all 3, 55 polynomials shared by non-congruent gems. These are exact, reproducible, and cheap to cite; but their mathematical interest is moderate (all lattice polytopes obey these). Dürer and Lo Shu values give a nice concrete example.
2. The Siamese Ehrhart closed forms (volume, c2, boundary count) are the most elegant new statements but are only fitted; include only after a proof (volume is derivable from the 12-vertex description) or mark as "verified for n<=17".
3. For the large-n discussion: report the random-permutation growth table (n=3..16) and that magic constraint barely changes E[V] (with the n=4 exact and n=5..8 sampled numbers, sampling caveat), and emphasise the contrast with the constant-12 Siamese family. Do not claim growth law beyond "slow, sub-polynomial, consistent with polylog".
4. Do not claim anything about uniformity of magic sampling for n>=5.

## Reproduce
`ehrhart.py` -> `ehrhart_analysis.py`, `ehrhart_named.py`, `ehrhart_siamese_more.py`, `ehrhart_plots.py`; `cc -O2 sa_magic.c -o sa_magic -lm; run_sa.sh n total steps T0 T1` (parameters used: n=4 20000/2e5/20/0.5; n=5 60000/4e5/30/0.5; n=6 24000/1e6/40/0.5; n=7 8000/1.5e6/60/0.5; n=8 2400/2.5e6/80/0.5); `random_perm_hulls.py`; `magic_hulls.py`; `largen_report.py`.
