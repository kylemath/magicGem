# Response to the referee

Thank you for the careful report. The paper has been restructured around the strongest content, as suggested. Its main result is now a two-sided bound for the permutation threshold, with exact values for n <= 40. The variance formulas are now proved. The trivial material has been demoted or cut, and the defensive text has been removed.

The new title is "Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies". The paper is 21 pages, including about 4 pages of references and appendices; the body is about 17 pages, and the previous version had 25 pages.

Numbering below refers to the revised version, with old numbers in brackets.

## Recommendation / Section 4.1: the permutation threshold

**Reframing via Prouhet–Tarry–Escott and Borwein–Erdélyi–Kós.**
- Changed in Section 3.2.
  - Lemma 3.2 shows that the degree-k conditions are equivalent to (t-1)^{k+1} dividing P_γ, and similarly for P_ρ.
  - The lattice Λ_{n,k} is introduced.
  - The Prouhet–Tarry–Escott reading is explained, with Wright (1959) and Allouche–Shallit.
  - The Thue–Morse vectors and BEK Theorem 2.7 are mentioned.

**Upper bound.**
- Theorem 3.7(a) gives k*(n) ≤ ⌊√(πe(n−1) log(n⁴/4))⌋ ≤ 2√(πe) √(n log n).
- The proof is self-contained (Lemma 3.9). It uses Jensen's formula (Mahler measure ≥ 1), the Taylor remainder at 1, and the bound ‖γ‖₁ ≤ n⁴/4 from the new column-feasibility Lemma 3.8.
- After the proof we note that BEK Theorem 2.1 gives the same order with an unspecified constant. We checked the hypotheses against the text of the paper: |a_j| ≤ 1, and the zero count is c√(n(1−log|a_0|)).

**Lower bound / realisability.**
- Theorem 3.7(b) gives liminf k*(n)/√n ≥ √2. This is stronger than the √(n/log n) you suggested.
- The realisability device follows your suggestion of swaps within a row:
  - Lemma 3.11 (twin swaps): in a semi-magic square whose rows i and i' are complementary on a set of columns, a swap in row i moves d between two columns, and the same swap in row i' moves −d.
  - Lemma 3.12 gives explicit semi-magic squares with many twin rows. The proof is in Appendix B.
  - Proposition 3.13 gives a box-principle criterion.
- The open question is now √n against √(n log n) (Section 6, item 1). The O(log n) heuristic of the old Open Question 2 has been deleted.

**Exact values.**
- Theorem 3.7(c) gives:
  - k*(n) = n−1 for 3 ≤ n ≤ 13;
  - k*(n) = n−2 for 14 ≤ n ≤ 17;
  - k*(n) ≤ n−3 for all n ≥ 18, from the rank-2 lattices for 18 ≤ n ≤ 400 and part (a) for n ≥ 166;
  - exact values for 14 ≤ n ≤ 40 in Table 1, from lattice enumeration plus witness arrangements.
- The upper bounds for 14 ≤ n ≤ 33 were reproduced independently by an integer-programming cross-check (`anc/kstar_crosscheck/`); for 34 ≤ n ≤ 40 they rest on the exact lattice enumeration alone (`anc/kstar_verify.py`), as the caption of Table 1 states. That the column-feasibility inequalities are the only obstruction is stated as an observation for n ≤ 40, not as a theorem.
- Figure 2 shows the exact values, the enumeration upper bounds up to n = 100, the bound (a), n−1 and √(2n).
- The "level n−2 suffices iff n ≥ 14" statement survives inside the proof of (c).

**Search description (point 9).**
- Added the paragraph "The witnesses" in Section 3.5. It gives the target vectors, the moves, the objective, the annealing, and how close the witnesses come to the bound: 924 vs 1014 at n = 13, and 24150 vs 24642 at n = 37.
- We give no run times because they were not recorded systematically.

## Section 3: verdicts on numbered items

| old item | action |
|---|---|
| Def 2.1, "height function" | Renamed "centred value function". A sentence in §2.1 cites Thurston (1990) and explains why the term is avoided. The coordinates are now defined once (Def 2.1); the introduction only previews them. |
| Lemma 3.1 | Kept as the short Lemma 2.2, with a one-line proof. |
| Def 3.2 | Kept (Def 2.4). It now cites Pinn–Wieczerkowski for the energy. I checked the reference (IJMPC 9 (1998) 541–546, arXiv cond-mat/9804109): their eq. (2) is exactly Σ_L(S_L − M)² over rows, columns and both diagonals, i.e. N²E_full. Their Metropolis move swaps the values k and k+1. |
| Rem 3.3 | Corrected per C3; now Remark 2.5. |
| Prop 3.4 (D4) | Reduced to one sentence in §2.2. |
| Rem 3.5 | Reduced to one sentence ("omitting them would destroy the D4-invariance"). |
| Lemmas 3.6, 3.7, 3.8 | Merged into Lemma 2.3 (line space). It cites Ward (1980) and Stanley EC1 §4.6 for dim = n² − 2n. The "projection lemma" name is gone. |
| Rem 3.9 | Deleted. |
| Prop 3.11 | Now Prop 3.3, with a three-line proof via Lemma 3.2. Part (c) is the polynomial (1−t)^{k+1}, so the shift-operator proof is gone. Old Thm 4.1(b,c) is absorbed in part (a). |
| Cor 3.12 | Reduced to one sentence at the end of §3.1. |
| Cor 3.13 | Kept as Cor 3.5, shortened. The list "60, 340, …" has been deleted. |
| Cor 3.14 | Moved after the result it uses: now Cor 4.2 in §4.1, after Prop 4.1. The probability is given exactly: Pr(I = 340) = 13049/450450. |
| Thm 3.15 / Rem 3.16 | Replaced by Theorem 3.7 and §§3.3–3.5 (see above). |
| Rem 3.17 | See C12. |
| Thm 3.18, Lemma 3.19, Cor 3.20, Rem 3.21 | Merged into the single Remark 5.2. It states that the formula is the incremental evaluation used in local search [Pinn–Wieczerkowski]. It is no longer a contribution or a novelty claim, and the E_low swap remark was cut. |
| Rem 3.22 | Merged with old Thm 4.1(d) into Remark 3.4 (mixed moments). |
| Thm 4.1 | Removed as a theorem. (a) is Lemma 2.3(3), (b, c) are Prop 3.3(a), and (d) is Remark 3.4. |
| Thm 4.2 | Now Remark 3.15. The improved odd-n constant was verified (see C10). The numerical check of the proved inequality and Fig. 2(a) have been deleted. |
| Prop 4.3, Rem 4.4 | Cut to two sentences in §3.7: the Lo Shu ring value and the n = 4 comparison. |
| Rem 4.5, Rem 4.6, Table 1 | Deleted. |
| Prop 5.1 | Split. The means are Prop 4.1, with the one-line sampling-without-replacement derivation added. The variances are now proved (Theorems 4.3, 4.4); see C1. |
| Cor 5.2 | Now Cor 4.5, with a corrected Hoeffding condition and a corrected proof (C2). |
| Rem 5.3 | Now Remark 4.6, rewritten (C4). |
| Prop 5.4 | Now Prop 5.1. The "acts freely" statement is corrected (C7). |
| App. B | Replaced by Appendix C, which has the full derivation. The polynomials are printed in Theorem 4.4. |

## Overselling and tone (Section 3 end, Section 6)

- The abstract has been rewritten. It now leads with the k*(n) theorem and does not claim balance or swap results as contributions. "Exact" is used only for proved statements.
- The contributions list has been replaced by three plain paragraphs (threshold; random arrangements; the L_4 count). A single paragraph, "Classical and new material", says what is classical and lists the four results claimed as new. The swap formula is explicitly attributed to standard local-search practice.
- All quoted defensive phrases have been deleted:
  - "nothing more"
  - "we claim no novelty"
  - "we make no claim"
  - Rem 3.9
  - the §6.1 paragraphs
  - the conclusion's "viewpoint, not a result"
  - "change the picture in an interesting way"
  - "the price of invariance"
  - "which we use constantly"
  - "more rugged"
  - "so local search is cheap"
  - "banded"
  - "one cannot hope for more"
- The Discussion's local-search subsection, Table 5 and its caption details have been cut. One sentence remains in §5.2, and the details are in `anc/README.md`.
- The conclusion has been replaced by two sentences at the start of §6.
- The commented-out package lines have been removed from the preamble. cleveref is not installed in the basic TeX Live used to build the paper, so a short labelled helper macro is kept, with a neutral comment.

## Section 4.2–4.4

- **4.2.** The energy is now attributed to Pinn–Wieczerkowski, and the swap formula is described as delta evaluation. Table 5 has been removed.
- **4.3.** The balance section is now §3.7, of about half a page: one remark on separable moments and Cauchy–Schwarz, plus the Lo Shu ring value and the n = 4 comparison.
- **4.4.** The Monte Carlo columns have been removed from the table of exact moments (now Table 2). The table has exact mean, exact sd, Gaussian sd and the variance ratio. One sentence in Appendix A records the Monte Carlo sanity check.

## Section 5: correctness

- **C1 (variances not proved).** Now proved.
  - Theorem 4.3 gives a general identity: Var(zᵀAz) = −N(N+1)(2N+3)/360 (trA)² + N(N²−1)(5N+6)/360 tr(A²) − N²(N+1)²/120 Σ A_aa², for symmetric A with zero row sums. The main text has a proof sketch; Appendix C has the full derivation, by Möbius inversion over equality patterns, where only the four singleton-free partitions survive.
  - The invariants of the two energies are derived in Appendix C, eqs. (17)–(18).
  - Theorem 4.4 prints all four polynomials, which answers the question about the denominators.
  - The asymptotics are now Var(E_low) = n⁸/5184 − 41n⁶/64800 + O(n⁴), so the n⁷ coefficient is zero, and Var(E_full) = n³/36 − n²/18 − 7n/180 + O(1).
  - We re-checked the identity independently: by enumerating all N! permutations for random zero-row-sum integer matrices (N = 4–8), and against the explicit energy matrices for n = 3–11, where it agrees with the closed forms.
  - We note that the identity is a special case of the classical moment formulas for quadratic assignment statistics (Mantel 1967; Hubert 1987).
- **C2 (Hoeffding).**
  - §2.3 now states the condition as a ratio → 0, together with the simpler sufficient condition max|d_N| / (N⁻¹Σd_N²)^{1/2} → 0.
  - I could not access the original paper. The wording follows the restatement of Hoeffding's Theorem 3 in M. Albert, "Concentration inequalities for randomly permuted sums" (arXiv:1805.03579). That restatement gives the ratio condition "for some r > 2" and the max condition as the simpler sufficient one. We use only the max condition, which implies the ratio condition for every r > 2, so the result does not depend on the exact wording.
  - The proof of Cor 4.5 now verifies the max condition directly. The quotient factorises as (max|a|/‖a‖)·(max|b|/rms b) = o(1)·√3.
  - Motoo (1957) and Bolthausen (1984) are cited.
- **C3.** Remark 2.5 now says: for every n ≥ 3 the four conditions are strictly weaker on real z; for permutations they coincide when n = 3 and not when n = 4.
- **C4.** The clause has been deleted. Remark 4.6 states that the Gaussian sd of E_full at n = 3 is about twice the exact one. It gives the exact/Gaussian variance ratio 1 − 2/n − 7/(5n²) + O(n⁻³) for E_full, and 1 − 82/(25n²) + O(n⁻³) for E_low, which I verified symbolically.
- **C5.** Corrected in §2.4: 275,305,224 D4-orbits, i.e. 2,202,441,792 squares (Schroeppel 1973, reported by Gardner 1976).
- **C6.** The table has been removed together with the unit-vector material. The surviving sentence uses "the magic mean lies at the 7.4th percentile".
- **C7.** §5.1 now says that D4 acts freely on all arrangements and preserves L_4.
- **C8.** The constants have been fixed as suggested: 15/8 for odd n ≥ 15, and the right-side ratio decreases, equal to 225/182 at n = 14 (proof of Theorem 3.7(c)).
- **C9.** Prop 3.3(a) now takes a, b defined on {x_0, …, x_{n−1}}.
- **C10.** Verified and adopted. ‖P_W z‖² ≤ λ_n E_full, with λ_n = n²/(n−1) for odd n and n²/(n−2) for even n (Remark 3.15), since the eigenvalues of Γ_D are n−1, n−1 for odd n.
- **C11.** Remark 5.2: the values "lie in the set {d²λ}". The text adds that 70 values occur, out of 105,600 swaps.
- **C12.** We tried the suggested argument. The four lines through the centre give only 3e = 15 − 2(t+u), where e is the centre value and γ = t(1,−2,1), ρ = u(1,−2,1); this does not force t = u = 0 without further case analysis. Remark 3.14 therefore states the equivalence as verified by exhaustive enumeration, records the partial argument, and says that no shorter proof is given.
- **C13.** The colour bar of Fig. 4(b) is now labelled "number of swaps". The annotation arrows of panel (a) have been replaced by a legend.

## Section 7: notation and presentation

- **G.** The 2×2 diagonal Gram matrix is now Γ_D, and the Gram matrix of test functions is Γ. The F, G of old Prop 4.3 are gone.
- **E.** The shift operator is gone.
- **Δ.** No longer used. The swap gap is d²λ and the minimum gap is g_min.
- **m.** m is now only the power index. The swap multiplicity is λ(a,b), the moments m_ab are gone, and "lines meeting in ℓ cells" is used.
- **δ.** δ is only line deviations. The Kronecker delta and δ_mean are gone.
- **T.** Φ_a is the generic statistic (§2.3), T_φ = Cov(φ, Z) is used in §4, and U_1, …, U_4 are the uncentred sums (§5.1).
- **Σ.** Σ_n has been replaced by σ_n²Γ, and Σ_U is the covariance of the U_i.
- **D in eq. (17).** Replaced.
- **C_j.** The statement now reads "E Cov(1_L, Z)² for every line L".
- **σ_n².** Defined once, in eq. (7).
- **γ, ρ.** The column and row sums of a general f are distinguished once, at the start of §3.1.
- **Forward references.**
  - Cor 3.14 has moved (see above).
  - The Lemma 3.8(3) claims are now Remark 3.14 / Remark 2.5.
  - The label `sec:results` has been renamed `sec:computations`.
  - Local search is no longer in the Discussion.
- **§7.3.**
  - The triple definitions have been removed.
  - Paper A is mentioned once in the introduction and once in §2.1, with one sentence each.
  - The text now says "0.80 times the Gaussian local-limit estimate".
  - Rem 3.5's reflection has been reduced to the invariance sentence.
  - w_D, Q and the lemma clause are gone.
  - The list 60, 340, … has been deleted.
  - The Cor 3.14 statistics are given exactly.
  - The theorem title is now "The permutation threshold".
  - The numerical check of a proved inequality has been deleted.
  - The percentile phrasing has been fixed.
  - The 40/27 parenthesis now reads "coincide iff (n²−1)/6 = 2(n−1)/n, i.e. n = 3".
  - The mode/maxima statistics have been dropped.
  - The 105,600-swap "verification" sentence has been dropped; only the gap distribution remains.
  - The |L_n| heuristic is softened to "one expects", with citations to Kuperberg–Lovett–Peled, Eberhard–Manners–Mrazović and Canfield–McKay.
  - Open question 4 no longer mentions semi-magic squares.
- **§7.4 captions.**
  - Fig. 1 explains W and W^⊥ ∩ 1^⊥, with dimensions.
  - Fig. 2 (balance) has been deleted.
  - The Fig. 3 caption has been shortened.
  - The Fig. 4 colour bar and annotations have been fixed.
  - Table 1 has been deleted.
  - The Monte Carlo columns of Table 3 have been dropped.
  - The argument from the Table 4 caption has moved into the text.
- **§7.5.** MSC is now 05B20 (primary); 05A05, 11C08, 60C05, 60F05. The keywords include Prouhet–Tarry–Escott.

## Section 8: structure

- All the cuts listed have been made, except that Fig. 1 (the line-space illustration) is kept.
- All the merges listed have been made.
- Cor 3.14 has moved.
- Theorem 3.15 has been expanded into §§3.2–3.5.
- The proof of the variances has been expanded.

The body is about 17 pages rather than the 10–12 you suggested. The additional length is the new material on the threshold: the upper and lower bound proofs, the exact values, and Appendix B.

## Section 10: literature

The following have been added:
- Wright (1959);
- Allouche–Shallit (1999);
- P. Borwein's book (2002);
- BEK (1999), with the DOI and theorem numbers checked against the paper;
- Ward (1980), with the reference checked;
- Stanley EC1 (2012);
- Pinn–Wieczerkowski (1998), checked;
- Noether (1949);
- Motoo (1957);
- Bolthausen (1984);
- Canfield–McKay (2010);
- Kuperberg–Lovett–Peled (2017);
- Eberhard–Manners–Mrazović (2019);
- Thurston (1990);
- Frénicle (1693);
- Mantel (1967) and Hubert (1987), for quadratic assignment moments.

Barvinok (2010) was not added, because nothing in the text depends on it. The Trump entry already carries a URL and an access date. The order-5 count is attributed to Schroeppel via Gardner.

## Not addressed, or only partly

- The two-line human proof for n = 3 (C12): we could not find one. See above.
- The target length of 10–12 pages: the paper is longer because of the new threshold theorem.
- The original Hoeffding (1951) Theorem 3 could not be consulted directly. The formulation used is robust to the precise wording; see C2.
