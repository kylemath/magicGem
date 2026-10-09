# Referee B — Round 3 sign-off on *Magic Gems* (final PDF, 27 pp. at 11pt)

## (1) Round 2 minor points
- N1 (24,192-vs-72 inside Cor. 4.12 statement): **done** — statement now says "much weaker than the degree-2 conditions (see below)"; the count and the `check_round1.py` pointer are in the attribution paragraph that follows.
- N2 ("every axial moment … Rogers and Loly observed"): **done** in both places — "as Rogers and Loly observed for the dipole and quadrupole moments of a magic cube [20]" (Intro "What is and is not new" and after Prop. 4.10).
- N3 (hypothesis wording of Cor. 4.13): **done** — "invariant under relabelling of the values 1,…,N (in particular the uniform distribution)"; population-mean sentence kept.
- N5(a) (name v4's 4×10⁸ for n = 5): **done** in corrections item (e). N5(b) (Table 2 interrupting §5.4): **done** — the investigation paragraph is now continuous.
- N6: **done** with N1. N7 (Fig. 1 caption, red point): **done** — "the centre point (0,0,0) is the only interior point".
- Length cuts 1–4 of my list: **done** — App. C reduced to the n = 5 witness, App. D trimmed, Table 3 reduced to V/squares/types/volumes/f-vector counts, App. B polynomials moved to `revision_round2/appendix_data.json`. Fig. 1 strip, §6.2 and Fig. 2 kept per rulings.

## (2) Attribution and corrections text
- Loly: Cor. 4.12 and the following paragraph are now correct in direction ("Loly's value iff Cov(Z, X²+Y²) = 0 … implied by the degree-2 conditions … but much weaker") and in attribution (invariance, semi-magic validity and the I_x = I_y split credited to [13]; "the corollary re-derives this").
- Rogers–Loly: dipole/quadrupole wording correct; [20] bibliographic data correct.
- Cor. 4.13: formulas unchanged from Round 2 (verified there); wording fixed.
- Corrections item (e): names both v4 sample sizes, states the archived 10⁵ samples, and says "the cause cannot be reconstructed from the repository". Candid and complete; consistent with §5.4.

## (3) Spot checks (all agree)
- Table 3 f-vector counts per V: 4,1,6,5,7,5,5,3,3 = 39; `appendix_data.json` holds 39 f-vectors summing to 880, with the modal (12,26,16):164 as stated in the text.
- Appendix C witness n = 5: row sums all 65; column sums 66, 61, 71, 61, 66, i.e. γ = (1,−4,6,−4,1), as printed; identical to `theory/results.json`.
- Appendix B: polynomials in `appendix_data.json` are the Round 2 ones; n = 4 values 14093/1440 and 527/640 reproduce Table 1's 3.1284 / 0.9074.
- Cross-references after renumbering (Thm 4.17, Cor. 4.19, Rem. 4.16, Rem. 4.21) checked at every occurrence in the text: consistent.

## (4) Regressions from the cuts
None found. Table 3's reduction loses nothing that is not in the ancillary file and the text still names the extreme and modal f-vectors; Appendix C's pointer plus Remark 4.15 preserve the logical status of k*(n) = n−1 for n ≤ 13 as computer-verified; Appendix D still contains the inequalities and incidence table needed with Fig. 4.

## Recommendation: **Accept.**
No remaining fixes. (Housekeeping only, outside the manuscript: `Analysis/revision/lowmode_n4/SUMMARY.md` still reads "−1/(N−1)"; the paper is correct.)
