# Response to Round 2 (v5-r1 → v5-r2)

Compiled: pdflatex → bibtex → pdflatex ×2; zero errors, zero undefined references/citations, zero bibtex warnings; two overfull boxes of 2.3 pt (Table 1) and 4.2 pt (a bibliography URL). **27 pages at 11pt.** PDF: `arxiv_submission/magicGemV5.pdf`. New: `Analysis/revision_round2/make_appendix_data.py` → `appendix_data.json` / `appendix_data.md` (witnesses n = 5..13, exact variance polynomials, the 39 f-vectors with multiplicities), added to `anc/analysis_code.zip` as `analysis_code/revision_round2/`. `Analysis/revision` and `Analysis/src` untouched.

## Editor rulings (Round 2)

1. **Appendix C** now prints the n = 5 witness only, with a pointer to `revision_round2/appendix_data.json` for n = 6..13 (`sections/appendix.tex`, `sec:app_witnesses`). **Appendix B** keeps the structure of (21) (denominators, degrees, leading coefficients) and the leading terms; the polynomials are in the ancillary file (`sec:app_variance`). **Table 3** is a 4-row count table (squares / types / volumes / f-vectors by V) with the three extreme f-vectors and the modal one named in the text (`tab:gem-fvectors`, §5.5). **Appendix D** trimmed to the reduction summary, the eight inequalities, the incidence table and the closing argument (`sec:app_siamese`). Fig. 1 strip, §6.2 and Fig. 2 kept. Result 27 pp (target ≈ 26).
2. **Theorem 4.14** now states only the proved facts (k* ≤ n−2 for n ≥ 14; k* ≤ n−1; k*(3) = 2, k*(4) = 3 with witnesses). The n ≤ 13 equality is the new **Remark 4.15** (`rem:kstar_search`), titled "k*(n) = n−1 for 5 ≤ n ≤ 13; computer-verified". Contribution 1 points to the remark.
3. **Abstract:** variance formula replaced by "with an explicit variance"; item (i) split into four sentences (`sections/abstract.tex`).
4. **Cor. 4.12:** the 24,192-vs-72 count is out of the statement ("but it is much weaker than the degree-2 conditions (see below)") and in the attribution paragraph that follows; the proof sentence about the enumeration moved with it (`cor:loly`, `sections/theory.tex`).
5. **Attribution:** both places now read "as Rogers and Loly observed for the dipole and quadrupole moments of a magic cube" (paragraph after Prop. 4.10; "What is and is not new").
6. **Corrections item (e):** names "6×10⁷ samples for n = 4 and 4×10⁸ for n = 5" and adds "the cause cannot be reconstructed from the repository"; the same sentence closes the investigation paragraph in §5.4.
7. **Table 2** is placed in-flow (`[H]`) directly after the proof of Prop. 5.4, so the §5.4 sampling paragraph is unbroken (p. 18). **Fig. 3(c)** tick labels thinned to 1, 2, 3, 4, 8, 16, 32 (`Analysis/revision_round1/make_fig_geometry.py`, regenerated `figures/fig_gem_geometry_880.pdf`).
8. Recompiled; `CHANGES_V5.md` Round 2 section; this file.

## Referee A

- **A15 / N5 (Fig. 3(c) ticks)** — CONCEDE: thinned (ruling 7).
- **A6 (length)** — CONCEDE: the two required cuts (Appendix C → one witness + pointer; Table 3 f-vector list → ancillary) made, plus Appendix B polynomials → ancillary and Appendix D trimmed; 27 pp.
- **N1 (Thm 4.14 mixes proved bound and computer-verified equality)** — CONCEDE: moved to Remark 4.15 (ruling 2).
- **N2 (abstract variance formula)** — CONCEDE: "with an explicit variance" (ruling 3).
- **N3 ("the cause cannot be reconstructed from the repository")** — CONCEDE: added in corrections item (e) and §5.4 (ruling 6).
- **N4 (connectivity step in the sketch)** — CONCEDE: the sketch in the proof of Prop. 5.7 now says "closed under edge-adjacency, hence all facets (so P = Q)" (`sections/computations.tex`).
- **N6** — no change needed.
- **N7 (70-word abstract sentence)** — CONCEDE: split (ruling 3).

## Referee B

- **N1 (24,192-vs-72 inside the corollary statement)** — CONCEDE: moved to the following paragraph (ruling 4); the proof sentence moved with it (N6).
- **N2 ("every axial moment" over-attributes)** — CONCEDE: "dipole and quadrupole moments" in both places (ruling 5).
- **N3 (hypothesis wording)** — CONCEDE: Cor. 4.13 now reads "invariant under relabelling of the values 1,…,N (in particular the uniform distribution)"; the "population mean" sentence kept (`cor:loly_null`).
- **N4** — verified, no change.
- **N5(a)** — CONCEDE: 4×10⁸ for n = 5 named in item (e). **N5(b)** — CONCEDE: Table 2 placement fixed (ruling 7).
- **N6** — CONCEDE: see N1.
- **N7 (Fig. 1 caption red point)** — CONCEDE: caption now says "the centre point (0,0,0) is the only interior point" without relying on the colour (`sections/gem.tex`, `fig:construction`).
- **N8, N9** — no change needed.
- **Length (§4)** — CONCEDE: cuts 1–4 of the referee's list are exactly those made (ruling 1).

## Open items
None from the referees. Not done, by ruling: §6.2, the Fig. 1 strip and Fig. 2 are kept. The `lowmode_n4/SUMMARY.md` "−1/(N−1)" slip remains in the read-only results directory (noted in Round 1).
