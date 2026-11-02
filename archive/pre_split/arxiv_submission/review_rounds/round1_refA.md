# Referee A — Round 1 report on v5
**Manuscript:** "Magic Gems: Magic Squares as Orthogonality Conditions on a Height Function", K. E. Mathewson, v5 (26 pp., 10pt)

## 1. Summary and recommendation

The author places the centred entries of an n×n arrangement as heights z over the centred grid and observes that the magic conditions say z ⊥ W, where W is the 2n-dimensional span of the centred line indicators (stated explicitly as a reformulation, not a theorem). From this viewpoint the paper derives: (i) a "moment hierarchy" — orthogonality to x^m, y^m for m ≤ k is equivalent to equal row/column sums iff k ≥ n−1 (a Vandermonde fact), plus an integrality argument showing the permutation threshold drops below n−1 for n ≥ 14; (ii) exact mean/variance of two energies on a random arrangement and a Hoeffding CLT; (iii) an exact single-swap formula N²ΔE = d²m + 2d(u(a)−u(b)); (iv) |L_4| = 14,639,440 by meet-in-the-middle; (v) an exact classification of the 880 order-4 "gems" (39 f-vectors, 352 types, 616 congruence classes = complement orbits) and a computer-assisted proof that Siamese gems have 12 vertices.

**Recommendation: Major revision. Score 6/10.** Every mathematical statement I checked is correct (details below); the problems are presentation, length, one attribution, and one defective figure.

## 2. What I verified independently (scratch: `review_rounds/scratch_refA/`)

- Section 4 proofs read line by line: Lemma 4.1, 4.6, 4.7 (incl. the Gram/eigenvalue bounds in (10)), 4.8, Theorem 4.11(a)–(c), Prop. 4.14 (incl. the C(13,6)=1716 > 1274 base case and the induction ratios 2, 2n/(n+1) ≥ 28/15 vs. (n+1)²/(n(n−1)) ≤ 225/182), Theorem 4.17, Lemma 4.18, Cor. 4.19, 4.13, Prop. 4.22. All correct. Witnesses in Remark 4.3, 4.5, 4.16 and Prop. 4.14(2) recomputed by hand: correct.
- E[E_full] = σ²(2n+2)(n−1)/n² = (n⁴−1)/(6n²); E[E_low] = (n²+1)(n⁴−n²+12n−12)/(72n²): rederived; both give 40/27 at n=3.
- Exhaustive 9! (own code): means 40/27, Var 398/2187 and 1532/2187, 177/346 distinct values, modes 46/27 and 10/9, maxima 20/9 and 40/9, local minima 16 (8 non-magic) and 344 (336): all agree with Table 1.
- Var closed forms (20): I computed Var(E_full) and Var(E_low) exactly for n=3,4 by a different method (line-pair enumeration; quadruple equality patterns with p₂,p₄). Results 398/2187, 527/640, 1532/2187, 14093/1440 equal the paper's rational functions. Table 2's n=4 std 0.9074 = √(527/640): correct.
- 7040 magic squares / 880 classes regenerated; min-gap multiset {2:432, 3:420, 4:28}: correct.
- Hulls of all 880 (own exact facet-merging code): V-distribution 7/10/103/80/380/106/162/14/18, 39 f-vectors, volumes 58 … 292/3, mean 84.05, 155 distinct, 352 self-complementary classes, 880 distinct hull-vertex sets, 616 distance-signature classes of sizes 1 (352) and 2 (264): all match §5.5. Dürer (12,24,14) vol 92; #802 (16,36,22) vol 242/3; Lo Shu (8,16,10) vol 18: correct.
- Diagonal-only count 49,932,288,000 by direct combinatorics: correct. |L_4| and Table 4 reproduced by compiling and running the enumerator (7.6 s). `siamese_proof.py` runs and reports all symbolic checks pass; I checked the 12 vertex cells against the explicit order-5 Siamese square and the closed form s(i,j) against the Lo Shu.

So the numbers are right. My points are about what the paper claims to be and how much of it is needed.

## 3. Numbered points

**1. [BLOCKING] Figure 1 (p. 5) is defective.** The bottom strip has overprinted, illegible panel labels ("(i)(e)H-flip R0°", "(j)(f) V-flip R90°" …), carries a v4-era decorative banner "D4 Symmetry Group: Eight Magic Squares → One 3D Magic Gem", and shows four squares with eight 3D views, while the caption says "the eight images of the Lo Shu … each shown with its gem." The change log admits the figure was "not regenerated". Resolve: regenerate (panels a–d suffice; the D4 strip adds nothing a sentence does not) or drop it.

**2. [MAJOR] Attribution of the semi-magic inertia invariance (Cor. 4.13, Intro Contribution 1, §6.1).** The paper writes "I(S) = n²(n⁴−1)/12 for every semi-magic square S (no diagonal condition is needed)" and in the Introduction "Loly's invariance … holds for all semi-magic squares (Corollary 4.13)", presented as an output of the hierarchy. Loly's argument uses only row and column sums (I = Σ_i y_i²·rowsum + Σ_j x_j²·colsum) and his result is already stated for semi-magic squares (see e.g. the Science News account of Loly's note, and OEIS A126275). Resolve: state plainly that the semi-magic case is Loly's, and that Cor. 4.13 only re-derives it; the new content is the decomposition (12) into a degree-two cross-moment plus a constant. Also: Loly's invariant needs only ⟨x²+y², z⟩ = 0, a single combination, not both degree-2 conditions; "is the degree-two statement" is loose.

**3. [MAJOR] Theorem 4.11 is a lemma; the genuine content is Prop. 4.14(3).** Parts (a)–(c) say: a vector in Rⁿ orthogonal to 1, x, …, x^k is zero iff k ≥ n−1, witnessed by the alternating binomial vector. This is the invertibility of a Vandermonde matrix; calling it the paper's first "Theorem" and headline contribution oversells it. The non-trivial and new observation is 4.14(3): integrality plus the bound |γ_j| ≤ n²(n−1)/2 forces k*(n) ≤ n−2 for n ≥ 14. Resolve: demote 4.11 to a lemma, promote 4.14 to the theorem, and say in "What is and is not new" that the hierarchy itself is elementary.

**4. [MAJOR] "k*(n) = n−1 for 3 ≤ n ≤ 13" (Contribution 1, Prop. 4.14, Remark 4.15, Open Q. 2) rests on witnesses found by a "randomised swap search (verify_theory.py)" that are not in the paper.** For n=3,4 the witnesses are printed; for 5 ≤ n ≤ 13 the reader has nothing to check. Resolve: either print the witnesses (a 13×13 array is small; one table in the appendix) or state in Contribution 1 "(computer-verified; witnesses in the ancillary files)". As written the Introduction states it as a fact on par with the proved statements.

**5. [MAJOR] The Magic Gem is used only in §5.5–5.7 (and §4.5, which the paper itself calls "uninformative").** The title, abstract and §3 lead with the hull; §6.2 then concedes "The counting in this paper … neither of which needs the orthogonality language", and nothing in §4 or §5.1–5.4 uses the hull. The paper is honest about this, which I credit, but a title should describe the content. Resolve: either retitle (e.g. "Magic squares as orthogonality conditions on a height function, with a classification of the 880 order-four gems") or move the gem material to the front and make §4 the supporting theory. I will not insist on which, but one of the two.

**6. [MAJOR] Length: 26 pp. for ~5 pp. of new mathematics.** Concrete cuts, in order of priority:
   (a) The paragraph "Corrections relative to version 4" (p. 2), Remark 4.5 (p. 7, ~20 lines), Remark 4.20, and the last sentences of §5.3, §5.4 ("the estimate … given in the previous version"), and the Conclusion's list of withdrawn claims. A journal paper is not a changelog for an unpublished preprint. One sentence ("An earlier preprint used an asymmetric energy; all statistics here use (6)") is enough.
   (b) §4.5 / Prop. 4.22 (inertia tensor of the gem): the paper says it is uninformative. One remark.
   (c) §6.3 and Table 6 (local search): two elementary heuristics on n ≤ 6, 200k runs, no comparison, admitted to be "small". Cut or reduce to three sentences.
   (d) Eq. (20) with the degree-11 polynomials: appendix.
   (e) The conjectural |L_5|, |L_6| Monte Carlo numbers in §5.4: a remark at most.
   (f) Figure 3 (six 4×4 arrays): a 6-row table or two examples.
   With (a)–(f) the paper is 18–20 pp. without losing a result.

**7. [MINOR] Cor. 5.3, proof.** Two gaps to close in one sentence each: (i) Hoeffding's condition should be written with |d_N(i,j)|^r (odd r); (ii) the Cramér–Wold step applies Hoeffding to a fixed linear combination Σα_kT_k of the *standardised* statistics; the paper bounds κ_r for each test function but not for the combination (it follows from Minkowski and the lower bound Var ≥ (1−o(1))Σα_k², but say so). Also "Hoeffding-type limit law" in the abstract is just Hoeffding's theorem applied; say "by Hoeffding's CLT".

**8. [MINOR] §5.5, "denominators are 1, 2, 3, 6 as they must be for lattice polytopes of the doubled lattice".** The doubled-lattice argument only gives volume ∈ (1/48)Z. The correct reason: all three coordinates are half-odd integers, so translating by (½,½,½) makes every gem a lattice polytope in Z³ and vol ∈ (1/6)Z. (The observed denominators are right; the justification is not.)

**9. [MINOR] Contribution 5 / Prop. 5.6(1): "no two gems coincide as point sets".** For the full 16-point sets this is trivial — the point set *is* the arrangement. The non-trivial statement is about hull-vertex sets (Prop. 5.6(1)); the Introduction should say "hull-vertex sets". Likewise "the same holds for the full 16-point sets" in 5.6(2) is only interesting for congruence, not identity.

**10. [MINOR] Background/Intro wording on the polytope literature.** Intro: "semi-magic squares with line sum t are the lattice points of the t-th dilate of the Birkhoff polytope, their counting function is an Ehrhart quasi-polynomial [20, 9]" — for the Birkhoff dilates (nonnegative integer matrices) the counting function is a *polynomial* (Stanley; §2.4 says so correctly); the quasi-polynomial arises for the distinct-entry/inside-out count [4, 3]. Also "semi-magic squares" here conflicts with Definition 1.1 (distinct entries 1..n²); say "nonnegative integer matrices with equal line sums".

**11. [MINOR] Remark 5.4:** "the two energies take 346 and 177 distinct values respectively" — the preceding sentence lists E_full first; make the order explicit. Table 2, column "KS": say against which distribution (the Gaussian mixture) in the column header.

**12. [MINOR] Prop. 4.14 statement (1) "k*(n) ≤ n−1 for all n" is just 4.11(b); (3) should be the headline. Open question 2's heuristic "k*(n) = O(log n)" needs one line of justification (2^k vs n³) or should be dropped.**

**13. [MINOR] Section 5.4, Gaussian estimate.** Fine as an honestly labelled heuristic. But "the achievable values … form the full lattice Z⁴ (Smith normal form of the single-transposition steps, n ≤ 8)" — say what was computed: the Z-span of the step vectors of all transpositions has index 1 in Z⁴. Also note that mean = target holds by symmetry, not by (2).

**14. [MINOR] References.** [8] Dürer's engraving is not a bibliographic reference; cite it in the text. [4] has a stray "MR 2254310" that no other entry has. [13] "88.30 The invariance…" — the Gazette note number should be dropped or formatted as in the journal ("Note 88.30"). [21] http → https, and "Schroeppel, 1973" (p. 3) has no reference; cite Gardner, Sci. Amer. 234 (Jan. 1976) or Schroeppel's note. The Rogers–Loly DOI should be checked (change log says it was not). "Frénicle de Bessy in 1693" — he died in 1675; the 880 were published posthumously in 1693, say so or cite.

**15. [MINOR] Figures 4, 5.** Fine, captions accurate; Fig. 4(c)'s bar chart is unreadable at this size (labels 1,2,3,…,32 stacked); a short table or the sentence already in the text suffices. Fig. 2(c) duplicates Table 2.

**16. [MINOR] Tone.** "What remains is a small set of exact statements about a classical object, and a polyhedron that is pleasant to look at" (Conclusion) is fine; but the abstract's "(v) a classification of the 880 order-four gems" should say "exact computation" rather than "classification" unless some structure (beyond counting types) is identified — the only structural statement is congruence classes = complement orbits, which is the one worth keeping in the abstract.

## 4. What would change my recommendation

To **Minor revision / accept**: fix Figure 1; attribute the semi-magic inertia invariance to Loly; relabel 4.11 as a lemma and 4.14 as the theorem; print or reference the n ≤ 13 witnesses; cut items 6(a)–(d); retitle or reorder. All checkable in a diff.

To **Reject**: if the author insists on keeping the changelog material, the local-search section and the v4 postmortems in a journal version, or on presenting Theorem 4.11 as the main result.

## 5. Confidential comments to the editor

The mathematics is correct — I rederived every closed form, re-enumerated n=3 exhaustively, recomputed the n=4 variances by an independent method, regenerated the 880 hulls with my own code and reproduced every number in §5.5, and ran the Siamese proof script. The author has done what previous reviewers asked and is now honest to a fault about what is and is not new. What remains is modest: one cute integrality argument (Prop. 4.14(3)), exact random-arrangement moments, a two-line swap formula, two exact enumerations and a computer-assisted 12-vertex theorem. It is too long and too technical for Mathematics Magazine. Trimmed to ~18 pp. with the title matched to the content, it is publishable in Experimental Mathematics or a venue such as Integers / J. Integer Sequences / Involve. I would be willing to see a revised version.
