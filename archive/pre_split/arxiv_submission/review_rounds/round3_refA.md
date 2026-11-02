# Referee A — Round 3 (final sign-off) on v5-r2 (27 pp., 11pt)

## (1) Round 2 minor points

| Point | Done? | Where |
|---|---|---|
| N1 n ≤ 13 equality out of Theorem 4.14 | **Done** | Thm 4.14 (p. 11) now states only the proved facts (n ≥ 14 bound, k* ≤ n−1, k*(3)=2, k*(4)=3 with witnesses); new Remark 4.15 "k*(n)=n−1 for 5 ≤ n ≤ 13; computer-verified" (p. 12). Contribution 1 points to the remark. |
| N2 variance formula out of abstract | **Done** | "with an explicit variance". |
| N3 "cause cannot be reconstructed" | **Done** | Corrections item (e), p. 3, and §5.4, p. 18; (e) now also names the v4 sample sizes 6×10⁷ / 4×10⁸. |
| N4 edge-adjacency sentence in the Siamese sketch | **Done** | p. 21 and Appendix D, p. 27. |
| N5 Fig. 3(c) ticks | **Done** | Ticks 1 2 3 4 8 16 32, legible (p. 20). |
| N7 abstract item (i) split | **Done** | Four sentences. |
| Required cuts: Appendix C → one witness + pointer; Table 3 list → counts | **Done** | App. C prints the n=5 witness (p. 26), rest in `revision_round2/appendix_data.json`; Table 3 is a 4-row count table (p. 19) with the extreme and modal f-vectors named in the text. Also App. B polynomials → ancillary, App. D trimmed. |

## (2) Regressions from the cuts

None found. Checked: zero "??" in the PDF; every cross-reference target exists (Sections A–D, Tables 1–4, Figures 1–4, Remark 4.15/4.16, Cor. 4.19 after the renumbering, Theorem 4.17); Appendix B is self-consistent (structure of (21), leading terms, n = 3, 4 values, pointer to the ancillary file); Appendix C's n=5 witness has column sums 66, 61, 71, 61, 66 as printed (γ = (1,−4,6,−4,1), verified in Round 2); Appendix D still carries the complete Step 2–3 argument including the connectivity step; Table 2 is in-flow after Prop. 5.4 and the §5.4 paragraph is unbroken; Cor. 4.12's 24,192-vs-72 count moved to the attribution paragraph with its proof sentence. One silent correction I approve of: "verified on 511 further orders" (v5) is now "5–11 further orders", which matches `random_energy/SUMMARY.md` and `fit_variance.py`.

## (3) Abstract and Introduction

No overclaiming remains. The abstract labels the hierarchy "a Vandermonde fact", calls (v) "an exact computation", and attributes the inertia invariance to Loly; the Introduction states where the hull is actually used, credits Loly's semi-magic derivation and Rogers–Loly's dipole/quadrupole observation, and the "What is and is not new" paragraph claims exactly the five items that are proved or exactly computed. The corrections list is complete and candid.

## Recommendation

**Accept.** No remaining fixes required. (Optional, copy-editing only: the Fig. 3(d) caption still says "the eight interior points are shown in red" — they are, so this is fine; and the Trump URL overfull box of 4.2 pt can be absorbed with `\sloppy` in the bibliography.)
