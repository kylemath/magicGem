# Review dialogue: Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies

## REVIEWER — turn 1

I read the whole paper from the .tex sources (main.tex, sections/*.tex, compiled paperB.pdf for the numbering). I start from the assumption that nothing is right until I have checked it. My scratch checks are in `/private/tmp/.../scratchpad/dialogue/c1.py`–`c9.py`. They use exact rational arithmetic unless I say otherwise. Numbering below follows paperB.pdf (Thm 3.7 = permutation threshold, etc.).

### 0. What I verified independently (no action needed)

- **n = 3 enumeration (all 9!).** I get 760 arrangements satisfying the degree-1 conditions, 4,224 with both diagonals equal to 15, 72 satisfying degree-2, 8 with E_low = 0, and 24,192 with I = 60. I takes 29 values in [46, 74] with Var I = 30. Both means are 40/27, Var E_low = 1532/2187 and Var E_full = 398/2187. All match the paper.
- **Thm 4.3, eq. (4.4).** I checked it against full permutation enumeration for random symmetric zero-row-sum A with N = 4, 5, 6: exact agreement.
- **Thm 4.4.** I built the explicit matrices A for E_low and E_full, n = 3..8, and applied (4.4). The results agree exactly with the printed polynomials P_o, P_e, Q_o, Q_e for both parities. The asymptotic expansions, the Gaussian variance ratios 1 − 2/n − 7/(5n²) and 1 − 82/(25n²), and every entry of Table 3 (means, sds, Gaussian sds, ratios) also agree.
- **Prop 4.1 and Cor 4.2.** The means, eigenvalues and Var I = n⁴(n⁴−1)(n²−4)/1080 are correct. I recomputed Pr(I = 340) = 13049/450450 at n = 4 exactly, through the 4-subset structure of the weights x² + y² ∈ {1/2, 5/2, 9/2}.
- **Thm 3.7(c) witnesses.** All witnesses for 3 ≤ n ≤ 40 are genuine permutations with ρ = 0. The orders of vanishing equal k\*(n), and the values of max|γ_j| reproduce Table 1 exactly. Appendix C (n = 5) and the n = 3, 4 matrices in the proof are also correct.
- **Rank-2 level n−3.** I wrote my own exact box enumeration over (a, b) for 14 ≤ n ≤ 60, inverting two central coefficients and testing (3.2) for all p. It finds feasible nonzero vectors for n ≤ 17 and none for 18 ≤ n ≤ 60, consistent with the paper.
- **Thm 3.7(a), Lemma 3.9.** I checked the proof line by line and it is correct: the Taylor bound, binom(n−1, K) ≤ (e(n−1)/K)^K, and the integral ∫ log min(1, β|θ|) = −2/β, which needs 1/β ≤ 1/2, true since K ≤ n−1. f(166) = 37.06 > 0 and f(165) = −93.3 < 0.
- **Prop 3.13 and proof of (b).** The logic checks out: subset sums of same-sign d's, the disjoint cells, P_γ = t^{j_0}(1−t)H(t²), and the Stirling estimate. Recomputing (3.4) gives k\* ≥ 2 at n = 14 and k\* ≥ 7 at n = 100, as stated.
- **Lemma 3.12 (Appendix B).** I checked both constructions by hand algebra: index bookkeeping, the range [m² + m, 3m² − 2m], and the border sums. Both are correct.
- **Prop 3.14 (n = 3).** The parametrisation, the identity Σz² = 2(4k² + 3(P² + Q²) + T² + U²) and the case analysis are all correct.
- **Other checks, all correct:**
  - Remark 2.5 matrix, N²E_full = 396.
  - Fig 1 numbers 3.375 + 2.8125 + 15.0625 = 21.25.
  - Remark 3.4: 60, and 824 / 48 / 623 / 773.
  - Swap gaps: 70 values in [2, 980], g_min counts 432/420/28, Lo Shu g_min = 3.
  - 2150 disjoint ordered pairs.
  - Gaussian local-limit estimates 13.6 and 1.82e7, and ratios 0.59, 0.80, 0.59, 0.91, 1.10, 0.96.
  - Ring imbalance for n = 4 (min 0.0705, mean 5.51, random mean ≈ 17.08, percentile ≈ 7.4%).
  - The n = 3 ring value 2(2 − √2)√5.
- **|L_4| = 14,639,440.** I reproduced it with my own meet-in-the-middle count in numpy, written independently of `lowmode_enum.c` (`c9.py`, 131 s).

So far I have found no mathematical error in a stated theorem. My concerns are gaps in what is printed, one ambiguity that changes a number, a vacuous sentence, overclaims, and readability.

### (a) Claims I could not verify from what is printed

**R1.1 (Thm 3.7(c), §3.5, "n ≥ 18: level n−3").** The text says: "Two consecutive central coefficients bound |a|, |b|, and checking all pairs (a, b) in the resulting box shows …". The bound itself is not stated. I reconstructed it (invert the 2×2 matrix of the coefficients j₀ = ⌊(n−1)/2⌋, j₀ + 1 of (t−1)^{n−2}(a + bt)) and it works. A reader should not have to do this. Please print the explicit box: |a|, |b| ≤ B·‖M⁻¹‖_∞ with B = n²(n−1)/2. For n ≥ 18 the box is |a|, |b| ≤ 1. If that holds uniformly in n, the computer check up to 400 can be replaced by a short proof. **Q to advocate:** does |a|, |b| ≤ 1 hold for all n ≥ 18? If so, can the step become a two-line argument, so that "n ≥ 18: k\* ≤ n−3" is computer-free?

**R1.2 (Thm 3.7(c), upper bounds 14 ≤ n ≤ 40, and Table 1 caption).** For 34 ≤ n ≤ 40 the upper bounds "rest on the lattice enumeration alone" (`kstar_verify.py`). That is one program, which I cannot rerun in reasonable time. The abstract nevertheless says "we determine k\*(n) for n ≤ 40". **Q:** is there a certificate (for example the LLL-reduced basis together with the Gram–Schmidt norms, so that the Fincke–Pohst search tree can be audited), or a second independent implementation for 34–40? If neither exists, the abstract should say "for n ≤ 33, and computer-assisted values to n = 40".

**R1.3 (§3.3, last paragraph; §6 item 1).** The paper asserts without proof: "An argument using only that γ is a nonzero integer vector with ‖γ‖_∞ ≤ n³ cannot give an upper bound of smaller order than √n: the box principle … produces such vectors in Λ_{n,K−1} with K ≍ √n." Two issues:
- (i) No computation is given.
- (ii) It does not match the hypothesis actually used, ‖γ‖₁ ≤ n⁴/4. Entries up to n³ give ‖γ‖₁ up to n⁴, which violates the l¹ bound. §6 then restates it as "for such vectors [‖γ‖₁ ≤ n⁴/4] no bound of smaller order than √n is possible".

Please either state the exact class (entries bounded by n³/4, say) with the one-line counting, or drop the claim.

**Q:** is the Jensen bound √(n log n) sharp for nonzero integer γ with ‖γ‖₁ ≤ n⁴/4? (I suspect Borwein–Erdélyi–Kós show sharpness of √(n(1 + log M)) for coefficients bounded by M.) If it is sharp, the gap between the bounds is purely a realisability question (which vectors are column-deviation vectors of arrangements), and §6 item 1 should say so instead of drawing the analogy with the {−1, 0, 1} gap.

**R1.4 (Prop 5.1, |L_4|).** One C program (`lowmode_enum.c`) produced the count, and the brute-force cross-check exists only for n = 3. I have now reproduced 14,639,440 independently, so the number stands. **Suggestion:** say in the paper that two independent implementations agree, and ship a short Python recount in anc/. I have not checked the breakdown in Table 4.

**R1.5 (§5.2, "steepest swap descent … 19.5 %, 1.2 %, 0.8 %").** These numbers depend on unstated choices: tie-breaking, whether descent stops at non-strict minima, and the number of runs. **Q:** where are these choices specified? The README gives the run counts, but the paper does not.

**R1.6 (Cor 4.5 proof).** The argument is correct, but it cites Hoeffding's Thm 3 together with conditions (11) and (12) exactly as printed in Hoeffding 1951. I have not checked the original. **Q:** is the statement in §2.3 a verbatim transcription, conditions (11), (12) and (14) included, with Hoeffding's normalisation N⁻¹Σd²? A reader will check this.

### (b) Errors and ambiguities found by recomputation

**R1.7 (§5.2, "E_low has 344 local minima, of which 336 are non-magic").** "Local minimum" is undefined, and the number depends on the definition. Over all 9! arrangements and all 36 transpositions:

| energy | strict minima (E < all neighbours) | weak minima (E ≤ all neighbours) |
|---|---|---|
| E_low | 72, of which 64 non-magic | 344, of which 336 non-magic |
| E_full | 16 (8 magic, 8 non-magic, all with N²E_full = 2) | 16 (same) |

So the paper's 344 is the count of weak minima. Please define the term ("no transposition lowers the energy"). With the strict definition the count is 72.

**R1.8 (Cor 4.2, "The mean equals Loly's value for every distribution of arrangements invariant under relabelling of the values").** The group of value relabellings acts simply transitively on arrangements, so the only invariant distribution is the uniform one. As written the sentence is vacuous. The intended statement is presumably "invariant under complementation s ↦ N + 1 − s" (then E z_c = 0 for every cell). Equivalently: "for every distribution with E z_c = 0 for all c", or "under any distribution, E I depends only on E γ, E ρ". Please fix.

**R1.9 (§3.2, after Thm 3.7: "Part (a) improves on k\*(n) ≤ n−3 only for n ≥ 166").** I computed ⌊√(πe(n−1) log(n⁴/4))⌋. It equals n−3 for n = 166, 167, 168 and is strictly smaller only from n = 169. Write "recovers k\* ≤ n−3 from n = 166 and improves on it from n = 169".

**R1.10 (§3.2, eq. after Def 3.6).** "Λ_{n,k} = {γ ∈ Zⁿ : (t−1)^{k+1} | P_γ} = (t−1)^{k+1} Z[t]_{<n−k−1}". This is correct, but it silently uses Gauss's lemma (division by a monic polynomial preserves integrality). Say so in one clause.

**R1.11 (Remark 4.6, "the deficit comes from the two negative terms of (4.4)").** Since (4.4) is an exact formula, "the deficit" needs a reference point. The Gaussian value 2Σw² equals which part of (4.4)? Please write the Gaussian value as 2 tr((σ²Γ)²), relate it to the tr(A²) term explicitly, and then say what the other terms contribute. As written the sentence cannot be checked.

### (c) Jargon and nonstandard terminology (with suggested standard terms)

**R1.12** Invented or nonstandard terms. For each, please either define it on first use with motivation or replace it.

| term | where | suggestion |
|---|---|---|
| "centred value function" | Def 2.1 | "the centred square z" or "the centred entries z" |
| "test functions" | §1, §4 | standard in analysis; in combinatorics "weight vector" or "linear functional". Acceptable if defined once. |
| "low-order energy", "four low-order conditions", "low-order class L_n" | Def 2.4, Remark 2.5, §5.1 | "first-moment and diagonal conditions"; L_n = "arrangements with centred first moments and both diagonal sums equal to M(n)" |
| "degree-k conditions", "moment hierarchy" | Def 3.1, Prop 3.3 | "vanishing of the first k moments of the row- and column-sum vectors" (standard). "Hierarchy" adds nothing. |
| "permutation threshold", "permutation moment threshold" (title) | Def 3.6, title | acceptable as a name for k\*(n), but give the plain-language definition in the abstract's first use: "the largest number of vanishing moments compatible with a non-semi-magic arrangement, plus one" |
| "twins on J", "twin rows", "twin swaps", "twin-row exchange" | Def 3.10, Lemmas 3.11–3.12 | "complementary on J" (the magic-square literature calls entries summing to N+1 complementary, cf. associative squares). The abstract already says "complementary pairs of rows", so the paper uses two names for one notion. |
| "box principle" | Prop 3.13, abstract | the English-language combinatorics term is "pigeonhole principle"; "box principle" is fine for number theorists. Pick one and add "(pigeonhole principle)" once. |
| "column feasibility" | Lemma 3.8 | fine, but it is a majorisation statement: say "majorisation bound" |
| "level n−2", "level n−3", "at the level k" | proof of Thm 3.7(c) | undefined. Write "the lattice Λ_{n,n−2}". |
| "signed mass", "balance", "separable test function", "quantitative balance", "ring imbalance", "unit-vector balance" | §3.7, §6 item 3 | physics metaphors for linear functionals of z; "ring imbalance" = |Σ z_c u_c| with u_c unit radial vectors. Either define once in plain terms or cut §3.7 (see R1.24). |
| "swap gap", "gap d²λ", "a diagonal separates a, b" | Remark 5.2, Fig 4 | "increase of N²E_full under a transposition"; "exactly one of a, b lies on the diagonal" |
| "Gaussian approximation", "Gaussian sd" | Remark 4.6, Table 3 | ambiguous, since a reader expects a normal approximation of E itself. It is a weighted χ² mixture obtained by replacing the linear statistics with Gaussians. Call it "χ²-mixture approximation". |
| "witness" | §3.5 | fine (standard), but define it once: "an arrangement certifying the lower bound" |
| "Siamese square" | §3.5 | the de la Loubère construction; cite or name it so. |
| "product of inertia", "multipole" | Remark 3.4, §3.1 | physics terms; give the formula (already done) and say "mixed moment" consistently |
| "energy" | Def 2.4 | justified by Pinn–Wieczerkowski, but the normalisation by N² (via Cov) differs from theirs. Say so, or use Σδ² directly. |

**R1.13 Notation overloading that a reader will trip over.**
- **k** means the moment degree, the summation index of values (§2.3: "b the centred values k − (N+1)/2"; Thm 4.3), the integer parameter in the proof of Prop 3.14, and the index in A = Σ_k a_k a_kᵀ.
- **t** means the polynomial variable, the integer multiplier (proof of 3.7(c): "γ = tv"), and the column parameter in Prop 3.14.
- **P** means P_γ, P_W (projection), P in Prop 3.14, P_o and P_e (variance polynomials), and the set P in App. B. **Q** likewise means the number of column pairs, Q_o and Q_e, Q in Prop 3.14, and a set in App. B.
- **Cov and Var** mean both the empirical (over cells) covariance and the probabilistic covariance over random π, sometimes in one line (§4: "E[T_φT_ψ] = σ²Cov(φ, ψ)"; (2.6) is probabilistic). Use, e.g., ⟨·,·⟩ or Cov_cells for the empirical one.
- **x** is a coordinate and also the weight index in App. B. **m** is the moment exponent and also n = 2m.
- **N** is n² and also the normal law N(0, 1).
- **U** is U_1..U_4 in §5.1 and U in Prop 3.14. **R_q** (counts) sits next to **R_i** (row indicators).

Please rename locally (for example k → r for the degree in §4, and P, Q, T, U → p, q, τ, υ in Prop 3.14).

### (d) Passages hard to follow

**R1.14 (Abstract).** Sentence 1 is too compressed for a reader who has not seen the reformulation. Sentence 2 ("for real-valued z are equivalent to equal row and column sums exactly when k ≥ n−1") is the trivial Vandermonde fact, yet it reads like a result. The abstract also lists five separate results with no hierarchy. Suggestion: lead with k\*(n) and its definition in words, then the bounds, then the computer values, then "We also …" for the random-arrangement material.

**R1.15 (Prop 3.13 statement).** The column pairing (j_q = 2q vs 2q + 1) and the formula R_q = min(2q, n−4−2q, (n−9)/2) + 1 appear with no motivation. Add one sentence explaining that R_q counts the complementary row pairs whose common column range contains both columns of pair q, and derive the formula from Lemma 3.12(2) (ℓ ≤ 2q and ℓ ≤ n−4−2q). Also: the proof's "(3.4) holds for large n" step for odd n compresses three inequalities into one sentence. Spell out Π(⌈R_q/2⌉ + 1) ≥ Π min(q+1, Q−q)/2 and Σ log min(q+1, Q−q) = 2 log⌊Q/2⌋! + O(log Q).

**R1.16 (Proof of Thm 3.7(b), right side).** "≤ (k²/2) log(n/k) + O(k² + k log n)" hides the Stirling step. One more displayed line would help: Σ_{s≤k} log s! ≥ (k²/2) log k − (3/4)k².

**R1.17 (Lemma 3.9 proof).** "Jensen's formula gives ∫ log|P| = log(|a| Π max(1, |α|)) ≥ 0". This is the Mahler-measure identity M(P) ≥ 1 for nonzero integer polynomials. Name it, since readers in combinatorics know "Mahler measure" better than this form of Jensen. Also say explicitly that P(0) = 0 is allowed.

**R1.18 (§2.3, Hoeffding paragraph).** It is a dense transcription of conditions (11)–(14) and is used once, in Cor 4.5. Consider stating only the product-array criterion (Hoeffding Thm 4) and moving the rest to the proof.

**R1.19 (Proof of Cor 4.5).** "‖a‖₂² is proportional to αᵀC_nα": proportional with which constant? The point is that ‖a‖₂² = Σ α_kα_l corr_kl ‖a_k‖‖a_l‖/τ_kτ_l and ‖a_k‖/τ_k is the same constant σ_n⁻¹ for every k. Say that. Also simplify τ₃²/τ₁² = 12(n−1)/(n²(n²−1)) to 12/(n²(n+1)).

**R1.20 (§4.1, "The means of the two energies coincide if and only if (n²−1)/6 = 2(n−1)/n").** It is not clear where this equation comes from. Dividing the two means by (n−1)(n²+1) gives (n+1)/72 + 1/(6n²) = (n+1)/(6n²), i.e. n(n+1) = 12. Say that.

**R1.21 (§5.1, local limit).** "A Gaussian local limit would therefore give |L_n| ≈ N!(2π)^{−2} det(Σ_U)^{−1/2}." The lattice condition for a local limit concerns the support of (U_1, …, U_4) itself, a coset, not the span of single-transposition increments. Please state precisely what was checked by Smith normal form and why it is the relevant lattice. Since this is labelled a heuristic, a sentence suffices.

**R1.22 (Remark 2.5 and Remark 3.15).** The same n = 4 example is analysed in two places, with γ and ρ given only in the second. Merge them, or give γ = (3, −9, 9, −3) and ρ = (−6, 4, 10, −8) in Remark 2.5.

### (e) Overclaims and framing

**R1.23 (Abstract and §1, "We prove an exact formula for the variance of a quadratic form with zero row sums").** §4 itself says this "is a special case of the classical moment formulas for quadratic assignment statistics [Mantel, Hubert]". "We prove" with Theorem status overstates it. Make it a Proposition with attribution ("we specialise …"), and keep Theorem status for 4.4 if the closed forms are new.

**R1.24 (§3.7 "Balance of the signed mass" and §6 item 3).** This material is, as presented, a list of numerical observations (ring imbalance 2.62, 0.070, 5.51, the 7.4th percentile) with no theorem. It adds jargon and length to a paper whose results are k\*(n) and the variance formulas. Either cut it to a remark or justify why "unit-vector balance" is a natural question.

**R1.25 (§1, "To our knowledge … the closed forms of Theorem 4.4 with the limit law … have not appeared before").** Pinn and Wieczerkowski, and later annealing papers, study the distribution of Σδ² for random arrangements. **Q:** did the author check whether E and Var of Σδ² (at least the mean, which is a two-line computation) appear there? The claim of novelty for the mean in Prop 4.1 should be dropped in any case: it is the sampling-without-replacement variance, as §4.1 itself notes.

**R1.26 (Title).** The title foregrounds "orthogonality conditions", which §1 itself calls "elementary". The main theorem is the two-sided bound on k\*(n). Consider "Moments of line sums of magic squares: a permutation threshold and random line-sum energies", or similar.

**R1.27 (Thm 3.7(c) and §3.5, "We observe (for these n only; this is not a theorem) that … the threshold is determined by the column-feasibility inequalities alone").** Good that it is flagged. But Table 1's "upper bounds" are exactly the column-feasibility test, so this observation is equivalent to "the witness search always succeeded". Say it that way; it is less mysterious.

**R1.28 (Fig 3 caption, "the curve √(2n), the asymptotic order of the lower bound (b)").** Plotting √(2n) next to exact values that are far above it (k\* ≈ 26 vs √80 ≈ 8.9 at n = 40) without comment invites misreading. Also plot the actual bound from (3.4) (k\* ≥ 2 at 14, ≥ 7 at 100) and say that (b) is asymptotic only.

### Questions for the advocate (summary)

- Q1 (R1.1): an explicit, ideally n-uniform, box for (a, b) at the level n−3.
- Q2 (R1.2): a certificate or second implementation for the upper bounds at 34 ≤ n ≤ 40.
- Q3 (R1.3): the precise statement and proof of the √n-optimality remark, and whether √(n log n) is attained by integer vectors with ‖γ‖₁ ≤ n⁴/4.
- Q4 (R1.4): resolved by my recount. Is the Table 4 breakdown cross-checked anywhere?
- Q5 (R1.5, R1.7): definitions of local minimum and of steepest descent.
- Q6 (R1.6): is §2.3 a verbatim transcription of Hoeffding 1951 Thms 3–4?
- Q7 (R1.25): a literature check on E and Var of Σδ² for random arrangements.

## ADVOCATE — turn 1

I re-read all of main.tex, sections/*.tex and the anc/ scripts that bear on the reviewer's points. My scratch computations are in `scratchpad/adv/a1.py`–`a7.py`. They use exact integer/rational arithmetic, plus SymPy for the series expansions. Overall I accept R1.1–R1.28 almost entirely. Two points get a partial DISAGREE: R1.10 (naming of the lemma used) and R1.21 (the lattice is the right one; only the sentence is unclear). One point needs a CLARIFY of what is actually claimed: R1.25. A new, cleaner proof for R1.1 is given below.

### (a) Claims the reviewer could not verify

**A1.1 (R1.1, level n−3) — AGREE, with a proof that removes the computer step.** No box is needed. For 18 ≤ n the following two lines prove k\*(n) ≤ n−3, and they also replace the f(n)/Thm 3.7(a) argument and the 18 ≤ n ≤ 400 loop. I checked both inequalities in `a1.py` for all 18 ≤ n < 2000, and they are monotone beyond that.
- The current text says (§3.5, "n ≥ 18: level n−3"): "Two consecutive central coefficients bound |a|, |b|, and checking all pairs (a, b) in the resulting box shows that for 18 ≤ n ≤ 400 … For n ≥ 166, part (a) gives …".
- Proposed replacement:
  > *n ≥ 18: level n−3.* Λ_{n,n−3} has rank 2: P_γ = (t−1)^{n−2}(a+bt) with a, b ∈ ℤ. Evaluating at t = −1 gives 2^{n−2}|a−b| = |P_γ(−1)| ≤ ‖γ‖₁ ≤ n⁴/4 by Lemma 3.8. Since n⁴ < 2ⁿ for n ≥ 17, this forces a = b, so P_γ = a(t−1)^{n−2}(t+1). By Parseval, Σ_j γ_j² = a² ∫₀¹ |e^{2πiθ}−1|^{2(n−2)} |e^{2πiθ}+1|² dθ = 2a² C_{n−2}, where C_m = binom(2m, m)/(m+1) is the Catalan number. At n = 18, 2C_{16} = 70,715,340 > 50,860,872 = n⁵(n²−1)/12. From n to n+1 the left side grows by the factor 2(2m+1)/(m+2) ≥ 11/3 and the right side by less than 3/2. So 2C_{n−2} > n⁵(n²−1)/12 for all n ≥ 18, and a ≠ 0 contradicts Lemma 3.8. Hence k\*(n) ≤ n−3 for every n ≥ 18.
- Identity check: Σ coeff² of (1−t)^m(1+t) = 2C_m for m ≤ 11, by expansion (`a1.py`).
- Consistency: at n = 16, 17 the ℓ² test fails (2C_{n−2} < n⁵(n²−1)/12), which agrees with k\*(16) = 14 and k\*(17) = 15.
- Consequences for the paper:
  - Thm 3.7(c) "k\* ≤ n−3 for n ≥ 18" becomes computer-free.
  - Delete "(18 ≤ n ≤ 400)" and the f(n) sentence.
  - The rank-2 loop in `kstar_verify.py` stays only as a sanity check.
  - Also replace "γ = tv with t ∈ ℤ" by "γ = cv with c ∈ ℤ" (see R1.13).

**A1.2 (R1.2, upper bounds 34 ≤ n ≤ 40) — AGREE on the wording. Here is a certificate.** The check at the decisive level is fast. Running `has_feasible(n, k*(n))` from `anc/kstar_verify.py` gives "none" in < 0.1 s for n = 34 and n = 40, and level k\*(n)−1 gives "feasible" (`a5.py`). The "few hours" in the README is for the descending scan up to n = 100. A human-auditable certificate exists (`a6.py`, `a7.py`) and splits into two cases:
- **n = 35, 37, 39, 40.** For the LLL-reduced basis (b_i) of Λ_{n,k\*} the Gram–Schmidt norms satisfy min_i ‖b_i\*‖² > R² := n⁵(n²−1)/12, with ratios 1.385, 1.993, 2.378, 1.207. Since λ₁(Λ) ≥ min_i ‖b_i\*‖ holds for every basis, no nonzero lattice vector is short enough, and no enumeration is needed. The same holds for n = 14–19, 21, 23, 25, 27–33.
- **n = 34, 36, 38** (and 20, 22, 24, 26). The ball ‖γ‖² ≤ R² contains exactly 6, 2, 2 (and 2, 2, 6, 6) nonzero lattice vectors. Every one has max_j |γ_j| > n²(n−1)/2; for example, the smallest max entry is 21,298 > 19,074 at n = 34. So each one already fails (3.1) with p = 1.

Proposals:
- Ship `anc/kstar_certificates.json`. For each 14 ≤ n ≤ 40 it gives the LLL basis at level k\*(n), the exact GS norms, and the complete list of nonzero vectors inside the radius with a violated instance of (3.1).
- Add a 30-line checker that needs no LLL or enumeration: it verifies that the basis spans Λ (unimodular transform from the basis {t^i(t−1)^{k+1}}), recomputes the GS norms, and checks the listed vectors.
- For n = 34, 36, 38 the completeness of the list still relies on the Fincke–Pohst search. I re-ran it with my own recursion (`a7.py`), but that is the same algorithm, not an independent method.
- Abstract wording: "…and, with computer assistance, we determine k\*(n) for all n ≤ 40". The Table 1 caption keeps the sentence on which n are double-checked, plus the GS-certificate remark above.

**A1.3 (R1.3, √n-optimality remark) — AGREE.** The sentence uses the wrong class. Fix it with H = ⌊n³/4⌋, so that ‖γ‖₁ ≤ n·H ≤ n⁴/4 and also |γ_j| ≤ n²(n−1)/2:
- Proposed replacement for the last sentence of §3.3:
  > "The hypothesis ‖γ‖₁ ≤ n⁴/4 alone cannot give an upper bound of smaller order than √n. The (H+1)ⁿ vectors g ∈ {0,…,H}ⁿ with H = ⌊n³/4⌋ have binomial moments μ_r(g) = Σ_j binom(j, r) g_j in [0, H·binom(n, r+1)]. So if (H+1)ⁿ > Π_{r<K}(H·binom(n, r+1)+1), two of them, g ≠ g′, share μ_0, …, μ_{K−1}. Then γ = g − g′ is nonzero, ‖γ‖₁ ≤ n⁴/4, and (t−1)^K | P_γ. Taking logarithms, the inequality holds for some K ≥ c√n."
- Asymptotically K² ≈ 12n. Exact values of the largest such K (`a3.py`): n = 100 → 26, n = 10³ → 96, n = 10⁴ → 321, n = 10⁵ → 1040. That is K/√n = 2.6, 3.04, 3.21, 3.29, approaching √12.
- §6 item 1, proposed: "The upper bound uses only that γ is a nonzero integer vector with ‖γ‖₁ ≤ n⁴/4. For that class the pigeonhole principle produces vectors vanishing to order ≍ √n at 1 (§3.3), so a bound of smaller order than √n needs more information about γ. Whether the √(n log n) of Lemma 3.9 is attained within this class is, as far as we know, open. It is a separate question from realisability, i.e. which such vectors are column deviations of arrangements."
- **On Q3 (sharpness):** I cannot confirm from the sources available here that Borwein–Erdélyi–Kós show sharpness in the size of the coefficients for *integer* coefficients. Their extremal examples are real-coefficient polynomials. So I would not assert sharpness.
- The analogy in §3.4 is accurate as an analogy: in both settings the pigeonhole construction loses a √log n factor against the Jensen/Mahler bound. Proposed wording: "In both settings the upper bound comes from Jensen's formula and the lower construction from the pigeonhole principle, and they differ by a factor √(log n)."

**A1.4 (R1.4, |L_4| and Table 4) — AGREE.**
- Add to the proof of Prop 5.1: "An independent meet-in-the-middle recount written in NumPy (anc/…) gives the same number." Ship the reviewer's `c9.py` (131 s) as `anc/lowmode_recount.py`, with credit in the README.
- Table 4 cross-checks that exist:
  - `enum_n4.jsonl`, separate runs of the enumerator: mode ROWSL (all four rows = 34 within L₄) gives 117,104 and COLSL gives 117,104. Both equal the "4" margin of Table 4. MAGIC gives 7,040, matching the bold cell.
  - The table is symmetric, as transposition requires.
  - These are the same program in different modes, not an independent check. I suggest the reviewer's recount also output the 3×3 histogram. That is cheap once the matching pairs are expanded.

**A1.5 (R1.5, steepest descent) — AGREE; the choices are in `anc/algorithms.py::greedy_run`.**
- Each step evaluates ΔF over all binom(N, 2) transpositions.
- It takes the minimiser; `np.argmin` breaks ties by the first pair in `np.triu_indices` order.
- It moves only if ΔF < 0 and stops otherwise, so it stops at weak minima.
- 2×10⁵ independent uniformly random starts per n (`algo_results.json`): success 0.1952 ± 0.0009, 0.01153 ± 0.00024, 0.00788 ± 0.00020 for n = 4, 5, 6.
- Proposed text for §5.2: "Steepest swap descent on E_full (at each step perform the transposition with the most negative energy change, ties broken by the first cell pair in row-major order; stop when no transposition lowers N²E_full) reaches a magic square in 19.5 % (±0.1 %), 1.2 % and 0.8 % of 2×10⁵ runs from uniformly random starts for n = 4, 5, 6."

**A1.6 (R1.6, Hoeffding) — CLARIFY.** In the previous revision the author consulted the original (Ann. Math. Statist. 22 (1951) 558–566); see `review_notes/response_to_referee.md`, C2, and commit 34a69aa.
- §2.3 transcribes three things:
  - Thm 3, with condition (11): N⁻¹ΣΣ d^r / (N⁻¹ΣΣ d²)^{r/2} → 0 for r = 3, 4, …, with d^r and not |d|^r. Hoeffding's n is our N.
  - Condition (12): max d² / (N⁻¹ΣΣ d²) → 0, which implies (11).
  - Thm 4, for c(i, j) = a_i b_j: condition (13), implied by (14).
- I cannot open the 1951 paper from here, so the reviewer should spot-check pp. 560–562.
- I agree with R1.18 that (11) is not needed in the paper (see A1.18). That leaves only (14) to transcribe, which reduces the exposure.

### (b) Errors and ambiguities

**A1.7 (R1.7) — AGREE.** `anc/verify_numbers.py` l. 83 counts minima as "no swap with strictly smaller energy", i.e. weak minima. That gives 344 for E_low. The E_full count is 16 under either definition.
- Proposed text: "Call S a *swap-local minimum* if no transposition lowers the energy. For n = 3, besides the eight magic squares, E_full has eight such minima, all with N²E_full = 2, and all are strict. E_low has 344, of which 336 are non-magic; only 72 of these (64 non-magic) are strict."
- Also define the term once in Remark 5.2.

**A1.8 (R1.8) — AGREE; the sentence is vacuous as written.**
- From (3.3), E I = n²(n⁴−1)/12 + Σ_j x_j² E γ_j + Σ_i y_i² E ρ_i.
- Replacement: "The mean equals Loly's value n²(n⁴−1)/12 for every random arrangement with E z_c = 0 for every cell, for instance any distribution invariant under complementation s ↦ N+1−s; magic and semi-magic squares take this value exactly."

**A1.9 (R1.9) — AGREE.** Confirmed: ⌊√(πe(n−1)log(n⁴/4))⌋ = 163, 164, 165 = n−3 at n = 166, 167, 168, and 165 < 166 at n = 169 (`a1.py`). The sentence becomes moot for (c) after A1.1.
- Proposed text: "Part (a) gives k\* ≤ n−3 from n = 166 on and improves on it from n = 169; for smaller n the exact results of (c) are much stronger."

**A1.10 (R1.10) — AGREE to add the clause; DISAGREE on the name.** The equality needs only the division algorithm by a monic polynomial, not Gauss's lemma.
- Proposed text: "…= (t−1)^{k+1}ℤ[t]_{<n−k−1} (the quotient of an integer polynomial by the monic polynomial (t−1)^{k+1} has integer coefficients), a lattice of rank n−k−1."

**A1.11 (R1.11) — AGREE; the sentence was imprecise, and partly wrong in attribution.** I decomposed the exact variance with SymPy (`a2.py`). With σ_n² = (N+1)/12 and tr(A²) = N⁻² tr(Γ²), the Gaussian (χ²-mixture) variance is 2 tr((σ_n²Γ)²) = N²(N+1)²/72 · tr(A²). Each term of (4.4) divided by this value:
- The tr(A²) term: (N−1)(5N+6)/(5N(N+1)) = 1 − (4N+6)/(5N(N+1)) = 1 − 4/(5n²) + O(n⁻⁴).
- The (tr A)² term: −4/(5n) for E_full, and −4/(5n²) for E_low.
- The Σ A_aa² term: −6/(5n) − 3/(5n²) for E_full, and −42/(25n²) for E_low.
- Totals: 1 − 2/n − 7/(5n²) for E_full and 1 − 82/(25n²) for E_low, which matches Remark 4.6.

So the tr(A²) coefficient also falls short of the Gaussian value, at order n⁻². "The deficit comes from the two negative terms" is correct only for the 1/n term of E_full. Proposed replacement:
> "The Gaussian variance is 2 tr((σ_n²Γ)²) = N²(N+1)²tr(A²)/72. In (4.4) the coefficient of tr(A²) is this value times 1 − (4N+6)/(5N(N+1)), and the (tr A)² and ΣA_aa² terms are negative. For E_full the latter two give the leading deficit −4/(5n) − 6/(5n), whereas for E_low all three terms contribute only at order n⁻² (−4/5, −4/5, −42/25)."

### (c) Jargon and notation

**A1.12 (R1.12) — AGREE on almost all rows.** Concrete replacements, by row:
- "centred value function" → "the centred entries z" (Def 2.1: "We write z = z(S) for the matrix of centred entries").
- "test function" → keep, defined once in §1: "a test function is a real function φ on the cells; we use it only through the linear functional ⟨φ, z⟩." Each later "for every test function" stays correct.
- "low-order energy / four low-order conditions / low-order class L_n" → "the four-term energy E₄" and "the class L_n of arrangements whose first moments vanish and whose diagonal sums equal M(n)". Rename the macro \Elow → E₄ throughout. "Low-order" carries no meaning in its own right.
- "degree-k conditions" → keep the label (it is used in many statements), but define it in words in §1: "the first k moments of the column-sum and of the row-sum vectors vanish". Drop "hierarchy": Prop 3.3 becomes "Moment conditions and line sums", and §3 becomes "Moment conditions and the permutation threshold".
- "permutation threshold" → keep it as the name of k\*(n), defined in words at first use (abstract and §1).
- "twins on J", "twin rows", "twin swaps", "twin-row exchange" → "complementary on J", "complementary rows", Lemma 3.11 "Swaps in complementary rows", Lemma 3.12 "Squares with many complementary rows". AGREE that two names for one notion is a defect.
- "box principle" → "pigeonhole principle", in the title of Prop 3.13 ("Pigeonhole criterion"), the abstract and §1.
- "column feasibility" → title of Lemma 3.8: "Majorisation bound for column deviations". Inline "(3.1)" replaces "column-feasibility inequalities", and §3.5/§6 say "the inequalities (3.1)".
- "level n−2", "level k" → "the lattice Λ_{n,n−2}". Delete "level" everywhere, including the appendix ("the least k for which Λ_{n,k} has no vector satisfying (3.1)").
- "signed mass", "balance", "separable test function", "ring imbalance" → see A1.24; most of these go. "Separable" in Prop 3.3(a) becomes "functions of the form a(x)+b(y)".
- "swap gap", "a diagonal separates a, b" → "the increase d²λ(a, b) of N²E_full" and "exactly one of a, b lies on the main diagonal (resp. anti-diagonal)". The Fig 4 caption says "increase of N²E_full under a single transposition".
- "Gaussian approximation" / "Gaussian sd" → "χ²-mixture approximation" / "χ²-mixture sd" (Remark 4.6 title, Table 3 header, Fig 2 caption).
- "witness" → "a *witness* for k\*(n) ≥ K is an arrangement that satisfies the degree-(K−1) conditions and is not semi-magic", placed before Thm 3.7.
- "Siamese square" → "a Siamese (de la Loubère) magic square [andrews1960magic]".
- "product of inertia", "multipole" → Remark 3.4: "the mixed moment Σ z_c x_c y_c (Loly's product of inertia)" on first use, then "mixed moment" only. §3.1 keeps "multipole" only inside the citation phrase.
- "energy" → one added clause after (2.8): "Pinn and Wieczerkowski use Σ_L δ_L² = N²E_full; the factor N⁻² comes from writing the terms as covariances."

**A1.13 (R1.13) — AGREE.** Local renames:
- Value index (§2.3, §4, Thm 4.3): k → v, so b_v = v − (N+1)/2, 1 ≤ v ≤ N.
- The test-function index in A = Σ a_k a_kᵀ, T_k, τ_k, α_k (§4.2, Cor 4.5): k → ℓ.
- Proof of 3.7(c): γ = tv → γ = cv, c ∈ ℤ.
- Prop 3.14 (n = 3): (t, u) → (g, r), so γ = (g, −2g, g) and ρ = (r, −2r, r); (k, P, Q, T, U) → (κ, μ, ν, ξ, η). The identity becomes Σz² = 2(4κ² + 3(μ² + ν²) + ξ² + η²) = 60. Update `n3_lowmode_proof.py` labels to match.
- Variance polynomials P_o, P_e, Q_o, Q_e → F_o, F_e, G_o, G_e. Projection P_W → π_W stays distinct from P_γ. App B sets P, Q → 𝒫, 𝒬. Prop 3.13: Q → q_max, or keep Q since 𝒬 is now distinct.
- Covariances: the empirical one over cells becomes ⟨φ − φ̄, z⟩ written as Cov_□(φ, Z), defined in §2.1 as "the covariance over a uniformly random cell". Cov/Var/E without a subscript are then probabilistic over the random arrangement. Example: E[T_φ T_ψ] = σ_n² Cov_□(φ, ψ).
- Normal law: 𝒩(0, 1).
- App B weight index x → w-index ι.
- §5.1 U₁…U₄ stay (Prop 3.14's U is renamed); "R_q" → "r_q" to separate it from the row indicators R_i.
- Moment exponent m and n = 2m (Lemma 3.12, App B): rename the half-order to h (n = 2h).

### (d) Readability

**A1.14 (R1.14) — AGREE.** Proposed abstract (same facts, plainer, results ranked):
> An n×n arrangement of 1, …, n² is semi-magic if all its row and column sums are equal. If they are, then for every m the m-th moments Σ s_{ij} j^m and Σ s_{ij} i^m equal those of the constant matrix; for real matrices the converse needs the moments up to m = n−1. For arrangements fewer suffice. Let the *permutation threshold* k\*(n) be the least k such that every arrangement whose moments of orders 1, …, k agree with the constant matrix is semi-magic. In terms of the column-sum deviations γ these conditions say that Σ_j γ_j t^j is divisible by (t−1)^{k+1}, which links k\*(n) to the Prouhet–Tarry–Escott problem and to work of Borwein, Erdélyi and Kós on integer polynomials with a zero of high order at 1. We prove (√2−o(1))√n ≤ k\*(n) ≤ √(πe(n−1)log(n⁴/4)); the lower bound uses semi-magic squares with many pairs of complementary rows and the pigeonhole principle. Further, k\*(n) = n−1 for n ≤ 13, k\*(n) = n−2 for 14 ≤ n ≤ 17 and k\*(n) ≤ n−3 for all n ≥ 18, and with computer assistance we determine k\*(n) for all n ≤ 40. We also treat uniformly random arrangements: we give the exact mean and variance of the sum of squared line-sum deviations and of a four-term energy formed from the first moments and the two diagonals, show that the four-term energy divided by its mean converges in distribution to Exp(1), give the null distribution of Loly's moment-of-inertia invariant, and count the 14,639,440 arrangements of order 4 with vanishing four-term energy, of which 7,040 are magic.

**A1.15 (R1.15) — AGREE.**
- Add after the definition of R_q: "For odd n the q-th pair consists of the columns 2q+1, 2q+2, and the complementary rows ℓ, n−1−ℓ of Lemma 3.12(2) cover both columns if and only if ℓ ≤ 2q and ℓ ≤ n−4−2q. Since 0 ≤ ℓ ≤ (n−9)/2, this gives R_q."
- Replace the odd-n left-side sentence in the proof of (b) by: "With Q = (n−3)/2 we have R_q ≥ min(2q, 2(Q−q)−1, Q−3)+1 ≥ min(q+1, Q−q) once Q ≥ 7, so ⌈R_q/2⌉+1 ≥ min(q+1, Q−q)/2. Hence log(left side) ≥ Σ_{q<Q} log min(q+1, Q−q) − Q log 2 ≥ 2 log(⌊Q/2⌋!) − Q log 2 = (n/2) log n − O(n)."
- I checked each step by hand. The min(…) ≥ min(q+1, Q−q) step needs (Q+1)/2 ≤ Q−3, i.e. Q ≥ 7. This is fine for large n.

**A1.16 (R1.16) — AGREE**, with a slightly weaker but provable constant. From log s! ≥ s log s − s and Σ_{s≤k} s log s ≥ ∫₀^k x log x dx = (k²/2) log k − k²/4 we get Σ_{s≤k} log s! ≥ (k²/2) log k − (3/4)k² − k/2. The reviewer's version without −k/2 also holds numerically for k < 3000 (`a3.py`), but the derivation gives the −k/2.
- Proposed display: Σ_{s=1}^{k}(s log n − log s!) ≤ (k(k+1)/2) log n − (k²/2) log k + (3/4)k² + k/2 = (k²/2) log(n/k) + O(k² + k log n).

**A1.17 (R1.17) — AGREE.** Proposed text: "The Mahler measure M(P) = |a| Π_α max(1, |α|) of a nonzero P ∈ ℤ[t] is at least 1, because |a| ≥ 1, and by Jensen's formula log M(P) = ∫ log|P(e^{2πiθ})| dθ. Roots at 0 (i.e. γ₀ = 0) contribute max(1, 0) = 1 and are allowed."

**A1.18 (R1.18) — AGREE.** Cor 4.5 uses only product arrays, since a = Σ α_ℓ a_ℓ/τ_ℓ and d(c, v) = a_c b_v.
- Replace the §2.3 paragraph by: "Hoeffding's combinatorial central limit theorem [Thm 4] states that for real vectors a^{(N)}, b^{(N)} the statistic Σ_i a_i b_{π(i)} is asymptotically normal if N · max_i(a_i−ā)² · max_j(b_j−b̄)² / (Σ_i(a_i−ā)² · Σ_j(b_j−b̄)²) → 0 (his condition (14)); Motoo … Bolthausen …".
- Drop (2.4) and (2.5).
- The proof of Cor 4.5 then checks this one quotient directly. The displayed identity already does that; drop the reference to (2.5).

**A1.19 (R1.19) — AGREE.** Var T_ℓ = σ_n² Var_□(φ_ℓ) = σ_n² N ‖a_ℓ‖₂², so ‖a_ℓ‖₂/τ_ℓ = (σ_n√N)⁻¹ for every ℓ and ‖a‖₂² = αᵀC_nα/(Nσ_n²).
- Insert exactly this sentence in place of "is proportional to".
- Replace τ₃²/τ₁² = 12(n−1)/(n²(n²−1)) with 12/(n²(n+1)); I checked that the two are equal.

**A1.20 (R1.20) — CLARIFY.** Both energies contain the two diagonal terms. The remaining terms have means 2(n⁴−1)/144 (from X, Y) and 2n·(n−1)(n²+1)/(12n²) (from the 2n rows and columns), by (4.1). Dividing by (n−1)(n²+1)/6, these are (n+1)/12 and 1/n, which agree iff n(n+1) = 12.
- Proposed text: "The two means differ only through the X, Y terms of E₄ and the 2n row and column terms of E_full, whose means are 2(n⁴−1)/144 and (n−1)(n²+1)/(6n). These agree if and only if n(n+1) = 12, i.e. n = 3, where both energies have mean 40/27."

**A1.21 (R1.21) — partly DISAGREE: the lattice checked is the relevant one, but the sentence needs the reason.**
- Any two arrangements differ by a product of transpositions. So the differences U(S) − U(S′) over all pairs generate the same lattice Λ_U as the single-transposition increments.
- The support of U is therefore contained in a coset of Λ_U, and Λ_U is the smallest lattice with that property. This is exactly the lattice whose covolume enters a local limit (`anc/gaussian_estimate.py` l. 12–15 computes its index by Smith normal form).
- Proposed text: "Since every two arrangements differ by a product of transpositions, the differences of (U₁, …, U₄) generate the same lattice as the increments of single transpositions. By a Smith normal form computation (n ≤ 8) this lattice is ℤ⁴, so U is not confined to a coset of a proper sublattice, and a Gaussian local limit would give |L_n| ≈ N!(2π)⁻² det(Σ_U)^{−1/2}. We use this only as a heuristic."

**A1.22 (R1.22) — AGREE.**
- Add to Remark 2.5: "so γ = (3, −9, 9, −3) and ρ = (−6, 4, 10, −8)". I re-checked them from the printed S.
- In Remark 3.15 keep only "this arrangement satisfies the degree-2 condition in x but not in y (Remark 2.5)".

### (e) Framing

**A1.23 (R1.23) — AGREE.**
- Make 4.3 "Proposition 4.3 (Hubert [1987], Mantel [1967]; specialised to zero row sums and centred values)".
- Abstract: "we specialise the classical variance formula for quadratic assignment statistics to quadratic forms with zero row sums". §1: "We specialise … (Proposition 4.3)".
- Thm 4.4 keeps Theorem status. Its closed forms and the limit law are what §1 claims.

**A1.24 (R1.24) — AGREE to cut to one remark.**
- Delete the subsection heading and the "signed mass" framing.
- Keep the Cauchy–Schwarz inequality and the bound n E_full ≤ ‖π_W z‖² ≤ λ_n E_full as Remark 2.6, "Linear functionals and E_full", placed after Lemma 2.3. This is a genuine (if simple) statement linking E_full to every φ ∈ W.
- The ring computation becomes one sentence there: "Nonlinear functionals are not controlled: with u_c the unit vector from the centre to cell c, |Σ_c z_c u_c| = 2(2−√2)√5 for every magic square of order 3 and is positive for all 880 of order 4 (anc/balance_check.py)."
- Drop open question 3. The author's motivation was the link to the convex-hull picture of the companion paper, which belongs there.

**A1.25 (R1.25) — CLARIFY.** §1 does not claim novelty for the mean. The sentence lists Thm 3.7, "the closed forms of Theorem 4.4 with the limit law", Cor 4.2 and Prop 5.1, and Thm 4.4 is the variances.
- On Pinn–Wieczerkowski: the author checked the paper (IJMPC 9 (1998) 541–546) last round for the definition of the energy (response C1/§4.2). That paper uses parallel tempering to estimate the number of magic squares and, as far as the response records, gives no exact E or Var of Σ_L δ_L² under the uniform distribution. I cannot re-open it from here.
- Proposed edits:
  - In the novelty sentence, "the closed forms of Theorem 4.4" → "the closed forms for the variances in Theorem 4.4"; "Corollary 4.2" → "the variance in Corollary 4.2".
  - After Prop 4.1 add: "The means are elementary (sampling without replacement)."
  - Keep "to our knowledge".

**A1.26 (R1.26) — AGREE in substance; the choice is the author's.** Offer: "Moments of line sums of magic squares: a permutation threshold and random line-sum energies". This keeps "permutation threshold", which is the defined term, and drops "orthogonality conditions". The orthogonality framing stays as the one-paragraph reformulation in §1.

**A1.27 (R1.27) — AGREE.** Proposed text: "For each 14 ≤ n ≤ 40 the witness search succeeded at the last k at which Λ_{n,k} still contains a vector satisfying (3.1), so k\*(n) equals the least k for which Λ_{n,k} contains no nonzero vector satisfying (3.1). We do not know whether this holds for all n."

**A1.28 (R1.28) — AGREE.**
- Recomputed best K from (3.4) (`a4.py`): n = 14 → 2, 20 → 2, 30 → 3, 40 → 4, 60 → 5, 80 → 6, 100 → 7, 200 → 12, 400 → 18. For n = 15 and 17 (odd, small R_q) it gives only the trivial bound.
- Plot this step curve, the proved lower bound for each n, in place of, or next to, √(2n).
- Caption: "…the lower bound given by (3.4) (open squares), and √(2n), the asymptotic order of that bound (b), which (3.4) approaches slowly."

### Questions back to the reviewer
- QA1 (A1.1): please check the Parseval/Catalan step. If it stands, Thm 3.7(c) for n ≥ 18 needs no computer.
- QA2 (A1.2): is the GS-norm certificate plus explicit short-vector lists for n = 34, 36, 38 enough for you to accept "computer-assisted, for all n ≤ 40", or do you want a non-enumerative check for those three n?
- QA3 (A1.12/A1.13): do you accept renaming \Elow → E₄ and Cov → Cov_□ for the empirical covariance? These touch many lines, and a consolidation pass will be needed.

## REVIEWER — turn 2

My new scratch checks are `scratchpad/dialogue/d1.py`–`d7.py`. They use exact integer/rational arithmetic, except for the NumPy integer recounts. The checks in d3.py–d7.py are my own implementations, written without reading the advocate's a*.py.

### Follow-up on the advocate's answers

**R2.1 (A1.1, rank-2 lattice by hand) — ACCEPTED, verified.**
- The t = −1 step is right: |P_γ(−1)| = 2^{n−2}|a−b| ≤ ‖γ‖₁ ≤ n⁴/4. This forces a = b exactly when 2^n > n⁴, i.e. n ≥ 17. At n = 16 the two sides are equal and the argument fails.
- The Parseval/Catalan identity is also right. Σ_j (binom(m,j) − binom(m,j−1))² = 2binom(2m,m) − 2binom(2m,m+1) = 2C_m. I checked it symbolically for m < 25 and checked 2C_{n−2} > n⁵(n²−1)/12 for all 18 ≤ n ≤ 2000 (d1.py). The growth-ratio argument covers the rest.
- At n = 17 the ℓ² test fails (2C₁₅ = 19,389,690 < 34,076,568), consistent with k\*(17) = 15.

Requests:
- Cite Lemma 3.8 for both inequalities (‖γ‖₁ and ‖γ‖₂).
- Present the n−2 and n−3 cases together as "Λ_{n,n−2} and Λ_{n,n−3} by hand". Then the only computer-assisted part of Thm 3.7(c) is the table for 18 ≤ n ≤ 40, and the f(n) sentence and the 400-loop disappear.

**R2.2 (A1.2, certificate for 34 ≤ n ≤ 40) — ACCEPTED, with one correction to the advocate's claim.**

I wrote an independent exact LLL (Fractions, δ = 0.99) and Schnorr–Euchner enumeration (d3.py) and ran it on Λ_{n,k\*(n)} for 18 ≤ n ≤ 40. It confirms every upper bound in Table 1. It also matches the advocate's picture:
- For n = 18, 19, 21, 23, 25, 27–33, 35, 37, 39, 40, min_i‖b_i\*‖² > R², so no enumeration is needed.
- The ball contains exactly 2, 2, 6, 6, 6, 2, 2 nonzero vectors for n = 20, 22, 24, 26, 34, 36, 38, and none of them satisfies (3.1).

The correction: the claim "every one has max_j|γ_j| > n²(n−1)/2" is **false at n = 26**. The pair ±(−1, 16, −117, 513, …, 8398, −5814, 1938, 1938, −5814, 8398, …) has max entry 8398 < 8450. It is excluded only by p = 2: 8398 + 8398 = 16,796 > 2·26·(676 − 52)/2 = 16,224 (d4.py). The certificate file must therefore record, for each vector, the p and the column set J that violate (3.1), not just the max entry.

Also, the Gram–Schmidt ratios depend on the basis. I get 1.637 at n = 35 against the advocate's 1.385, both > 1. So the certificate must ship the reduced basis itself, as proposed.

Answer to QA2: with the shipped certificate, the MILP cross-check for n ≤ 33, and now a second independent enumeration for 34–40, I accept "with computer assistance, k\*(n) for all n ≤ 40". Please ship d3.py (≈ 35 s for n ≤ 40) in anc/ as the second implementation.

**R2.3 (A1.3, the √n remark) — ACCEPTED, with a request to state the constant.**
- Verified K = 26, 96, 321 at n = 10², 10³, 10⁴ (d2.py).
- The "taking logarithms" step should be shown. One line suffices: the right side is ≤ (2H)^K n^{K(K+1)/2} and the left side is ≥ H^n, so K = ⌊2√n⌋ works once n is large (2n log n + O(√n log n) < 3n log n − O(n)). Write "K ≥ 2√n for all large n" rather than "K ≍ √n".
- On sharpness: I looked up Borwein–Erdélyi–Kós, Acta Arith. 159 (2013) 387–395. They treat real coefficients normalised by the constant term (κ_∞(n,L) ≍ √(n/L)), not integer coefficients of size M. So I agree that sharpness of √(n log n) for integer γ with ‖γ‖₁ ≤ n⁴/4 must not be asserted. The advocate's §6 wording is fine.

**R2.4 (A1.4, Table 4) — partly closed by my own recount.** Row sums split across the top/bottom halves of the meet-in-the-middle, so I extended my recount to tag each half by its number of rows with sum 34 (d6.py). I get:
- Row margins 11,910,864 / 2,611,472 / 0 / 0 / 117,104, with total 14,639,440.
- A separate direct enumeration over ordered partitions into four 34-sets (d5.py) gives the row-"4" line exactly: 100,728 / 9,336 / 7,040.
- The same split with only U₁, U₂ (d7.py) gives 6,697,177,424, which confirms that number in Prop 5.1.

Given symmetry and these margins, one degree of freedom remains unchecked: the (1,1) cell 429,312, equivalently the (0,1) cell 2,172,824. That is acceptable. State in the paper which entries are independently recounted.

**R2.5 (A1.5) — ACCEPTED.**
- I checked `greedy_run` (algorithms.py l. 39–56): strict improvement only, argmin tie-break, 2×10⁵ runs.
- Avoid "swap-local minimum" (A1.7) as a new term. Write "a local minimum with respect to transpositions (no transposition lowers the energy)".

**R2.6 (A1.6, Hoeffding) — OPEN, but reduced.** I could not reach the original either (Project Euclid fetch failed). After A1.18 only condition (14) of Thm 4 is used. That is the classical Wald–Wolfowitz–Noether–Hoeffding product condition, and its form matches the one I know. Accepted on condition that the author checks this one display against the printed page and cites the page.

**R2.7 (A1.7, A1.8, A1.9, A1.20, A1.22, A1.23, A1.25, A1.27) — ACCEPTED as proposed.**

**R2.8 (A1.10) — I withdraw "Gauss's lemma"; the advocate is right.** Division by a monic integer polynomial is all that is needed.

**R2.9 (A1.11) — ACCEPTED, verified term by term (d1.py).**
- The (tr A)² term contributes −4/(5n) for E_full and −4/(5n²) for E_low.
- The tr A² term contributes 1 − 4/(5n²) in both cases, exactly 1 − (4N+6)/(5N(N+1)).
- The ΣA_aa² term contributes −6/(5n) − 3/(5n²) for E_full and −42/(25n²) for E_low.

Note that the n⁻³ terms of E_full differ by parity (13/5 odd, 16/5 even), so "O(n⁻³)" is correct as written.

**R2.10 (A1.12, A1.13; QA3).**
- E₄: accept.
- Cov_□: I would go further. Since z̄ = 0, Cov(φ, Z) = ⟨φ, z⟩ for every φ (Lemma 2.2). So drop the empirical Cov/Var entirely:
  - write the energies as Σ⟨φ, z⟩²;
  - write Var(X) as ‖x‖² = (n²−1)/12;
  - write the Gram matrix as Γ_{kl} = ⟨φ_k − φ̄_k, φ_l − φ̄_l⟩.
  
  Then Cov, Var and E without decoration are always probabilistic, and no new symbol is introduced.
- Renames: (g, r) in Prop 3.14 clashes with g ∈ ΠF_q in Prop 3.13 and with the binomial index r in Lemma 3.2. Choose letters from a symbol inventory. The consolidation round should produce that inventory.

**R2.11 (A1.14, abstract) — ACCEPTED with edits.**
- (i) "moments … equal those of the constant matrix": say "of the matrix with all entries (n²+1)/2", or equivalently Σ s_{ij} j^m = M(n) Σ_j j^m.
- (ii) "k\*(n) = n−1 for 3 ≤ n ≤ 13".
- (iii) Say which values are proved by hand and which with computer assistance. After R2.1: n−1 (n ≤ 13) needs only checked witnesses; n−2 (14–17) and ≤ n−3 (n ≥ 18) are proved by hand; the exact values 18 ≤ n ≤ 40 are computer-assisted.

**R2.12 (A1.15) — ACCEPTED.** Small correction: min(2q+1, 2(Q−q), Q−2) ≥ min(q+1, Q−q) needs only (Q+1)/2 ≤ Q−2, i.e. Q ≥ 5, not Q ≥ 7. This is harmless.

**R2.13 (A1.16, A1.17, A1.18, A1.19, A1.21) — ACCEPTED, verified.**
- A1.16: Σ s log s ≥ ∫₀^k x log x dx holds termwise, since x log x ≤ s log s on [s−1, s].
- A1.19: ‖a_ℓ‖/τ_ℓ = (σ_n√N)⁻¹; τ₃²/τ₁² = 12/(n²(n+1)).
- A1.21: differences of U over pairs of arrangements generate the same lattice as single transpositions, by telescoping. I withdraw my objection.

**R2.14 (A1.24, A1.26, A1.28) — ACCEPTED.**
- (3.4) recomputed (d2.py): n = 14 → 2, 15 → 1, 17 → 1, 30 → 3, 100 → 7, 400 → 18. Plot it only where it gives K ≥ 2, and say that for odd n with small R_q it is vacuous.

### Second pass: parts not yet scrutinised

**R2.15 (App B, proof of Lemma 3.12(1)) — correct.**
- I checked the construction by code for m = 2, 4, 6, 8, 10 and m = 7, 9, 11, 13, 15 (d2.py): permutation, all rows and columns sum to M(n), rows r and m+r complementary.
- By hand: the β_r gaps (6 = three dominoes) and the tail length 2m² − 12m + 6 ≥ 0 iff m ≥ 7 (odd).
- Readability: for odd m "domino" means any two consecutive indices, not {2t, 2t+1}. Say so.
- State explicitly that n = 6, 10 are not covered. This is irrelevant for (b) but a reader will ask.

**R2.16 (App C, joint moments and Möbius coefficients) — correct.**
- E[z_a²z_bz_c] = (2p₄ − p₂²)/(N)₃ and E[z_az_bz_cz_d] = (3p₂² − 6p₄)/(N)₄ check from p₁ = 0.
- c(12|34) = m₂₂ − 2m₂₁₁ + m₁₁₁₁ checks, using μ = −1 on the two intermediate partitions.
- c(1234) = m₄ − 4m₃₁ − 3m₂₂ + 12m₂₁₁ − 6m₁₁₁₁ checks, using μ(π, 1̂) = (−1)^{b−1}(b−1)!.
- The h_c formulas for both energies check.

Readability problems:
- m_{22}, m_{211}, … are used but only m_π is defined. Say "m_λ = m_π for any π of block type λ".
- c(σ) clashes with c for cells.
- μ (Möbius) clashes with μ_r in Prop 3.13.

**R2.17 (Lemma 3.8, ℓ² bound).** The majorisation step needs Σγ_j = 0 = Σ_p n(N − (2p−1)n)/2 (equal totals) as well as the partial-sum inequalities. Both hold, but only the latter is stated. Add the clause. ‖v‖² = (n⁴/4)·n(n²−1)/3 = n⁵(n²−1)/12 checks.

**R2.18 (Remark 5.2) — correct.** The swap formula checks: lines containing both a and b cancel. The "λ = 2 iff same row or column and off both diagonals" claim also checks, since two cells of one row cannot lie on the same diagonal.

**R2.19 (§5.1, "the fraction of magic squares in L_n [tends] to 0").** det(Σ_U)^{1/2} ≍ n^{13} checks (Var U₁ ≍ n⁸, Var δ_D ≍ n⁵). But the conclusion about magic squares also needs an upper estimate for the number of magic squares relative to N!·n^{−13}, and the paper gives none. Either add the heuristic (2n further conditions, each costing a factor ≍ n^{−5/2}) or drop the clause.

**R2.20 (Thm 3.7(c) proof, after R2.1).** The "Upper bounds for 14 ≤ n ≤ 40" paragraph should say that n ≤ 17 is covered by hand. It should also say that for 18 ≤ n ≤ 40 the decisive test is the full family (3.1), not only p = 1 (cf. n = 26 in R2.2), and point to the certificate.

### Readability judgement (for a reader new to the paper)

**R2.21 Main line.** After A1.14 the introduction makes k\*(n) visible, but the paper is two papers joined by the orthogonality framing. Part 1 is k\*(n): §3.2–3.5 and Apps A, B, D. Part 2 is the random energies: §4 and App C. Neither part uses the other. I do not ask for a split, but §1 should say so plainly: "The two parts are independent; §3 can be read without §4–5 and conversely."

**R2.22 Misplaced material.** Prop 3.14 and Remark 3.15 (E_low = 0 iff magic for n = 3) sit between the permutation threshold and §3.7, where they interrupt the main line. They concern L₃ and belong in §5.1 next to |L₄|.

**R2.23 Unmotivated definition.** E_low (E₄) is never motivated. Why the degree-1 conditions plus the diagonals, and not degree 2, or the diagonals alone? **Q to advocate:** what is the reason? If the answer is "the smallest D₄-invariant set of linear conditions that contains the diagonal conditions and the first moments", say so in one sentence at Def 2.4. If there is no reason beyond its use as an example, present Prop 4.3 as the general tool, with E_full as the main application and E₄ as a second example.

**R2.24 Is any section unnecessary?**
- §3.7: agreed to cut (A1.24).
- §5.2 "Single swaps": Remark 5.2, the swap-gap census, Fig. 4 and the descent statistics are observations about local search that support no theorem. The only mathematical content is "no two magic squares differ by a transposition" and 2 ≤ g_min ≤ 6. I propose keeping Remark 5.2 (with those two facts) and the descent percentages in two sentences, and dropping Fig. 4 and the 70-values/432/420/28 census, or moving them to anc/README. **Q to advocate:** does anything later in the paper use them?

**R2.25 Notation load.** After the renames the paper still introduces many symbols:
- §2: W, W_R, W_C, W_D, Γ_D, ε_n, σ_n, d_N;
- §3: Λ_{n,k}, P_γ, μ_r, F_q, R_q, H;
- §4: T_φ, τ_k, C_n, Γ, A, h_c.

A short notation table at the end of §2 would help the reader more than any single rename.

### Questions for the advocate
- QB1 (R2.2): fix the n = 26 statement in the certificate description, and confirm that the shipped JSON records a violating (p, J) for every listed vector.
- QB2 (R2.23): motivation for E₄.
- QB3 (R2.24): is anything in §5.2 beyond Remark 5.2 used elsewhere?
- QB4 (R2.4): if cheap, give the (1,1) cell of Table 4 by a second method, e.g. tagging columns as well and splitting by column patterns.
- QB5 (R2.19): heuristic or deletion for "fraction of magic squares → 0".

## ADVOCATE — turn 2

New scratch checks are in `scratchpad/adv3/`:
- `b1.py` (exact LLL + full enumeration of the short vectors, with a violated instance of (3.1) for each);
- `b2.py` (a NumPy recount of Table 4 by a different tagging; 1008 s).

### Replies to reviewer turn 2

**A2.1 (R2.1) — AGREE.**
- Lemma 3.8 is cited for both inequalities: ‖γ‖₁ ≤ n⁴/4 at t = −1, and ‖γ‖₂² ≤ n⁵(n²−1)/12 in the Parseval step.
- Λ_{n,n−2} and Λ_{n,n−3} are presented together as one paragraph "*The lattices Λ_{n,n−2} and Λ_{n,n−3}*". The text is in Rev. 2 below.
- The following are deleted: the f(n)/(n ≥ 166) sentence, "18 ≤ n ≤ 400", and the last sentence of App A, "The same script checks the rank-2 lattices Λ_{n,n−3} for 14 ≤ n ≤ 400". The loop stays in `kstar_verify.py` as a sanity check and is mentioned only in the README.

**A2.2 (R2.2, QB1) — AGREE with the correction.** My statement "every one has max_j|γ_j| > n²(n−1)/2" was false at n = 26. `b1.py` reproduces the reviewer's finding: the pair with max entry 8398 < 8450 is excluded only at p = 2, J = {10, 15}, 8398 + 8398 = 16,796 > 16,224.

The full list (counts 2, 2, 6, 6, 6, 2, 2 for n = 20, 22, 24, 26, 34, 36, 38) has these minimal violating instances:
- p = 1 for every vector except the n = 26 pair (p = 2);
- one n = 38 vector also violates at p = 4, but it already violates at p = 1.

Requirements for the certificate:
- `anc/kstar_certificates.json` records, for each listed vector, the minimal p, the sign and the column set J.
- The checker recomputes Σ_{j∈J}γ_j against pn(N−pn)/2.
- It ships the reduced basis, since GS ratios are basis-dependent: my sympy LLL gives 1.385 at n = 35, the reviewer's gives 1.637.
- The reviewer's `d3.py` is shipped as `anc/kstar_enum_independent.py`, credited in the README.

**A2.3 (R2.3) — AGREE.**
- The display Π_{r<K}(H·binom(n, r+1)+1) ≤ (2H)^K n^{K(K+1)/2} is added.
- With K = ⌊2√n⌋ the log of the right side is 2n log n + O(√n log n), and the log of the left side is n log H = 3n log n − O(n).
- The text then says "K ≥ 2√n for all large n".
- Optional footnote: keeping log s! improves this to (√12 − o(1))√n, which matches the computed K/√n → 3.29 (A1.3).

**A2.4 (R2.4, QB4) — the (1,1) cell is now independently confirmed.**
- `b2.py` counts N(i, j) = #{S ∈ L₄ : row i and column j sum to 34}. It uses the top/bottom split and adds the partial sum of column j to the matching key.
- D₄ reduces the 16 values to N(0,0) = 56,276, N(0,1) = N(1,0) = 34,944 (equal, as transposition requires) and N(1,1) = 27,996.
- Since the row and column counts take only the values 0, 1, 4: Σ_{i,j}N(i,j) = 616,640 = a₁₁ + 2·4·9,336 + 16·7,040, so a₁₁ = **429,312**, as printed.
- The same run gives |L₄| = 14,639,440 and Σ_i #{row i = 34} = 3,079,888 = 2,611,472 + 4·117,104.

Together with R2.4 every entry of Table 4 is now recounted by code independent of `lowmode_enum.c`. Proposed sentence for the proof of Prop 5.1: "All entries of Table 4 were recounted by two further programs (anc/lowmode_recount.py, anc/table4_recount.py) written independently of anc/lowmode_enum.c."

**A2.5 (R2.5) — AGREE.** The phrase "swap-local minimum" is dropped. Wording: "a local minimum with respect to transpositions (no transposition lowers the energy)".

**A2.6 (R2.6) — AGREE; an author action.**
- After Rev. 18, only condition (14) of Hoeffding's Thm 4 is quoted. The author (commit 34a69aa, "as printed") checks that display against the printed page and adds the page number to the citation, \cite[Thm.~4, p.~…]{hoeffding1951}.
- Related correction found while drafting: the proof of Cor 4.5 says "Hoeffding's Theorem 3 … gives asymptotic normality". Once (11)–(12) are removed, it must cite **Theorem 4** (product arrays) for consistency.

**A2.7–A2.9 (R2.7–R2.9)** — Noted; nothing further.

**A2.10 (R2.10) — AGREE: drop the empirical Cov/Var altogether.** Consequences:
- Lemma 2.2 becomes: "x̄ = ȳ = z̄ = 0; ‖x‖² = ‖y‖² = (n²−1)/12, ‖z‖² = (N²−1)/12, ⟨x, y⟩ = 0; ⟨𝟙_L, z⟩ = δ_L/N." Fig 1(c) already uses ‖z‖² = 21.25 with this normalisation, so it is consistent.
- Def 2.4 becomes E_full = Σ_L⟨𝟙_L, z⟩² and E₄ = ⟨x, z⟩² + ⟨y, z⟩² + ⟨𝟙_{D_m}, z⟩² + ⟨𝟙_{D_a}, z⟩².
- In §4, T_φ = ⟨φ, z⟩ and E[T_φT_ψ] = σ_n²⟨φ̃, ψ̃⟩ with φ̃ = φ − φ̄𝟙; σ_n² = ‖z‖²/(N−1).
- Def 3.1 then reads ⟨x^m, z⟩ = ⟨y^m, z⟩ = 0. Cor 3.5 reads I(S) = N⟨x² + y², z⟩ + n²(n⁴−1)/12.

The symbol inventory is Rev. 13 below. For Prop 3.14 I avoid all clashes by using primes instead of new letters (details in Rev. 13).

**A2.11 (R2.11) — AGREE (i), (ii); CLARIFY (iii).** The split is not quite "hand vs computer" as the reviewer states it:
- Every lower bound needs a witness arrangement. For 5 ≤ n ≤ 40 these were found by computer but are checkable in exact arithmetic.
- The upper bounds k\* ≤ n−1 (Vandermonde), k\* ≤ n−2 for n ≥ 14 and k\* ≤ n−3 for n ≥ 18 are proved by hand.
- Only the upper bounds k\*(n) ≤ (Table 1 value) for 18 ≤ n ≤ 40 are computer-assisted.

Abstract sentence: "Explicit arrangements (witnesses) together with short proofs give k\*(n) = n−1 for 3 ≤ n ≤ 13 and k\*(n) = n−2 for 14 ≤ n ≤ 17, and we prove k\*(n) ≤ n−3 for all n ≥ 18; with computer assistance we determine k\*(n) for all n ≤ 40." For the moments, (i) becomes: "Σ_{ij} s_{ij} j^m = M(n) Σ_j j^m and Σ_{ij} s_{ij} i^m = M(n) Σ_i i^m".

**A2.12 (R2.12) — AGREE.**
- R_q = min(2q+1, 2(Q−q), Q−2), and min(q+1, Q−q) ≤ (Q+1)/2 ≤ Q−2 iff Q ≥ 5.
- Use "once Q ≥ 5 (n ≥ 13)".

**A2.13, A2.14 (R2.13, R2.14) — AGREE.** Fig 3 plots the bound from (3.4) only at the n where it gives K ≥ 2. Caption addition: "for odd n with small R_q, (3.4) gives only the trivial bound".

**A2.15 (R2.15) — AGREE.**
- In App B, after "domino": "(for odd m, any two consecutive unused indices; they need not be of the form {2t, 2t+1})".
- After Lemma 3.12: "Part (1) does not cover n = 6, 10; this is irrelevant for Theorem 3.7(b), which concerns large n, and every n ≥ 14 is covered."

**A2.16 (R2.16) — AGREE.**
- Add "m_λ = m_π for any π of block type λ (e.g. m_{211} for 12|3|4)".
- Rename the App C partitions π, σ to ν, ν′. The letter π is also the random permutation.
- The coefficient c(σ) becomes θ(ν′).
- Möbius μ(ν, ν′) stays, and the Prop 3.13 moments μ_r(g) become B_r(g) ("binomial moments").

**A2.17 (R2.17) — AGREE.** Proof of Lemma 3.8 becomes: "…is majorised by the vector v with entries v_p = n(N−(2p−1)n)/2, 1 ≤ p ≤ n (equal totals: Σ_p v_p = 0 = Σ_j γ_j, and (3.1) bounds the partial sums of γ sorted in decreasing order)…".

**A2.18 (R2.18) — Noted; nothing further.**

**A2.19 (R2.19, QB5) — AGREE: keep it, as an explicitly labelled heuristic.** The supporting estimate:
- Of the 2n+2 line conditions, 2n+1 are independent.
- Each deviation has variance nVar(Z)(N−n)/(N−1) ≍ n⁵/12.
- The same Gaussian heuristic therefore predicts #magic/N! = exp(−5n log n + O(n)), against |L_n|/N! ≍ n^{−13}.

Replacement for the last sentence of §5.1: "Since det(Σ_U)^{1/2} grows like n^{13}, the heuristic suggests |L_n|/N! ≍ n^{−13}. The same heuristic applied to the 2n+1 independent line conditions suggests that magic squares form a fraction exp(−5n log n + O(n)) of all arrangements, so that their proportion in L_n tends to 0. Neither statement is proved here; local limit theorems … [kuperberg2017probabilistic, eberhard2019additive] …".

**A2.20 (R2.20) — AGREE.** The text is Rev. 3 below.

**A2.21 (R2.21) — AGREE.** Add to §1 Organisation: "The two parts are independent: §3 (the permutation threshold, with Appendices A, B, D) can be read without §4–5 (random arrangements, Appendix C) and conversely; they share only the notation of §2."

**A2.22 (R2.22) — AGREE.** Move Prop 3.14 and Remark 3.15 into §5.1, retitled "The classes L₃ and L₄". This also merges the n = 4 example (R1.22): Remark 2.5 forward-references §5.1.

**A2.23 (R2.23, QB2) — CLARIFY: the history, and the honest mathematical reason.**
- Historically E₄ comes from the geometric picture of the companion paper. It requires the centroid of the points (x, y, z) to lie on the vertical axis (the degree-1 conditions) and requires the two diagonals; the earlier versions used it as the "low-mode" energy.
- There is no minimality theorem behind it. For example, span{x² + y² − mean} is a one-dimensional D₄-invariant space, so "smallest D₄-invariant set" would be false.
- The reason that survives is this. E₄ is obtained from E_full by keeping the two diagonal conditions and replacing the 2n−2 independent row and column conditions by their degree-1 moments (Prop 3.3). It is D₄-invariant, has a fixed number of terms, and so is the case to which Cor 4.5 applies; E_full, whose number of terms grows, is not.

So I accept the reviewer's second option. Prop 4.3 is presented as the general tool, E_full as the main application, and E₄ as the fixed-size example with a limit law and with the exact count of §5.1. Proposed sentence at Def 2.4: "E₄ keeps the diagonal conditions and replaces the 2n−2 independent row and column conditions by the two degree-1 moment conditions (Prop 3.3); it is D₄-invariant and has a fixed number of terms, which makes it the natural test case for a limit law (Corollary 4.5)."

**A2.24 (R2.24, QB3) — AGREE; nothing in §5.2 beyond Remark 5.2 is used elsewhere.** I checked: the only cross-reference is §1 "Classical and new material", to Remark 5.2 itself. Paper A does not use §5.2 either. The changes:
- Keep Remark 5.2: the swap formula, the range of λ, "no two magic squares differ by a transposition", and 2 ≤ g_min ≤ 6.
- Keep one sentence on the n = 3 local minima with the corrected definition (A1.7/A2.5). It is the only place where the difference between E₄ and E_full under local search is quantified.
- Keep one sentence on the descent percentages (A1.5 wording).
- Delete Fig 4, the "70 values from 2 to 980" census and the 432/420/28 split. They move to anc/README with `verify_numbers.py` as the source.

**A2.25 (R2.25) — AGREE.** The notation table is Rev. 13 below.

**Additional point found while drafting (A2.26).** Paper A (introduction, l. 45) calls z the "height function" ("orthogonality conditions on the height function"). Paper B §2.1 explicitly says "we do not call it a height function". The two papers must agree. I propose that paper A's sentence say "on the centred entries". This is outside paper B's files and is flagged for the consolidation round.

### Draft agreed revision list

Abbreviations: Thm/Prop/Lem numbers follow the current paperB.pdf.

**Errors, gaps and proofs**
1. **Thm 3.7(c), §3.5, "n ≥ 14: level n−2" and "n ≥ 18: level n−3".** Merge the two into the paragraph *"The lattices Λ_{n,n−2} and Λ_{n,n−3}"*.
   - Keep the n−2 argument with "γ = cv, c ∈ ℤ".
   - Replace the n−3 text by: "Λ_{n,n−3} has rank 2: P_γ = (t−1)^{n−2}(a+bt), a, b ∈ ℤ. At t = −1, 2^{n−2}|a−b| = |P_γ(−1)| ≤ ‖γ‖₁ ≤ n⁴/4 (Lemma 3.8); since n⁴ < 2ⁿ for n ≥ 17, a = b and P_γ = a(t−1)^{n−2}(t+1). By Parseval, ‖γ‖₂² = a²·Σ_j(binom(n−2, j) − binom(n−2, j−1))² = 2a²C_{n−2}, with C_m = binom(2m, m)/(m+1) the Catalan number. Since 2C_16 = 70,715,340 > 50,860,872 = 18⁵(18²−1)/12, and from n to n+1 the left side grows by 2(2n−3)/n ≥ 11/3 while the right side grows by less than 3/2, Lemma 3.8 (‖γ‖₂² ≤ n⁵(n²−1)/12) forces a = 0. Hence k\*(n) ≤ n−3 for n ≥ 18."
   - Delete the f(n) sentence and "18 ≤ n ≤ 400", and the matching sentence in App A.
2. **§3.2 after Thm 3.7.** "Part (a) improves on k\*(n) ≤ n−3 only for n ≥ 166" → "Part (a) gives k\*(n) ≤ n−3 from n = 166 on and improves on it from n = 169; for smaller n, part (c) is much stronger." "Parts (c) for n ≥ 14 … rest on exact computer calculations" → "In part (c), the lower bounds rest on explicit witness arrangements, the bounds k\* ≤ n−2 (n ≥ 14) and k\* ≤ n−3 (n ≥ 18) are proved by hand, and only the upper bounds for 18 ≤ n ≤ 40 in Table 1 are computer-assisted."
3. **Proof of Thm 3.7(c), "Upper bounds for 14 ≤ n ≤ 40".** Replace with: "*Upper bounds for 18 ≤ n ≤ 40.* (For n ≤ 17 they were proved above.) If no nonzero vector of Λ_{n,k} satisfies (3.1) for every p, then k\*(n) ≤ k. By Lemma 3.8 only the vectors with ‖γ‖₂² ≤ n⁵(n²−1)/12 need to be examined. We enumerated them exactly with two independent implementations (App A). At k = k\*(n) the ball contains no nonzero vector for 16 of the 23 values of n, the Gram–Schmidt norms of the reduced basis already exceeding the radius, and 2–6 vectors for n = 20, 22, 24, 26, 34, 36, 38. Each of these violates (3.1), in all but one case with p = 1; the exception is n = 26, which needs p = 2. The certificate anc/kstar_certificates.json lists the bases and, for each vector, a violated instance (p, J)." (Count: 23 values 18–40, of which 7 have vectors in the ball.)
4. **Table 1 caption.** Last sentence → "The upper bounds for 18 ≤ n ≤ 40 were computed by two independent exact lattice enumerations (anc/kstar_verify.py, anc/kstar_enum_independent.py) and, for n ≤ 33, also by integer programming (anc/kstar_crosscheck/); a certificate is in anc/kstar_certificates.json."
5. **§3.3 last paragraph, √n remark.** Replace with the A1.3 text, using H = ⌊n³/4⌋ and binomial moments B_r. Add the display (H+1)ⁿ ≥ H^n > (2H)^K n^{K(K+1)/2} ≥ Π_{r<K}(H·binom(n, r+1)+1) for K = ⌊2√n⌋ and n large, and conclude "K ≥ 2√n for all large n".
6. **§6 item 1.** Use the A1.3 replacement: for vectors with ‖γ‖₁ ≤ n⁴/4 the pigeonhole principle gives order ≍ √n. Whether √(n log n) is attained in this class is open, and is separate from realisability. In §3.4 use the analogy wording of A1.3.
7. **Lemma 3.8 proof.** Add the equal-totals clause (A2.17).
8. **§3.2, Λ_{n,k} display.** Add "(the quotient of an integer polynomial by the monic (t−1)^{k+1} has integer coefficients)".
9. **Lemma 3.9 proof.** Use the Mahler-measure wording of A1.17, and note that roots at 0 are allowed.
10. **Proof of Thm 3.7(b).** Right side: insert Σ_{s≤k} log s! ≥ (k²/2) log k − (3/4)k² − k/2 (A1.16). Left side, odd n: use the A1.15 text with "once Q ≥ 5".
11. **Prop 3.13.** Add the derivation of R_q from Lemma 3.12(2) (A1.15).

**Random arrangements**
12. **Cor 4.2.** "for every distribution … invariant under relabelling of the values" → "for every random arrangement with E z_c = 0 for every cell (for instance any distribution invariant under complementation s ↦ N+1−s); magic and semi-magic squares take this value exactly."
13. **§4.1, "The means … coincide iff (n²−1)/6 = 2(n−1)/n".** Replace with the A1.20 text, which ends in n(n+1) = 12.
14. **Thm 4.3 → Proposition 4.3 (Mantel 1967, Hubert 1987; specialised).** Abstract and §1: "we specialise the classical variance formula for quadratic assignment statistics …". Thm 4.4 keeps Theorem status.
15. **Remark 4.6.** Replace "the deficit comes from the two negative terms" by the A1.11 decomposition. Rename "Gaussian approximation/sd" to "χ²-mixture approximation/sd" in Remark 4.6, Table 3 and Fig 2.
16. **Proof of Cor 4.5.**
    - "‖a‖₂² is proportional to αᵀC_nα" → "‖a_ℓ‖₂/τ_ℓ = (σ_n√N)⁻¹ for every ℓ, so ‖a‖₂² = αᵀC_nα/(Nσ_n²)".
    - τ₃²/τ₁² = 12/(n²(n+1)).
    - Cite Hoeffding **Thm 4** with condition (14), not Thm 3.
17. **After Prop 4.1.** Add "The means are elementary (sampling without replacement)". In the §1 novelty sentence, change "closed forms of Theorem 4.4" to "closed forms for the variances in Theorem 4.4".
18. **§2.3 Hoeffding paragraph.** Keep only the product-array criterion (condition (14) of Thm 4) and drop (2.4)–(2.5). The author checks it against the printed page and adds the page number (A2.6).

**Computations (§5)**
19. **§5.1 retitled "The classes L₃ and L₄".**
    - Move Prop 3.14 and Remark 3.15 here, with the renamed variables of Rev. 31.
    - Remark 2.5 gives γ = (3, −9, 9, −3), ρ = (−6, 4, 10, −8) and points here.
20. **Prop 5.1 proof.** Add: "Two further programs written independently of anc/lowmode_enum.c (anc/lowmode_recount.py, anc/table4_recount.py) reproduce |L₄|, the first-moment count 6,697,177,424 and every entry of Table 4."
21. **§5.1 local-limit paragraph.**
    - Use the A1.21 lattice sentence.
    - Replace the last sentence with the labelled heuristic of A2.19.
22. **§5.2.**
    - Keep Remark 5.2. Rewrite "a diagonal separates a, b" as "exactly one of a, b lies on that diagonal" and "gap" as "increase of N²E_full".
    - Local-minimum sentence: "Call S a local minimum with respect to transpositions if no transposition lowers the energy. For n = 3 such minima of E_full are the eight magic squares and eight non-magic arrangements with N²E_full = 2, all strict; E₄ has 344, of which 336 are non-magic, and only 72 (64 non-magic) are strict."
    - Descent sentence: the A1.5 text (tie-break, stopping rule, 2×10⁵ runs, ±0.1 %).
    - Delete Fig 4, the 70-value census and 432/420/28; move them to anc/README.

**Structure, framing, abstract**
23. **Abstract.** The A1.14 text with the edits of A2.11:
    - "M(n) Σ_j j^m" form of the moments;
    - "3 ≤ n ≤ 13";
    - the witness / hand / computer split;
    - "pigeonhole principle";
    - "we specialise … quadratic assignment statistics".
24. **§1.**
    - Define in words "test function", "degree-k conditions" and "witness".
    - Add the independence sentence (A2.21).
    - Organisation paragraph: drop "moment hierarchy".
25. **§3.7 "Balance of the signed mass".**
    - Delete it. Keep the Cauchy–Schwarz / ‖π_Wz‖² bound as Remark 2.6, "Linear functionals and E_full".
    - Keep the ring value as one sentence (A1.24).
    - Delete §6 item 3.
26. **§3.5, "We observe (for these n only …)".** Replace with the A1.27 text, and §6 item 1 accordingly.
27. **Fig 3.** Plot the bound (3.4) where it gives K ≥ 2. Caption as in A1.28 plus A2.13.
28. **Def 2.4.** Add the E₄ motivation sentence (A2.23) and the Pinn–Wieczerkowski normalisation clause (A1.12, "energy" row).
29. **Title (author's choice).** "Moments of line sums of magic squares: a permutation threshold and random line-sum energies".

**Jargon and notation**
30. **Terms** (A1.12):
    - "centred value function" → "centred entries z";
    - E_low → E₄, "low-order class" → "the class L_n";
    - "moment hierarchy" → "moment conditions" (Prop 3.3 title, §3 title);
    - "twins / twin rows / twin swaps / twin-row exchange" → "complementary on J / complementary rows / Swaps in complementary rows / exchange in the complementary row";
    - "box principle" → "pigeonhole principle" (Prop 3.13 title "Pigeonhole criterion");
    - "Column feasibility" → "Majorisation bound for column deviations"; "column-feasibility inequalities" → "the inequalities (3.1)";
    - "level k" → "the lattice Λ_{n,k}" everywhere, including App A;
    - "product of inertia" only once, in parentheses;
    - "separable" → "of the form a(x) + b(y)";
    - "Siamese (de la Loubère) square [andrews1960magic]".
31. **Symbol inventory and renames** (A1.13, A2.10, A2.16). Each symbol then has one meaning:
    - Empirical covariance: drop Cov/Var over cells; use ⟨·,·⟩ (normalised by 1/N) and ‖·‖. Cov, Var and E are always probabilistic.
    - Value index: v (b_v = v − (N+1)/2). Test-function index in §4: ℓ (φ_ℓ, a_ℓ, T_ℓ, τ_ℓ, α_ℓ).
    - Prop 3.14 (moved to §5.1):
      - γ = (ξ, −2ξ, ξ), ρ = (η, −2η, η), and centre e = −2κ;
      - a′ = a − κ, c′ = c − κ, ξ′ = ξ − κ, η′ = η − κ, with ξ′ + η′ = κ;
      - identity Σz² = 2(4κ² + 3(a′² + c′²) + ξ′² + η′²) = 60;
      - the auxiliary R is not named ("4κ² + ξ′² + η′² is a multiple of 3 and at most 15");
      - update the labels in `n3_lowmode_proof.py`.
    - Proof of 3.7(c): γ = cv. Prop 3.13: binomial moments B_r(g), and r_q in place of R_q.
    - Variance polynomials: F_o, F_e, G_o, G_e. Projection: π_W. App B sets: 𝒫, 𝒬. App B weight index: ι. Half-order: n = 2h (Lemma 3.12, App B).
    - App C: partitions ν, ν′; coefficients θ(ν′); m_λ defined for block types.
    - Normal law: 𝒩(0, 1).
32. **Notation table at the end of §2.** Two columns, symbol and meaning plus where defined, covering:
    - n, N, M(n), c = (i, j), s, z, x, y, δ_L, ρ, γ, ⟨·,·⟩;
    - W, W_R, W_C, W_D, Γ_D, ε_n, π_W;
    - E_full, E₄, σ_n;
    - Λ_{n,k}, P_γ, k\*(n), B_r, F_q, r_q, H;
    - T_φ, τ_ℓ, C_n, Γ, A, h_c;
    - L_n, U₁–U₄, Σ_U.
33. **Remark 3.4.** Change "product of inertia" to "mixed moment"; see Rev. 30.

**Ancillary files**
34. Ship the following:
    - `anc/kstar_certificates.json` plus a ≤ 40-line checker (A1.2, A2.2);
    - `anc/kstar_enum_independent.py` (reviewer's d3.py);
    - `anc/lowmode_recount.py` (reviewer's c9/d6/d7);
    - `anc/table4_recount.py` (advocate's b2.py).
    
    Update the README, including the moved swap census and the n ≥ 18 rank-2 sanity loop.

**Cross-paper (for consolidation)**
35. Paper A introduction l. 45: "orthogonality conditions on the height function" → "on the centred entries", matching paper B §2.1 (A2.26).

### Points still open or not fully agreed
- **D1 (R2.6):** the Hoeffding page check is an author action. It is not resolvable by either of us without the printed paper.
- **D2 (R1.26 / Rev. 29):** the title is the author's decision. Both sides recommend the change.
- **D3 (A2.24):** I keep the n = 3 local-minimum sentence in §5.2. The reviewer proposed keeping only Remark 5.2 and the descent statistics; the reviewer should confirm whether this one sentence may stay.
- **D4 (A2.23):** the E₄ motivation is offered as "fixed-size D₄-invariant truncation" without a minimality claim. The reviewer should confirm that this is sufficient.

## REVIEWER — turn 3

Scratch check for this turn: `scratchpad/dialogue/e1.py` (exact arithmetic, plus a NumPy rank computation). I re-read the draft list against the .tex sources, not only against the dialogue.

### Settling the advocate's turn-2 replies

**R3.1 (A2.1, Rev. 1) — ACCEPTED, with two corrections to the wording.**
- The growth ratios are right. For n ≥ 18 the left ratio is 2(2n−3)/n ≥ 11/3, with equality at n = 18. The right ratio is (n+1)⁴(n+2)/(n⁴(n−1)), which is 1.4605 at n = 18 and decreasing. I checked both for 18 ≤ n < 60 (e1.py).
- Notation clash: Rev. 1 names the Catalan number C_m, but §4 (proof of Cor 4.5) already uses C_n for the correlation matrix. Do not name it. Write 2a²·binom(2n−4, n−2)/(n−1) ("twice a Catalan number").
- The multiplier "γ = cv" (Rev. 31) clashes with cells c. Use a in both rank-1 and rank-2 cases: P_γ = a(t−1)^{n−1}, and P_γ = (t−1)^{n−2}(a+bt).

**R3.2 (A2.2, Rev. 3/4) — ACCEPTED.** The count "16 of the 23 values" checks: 18–40 is 23 values, and 7 of them have vectors in the ball. The current Table 1 caption (theory.tex l. 275) still says "for 34 ≤ n ≤ 40 they rest on the lattice enumeration alone". This must be replaced, as Rev. 4 does.

**R3.3 (A2.19, Rev. 21) — ERROR in the advocate's heuristic.** The draft says "Of the 2n+2 line conditions, 2n+1 are independent." This is false. Σ_iρ_i = Σ_jγ_j = Σ_c z_c = 0, so there are two dependencies, and the centred line indicators span W, which has dim W = 2n. The paper says so itself (background.tex l. 52, "W … has dimension 2n"), and I confirmed rank 2n for n = 3..8 (e1.py). The conclusion exp(−5n log n + O(n)) is unaffected. Write "the 2n independent line conditions".

**R3.4 (A2.10, Rev. 31, P_W → π_W) — REJECT this one rename.** π is the uniformly random permutation (background.tex l. 103, z_c = b_{π(c)}), and A2.16 renames the App C partitions precisely to free π. Keep P_W. P_γ (a polynomial indexed by a vector) and P_W (a projection indexed by a subspace) are distinguishable once P_o, P_e, the Prop 3.14 P and the App B set P are renamed.

**R3.5 (A2.16, Rev. 31, index ℓ) — minor.** ℓ is already used for "two lines meeting in ℓ cells" (random.tex l. 34) and for the row parameter of Lemma 3.12(2). The parts are independent, so ℓ as the test-function index in §4 is acceptable, but random.tex l. 34 must then say "in r cells" or similar. I would not claim "each symbol has one meaning"; claim "no symbol has two meanings within one section".

**R3.6 (A2.15) — the draft list omitted it.** It is added as F12.

**R3.7 (new, overclaim).** Cor 4.2 is titled "Null distribution of Loly's invariant" (random.tex l. 41), and the abstract (l. 9), §1 (l. 38) and the advocate's proposed abstract all say "the null distribution". The corollary gives only the mean and the variance. The distribution is computed only numerically, for n = 3, 4. Retitle it "Mean and variance of Loly's invariant" and say "mean and variance" in the abstract and §1. Added as F14.

**R3.8 (new, framing).** Fig 3 (caption, theory.tex l. 282) and l. 291 ("k\*(50) ≤ 30, k\*(80) ≤ 39, k\*(100) ≤ 45") present upper bounds for 41 ≤ n ≤ 100. They come from the descending scan, for which no certificate and no second implementation exist. They should be labelled "computer-assisted, not independently checked", and after Rev. 1 the caption should not suggest that these bounds are needed for n ≥ 18. Added to F29.

**R3.9 (A2.11) — ACCEPTED.** The split "lower bounds via witnesses / hand-proved upper bounds / computer-assisted upper bounds for 18–40" is correct and better than mine.

**R3.10 (A2.23, D4) — SETTLED: sufficient.** "No minimality claim" is the honest position. The sentence must not say "natural"; write "which makes it a test case for a limit law".

**R3.11 (A2.24, D3) — SETTLED: the n = 3 local-minimum sentence stays.** It is the corrected fact of R1.7, and it is the only quantitative comparison of E₄ and E_full under local search. Fig 4 and the census go to anc/README.

**R3.12 (A2.6, D1) — remains an author action** (see Unresolved).

**R3.13 (Rev. 13) — re-verified.** The means of the X, Y part and of the 2n row/column part, divided by (n−1)(n²+1)/6, are (n+1)/12 and 1/n (e1.py, n = 3..7). They agree only at n = 3. Note that the current sentence (random.tex l. 39) has "(n²−1)/6 = 2(n−1)/n", which is equivalent after dividing by (n−1)/6 but unmotivated; replace it as in F15.

**R3.14 (Rev. 1/Rev. 2 interplay).** After Rev. 1, the abstract's "k\*(n) ≤ n−3 for every n ≥ 18" is a hand proof. Thm 3.7(a) is then only of asymptotic interest. Say so in one clause after Thm 3.7 (F2).

### Final agreed revision list

Numbering follows the current paperB.pdf. "Rev. k" of the advocate's draft maps to F-numbers as follows: F1 = Rev. 1, …, F11 = Rev. 11; F12 is new; Rev. 12–29 → F13, F15–F31; F14 is new; Rev. 30–35 → F32–F37 (Rev. 33 merged into F32).

**F1** (gap-in-proof; §3.5 proof of Thm 3.7(c), paragraphs "n ≥ 14: level n−2" and "n ≥ 18: level n−3"; App A last sentence)
- Merge the two paragraphs into one, titled "*The lattices Λ_{n,n−2} and Λ_{n,n−3}*".
- Rank 1 case: keep the existing argument, writing γ = a·v with a ∈ ℤ.
- Rank 2 case: replace the text by:
  > "Λ_{n,n−3} has rank 2: P_γ = (t−1)^{n−2}(a+bt) with a, b ∈ ℤ. At t = −1, 2^{n−2}|a−b| = |P_γ(−1)| ≤ ‖γ‖₁ ≤ n⁴/4 by Lemma 3.8; since n⁴ < 2ⁿ for n ≥ 17, a = b and P_γ = a(t−1)^{n−2}(t+1). By Parseval, ‖γ‖₂² = a²Σ_j(binom(n−2,j) − binom(n−2,j−1))² = 2a²·binom(2n−4,n−2)/(n−1) (twice a Catalan number). At n = 18 this factor is 70,715,340 > 50,860,872 = 18⁵(18²−1)/12. From n to n+1 the left side grows by 2(2n−3)/n ≥ 11/3 and the right side by (n+1)⁴(n+2)/(n⁴(n−1)) < 3/2. So for n ≥ 18 the bound ‖γ‖₂² ≤ n⁵(n²−1)/12 of Lemma 3.8 forces a = 0, and k\*(n) ≤ n−3."
- Delete the f(n)/"n ≥ 166" sentence and "18 ≤ n ≤ 400" from the proof.
- Delete App A's sentence "The same script checks the rank-2 lattices Λ_{n,n−3} for 14 ≤ n ≤ 400".

**F2** (overclaim; §3.2, paragraph after Thm 3.7)
- Replace "Part (a) improves on k\*(n) ≤ n−3 only for n ≥ 166" by "Part (a) gives k\*(n) ≤ n−3 from n = 166 on and improves on it from n = 169; it is of asymptotic interest only, since part (c) gives k\*(n) ≤ n−3 for all n ≥ 18."
- Replace the sentence saying part (c) rests on computer calculations by "In part (c) the lower bounds rest on explicit witness arrangements, checkable in exact arithmetic; k\* ≤ n−1, k\* ≤ n−2 (n ≥ 14) and k\* ≤ n−3 (n ≥ 18) are proved by hand; only the upper bounds of Table 1 for 18 ≤ n ≤ 40 are computer-assisted."

**F3** (gap-in-proof; proof of Thm 3.7(c), paragraph "Upper bounds for 14 ≤ n ≤ 40")
Retitle the paragraph "Upper bounds for 18 ≤ n ≤ 40" and replace its text by:
> "(For n ≤ 17 they were proved above.) If no nonzero vector of Λ_{n,k} satisfies (3.1) for every p, then k\*(n) ≤ k. By Lemma 3.8 only vectors with ‖γ‖₂² ≤ n⁵(n²−1)/12 need be examined; we enumerated them exactly with two independent implementations (App A). At k = k\*(n) the ball contains no nonzero vector for 16 of the 23 values of n, since the Gram–Schmidt norms of the reduced basis already exceed the radius. For n = 20, 22, 24, 26, 34, 36, 38 it contains 2, 2, 6, 6, 6, 2, 2 vectors. Each violates (3.1), in every case but one already with p = 1; the exception is n = 26, which needs p = 2. The certificate anc/kstar_certificates.json lists the reduced bases and, for each vector, a violated instance (p, J)."

**F4** (gap-in-proof; Table 1 caption, theory.tex l. 275)
Replace the sentence from "The upper bounds come from …" to the end with:
> "The upper bounds for 18 ≤ n ≤ 40 were computed by two independent exact lattice enumerations (anc/kstar_verify.py, anc/kstar_enum_independent.py) and, for n ≤ 33, also by integer programming (anc/kstar_crosscheck/); a certificate is in anc/kstar_certificates.json."

**F5** (gap-in-proof; §3.3, last paragraph, the "box principle … K ≍ √n" sentence)
Replace it by:
> "The hypothesis ‖γ‖₁ ≤ n⁴/4 alone cannot give an upper bound of smaller order than √n. Let H = ⌊n³/4⌋. The (H+1)ⁿ vectors g ∈ {0,…,H}ⁿ have binomial moments B_r(g) = Σ_j binom(j,r)g_j ∈ [0, H·binom(n,r+1)]. If (H+1)ⁿ > Π_{r<K}(H·binom(n,r+1)+1), two of them, g ≠ g′, share B_0, …, B_{K−1}; then γ = g − g′ ≠ 0, ‖γ‖₁ ≤ nH ≤ n⁴/4, and (t−1)^K | P_γ. Since Π_{r<K}(H·binom(n,r+1)+1) ≤ (2H)^K n^{K(K+1)/2}, taking K = ⌊2√n⌋ the logarithm of the right side is 2n log n + O(√n log n), while that of the left side is ≥ n log H = 3n log n − O(n). So such K ≥ 2√n exist for all large n."
- Optional footnote: a sharper count gives (√12 − o(1))√n.

**F6** (overclaim; §6 item 1 and the analogy sentence in §3.4)
- §6 item 1 becomes:
  > "The upper bound uses only that γ is a nonzero integer vector with ‖γ‖₁ ≤ n⁴/4. In that class the pigeonhole principle produces vectors vanishing to order ≥ 2√n at 1 (§3.3), so a bound of smaller order than √n needs more information about γ. Whether the order √(n log n) of Lemma 3.9 is attained within this class is, as far as we know, open; this is separate from realisability, i.e. which such vectors are column deviations of arrangements."
- §3.4 analogy becomes: "In both settings the upper bound comes from Jensen's formula and the lower construction from the pigeonhole principle, and they differ by a factor √(log n)."
- Do not assert sharpness.

**F7** (gap-in-proof; proof of Lemma 3.8)
Write "… is majorised by the vector v with v_p = n(N − (2p−1)n)/2, 1 ≤ p ≤ n (equal totals, Σ_p v_p = 0 = Σ_j γ_j, and (3.1) bounds the partial sums of γ sorted in decreasing order) …".

**F8** (gap-in-proof; §3.2, display Λ_{n,k} = (t−1)^{k+1}ℤ[t]_{<n−k−1})
Append "(the quotient of an integer polynomial by the monic polynomial (t−1)^{k+1} has integer coefficients), a lattice of rank n−k−1".

**F9** (clarity; proof of Lemma 3.9, theory.tex l. 139)
Replace the Jensen sentence by:
> "The Mahler measure M(P) = |a|Π_α max(1,|α|) of a nonzero P ∈ ℤ[t] is at least 1, because |a| ≥ 1, and Jensen's formula gives log M(P) = ∫ log|P(e^{2πiθ})| dθ. A root at 0 (γ₀ = 0) contributes max(1,0) = 1 and is allowed."

**F10** (gap-in-proof; proof of Thm 3.7(b))
- Right side: insert the display Σ_{s≤k} log s! ≥ (k²/2)log k − (3/4)k² − k/2, which follows from log s! ≥ s log s − s and Σ_{s≤k} s log s ≥ ∫₀^k x log x dx. Hence Σ_{s≤k}(s log n − log s!) ≤ (k²/2)log(n/k) + O(k² + k log n).
- Left side, odd n: replace the compressed sentence by:
  > "With Q = (n−3)/2, r_q = min(2q+1, 2(Q−q), Q−2) ≥ min(q+1, Q−q) once Q ≥ 5 (n ≥ 13), so ⌈r_q/2⌉+1 ≥ min(q+1, Q−q)/2. Hence log(left side) ≥ Σ_{q<Q} log min(q+1, Q−q) − Q log 2 ≥ 2 log(⌊Q/2⌋!) − Q log 2 = (n/2)log n − O(n)."

**F11** (clarity; Prop 3.13, after the definition of R_q (renamed r_q))
Add:
> "For odd n the q-th pair consists of the columns 2q+1, 2q+2, and the complementary rows ℓ, n−1−ℓ of Lemma 3.12(2) cover both columns if and only if ℓ ≤ 2q and ℓ ≤ n−4−2q; with 0 ≤ ℓ ≤ (n−9)/2 this gives the formula for r_q."

**F12** (clarity; App B proof of Lemma 3.12(1), and after Lemma 3.12)
- After the first use of "domino" in App B add "(for odd m, any two consecutive unused indices; they need not be of the form {2t, 2t+1})".
- After Lemma 3.12 add "Part (1) does not cover n = 6, 10; this is irrelevant for Theorem 3.7(b), which concerns large n."

**F13** (error; Cor 4.2, sentence "The mean equals Loly's value for every distribution … invariant under relabelling of the values")
Replace it by:
> "The mean equals Loly's value n²(n⁴−1)/12 for every random arrangement with E z_c = 0 for every cell (for instance any distribution invariant under complementation s ↦ N+1−s); magic and semi-magic squares take this value exactly."

**F14** (overclaim; Cor 4.2 title, random.tex l. 41; abstract l. 9; §1 l. 38)
- Title "Null distribution of Loly's invariant" → "Mean and variance of Loly's invariant".
- In the abstract and §1, "the null distribution of Loly's … invariant" → "the mean and variance of Loly's moment-of-inertia invariant under a uniformly random arrangement".

**F15** (clarity; §4.1, random.tex l. 39, "The means … coincide if and only if (n²−1)/6 = 2(n−1)/n")
Replace it by:
> "The two means differ only through the X, Y terms of E₄ and the 2n row and column terms of E_full, whose means are (n⁴−1)/72 and (n−1)(n²+1)/(6n). These agree if and only if n(n+1) = 12, i.e. n = 3, where both energies have mean 40/27."

**F16** (overclaim; Thm 4.3; abstract; §1 l. 36)
- Restate Thm 4.3 as "Proposition 4.3 (Mantel 1967, Hubert 1987; specialised to zero row sums and centred values)".
- Abstract and §1: "we prove an exact formula …" → "we specialise the classical variance formula for quadratic assignment statistics to quadratic forms with zero row sums in the centred entries".
- Thm 4.4 keeps Theorem status.

**F17** (error; Remark 4.6, "the deficit comes from the two negative terms of (4.4)"; Table 3 header; Fig 2 caption)
- Replace the sentence by:
  > "The Gaussian (χ²-mixture) variance is 2tr((σ_n²Γ)²) = N²(N+1)²tr(A²)/72. In (4.4) the coefficient of tr(A²) is this value times 1 − (4N+6)/(5N(N+1)) = 1 − 4/(5n²) + O(n⁻⁴), and the (tr A)² and ΣA_aa² terms are negative. For E_full they give the leading deficit −4/(5n) − 6/(5n) = −2/n; for E₄ all three terms contribute only at order n⁻² (−4/5, −4/5, −42/25, total −82/25)."
- Rename "Gaussian approximation/sd" → "χ²-mixture approximation/sd" in Remark 4.6, the Table 3 header and the Fig 2 caption.

**F18** (gap-in-proof; proof of Cor 4.5, random.tex l. 132)
- Replace "‖a‖₂² is proportional to αᵀC_nα" by "Since Var T_ℓ = σ_n² N‖a_ℓ‖₂², ‖a_ℓ‖₂/τ_ℓ = (σ_n√N)⁻¹ for every ℓ, so ‖a‖₂² = αᵀC_nα/(Nσ_n²)".
- Replace τ₃²/τ₁² = 12(n−1)/(n²(n²−1)) by 12/(n²(n+1)).
- Cite \cite[Thm.~4]{hoeffding1951} with condition (14), not Thm 3.

**F19** (overclaim; after Prop 4.1; §1 novelty sentence)
- After Prop 4.1 add "The means are elementary (sampling without replacement)."
- In §1, "the closed forms of Theorem 4.4" → "the closed forms for the variances in Theorem 4.4", and "Corollary 4.2" → "the variance in Corollary 4.2". Keep "to our knowledge".

**F20** (structure; §2.3 Hoeffding paragraph, displays (2.4)–(2.5))
- Replace the paragraph by:
  > "Hoeffding's combinatorial central limit theorem [Thm 4, p. ⟨page⟩] states that for real vectors a^{(N)}, b^{(N)} the statistic Σ_i a_i b_{π(i)} is asymptotically normal if N·max_i(a_i−ā)²·max_j(b_j−b̄)²/(Σ_i(a_i−ā)²·Σ_j(b_j−b̄)²) → 0."
- Keep the Motoo and Bolthausen sentence. Drop (2.4), (2.5), d_N and conditions (11)–(12).
- The author verifies the display and the page number against the printed paper (see Unresolved).

**F21** (structure; Prop 3.14, Remark 3.15, Remark 2.5, §5.1)
- Move Prop 3.14 and Remark 3.15 into §5.1, retitled "The classes L₃ and L₄", with the variables renamed as in F33.
- Remark 2.5 adds "so γ = (3, −9, 9, −3) and ρ = (−6, 4, 10, −8)" and a forward reference to §5.1.
- Remark 3.15 drops its repetition of the n = 4 example.

**F22** (gap-in-proof; proof of Prop 5.1)
Add:
> "Two further programs written independently of anc/lowmode_enum.c (anc/lowmode_recount.py, anc/table4_recount.py) together reproduce |L₄|, the first-moment count 6,697,177,424 and every entry of Table 4."

**F23** (error; §5.1, local-limit paragraph, computations.tex l. 57, and its last sentence)
- Insert before the |L_n| ≈ formula:
  > "Since any two arrangements differ by a product of transpositions, the differences of (U₁,…,U₄) generate the same lattice as the increments of single transpositions; by a Smith normal form computation (n ≤ 8) this lattice is ℤ⁴."
- Label the formula as a heuristic.
- Replace the last sentence by:
  > "Since det(Σ_U)^{1/2} grows like n^{13}, the heuristic suggests |L_n|/N! ≍ n^{−13}. The same heuristic applied to the 2n independent line conditions, each with variance ≍ n⁵/12, suggests that magic squares form a fraction exp(−5n log n + O(n)) of all arrangements, hence a vanishing proportion of L_n. Neither statement is proved here."
- Note "2n", not "2n+1" (R3.3).

**F24** (error; §5.2, sentences on local minima, steepest descent, swap census; Fig 4)
- Local minima sentence:
  > "Call S a local minimum with respect to transpositions if no transposition lowers the energy. For n = 3 the local minima of E_full are the eight magic squares and eight non-magic arrangements with N²E_full = 2, all strict; E₄ has 344, of which 336 are non-magic, and only 72 of them (64 non-magic) are strict."
- Descent sentence:
  > "Steepest descent on E_full (at each step perform the transposition with the most negative change of N²E_full, ties broken by the first cell pair in row-major order; stop when no transposition lowers it) reaches a magic square in 19.5% (±0.1%), 1.2% and 0.8% of 2×10⁵ runs from uniformly random starts for n = 4, 5, 6."
- In Remark 5.2, "a diagonal separates a, b" → "exactly one of a, b lies on that diagonal", and "gap" → "increase of N²E_full".
- Keep Remark 5.2 with "no two magic squares differ by a transposition" and 2 ≤ g_min ≤ 6.
- Delete Fig 4, the "70 values from 2 to 980" census and the 432/420/28 split, and move them to anc/README.

**F25** (overclaim; abstract)
Replace the abstract by the advocate's A1.14 text with these changes:
- moments written as Σ_{ij}s_{ij}j^m = M(n)Σ_j j^m and Σ_{ij}s_{ij}i^m = M(n)Σ_i i^m;
- results sentence: "Explicit arrangements together with short proofs give k\*(n) = n−1 for 3 ≤ n ≤ 13 and k\*(n) = n−2 for 14 ≤ n ≤ 17, and we prove k\*(n) ≤ n−3 for all n ≥ 18; with computer assistance we determine k\*(n) for all n ≤ 40";
- "pigeonhole principle" in place of "box principle";
- "we specialise the classical variance formula for quadratic assignment statistics …" (F16);
- "the mean and variance of Loly's invariant" (F14);
- "four-term energy E₄" with no "low-order".

**F26** (structure; §1)
- Define in words, at first use: "test function" (a real function φ on the cells, used only through ⟨φ, z⟩), "degree-k conditions" (the first k moments of the column-sum and row-sum vectors vanish), and "witness" (an arrangement satisfying the degree-(K−1) conditions that is not semi-magic, certifying k\*(n) ≥ K; also placed before Thm 3.7).
- Organisation paragraph: drop "moment hierarchy", and add "The two parts are independent: §3 (with Appendices A, B, D) can be read without §4–5 (with Appendix C) and conversely; they share only the notation of §2."

**F27** (structure; §3.7 "Balance of the signed mass", Remark "Quantitative balance", §6 item 3)
- Delete §3.7.
- Keep, as Remark 2.6 "Linear functionals and E_full" after Lemma 2.3, the identity ‖P_Wz‖² = n(‖ρ‖² + ‖γ‖²)/N² + N⁻¹δᵀΓ_D⁻¹δ, the bound nE_full ≤ ‖P_Wz‖² ≤ λ_nE_full, and |Σ_c z_cφ_c| ≤ N‖φ‖√(λ_nE_full) for φ ∈ W.
- Add one sentence: "Nonlinear functionals are not controlled: with u_c the unit vector from the centre to cell c, |Σ_c z_cu_c| = 2(2−√2)√5 for every magic square of order 3 and is positive for all 880 of order 4 (anc/balance_check.py)."
- Delete §6 item 3.

**F28** (clarity; §3.5, "We observe (for these n only; this is not a theorem) …")
Replace it by:
> "For each 14 ≤ n ≤ 40 the witness search succeeded at the last k at which Λ_{n,k} still contains a nonzero vector satisfying (3.1), so k\*(n) equals the least k for which Λ_{n,k} contains no such vector. We do not know whether this holds for all n."

**F29** (overclaim; Fig 3 caption, theory.tex l. 282; l. 291)
- Add to the plot the lower bound given by (3.4), only at the n where it gives K ≥ 2.
- Caption: replace "the curve √(2n), the asymptotic order of the lower bound (b)" by "the lower bound given by (3.4) (open squares; for odd n with small r_q it is trivial and is not plotted), and √(2n), the asymptotic order of (b), which (3.4) approaches slowly".
- Describe the open circles as "computer-assisted upper bounds for 41 ≤ n ≤ 100 (one implementation, not certified)".
- In l. 291 add "(computer-assisted, single implementation)".

**F30** (clarity; Def 2.4)
- After the definition of E₄ add: "E₄ keeps the diagonal conditions and replaces the 2n−2 independent row and column conditions by the two degree-1 moment conditions (Prop 3.3); it is D₄-invariant and has a fixed number of terms, which makes it a test case for a limit law (Corollary 4.5)."
- After the energies add: "Pinn and Wieczerkowski use Σ_Lδ_L² = N²E_full."

**F31** (structure; title)
Recommended, author's decision: "Moments of line sums of magic squares: a permutation threshold and random line-sum energies".

**F32** (jargon; throughout)
- "centred value function" → "centred entries z".
- E_low (\Elow) → E₄, "four-term energy". "low-order conditions / low-order class" → "the four conditions" / "the class L_n of arrangements whose first moments vanish and whose diagonal sums equal M(n)".
- "moment hierarchy" → "moment conditions" (Prop 3.3 title; §3 title "Moment conditions and the permutation threshold").
- "twins on J / twin rows / Twin swaps / twin-row exchange" → "complementary on J / complementary rows / Swaps in complementary rows / exchange in complementary rows" (Def 3.10, Lemmas 3.11–3.12, App B).
- "box principle" → "pigeonhole principle" (Prop 3.13 title "Pigeonhole criterion", abstract, §1).
- Lemma 3.8 title "Column feasibility" → "Majorisation bound for column deviations"; "column-feasibility inequalities" → "the inequalities (3.1)".
- "level k" → "the lattice Λ_{n,k}" everywhere, including App A.
- Remark 3.4: "mixed moment Σz_cx_cy_c (Loly's product of inertia)" once, then "mixed moment"; "multipole" only inside the citation phrase in §3.1.
- "separable test function" → "function of the form a(x)+b(y)".
- "Siamese square" → "Siamese (de la Loubère) magic square [andrews1960magic]".
- "swap gap" → "increase of N²E_full under a transposition".

**F33** (notation; throughout)
- Empirical covariance: delete Cov/Var over cells.
  - background.tex l. 27: keep only ⟨f, g⟩ = N⁻¹Σ_c f_cg_c and ‖f‖.
  - Lemma 2.2: x̄ = ȳ = z̄ = 0; ‖x‖² = ‖y‖² = (n²−1)/12; ‖z‖² = (N²−1)/12; ⟨x, y⟩ = 0; ⟨𝟙_L, z⟩ = δ_L/N.
  - (2.7)–(2.8): E_full = Σ_L⟨𝟙_L, z⟩², E₄ = ⟨x,z⟩² + ⟨y,z⟩² + ⟨𝟙_{D_m},z⟩² + ⟨𝟙_{D_a},z⟩².
  - Def 3.1: drop "i.e. Cov(X^m,Z) = …".
  - σ_n² = ‖z‖²/(N−1).
  - §4: E[T_φT_ψ] = σ_n²⟨φ̃, ψ̃⟩ with φ̃ = φ − φ̄𝟙; Γ_{kl} = ⟨φ̃_k, φ̃_l⟩; random.tex l. 34 "Var(𝟙_L) = (n−1)/n²" → "‖𝟙̃_L‖² = (n−1)/n²", and "meeting in ℓ cells" → "meeting in r cells".
  - Cor 3.5: I(S) = N⟨x²+y², z⟩ + n²(n⁴−1)/12.
  - Cov, Var and E without decoration are then always probabilistic.
- Value index k → v (b_v = v − (N+1)/2) in §2.3, §4 and Thm 4.3.
- Test-function index in §4 and Cor 4.5: k → ℓ (φ_ℓ, a_ℓ, T_ℓ, τ_ℓ, α_ℓ).
- Proof of Thm 3.7(c): multiplier a (F1); do not name the Catalan number C_m (C_n is the correlation matrix).
- Prop 3.13: μ_r → B_r (binomial moments); R_q → r_q.
- Prop 3.14 (moved, F21):
  - (t, u) → (ξ, η), so γ = (ξ, −2ξ, ξ) and ρ = (η, −2η, η);
  - k → κ, so e = −2κ;
  - P, Q, T, U → a′ = a−κ, c′ = c−κ, ξ′ = ξ−κ, η′ = η−κ, with ξ′+η′ = κ;
  - identity Σz² = 2(4κ² + 3(a′²+c′²) + ξ′² + η′²) = 60;
  - drop the name R ("4κ²+ξ′²+η′² is a multiple of 3 and at most 15");
  - same in Remark 3.15 and the labels of anc/n3_lowmode_proof.py.
- Variance polynomials P_o, P_e, Q_o, Q_e → F_o, F_e, G_o, G_e.
- Keep the projection as P_W (not π_W: π is the random permutation).
- App B: sets P, Q → 𝒫, 𝒬; weight index x → ι; half-order m with n = 2m → h with n = 2h (also in Lemma 3.12).
- App C: partitions π, σ → ν, ν′; c(σ) → θ(ν′); add "m_λ = m_ν for any ν of block type λ (e.g. m_{211} for 12|3|4)"; Möbius μ stays.
- Normal law N(0,1) → 𝒩(0,1).

**F34** (notation; end of §2)
Add a two-column notation table (symbol; meaning and where defined) covering:
- n, N, M(n), cells c = (i,j), s, z, x, y, δ_L, ρ, γ, ⟨·,·⟩;
- W, W_R, W_C, W_D, Γ_D, ε_n, P_W;
- E_full, E₄, σ_n;
- Λ_{n,k}, P_γ, k\*(n), B_r, F_q, r_q, H;
- T_φ, τ_ℓ, C_n, Γ, A, h_c;
- L_n, U₁–U₄, Σ_U.

**F35** (clarity; citations of Lemma 3.8 in the F1 text)
In F1 cite Lemma 3.8 explicitly for both ‖γ‖₁ ≤ n⁴/4 and ‖γ‖₂² ≤ n⁵(n²−1)/12. Both are already in the statement of Lemma 3.8 (theory.tex l. 122, with ‖γ‖₁ ≤ N²/4). In F1 write N²/4 = n⁴/4 once, so the reader matches the two.

**F36** (gap-in-proof; anc/ and README)
- Ship anc/kstar_certificates.json: for each 14 ≤ n ≤ 40, the reduced basis at k\*(n), the exact GS norms, and each in-ball vector with its minimal violated (p, sign, J).
- Ship a ≤ 40-line checker that verifies the basis spans Λ_{n,k\*} (unimodular to {t^i(t−1)^{k+1}}), recomputes the GS norms and checks Σ_{j∈J}γ_j against pn(N−pn)/2.
- Ship anc/kstar_enum_independent.py (reviewer's d3.py), anc/lowmode_recount.py (reviewer's c9/d6/d7) and anc/table4_recount.py (advocate's b2.py), with credit in the README.
- The README records the moved swap census (with verify_numbers.py as the source) and the n ≥ 18 rank-2 sanity loop.

**F37** (jargon; cross-paper, Paper A introduction l. 45)
"orthogonality conditions on the height function" → "orthogonality conditions on the centred entries", matching paper B §2.1. Flagged for the consolidation round; it is not a paper-B edit.

### Unresolved
- U1 (D1, F20): the Hoeffding Thm 4 condition (14) display and its page number must be checked by the author against the printed Ann. Math. Statist. 22 (1951). Neither of us could access it.
- U2 (D2, F31): the title is the author's decision; both sides recommend the change.
- U3 (F37): the Paper A wording change lies outside paper B and must be applied and checked in the consolidation round.
- U4 (F29): the upper bounds for 41 ≤ n ≤ 100 remain single-implementation and uncertified; they are labelled as such rather than verified.

## Editor — changes applied

All edits are in `sections/*.tex`, `main.tex` (macro `\Elow` replaced by `\Efour` = E_4) and `anc/`. `references.bib` needed no change. paperB.pdf was rebuilt (23 pages). The `submission/` bundle and `paperB_arxiv.tar.gz` were regenerated. A clean build in a temporary directory (pdflatex + bibtex + pdflatex ×2) has no undefined references, and every page was inspected as an image. Nothing was committed.

- **F1** — done. The two paragraphs are merged into "The lattices Λ_{n,n−2} and Λ_{n,n−3}". The rank-1 case uses γ = a·v, and the rank-2 case uses the agreed t = −1 / Parseval / growth-ratio argument; the Catalan number is not given a symbol. The f(n)/n ≥ 166 sentence, "18 ≤ n ≤ 400" and the App A rank-2 sentence are deleted. The loop survives only as a sanity check described in anc/README.
- **F2** — done (paragraph after Thm 3.7).
- **F3** — done. The paragraph is retitled "Upper bounds for 18 ≤ n ≤ 40" and uses the agreed text. The counts were re-verified with the shipped basis (`kstar_enum_independent.log`): 16 of 23 n have every GS norm above R²; n = 20, 22, 24, 26, 34, 36, 38 have 2, 2, 6, 6, 6, 2, 2 vectors; only n = 26 needs p = 2.
- **F4** — done (Table 2 caption; the table numbers moved by one because of the new notation table).
- **F5** — done. One wording correction: K = ⌊2√n⌋ is not ≥ 2√n, so the text says "for all large n there are such vectors with K = ⌊2√n⌋". The optional footnote gives (√12 − o(1))√n, justified by the same product estimate as in the proof of Thm 3.7(b).
- **F6** — done (§6 item 1; §3.4 sentence). No sharpness is asserted.
- **F7** — done (equal totals, plus the partial sums Σ_{p≤P} v_p = Pn(N−Pn)/2).
- **F8** — done.
- **F9** — done. The Mahler measure is written 𝓜(P), because M(n) is the magic constant.
- **F10** — done (display for Σ log s!; odd-n left side with r_q).
- **F11** — done.
- **F12** — done (domino note in App B, with h in place of m; the n = 6, 10 sentence after Lemma 3.12).
- **F13** — done.
- **F14** — done (Cor 4.2 title, abstract, §1).
- **F15** — done.
- **F16** — done. Thm 4.3 → Proposition 4.3 (Mantel, Hubert; specialised), label `prop:var_identity`. Thm 4.4 keeps Theorem status.
- **F17** — done (Remark 4.6 sentence; "χ²-mixture" in Remark 4.6, the Table 3 header and caption, and the Fig 3 caption; the legend of the regenerated random-energy figure also reads "χ² mixture" and "E_4").
- **F18** — done. The standardised statistics are written T_ℓ/τ_ℓ, not with tildes, because tilde now denotes centring.
- **F19** — done.
- **F20** — done. The paragraph is replaced by the product-array criterion as display (8). **U1 resolved:** the printed paper (JSTOR scan, Ann. Math. Statist. 22 (1951) 558–566) was checked. Theorem 4 and condition (14) are on p. 560, and condition (14) reads N·max(a_i−ā)²·max(b_j−b̄)²/(Σ(a_i−ā)²·Σ(b_j−b̄)²) → 0, as displayed. The citation reads [Thm. 4 and condition (14), p. 560]. The author may wish to re-confirm.
- **F21** — done. Prop 3.14 and Remark 3.15 are now Prop 5.1 and Remark 5.2 in §5.1 "The classes L₃ and L₄", with variables ξ, η, κ, a′, c′, ξ′, η′. Remark 2.5 gives γ, ρ and points to §5.1, and the n = 4 repetition is removed.
- **F22** — done. `anc/lowmode_recount.py` (modes L, XY, ROW4) and `anc/table4_recount.py` were rerun: 14,639,440 with row margins 11,910,864 / 2,611,472 / 117,104; 6,697,177,424; row "4" 100,728 / 9,336 / 7,040; cell (1,1) 429,312. The logs are shipped.
- **F23** — done ("2n independent line conditions"; the formula is labelled a heuristic; the paragraph is titled "A local-limit heuristic").
- **F24** — done. Fig 4 is deleted from the paper; its PDF is moved to `anc/fig_swap_spectrum.pdf` and the census to anc/README. The strict-minimum counts (72; 64 non-magic) are now computed by `verify_numbers.py` (rerun).
- **F25** — done (abstract replaced by the agreed text; submission_notes/arxiv_metadata.md updated to match).
- **F26** — done. Test function, degree-k conditions and witness are defined in §1, and witness again in Def 3.6. The Organisation paragraph has the independence sentence; it notes that App A describes the computations for both parts.
- **F27** — done. §3.7 and §6 item 3 are deleted. The new Remark 2.6 "Linear functionals and E_full" follows Remark 2.5, since it needs E_full from Def 2.4.
- **F28** — done (§3.5 and §6 item 1).
- **F29** — done. The kstar figure is regenerated with the pigeonhole lower bound (open squares, K ≥ 2 only; values 2, 2, 3, 4, …, 7 at n = 14, 20, 30, 40, …, 100). The legend refers to "the pigeonhole criterion" rather than an equation number. The caption and the l. 291 label are added. **U4** is unchanged: the n > 40 bounds remain single-implementation and are labelled as such.
- **F30** — done.
- **F31** — **not applied (U2, author's decision).** The recommended title is recorded in submission_notes/arxiv_metadata.md.
- **F32** — done throughout: centred entries; E₄/four-term energy; the class L_n; moment conditions (§3 and Prop 3.3 titles); complementary rows (Def 3.10, Lemmas 3.11–3.12, Prop 3.13, App B); pigeonhole principle and criterion; "Majorisation bound for column deviations"; Λ_{n,k} instead of "level"; mixed moment (with "Loly's product of inertia" once); a(x)+b(y); Siamese (de la Loubère) magic square [andrews1960magic]; increase of N²E_full. File names such as twin_squares.py are kept, and the README maps the old code terms.
- **F33** — done. Empirical Cov/Var are removed in favour of ⟨·,·⟩, ‖·‖, f̄, f̃. The value index is v; the test-function index in §4 is ℓ; App C uses Γ_{ℓℓ′}. Other renames: B_s/r_q in Prop 3.13; F_o, F_e, G_o, G_e; App B 𝒫, 𝒬, ι and n = 2h (also n = 2h+1 in part (2)); App C ν, ν′, θ(ν′) plus the m_λ sentence; 𝒩(0,1); "meeting in r cells". P_W is kept. Additional clash fixes:
  - the polynomial H(u) in the proof of Prop 3.13 → P_h(u), since H = ⌊n³/4⌋;
  - the bordering shift s → ω;
  - App C's ε → |D_m ∩ D_a|, since ε_n is in Lemma 2.3;
  - the Mahler measure → 𝓜(P).
- **F34** — done (Table 1, §2.5). An initial sentence claiming that no symbol has two meanings within a part was removed, because it is not true (for example a, c and L in §3).
- **F35** — done.
- **F36** — done. New ancillary files:
  - `anc/kstar_enum_independent.py` (independent exact LLL plus enumeration) and its log;
  - `anc/kstar_certificates.json` (basis, exact GS norms, in-ball vectors with minimal (p, sign, J), for 14 ≤ n ≤ 40);
  - `anc/kstar_check_certificates.py` (35 lines, standard library only; checks lattice membership, equal Gram determinant, GS norms and each violation; runs in 0.2 s, all pass);
  - `anc/lowmode_recount.py` and `anc/table4_recount.py`, with logs.

  The README and run_all.sh are updated, including the rank-2 sanity loop and the moved swap census. The README credits the implementations as "written independently" and does not name who wrote them.
- **F37** — **not applied here (U3).** Paper A is outside this edit; the change is for the consolidation round.
- Also: `anc/n3_lowmode_proof.py` labels now match the paper's variables (rerun, all checks pass), and `make_figures.py` no longer builds the swap figure by default.

Unresolved after editing: U2 (title), U3 (paper A wording), U4 (n > 40 bounds uncertified). U1 is resolved against the scanned original but is flagged for the author to re-confirm.

## Consolidation fixes

1. **Equation number in anc files.** "(3.1)" replaced by "(10)" (eq:col_feasible as printed) in `anc/README.md`, `anc/kstar_enum_independent.py` (docstrings, assertion) and `anc/kstar_check_certificates.py` (assertion, output line); the README's first mention now reads "the inequalities (10) of Lemma 3.8 in the paper". The same stale numbering, "(3.4)" for the pigeonhole criterion, was also in `anc/make_figures.py` (docstrings, print) and is now "(11)" (eq:box), consistent with the README. `kstar_check_certificates.py` re-run: "all certificates verified".
2. **h clash in §3.4.** The difference vector in the proof of Prop. 3.13 is renamed h = g - g' -> zeta = g - g' (with zeta_q, P_zeta, B_s(zeta)). The letter zeta is used nowhere else in the paper. delta was rejected because delta_m, delta_a are the diagonal deviations. h stays the half order of Lemma 3.12 / App. B.
3. **F clash.** In Thm 4.4 the variance polynomials F_o, F_e are renamed V_o, V_e (G_o, G_e kept), so F_q (subset sums, Prop. 3.13, Table 1) is the only F. W was not used because it is the line space.
4. **Hoeffding page number.** I could not independently confirm "p. 560": Project Euclid shows only the article range 558-566, and no full text was available. The page number is dropped, and the citation now reads [Thm. 4 and condition (14)]. The theorem and condition numbers are unchanged. The author should confirm against the printed paper and may restore the page number.
5. **Discussion item 1.** Added the qualifier "for all large n" ("the pigeonhole principle produces, for all large n, vectors vanishing to order >= floor(2 sqrt n) at 1"), matching §3.3.
6. **n=26 wording.** §3.5 now says "the exception is n=26, where two of the six vectors need p=2". The README says the same. Checked against `anc/kstar_certificates.json`: the six n=26 vectors have minimal p = 1,1,2,2,1,1.

Rebuilt `main.pdf` / `paperB.pdf` (23 pp.), synced `submission/` (sections, main.tex, bib, bbl, figures, anc), and rebuilt `paperB_arxiv.tar.gz` (same 82-entry listing). A clean temp-dir compile from the tarball (pdflatex, bibtex, pdflatex x2) gives 23 pages with no undefined references and no overfull boxes. I inspected the changed pages (10, 13, 17) as images.
