# Magic Gems — Revision Plan for v5 (2026-10-07)

Paper: arXiv:2512.09170 (v4, 28 Dec 2025). Source: `arxiv_submission/`.
Inputs considered: v4 manuscript, four simulated reviews (Beck, Diaconis, Loly, confidential),
the Toronto review, three Strancher rounds, `internalReview/deepFollowUp`, the code in `Analysis/`,
literature search, and fresh computations run today (see "Verified today").

---

## 1. Honest assessment

The paper has one genuinely good idea (the Magic Gem representation + the "constraints as orthogonality
to test functions" lens) wrapped around a main theorem that two of four reviewers correctly call a
tautology, several computational claims that are artifacts, and ~30% too much prose. Beck and the
confidential reviewer are right about the mathematics; Diaconis is right that the *framing* is valuable.
Loly is right that attribution and physics are under-developed.

### Verified today (these change the plan)

| Finding | Evidence | Consequence |
|---|---|---|
| **E_full as defined is NOT D4-invariant.** Dropping row/column n−1 from the sum makes E(S) ≠ E(rot90 S) (e.g. 0.0117 vs 0.0078 for a swapped n=4 square). | direct computation on the 880 squares | Every E_full statistic in the paper (perturbation gaps, "bands", local-minima counts) is basis-dependent. Must redefine E_full symmetrically (all 2n indicators, or an orthonormal basis of the line-sum space) and recompute. |
| **The "trimodal structure" is an arithmetic artifact.** Single-swap gaps take exactly the values d²·k/256 (d = value difference, k = number of affected indicator terms). With the asymmetric energy the min-gap multiset is {1/256: 252, 2/256: 604, 3/256: 24}; with the symmetric energy it is {2/256: 432, 3/256: 420, 4/256: 28}. | direct computation | Delete the trimodal claim and `fig_n4_bands_geometry`; replace with an exact swap-gap formula (a two-line proposition) and the exact 1/n⁴ scaling of the minimum gap. The gap values in Table 1 (0.0039 etc.) are also inconsistent with the paper's own figure caption ranges (0.025–0.040). |
| **Exact random-arrangement moments exist.** For a uniform permutation, E[Cov(X,Z)²] = Var(X)Var(Z)/(n²−1) = (n⁴−1)/144 exactly; E[Cov(D,Z)²] = n(n²−n)Var(Z)/((n²−1)n⁴). Monte Carlo agrees to 3 digits for n=3..6. | Hoeffding-type permutation variance identity + simulation | Replace "quadratic scaling with R²>0.99 on three points" by a theorem (mean grows like n⁴ under the paper's 1/n² normalization) plus the combinatorial CLT (Hoeffding 1951) giving the limiting weighted-χ² shape. Drop the binned "landscape entropy" entirely (it is binning-dependent and trivially scale-free). |
| **Reported landscape statistics do not match the stated definition.** Paper: mean E_low(n=3)=4.44, mode 3.12. Definition in the paper gives mean 1.48 (exhaustive n=3 is cheap to check). | simulation vs. paper table | Recompute all of Table 3 / Fig. 6 / Fig. 7 from the written definition. |
| **880 gems are geometrically diverse but far from "canonical".** Hull vertex counts 8–16 (12 is modal: 380/880); 155 distinct volumes; 329 distinct (vertex-count, volume) pairs. | direct computation | The class→gem map is not injective on simple invariants. A real classification (f-vectors, combinatorial types, congruence classes) is the geometric content Beck asked for. |
| **Loly's moment-of-inertia invariance IS the paper's "higher-order moment vanishing".** Σ s_ij(x²+y²) = N·Cov(Z, X²+Y²) + const, and Cov(Z,X²)=0 for any square with equal column sums. | algebra | State this explicitly: it gives Loly full credit, proves his 2004 result in one line, and shows Loly's statistic is the *degree-2* member of the test-function hierarchy. Also the diagonal of the inertia tensor is arrangement-independent for *every* permutation (fixed z multiset) — so "principal moments" are trivial and should be stated as such. |
| The 12-hull-vertex pattern for Siamese squares (n=5,7,9) and the exact variance formulas from `deepFollowUp` are correct but minor. | prior exploration | Keep variance formulas (one line). Try to prove the 12-vertex statement; otherwise one sentence as an observation. |

### Decision: one paper, not two
Neither half (theory note / computational geometry) is large enough to stand alone. The right product is a
**single, shorter (~18–20 pp), honestly framed paper** whose contributions are:

1. The Magic Gem representation and its D4-invariance (keep; it is the memorable idea).
2. **Projection Lemma** (demoted from "Main Theorem"): line-sum constraints ⟺ f ⟂ a (2n−1)-dim test-function space; E_full = ‖P_W f‖². Stated as a reformulation, not a discovery.
3. **Moment-hierarchy theorem** (new, provable): with polynomial test functions of degree ≤ k in x and y, "all cross-moments E[X^m Z]=E[Y^m Z]=0 for m≤k" characterizes equal row/column sums iff k ≥ n−1. The paper's E_low is the k=1 truncation; Loly's inertia invariance is the k=2 statement. Explains why n=3 "works" with k=1 only because of the permutation constraint (verified exhaustively).
4. **Exact theory of the random-arrangement energy** (new): closed-form mean and variance of E_low and E_full, limiting weighted-χ² law by the combinatorial CLT, confirmed numerically for n=3..8. Replaces all scaling fits and the entropy claim.
5. **Exact single-swap gap formula and isolation for all n** (new, replaces computational "for n=3,4" proposition and the trimodal claim). Minimum gap = c·d_min²/n⁴ with d_min the smallest value difference among cells sharing a line.
6. **Exact enumeration of the low-mode-balanced class for n=4** (new number): |{S : E_low(S)=0}| via meet-in-the-middle over 8/8 cell splits, with breakdown magic / semi-magic / diagonal-only / other. Plus the n=3 count (8 = magic only, and the 760 with Cov(X,Z)=Cov(Y,Z)=0).
7. **Geometric classification of the 880 n=4 Magic Gems** (new): f-vectors, number of combinatorial types, congruence classes, volume distribution; whether class→gem is injective. Siamese 12-vertex result if provable.
8. Visualization, web app, reproducible code (keep, condensed).

Target: arXiv v5 first (needs user go-ahead). Venue recommendation: **Mathematics Magazine** or **The Mathematical Intelligencer** (new small theorems + strong exposition); *Experimental Mathematics* only if items 6–7 produce something surprising.

---

## 2. Section-by-section plan

Format: **Have** → **Need** → **Do**.

### Title / abstract
- Have: "A Polyhedral Framework…Connecting Combinatorics, Geometry, and Linear Algebra"; abstract says "we introduce", "prove… if and only if".
- Need: modest, concrete; no claim of characterization-as-discovery.
- Do: Title → *Magic Gems: Magic Squares as Orthogonality Conditions on a Height Function* (subtitle dropped). Abstract lists the 7 concrete contributions above in ≤180 words; "we introduce"→"we study"; name Loly in the abstract.

### 1 Introduction
- Have: history, definition, construction story, contributions paragraph that oversells Thm 3.17.
- Need: explicit positioning vs Loly (2004, Rogers–Loly 2004), Ahmed–De Loera–Hemmecke (2003), Beck–van Herick (2011), Stanley (1973)/Ehrhart; statement that E_full=0 ⟺ magic is a reformulation.
- Do: rewrite contributions as the numbered list above; add one paragraph "What is and is not new"; cut the Pickover/Dürer colour to one sentence; keep web-app sentence (described, per Diaconis).

### 2 Background
- Have: enumeration facts, D4, convex hulls, covariance vs inertia (vague).
- Need: precise inertia↔covariance relation (I_jk = N(δ_jk tr Σ − Σ_jk)); Hoeffding's permutation-statistic variance identity and combinatorial CLT; brief polytope-literature paragraph (semi-magic squares = lattice points in dilates of the Birkhoff polytope; magic squares via inside-out polytopes).
- Do: move §5.6 "Related work" here (per Loly); add the two tools (permutation variance identity, CLT) as Lemma 2.x with citations; delete the unused Delaunay/face-lattice generalities.

### 3 Methodology → rename "The Magic Gem and the orthogonality reformulation"
- Have: construction, D4-invariance, vector representation (two subsections saying the same thing), forward proposition, insufficiency remarks (3 remarks + figure), diagonal indicators, perturbation proposition, energy landscape with Theorem 3.17, low-mode definition, isolation proposition (computational), inertia tensor.
- Need: D4-invariant energy; demoted theorem; the hierarchy theorem; exact swap formula; remove duplication.
- Do:
  - 3.1 Construction + Prop (D4 invariance) with the explicit isometry (Diaconis's wording). Keep Fig. 1 but reduce the eight-variant block to a 2×4 strip (half page).
  - 3.2 Test functions and the Projection Lemma: define W = span{R_k, C_ℓ, D_main, D_anti} ⊖ constants, dim 2n−1 (check n=3 independence); E_full := ‖P_W f‖² using an *orthonormal* basis of W (basis-independent, D4-invariant). Lemma: E_full(S)=0 ⟺ S magic. Remark stating plainly that this is a restatement of the definition and that the value lies in what follows.
  - 3.3 The moment hierarchy: E_k with polynomial test functions; Theorem (k ≥ n−1 iff semi-magic); Corollary: E_low = E_1 + diagonals; Corollary: Loly's inertia invariance (k=2 case, holds for semi-magic squares). Keep the 4×4 counterexample as one example (delete two of the three remarks).
  - 3.4 Single-swap formula: ΔE for swapping cells a,b with values differing by d, in terms of which lines they share; Corollary: every magic square is a strict local minimum for all n (replaces Prop 3.19); Corollary: Δ_min = c·d_min²/n⁴ exactly.
  - 3.5 Inertia tensor: diagonal entries arrangement-independent (one line); off-diagonals = −N·Cov; Loly's 2D inertia = degree-2 moment. Delete the vector-representation subsection (fold one sentence into 3.1).

### 4 Results → "Computations"
- Have: n=3 exhaustive; perturbation 9-panel figure + Table 1 (artifact bands); 3×3 four-panel figure; n=4 low-mode vs full scatter; "geometric structure of n=4" (speculation only); cross-order comparison figure + Table 2; large-scale landscape (460M samples, 9-panel figure, Table 3 with inconsistent numbers, scaling fits, entropy); 4-panel scaling summary; verification summary list.
- Need: everything recomputed with the symmetric energy and the stated normalization; artifacts removed; two new computational results (low-mode count n=4; 880-gem classification).
- Do:
  - 4.1 n=3 exhaustive: counts (8 magic; 760 with first-moment balance; local minima counts recomputed with symmetric E_full and E_low). One table.
  - 4.2 Random-arrangement energy: theorem vs Monte Carlo for n=3..8 (exhaustive n=3). **One** figure: histogram overlays with the predicted weighted-χ² density, and mean/variance vs n on log axes with the exact curves. Delete entropy, delete Fig. 7 (4-panel scaling), delete 9-panel landscape figure.
  - 4.3 Swap gaps: verify exact formula on all 8 + 880 + 35 squares (100% agreement); one small table; delete the 9-panel perturbation figure.
  - 4.4 The low-mode-balanced class for n=4: exact count, breakdown table, gallery figure of 6 examples (reuse `zero_energy_nonmagic_examples` style). Comment on rarity (count/16!) explaining why sampling failed.
  - 4.5 Geometry of the 880 gems: f-vector table, number of combinatorial types, congruence classes, volume histogram, injectivity statement; one figure with the extreme gems (8-vertex and 16-vertex) rendered. Siamese 12-vertex result (theorem or observation).
  - 4.6 Cross-order gem comparison: keep Fig. 5 top row only (3 gems side by side) and the hull-fraction panel; drop the M(n) panel.

### 5 Discussion
- Have: ~9 pages: zero-covariance meaning, vector interpretation, physical/algebraic, ground states, scaling, parity, rarity, related work, limitations, applications, algorithms.
- Need: ≤3 pages; no poetry; no claims beyond results.
- Do: four short subsections — (i) what the orthogonality lens buys (hierarchy, Loly, statistics for random arrangements); (ii) what it does not (it is a reformulation; low-mode zeros; non-injectivity of gems); (iii) algorithms: one paragraph + one small experiment: swap-descent/annealing on E_full for n=4,5 with success rates vs. restarts (gives Diaconis his worked example, cheap); (iv) open questions (asymptotic count of low-mode class, combinatorial types for n=5, semi-magic/pandiagonal gems). Delete §5.3 scaling, §5.4 parity, §5.5 rarity, §5.8 applications beyond two sentences.

### 6 Conclusion
- Have: 1.5 pages, restates everything, "stones in valleys".
- Do: half a page; one closing sentence may keep the gem image.

### Appendix
- Have: duplicate proof of Prop 3.6, duplicate statement of theorem, counterexample, computational methods, summary table.
- Do: delete duplicate proofs. Keep: computational methods (hardware/software, seeds, meet-in-the-middle algorithm description, hull-type algorithm), the 4×4 counterexample table, link to code. Fix "Mac Studio M5" → actual hardware.

### References
- Add: Rogers & Loly 2004 (Am. J. Phys. inertia tensor of a magic cube); Loly & Rogers 2004 CUPJ note (if locatable); Stanley 1973 (linear homogeneous Diophantine equations and magic labelings); Ehrhart 1973; Hoeffding 1951 (combinatorial CLT); Diaconis & Gangolli 1995; Goldstein (Classical Mechanics); Cameron–Rogers–Loly 2013 (signatura); Trump's site with access date. Verify every DOI via `Analysis/scripts/generate_reference_audit_md.py`.

### Figures (target: 6, all vector PDF, regenerated from code)
1. Construction + D4 strip (revised Fig. 1)
2. 3×3 analysis (keep, 4 panels)
3. Random-arrangement energy: theory vs simulation (new)
4. Low-mode-balanced gallery for n=4 (new)
5. Gem geometry of the 880: f-vector/volume distributions + extreme gems (new)
6. Cross-order gems (reduced Fig. 5)
Delete: Complete_Perturbation_Analysis_n345.png, energy_landscapes_comparison.png, Figure7_ScalingSummary.png, fig_n4_bands_geometry.pdf, fig_lowmode_failure_n4.pdf (merge into 4), fig_energy_comparison_n4.pdf (fold one panel into 3 or drop).

### Code / ancillary
- Fix `compute_full_magic_energy` to the symmetric definition; add `energy_hierarchy(S,k)`, exact-moment formulas, swap-gap formula, meet-in-the-middle enumerator, hull-type classifier; regenerate `anc/analysis_code.zip`; README reproducibility steps.

---

## 3. Execution (subagents)

Phase 1 (parallel, independent, write only inside their own directories):
- **A. Theory writer** → `sections/drafts/theory.tex` + `Analysis/revision/verify_theory.py` (items 2,3,5 of §1 + inertia/Loly link; all proofs complete; numerical sanity checks).
- **B. Random-energy** → `Analysis/revision/random_energy/` (closed forms, CLT statement, exhaustive n=3 recount, MC n=4..8, Fig. 3, LaTeX fragment with table).
- **C. Low-mode enumeration** → `Analysis/revision/lowmode_n4/` (exact count via meet-in-the-middle in numpy; breakdown; Fig. 4; LaTeX fragment).
- **D. Gem geometry** → `Analysis/revision/gem_geometry/` (880 hulls: f-vectors, combinatorial types, congruence classes, volumes, injectivity; swap-gap verification with symmetric energy; Siamese 12-vertex; Fig. 5; LaTeX fragment).

Phase 2 (sequential):
- **E. Integrator/editor** → rewrites all `sections/*.tex`, bib, main.tex, figures dir; compiles; ≤20 pp.
- **F. Adversarial referee (Beck persona) + fix pass**; reference audit; final compile; change log `CHANGES_V5.md`; refresh `anc/analysis_code.zip`.

Not done without the user's go-ahead: arXiv upload (v5) and any journal submission.

---

## 4. Phase 3 protocol: adversarial review rounds (added 2026-10-07 at the user's request)

- Referee A (persistent agent, Beck persona): rigorous combinatorics; lists numbered points with severity (blocking / major / minor), states explicitly what would change the recommendation. Checks proofs line by line and reruns verification scripts when in doubt.
- Referee B (persistent agent, Loly persona): attribution, physics, consistency between claims and computations, exposition.
- Author (persistent agent): for every point chooses CONCEDE (edit LaTeX, cite the change) or REBUT (argue, with computation or proof); writes `review_rounds/roundK_response.md`; no sycophancy, no unjustified changes; recompiles.
- Editor (lead session): adjudicates disputes, decides to continue or stop. Stop when both referees recommend accept/minor, or after 3 rounds.
- Files: `arxiv_submission/review_rounds/roundK_refA.md`, `roundK_refB.md`, `roundK_response.md`, `editor_decisions.md`.
