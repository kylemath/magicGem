# Referee A — Round 2 report on v5-r1
**Manuscript:** "Magic Gems: Magic Squares as Orthogonality Conditions on a Height Function", v5-r1 (28 pp., 11pt)

What I re-verified this round (scratch: `review_rounds/scratch_refA/`): the new Fig. 1, Fig. 3 and Fig. 4 pages rendered and inspected; Cor. 4.13 rederived by hand (Var(X²) = (n²−1)(n²−4)/180, so Var(X²+Y²) = (n²−1)(n²−4)/90 and Var(I) = n⁴(n⁴−1)(n²−4)/1080; n=3 gives 30); the n=3 distribution of I enumerated exhaustively with my own code (24,192 arrangements at I=60, 29 values from 46 to 74, mean 60, variance 30 — all as printed); all nine Appendix C witnesses (n = 5,…,13) parsed from `sections/witnesses.tex` and checked independently in exact arithmetic (permutation of 1..n², all row sums M(n), γ_j = (−1)^j C(n−1,j), moments of degree ≤ n−2 zero, degree n−1 nonzero: all pass); the Hoeffding condition, the Minkowski step, the (½,½,½) translate and the −1/(n−1) correction located in the source.

## 1. Status of Round 1 points

| # | Point | Status | Why |
|---|---|---|---|
| 1 | Figure 1 defective | **RESOLVED** | Regenerated from code; (a)–(d) construction plus a clean 2×4 strip with the eight arrays printed; caption matches; no banner, no overprinting. |
| 2 | Semi-magic inertia invariance attributed to Loly | **RESOLVED** | Cor. 4.12 and the paragraph after it credit Loly for the invariance, its semi-magic validity and the I_x = I_y split; the corollary now claims only the decomposition (11) and the "one scalar condition" observation. Abstract/Contribution 1 reworded. |
| 3 | Thm 4.11 is a lemma; 4.14(3) is the content | **RESOLVED** | Hierarchy is Prop. 4.10 with an explicit "Vandermonde, no novelty claimed" sentence; integrality bound is Thm. 4.14 with the n ≥ 14 statement as headline. |
| 4 | Witnesses for k*(n)=n−1, n ≤ 13 | **RESOLVED** | Appendix C prints all nine; flagged computer-verified; I verified each independently. |
| 5 | Title vs content | **PARTLY** (accepted) | Title kept per editor ruling 7; the one-sentence disclosure ("The convex hull itself is the object of Sections 5.5–5.6 …") is in the Introduction. See rebuttal verdict below. |
| 6 | Length | **PARTLY** | All cuts I listed were made ((a) changelog → 6 bullets kept by ruling; (b) Prop. 4.22 → 6-line remark; (c) §6.2 halved, kept by ruling; (d) (20) → App. B; (e) |L_5|,|L_6| → one sentence; (f) Fig. 3 gallery dropped) plus more (v5 Tables 1, 3 and Fig. 5 folded into text). Still 28 pp at 11pt because ~4 pp were added at referee/editor request. See §4 below. |
| 7 | Cor. 5.3 proof gaps | **RESOLVED** | |d_N|^r in §2.3 and the proof; Minkowski + variance lower bound closes the Cramér–Wold step; abstract says "by Hoeffding's combinatorial CLT". |
| 8 | Volume-denominator justification | **RESOLVED** | Now via the (½,½,½) translate being a lattice polytope of Z³. |
| 9 | "distinct point sets" trivial | **RESOLVED** | "hull-vertex set" in Contribution 5 and Prop. 5.5(1), with the triviality of the full-set statement noted. |
| 10 | Birkhoff polynomial / "semi-magic" wording | **RESOLVED** | Introduction now correct: polynomial for Birkhoff dilates, quasi-polynomial for the inside-out count. |
| 11 | "respectively"; KS header | **RESOLVED** | Explicit wording; KS defined in caption. |
| 12 | Prop. 4.14 structure; O(log n) heuristic | **RESOLVED** | Theorem leads with the bound; Open Q. 2 gives the 2^k ≳ n³ line with its caveat. |
| 13 | Smith-normal-form wording; mean by symmetry | **RESOLVED** | Both sentences as requested. |
| 14 | References | **RESOLVED** | Dürer entry removed, MR number removed, Loly note formatted, https, Gardner 1976 added for Schroeppel, Frénicle "published posthumously in 1693". |
| 15 | Fig. 4(c) unreadable; Fig. 2(c) redundant | **PARTLY** | Fig. 3(c) regenerated with log axis and a size table in the text — but the x-axis tick labels (1 2 3 4 5 6 7 8 10 13 14 16 26 32) still overprint at the right end (p. 20). Fig. 2(c) kept — rebuttal accepted (below). |
| 16 | "classification" → "exact computation" | **RESOLVED** | Abstract, Contribution 5, Conclusion reworded. |

## 2. Verdicts on the author's rebuttals

- **A5 (title kept).** *Accept.* The editor ruled; the author conceded the factual point and placed the disclosure where a reader meets it first. I still think the title promises more hull than the paper delivers, but the Introduction now says so in plain words, which is what matters.
- **A15 (Fig. 2(c) kept).** *Accept.* The author is right that panel (c) is the only statement of the exact mean/sd for 3 ≤ n ≤ 40 and that Table 1 stops at n = 8; it is not a duplicate.
- **B16 ("10^8" in Fig. 2 legend).** Not my point, but I confirm from the rendered page that the superscript is typeset correctly; the pdftotext layer is the only thing that prints "108".
- **Length "Open item 1" (author would rather the editor choose the cuts).** *Partly accept.* Reasonable for material the rulings mandated; see §4 for the two cuts I do require.

## 3. New points introduced by the revision

**N1 [MINOR] Theorem 4.14 statement mixes a proved bound with a computer-verified equality.** The theorem's last clause "with equality for 3 ≤ n ≤ 13 … by the computer-verified witnesses printed in Section C" sits inside the theorem statement. The witnesses are correct (I checked all nine), but a theorem should not depend on an appendix table for part of its statement. Resolve: keep "k*(n) ≤ n−2 for n ≥ 14" as the Theorem; move "k*(n) = n−1 for 3 ≤ n ≤ 13 (witnesses: Appendix C, computer-verified)" into a following Proposition or Remark. Two lines of editing.

**N2 [MINOR] Corollary 4.13 — correct, and the presentation is right.** Formula, hypotheses ("every arrangement distribution invariant under permutations of the values" — correct by linearity) and the n = 3 numbers all check. The remark "magic and semi-magic squares sit exactly at the population mean of I, and the invariance says that their fluctuation vanishes, not that their value is extreme" is the right way to say it and is the one genuinely new sentence about Loly's invariant in the paper. No change requested — except that the abstract now carries the full variance formula n⁴(n⁴−1)(n²−4)/1080; a formula of that length does not belong in an abstract. Say "with an explicit variance".

**N3 [MINOR] Corrections item (e) and §5.4, "misreported sample size".** The investigation is honestly reported (archived file holds 10⁵ samples; expected 0.07 members; floating-point and zero-set causes excluded). "We attribute the earlier statement to a misreported sample size" is the only available explanation and is stated as an attribution, not a fact; acceptable. I would add the four words "the cause cannot be reconstructed from the repository" so that a reader does not take the attribution as established.

**N4 [MINOR] Figure 4 (Siamese layers) and Appendix D.** The figure is informative and earns its half page: it makes Steps 2–3 legible in a way the text alone did not. The proof sketch on p. 21 correctly summarises what is deferred. One nit: the sketch says "Sixteen explicit planes … are shown to support the convex hull of twelve named points … in facets that close up into a surface"; add "closed under edge-adjacency, hence all facets" since that connectivity step is what makes P = Q.

**N5 [MINOR] Fig. 3(c) tick labels** (see point 15): thin the x-tick labels (e.g. label 1, 2, 3, 4, 8, 16, 32 only) or rotate them.

**N6 [MINOR] "What is and is not new" (p. 3).** Now accurate and, with the Rogers–Loly 2005 multipole precedent, properly placed. Fine.

**N7 [MINOR] Abstract length.** Item (i) is now a 70-word sentence. Split it: the Vandermonde fact, the n ≥ 14 integrality bound, Loly's invariance as a consequence, the null distribution.

No new mathematical errors found.

## 4. Length

Page map (11pt): Intro 1–3, Background 3–4, §3 4–5, §4 5–14 (9 pp.), §5 14–22 (8 pp.), §6–7 22–24, Appendices 25–28.

My position: the manuscript is now 28 pp. because the referees and editor asked for ~4 pp. of additional material and the standard 11pt; the author cut everything I asked for and more. I will not ask for verified content to be removed to hit a number. Of the author's candidate cuts I **require two**, which lose nothing:

1. **Appendix C → one printed witness (n = 5) plus a pointer to the ancillary file for n = 6,…,13** (−0.6 pp). The arrays are machine-verified and unreadable by eye; one example conveys the construction.
2. **Table 3 (the 39 f-vectors with multiplicities) → keep the V-distribution line and the count "39 f-vectors", drop the full list** (−0.5 pp); the list is in the ancillary JSON.

I **do not require**: dropping §6.2/Table 4 (ruling 4), the Fig. 1 strip (ruling 1), Fig. 2, or shortening Appendix D (it is the proof). With the two cuts the paper is ~27 pp. For the venues I named in Round 1 — Experimental Mathematics, Integers, J. Integer Sequences, Involve — 27–28 pp. at 11pt is within normal range; it is the content, not the page count, that was my concern, and the content is now stated at the right level of claim. (For Mathematics Magazine the paper is unsuitable at any length, as I said before.)

## 5. Recommendation

**Minor revision. Score 7/10** (from 6). Every mathematical statement checked in two rounds is correct; the attribution to Loly is now right; the real theorem is labelled as such; the figures are regenerated from code and the new ones (Fig. 1, Fig. 4) are an improvement; the corrections list is complete and honest, including the admission about v4's sample size.

What would still change it: upward to accept after N1 (move the n ≤ 13 equality out of the theorem statement), the two cuts in §4, the abstract trim (N2, N7), and the Fig. 3(c) ticks — all mechanical, no further refereeing round needed. Nothing I have seen would move it downward.
