# Review dialogue: Magic Gems: A Polyhedral Framework for Magic Squares

## REVIEWER — turn 1

I read every `.tex` file (abstract, introduction, gem, balance, symmetry, geometry, siamese, discussion, appendix) and `anc/siamese_slacks.tex`. I did not take any number on trust. I wrote my own exact convex-hull code: brute force over all triples, integer planes, no Qhull and no code from `anc/` (scratch: `.../scratchpad/dialogue/hull.py`, `t1.py`–`t6.py`). I used it to recompute the items below.

**Verified independently (no action needed):**
- V0.1 Lo Shu (Ex. 2.4): f = (8,16,10), volume 18, one interior point.
- V0.2 Dürer: f = (12,24,14), volume 92, V° = 4.
- V0.3 #54: f = (8,14,8). #802: all 16 points are vertices. #379: volume 292/3. #593: the entry 2 is a boundary non-vertex point. The seven matrices printed in Sec. 5 equal lines #45, #54, #102, #124, #379, #593 and #802 of `squares880.txt`, and each is in Frénicle standard form.
- V0.4 Table 2, every row (squares, volumes per V, min/mean/max of vol/135), the V° and V∂ rows, 39 f-vectors, most frequent (12,26,16) with 164 gems, 155 volumes in [58, 292/3], mean 84.053, mean V = 269/22. I also checked that the vertical-facet counts are 856/20/4 and the symmetry classes 48/304/528.
- V0.5 Thm 4.3 (order four). For every gem I counted the distance-preserving permutations of the vertex set: 528 gems have 1 and 352 have 2. These are exactly the isometries, since the vertices span R³.
- V0.6 Prop. 5.1. The 880 vertex sets have 880 distinct D4-canonical forms. The sorted multiset of squared distances takes exactly **616** values over the 880 vertex sets. Since 616 classes is also an upper bound (complement orbits), this alone proves "616 congruence classes" (see R1.19).
- V0.7 Mixed moment: |8Σzxy| takes 48 values in [0, 480] and is 0 for 56 squares. The associative squares have V° ∈ {0, 2, 4} with counts (4, 23, 21).
- V0.8 Thm 6.2. For n = 5, 7, 9, 11 the vertex cells and entries match the 12-cell table and f = (12,26,16); the n = 5 volume is 830/3. Symbolically I recomputed:
  - all 128 slack entries of Table 3: each agrees exactly, factorisation included;
  - the layer description of ζ, with an exhaustive check for m = 2..7;
  - the 16 facet lists close up (26 edges, each in exactly 2 facets);
  - Φ is linear (λ has zero constant term), so the antipodal relations are legitimate;
  - the Step 5 norms and inner products, and that the original z-coordinates equal λ + nζ.
- V0.9 Digit-exchanged square: magic for n = 3..11, and f = (12,24,14) for n = 5, 7, 9.
- V0.10 Dudeney labels: group III is exactly the associative squares (384/8 = 48). Group VI has 2432/8 = 304 squares.
- V0.11 By hand: Lemma 2.2, Prop. 2.3 (the u, w argument is complete), Lemma 4.1, Thm 4.2, Cor. 3.1 (s̄·2Na_n = n²(n⁴−1)/12), Lemma 3.2, Lemma 4.4, Lemma 6.1 (|εz| < 1/2 is the point), Step 1 induction, Rogers–Shephard constants (binom(6,3)/8 = 5/2).

My overall view: the mathematics I could check is correct, and the census is reproducible. My concerns are gaps in exposition, a few unproved sub-claims, terminology, and readability.

### (a) Claims or proof steps I could not verify from the text

- **R1.1** Thm 6.2, Step 3: "a case check of the two floors shows that ζ takes five values, on the lattice points of five convex lattice polygons". The case check is not printed. It is short, and a reader needs it: of the nine pairs (⌊A/n⌋, ⌊B/n⌋) ∈ {−1,0,1}², only five occur, and they occur on the stated regions. Please print the three-line argument. For example, A < 0 forces B < 0, and A ≥ n forces B ≥ n. I checked this exhaustively for m ≤ 7 but not in general.
- **R1.2** Thm 6.2, Step 4: "(2),(3) … which are convex in the cyclic orders given". The appendix says convexity was checked only "for m ≤ 60", but the theorem claims every m ≥ 2. Convexity itself is automatic: all four points are vertices of P, so they are in convex position. What needs proof is the **cyclic order**, because the edge count of 26 depends on it. It has a two-line proof for all m:
  - (2) is the trapezoid with parallel sides ζ = 2m+2 (x ∈ [−m, −1]) and ζ = 0 (x ∈ [0, m]);
  - in (3), v4 = (y,ζ) = (0,1) lies strictly below the segment from v5 = (−m,0) to v1 = (m,2m+2), which has height m+1 at y = 0, while v3 lies above it.

  Please replace the m ≤ 60 check by this argument.
- **R1.3** Step 4: the eight inequalities appear with no derivation. A reader can check them only by evaluating them against the 16 points. Please state each one as "the plane through v_a, v_b, v_c" (that information is already in the zero pattern). Then the reader sees why these planes are the candidates, and the table becomes a check rather than a revelation.
- **R1.4** Prop. 2.5(4): "The face lattice of G(S), with vertices labelled by cells, is determined by the pair (S(z), S(−z))". The proof is one sentence. It omits the facts that make the gluing work:
  - a lower facet and an upper facet can share an edge only over ∂conv A (the vertical width is positive over int conv A);
  - the vertical facets are exactly the polygons between the lower and upper boundary chains.

  Please give two more sentences, or downgrade the item to a remark.
- **R1.5** Rem. 4.5 (Facet orbits): "a facet plane is ι_h-invariant if and only if its normal is parallel to the axis". The proof omits a second case: normals perpendicular to the axis, which give invariant planes exactly when the plane passes through the origin. That case is excluded because 0 is interior (Prop. 2.3), but the text should say so.
- **R1.6** Sec. 2.1, the paragraph after Prop. 2.5: "the other forced vertices of Lemma 6.1 are the lowest and the highest lifted point over each edge of conv A, which are vertices of the restrictions of S(z) and S(−z) to that edge". "Restriction of a subdivision to an edge" is not defined. Is this meant as the induced 1-dimensional regular subdivision of the side? Please make it precise or delete it.
- **R1.7** Rem. 6.3 (linear squares). I cannot reproduce this from the text. Questions for the advocate:
  - (i) What exactly is enumerated? Are u, w ∈ Z_n² and α, β ∈ Z_n all included, with which conditions (bijectivity, magic), and are classes counted up to D4 only or also up to complement?
  - (ii) Why does n = 9 have only 441 classes against 3159 for n = 7? I assume 3 | n kills many (u, w); the text should say so.
  - (iii) The text says "the minimum 12 is attained by exactly two classes for n = 7, 9, 11 … For n = 7 the other is the square [digit-exchanged]". My computation gives the digit-exchanged square V = 12 for n = 9 as well, and the remark itself says (12,24,14) for n = 5..31. So is the other class the digit-exchanged square for n = 9 and 11 too? If so, write "for n = 7, 9, 11". If not, which class is it?
  - (iv) For n = 5 the minimum is 11 < 12. Which square attains it?
- **R1.8** Discussion Q3: "standard errors at most 0.01", and the annealer means. These are floating-point Monte Carlo with no stated seed. Fine for an open question, but please say they are not claimed as results, and give seeds or the script line.
- **R1.9** Sec. 3, "for order six the count … was computed exactly by H. Mino in 2024 [trump2012enumeration]". The citation key says 2012, the bib entry 2024, and it is a website. Is there a primary source (arXiv or a report by Mino)? If not, cite the website as the source of the announcement and say so.

### (b) Errors found

No mathematical error survived my recomputation. Two inconsistencies:

- **R1.10** `anc/all7040_dudeney.csv`:
  - It is **tab-separated** despite the `.csv` extension; `csv.DictReader` without `delimiter='\t'` fails.
  - Its column `Nr.` is **1-based**: CSV `Nr. 102` is the paper's **#101**. Its first data row has `Nr. 102`, which a reader will take for the paper's #102 (a different square with the same first row 1 8 10 15).

  Please rename the file to `.tsv` or convert it, and state the offset in the README, or renumber.
- **R1.11** Rem. 4.6 attributes both bounds to Rogers–Shephard. The lower bound vol(K−K) ≥ 2³vol K, with equality iff K is centrally symmetric, is Brunn–Minkowski. Rogers–Shephard is the upper bound. A small attribution error.

### (c) Jargon and nonstandard terminology (with the standard alternative)

- **R1.12** Invented names a combinatorialist would trip on:
  - "Magic Gem" / "gem" is acceptable as a name, but the first sentence should say plainly that it is the *lift* of the grid by the heights (the term used in the regular-subdivision literature).
  - "gem coordinates" (Def. 2.1 title): just "Definition (the lifted point set)".
  - "centred entry": "the entry minus the mean entry".
  - "deviation δ_L": "line-sum defect" or simply "s(L) − μ_n". This is a minor point.
  - "vertex fraction V/N": drop; it is used twice.
  - "boundary non-vertex point": "non-vertex boundary point" (word order as in the literature) or "point in the relative interior of an edge or facet".
  - "forced vertices": "vertices common to all arrangements" or "universal vertices". At minimum, define the term in the lemma statement, not only by reference.
  - "layers", "layer polygons", "affine reduction to five layers": "after the shear Φ the heights take five values; the level sets are the lattice points of five polygons". Say "shear", which is what Φ is.
  - "slack polynomials": fine, but say once "slack = right-hand side minus left-hand side", as in Step 4, earlier in the abstract and introduction.
  - "digit-exchanged Siamese square": define it by its formula at first use.
  - "central-symmetry defect σ": the literature calls vol(K−K)/(8 vol K) the (normalised) difference-body volume ratio, or speaks of the Rogers–Shephard ratio; avoid a new name.
- **R1.13** Notation from outside mathematics:
  - The Schoenflies symbols C_i, C_2 (Table 1, Thm 4.3) come from chemistry. Write {±id} and "the cyclic group generated by a half-turn".
  - "Chiral" is acceptable in geometry, but define it: "has no orientation-reversing isometry".
  - "Dipole moment", "multipole language" and the checkers in Fig. 4 are physics metaphors. Keep "dipole moment" only as an attributed aside ("called the dipole moment by Rogers and Loly") and use "the first moments Σz·x, Σz·y" in the statements, including the hypothesis of Thm 4.2.
- **R1.14** "Row-by-row arrangement" (Prop. 2.3): the standard name is the "natural square" (or "natural arrangement"). Also, "arrangement" is the paper's own word for a bijection cells → [N]. This is acceptable, but say it is a permutation.
- **R1.15** "Weisfeiler–Lehman hash" appears in the main text (Sec. 5). It is an implementation detail; keep it in the appendix and state in Sec. 5 only that types were determined by graph isomorphism tests of the vertex–facet incidence graphs.
- **R1.16** "Injectivity" (Prop. 5.1 title): injectivity of which map? Say "The vertex set determines the square".

### (d) Passages hard to follow

- **R1.17** Notation clashes that cost a reader time:
  - **v**: the reflection v ∈ D4, the vertex **v** in the proof of Prop. 2.5(3), and v_1..v_12 in Thm 6.2.
  - **t**: the transpose, the variable in φ(t), the argument of ⟨t⟩, and p(2+t) in the appendix.
  - **A**: the grid A, and the isometry A in the proof of Thm 4.2.
  - **P**: the point set P_S, and the polytope P = conv{v_k} in Step 4.
  - **q, r**: Euclidean quotient/remainder in Step 1, while r is the quarter-turn.
  - **Q** (polyhedron) and **q** (point).
  - **Γ** is introduced for facets and then used only in a figure caption.

  Please rename: for instance σ_h, σ_v, σ_d for the reflections, T for the transpose, and drop Γ.
- **R1.18** Forward references: Lemma 6.1 ("forced vertices") is used in Sec. 2.1 and Sec. 5 before it is stated in Sec. 6. It is a self-contained, four-line, general-n fact. Move it to Sec. 2, right after Prop. 2.3. Sec. 6 then needs only the Siamese material.
- **R1.19** Prop. 5.1(2): the "only if" direction is certified by an all-pairs isomorphism test of edge-labelled complete graphs (appendix). A much simpler certificate exists, which I verified (V0.6): the sorted multiset of the 120 or fewer pairwise squared distances of the vertex set takes 616 distinct values. This lower bound, with the "if" direction, gives 616 at once. Suggest using it; a reader can check it in ten lines.
- **R1.20** Thm 4.2 is stated for "arrangements whose dipole moments vanish, for instance semi-magic squares". The abstract and introduction say "semi-magic". Fine, but the theorem is in Sec. 4 while the term is defined in Sec. 3 inside a paragraph. Put the hypothesis in words in the theorem: "Σ z_ij x_ij = Σ z_ij y_ij = 0".
- **R1.21** Sec. 2.1 is dense for a reader outside triangulation theory: secondary cone, marked subdivision, "lower faces ... outer normal negative last coordinate" in one paragraph. Proposal:
  - add one sentence of motivation (the gem is two regular subdivisions glued along the boundary);
  - add one small picture or example for the Lo Shu: S(z) and S(−z) for the 3×3 grid;
  - say explicitly that cells are *marked* (they may contain non-vertex grid points).
- **R1.22** Thm 6.2 Step 4: "every entry is 0 or a product of factors that are positive for m ≥ 2". Several entries are irreducible quadratics (e.g. 4m²−3m+1, 2m²+2m−1). Say "each non-zero entry is a product of polynomials with positive values at every integer m ≥ 2 (verified by the coefficient test of the appendix)", or note that each quadratic has its roots below 2.
- **R1.23** Sec. 5, "For these 880 gems the multiset of facet sizes is determined by the f-vector". This is a computed curiosity with no stated use. Cut it, or say why it matters.
- **R1.24** Sec. 5, "The vertex count is not tied to Dudeney's groups". This is vague. State the fact ("each group with more than eight members contains gems with at least three different vertex counts") and drop the interpretation.

### (e) Overclaims

- **R1.25** Sec. 2.1, last paragraph: "The census of combinatorial types … thus records which pairs of secondary cones of the 4×4 grid contain the pairs (z,−z)". It does not. Combinatorial types are unlabelled face lattices up to isomorphism, whereas a pair of secondary cones is a *labelled* datum. The census is a coarsening. Likewise "the Siamese theorem … is the computation of S(±z)" is loose, because the proof computes the hull directly. Suggest: "the census is a coarse invariant of the pair (S(z), S(−z))".
- **R1.26** Intro, item 3: "The proof is printed in full as a table of slack polynomials". After R1.1–R1.3 this will be true. As it stands, two steps (the layer case check and the cyclic order) are not printed.
- **R1.27** Novelty paragraph: "New are the symmetry and congruence theorem for point sets of every order …". Thm 4.2 is correct and pleasant, but its proof is a few lines once Lemma 3.2 is known. I would present it as "a short observation that settles …" rather than as the main theorem. The paper's genuinely non-trivial results are Thm 6.2 and the exact order-four census. Ask: would the author accept reordering the abstract so that Thm 6.2 and the census lead?
- **R1.28** Abstract: "we compute the gems exactly and show that no gem has an isometry beyond those of its point set". Add "by exact computer enumeration" in the abstract, as in the theorem title, so the reader knows which results are computer-assisted.
- **R1.29** Discussion Q3 compares with Bárány's Θ(ln² N) for i.i.d. uniform points in a polytope. Our points are not i.i.d.: the grid is fixed and the heights are a random permutation. Present this as a heuristic analogy, not as the expected answer.

### Questions for the advocate

- **Q1.1** (R1.7) The exact definition and parameter ranges of the "linear magic squares" in `anc/linear_squares.py`, and the answers to R1.7(ii)–(iv).
- **Q1.2** (R1.2) Is there any reason the m ≤ 60 convexity check was used rather than a proof for general m? Is anything else in `siamese_slacks.py` checked only for bounded m?
- **Q1.3** (R1.9) Primary source for the order-six count.
- **Q1.4** (R1.27) Is the author attached to Thm 4.2 leading the abstract and introduction?
- **Q1.5** Thm 6.2 includes n = 3 in its hypothesis ("n = 2m+1 ≥ 3"), but the f-vector and isometry claims are for n ≥ 5, and the abstract says n ≥ 5. Should the statement be split as "n = 3: Lo Shu, f = (8,16,10); n ≥ 5: …" for clarity?

## ADVOCATE — turn 1

Checks run for this turn (scratch: `.../scratchpad/adv/`): `linmin.py` (all linear magic squares n = 5, 7, 9, 11, using the hull routine in `anc/gem_geometry.py`; prints the classes with the fewest vertices), `dist616.py` (multisets of squared distances of the 880 vertex sets), a classification of the Lo Shu facets into lower, upper and vertical, a byte dump of `anc/all7040_dudeney.csv`, and a reading of `anc/siamese_slacks.py`, `anc/vertex_stats_*.json`, `anc/run_sa.sh` and `anc/vertex_statistics.py`. I accept V0.1–V0.11 as stated.

### (a) Unverified steps

- **A1.1 (R1.1) AGREE.** Proposed text for Step 3, replacing "a case check of the two floors shows":
  > Put A = x−y+m and B = 2x−y+m, so that ζ = −n⌊A/n⌋ − ⌊B/n⌋ and B = A + x. For |x|,|y| ≤ m we have −m ≤ A ≤ 3m and −2m ≤ B ≤ 4m, so both floors lie in {−1,0,1}.
  > - If A < 0, then x ≤ y−m−1 ≤ −1, so B = A+x < 0 and ζ = n+1.
  > - If A ≥ n, then x ≥ y+m+1 ≥ 1, so B ≥ n and ζ = −(n+1).
  > - If 0 ≤ A ≤ 2m, then ⌊B/n⌋ = −1, 0, 1 according as y ≥ 2x+m+1, |y−2x| ≤ m, or y ≤ 2x−m−1.
  >
  > Conversely, |y−2x| ≤ m together with |x|,|y| ≤ m forces 0 ≤ A ≤ 2m. (If y > x+m, then y ≤ 2x+m gives x > 0 and so y > m; the other side is symmetric.) So only the five pairs (−1,−1), (0,−1), (0,0), (0,1), (1,1) occur, on the regions stated.

  I checked the three regions against the polygon vertices printed in lines 77–79 of `siamese.tex`. Each region's real vertices are lattice points, so the region equals the convex hull of its lattice points. Example: Λ₊₁ has the corner (−1, m−1), where y = 2x+m+1 meets y = x+m.
- **A1.2 (R1.2, Q1.2) AGREE.** Use your argument and delete the m ≤ 60 loop, both from the script (lines 104–111 of `siamese_slacks.py`) and from the sentence in the appendix. Wording:
  > All four points of each quadrilateral are vertices of P (they are forced vertices), so they are in convex position, and the cyclic order is the only thing to check.
  > - In the plane y = m, the points v₁ = (−m, 2m+2), v₂ = (−1, 2m+2), v₈ = (m, 0), v₇ = (0, 0), written as (x, ζ), form a trapezoid. Its parallel sides v₁v₂ and v₈v₇ are traversed in opposite directions.
  > - In the plane x = −m, written as (y, ζ), the line through v₅ = (−m, 0) and v₁ = (m, 2m+2) has height (m+1)(y+m)/m. At y = 0 this is m+1 > 1, so v₄ = (0, 1) lies below the line. At y = 1 it is m+2+1/m < 2m+2, so v₃ = (1, 2m+2) lies above it. Hence v₁v₅ is a diagonal, and v₁v₃v₅v₄ is the cyclic order.

  Answer to Q1.2: the m ≤ 60 loop is the only bounded-m check that the proof relies on. The loop over n = 5..41 (script lines 116–126) is an extra numerical cross-check. The isometry part uses polynomial identities and root tests that hold for all m.
- **A1.3 (R1.3) AGREE.** Add a column "plane through" to the inequality list, or one sentence before it:
  > (k) is the plane through the first three points of its list below.

  That is: (1) v₁v₂v₃; (2) v₁v₂v₈; (3) v₁v₃v₅; (4) v₁v₄v₇; (5) v₂v₃v₆; (6) v₂v₆v₉; (7) v₂v₈v₉; (8) v₃v₅v₆. Then the reader can rederive each normal as a cross product.
- **A1.4 (R1.4) AGREE.** Add to the proof of Prop. 2.5(4):
  > Let U and L be the upper and lower boundary functions over conv A. The vertical width U − L is concave and non-negative, and it is positive at the projection of an interior point, so it is positive on int conv A. Hence a lower face and an upper face meet only over ∂conv A. Over a side e of conv A, the gem meets the vertical plane in conv{p_c : c ∈ e} (e is a face of conv A). This polygon is bounded below and above by the chains of S(z) and S(−z) restricted to e, and it is a vertical facet exactly when the two chains differ.
- **A1.5 (R1.5) AGREE.**
  > The image of the plane a·p = b under ι_h is the plane ι_h(a)·p = b. The two planes coincide iff ι_h(a) = a, i.e. a is parallel to the axis, or ι_h(a) = −a and b = 0. The second case is a plane through 0, and 0 is interior (Prop. 2.3).
- **A1.6 (R1.6) CLARIFY.** "Restriction" here means the regular subdivision of the n collinear points on a side, induced by the heights on that side. It equals the trace of S(z) on that side, because the side is a face of conv A. Replacement for the paragraph after Prop. 2.5:
  > In this language, the four corner cells are vertices of conv A and so give vertices of every gem. The other forced vertices of Lemma 2.x are, for each side e of the grid, the lowest and the highest lifted point over e. These are vertices of the polygon conv{p_c : c ∈ e}, the face of 𝒢(S) over e.
- **A1.7 (R1.7, Q1.1)** Answers, all re-run:
  - (i) **CLARIFY.** The script (`anc/linear_squares.py`, lines 23–31) takes all (a₁,a₂,b₁,b₂,α,β) ∈ Z_n⁶, i.e. **u** = (a₁,a₂), **w** = (b₁,b₂). It keeps the bijective squares that are magic (rows, columns, both diagonals) and counts them up to D₄ only, not up to complement. I checked that each of the four families is closed under complement. Proposed sentence:
    > all (u, w, α, β) ∈ Z_n² × Z_n² × Z_n × Z_n giving a magic square, counted up to D₄ (each family is closed under complementation, which is not factored out).
  - (ii) **AGREE.** The usual sufficient conditions ask a₁, a₂, a₁±a₂ (and likewise the b's) to be units mod n. If 3 | n and a₁, a₂ are units mod 3, then one of a₁±a₂ is ≡ 0 mod 3. So one diagonal is never a full transversal, and that diagonal sum holds only for special α, β. This is why n = 9 has fewer classes (441) than n = 7 (3159). This is an explanation, not a theorem. Proposed sentence:
    > (the count is small for n = 9 because, when 3 | n, a₁ + a₂ and a₁ − a₂ cannot both be units).
  - (iii) **AGREE, with a correction to the text.** For n = 7, 9 and 11 the two classes with V = 12 are the Siamese square, f = (12,26,16), and the digit-exchanged square, f = (12,24,14); `linmin.py` labels both for each n. Replace "For n = 7 the other is" with "For n = 7, 9, 11 the other is".
  - (iv) **AGREE, adding the answer.** For n = 5 the minimum V = 11 is attained by two classes. They are complements of each other (up to D₄), both are pandiagonal, neither is associative, and both have f = (11,23,14). In Frénicle-type form the first is
    ```
     1 18 10 22 14 / 25 12 4 16 8 / 19 6 23 15 2 / 13 5 17 9 21 / 7 24 11 3 20
    ```
    with **u** = (1,2), **w** = (1,3). At n = 5 the Siamese and digit-exchanged squares have V = 12. Add one clause to Rem. 6.3:
    > for n = 5 the minimum 11 is attained by a complementary pair of pandiagonal squares, e.g. [matrix]
- **A1.8 (R1.8) AGREE.** Seeds exist and should be stated: random arrangements use `default_rng(7000n + c)` (`vertex_statistics.py`, line 80); the annealer uses seeds 1000s + n, s = 1..16 (`run_sa.sh`). The largest SEM in `vertex_stats_table.log` is 0.010 (n = 10), so "at most 0.01" is correct. Add to Q3:
  > These are Monte Carlo estimates, given to motivate the question and not claimed as results; seeds are in `anc/vertex_statistics.py` and `anc/run_sa.sh`.
- **A1.9 (R1.9, Q1.3) AGREE.** We have no primary source in the project. A web search found no arXiv or journal paper by Mino. The count is posted on Mino's own site, "The number of magic squares of order 6" (magicsquare6.net), with the correction dated 31 May 2024, and Trump's page (https://www.trump.de/magic-squares/) reports it. Proposal:
  - rename the key `trump2012enumeration` to `trump_howmany`;
  - add `@misc{mino2024order6}` for Mino's site and cite both.

  Text:
  > and was computed exactly by H. Mino in 2024, as announced on his web page [mino2024order6] and reported in [trump_howmany].

  The author should open Mino's page to confirm the title and the date before citing. (Sources consulted: [Trump, Notes on Magic Squares](https://www.trump.de/magic-squares/); OEIS A266237 via [mirror](https://backiee.wasmer.app/https_oeis_org/A266237/internal). Do not confuse this with [Ripatti, arXiv:1807.02983](https://arxiv.org/pdf/1807.02983), which counts semi-magic squares.)

### (b) Errors

- **A1.10 (R1.10) AGREE, confirmed.** `od -c` shows tab separators. CSV row "Nr. 102" is `1 8 10 15 12 13 3 6 7 2 16 9 14 11 5 4`, which is line 102 of `squares880.txt`, i.e. the paper's **#101**. The paper's #102 is line 103, `1 8 10 15 13 12 6 3 …`. Fix:
  - rename the file to `all7040_dudeney.tsv`;
  - rename the column to `line_in_squares880 (1-based; paper # = line − 1)`, or renumber to 0-based to match the paper (preferred);
  - update the README (line 5) and `geometry.tex` line 5.
- **A1.11 (R1.11) AGREE.** Replacement:
  > By the Brunn–Minkowski inequality, σ(K) ≥ 1, with equality iff K is centrally symmetric; by the Rogers–Shephard inequality [rogers1957difference], σ(K) ≤ (6 choose 3)/8 = 5/2, with equality iff K is a simplex.

  Add a Brunn–Minkowski reference: Schneider [schneider2014convex] is already in the bib.

### (c) Jargon

- **A1.12 (R1.12)** I agree with all items except one, which I partly dispute:
  - **"gem coordinates"**: AGREE. Retitle Def. 2.1 as "Definition (Lifted point set and Magic Gem)". Make its first sentence: "The Magic Gem is the lift of the grid by the heights z (the lifting used for regular subdivisions)".
  - **"centred entry"**: AGREE. Use "z_ij = s_ij − s̄, the entry minus the mean entry" (abstract, intro line 18).
  - **"deviation δ_L"**: AGREE. Replace with "the excess δ_L = Σ_{c∈L} s_c − μ_n of the line sum over the magic constant". In Sec. 3, call R_i, C_j the "row and column excesses".
  - **"vertex fraction"**: AGREE, drop it. Write "12 of the n² points" (Sec. 5 line 83, Sec. 6 line 48).
  - **"boundary non-vertex point"**: AGREE. Use "non-vertex boundary point" throughout: Sec. 2 terminology, Table 2, captions of Figs. 4, 5, 7, Lemma 4.4.
  - **"forced vertices"**: partly DISAGREE. "Vertices common to all arrangements" or "universal vertices" would be **false**. Only the four corner cells are vertices for every arrangement. The other eight forced cells depend on S, as the side extremes. Keep "forced", and define it in the statement:
    > Lemma (Forced vertices). Let S be an arrangement of order n ≥ 2. The following points are vertices of 𝒢(S); we call them the forced vertices of S: …
  - **"layers"**: AGREE. In Step 3, use "after the shear Φ the height ζ takes five values; its level sets are the lattice points of five polygons Λ_k (the level polygons)". Replace "layer" by "level" throughout Sec. 6 and Fig. 8, and say "Φ is a shear" in the first sentence of Step 3.
  - **"slack polynomials"**: AGREE. In the abstract, write "the proof reduces to a table of polynomials in m = (n−1)/2, the slacks (right-hand side minus left-hand side) of sixteen facet inequalities at sixteen points".
  - **"digit-exchanged"**: AGREE. Give the formula at its first use (Rem. 6.3 already does), and use the same name in Q5 of the Discussion, which says "digit-exchanged Siamese square".
  - **"central-symmetry defect"**: AGREE. Rename to "the difference-body ratio σ(K)". Remark title: "Difference-body ratio".
- **A1.13 (R1.13) AGREE.**
  - Table 1 and Thm 4.3: write "{±id}" and "{id, ι_g} (a half-turn)" in place of C_i and C_2.
  - Define chiral after Thm 4.3: "(chiral: having no orientation-reversing isometry)".
  - Thm 4.2 hypothesis: "arrangements with Σ z_ij x_ij = Σ z_ij y_ij = 0 (the first moments of the heights vanish), for instance semi-magic squares".
  - Sec. 3 line 16: "these are the first moments of the heights, called the dipole moment in [rogers2005multipole]". Delete "in the multipole language".
  - Fig. 4(a), CLARIFY: the checkers panel is a literal picture of a centre-of-mass statement, and I would keep it. Change the caption to "the centre of mass of each row and column lies over O", with no physics terms.
- **A1.14 (R1.14) AGREE.** Use "natural square s_ij = ni + j + 1" in Prop. 2.3, Prop. 2.5, Lemma 4.4 and the remarks after them. In Def. 1.1 add "(a permutation of 1, …, n² written into the grid)".
- **A1.15 (R1.15) AGREE.** In Sec. 5, line 53, write: "Testing all pairs of incidence graphs for isomorphism gives 352 types (Appendix)." The hash stays in the appendix.
- **A1.16 (R1.16) AGREE.** Title Prop. 5.1 "The vertex set determines the square; congruence".

### (d) Readability

- **A1.17 (R1.17) AGREE in substance, with one counter-proposal.** Your σ_h, σ_v, σ_d would collide with σ(K) in Rem. 4.6. I propose:
  - **D₄ elements:** keep r, h, v; transpose t → **d** (diagonal reflection).
  - **Thm 6.2:** v₁..v₁₂ → **q₁..q₁₂** (keep u₁..u₄); polyhedron Q → **H** ("intersection of half-spaces"); polytope P = conv{v_k} → **Π**; "images under q ↦ −q" → "images under −id".
  - **Step 1:** k−1 = nq + r → **k−1 = n k₁ + k₀** (the two base-n digits).
  - **Thm 4.2 proof:** isometry A → **ψ**.
  - **Prop. 2.5(3) proof:** bold **v** → **p_c**.
  - **Γ:** drop it. Delete line 25 of `gem.tex`; in the Fig. 6 caption write "a pair of opposite facets (orange, green)".
  - **φ(t), ⟨t⟩ and p(2+t)** are dummy variables and can stay once the transpose is d.
- **A1.18 (R1.18) AGREE.** Move Lemma 6.1 and its proof to Sec. 2, after Prop. 2.3, as "Lemma 2.4 (Forced vertices)". Sec. 6.1 then shrinks to the sentence "For the Siamese squares nothing else is a vertex." The census paragraph in Sec. 5 and the paragraph after Prop. 2.5 then refer backwards.
- **A1.19 (R1.19) AGREE, confirmed independently.** My `dist616.py` uses the anc hull routine and code separate from yours. It gives 880 vertex sets and 616 distinct sorted multisets of squared distances. New proof of Prop. 5.1(2):
  > "If" is (2.d4) and (4.complement). The sorted multiset of squared distances is a congruence invariant of the vertex set, and it takes 616 values over the 880 gems. The 880 gems form 616 complement orbits (Table 1), and gems in one orbit are congruent. Hence the congruence classes are exactly the orbits.

  The all-pairs isomorphism test can leave the appendix, or stay as a redundant check.
- **A1.20 (R1.20) AGREE.** Same fix as A1.13.
- **A1.21 (R1.21) AGREE.** I computed the Lo Shu example. Cells are labelled by their entries:
  - S(z) has maximal cells {1,2,6}, {1,3,8} and {1,2,3,4}.
  - S(−z) has maximal cells {2,7,9}, {4,8,9} and {6,7,8,9}.
  - The four vertical facets are triangles over the four sides: {2,9,4}, {2,7,6}, {6,1,8}, {4,3,8}.

  In each subdivision the quadrilateral cell contains the centre cell geometrically, but the centre is not a point of that cell, because its lift (height 0) lies above the lower face and below the upper face. This is exactly the "marked" subtlety, so it is a good example. Proposal:
  - add the motivating sentence "the gem is two regular subdivisions, by z and by −z, glued along the boundary of the grid";
  - add the sentence "cells are marked: a cell is a set of grid points, and its convex hull may contain grid points that are not in it";
  - add an Example 2.6 with the cells above. Optionally add panel (e) to Fig. 2 with S(z) and S(−z) drawn on the 3×3 grid; this is the author's choice.
- **A1.22 (R1.22) AGREE.** The table's irreducible quadratic factors are 2m²+2m±1, 4m²±2m−1/+1, 4m²+m+1, 4m²−3m+1 and m²+m+1. All have negative discriminant except 2m²+2m−1 and 4m²+2m−1, whose roots are below 1/2. Proposed text:
  > Every non-zero entry is a product of polynomials in m each of which is positive for every m ≥ 2: the linear factors visibly, and each quadratic factor has no real root or only roots below 1/2. (The appendix certifies this by the coefficients of p(2+t).)
- **A1.23 (R1.23) AGREE.** Cut line 45 of `geometry.tex`. It has no use in the paper.
- **A1.24 (R1.24) AGREE.** Line 63: replace "The vertex count is not tied to Dudeney's groups:" with "Each of Dudeney's groups with more than eight members contains gems with at least three different vertex counts and at least 20 combinatorial types…". Keep the rest of the sentence.

### (e) Overclaims

- **A1.25 (R1.25)** First half AGREE: the unlabelled census is a coarsening. Second half CLARIFY: by Prop. 2.5(1), computing the hull is computing S(±z), and Step 3 (Φ) uses exactly the invariance of S under adding affine functions and positive scaling. So the clause is accurate but cryptic. Replacement for line 134 of `gem.tex`:
  > The combinatorial types of Section 5 are a coarse invariant of the pair (S(z), S(−z)) (face lattices without cell labels). In the proof of the Siamese theorem, the shear Φ of Step 3 uses that S(±z) is unchanged when an affine function of (x, y) is subtracted from z and the result is divided by n.
- **A1.26 (R1.26) AGREE.** With A1.1–A1.3 in place, the sentence becomes true. Wording:
  > The proof is complete on paper: a three-case reduction, a table of 128 polynomial slacks, and a closing argument on 16 facets.
- **A1.27 (R1.27, Q1.4) AGREE in part; author decision flagged.** I cannot speak for the author's attachment. What the author intended, as I understand it: Thm 4.2 is the only every-order statement, and it gives meaning to Thm 4.3 and Prop. 5.1, which is why it is stated first. I agree that it is short and should be described as short. Proposal:
  - Abstract order: (1) definition; (2) the Siamese theorem; (3) the order-four census, by exact computer enumeration; (4) one sentence for Thm 4.2, "a short covariance argument shows that, for every order, …"; (5) linear squares.
  - Keep "Theorem" for 4.2, because Prop. 5.1 and Thm 4.3 cite it.
  - In "Relation to previous work" line 44, write "New are the Siamese theorem and the exact order-four census, together with a short covariance argument that settles symmetry and congruence of the point sets for every order".
- **A1.28 (R1.28) AGREE.** Abstract line 4: "we compute the gems exactly, by computer, and show…".
- **A1.29 (R1.29) AGREE.** Q3:
  > For comparison only: for N independent uniform points in a polytope the expected vertex count is Θ(ln²N) [barany1993random]. Our points are not independent (the grid is fixed and only the heights are permuted), so this is a heuristic analogy.

- **A1.Q5 (Q1.5) AGREE.** Split Thm 6.2 into two parts:
  > (a) n = 3: the gem of the Lo Shu, with vertices the 8 boundary points and f = (8,16,10) (Ex. 2.4).
  > (b) n ≥ 5: the twelve vertices, f = (12,26,16), Iso = {±id}.

  The proof's "for n = 3 … let m ≥ 2" then becomes the proof of (a).

**Status after turn 1:**
- Every reviewer point is accepted or clarified. The only dissent is the replacement name for "forced vertices" (A1.12): "universal" would be false.
- The new facts for the text are:
  - R1.7: the digit-exchanged square for n = 7, 9, 11, and the pandiagonal complementary pair with f = (11,23,14) at n = 5;
  - R1.10: CSV Nr. = paper # + 1;
  - R1.19: 616 confirmed;
  - R1.21: the Lo Shu subdivisions.
- Open for the author: the order of the abstract (A1.27), the primary source for Mino (A1.9), and the optional Lo Shu panel (A1.21).

## REVIEWER — turn 2

New scratch for this turn (`.../scratchpad/dialogue/`): `r2lib.py` is my own exact hull. Qhull only proposes a triangulated surface. Every triangle plane is then recomputed as a primitive integer plane and checked against all N points, and the surface is checked to be closed (every triangle edge in exactly two triangles). A closed surface inside the boundary sphere is the whole boundary, so this certifies the facet list. The scripts are `r2a.py` (the 880 gems), `r2b.py` (all linear magic squares of order n, my own enumeration) and `r2c.py` (Lo Shu, the n = 5 pair, σ, Ehrhart). I did not import anything from `anc/`.

### (a) Follow-up on the advocate's turn-1 answers

- **R2.1 (A1.1) ACCEPT.** I checked the three cases line by line.
  - A < 0 gives x ≤ y−m−1 ≤ −1, so B = A + x < 0. Since B ≥ −2m > −n, ⌊B/n⌋ = −1.
  - A ≥ n gives B ≥ n+1 and B ≤ 4m < 2n.
  - The middle case is correct.
  - The vertices of the three regions are lattice points: (−m,1), (−1,m), (−m,m); (−m,1−m), (−m,0), (−1,m−1); (−m,−m), (0,m), (m,m), (0,−m). Each region therefore equals the convex hull of its lattice points.

  One simplification. The "conversely" sentence can be one line: "If |y−2x| ≤ m, then A < 0 is impossible, since it would force B < 0, i.e. y ≥ 2x+m+1; likewise A ≥ n would force y ≤ 2x−m−1." This avoids the separate argument about y > x+m.
- **R2.2 (A1.2) ACCEPT.** The trapezoid and the position of v₄, v₃ relative to the line v₅v₁ are correct; (m+1)²/m < 2m+2 holds iff m > 1. I also checked that the non-vertex point u₁ = (−m,1−m,1), which has slack 0 in (3), lies inside the quadrilateral. At y = 1−m the edge v₅v₄ has height 1/m and the edge v₃v₅ has height 2, and u₁ has height 1. This is not needed for the proof, because P = Q settles it, but a reader who sees the bold 0 in the u₁ row will ask. Add a half-sentence: "(u₁ lies on plane (3) inside this quadrilateral)".
- **R2.3 (A1.3) ACCEPT.** The "plane through" list agrees with the zero pattern of Table 3.
- **R2.4 (A1.4) ACCEPT.** The concavity argument is right: U−L is concave, non-negative, and positive at one interior point, hence positive on the interior. I would add one clause that the reader needs for "determined by": the vertices of a lower facet are the lifts of the vertices of the polygon conv(cell), because an affine map from a non-vertical plane to the floor is a bijection. So marked cells determine the vertex–facet incidences.
- **R2.5 (A1.5) ACCEPT.**
- **R2.6 (A1.6) ACCEPT.**
- **R2.7 (A1.7) Re-run independently.** My own enumeration covers all (a₁,a₂,b₁,b₂,α,β) ∈ Z_n⁶ with unit determinant, magic, counted up to D₄. It reproduces 184 / 3159 / 441 classes for n = 5, 7, 9 and the vertex ranges [11,18], [12,25], [12,31]. For n = 7 and 9 the two V = 12 classes are exactly the Siamese square, with (12,26,16), and the digit-exchanged square, with (12,24,14). Both are self-complementary. For n = 11 I also get 89,125 classes, the range [12,36], and the same two classes at V = 12. Rem. 6.3 and the abstract's 18/25/31/36 are confirmed. Two corrections to the advocate's text:
  - **(iv)** The two n = 5 classes with V = 11 are complements of each other, both are pandiagonal and neither is associative: confirmed, with f = (11,23,14). But the printed Frénicle-form matrix is **not** given by u = (1,2), w = (1,3). Those are the parameters of a D₄-image. The printed matrix is 5⟨4i+3j⟩ + ⟨4i+2j⟩ + 1, i.e. **u = (−1,−2), w = (−1,2), α = β = 0**. Print either the matrix in the parameters' orientation or the correct parameters, not a mixture.
  - **(ii)** The proposed causal sentence is not convincing. The Siamese square itself has a₁ − a₂ = 0, because its leading digit is constant on the anti-diagonal, for every n. So "a₁ ± a₂ units" is not what separates n = 9 from n = 7. Either analyse it or state the counts without a reason. I prefer: "we have not analysed why the count for n = 9 is small".
- **R2.8 (A1.7(iii) and Rem. 6.3) New gap: "it is magic for every odd n" has no proof.** Rows, columns and the anti-diagonal are easy. The main diagonal is not when 3 | n, because the leading digit ⟨3i−2m⟩ is then not a permutation of Z_n. Here is a proof the author can print. If 3 | n, then m ≡ 1 (mod 3), so ⟨3i−2m⟩ runs three times over the residues ≡ 1 (mod 3) in [0, n). Their sum is 3·(n/3)·(n−1)/2 = n(n−1)/2, the same as for a permutation. On the anti-diagonal the trailing digit is the constant m, which contributes n·m = n(n−1)/2, again the same. The same three lines prove that the Siamese square is magic, so Step 1 then needs no outside citation for magicness. I checked n = 3, …, 39 numerically.
- **R2.9 (A1.8) ACCEPT.** The seeds are as stated (`7000n + c`; `1000s + n`). The largest SEM in `vertex_stats_table.log` is 0.010. The ratio E[V]/ln²N runs from 8.218/ln²9 = 1.70 to 27.909/ln²100 = 1.32: confirmed. New, minor: the same log shows an annealed **order-5 magic square with V = 10** ("min 10"), below the Siamese 12 and the linear minimum 11. Say this in Rem. 6.3 or Q3. Otherwise a reader of Thm 6.2 may assume the Siamese gem is vertex-minimal at order five.
- **R2.10 (A1.9) ACCEPT conditionally.** The citation is acceptable as a web announcement once the author has opened the page and checked the title and date. Do not state the count itself unless it is copied from that page.
- **R2.11 (A1.10) ACCEPT, confirmed.** Line 102 of `squares880.txt` equals CSV `Nr. 102`, and line 103 is `1 8 10 15 13 12 6 3 …`. With `delimiter='\t'` I mapped all 7040 CSV rows to the 880 classes. Each class gets exactly one group label.
- **R2.12 (A1.11) ACCEPT.** Brunn–Minkowski gives vol(½K + ½(−K))^{1/3} ≥ vol(K)^{1/3}, with equality iff K is a translate of −K. Cite the theorem in Schneider by number, not just the book.
- **R2.13 (A1.12, "forced") ACCEPT the advocate's dissent.** I recounted for n = 4: the only cells that are vertices of all 880 gems are the four corners, and the only entries that always label a vertex are 1 and 16. So "universal" would be false, and "forced vertices of S", defined in the lemma statement, is right. I also confirmed that the forced sets have 4 to 13 points (counts 8, 8, 104, 16, 332, 164, 132, 36, 72, 8 for sizes 4..13), and that in every gem they are vertices.
- **R2.14 (A1.17) ACCEPT with two amendments.**
  - "d" for the transpose: D₄ has two diagonal reflections, so write "d, the reflection in the main diagonal i = j".
  - The proposal keeps u₁..u₄ for the four non-vertex polygon vertices. That clashes with **u**, **w** of Rem. 6.3 and with u, w in the proof of Prop. 2.3. Better: number all sixteen polygon vertices q₁..q₁₆, with q₁..q₁₂ the images of the forced vertices and q₁₃..q₁₆ the rest. Table 3 then has one index.
- **R2.15 (A1.19) ACCEPT.** Pigeonhole: 616 values of an invariant that is constant on each of 616 orbits, so the classes are exactly the orbits. This is a better proof than the all-pairs graph test.
- **R2.16 (A1.21) ACCEPT, confirmed.** My hull gives S(z) = {1,2,6}, {1,3,8}, {1,2,3,4}; S(−z) = {2,7,9}, {4,8,9}, {6,7,8,9}; vertical facets {2,4,9}, {2,6,7}, {1,6,8}, {3,4,8}. The plane of {1,2,3,4} is z = −x−y−3, which is −3 < 0 at the centre, so the centre cell is unused. I recommend the Fig. 2 panel; a picture of two subdivisions of a 3×3 grid costs little.
- **R2.17 (A1.22) ACCEPT, but fix the list.** "4m²±2m−1/+1" is garbled. The irreducible quadratic factors in Table 3 are exactly 2m²+2m+1, 2m²+2m−1, 4m²+2m−1, 4m²−2m+1, 4m²+m+1, 4m²−3m+1 and m²+m+1. A test a reader can do faster than discriminants: each is positive at m = 1 and increasing for m ≥ 1 (vertex at m ≤ 3/8).
- **R2.18 (A1.24) ACCEPT, confirmed.** By group, the vertex counts and type counts are: I {11..15}, 20 types; II {10..16}, 22; III {10,12,14,16}, 30; IV {10..14}, 43; V {10..15}, 48; VI {8,10,12,14,16}, 126; VII {11..15}, 28; VIII {8..13}, 20; IX {9..14}, 25; X {12,13,14}, 26. The minimum of 20 types is attained by groups I and VIII; X has exactly three vertex counts. The 8-vertex gems are VI: 3, VIII: 4.
- **R2.19 (A1.25, A1.26, A1.27, A1.28, A1.29, A1.Q5) ACCEPT.** For A1.Q5, part (a) can also state Iso = {±id} for n = 3: the vertex set is P_S∖{0}, its centroid is 0, so Iso(vert) ⊆ Iso(P_S) = {±id}.

### (b) Second pass: computer-assisted statements I had not checked in turn 1

All reproduced with my own code unless marked otherwise.

- **V2.1** Sec. 2.1: vertical facets 856/20/4. There are **417** regular subdivisions up to D₄; the count is the same whether or not complements are included, as it must be. **548** of the S(z) are triangulations, i.e. every lower cell has exactly 3 points.
- **V2.2** Rem. 4.5: among the 304 h/v-self-complementary squares (208 with h, 96 with v), 282 / 18 / 4 have 2 / 1 / 0 non-arithmetic rows (for h) or columns (for v), i.e. fixed facets.
- **V2.3** Sec. 5: **352 combinatorial types**, with the size distribution exactly as printed, 93 singletons (all self-complementary), and 201 pairs (177 mirror pairs, 24 pairs of self-complementary squares). Types are unions of complement orbits. The largest type has 32 members and f = (10,22,14), with 12 triangles and 2 quadrilaterals.
- **V2.4** Sec. 5: 48 pandiagonal squares, V ∈ {11..15} with counts 10/20/12/4/2, V° ∈ {1..4}, none associative. Entry 2 is a non-vertex boundary point in exactly 8 gems (#448, 593, 596, 600, 613, 651, 655, 665).
- **V2.5** Rem. 4.6 (floating point only): σ = 1 for exactly 48 gems; the other values have min 1.0383104 = 1057/1018 and max 1.6477273 = 145/88.
- **V2.6** Sec. 5: **554** distinct Ehrhart polynomials. I determined each by (vol, L(1), L(2)), counting lattice points of G + (½,½,½) and of its double directly.

### (c) New points

- **R2.20 Appendix, "Exact hulls": the certification described is not the one run for every computation.** The appendix says each hull is certified by "every edge of every facet polygon lies in exactly two facets". In `anc/`, that closure check is in `verify_revision.py` block F and runs only on the 880 order-four hulls. The shared routine `gem_geometry.exact_hull`, which `linear_squares.py` uses for Rem. 6.3 and for the abstract's 18/25/31/36, checks only that the planes are valid, that V−E+F = 2, and that its vertex set agrees with Qhull's. Neither check certifies that no facet is missing. (Euler's formula can hold for a wrong complex, and agreeing with Qhull is not exactness.) The numbers are right (R2.7), but the appendix should either say which certification applies to which computation or move the closure check into `exact_hull`. A one-line alternative is the closed-triangulation check I used (`r2lib.py`).
- **R2.21 Appendix, "Combinatorial types": say "isomorphisms mapping vertices to vertices".** The code does this (`node_match` on `kind`); the text does not. Otherwise a type and its dual type, for a gem with V = F such as (8,14,8), could be merged. In the 880 it makes no difference: I get 352 types either way. The definition should still be the standard one.
- **R2.22 Intro, Results item 3 and abstract, last sentence: "the largest vertex count grows with n" / "so bounded vertex counts are not a feature of linear constructions in general".** Four values (18, 25, 31, 36) do not show growth or unboundedness. Write: "for n = 5, 7, 9, 11 the largest vertex count over all linear magic squares is 18, 25, 31, 36; in particular other linear squares have more than twelve vertices". The question of unboundedness is already Q5.
- **R2.23 Thm 4.3: "the 880 essentially different magic squares".** This is recreational usage. Write "the 880 D₄-classes" (the paper's own term elsewhere); the same applies to Sec. 5 and Q2 ("275,305,224 essentially different").
- **R2.24 Unused statements.** No later text cites Cor. 3.1 (Loly), Lemma 4.4 (parity), Rem. 4.5, Rem. 4.6 or Ex. 2.4 (`\label`s never referenced). Ex. 2.4 should stay as the running example, and Lemma 4.4 and Rem. 4.5 are short and correct. But Cor. 3.1 is a known result, re-proved and then never used. It would be better as one sentence with the citation inside Sec. 3.
- **R2.25 Is Sec. 3 needed as a section?** Its only role in the logic is Lemma 3.2: the covariance is diag(a_n, a_n, b_n) when the first moments vanish. Thm 4.2 rests on that alone. Two figures (Figs. 4 and 5) illustrate a one-line identity and the mixed moment, which nothing uses. Proposal:
  - make Sec. 3 a short subsection opening Sec. 4, containing (3.1) and Lemma 3.2;
  - keep Fig. 4(a), which shows "each row's centre of mass is over O";
  - cut Fig. 5;
  - reduce the mixed-moment paragraph to one sentence or drop it.

  This brings the main theorem a page closer to the definition.
- **R2.26 The intro does not say what the convex hull adds to the point set.** Readability for a newcomer: the intro motivates the point set (vectors cancel along lines) but not the hull. The paper's three main results all answer one question: **how much of the square can the hull see?**
  - Thm 4.3: the hull has no symmetry the square lacks.
  - Prop. 5.1: at order four the vertices alone determine the square.
  - Thm 6.2: for the Siamese squares the hull sees only 12 of the n² entries, the minimum the boundary allows.

  Say this in two sentences at the start of "Results". It is the main line of argument, and at present the reader has to reconstruct it.
- **R2.27 Abstract readability.** The abstract is one paragraph of five long sentences, with symbols (a_n, b_n, f-vectors, m) that are defined only in the body. After the reordering agreed in A1.27:
  - drop a_n ≠ b_n (say "the covariance matrix is diagonal with two equal entries");
  - drop m (say "a table of polynomial inequalities in n");
  - keep only the counts 880, 48/304/528, 616, 352 and 12/(12,26,16).
- **R2.28 Step 4 sentence: "Hence each of the sixteen planes meets P ⊆ Q in a polygon, which is therefore a facet of P."** "Polygon" should be "2-dimensional face". The reason is that each plane contains three non-collinear v_k from the list, which is visible from the coordinates but should be said. A reader of a computer-assisted proof checks exactly this kind of step.
- **R2.29 Prop. 2.5(1): "(1) is the definition of S(±z)".** For the upper facets this needs one more word: the upper faces of the lift by z are the reflections of the lower faces of the lift by −z (stated just before the proposition). Write "(1) is the definition of S(z) and, after reflecting in z = 0, of S(−z)".

### (d) Readability verdict at this stage

The mathematics holds up under a second pass; I found no error in any theorem. The census is reproducible from independent code, including the parts I skipped in turn 1 (types, subdivisions, Ehrhart, σ, the linear squares).

The remaining work is presentation:
- R2.26: say the main question once;
- R2.25: shorten Sec. 3;
- A1.18: move the forced-vertex lemma forward;
- R2.20, R2.21: make the appendix match what the code certifies;
- R1.1–R1.3: print the two short arguments.

No section is unnecessary except, arguably, the standalone status of Sec. 3.

### Questions for the advocate

- **Q2.1** (R2.20) Will `exact_hull` get the closure check, or will the appendix be reworded? Which certification did the Siamese cross-check for n ≤ 41 and the n = 5..31 digit-exchanged check use?
- **Q2.2** (R2.7(iv)) Please give the corrected parameters, or the orientation, for the printed n = 5 square.
- **Q2.3** (R2.25) Does the author object to merging Sec. 3 into Sec. 4 and cutting Fig. 5?
- **Q2.4** (R2.9) Is the V = 10 order-five annealed square available (the log says the sampled squares are not included)? If so, print it in Q3. It is a better example than a bare minimum.

## ADVOCATE — turn 2

New checks for this turn are in `.../scratchpad/adv2/`. They use `anc/gem_geometry.exact_hull` together with my own closure test: every edge of every facet polygon must lie in exactly two facets (the block-F test from `verify_revision.py`, copied out).
- `cert.py` applies the closure test to the Siamese squares n = 3..41, the digit-exchanged squares n = 5..31, and every linear magic square class for n = 5, 7, 9.
- `lin5.py` checks the n = 5 parameters, and that both closed forms are magic for n = 3..39.
- `v10.py` and `v10b.py` scan the saved order-5 annealer output for gems with 10 vertices.

### (a) Replies to the reviewer's follow-ups

- **A2.1 (R2.1) AGREE.** I take your one-line converse. Step 3 now reads: the three cases of A1.1, then
  > Conversely, if |y−2x| ≤ m then A < 0 is impossible, since it would force B < 0, i.e. y ≥ 2x+m+1; likewise A ≥ n would force y ≤ 2x−m−1.
- **A2.2 (R2.2) AGREE.** Add after the cyclic-order sentence of A1.2:
  > (the non-vertex point q₁₃ (formerly u₁) = (−m, 1−m, 1) lies on plane (3) inside this quadrilateral).
- **A2.3 (R2.3) Nothing to add.**
- **A2.4 (R2.4) AGREE.** Append to the A1.4 text:
  > A lower facet projects bijectively onto its cell (the facet plane is not vertical), so its vertices are the lifts of the vertices of the polygon conv(cell). Hence the marked cells of 𝒮(z) and 𝒮(−z), together with the two boundary chains over each side, determine every vertex–facet incidence.
- **A2.5, A2.6 (R2.5, R2.6) Nothing to add.**
- **A2.7 (R2.7) AGREE on both corrections.**
  - **(iv), answering Q2.2.** I recomputed the printed matrix `1 18 10 22 14 / 25 12 4 16 8 / 19 6 23 15 2 / 13 5 17 9 21 / 7 24 11 3 20`. It is 5⟨4i+3j⟩ + ⟨4i+2j⟩ + 1, i.e. **u = (−1,−2), w = (−1,2), α = β = 0**, as you say. It is magic and pandiagonal, and its hull has f = (11,23,14) and passes the closure test (`lin5.py`). My turn-1 parameters u = (1,2), w = (1,3) belonged to a D₄-image, and I withdraw them. Text for Rem. 6.3:
    > for n = 5 the minimum 11 is attained by two classes, complements of each other, both pandiagonal and not associative, with f = (11,23,14); one is s = 5⟨4i+3j⟩+⟨4i+2j⟩+1 =
    > [matrix as above].
  - **(ii)** Your counterexample is decisive. The Siamese square has u = (1,1), so a₁ − a₂ = 0 for every n, and my units argument cannot be what separates n = 9 from n = 7. I withdraw the causal sentence. Text: "(we have not analysed why the count for n = 9 is small)". An honest alternative is to give the counts and say nothing.
  - Reproduction: `cert.py` re-enumerates n = 5, 7, 9 and gets 184 / 3159 / 441 classes with V ∈ [11,18], [12,25], [12,31]. With your n = 11 run, every number in Rem. 6.3 has been reproduced twice.
- **A2.8 (R2.8) AGREE: a real gap, and your proof is right.** I checked it. If 3 | n then n = 2m+1 ≡ 0 (mod 3), so m ≡ 1 and 3i − 2m ≡ −2 ≡ 1 (mod 3). The leading digit on the main diagonal therefore runs three times over {1, 4, …, n−2}, whose mean is (n−1)/2, so the diagonal sum is the magic sum. If 3 ∤ n, then ⟨3i−2m⟩ is a permutation. The other lines are permutations or constants: rows, columns, the trailing digit ⟨2i−m⟩ on the diagonal, the leading digit ⟨2m−i⟩ on the anti-diagonal, and the constant trailing digit ⟨m⟩ on the anti-diagonal. Bijectivity: det[(1,2);(1,1)] = −1 is a unit. The Siamese square is the same computation with the two digits swapped. `lin5.py` confirms both squares are magic for n = 3..39. Proposal:
  - Add **Lemma 6.0 (Two linear squares).** "For odd n = 2m+1, both s(i,j) = n⟨i+j−m⟩ + ⟨i+2j−2m⟩ + 1 (Siamese) and s′(i,j) = n⟨i+2j−2m⟩ + ⟨i+j−m⟩ + 1 (digit-exchanged) are magic squares." Use the proof above.
  - Step 1 then needs [andrews1960magic] only for the identification with de la Loubère's construction, not for magicness.
  - Rem. 6.3 drops "it is magic for every odd n" and cites the lemma.
- **A2.9 (R2.9) AGREE. Answer to Q2.4: yes, the squares exist.** The annealer output is not in `anc/`, but it is saved in `Analysis/gem_explorations/ehrhart_largen/sa_out/sa_n5_*.txt`: 16 files, 60,000 rows, seeds 1000s + 5, all magic. Three provenance points:
  - `vertex_statistics.py` (magic mode) reduces the rows to D₄-classes. Those are the **59,993** in the log, so the log's "59993 squares" means 59,993 distinct D₄-classes. The reviewer's "min 10" is therefore from this run.
  - Exact hulls, closure-certified, give **15 D₄-classes with V = 10**. One has f = (10,23,15); the other 14 have (10,22,14). None is associative or self-complementary, and no two are complements of each other.
  - Proposed example for Q3 / Rem. 6.3 (Frénicle form), f = (10,22,14), volume 845/3, 8 interior points:
    ```
     1 19 15 13 17
    23  5 14 20  3
    10 21 12  4 18
    24  9  8 22  2
     7 11 16  6 25
    ```
  - Text (Rem. 6.3, end):
    > The Siamese gem is not vertex-minimal at order five: annealed sampling (Sec. 7, Q3) found magic squares of order 5 whose gems have 10 vertices, e.g. [matrix], with f = (10,22,14).
  - In the stats sentence of Q3, change "59,993 squares" (if printed) and the log label to "59,993 distinct D₄-classes". Copy the 15 squares into `anc/` (e.g. `sa_n5_V10.txt`) so the example can be reproduced without the raw output.
- **A2.10 (R2.10) AGREE.** The author must open Mino's page before submission and quote no number that is not on it. Flagged as an author action.
- **A2.11 (R2.11) Nothing to add.**
- **A2.12 (R2.12) AGREE.** Cite "[schneider2014convex, Thm 7.1.1]" (Brunn–Minkowski, 2nd ed.). The author should confirm the theorem number against the edition in the bib. Equality: K and −K are homothetic with equal volume, hence translates.
- **A2.13 (R2.13) Nothing to add.** Thanks for the forced-set size counts. They could go in one sentence after Lemma 2.4 ("at order four the forced sets have 4 to 13 points"), but this is optional.
- **A2.14 (R2.14) AGREE with both amendments.**
  - The transpose becomes "d, the reflection in the main diagonal i = j".
  - In Thm 6.2 all sixteen polygon vertices become q₁..q₁₆: q₁..q₁₂ = old v₁..v₁₂ (forced) and q₁₃..q₁₆ = old u₁..u₄.
  - `anc/siamese_slacks.py` (the `names` dict and `ORDER`) must be updated so that the generated Table 3 matches.
- **A2.15, A2.16 (R2.15, R2.16) AGREE.** Adding the Fig. 2 panel (S(z), S(−z) of the Lo Shu) is now in the list.
- **A2.17 (R2.17) AGREE.** My list was garbled. Your seven quadratics are right. I checked your test: each is positive at m = 1, and each has its vertex at m ≤ 3/8 (4m²−3m+1 has the largest, 3/8). Use the test in the text, since it is quicker than discriminants.
- **A2.18 (R2.18) AGREE.** Use your data: "each group with more than eight members contains gems with at least three vertex counts and at least 20 combinatorial types".
- **A2.19 (R2.19) AGREE**, including Iso = {±id} for n = 3. An isometry of the vertex set fixes its centroid 0, so it extends to P_S = vert ∪ {0}. Thm 4.2 gives Iso(P_S) = {±id}, because the Lo Shu is associative, and −id preserves the vertex set.

### (b) On V2.1–V2.6

Accepted. V2.1 adds two facts not in the paper: 417 regular subdivisions up to D₄, of which 548 S(z) are triangulations. The second is a count over gems, not over subdivisions; please say which. Include them only if Sec. 2.1 has a use for them. I suggest it does not.

### (c) New points

- **A2.20 (R2.20, Q2.1) AGREE. Both fixes.**
  - Q2.1 answer: the Siamese cross-check in `verify_revision.py` block I (n = 3..41), the digit-exchanged check (n = 5..31) and Rem. 6.3 all used `exact_hull`, i.e. valid planes + V−E+F = 2 + agreement with Qhull, **without** closure. The n = 5..41 loop in `siamese_slacks.py` is weaker still: it checks only that every reduced lattice point satisfies the 16 inequalities.
  - None of this is used in the proof of Thm 6.2.
  - I have now run the closure test on all of them except linear n = 11, which you certified independently. **0 failures** (`cert.py`).
  - Fix (code): move the block-F closure test into `exact_hull`, so every caller is certified, and re-run `linear_squares.py`, `verify_revision.py` and `run_geometry_880.py`.
  - Fix (text): appendix "Exact hulls": keep the three-part certificate and add "This certificate is applied to every hull in the paper (order four, Siamese, digit-exchanged and linear squares)". Q3's sampling paragraph already says it uses floating point.
- **A2.21 (R2.21) AGREE.** Appendix: "Combinatorial types are the isomorphism classes of the vertex–facet incidence graphs, under isomorphisms that map vertices to vertices and facets to facets (so a polytope and its dual are not identified)".
- **A2.22 (R2.22) AGREE.**
  - Abstract, last sentence: "Over all linear magic squares of orders 5, 7, 9, 11 the largest vertex count is 18, 25, 31, 36, so other linear squares have more than twelve vertices."
  - Intro item 3: "Other linear magic squares have more vertices: up to 18, 25, 31, 36 for n = 5, 7, 9, 11 (Rem. 6.3)."
  - The A2.9 fact also cuts the other way (10 < 12 at n = 5), and the intro could say so in one clause.
- **A2.23 (R2.23) AGREE.**
  - Thm 4.3: "For each of the 880 D₄-classes of magic squares of order 4".
  - Sec. 5 line 6 and Q2: "275,305,224 magic squares of order five up to D₄".
  - Define "D₄-class" once, at the first count in Sec. 1: "880 magic squares of order four up to rotation and reflection (D₄-classes)".
- **A2.24 (R2.24) AGREE.**
  - Cor. 3.1 becomes one sentence inside the moment paragraph: "With φ(t) = t² this gives Loly's invariant [loly2004invariance]: Σ s_ij(x_ij²+y_ij²) = n²(n⁴−1)/12 for every semi-magic square."
  - Keep Ex. 2.4, Lemma 4.4 and Rem. 4.5–4.6, and reference Ex. 2.4 from the new Lo Shu subdivision example (A1.21).
- **A2.25 (R2.25, Q2.3) AGREE, as the advocate. The final decision is the author's, but I see nothing the author's intent needs from a standalone Sec. 3.** Plan:
  - Rename Sec. 4 "Moments, symmetry and congruence". §4.1 "First and second moments" holds (3.1), the Loly sentence and Lemma 3.2.
  - Keep Fig. 4(a) with the caption of A1.13.
  - Cut Fig. 4(b) and Fig. 5. Both illustrate only the mixed moment Σz·xy, which nothing uses.
  - Replace the mixed-moment paragraph with: "The mixed moment Σ z·xy is not forced by the line conditions; it vanishes for associative squares (z is odd under −id) but not in general."
  - Drop the "48 values / 56 classes" numbers. V0.7 confirmed them, but they serve nothing.
  - Delete `fig_weighted_sum.pdf` and its script from the build list, keeping the script in `anc/` only if Fig. 4 needs it.
- **A2.26 (R2.26) AGREE. This is the best readability point of the review.** New first paragraph of "Results", before the list:
  > The point set determines the square, but its convex hull keeps only the extreme points. All three results below ask how much of the square the hull still sees. For every order, the point set has no symmetry the square lacks (item 1). At order four, the hull has no symmetry the point set lacks, and its vertices alone determine the square (item 2). For the Siamese squares, the hull sees only the twelve entries that the boundary of the grid forces, for every odd order (item 3).
- **A2.27 (R2.27) AGREE.** Draft abstract, in the order agreed in A1.27:
  > To an n×n magic square we attach the n² points (x, y, z) in ℝ³, where (x, y) is the position of a cell, measured from the centre of the grid, and z is its entry minus the mean entry; their convex hull is the *Magic Gem*. Its lower and upper faces are the regular subdivisions of the grid induced by the entries and by their negatives. For the Siamese (de la Loubère) square of every odd order n ≥ 5 we prove that the gem has exactly twelve vertices, the minimum the boundary of the grid allows (the four corners and, on each side, the cells of the smallest and largest entry), with f-vector (12,26,16) and isometry group {±id}; the proof reduces to checking the signs of a table of polynomials in n. For the 880 magic squares of order four we compute all gems exactly, by computer: no gem has an isometry that its point set lacks, 48 gems are centrally symmetric, 304 have a single half-turn symmetry and 528 have none, the vertex set determines the square, and the gems form 616 congruence classes and 352 combinatorial types. A short covariance argument shows that, for semi-magic squares of every order, the point set has a non-trivial isometry exactly when the square equals its complement up to rotation and reflection. Other linear magic squares have more vertices: up to 18, 25, 31 and 36 for orders 5, 7, 9 and 11.

  Check against the text: the "minimum the boundary allows" claim is justified by Lemma 2.4 together with "the twelve are distinct for the Siamese square". For an arbitrary square the forced set can be smaller (4 points at n = 4, R2.13, and V = 10 at n = 5, A2.9). So "minimum" is **wrong** as a general claim. The safe wording is "exactly the twelve vertices that the boundary of the grid forces". I have used that in the revision list (item 33), and I flag it so that this wording is not introduced elsewhere.
- **A2.28 (R2.28) AGREE.** Replace with:
  > Each of the sixteen planes contains at least three non-collinear points q_k of its list (Table 3, zero entries), so it meets Π ⊆ H in a 2-dimensional face, i.e. a facet of Π.
- **A2.29 (R2.29) AGREE.** Use your wording verbatim.

### Draft agreed revision list

Status labels: [E] error or gap, [P] proof completion, [C] clarity, [J] jargon, [N] notation, [O] overclaim, [S] structure, [X] supplementary/code, [T] typo/attribution.

**Proofs and errors**
1. [P] Thm 6.2 Step 3: replace "a case check of the two floors shows…" with the three-case argument of A1.1 plus the one-line converse of A2.1. (R1.1, R2.1)
2. [P] Thm 6.2 Step 4: replace the m ≤ 60 convexity check with the trapezoid / below-the-line argument of A1.2, plus "(q₁₃ lies on plane (3) inside this quadrilateral)". Delete the m ≤ 60 loop in `siamese_slacks.py` (l. 97–106) and the clause "the convexity of the quadrilaterals for m ≤ 60" in appendix l. 21. (R1.2, R2.2)
3. [P] Step 4: label each inequality "plane through q_a q_b q_c": (1) q₁q₂q₃, (2) q₁q₂q₈, (3) q₁q₃q₅, (4) q₁q₄q₇, (5) q₂q₃q₆, (6) q₂q₆q₉, (7) q₂q₈q₉, (8) q₃q₅q₆. (R1.3)
4. [P] Step 4 positivity sentence: "Every non-zero entry is a product of linear factors positive for m ≥ 1 and the quadratics 2m²+2m±1, 4m²+2m−1, 4m²−2m+1, 4m²+m+1, 4m²−3m+1, m²+m+1, each positive at m = 1 with its minimum at m ≤ 3/8, hence positive for m ≥ 1." (R1.22, R2.17)
5. [P] Step 4: "polygon, which is therefore a facet" → A2.28 wording. (R2.28)
6. [P] Prop. 2.5(4) proof: add the concavity argument (A1.4) and the bijective-projection clause (A2.4). (R1.4, R2.4)
7. [P] Prop. 2.5(1) proof: "(1) is the definition of 𝒮(z) and, after reflecting in z = 0, of 𝒮(−z)." (R2.29)
8. [P] Rem. 4.5: add the case ι_h(a) = −a, b = 0, excluded because 0 is interior (A1.5). (R1.5)
9. [E] New Lemma 6.0 (Siamese and digit-exchanged squares are magic for every odd n), with the 3 | n argument of A2.8. Step 1 cites it, and Rem. 6.3 drops the unproved "it is magic for every odd n". (R2.8)
10. [E] Rem. 6.3: "For n = 7 the other is" → "For n = 7, 9, 11 the other is". (R1.7(iii))
11. [E] Rem. 6.3: add the n = 5 minimum: two complementary pandiagonal, non-associative classes with f = (11,23,14), e.g. s = 5⟨4i+3j⟩+⟨4i+2j⟩+1 (u = (−1,−2), w = (−1,2)), with the matrix printed. (R1.7(iv), R2.7)
12. [E] Rem. 6.3: state the enumeration precisely: "all (u, w, α, β) ∈ ℤ_n²×ℤ_n²×ℤ_n×ℤ_n giving a magic square, counted up to D₄ (complements not identified)". For n = 9 write "(we have not analysed why the count for n = 9 is small)", with no causal claim. (R1.7(i,ii), R2.7(ii))
13. [E] Rem. 6.3 or Q3: add the order-five V = 10 example of A2.9; the Siamese gem is not vertex-minimal at n = 5. Add the 15 squares to `anc/`. (R2.9, Q2.4)
14. [T] Rem. 4.6: lower bound by Brunn–Minkowski [schneider2014convex, Thm 7.1.1, number to confirm], upper bound by Rogers–Shephard; rename to "difference-body ratio σ(K)". (R1.11, R2.12, R1.12)
15. [P] Prop. 5.1(2): replace the all-pairs graph test with the pigeonhole proof via the 616 sorted squared-distance multisets (A1.19). Keep the graph test in the appendix as a redundant check. (R1.19, R2.15)
16. [P] Thm 6.2 statement: split into (a) n = 3: Lo Shu, f = (8,16,10), Iso = {±id} (A2.19 argument); (b) n ≥ 5. (Q1.5, R2.19)

**Structure**
17. [S] Move Lemma 6.1 (forced vertices) to Sec. 2 as Lemma 2.4, after Prop. 2.3. Define "forced vertices of S" in its statement and keep the name. Sec. 6.1 then says only "for the Siamese squares nothing else is a vertex". (R1.18, A1.12, R2.13)
18. [S] Merge Sec. 3 into Sec. 4 as §4.1 "First and second moments". Cor. 3.1 becomes one cited sentence. Cut Fig. 4(b) and Fig. 5, and shorten the mixed-moment paragraph to one sentence (A2.25). Author to confirm. (R2.24, R2.25)
19. [S] Intro "Results": add the "how much of the square does the hull see" paragraph (A2.26). (R2.26)
20. [S] Abstract: rewrite in the order Siamese → census → covariance → linear, with no a_n, b_n, m (draft in A2.27, with the "exactly the twelve forced" wording, not "minimum"). Author to confirm the order. (R1.27, R1.28, R2.27)
21. [S] Relation to previous work: "New are the Siamese theorem and the exact order-four census, together with a short covariance argument that settles symmetry and congruence of the point sets for every order". (R1.27)
22. [S] Sec. 2.1: add the motivating sentence ("two regular subdivisions, by z and −z, glued along the boundary"), the definition of marked cells, and Example 2.6 (Lo Shu: 𝒮(z) = {1,2,6}, {1,3,8}, {1,2,3,4}; 𝒮(−z) = {2,7,9}, {4,8,9}, {6,7,8,9}; vertical facets {2,4,9}, {2,6,7}, {1,6,8}, {3,4,8}; the centre is unmarked). Add Fig. 2 panel (e). (R1.21, R2.16)
23. [C] Paragraph after Prop. 2.5: replace "restrictions … to that edge" with the A1.6 wording. (R1.6)
24. [O] gem.tex l. 134: replace with the A1.25 text (census = coarse invariant; Φ uses invariance of 𝒮 under affine changes). (R1.25)
25. [O] Intro item 3: "The proof is complete on paper: a three-case reduction, a table of 128 polynomial slacks, and a closing argument on 16 facets"; drop "the largest vertex count grows with n" (A2.22). (R1.26, R2.22)
26. [O] Abstract, last sentence: per A2.22. (R2.22)
27. [O] Q3: "Monte Carlo estimates, not claimed as results; seeds 7000n + c (`vertex_statistics.py`) and 1000s + n (`run_sa.sh`)". Bárány's Θ(ln² N) is labelled "a heuristic analogy (our points are not independent)". Counts are labelled "distinct D₄-classes". (R1.8, R1.29, R2.9)
28. [T] Mino: "computed exactly by H. Mino in 2024, as announced on his web page [mino2024order6] and reported in [trump_howmany]"; rename the bib key. The author must check the page first. (R1.9, R2.10)

**Jargon and notation**
29. [J] Def. 2.1 title "Lifted point set and Magic Gem"; first sentence "the lift of the grid by the heights z". (R1.12)
30. [J] "centred entry" → "entry minus the mean entry"; "deviation" → "excess δ_L of the line sum over the magic constant", R_i, C_j "row/column excesses"; drop "vertex fraction"; "boundary non-vertex" → "non-vertex boundary point" everywhere; "layer(s)" → "level set / level polygon", and say "Φ is a shear"; define "slack = right-hand side minus left-hand side" at first use; give the digit-exchanged formula at first use. (R1.12)
31. [J] C_i, C_2 → {±id}, {id, ι_g} (half-turn); define "chiral"; "dipole moment" only as an attributed aside; Thm 4.2 hypothesis "Σz x = Σz y = 0 (first moments vanish), e.g. semi-magic squares"; Fig. 4(a) caption without physics terms; delete "in the multipole language". (R1.13, R1.20)
32. [J] "row-by-row arrangement" → "natural square s_ij = ni + j + 1"; Def. 1.1 "(a permutation of 1, …, n² written into the grid)". (R1.14)
33. [J] Sec. 5: no "Weisfeiler–Lehman" in the main text (A1.15). Prop. 5.1 title "The vertex set determines the square; congruence". "Essentially different" → "D₄-classes", defined once (A2.23). Use "exactly the twelve vertices the boundary forces", never "minimal". (R1.15, R1.16, R2.23, A2.27)
34. [N] Renaming: transpose t → d (reflection in i = j); Thm 6.2 points → q₁..q₁₆ (forced first); polyhedron Q → H; polytope P → Π; Step 1 k−1 = n k₁ + k₀; Thm 4.2 isometry A → ψ; Prop. 2.5(3) bold v → p_c; drop Γ (Fig. 6 caption "a pair of opposite facets"). Regenerate Table 3 from the updated script. (R1.17, A1.17, R2.14)

**Census text**
35. [C] Cut geometry.tex l. 45 (facet-size multiset). (R1.23)
36. [C] geometry.tex l. 63: the factual Dudeney-groups sentence of A2.18. (R1.24, R2.18)

**Appendix and supplementary material**
37. [X] Appendix "Exact hulls": the closure test is applied to every hull. In code, move the closure test into `gem_geometry.exact_hull` and re-run all hull scripts (A2.20). (R2.20)
38. [X] Appendix "Combinatorial types": "isomorphisms mapping vertices to vertices and facets to facets"; mention the WL hash only here. (R2.21)
39. [X] `all7040_dudeney.csv` → `.tsv`; renumber to the paper's 0-based # (or document "line = # + 1"); update README l. 5 and geometry.tex l. 5. (R1.10, R2.11)
40. [X] `siamese_slacks.py`: delete the m ≤ 60 loop and rename points to q₁..q₁₆; `vertex_stats_table.log` label "squares" → "D₄-classes".

### Still in dispute / open for the author

- **None between reviewer and advocate.** The one dissent ("forced" vs "universal") was settled in R2.13.
- **Author decisions:**
  - (i) abstract order (item 20);
  - (ii) merging Sec. 3 and cutting Fig. 5 (item 18);
  - (iii) adding Fig. 2(e) (item 22);
  - (iv) verifying Mino's web page (item 28);
  - (v) confirming the Schneider theorem number (item 14);
  - (vi) whether to print one V = 10 order-five example or only mention it (item 13).

## REVIEWER — turn 3

New scratch for this turn: `.../scratchpad/dialogue/r3.py`. It uses only my own `r2lib.py`, the closed-triangulation hull from turn 2, plus an exact volume routine (a fan over the vertex polygons from the origin). I re-read `siamese.tex`, `gem.tex` (ll. 106–134), `geometry.tex` (ll. 5, 45, 53, 63, 66–80), `symmetry.tex` (ll. 1–30), the appendix and `anc/siamese_slacks.tex`/`.py` against the draft list.

### (a) New independent checks of turn-2 material

- **V3.1 (A2.9)** The proposed order-five example `1 19 15 13 17 / 23 5 14 20 3 / 10 21 12 4 18 / 24 9 8 22 2 / 7 11 16 6 25` checks out:
  - it is magic;
  - its gem has f = (10,22,14), volume 845/3 and 8 interior points.

  Confirmed.
- **V3.2 (A2.7(iv))** The printed n = 5 matrix equals 5⟨4i+3j⟩+⟨4i+2j⟩+1 entry by entry. It is magic and pandiagonal, with f = (11,23,14). Confirmed.
- **V3.3 (A2.8)** Both closed forms, n⟨i+j−m⟩+⟨i+2j−2m⟩+1 and n⟨i+2j−2m⟩+⟨i+j−m⟩+1, are magic for n = 3, 5, …, 39. For n = 5 the first reproduces the matrix printed in Sec. 6.2. I also re-did the 3 | n step by hand: −2m ≡ 1 (mod 3), and the mean of {1, 4, …, n−2} is (n−1)/2. The total is then n·n(n−1)/2 + n(n−1)/2 + n = μ_n.

### (b) Corrections to the draft list

- **R3.1 (item 4) Error in the agreed wording.** The draft says "linear factors positive for m ≥ 1". Table 3 has the factor m−1 in 20 entries (e.g. v₁ column (5): 2(m−1)(m+1)), and m−1 vanishes at m = 1. That is precisely why the text says "For m = 1 several entries vanish". The sentence must say m ≥ 2 for the linear factors. The quadratics are positive for all m ≥ 1, which is harmless.
- **R3.2 (item 2) Line numbers.** The m ≤ 60 loop in `siamese_slacks.py` is at ll. 98–106: the comment on l. 98, then `for k in (2, 3)` through the `assert`. A1.2 cites ll. 104–111 and the draft cites ll. 97–106; neither is right. Identify the block by its comment, not by line numbers.
- **R3.3 (item 1) Notation clash introduced by A1.1.** The Step 3 text uses A = x−y+m and B = 2x−y+m. But A is the grid, and R1.17 removed A as a second symbol. Use ℓ₁ = x−y+m and ℓ₂ = 2x−y+m, so that ζ = −n⌊ℓ₁/n⌋ − ⌊ℓ₂/n⌋ and ℓ₂ = ℓ₁ + x.
- **R3.4 (item 19, A2.26) One sentence is imprecise.** "For every order, the point set has no symmetry the square lacks" has no clear meaning, because a magic square of order ≥ 3 is fixed by no non-trivial element of D₄. What Thm 4.2 says is: "the point set has a non-trivial isometry exactly when the square is self-complementary, i.e. a rotation or reflection of the grid turns it into its complement". Use that.
- **R3.5 (A2(b), V2.1) The advocate's premise is wrong; no action needed.** "417 regular subdivisions" and "for 548 of the 880 classes S(z) is a triangulation" are **already in the paper** (`gem.tex` l. 133; Q4). I reproduced both in V2.1. The 548 is a count over the 880 D₄-classes, as the text already says. Nothing to add or cut.
- **R3.6 (item 6) Align the wording with Prop. 2.5(2).** "It is a vertical facet exactly when the two chains differ" is correct. The proposition, however, states the same condition as "the entries along that side are not an arithmetic progression". Say both in one clause, so the reader does not meet two criteria and wonder whether they agree.
- **R3.7 (item 12) Settle the n = 9 sentence.** Neither the causal claim nor "we have not analysed why…" earns its place. Give the counts without comment.
- **R3.8 (item 9) Placement and numbering.** Once the forced-vertex lemma moves to Sec. 2 (item 17), the new lemma should be stated in Sec. 6 just before Thm 6.2, as "Lemma 6.1 (Two linear magic squares)". The digit-exchanged square should be defined there, by its formula. That is its first use, which also settles the "define at first use" part of item 30.
- **R3.9 (item 34) Complete the renaming.**
  - Step 5 also uses v₁..v₆ in the original coordinates, so rename these to q₁..q₆ as well.
  - Fig. 8 says "vertex cells v₁,…,v₁₂ circled" and "layer value"; update it to q₁..q₁₂ and "level value". The figure script (`anc/make_fig_siamese_layers.py`) must be regenerated, not only `siamese_slacks.py`.
- **R3.10 (item 27) Label each count correctly.** The relabelling "D₄-classes" is established only for the n = 5 count, 59,993 (A2.9). Apply it to the counts for n = 6, 7, 8 only if `vertex_stats_sa*.log` shows that they too are distinct D₄-classes; otherwise call them "samples".

### (c) Settling the open points

- **Forced vs universal.** Settled in R2.13: keep "forced vertices of S", defined in the lemma statement.
- **(vi) V = 10 example.** Print it, in Rem. 6.3 (V3.1). A 5×5 matrix whose gem has fewer vertices than the Siamese gem is cheap to print. Any reader can check it, and it stops readers from taking Thm 6.2 for a minimality result.
- **(i) Abstract order and (ii) merging Sec. 3.** My final position is that both are recommended and both are reasonable for the author to decline. If the author keeps Sec. 3 as a section, the minimum is:
  - Cor. 3.1 becomes one cited sentence;
  - Fig. 5, Fig. 4(b) and the 48/56 numbers are cut.
- **(iii) Fig. 2(e).** Recommended, not required. Example 2.6 in text is required.
- **(iv) Mino and (v) the Schneider theorem number.** These are author actions and cannot be settled here.

### Final agreed revision list

The list is given with full replacement texts in the structured output. Ids F1–F41 follow the draft items 1–40, plus F41 (new, R3.4 is folded into F19). Kinds: error, gap-in-proof, clarity, jargon, notation, overclaim, structure, typo.

**Proofs and errors**
- **F1** [gap-in-proof] Thm 6.2 Step 3: print the three-case floor argument, with ℓ₁, ℓ₂ in place of A, B (R3.3), and the one-line converse.
- **F2** [gap-in-proof] Step 4: replace the "convex in the cyclic orders" claim (checked for m ≤ 60) with the trapezoid / below-the-line proof for all m. Add the remark that q₁₃ lies on plane (3). Delete the m ≤ 60 block (`siamese_slacks.py` ll. 98–106) and the matching appendix clause.
- **F3** [clarity] Step 4: label each plane (k) by three of its points.
- **F4** [gap-in-proof] Step 4 positivity sentence, with m ≥ 2 for the linear factors (R3.1) and the seven quadratics.
- **F5** [gap-in-proof] Step 4: "polygon" → "2-dimensional face, since the plane contains three non-collinear q_k".
- **F6** [gap-in-proof] Prop. 2.5(4): add the concavity argument, the vertical-facet criterion and the bijective projection (R3.6).
- **F7** [gap-in-proof] Prop. 2.5(1): "after reflecting in z = 0".
- **F8** [gap-in-proof] Rem. 4.5: add the case of planes through 0.
- **F9** [gap-in-proof] Add Lemma 6.1 (Two linear magic squares) with its proof. Step 1 and Rem. 6.3 cite it.
- **F10** [error] Rem. 6.3: "For n = 7, 9, 11 the other is…".
- **F11** [error] Rem. 6.3: add the n = 5 minimum-11 pair, with the correct parameters.
- **F12** [clarity] Rem. 6.3: define the enumeration precisely; give the n = 9 count without a reason.
- **F13** [overclaim] Rem. 6.3: add the V = 10 order-five example. Add the 15 squares to `anc/`.
- **F14** [typo] Rem. 4.6: attribute the lower bound to Brunn–Minkowski and the upper to Rogers–Shephard; rename the quantity "difference-body ratio".
- **F15** [gap-in-proof] Prop. 5.1(2): replace the proof by the pigeonhole proof via the 616 squared-distance multisets.
- **F16** [clarity] Thm 6.2: split the statement into (a) n = 3 and (b) n ≥ 5, giving Iso for n = 3.

**Structure**
- **F17** Move the forced-vertex lemma to Sec. 2.
- **F18** Merge Sec. 3 into Sec. 4 (recommended), or at least: Cor. 3.1 becomes one sentence; cut Figs. 4(b) and 5; mixed-moment material down to one sentence.
- **F19** Add the "how much of the square does the hull see" paragraph to the intro, corrected per R3.4.
- **F20** Abstract: reorder; drop a_n, b_n and m; never "minimum".
- **F21** Novelty sentence.
- **F22** Sec. 2.1: motivation, marked cells, Example 2.6 (Lo Shu), optional Fig. 2(e).

**Clarity and overclaims**
- **F23** Replace the "restrictions to that edge" paragraph.
- **F24** `gem.tex` l. 134: say "coarse invariant".
- **F25** Intro item 3: "complete on paper"; drop "grows with n".
- **F26** Abstract, last sentence.
- **F27** Q3: say these are Monte Carlo estimates, give the seeds, call Bárány's result a heuristic analogy, and label the counts correctly (R3.10).
- **F28** Mino citation (author must check the page).

**Jargon and notation**
- **F29** Def. 2.1: title and first sentence.
- **F30** Term replacements (centred entry, deviation, vertex fraction, non-vertex boundary point, level polygons and shear, slack, digit-exchanged).
- **F31** Remove C_i/C₂, define "chiral", drop the physics metaphors, state Thm 4.2's hypothesis as Σzx = Σzy = 0.
- **F32** "Natural square"; say "permutation" in Def. 1.1.
- **F33** WL hash only in the appendix; retitle Prop. 5.1; "D₄-classes" in place of "essentially different".
- **F34** Notation renaming, including Step 5 and Fig. 8 (R3.9).

**Census text**
- **F35** Cut `geometry.tex` l. 45.
- **F36** Rewrite `geometry.tex` l. 63 as a factual sentence.

**Appendix and supplementary material**
- **F37** [overclaim] Closure certificate: put it into `exact_hull`, re-run all hull scripts, and correct the appendix sentence.
- **F38** Combinatorial types: say "isomorphisms that map vertices to vertices".
- **F39** `all7040_dudeney.csv`: change to .tsv and fix the numbering offset.
- **F40** Script updates (siamese_slacks names; vertex_stats labels).
- **F41** [clarity] `geometry.tex` l. 83: drop "vertex fractions" (write "8 of 9, 12 of 16 and 12 of 25 points"). The same applies to `siamese.tex` after Thm 6.2 ("So the vertex fraction 12/n² tends to zero" → "So only 12 of the n² points are vertices, for every odd n ≥ 5"). This splits out the F30 item, which the draft attached to the wrong lines.

**Unresolved (author decisions or actions):**
- the abstract order (F20);
- merging Sec. 3 (F18);
- Fig. 2(e) (F22);
- opening Mino's page before citing it (F28);
- the Schneider theorem number (F14);
- re-running the hull scripts after F37 and confirming that no number changes.

**Verdict:** no mathematical error in any theorem. Two real gaps remain. The magicness of the digit-exchanged square and the cyclic order checked only for m ≤ 60 are now closed by short proofs (F2, F9). Two factual slips in the remarks are fixed (F10, F11). The rest is presentation, and the paper is publishable once these revisions are applied.

## Editor — changes applied

Section numbers below refer to the rebuilt paper (20 pages): Sec. 3 is now "Moments, symmetry and congruence" (old Secs. 3 and 4 merged), Sec. 4 the census, Sec. 5 the Siamese gems, Sec. 6 the open questions. The forced-vertex lemma is now Lemma 2.4, the subdivision proposition Prop. 2.6, the new lemma on the two linear squares Lemma 5.1, the Siamese theorem Thm 5.2, the linear-squares remark Rem. 5.3.

**Proofs and errors**
- **F1** Done. Step 3 now prints the three-case floor argument with ℓ₁ = x−y+m, ℓ₂ = 2x−y+m = ℓ₁+x, and the converse, then the list of the five regions Λ. Independently re-derived (range bounds, all three cases, converse).
- **F2** Done. Trapezoid argument (plane y = m) and below/above-the-line argument (plane x = −m) inserted after the facet list, with the remark on q₁₃. Re-checked: (m+1)²/m < 2m+2 ⇔ m > 1. Appendix clause "the convexity of the quadrilaterals for m ≤ 60" deleted; the m ≤ 60 block in `anc/siamese_slacks.py` deleted (identified by its comment).
- **F3** Done. Each inequality (k) labelled by its three points before the list.
- **F4** Done, with m ≥ 2 for the linear factors. The factor list was recomputed from the table with SymPy: the linear factors are m−1, m, m+1, m+2, 2m−1, 2m+1, 2m+3, 4m−3, 4m−1 (2m+3 was hidden in the agreed "…"; now listed explicitly) and the quadratics are exactly the seven named; m−1 occurs in 20 entries.
- **F5** Done (wording as agreed).
- **F6** Done; the vertical-facet clause states both criteria (chains differ / not an arithmetic progression), per R3.6.
- **F7** Done.
- **F8** Done (Rem. 3.6).
- **F9** Done: Lemma 5.1 (Two linear magic squares) with proof, placed just before Thm 5.2; Step 1 cites [andrews1960magic] only for the identification with de la Loubère's construction and cites Lemma 5.1 for magicness; associativity is now proved in Step 1. **Correction to the agreed text:** it said the map (i,j) ↦ (⟨i+j−m⟩, ⟨i+2j−2m⟩) has determinant −1; its linear part [[1,1],[1,2]] has determinant 1 (as Step 1 already said). The lemma says "determinant 1". The 3 | n argument was re-checked by hand (sum of {1,4,…,n−2} taken three times = n(n−1)/2).
- **F10** Done ("For n = 7, 9, 11 the other is …"); re-verified for n = 9 (the two 12-vertex classes among 441 are the Siamese and digit-exchanged squares).
- **F11** Done; the matrix is printed as a displayed matrix. Re-verified: magic, pandiagonal, not associative, f = (11,23,14); exactly two V = 11 classes among the 184, complements of each other.
- **F12** Done; counts given without comment on n = 9.
- **F13** Done. Example printed (displayed next to the F11 matrix); `anc/sa_n5_V10.txt` added (15 squares, extracted from the annealer output with exact hulls: 14 with f = (10,22,14), one with (10,23,15); none are complements of each other) and listed in `anc/README.md`. Example re-checked: f = (10,22,14), volume 845/3, 8 interior points.
- **F14** Done: Rem. 3.7 "Difference-body ratio", σ(K) = vol(K−K)/(8 vol K); Brunn–Minkowski [schneider2014convex, Thm 7.1.1] for the lower bound, Rogers–Shephard for the upper. Script renamed `anc/central_symmetry_defect.py` → `anc/difference_body_ratio.py` (output unchanged). **Author to confirm** Thm 7.1.1 in the 2nd edition (2014) listed in the bib.
- **F15** Done. New proof of Prop. 4.1(2) by the 616 distance multisets; the count 616 was recomputed and is now asserted in `verify_revision.py` (block D). The all-pairs test is kept in the appendix as a redundant check.
- **F16** Done: Thm 5.2 split into (a) n = 3 and (b) n ≥ 5, with the proof of (a) placed after Step 2.

**Structure**
- **F17** Done: Lemma 2.4 (Forced vertices), with the definition of "sides" and the sentence on 4 to 13 forced vertices at order four, now follows Prop. 2.3; Sec. 5 opens with "For the Siamese squares nothing other than the forced vertices is a vertex (Thm 5.2)". The census paragraph was reworded to avoid repeating the 4–13 sentence.
- **F18** Done, including the recommended merge (old Sec. 3 is now §3.1 "First and second moments" of Sec. 3 "Moments, symmetry and congruence"; `balance.tex` removed). Cor. 3.1 replaced by the one-sentence Loly invariant; mixed-moment paragraph reduced to one sentence; the 48/56 numbers dropped. Fig. 4(b) cut (`make_fig_moments.py` regenerated with panel (a) only). **Fig. 5 was NOT cut**: the head-to-tail weighted vector sum is one of the author-requested figures that must be kept. Instead its mixed-moment quadrant tables were removed (`make_fig_weighted_sum.py` regenerated); it now illustrates only the vanishing first moments, which are used in Thm 3.3. **Correction to the agreed text (F31):** the proposed Fig. 4 caption "the centre of mass of each row and column lies over O" is false (a row's checkers sit at y = y_i); caption and figure now say the centre of mass of all the checkers lies over O.
- **F19** Done (paragraph before the enumerate, with the R3.4 wording).
- **F20** Done with the recommended order (author may reorder). Also updated the plain-text abstract in `submission_notes/arxiv_comments.md`.
- **F21** Done.
- **F22** Done: motivating sentence, marked cells, Example 2.7 (Lo Shu, continuing Ex. 2.5) — all cells, vertical facets and the plane z = −x−y−3 re-checked by exact hull. Optional Fig. 3 panel (e) not added (left to the author).

**Clarity and overclaims**
- **F23**, **F24**, **F25** Done (F25 also defines "slack" at first use).
- **F26** Covered by F20.
- **F27** Done. Status sentence and seeds added; Bárány sentence replaced; `vertex_stats_magic.json` shows raw = distinct for n = 6, 7, 8, so all four counts are written "distinct D₄-classes". Q2 now says "magic squares of order five up to D₄".
- **F28** Done: key renamed `trump_howmany`; `@misc{mino2024order6}` added. The page https://magicsquare6.net/ was opened: title "The number of magic squares of order 6", author Hidetoshi Mino; it gives 17,753,889,197,660,635,632 up to D₄, with corrections dated 2024-02-17 and a number file dated 2024-05-20 (no single announcement date). No number from the page is quoted in the paper. **Author to confirm** the year 2024 for the citation.

**Jargon and notation**
- **F29**–**F33** Done throughout (excess / row and column excesses; non-vertex boundary point; level polygons and shear; natural square; permutation in Def. 1.1; {±id} and {id, ι_g} in Table 1; chiral defined; first moments with "dipole moment" only as an attributed aside; WL hash only in the appendix; Prop. 4.1 retitled; "D₄-classes" in Thm 3.4 and Sec. 1). Fig. 3 panel (b) relabelled "cell positions" (was "centred cells").
- **F34** Done: d for the diagonal reflection; q₁..q₁₆ (forced vertices first) in Step 4, Table 3, the antipodal list and Fig. 8; q̃_k = Φ⁻¹(q_k) for the original-coordinate points in Step 5 (to avoid using q_k for two different points); H, Π, −id, k₁/k₀, ψ, p_c; Γ removed. `siamese_slacks.py` (names, ORDER) and `make_fig_siamese_layers.py` updated; Table 3 and Fig. 8 regenerated (all assertions pass).

**Census text**
- **F35**, **F36** Done.

**Appendix and supplementary material**
- **F37** Done. The closure test is now `gem_geometry.certify_closure`, called inside `exact_hull`; `verify_revision.py` block F calls it explicitly. Re-ran `verify_revision.py`, `run_geometry_880.py`, `box_and_classes.py`, `difference_body_ratio.py` and `linear_squares.py 5 7 9 11`: no reported number changed (the JSON outputs are identical apart from run times; log diffs are only the renamed terms and one new line). The appendix states that the certificate is applied to every hull; Sec. 5 calls the n ≤ 41 hull check a cross-check, not part of the proof. Side effect: certified hulls take about 16 ms instead of 6 ms, so the appendix timing is now "about 15 s" and Q2's estimate "about 16 ms per certified exact hull … about seven CPU-weeks" (was 6 ms, three weeks).
- **F38** Done (definition, plus the 616-multiset certificate).
- **F39** Done: `all7040_dudeney.tsv` with column `paper_no` (0-based paper #; all 7040 rows checked against `squares880.txt`), old `.csv` removed, scripts, README and Sec. 4 updated.
- **F40** Done: `siamese_slacks.tex` and `vertex_stats_table.log` regenerated ("distinct D4-classes").
- **F41** Done (both places).

**Other edits made while applying the list:** README section/lemma/figure numbers updated to the new numbering; leftover process comments ("round 1", "RefB") removed from two figure scripts; old terms ("row-by-row", "boundary non-vertex") updated in script comments and log strings.

**Unresolved (author decisions or actions)**
- Abstract order (F20): applied in the recommended order; the author makes the final call.
- Merging Sec. 3 into Sec. 4 (F18): applied; Fig. 5 kept (author-requested), only its mixed-moment tables removed.
- Fig. 3 panel (e) with the Lo Shu subdivisions (F22): not added; Example 2.7 is in the text.
- Mino citation (F28): page opened and title confirmed; author to confirm the year.
- Schneider theorem number (F14): author to confirm Thm 7.1.1 in the 2nd edition.
- Hull scripts re-run after F37 with no number changed; the n = 6, 7, 8 annealer counts are distinct D₄-classes (raw = distinct in `vertex_stats_magic.json`).

## Consolidation fixes

1. Abstract, intro item 3, submission/main.tex, arxiv_comments.md: "Other linear magic squares have more vertices" -> "can have many more vertices: up to 18, 25, 31 and 36 for orders 5, 7, 9 and 11"; intro adds "and as few as 11 at order five", and the ten-vertex order-five squares are described as not linear. Checked against results_linear_squares.json (V ranges [11,18], [12,25], [12,31], [12,36]); I checked exactly that none of the 15 squares in sa_n5_V10.txt is linear (neither digit is affine mod 5).
2. Intro Results paragraph: "every odd order" -> "every odd order $n\ge5$". The n=3 gem has 8 vertices (Thm 5.2(a)), and the digit-exchanged square at n=3 also gives (8,16,10) in an exact hull.
3. anc/verify_revision.py comment: Prop. 5.1(2) -> Prop. 4.1(2) (aux: prop:gem-injective = 4.1).
4. Stale anc section references: siamese_slacks.py Section 6 -> 5; linear_squares.py Section 6 -> 5; README Ehrhart row Section 5 -> 4; solid_centroid.py "quoted in Section 3" -> supplementary, because the paper no longer quotes that number. "Section 6, question 3" in the README is correct (Open questions = Sec. 6).
5. Fixed a syntax error introduced in anc/linear_squares.py: the log string "digit-exchanged square s' = ..." had an unescaped quote. All anc/*.py files now compile.
6. Appendix: "every hull" -> "every exact hull in the paper (..., and the 15 ten-vertex order-five squares)", consistent with the floating-point Sampling paragraph.
7. Abstract and arXiv comments: "polynomials in n" -> "polynomials in m=(n-1)/2". I re-ran siamese_slacks.py (SymPy, exact); the output table is unchanged.
8. fig_moments in-figure label: "so the centre of mass of all the checkers lies over O". Regenerated figures/fig_moments.pdf.
9. Def. 2.1: "The Magic Gem is the convex hull of the lift of the grid by the heights z defined below". Sec. 2.1 adds "(with vertical facets over the sides where the entries are not in arithmetic progression)", matching Prop. 2.6(2).
10. Rem. 5.3: merged the repeated "For n=7,9,11" into "one of them the Siamese square and the other the digit-exchanged square s'". Exact hulls of s' for n=5..15 give (12,24,14).

Rebuilt main.pdf/paperA.pdf (20 pp, no undefined refs and no overfull boxes) and the flat submission/ (sections and the slack table inlined, anc synced). Also rebuilt paperA_arxiv.tar.gz. A clean temp-dir compile with pdflatex+bibtex gives 20 pp, a clean log, and the same text as paperA.pdf. I inspected changed pages 1, 2, 3, 6, 8, 17 and 20 as images.
