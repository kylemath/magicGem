# Adversarial verification of the k*(n) claims (kstar_proofs.md, paperB_kstar_section.tex)

Verifier: independent agent, 2026-10-08. No files in this directory or the paper directories were edited, apart from this new file.
My scripts are in the session scratchpad (`.../scratchpad/v/`: `wit.py`, `milp_ub.py`, `rank2.py`, `boxr.py`, `boxrun2.py`, `thA.py`, `brute18.py`, `cons.py`).
They do not import `lattice.py` or `exact_kmax.py`. `cons.py` imports only `constructions.construct` and checks its output with its own code.

Definitions used (theory.tex, Def. 3.x / Prop. `prop:hierarchy` / Thm `thm:perm_threshold`): degree-k means
Σ_j x_j^m γ_j = 0 and Σ_i y_i^m ρ_i = 0 for 1 ≤ m ≤ k. Here Σγ = Σρ = 0 holds automatically. k*(n) is the least k such that degree-k
forces γ = ρ = 0. So a non-semi-magic arrangement satisfying degree-k gives k*(n) ≥ k+1. If degree-k forces semi-magic, then k*(n) ≤ k.

## Summary table

| Claim | Verdict |
|---|---|
| Lemma 0 (degree-k ⇔ (t−1)^{k+1} \| P_γ) | VERIFIED |
| F1, F2, ‖γ‖₁ ≤ n⁴/4, ‖γ‖₂² ≤ n⁵(n²−1)/12 | VERIFIED |
| Lemma 1 (K² ≤ πe(n−1) log‖γ‖₁) | VERIFIED |
| Theorem A (k*(n) ≤ ⌊√(πe(n−1)log(n⁴/4))⌋ ≤ 2√(πe)√(n log n)) | VERIFIED |
| Crossover: A(n) ≤ n−3 exactly for n ≥ 166 | VERIFIED WITH FIX (add a one-line analytic argument for n > 10⁶) |
| Lemmas 2–5, Cor. 6 (twin-row squares) | VERIFIED (algebra rechecked by hand; outputs checked for 7 ≤ n ≤ 79, 101, 150) |
| Theorem B (★) and Cor. 7 (liminf k*/√n ≥ √2) | VERIFIED |
| Witnesses n = 14..40 (lower bounds k*(n) ≥ table value) | VERIFIED (exact, fresh code) |
| Upper bounds n = 14..40 (k*(n) ≤ table value) | VERIFIED for 14–33 (exact independent proof for 14–23; MILP cross-check for 24–33). For 34–40: rigorous in method and code reviewed, but not independently reproduced (MILP timed out) |
| k*(n) = n−2 for 14 ≤ n ≤ 17 | VERIFIED |
| k*(n) ≤ n−3 for all n ≥ 18 | VERIFIED (exact rank-2 check of my own for 18–170, plus Theorem A) |
| U(n) for 41 ≤ n ≤ 113 (kstar_table.md) | Rigorous modulo correctness of `lattice.py` (all statuses `ok`). Not independently re-run |
| BEK 1999 citation and theorem statements | VERIFIED (minor wording fix) |
| Wright 1959 citation | VERIFIED (bibliographic data only; full text not read) |
| "Twin rows / F1–F2 are the only obstruction" | Correctly labelled as an observation, not a theorem |

No claim was found FALSE.

## (A) Upper bound

**Lemma 0.** span{x_j^m : m ≤ k} and span{C(j,r) : r ≤ k} are both the polynomials of degree ≤ k restricted to {0,…,n−1}.
P_γ^{(r)}(1)/r! = Σ_j C(j,r) γ_j, so P_γ = Σ_r (Σ_j C(j,r)γ_j)(t−1)^r. The paper's m = 0 condition (Σγ = 0) is automatic for deviations,
so "degree-k" ⇔ multiplicity ≥ k+1 at t = 1 exactly. For k ≥ n this forces P = 0, which is consistent with Prop. (b).
The row side uses y_i = (n−1)/2 − i. This is a degree-1 polynomial in i, so the same lemma applies to P_ρ(t) = Σ ρ_i t^i.
I also checked the equivalence numerically: for every witness the binomial-moment multiplicity equals the largest k with the x^m conditions satisfied.

**F2.** p columns contain pn distinct values, whose sum is ≤ pn(2N−pn+1)/2. Subtracting pM gives pn(N−pn)/2.
‖γ‖₁ = 2·Σγ⁺ ≤ 2·max_u u(N−u)/2 = N²/4. The majorant v_p = n(N−(2p−1)n)/2 has partial sums pn(N−pn)/2 and total 0.
Schur convexity then gives Σv_p² = (n⁴/4)·n(n²−1)/3 = n⁵(n²−1)/12. All correct.

**Lemma 1, line by line.**
- (a) Jensen/Mahler: ∫ log|P(e^{2πiθ})| = log|a_d| + Σ log⁺|α| ≥ log|a_d| ≥ 0, since a_d is a nonzero integer.
  Roots at 0 (the case P_γ(0) = 0) contribute log⁺0 = 0, so no division by t^r is needed. Degree d ≤ n−1, and K ≤ d ≤ n−1 because P ≢ 0.
- (b) |P| ≤ L₁ on |z| = 1. Correct.
- (c) Taylor with integral remainder: P(z) = (z−1)^K/(K−1)! ∫₀¹(1−s)^{K−1}P^{(K)}(1+s(z−1))ds is valid for polynomials on a complex segment, and |1+s(z−1)| ≤ 1 by convexity.
  |P^{(K)}(w)| ≤ Σ|γ_j| j^{\underline K} ≤ L₁(n−1)^{\underline K}, and ∫(1−s)^{K−1} = 1/K, giving L₁ C(n−1,K)|z−1|^K ≤ L₁(e(n−1)/K)^K|z−1|^K. Correct.
- (d) |e^{2πiθ}−1| = 2|sin πθ| ≤ 2π|θ|. a = 2πe(n−1)/K ≥ 2πe > 2.
  ∫_{−1/2}^{1/2} log min(1,a|θ|) = (2/a)∫₀¹ log u = −2/a. Then 2K/a = K²/(πe(n−1)). Correct.
- Edge cases: Σγ = 0 gives K ≥ 1, and L₁ ≥ 2, so log L₁ > 0. Zeros of P on the circle make log|P| = −∞ only on a null set; the inequality still holds.

**Theorem A.** If K₀ = ⌊√X⌋ then (K₀+1)² > X, so degree-K₀ forces γ = 0 and, by transposition (F1–F2 hold for rows), ρ = 0. Hence k*(n) ≤ K₀.
Both rows and columns are covered.
(n−1)log(n⁴/4) < 4n log n, so K₀ ≤ 2√(πe)√(n log n) with 2√(πe) = 5.8446. Checked numerically for 3 ≤ n < 10⁵.

**Crossover.** Exact floating evaluation for 3 ≤ n ≤ 10⁶: the largest n with A(n) > n−3 is 165, and A(165) = A(166) = 163.
So "A(n) ≤ n−3 for all n ≥ 166" holds on the checked range.
*Fix:* "for larger n it follows from the asymptotics" should be a one-line argument. For example, A(n) ≤ 5.85√(n log n) and 5.85√(n log n) ≤ n−3 for n ≥ 2000,
because √(log n/n) is decreasing. The A(n) column of kstar_table.md matches my recomputation (spot checks at n = 14, 40, 50, 100, 113).

## (B) Lower bound

- **Lemma 2.** If the row-i swap gives column j the amount +d, then the row-i′ swap gives s_{i′j′} − s_{i′j} = −d. Correct.
  In step 4 each twin pair is used at most once (I∖I′ and I′∖I are disjoint), and different column pairs are disjoint. The cells are therefore disjoint and the effects add.
  Every swap stays inside one row, so ρ = 0 is kept exactly and the ROW degree-k conditions hold trivially.
- **Lemma 3** (I checked the algebra):
  - quadruple 8r+1+8r+3+8r+5−(8r+7) = 16r+2;
  - pair 2(α_r−β_r) = −2(8r+1);
  - row size 4+2+2(m−3) = n;
  - α ∈ [4m, 5m−1] and β ∈ {5m+7r} ⊂ [5m, 12m−7], with gaps of 6;
  - tail length 2m²−12m+6 ≥ 0 for m ≥ 7;
  - domino count 3(m−1)+(m²−6m+3) = m(m−3).
  Column sums are m(N+1) = M.
- **Lemma 5** (rechecked):
  - c−A+B = 2m²+2m−1 ∈ [m²+m, 3m²−2m] ⇔ m²−4m+1 ≥ 0, which holds for m ≥ 4;
  - ΣP−ΣQ = (6m²−5m+2)−(2m²−m) = 4m²−4m+2;
  - left column residual 2m²−6m+3 = c−A−B;
  - the border uses 8m values, and the inner block uses 4m+1 … N−4m = (n−2)² values (shift 2n−2 = 4m).
  The partition of [1,4m]∖{A,B} into P ∪ Q is consistent.
- **Construction outputs.** For every n in {7…79, 101, 150} except n ≡ 2 mod 4 with n < 14, `construct(n)` was checked by my own code. Each output is a permutation, is semi-magic, and has exactly the claimed twin relations (even: rows r, m+r on all columns; odd: rows ℓ, n−1−ℓ on columns ℓ+1..n−2−ℓ for ℓ ≤ (n−9)/2). No failures.
- **Box principle (★).**
  - F_q (cumulative sums of ⌈R_q/2⌉ same-sign d's, plus 0) has ⌈R_q/2⌉+1 distinct elements, each a sub-multiset sum.
  - Sub-sums lie in an interval of length Σ|d| ≤ R_q(N−1). μ_r ranges over at most (N−1)Σ_q R_q C(q,r)+1 integers, since C(q,r) ≥ 0.
  - A collision gives δ = g−g′ ≠ 0 with Σ_q δ_q C(q,r) = 0 for r ≤ K−2, so (u−1)^{K−1} | G.
  - P_γ = t^{j₀}(1−t)G(t²), so (t−1)^K | P_γ. This gives degree-(K−1), γ ≠ 0, and k*(n) ≥ K. Correct.
  - R_q for odd n: the pair (2q+1, 2q+2) lies inside [ℓ+1, n−2−ℓ] ⇔ ℓ ≤ min(2q, n−4−2q). Correct.
  - `pigeonhole_demo.py` produced explicit witnesses for n = 14 (K = 4) and n = 26 (K = 4); its exact checks pass.
- **Cor. 7 asymptotics.**
  - RHS: there are k = K−1 factors, each ≤ n⁴C(n,s) with s = r+1. Σ log C(n,s) ≤ (k²/2)(log n − log k) + O(k²) = (α²/4) n log n + O(n) for k = α√n. Correct.
  - LHS even: (n/2) log(⌈n/4⌉+1).
  - LHS odd: R_q ≥ min(2q+1, 2(Q−q), (n−7)/2) ≥ min(q+1, Q−q, (n−9)/2), so Σ log ≥ 2 log⌊Q/2⌋! − O(n) = (n/2)log n − O(n).
  - Hence α < √2 suffices. The coverage (all odd n ≥ 9, all even n ≥ 14, and n ≡ 0 mod 4) is enough for a liminf over all n. Correct.
  - The o(1) is ineffective but genuine. The paper should present it only as an asymptotic statement, which it does.

## (C) Exact values

**Lower bounds (witnesses).** `wit.py` uses exact integers and Fractions and parses the JSON afresh. For all 27 n = 14..40 I checked that:
- each array is n×n and a permutation of 1..N;
- every row sum is M, so ρ = 0;
- γ ≠ 0 and equals the stored γ;
- the binomial-moment multiplicity of P_γ at 1 equals exactly the claimed k*(n);
- the x^m (and trivially the y^m) conditions hold for 1 ≤ m ≤ k*(n)−1.

So k*(n) ≥ table value for every n.

**Upper bounds.** What is assumed: only F1 and F2, both proved, necessary conditions. There is no unproved realisability or "feasibility assumption" in the upper bounds. The unproved statement ("F1–F2 are the only obstruction") is used only for the observation and to choose candidates for witness search. The enumeration radius n⁵(n²−1)/12 contains every F2-feasible vector (majorisation, above). In `lattice.py` I checked:
- the per-level interval [⌊c⌋−⌈√rad⌉−1, ⌈c⌉+⌈√rad⌉+1] contains all admissible x_i;
- pruning is exact (Fractions);
- the sign normalisation is harmless because F1/F2 are sign-symmetric;
- a limit hit would still give a valid (weaker) bound, and none occurred: all 98 entries in `upper_scan_14_160.json` have status `ok`.

Independent checks (no use of their enumerator):
1. **Exact box enumeration** (`boxr.py`).
   - Method: write γ = Σ y_i t^i(t−1)^{k+1} (the echelon basis is saturated: leading coefficient ±1). The inverse of an r×r block of middle rows bounds y_1..y_{r−1} exactly. y_0 is then an exact integer interval from all n strips |γ_j| ≤ n²(n−1)/2.
   - At level k = k*(n) I found **zero** nonzero F1-feasible vectors for every n = 14..23. Hence the upper bounds k*(n) ≤ table value are proved independently for 14 ≤ n ≤ 23.
   - Positive controls at level k*−1 (n = 14, 15, 18, 19, 21) find F1F2-feasible vectors, as expected.
   - A further brute force for n = 18 at level 15 over all |a|, |b| ≤ 2754 also finds 0.
2. **Rank-2 family** (`rank2.py`, exact). At level n−3 there are zero F1-feasible nonzero vectors for every 18 ≤ n ≤ 170. For 14 ≤ n ≤ 17 there are F1F2-feasible vectors (7, 2, 1, 1), consistent with k*(n) = n−2 there. Together with Theorem A for n ≥ 166, **k*(n) ≤ n−3 for all n ≥ 18** is confirmed.
3. **MILP** (`milp_ub.py`, HiGHS).
   - Setup: γ = R^T y with R an LLL basis whose unimodular equivalence to the echelon basis I verified exactly in SymPy (U integer, det ±1). F1 is imposed, and F2 is imposed for every p on both sides via the LP-dual (λ_p, μ_{pj}) encoding. Nonzero is enforced by lowest-index normalisation.
   - Results:
     - n = 14–33: at level k*(n) the MILP is infeasible, which agrees with the claimed upper bound.
     - n = 34: the MILP hit its time limit (600 s) and is inconclusive.
     - n = 35–40: not run to completion. I stopped my run because of time.
     - At level k*(n)−1 the MILP found an F1F2-feasible vector for every n = 14–34 except n = 32, where it timed out. For all n the stored witness γ passes F1F2, so feasibility at k*−1 is anyway certified by the witnesses.
   - This is floating point, so it is a cross-check only. For 24 ≤ n ≤ 40 the rigorous statement rests on `lattice.py`, whose logic I reviewed and found correct. My independent cross-check covers n ≤ 33 by MILP and n ≤ 23 exactly.
   - Status: the upper bounds for 34 ≤ n ≤ 40 are not independently reproduced, only reviewed (code logic). A longer MILP run or a second exact enumerator would close this.

`kstar_table.md` agrees: U(n) = k*(n) for n = 14..40.

## (D) Literature

- Borwein–Erdélyi–Kós, "Littlewood-type problems on [0,1]", Proc. London Math. Soc. (3) 79 (1999) 22–46.
  - The bibliographic data is confirmed by web search (author PDF people.tamu.edu/~terdelyi/papers-online/PLMS.pdf; also cited this way in arXiv:1406.2560).
  - Checked against `lit/BEK1999.txt`: Thm 2.1 (c(n(1−log|a₀|))^{1/2}, |a_j| ≤ 1, complex) is quoted correctly. Thm 2.4 ((16/7)√n + 4 when |a₀| = 1) is correct. Thm 2.7 (box principle, c√(n/log(n+1)) for F_n) is correct. Thm 2.8 ((44/7)(L+1)√n + 5 under |a₀| ≥ e^{−L²}, |a_j| ≤ 1 for j > L²) is correct. The "quite difficult" remark is correct.
  - The application of 2.1 to P_γ/(H t^r) satisfies the hypotheses: degree ≤ n−1, |a₀| ≥ 1/H.
  - *Fix:* kstar_proofs.md says "p. 1109 of the text file"; that is line 1109 of BEK1999.txt. In the paper cite "proof of Theorem 2.7" instead.
- Wright, "Prouhet's 1851 solution of the Tarry–Escott problem of 1910", Amer. Math. Monthly 66 (1959) 199–201 (DOI 10.2307/2309513). The bibliographic data is confirmed. I did not read the full text; the cited fact (the Prouhet–Thue–Morse product) is classical.
- Boyd 1997 is correctly marked as not consulted.

## Recommended fixes (none affect correctness)

1. Crossover n ≥ 166: replace "checked to 10⁶ / asymptotics" with an explicit analytic tail argument.
2. "p. 1109" → "line 1109 of the text extraction" (or drop it).
3. In the .tex, Lemma `lem:twin_squares` has only a sketch proof. Either include the full proofs of Lemmas 3 and 5 from kstar_proofs.md in an appendix, or keep the sketch with the ancillary pointer. The sketch as written is accurate.
4. In the .tex proof of (c), say explicitly that the enumeration certifies k*(n) ≤ k by excluding Λ_{n,k} (degree-k), as it does. The md uses an index shift (Λ_{n,k+1} ⇒ k*(n) ≤ k+1). Both are consistent; I checked the off-by-one conventions against the JSON (`kmax` = k*−1).
