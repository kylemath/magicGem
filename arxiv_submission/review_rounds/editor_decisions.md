# Editor decisions

## Round 1 (2026-10-07)

Both referees: Major revision, 6/10. Both independently re-verified every proof and every number; no mathematical errors found except one typo (Sec. 5.4 correlation −1/(n²−1) → −1/(n−1)). Disputes are framing/attribution/length.

Rulings (author must follow unless a rebuttal is backed by a computation or proof):

1. **Fig. 1 [BLOCKING, A]** — regenerate from code: construction row (a–d) + a 2×4 strip of the eight D4 variants with matching caption; no v4 banner, no overprinted labels. Vector PDF.
2. **Loly attribution [A1, B1, B2]** — concede fully. The semi-magic validity of the inertia invariance is Loly's. Loly's statistic is the single scalar condition Cov(Z, X²+Y²)=0, which is *implied by* the degree-2 conditions, not equivalent to them (RefB: 24,192 n=3 arrangements have I=60 vs 72 semi-magic). Reword abstract, contributions, Cor. 4.13, intro. Cite Rogers–Loly 2005 (EJP 26:809, DOI 10.1088/0143-0807/26/5/013) as the direct precedent for vanishing low multipole moments of semi-magic objects. Note that the hierarchy uses pure powers only and that mixed moments are not fixed by line sums.
3. **Theorem 4.11 vs Prop 4.14 [A2]** — concede: the real-height-function statement becomes a Proposition (Vandermonde); the integrality result k*(n) ≤ n−2 for n ≥ 14 becomes the Theorem of §4.3. Print the witness squares for k*(n)=n−1, n ≤ 13 (compact appendix table or explicit pointer to anc file), flagged as computer-verified.
4. **Length [A5, B]** — return to 11pt (standard); target ≤ 22 pp at 11pt. Cuts: Remarks 4.5, 4.20, Prop. 4.22, move the variance closed forms (20) and the Siamese proof details to the appendix. KEEP a compact algorithms paragraph + small table (Diaconis-type readers want it; ≤ half page). KEEP the corrections-to-v4 paragraph but as a compact bullet list (≤ 8 lines) that is complete per RefB point 5 (add gap scaling 1/n² → Θ(n⁻⁴), v4 Table 2 values, v4 semi-magic claim). On the v4 sampling failure (6×10⁷ samples should have contained ~42 members of L_4): investigate Analysis/src/analysis.py sampling code for ≤ 30 min; report the cause if found, otherwise state "cause not determined".
5. **Siamese layer figure [B6]** — add only if it fits in ≤ half page or replaces the unreadable Fig. 4(c); otherwise describe the five layers in one sentence in the appendix proof.
6. **Null distribution of Loly's I [B7]** — add: one sentence + formula (E[I] equals Loly's value for every arrangement distribution symmetric under permutations; Var given), verified numerically.
7. **Title/gem usage [A4]** — keep the title (the gem is the paper's name and the figures' object), but the introduction must state in one sentence that the convex hull is used in §5.5–5.7 and the height function elsewhere.
8. All [MINOR] points from both referees: concede unless factually wrong; list each in the response.
9. Web-app sentence: soften to what is verifiable from the live page (points, hull, vectors, axes, orthographic views; selectable squares) — do not claim it "lists the 880" unless checked in the page's JavaScript.

Author may REBUT any point with evidence; rebuttals go in round1_response.md and will be adjudicated.

## Round 2 (2026-10-07)

RefA: Minor revision 7/10 (13/16 resolved, 3 partly; both rebuttals accepted). RefB: Minor revision 8/10 (18/19 resolved; rebuttal accepted). No new mathematical errors.

Rulings — author implements ALL of the following, no further rebuttal expected:
1. Appendix C → keep one witness square (n=5) + pointer to the ancillary file for the rest; Appendix B exact variance polynomials → ancillary (keep the leading-order statements in the text); drop the full f-vector listing in Table 3 (keep counts + the three extreme f-vectors); trim Appendix D. Target ≈ 26 pp at 11pt. Keep Fig. 1 strip, §6.2, Fig. 2 (RefB).
2. Theorem 4.14 statement: remove the computer-verified "k*(n)=n−1 for n≤13" clause from the statement; place it in a Remark flagged computer-verified.
3. Abstract: drop the variance formula; split the 70-word sentence.
4. Cor. 4.12/4.13 vicinity: move the 24,192-vs-72 count out of the corollary statement into the following remark/text.
5. Attribution: "Rogers–Loly observed dipole and quadrupole vanishing" (not "every axial moment").
6. Corrections item (e): also name v4's 4×10⁸ n=5 claim; add "the cause cannot be reconstructed from the repository".
7. Table 2 placement so it does not interrupt the §5.4 paragraph; Fig. 3(c) tick labels thinned.
8. Recompile, zero errors; update CHANGES_V5.md (Round 2) and round2_response.md.
Decision after Round 2 author pass: brief sign-off check by both referees, then ACCEPT for arXiv v5 pending the user's go-ahead.

## Round 3 / Decision (2026-10-07)
RefA: Accept (no remaining fixes). RefB: Accept (no remaining fixes). Editor: ACCEPTED for arXiv v5. Final: 27 pp at 11pt, 4 figures, clean-directory compile verified; title line break adjusted. Upload awaits the author's (Kyle's) explicit go-ahead.
