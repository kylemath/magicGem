# Referee B — Round 2 report on *Magic Gems* (v5-r1, 28 pp. at 11pt)

Checked: `round1_response.md`, `editor_decisions.md`, the revised PDF and `sections/*.tex`, the Round 1 section of `CHANGES_V5.md`, `Analysis/revision_round1/` (log, results, figure scripts). Independent recomputations in `review_rounds/scratch_refB/check_r2.py` and `check_n3.py`.

---

## 1. Status of Round 1 points

| # | Point | Status | Why |
|---|---|---|---|
| B1 | "degree-two case" conflation | **RESOLVED** | Cor. 4.12 now: Loly's value iff the single condition Cov(Z, X²+Y²)=0, "implied by, but much weaker than" the degree-2 level; 24,192 vs 72 printed. Abstract/Contribution 1/§6.1/Conclusion reworded consistently. |
| B2 | semi-magic validity is Loly's | **RESOLVED** | Paragraph after Cor. 4.12 attributes invariance, semi-magic validity and the I_x = I_y = n²(n⁴−1)/24 split to [13]; removed from contributions; OQ 5 reworded. |
| B3 | Rogers–Loly 2005 uncited | **RESOLVED** | [20] added with correct data; cited in Intro, §2.4, "What is new", and after Prop. 4.10 with the pure-vs-mixed-moment sentence. One wording quibble, new point N2 below. |
| B4 | ref. [5] miscast | **RESOLVED** | Now "singular-value signatures and entropies", grouped with spectral refs. |
| B5 | Prop. 4.22 → remark; product of inertia | **RESOLVED** | Remark 4.20 (six lines, "oblate symmetric top ... carries no information"); P_xy statistics over the 880 added. I recomputed from `magic_squares_880 (1).npy`: 65 distinct values, range −60..24, 56 zeros, 48 distinct |P_xy|. Matches. |
| B6 | how Loly's I is the same object | **RESOLVED** | §2.2 closing sentence. |
| B7 | −1/(n²−1) | **RESOLVED** | §5.4 now −1/(n−1); consistent with Cor. 5.2 proof and the code. |
| B8 | terminology | **RESOLVED** | "energy is a label" sentence after Def. 4.2; "respectively" fixed in §5.1 and Rem. 5.3. |
| B9 | KS at n=3; z-clause | **RESOLVED** | Rem. 5.3 discreteness sentence; Table 1 caption no longer claims unseen z-scores. |
| B10 | spot checks | — | no action needed. |
| B11 | 61 vs 70; v4 sample size | **RESOLVED** | "70.0 ± 8.4 (1.1 sd low)"; "6 × 10⁷ ... a 42-fold shortfall"; investigation reported. See N5 on placement. |
| B12 | corrections paragraph incomplete | **RESOLVED** | Six-item list (a)–(f) now covers gap scaling, v4 Table 2, the withdrawn characterisation claim, the sampling statement and hardware. |
| B13 | Fig. 1 | **RESOLVED** | Regenerated from code; I checked all eight printed squares are the correct D4 images of the Lo Shu and are pairwise distinct; caption matches the panels. |
| B14 | Fig. 4(c) unreadable | **RESOLVED** | Log-scale panel with labelled bars, plus the one-line table (93, 201, 8, 20, 4, 7, 4, 5, 5, 1, 1, 1, 1, 1 — sums to 352 types / 880 squares). |
| B15 | Siamese figure | **RESOLVED** | New Fig. 4 (n = 9); layers, heights ±10, ±1, 0 and the twelve circled cells agree with Appendix D's v₁…v₁₂; caption accurate. |
| B16 | "10^8" in Fig. 2 legend | **RESOLVED (rebuttal accepted)** | see §2. |
| B17 | length cuts | **PARTLY** | All specific cuts I named were made (bound (10) gone, polynomials to App. B, duplicate computation paragraph removed, Siamese Steps 2–3 to App. D), but the 11pt reset and the additions leave 28 pp. See §4. |
| B18 | small items | **RESOLVED** | (i), (iii), (iv) done; 980 = 14²·5 added. |
| B19 | null distribution of Loly's I | **RESOLVED** | New Cor. 4.13 with E[I] and Var(I) = n⁴(n⁴−1)(n²−4)/1080; verified by me, see N1. |

## 2. Verdicts on the author's rebuttals (Referee B items)

- **B16 (Fig. 2 legend "108"): REBUTTAL ACCEPTED.** The author is right that this is a text-extraction artefact of a mathtext superscript; the rendered figure is fine. I withdraw the point.
- **B12 — the author notes Referee A wanted the corrections paragraph removed and the editor ruled to keep it compact and complete.** I concur with the ruling; the six-item list is the right form.
- **B17/A6 (page target not met) — the author declines to cut unilaterally and asks the editor to choose.** Reasonable; my choice is in §4.
- No other item was rebutted; every concession is implemented as described, and I found no case where the response overstates what was changed.

## 3. New points on the revision

**N1. [VERIFIED] Var(I) = n⁴(n⁴−1)(n²−4)/1080 (Cor. 4.13).** Re-derived: Var_grid(x²+y²) = 2Var(X²) = 2[(n²−1)(3n²−7)/240 − ((n²−1)/12)²] = (n²−1)(n²−4)/90; times N²σ_n² = n⁴(n²+1)/12 gives the stated form. Recomputed independently from the Wald–Wolfowitz expression as exact rationals for n = 3,…,8: 30, 2176/3, 22750/3, 49728, 240100, 931840 — all equal to the closed form. Independent n = 4 Monte Carlo (1.6 × 10⁷, different generator and seed): mean 339.999, var 725.55 (exact 725.33), fraction at I = 340 is 2.895 % — matches the paper's "2.9 %". The implication direction in Cor. 4.12 is now correct ("iff the single condition ... implied by the degree-2 conditions"). One placement remark: the 24,192-vs-72 count sits inside the *statement* of Cor. 4.12; a corollary statement should not contain an enumeration result. Move that sentence to the attribution paragraph that follows (which already discusses what the corollary adds). [MINOR]

**N2. [MINOR] Over-attribution to Rogers–Loly in the paragraph after Prop. 4.10 and in "What is and is not new".** Both say the vanishing of the axial moments "for every m" / "every axial multipole moment" is "which Rogers and Loly observed for the magic cube". Rogers–Loly 2005 observed the vanishing of the *dipole and quadrupole* moments. Write "as Rogers and Loly observed for the dipole and quadrupole moments of a magic cube [20]". The author has now swung from under- to slight over-attribution; the fix is three words.

**N3. [MINOR] Cor. 4.13, "for every distribution of arrangements that is invariant under permutations of the values".** Correct (then each cell's value is uniform on 1..N, so E[s_c] = (N+1)/2 and E[I] = (N+1)/2·Σ(x²+y²)). But the hypothesis as phrased could be read as permuting the *cells*; say "invariant under relabelling of the values 1,…,N (in particular the uniform distribution)". Also "magic and semi-magic squares sit exactly at the population mean of I" — good sentence; keep it.

**N4. [VERIFIED] Spot checks of new/changed numbers (all agree with results files or my recomputation):** (i) App. B at n = 4: Var(E_low) = 14093/1440 → sd 3.1284, Var(E_full) = 527/640 → sd 0.9074 (I evaluated P_e(4) = 19,100,160 and Q_e(4) = 4464 by hand; both match Table 1). (ii) Fig. 1 squares (f)–(l) are r, r², r³, h, v, t, tr² of the Lo Shu — checked cell by cell. (iii) Fig. 4 vertex cells v₁…v₁₂ at n = 9 against the general formulas of App. D. (iv) Remark 4.20: |P_xy| 48 values, 56 zeros, range of P_xy −60..24 — recomputed. (v) §5.4: archived `large_scale_landscape.json` has n_samples = 100,000 for n = 4 and 5 (I opened the file); expected members 0.07; 6 × 10⁷ × 6.997 × 10⁻⁷ = 42. (vi) Type-size table sums: 322 types in sizes 1–4 (599 squares), 30 types in sizes 5–32 (281 squares). (vii) Thm. 4.14 witnesses: the author's log re-verifies all nine (rows equal, γ = alternating binomial, degree-(n−2) moments zero, degree-(n−1) moment nonzero); I did not re-run these but the printed n = 5 witness matches `theory/results.json`.

**N5. [MINOR] The sampling disclosure is candid, but split across two places.** Corrections item (e) says the 6 × 10⁷ statement "is unsupported by the archived data, which hold 10⁵ samples"; §5.4 gives the investigation and "we attribute the earlier statement to a misreported sample size". That is the right level of candour and the right conclusion. Two edits: (a) item (e) should also say "4 × 10⁸ for n = 5" since v4's Table 3 reported both; (b) §5.4's investigation paragraph is interrupted by Table 2 in the current layout (the sentence "On re-examination, the archived data file…" starts after the table) — a float placement fix.

**N6. [MINOR] Cor. 4.12 proof ends "The count for n = 3 is by enumeration of all 9! arrangements (check_round1.py, Section A)".** Fine, but see N1: once the count is moved out of the statement, this sentence moves with it.

**N7. [MINOR] Fig. 1 caption:** "(d) their convex hull … (the centre point, in red, is interior)" — in panel (d) at print size the red point is barely visible behind the translucent faces; consider drawing it slightly larger or saying "the centre point (0,0,0) is interior" without relying on the colour.

**N8. [MINOR] Reference [13]:** "Note 88.30" moved to the end — fine. Reference [9] Gardner 1976 for Schroeppel's count is the standard citation; good addition.

**N9. [OK] Hoeffding condition** now stated with |d|^r and the Cramér–Wold bound includes the Minkowski step; Cor. 5.2's proof is complete as far as this referee is concerned.

No new mathematical errors found. Every equation I re-derived in this round (N1, N4) is correct.

## 4. Length

28 pages at 11pt (A4, 0.9 in margins) for a paper whose core results fit in §4–5 is long but not unreasonable for a general-readership journal; 24–25 would be comfortable. Of the author's candidates I would take, in this order:

1. **Appendix C → ancillary file** with a two-line pointer and the n = 5 witness kept as an example (−0.7 pp). Permitted by ruling 3; the verification script is archived, and nobody will check a 13 × 13 array by hand.
2. **Appendix D → the eight inequalities and the incidence table (b) only** (−0.5 pp); Fig. 4 now carries the geometric content, and Steps 2–3's prose is reproducible from `siamese_proof.py`.
3. **Table 3 → keep the V / squares / types / vols columns, drop the f-vector listing** (−0.4 pp); the 39 f-vectors are in the ancillary JSON.
4. **Appendix B polynomials → ancillary**, keeping (21)'s structure and leading terms (−0.3 pp).

I would **not** drop the Fig. 1 strip (ruling 1), §6.2/Table 4 (ruling 4), or Fig. 2 (it is the only picture of the limit law). That lands at ≈ 26 pp; I consider that acceptable and would not hold the paper for the last two pages.

## 5. Updated recommendation

**Minor revision — score 8/10.** All Round 1 substantive points are resolved; the attribution to Loly and Rogers–Loly is now accurate and generous in the right direction; the one internal inconsistency is fixed; the corrections list is complete and the v4 sampling statement is retracted candidly; the new Cor. 4.13 is correct and is exactly the kind of statement the physics-of-magic-squares community can use. Remaining items N1 (placement), N2 (three words), N3, N5(a)–(b), N7 are editorial and need no further refereeing; the editor can verify them from the next diff. Nothing I found would now change the recommendation downward; the length cuts in §4 are at the editor's discretion.

**Confidential note to the editor.** The response is accurate point by point — I checked each claimed change against the PDF and found none overstated. The author's own re-verification script reproduces my Round 1 numbers independently and I reproduced theirs. I am content for this to be accepted after the minor edits above without returning to me.
