# Changes in v5 (relative to arXiv:2512.09170v4)

Manuscript: `arxiv_submission/main.tex` + `sections/{abstract,introduction,background,gem,theory,computations,discussion,conclusion,appendix}.tex`.
Compiled PDF: `magicGemV5.pdf` (26 pages at 10pt; v4 was 34 pages at 11pt). Zero errors, zero undefined references or citations, zero overfull boxes.
New title: *Magic Gems: Magic Squares as Orthogonality Conditions on a Height Function*.

## Corrections to v4 (stated in the paper, Introduction, paragraph "Corrections relative to version 4")

1. **Energy definition.** v4's `E_full` dropped row and column `n-1` and was therefore not `D4`-invariant. v5 uses the symmetric sum over all `2n+2` lines, `N^2 E_full = sum of squared line deviations` (Definition 4.2, Remark 4.5 with an explicit 4x4 example).
2. **Sampled landscape statistics** (v4 Table 3, Figs. 6-7: means 4.44 / 12.04 / 26.00, mode 3.12, "landscape entropy", quadratic fits with R^2 > 0.99) were computed with the diagonal terms weighted by `n^2` relative to the stated definition. All withdrawn; replaced by exact closed forms (Proposition 5.1) and a limit law (Corollary 5.3).
3. **"Trimodal bands" of swap gaps** (v4 Fig. 2, Table 1, Sec. 4.3): an arithmetic artifact. Gaps are exactly `d^2 m / n^4` (Theorem 4.17); the "modes" were `d^2 m in {2,3,4}` (Remark 4.20, Table 3).
4. **Local minima for n = 3**: v4's "24 under E_full" used the asymmetric energy; the symmetric energy has 16 (8 magic + 8 non-magic at `E_full = 2/81`). The 344 under `E_low` stands (Table 1).
5. **Rarity of low-mode zeros**: v4 estimated `P(E_low = 0) < 1e-8` for n = 4 and explained the sampling failure by rarity; the exact value is `7.0e-7` (`|L_4| = 14,639,440`), and the earlier failure is not explained by rarity (Section 5.4).
6. **Minimum-gap scaling**: v4 claimed `1/n^2`; exact result is `Theta(n^-4)` with constants 2 and 6 (Corollary 4.19).
7. v4's "Mac Studio M5" hardware statement replaced by the actual machine (Apple M4 Max, 16 cores, 128 GB).
8. v4 Table 2 ("hull vertices (typical) 16 for n = 5", volume 95.0 for n = 4) replaced by exact values for named squares (Durer: 12 vertices, volume 92; Siamese 5: 12 vertices, volume 830/3).

## By reviewer

### M. Beck (simulated; rigour, novelty, polytope literature)
- "Theorem 3.17 is circular": demoted to the **Projection Lemma** (Lemma 4.7/4.8) with Remark 4.9 stating plainly that it is a restatement of the definition; the Introduction says "We make no claim that the energy reformulation by itself is a result."
- "Polytope connection is not novel / engage with Ehrhart theory": new Background 2.4 on Birkhoff-polytope dilates, Stanley 1973, Ehrhart 1973, inside-out polytopes (Beck-Zaslavsky), Beck-van Herick, Ahmed-De Loera-Hemmecke; explicit statement that the Magic Gem is a polyhedron attached to one square, not the polytope whose lattice points are the squares. New "What is and is not new" paragraph in the Introduction.
- "Trimodal structure abandoned": replaced by the exact swap formula (Theorem 4.17, Lemma 4.18, Corollary 4.19) and exact verification on all 105,600 + 288 swaps (Section 5.3).
- "Face structure / combinatorial types of the 880 gems": new Section 5.5: 39 f-vectors, 352 combinatorial types, 616 congruence classes = complement orbits, injectivity as point sets, Dudeney cross-tabulation summarised; Figure 4.
- "Three data points for quadratic scaling": all fits removed; exact means/variances for all n (Proposition 5.1), Monte Carlo n = 3..8 with standard errors (Table 2).
- "Actual enumeration": exact count of the low-mode class for n = 4 by meet-in-the-middle (Proposition 5.5, Table 4).
- "30% shorter, remove duplicate proofs, appendix duplication": 34 -> 26 pages; appendix now contains computational methods only; vector-representation subsection, three insufficiency remarks (one example kept), computational isolation proposition, 9-panel and 4-panel figures all removed.
- "Metaphorical language": removed ("stones in valleys", "remarkable", "striking"); neutral tone throughout.
- "Pickover citation / web app URL": Pickover kept only as a general history reference in one sentence; the web app is described in one sentence (per Diaconis) and in the appendix.

### P. Diaconis (simulated; framing, algorithms, random arrangements)
- "Derive expected covariance for random arrangements": Proposition 5.1 gives exact `E[E_low] = (n^2+1)(n^4-n^2+12n-12)/(72n^2)`, `E[E_full] = (n^4-1)/(6n^2)`, exact variances, and Corollary 5.3 the Hoeffding CLT limit `E_low/E[E_low] -> Exp(1)`; Figure 2.
- "Worked algorithmic example": Section 6.3 with Table 6 (swap descent 19.5% / 1.15% / 0.79% success for n = 4,5,6; simulated annealing 100% / 78% / 50%), including what the non-magic local minima look like (a diagonal off by one).
- "Reframe E_low positively as a hierarchy": Section 4.3 (moment hierarchy, Theorem 4.11) with `E_low` as the degree-one truncation (Corollary 4.12) and Loly's inertia as the degree-two member.
- "Explicit isometry in Prop 3.4": Proposition 3.3 now states `g^(x,y,z) = (g(x,y), z)`.
- "Describe the web application": one sentence in the Introduction.
- "Clarify 'zeros found: 0'": the table is gone; Section 5.4 gives the exact count and explains the earlier sampling result.
- "Birkhoff polytopes / contingency tables with fixed margins": Background 2.4 cites Diaconis-Gangolli 1995.

### P. Loly (simulated; attribution, physics)
- Loly named in the abstract; "we study" instead of "we introduce"; explicit positioning in the Introduction.
- Precise inertia-covariance relation `I_jk = N(delta_jk tr Sigma - Sigma_jk)` in Background 2.2 (with Goldstein cited), and the distinction between the 3D unit-mass tensor and Loly's planar value-weighted moment made explicit.
- **Corollary 4.13**: Loly's invariance `n^2(n^4-1)/12` proved as the degree-two case of the hierarchy, valid for all semi-magic squares; OEIS A126275 values listed.
- **Proposition 4.22**: all three principal moments of the 3D gem computed (`n^2(n^2-1)(n^2+2)/12` twice, `n^2(n^2-1)/6`), shown to be the same for every arrangement; discussion states this is uninformative and that the informative inertia statement is Loly's planar one.
- Higher-order moment vanishing is now Theorem 4.11(a).
- Rogers-Loly (inertia tensor of a magic cube, 2004), Cameron-Rogers-Loly 2013 and Loly 2007 cited; semi-magic / Franklin gems listed as open question 5.
- "arrangement" vs "configuration": "arrangement" used throughout.
- Related work moved from the Discussion to the Background.

### Confidential reviewer (tautology; "AI-polished"; strip to a short note)
- The energy equivalence is explicitly a reformulation (Remark 4.9); the paper's claims are the five numbered contributions, each with a proof or an exact computation.
- Length reduced; no checklists, no tables of "physical intuition vs formalisation"; neutral prose.
- Every exact statement in Section 4 is checked by `Analysis/revision/theory/verify_theory.py` (21/21 pass); every number in Section 5 comes from a results JSON in `Analysis/revision/*`.

### Toronto review (Theorem 3.1 false; semi-magic inconsistency; computational details)
- The false "Cov(X,Z)=Cov(Y,Z)=0 iff semi-magic" claim is gone; Theorem 4.11 and Proposition 4.14 give the correct statement with the exact degree threshold, and Remark 4.16 explains why n = 3 misleads (760 degree-one arrangements, 72 semi-magic = degree-two).
- Semi-magic now defined once (Definition 1.1) and used consistently.
- Floating-point tolerances no longer matter: all counts and gaps are in exact integer/rational arithmetic (Appendix A).
- Vector figures only (all PNGs removed).

### J. Strancher rounds 1-3 (E = 0 does not characterise for n >= 4; projection viewpoint)
- The projection viewpoint is now the organising principle of Section 4 (Lemma 4.7).
- The 4x4 counterexample is kept as Remark 4.3 and generalised by the exact count (Proposition 5.5) and gallery (Figure 3).
- "880 squares" vs "880 equivalence classes" wording fixed throughout ("essentially different").

## Figures
Kept: `fig02_combined_construction_symmetries.pdf` (Fig. 1; caption now describes the D4 strip; not regenerated).
New: `fig_random_energy.pdf` (Fig. 2), `fig_lowmode_gallery.pdf` (Fig. 3), `fig_gem_geometry_880.pdf` (Fig. 4), `fig_gems_cross_order.pdf` (Fig. 5).
Dropped: `fig03_combined_3x3_analysis.pdf` (for length; the Lo Shu gem is in Figs. 1 and 5), `fig06_combined_comparison_scaling.pdf`, `Complete_Perturbation_Analysis_n345.png`, `energy_landscapes_comparison.png`, `Figure7_ScalingSummary.png`, `fig_energy_comparison_n4.pdf`. `fig_lowmode_vs_full_n4.pdf` is in `figures/` but not used.

## References
Added: Stanley 1973, Ehrhart 1973, Hoeffding 1951, Wald-Wolfowitz 1944, Imhof 1961, Diaconis-Gangolli 1995, Rogers-Loly 2004 (Am. J. Phys.), Cameron-Rogers-Loly 2013, Goldstein 2002, Ziegler 1995, Dudeney 1917; Trump's site with access date.
Removed (no longer cited): Ahmed 2004 (Franklin squares), Barvinok 2002. The unverified `rogers2005rotational` entry was not used.

## Items left for the referee pass (Phase F)
- Verify the DOI of Rogers-Loly 2004 (`10.1119/1.1643371`) and the Dudeney 1917 publisher line; verify the Schroeppel 1973 attribution for the order-5 count.
- Refresh `anc/analysis_code.zip` with `Analysis/revision/*` (the appendix refers to ancillary files containing the revision scripts and JSON results).
- Page count is 26 at 10pt (target was 18-22). The theory section (8 pp) was taken essentially as delivered; the Siamese proof (1.5 pp) and the variance closed forms could be moved to an appendix or cut if a shorter paper is wanted. At 11pt the same text runs to 32 pages.
- The Dudeney cross-tabulation (V vs. group) was reduced to a sentence; the full table is in `Analysis/revision/gem_geometry/fragment.tex` if wanted back.
- Section 5.4's claim that the `10^8`-sample Monte Carlo found 61 members of `L_4` is taken from `Analysis/revision/random_energy/SUMMARY.md`.

## Round 1 (2026-10-07): response to referees A and B

Full point-by-point response: `review_rounds/round1_response.md`. Rulings: `review_rounds/editor_decisions.md`.
Compiled PDF: `magicGemV5.pdf`, **28 pages at 11pt** (a4, 0.9 in margins, small captions); zero errors, zero undefined references/citations, two overfull boxes < 5 pt; Type 1 fonts only (the `[T1]{fontenc}` line was removed: without cm-super it produced bitmap Type 3 text in v5).

### Content
- **Loly attribution (A2, B1, B2, B3, B6).** Cor. 4.12 "Loly's invariant from the hierarchy": I = N Cov(Z, X^2+Y^2) + n^2(n^4-1)/12; Loly's value iff the single condition Cov(Z, X^2+Y^2) = 0, implied by but much weaker than the degree-2 conditions (n = 3: 24,192 arrangements with I = 60 vs 72 degree-2). Semi-magic validity and the I_x = I_y split attributed to Loly. Rogers-Loly 2005 (EJP 26:809, DOI 10.1088/0143-0807/26/5/013) cited as the precedent for vanishing axial multipoles; pure vs mixed moments stated. Cameron-Rogers-Loly 2013 recast as a spectral reference.
- **New Cor. 4.13 (B19):** null distribution of Loly's I: E[I] = Loly's value, Var(I) = N^2 sigma_n^2 Var(X^2+Y^2) = n^4(n^4-1)(n^2-4)/1080 (n = 3: 30; n = 4: 2176/3), verified exactly (n <= 12), exhaustively (n = 3) and by Monte Carlo (n = 4, 5).
- **Theorem/Proposition swap (A3, A12):** moment hierarchy is Prop. 4.10 (Vandermonde); integrality result k*(n) <= n-2 for n >= 14 is Theorem 4.14; witnesses for k*(n) = n-1, 5 <= n <= 13 printed in Appendix C (computer-verified, re-checked by `check_round1.py`).
- **Sec. 5.4:** diagonal correlation corrected to -1/(n-1) (B7); "61 vs 70.0 +/- 8.4" (B11); the v4 sampling failure investigated: the archived data hold 10^5 samples per order (expected 0.07 members of L_4), no record of a 6x10^7 run; energy zero set and float tolerance excluded as causes.
- **Corrections list** (intro) now a 6-bullet list including the gap scaling, v4 Table 2, the withdrawn E_low characterisation claim and the sampling statement (B12).
- Minor: Hoeffding condition with |d|^r and the Cramer-Wold bound (A7); lattice-volume argument via the (1/2,1/2,1/2) translate (A8); "hull-vertex sets" (A9); Birkhoff polynomial vs inside-out quasi-polynomial (A10); "respectively" and KS caption (A11, B9); Smith-normal-form wording (A13); energy-as-label sentence (B8); 980 = 14^2 * 5 (B18); Open Question 2 heuristic justified (A12); product of inertia over the 880: |P_xy| takes 48 values in [0, 60], zero for 56 squares (B5).
- References: Durer entry removed (cited in text); MR number removed; Loly note title fixed; Trump https; Gardner 1976 added for Schroeppel's count; Frenicle "published posthumously in 1693".

### Length and structure (ruling 4)
Removed: Remark 4.5 (-> 3 sentences), Remark 4.20, Prop. 4.22 (-> Remark 4.20, 6 lines), bound (10), the |L_5|, |L_6| display, Fig. 3 (gallery), Fig. 5 (cross-order; Sec. 5.7 merged into 5.5), Tables 1 and 3 (folded into text), the duplicate computation paragraph in Prop. 5.4. Moved to appendices: variance closed forms (App. B), witnesses (App. C), Siamese proof Steps 2-3 (App. D). Compressed: intro, background 2.4, Lemmas 4.5/4.6/4.17 proofs, remarks, Cor. 5.2 proof, discussion, conclusion, Appendix A. Kept per rulings: compact algorithms paragraph + table (Sec. 6.2), corrections list.
Target of <= 22 pages not reached (28); candidate further cuts listed in the response under "Open items".

### Figures
- `fig01_construction_d4.pdf` (new Fig. 1, `Analysis/revision_round1/make_fig1.py`): construction (a)-(d) + 2x4 strip of the D4 images, each with its square printed; vector.
- `fig_gem_geometry_880.pdf` regenerated with a legible panel (c) (`make_fig_geometry.py`, a copy of `Analysis/revision/gem_geometry/make_figures.py` with only panel (c) changed; the original is untouched).
- `fig_siamese_layers.pdf` (new Fig. 4, `make_fig_siamese_layers.py`): five layers in the plane with the twelve vertex cells, and the reduced polytope with 16 facets.
- No longer used: `fig02_combined_construction_symmetries.pdf`, `fig_lowmode_gallery.pdf`, `fig_gems_cross_order.pdf`.

### Files
- `Analysis/revision_round1/`: `check_round1.py` (+ `results_round1.json`, `check_round1.log`), `make_fig1.py`, `make_fig_geometry.py`, `make_fig_siamese_layers.py`, `make_witness_table.py` (writes `sections/witnesses.tex`). Added to `anc/analysis_code.zip`.
- `Analysis/revision/` and `Analysis/src/` unchanged.

## Round 2 (2026-10-07): editorial pass after both referees recommended Minor revision

Response: `review_rounds/round2_response.md`. PDF `magicGemV5.pdf`: **27 pages at 11pt**, zero errors / undefined references, two overfull boxes < 5 pt.
- Appendix C: only the n = 5 witness printed; n = 6..13 in the ancillary `revision_round2/appendix_data.json` (+ `.md`), generated by `Analysis/revision_round2/make_appendix_data.py` from read-only `Analysis/revision/*` results; the same file holds the exact variance polynomials (Appendix B now gives only the structure and leading terms of (21)) and the 39 f-vectors with multiplicities (Table 3 reduced to counts by V; extreme and modal f-vectors named in the text). Appendix D trimmed. `anc/analysis_code.zip` refreshed (adds `revision_round2/`, `revision_round1/make_fig_geometry.py`).
- Theorem 4.14 states proved facts only; "k*(n) = n-1 for n <= 13" is Remark 4.15, flagged computer-verified.
- Abstract: variance formula dropped ("with an explicit variance"); item (i) split into short sentences.
- Cor. 4.12: the 24,192-vs-72 enumeration moved from the statement to the attribution paragraph; Cor. 4.13 hypothesis reworded ("invariant under relabelling of the values 1..N").
- Rogers-Loly attribution: "dipole and quadrupole moments of a magic cube" (two places).
- Corrections item (e): names v4's 6x10^7 (n = 4) and 4x10^8 (n = 5) claims; "the cause cannot be reconstructed from the repository" (also in Sec. 5.4).
- Table 2 placed in-flow after Prop. 5.4 so the Sec. 5.4 paragraph is unbroken; Fig. 3(c) tick labels thinned (1, 2, 3, 4, 8, 16, 32); Siamese proof sketch adds the edge-adjacency/connectivity step; Fig. 1 caption no longer relies on colour for the interior point.
- New file `ARXIV_SUBMISSION_CHECKLIST.md`.
