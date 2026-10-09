# Response to the referee

We thank the referee for a detailed and constructive report. Every point is answered below in the order of the report; section, theorem and figure numbers refer to the revised manuscript (19 pp.). New exact checks are in `anc/verify_revision.py`, `anc/siamese_slacks.py` and `anc/linear_squares.py`. All of them assert their statements and are listed in `anc/README.md`.

Summary of the main changes:
- The two false statements (old Prop. 3.1 interior, old Prop. 4.5 parity) are corrected. The coplanar arrangements are classified exactly (Prop. 2.3): the eight D4-images of the row-by-row square.
- The ill-posed Prop. 5.1(1) is replaced by a D4-invariant statement (Prop. 5.1).
- The covariance argument is proved for every order (Thm 4.2). Thm 4.3 is restated as the hull-level statement for n = 4.
- The gem is placed in the framework of regular subdivisions (Sec. 2.1, Prop. 2.5).
- The Siamese result is now Theorem 6.2 in its own section. It is stated as "vertices = forced vertices", and it adds Iso(G) = {±id}. The proof is printed in full, with a table of slack polynomials (Table 3).
- The linear-square generalisation was tested (Remark 6.3): the answer is negative.
- Section 3 is reduced to about one page. The Ehrhart subsection, Rem. 3.4, Rem. 3.5 and Table 4 are cut or reduced. The figures are cut from 9 to 8, with smaller panels, and the abstract and introduction are rewritten.

---

## 1.1 Result-by-result verdicts

| Item | Response |
|---|---|
| Lemma 2.2 trivial | Kept as Lemma 2.2, because Lemma 3.2 and Thm 4.2 use it. (2) now states the 1/N normalisation and names a_n, b_n. |
| Prop. 2.4 (D4-invariance) trivial | Demoted to one sentence and equation (2) in Sec. 2. |
| Prop. 3.1 trivial and false | The centroid statement is now one clause (start of Sec. 3). The interior statement is corrected in Prop. 2.3 (see 1.3(a)). |
| Prop. 3.2 restates semi-magic; "n ≥ 3" unnecessary; diagonals absent | Demoted to the paragraph "Row and column sums as moment conditions" in Sec. 3, with no hypothesis on n. The text now says that it characterises *semi-magic* squares and that the diagonal conditions are not of this form. |
| Cor. 3.3 known | Kept as Cor. 3.1 with the one-line proof, credited to Loly in the statement. |
| Rem. 3.4 trivial; contains the key to a general theorem | Replaced by Lemma 3.2 (covariance = diag(a_n, a_n, b_n) for semi-magic squares). This is the ingredient of Thm 4.2. The inertia-tensor discussion is deleted. |
| Rem. 3.5 out of scope | Deleted. The random-volume statistics are no longer in the paper. |
| Lemma 4.1 trivial | Now equation (4) in Sec. 4. |
| Prop. 4.2 folklore; garbled proof | Demoted to Lemma 4.1. The proof uses the referee's chain g²S = g S̄ = (gS)‾ = S. Uniqueness of g is added (Thm 4.2 needs it). |
| Thm 4.3 modest; point-set part holds for all n | Split into two results. Thm 4.2 (all n, point sets, the covariance argument) and Thm 4.3 (n = 4: Iso(G) = Iso(P_S), the only part that needs the computer). Sec. 4 credits Dudeney for the 48/304/528 partition and says that what is new is the absence of extra hull isometries. |
| Prop. 4.4 trivial plus data; confusing sentence | Demoted to Remark 4.5 and shortened. The sentence about rotation by π is deleted. Fixed facets of the half-turn are now identified as the vertical facets of Prop. 2.5(2). |
| Prop. 4.5 trivial and false | Lemma 4.4 adds the hypothesis (not a D4-image of the row-by-row arrangement, e.g. semi-magic). The paper gives the counterexample. |
| Rem. 4.6 classical plus data | Merged into Sec. 5 as two sentences, citing Ollerenshaw–Brée for pandiagonal squares. The list of 8-vertex squares is cut. |
| Rem. 4.7 standard; upper bound missing; σ = 1 is a corollary | Now Remark 4.6. It cites Rogers–Shephard for both bounds 1 ≤ σ ≤ 5/2 (with equality cases) and Grünbaum and Schneider for measures of symmetry. It states σ = 1 ⇔ associative as a consequence of Thm 4.3. |
| Table 2 / 352 types | Sec. 5 explains that types are unions of complement orbits. The 93 one-member types are self-complementary squares; of the 201 two-member types, 177 are mirror pairs and 24 consist of two self-complementary squares (verified). The "numerical coincidence" remark is deleted. |
| Prop. 5.1 ill-posed / trivial at point-set level | (1) is replaced by a D4-invariant statement (see 1.3(c)). Thm 4.2 now covers the point-set part for all n. |
| Prop. 5.2 trivial/standard | Demoted to Lemma 6.1 (forced vertices). It is the preamble to the Siamese theorem and is interpreted via regular subdivisions. The box is now one sentence in Sec. 5. |
| Sec. 5.3 Ehrhart | Cut to two sentences in Sec. 5. They state the count and the referee's remark that for lattice 3-polytopes the polynomial is equivalent to volume, normalised surface area and lattice-point count. The redundant checks at t = 4, 5, 6 are no longer described. The script remains in anc/. |
| Prop. 5.3 Siamese | Promoted to Theorem 6.2 in its own Section 6 and stated as "the vertices are exactly the forced vertices". See 1.3(d). |
| Table 4 | Removed. The numbers are given once, with the sampling caveat, in Open Question 3, which is rephrased as a growth-rate question. The "magic" values for n ≥ 5 are now labelled as annealing samples. |

## 1.2 General symmetry theorem
Done as Thm 4.2. The statement covers every order n ≥ 2 and every arrangement with vanishing dipole moment (in particular all semi-magic squares). It gives (1) every isometry between point sets is ĝ or ĝτ; (2) point sets are congruent iff T ∈ D4·S ∪ D4·S̄; (3) Iso(P_S) is {id} or {id, ι_g}. The proof follows the referee's argument: centroid fixed, A Σ Aᵀ = Σ, eigenspaces, grid symmetry. Sec. 4 then states the residual hull-level question. Thm 4.3 answers it for n = 4 by exact computation, and Thm 6.2 answers it for every Siamese gem (Step 5, by hand). It is Open Question 1 in general. The assertions in `verify_revision.py` (part C) check, for all 880 squares and the Siamese squares of orders 3–15, that every point-set isometry is block-diagonal and that the group orders are as stated.

## 1.3 Errors and gaps
- (a) Prop. 3.1. The new Prop. 2.3 proves that the points are coplanar iff S is one of the eight D4-images of s_ij = ni+j+1, for every n ≥ 2. The proof: integer differences u, w; WLOG 1 ≤ u ≤ w; the entry 2 forces u = 1; the entry n+1 forces w = n. Otherwise the gem is a 3-polytope with 0 in its interior. Semi-magic squares are never coplanar, because affine z with zero row and column sums is 0. The classification was verified exhaustively for n = 2 (24 arrangements) and n = 3 (9! arrangements), with an independent rank test (`verify_revision.py`, part A). A first version of the test, which checked only additive separability, gave 72 for n = 3. It was corrected before use and cross-checked against matrix rank.
- (b) Prop. 4.5. Now Lemma 4.4 with the full-dimensionality hypothesis. The row-by-row counterexample is stated after it. The terminology of interior and boundary points is now introduced after full-dimensionality is available (Prop. 2.3).
- (c) Prop. 5.1(1). Replaced by: "if ĝ vert G(S) = vert G(T) for some g ∈ D4 then T = gS". In words, the vertex set up to D4 determines the class. The proof combines the pairwise distinctness of the D4-canonical forms of the 880 vertex sets (exact) with Thm 4.3. Part (2) is the congruence statement (616 classes = complement orbits), re-verified from scratch in `verify_revision.py` (part D).
- (d) Siamese proof. Step 1 now contains both missing facts. The induction uses κ(i,j) = (⟨i+j−m⟩, ⟨i+2j−2m⟩). The up-right move is blocked exactly when n | k, because the target cell κ⁻¹(q,0) holds nq+1. The cell below is κ⁻¹(q+1,0), which is empty. Each run fills one broken diagonal. Further changes:
  - Step 2 proves from the closed form, for all m ≥ 2, that the forced set of Lemma 6.1 is exactly the twelve listed cells. Theorem 6.2 is therefore stated as "the vertices are exactly the forced vertices". This also covers n = 3, where the forced set is the eight boundary points.
  - Because the forced vertices are vertices by Lemma 6.1, the old step (d) (three independent tight normals) is no longer needed.
  - The verification is printed in full. Table 3 lists the slack polynomials of the 8 inequalities at the 16 layer-polygon vertices, factored so that positivity for m ≥ 2 is visible. With central symmetry this covers all 16 inequalities. The text gives the facet list with cyclic orders. The proof is now checkable by hand, and the label "computer-assisted" is gone.
  - A new Step 5 proves Iso(G) = {±id} for all m ≥ 2 by hand: the six antipodal vertex pairs have distinct norms, and v_1 is orthogonal to no other vertex.
  - The Fig. 8 caption now reads "The combinatorics of the layer polygons does not depend on m ≥ 2".
- (e) "Height-weighted centroid" is renamed "dipole moment" throughout, with the citation to Rogers–Loly at that point.
- (f) Open Question 1 is rewritten. For odd n, Lemma 4.1 and Thm 4.2 give the point-set statement; the hull statement is posed as open.
- (g) Appendix A now states the certificate explicitly. Every point is checked against every integer facet inequality, and every edge of every facet polygon lies in exactly two facets (closed surface). Euler's relation is checked in addition. The closure check is new and passes for all 880 gems (`verify_revision.py`, part F).

## 1.4 Framing: regular subdivisions
New Sec. 2.1 and Prop. 2.5, citing De Loera–Rambau–Santos (Ch. 2) and Gelfand–Kapranov–Zelevinsky (Ch. 7). The proposition states the following.
- The lower and upper facets project onto the maximal cells of S(z) and S(−z).
- Vertical facets lie only over the four sides, and occur iff the side's entries are not in arithmetic progression. We checked this and corrected the referee's description: the vertical facets are not automatic, and square #45, whose top row is 1 6 11 16, has none over that row.
- Vertices are exactly the vertices of cells of S(z) or S(−z).
- The labelled face lattice depends only on the pair of secondary cones containing z and −z, and complementation swaps the two subdivisions.

The paragraph after Prop. 2.5 states what the framework gives concretely:
- the forced-vertex lemma;
- the reading of the Siamese shear Φ as invariance of S under adding affine functions;
- the n = 4 data: 856/20/4 gems with 4/3/2 vertical facets, 417 regular subdivisions of the 4×4 grid up to D4 induced by the 7040 magic height functions, and 548 of the 880 lower subdivisions are triangulations (all verified, part G);
- the reformulation of the type census as a question about secondary cones (Open Question 4).

We kept the title, because the arXiv replacement must keep it. The subdivision framework, Thm 4.2 for all orders and the Siamese family theorem are what the word "framework" now refers to. The introduction says precisely what is new.

## 1.5 Stronger paper
1. Done (Thm 4.2, Thm 4.3).
2. Done (Sec. 2.1).
3. Done as an experiment, with a negative answer (Remark 6.3, `linear_squares.py`). We enumerated all linear magic squares s = n⟨u·c+α⟩ + ⟨w·c+β⟩ + 1 for n = 5, 7, 9, 11: 184, 3159, 441 and 89,125 D4-classes. The vertex counts range over [11,18], [12,25], [12,31] and [12,36], so there is no uniform bound for the family. The minimum 12 is attained by exactly two classes for n = 7, 9, 11. One is the Siamese square. For n = 7 the other is the digit-exchanged Siamese square, which has f = (12,24,14) for every odd n from 5 to 31; this is posed as Open Question 5. We did not cite Cook–Hartmann–Kannan–McDiarmid, because the paper does not use integer-hull vertex bounds.
4. Not done. The full order-5 census (2.75·10⁸ squares) would take about three CPU-weeks at our measured 6 ms per exact hull. We did not run it, and Open Question 2 states this estimate honestly instead of calling the computation "feasible". We also tried to enumerate the order-5 pandiagonal subclass with a simple backtracking search, but it was too slow to finish in the time available, so we report nothing about it. The general Thm 4.2 and the linear-square census provide the order-independent strengthening instead.
5. Done: Open Question 3 is now a growth-rate question. It cites Bárány–Buchta (Θ(ln² N) for points in a polytope), reports that E[V]/ln² N decreases from 1.70 to 1.32 over n = 3..10, and notes that the analogy with i.i.d. points is heuristic.

## 1.6 Abstract and introduction
- Centring identity, box and Ehrhart count: removed from the abstract.
- "Semi-magic" is now used wherever only row and column sums are involved.
- "155 distinct volumes": fixed.
- Ill-posed "no two gems have the same vertex set": replaced (Prop. 5.1(1)).
- Novelty: the introduction now credits Dudeney for the partition, Loly and Rogers for the moments, and DRS/GKZ for the lifting. It states that the new results are Thm 4.2, the hull-level classification and census, and the Siamese theorem.
- "Every order n ≥ 3": fixed.

## 2. Tone
All items are addressed:
- "misreadings" sentence → "We record them in the coordinates of the gem for later use".
- Sec. 3 title → "Moments of the point set".
- "what magic means" → "Row and column sums as moment conditions".
- The repeated centring caveats are reduced to one clause (Sec. 3). The meta-statement is removed from Def. 2.1; one neutral sentence about unit weights remains after the definitions.
- The Sec. 1 item 1 sentence is deleted.
- The Rem. 3.5 hedges are deleted with the remark.
- The hash sentence, "classical reference partition", "expected one", "numerical only" and "This is a theorem…" are all deleted.
- "To the author's knowledge" is replaced by a factual statement: Pinn–Wieczerkowski estimate, and an exact order-6 count by H. Mino (2024) as reported on Trump's site.
- "Dürer's own gem" → "The gem of Dürer's square".
- The rhetorical sentences in Sec. 6 are deleted; Sec. 7 now contains only open questions.
- "The picture." → "The construction."; "What is and is not new." → "Relation to previous work."
- LaTeX process comments are removed from `main.tex`. We kept a short `\Cref` macro rather than loading `cleveref`. The package is not installed in our TeX distribution, so we could not test the build with it. The macro produces the same output, needs no package, and compiles on arXiv.

## 3. Language and presentation
**3.1 Notation.** Every listed clash is fixed. Renamings, by referee item:
- ρ (reflection) → τ. The row sums ρ_i → R_i and the column sums γ_j → C_j.
- V for the vertex set → vert G. V remains the count.
- F for a facet → Γ. F remains the count.
- I (interior count) → V°; Loly's moment I(S) → J(S). The inertia tensor is removed.
- B (boundary count) → V^∂; the box B_n → 𝓑_n. The Siamese layers T, U, M, D, B → Λ_{+2}, Λ_{+1}, Λ_0, Λ_{−1}, Λ_{−2}, also in Fig. 8.
- The Siamese affine part L(x,y) → λ(x,y). L_S(t) (Ehrhart) is removed.
- The magic constant M(n) → μ_n.
- c = (n²+1)/2 → s̄; Σ_zz = c → b_n.
- The signed-mass notation m_ij is removed, so m now means only (n−1)/2.
- T vs t and D vs D_4: resolved by the layer renaming.
- Iso(X) is now defined for arbitrary subsets of R³.

Since the notation is now unambiguous and is introduced in one place (Sec. 2, "Terminology"), we did not add a separate notation table.

**3.2 Terminology.** The terms "vertex", "interior point", "boundary non-vertex point" and "vertex fraction V/N" are fixed in Sec. 2 and used throughout, also in the figures; "strictly interior" is removed from Fig. 1. "Order four" is the noun and "order-four" the adjective throughout. "Combinatorial type" is defined once (Sec. 5).

**3.3 Specific sentences.**
- Prop. 4.2 proof: chain replaced as suggested.
- "the 832 gems in cases (2) and (3)": fixed.
- Prop. 5.1 title → "Injectivity and congruence".
- The "while" sentence → "At most four points are interior, and at most six are boundary non-vertex points".
- Euler's relation: moved to App. A as a check.
- Facet sizes: now "For these 880 gems …".
- Prop. 3.2(2) parentheses: removed with the restructuring.
- Lemma 2.2(2): normalisation 1/N stated.
- Square numbering: defined in Sec. 2 at first use (lexicographic order of Frénicle standard forms, verified in `verify_revision.py` part J). Every cited square (#45, #54, #102, #124, #379, #593, #802) is displayed as a full matrix in Sec. 5, or printed in its figure.
- `\smallmatrix` squares: replaced by displayed matrices (Sec. 5, and the order-5 Siamese square in Sec. 6).
- The paragraph before Fig. 4: removed. Fig. 4 now has one caption sentence per panel.
- Table 3 (now in Table 2): k = 5 added (both counts 0).
- Volumes row: the caption now explains that the per-V counts add up to more than 155.
- Table 4: removed (see 1.1).
- Fig. 4(d): now prints the integers 8zxy (sums 0 and 480).
- Hardware: removed; run times are given in App. A and anc/README.md.

**Bibliography.**
- `trump2012enumeration` now has a title, URL, year and access date.
- The companion paper is cited once as a manuscript, with the statement that none of its results is used.
- MSC codes are added (05B15, 52B05, 52B15, 52B20).
- The `beck2010enumeration` key is internal only; the printed year (2011) is correct.

**3.4 Structure and figures.**
- Section 3 is now about one page of text plus two figures.
- The data that sat in numbered statements (facet orbits, classes, σ) is moved into remarks or into the single census table (Table 2), which merges old Tables 2 and 3.
- The Siamese theorem has its own Section 6, with the forced-vertex lemma as preamble. Section 7 contains only the open questions.
- Figures 9 → 8, by figure:
  - Old Fig. 3, rows e–l (eight congruent D4 images): cut. The remaining top row is now a small strip (Fig. 3).
  - Old Fig. 4: reduced to two panels, the checkers and the 8zxy tables. The heights panel and the lever panel are cut.
  - Old Figs. 6 and 7: merged into one figure (Fig. 6, gems on top, point sets below).
  - Figs. 1, 2, 5 (now Fig. 5, the weighted head-to-tail sum), the checkers panel and the point-set stem panels are kept, because they are the visual explanation of the construction that the paper is built around. Fig. 1(b) is kept for the same reason; its footer restating the centring identity is removed.
- Captions are shortened, and "has no other symmetry" is gone with the rewritten Fig. 6 caption.

## 4. Ten most important changes
All addressed above. Item 4: the title is unchanged, for the reason given under 1.4. Item 8: we chose the linear-square direction, which has a negative answer. Item 10: 9 → 8 figures, for the reason given under 3.4.

## 5. Literature
Added:
- Rogers–Shephard 1957
- Grünbaum 1963
- De Loera–Rambau–Santos 2010
- Gelfand–Kapranov–Zelevinsky 1994
- Bárány–Buchta 1993
- Pinn–Wieczerkowski 1998
- Frénicle 1693
- de la Loubère (1693 English translation of the 1691 original)
- Ollerenshaw–Brée 1998

Not added: Cook et al., because nothing in the paper uses vertex bounds for integer hulls.

Dudeney's group labels: since numbering conventions differ between reproductions, the labels used are tabulated for all 7040 squares in `anc/all7040_dudeney.csv`, and the text says so. Rogers–Loly is cited where the dipole moment appears. The bibliography year issue is noted above.

## Restructuring per author decisions

After the exchange above, the author fixed the open points as follows; the manuscript now implements them.

- **Order.** The paper now runs from what the figures show to the theory, in the order of the themes: (2) the construction and the pictures of Dürer's square and the Lo Shu; (3) a separate section on balance; (4) symmetry and congruence (covariance argument for every order, complement, the isometry groups of the order-four gems); (5) the exact geometry of the 880 order-four gems (bounding box and forced vertices, regular subdivisions, census); (6) larger orders, ending with the Siamese theorem, the remark on linear squares, and (7) open questions. The abstract and the list of results in the introduction follow the same order and end on the Siamese theorem. Statements and proofs are unchanged apart from renumbering; the forced-vertex lemma and the subdivision proposition moved from Section 2 to Section 5.1, and each section now opens with a sentence on why it follows from the previous one.
- **Balance section restored** (Section 3): unweighted balance holds for every arrangement (and the solid centroid is not the origin for 829 of the 880 order-four gems); the height-weighted moments, in particular the dipole moment, vanish exactly for semi-magic squares; Loly's invariant is again a corollary with proof; the mixed moment is not forced (48 values of |Σ z xy| over the 880 squares, 56 zeros, 48 of them associative); the covariance lemma closes the section and leads into Section 4. Fig. 4 (checkers with the raw entries) is kept, and Fig. 5 (head-to-tail weighted vector sum) again carries the quadrant tables of the mixed moment (totals 0 and 60), regenerated by `anc/make_fig_weighted_sum.py`, which asserts both totals.
- **Lo Shu subdivision panel.** Fig. 3 has a panel (e) with S(z) and S(−z) of the Lo Shu, drawn by `anc/make_fig_construction.py`, which recomputes the marked cells and vertical facets from the exact hull and asserts that they are those of Example 5.3.
- **Appendix B, "Lattice-point counts and vertex statistics".** The Ehrhart material (Q = G + (1/2,1/2,1/2) a lattice polytope; exact Ehrhart polynomials and h*-vectors of all 880 gems, all h* non-negative; 554 distinct polynomials against 616 congruence classes, 352 types, 39 f-vectors and 155 volumes; Lo Shu and Dürer polynomials) and the numerical vertex-count table for random arrangements (n = 3..10) and annealed magic squares (n = 5..8), with the sampling caveats, are restored in one short appendix. Every number was re-checked by rerunning `anc/ehrhart_880.py` (identical log) and `anc/vertex_statistics.py table`.
- **Schneider.** Brunn–Minkowski is cited to the book without a theorem number.
- **Companion paper.** Cited under its present title, "Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies".
