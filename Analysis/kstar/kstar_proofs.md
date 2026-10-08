# The permutation threshold k*(n): two-sided bounds and exact values for 14 ≤ n ≤ 40

Working notes for paper B (`paper_B_orthogonality`), Theorem 3.15 / Remark 3.16 / Open Question 2.
Everything below marked **Theorem**, **Lemma** or **Proposition** is proved here in full; computational
statements are produced by the scripts in this directory in exact integer arithmetic (one floating-point
MILP run is used only as a cross-check and is labelled as such). Nothing in the paper directories was edited.

**Summary.**

* (Upper bound, Theorem A, self-contained.) Every arrangement satisfying the degree-k conditions with
  (k+1)^2 > πe(n−1)·log(n^4/4) is semi-magic. Hence k*(n) ≤ √(πe(n−1) log(n^4/4)) = (2√(πe)+o(1))·√(n log n) ≈ 5.84·√(n log n).
  This beats k*(n) ≤ n−2 for every n ≥ 166; for 14 ≤ n ≤ 165 exact lattice enumeration gives much better upper bounds (table §4).
  The same order √(n log n) follows from Borwein–Erdélyi–Kós (1999), Theorem 2.1, with an unspecified constant (or from their Theorem 2.8 with the constant 44/7); the hypotheses are checked in §1.
* (Lower bound, Theorem B, constructive and new.) k*(n) ≥ (√2 − o(1))·√n. This is stronger than the √(n/log n) the referee asked for.
  The proof combines a box-principle argument (as in BEK Theorem 2.7) with an explicit realisability device: semi-magic squares with
  many pairs of "twin" rows that are complementary on many columns. In such squares a swap inside one row of a twin pair shifts mass
  between two columns, and a swap in the twin row shifts the same mass back. All row sums stay equal to M(n).
* So √n ≲ k*(n) ≲ √(n log n). Closing the √(log n) gap is the analogue of the gap left open in BEK for {−1,0,1} polynomials (between √(n/log n) and √n). We could not close it.
* (Exact values, computer-verified.) k*(n) = n−2 exactly for 14 ≤ n ≤ 17, and k*(n) ≤ n−3 for every n ≥ 18. The values for 14 ≤ n ≤ 40 are
  12,13,14,15,15,16,16,17,17,18,18,19,19,20,21,21,22,22,23,23,23,24,24,25,25,26,26.
  For each n the upper bound is an exact lattice enumeration, and the lower bound is an explicit arrangement verified in exact arithmetic.
* The heuristic k*(n) = O(log n) in Open Question 2 is false: by Theorem B, k*(n) ≥ (√2 − o(1))√n.

---------------------------------------------------------------------------------------------------------

## 0. Setting and the polynomial reformulation

S is an arrangement of {1,…,N} (N = n^2) on the n×n grid, M = M(n) = n(N+1)/2. γ_j is the deviation of column j (column sum minus M),
ρ_i the deviation of row i, and Σ_j γ_j = Σ_i ρ_i = 0. Put P_γ(t) = Σ_{j=0}^{n−1} γ_j t^j.

**Lemma 0.** For γ ∈ R^n and k ≥ 0 the following are equivalent:
(i) Σ_j γ_j = 0 and Σ_j x_j^m γ_j = 0 for 1 ≤ m ≤ k (x_j = j − (n−1)/2);
(ii) Σ_j C(j,r) γ_j = 0 for 0 ≤ r ≤ k;
(iii) (t−1)^{k+1} divides P_γ(t).

*Proof.* The vectors (x_j^m)_j for m ≤ k and (C(j,r))_j for r ≤ k span the same space, namely the restrictions to {0,…,n−1} of the
polynomials of degree ≤ k in j. So (i)⇔(ii). Taylor expansion at 1 gives P_γ(t) = Σ_r (Σ_j C(j,r)γ_j)(t−1)^r, because
P_γ^{(r)}(1)/r! = Σ_j C(j,r)γ_j. Hence (ii)⇔(iii). ∎

So S satisfies the degree-k conditions iff (t−1)^{k+1} | P_γ and (t−1)^{k+1} | P_ρ. As in the paper, k*(n) is the least k for which
this forces γ = ρ = 0. Write Λ_{n,k} = {γ ∈ Z^n : (t−1)^{k+1} | P_γ} = (t−1)^{k+1}·Z[t]_{<n−k−1}, a lattice of rank n−k−1.

**Column feasibility (used throughout).** If γ is the column-deviation vector of an arrangement, then:

* (F1) |γ_j| ≤ n(N−n)/2 = n^2(n−1)/2;
* (F2) for every p, the sum of the p largest γ_j is at most pn(N−pn)/2, and the sum of the p smallest is at least −pn(N−pn)/2.

*Proof.* p columns hold pn distinct values. Their total is at most the sum of the pn largest values, pn(2N−pn+1)/2. Subtracting pM = pn(N+1)/2 gives pn(N−pn)/2. The other side is symmetric, and F1 is the case p = 1. ∎

Consequences of F2:

* ‖γ‖_1 = 2·(sum of the positive γ_j) ≤ 2·max_p pn(N−pn)/2 ≤ N^2/4 = n^4/4.
* γ is majorised by v with v_p = n(N−(2p−1)n)/2. By Schur convexity, ‖γ‖_2^2 ≤ Σ_p v_p^2 = n^5(n^2−1)/12.

---------------------------------------------------------------------------------------------------------

## 1. What can be cited from the literature (checked against the paper's text)

P. Borwein, T. Erdélyi, G. Kós, *Littlewood-type problems on [0,1]*, Proc. London Math. Soc. (3) 79 (1999) 22–46.
(The PDF from T. Erdélyi's homepage is in `lit/BEK1999.pdf`, and its text is in `lit/BEK1999.txt`.)

* **Theorem 2.1 (verbatim).** "There is an absolute constant c > 0 such that every polynomial p of the form
  p(x) = Σ_{j=0}^n a_j x^j, |a_j| ≤ 1, a_j ∈ C, has at most c(n(1 − log|a_0|))^{1/2} zeros at 1."
  *Application.* Let γ ≠ 0 with (t−1)^K | P_γ. Let r be the least index with γ_r ≠ 0 and H = max_j|γ_j|, and put
  p(t) = P_γ(t)/(H t^r). Then p has degree ≤ n−1, its coefficients have modulus ≤ 1, |a_0| = |γ_r|/H ≥ 1/H, and p has the same
  multiplicity K at 1. So K ≤ c√((n−1)(1+log H)). With H ≤ n^2(n−1)/2 (F1) this gives k*(n) ≤ c'√(n log n).
  The hypotheses are satisfied exactly. Only the absolute constant is unspecified.
* **Theorem 2.8 (verbatim).** "If |a_0| ≥ exp(−L^2) and |a_j| ≤ 1 for each j = L^2+1, …, n, then the polynomial p(x) = Σ a_j x^j,
  a_j ∈ C has at most (44/7)(L+1)√n + 5 zeros at 1." With the same p, |a_0| ≥ 1/H. Take L = ⌈√(log H)⌉, so that L^2 is an
  integer ≥ log H. This gives the explicit bound k+1 ≤ (44/7)(⌈√(log H)⌉+1)√(n−1) + 5, which is weaker than Theorem A below.
* **Theorem 2.7** (box principle). Some p ∈ F_n (coefficients in {−1,0,1}) has at least c√(n/log(n+1)) zeros at 1. The proof
  (p. 1109 of the text file) is the pigeonhole argument we adapt in §3. **Theorem 2.4:** if |a_0| = 1 and |a_j| ≤ 1, there are at most (16/7)√n + 4 zeros at 1.
  BEK remark that for F_n the true order lies between √(n/log n) and √n and that "completely closing the gap … looks quite difficult."
* BEK say Theorem 2.1 "sharpens and generalizes results of Amoroso, Bombieri and Vaaler, and Hua … for polynomials with integer
  coefficients". Our Lemma 1 is a short self-contained integer-coefficient argument (Jensen + Taylor) in that spirit.
* Prouhet–Thue–Morse: Π_{i<K}(1 − t^{2^i}) has coefficients ±1, degree 2^K − 1, and is divisible by (t−1)^K (each factor is
  divisible by (t−1)). Classical (Prouhet 1851; Wright, Amer. Math. Monthly 66 (1959) 199–201). It only gives k ≈ log_2 n and is superseded by §3.
* *Not checked:* D. W. Boyd, *On a problem of Byrnes concerning polynomials with restricted coefficients*, Math. Comp. 66 (1997)
  1697–1703 (±1 polynomials divisible by high powers of (x−1)). We did not consult it and do not rely on it.

---------------------------------------------------------------------------------------------------------

## 2. Upper bound

**Lemma 1 (order of vanishing at 1 of an integer polynomial).** Let γ ∈ Z^n \ {0} and suppose (t−1)^K | P_γ with K ≥ 1. Then
K^2 ≤ πe(n−1)·log‖γ‖_1.

*Proof.* Write P = P_γ and L_1 = ‖γ‖_1. Since P ≠ 0 has degree ≤ n−1, K ≤ n−1.

(a) *Mahler measure.* P has integer coefficients and a nonzero leading coefficient a. By Jensen's formula,
∫_{−1/2}^{1/2} log|P(e^{2πiθ})| dθ = log( |a| Π_α max(1,|α|) ) ≥ log|a| ≥ 0.

(b) *Trivial bound.* |P(z)| ≤ L_1 for |z| = 1.

(c) *Near 1.* Since P^{(i)}(1) = 0 for i < K, Taylor's formula with integral remainder along the segment [1,z] gives
P(z) = (z−1)^K/(K−1)! · ∫_0^1 (1−s)^{K−1} P^{(K)}(1+s(z−1)) ds. For |z| ≤ 1 the point w = 1+s(z−1) satisfies |w| ≤ 1. Hence
|P^{(K)}(w)| ≤ Σ_j |γ_j| j(j−1)…(j−K+1) ≤ L_1 (n−1)!/(n−1−K)!, and therefore
|P(z)| ≤ L_1 C(n−1,K) |z−1|^K ≤ L_1 (e(n−1)|z−1|/K)^K.

(d) For z = e^{2πiθ}, θ ∈ [−1/2,1/2], we have |z−1| = 2|sin πθ| ≤ 2π|θ|. With a = 2πe(n−1)/K, (b) and (c) give
log|P(e^{2πiθ})| ≤ log L_1 + K·log min(1, a|θ|). Since K ≤ n−1, a ≥ 2πe > 2, so 1/a < 1/2, and
∫_{−1/2}^{1/2} log min(1, a|θ|) dθ = (2/a)∫_0^1 log u du = −2/a.

Integrating (d) and using (a): 0 ≤ log L_1 − 2K/a = log L_1 − K^2/(πe(n−1)). ∎

**Theorem A.** Let n ≥ 3 and let S be an arrangement satisfying the degree-k conditions with
(k+1)^2 > πe(n−1)·log(n^4/4). Then S is semi-magic. Consequently
k*(n) ≤ ⌊√(πe(n−1) log(n^4/4))⌋ ≤ 2√(πe)·√(n log n) (≈ 5.84·√(n log n)).

*Proof.* By Lemma 0, (t−1)^{k+1} | P_γ. If γ ≠ 0, Lemma 1 with ‖γ‖_1 ≤ n^4/4 (consequence of F2) gives
(k+1)^2 ≤ πe(n−1) log(n^4/4), a contradiction. So γ = 0. The rows satisfy F1, F2 as well (by transposition), so ρ = 0 by the same argument.
For the last inequality: (n−1)·log(n^4/4) < 4n log n. ∎

*Numerics.* ⌊√(πe(n−1)log(n^4/4))⌋ < n−2 holds for every n ≥ 166 (checked to n = 10^6; for larger n it follows from the asymptotics).
For n ≤ 165 the exact enumeration of §4 gives far better values. In particular, `below_n_minus_2.py` checks that for every
18 ≤ n ≤ 170 the rank-2 lattice Λ_{n,n−3} has no nonzero vector passing F1–F2. Together with Theorem A for n ≥ 166 this gives
**k*(n) ≤ n−3 for all n ≥ 18**. With §4 and the paper's Remark 3.16, the complete picture of the "linear regime" is:
k*(n) = n−1 for 3 ≤ n ≤ 13, k*(n) = n−2 for 14 ≤ n ≤ 17, and k*(n) ≤ n−3 for all n ≥ 18.

*Remarks.*

* With the explicit-constant BEK Theorem 2.8 one gets about (44/7)·√(3 log n)·√n ≈ 10.9√(n log n), which is worse. Lemma 1 is preferable for the paper because it is short and self-contained.
* Lemma 1 is only as good as the integrality and size information it uses. For integer vectors with |γ_j| ≤ H = n^3 and length n, the box-principle construction (as in §3, without realisability) gives multiplicity ≍ √(n log H/ log n) ≍ √n. So no argument that uses only "integer + bounded entries" can give an upper bound below order √n, and Lemma 1 is off from that by at most √(log n).

---------------------------------------------------------------------------------------------------------

## 3. Lower bound

### 3.1 Twin rows and the realisability device

**Definition.** Rows i ≠ i' of an arrangement S are *twins on* a set J of columns if s_{ij} + s_{i'j} = N+1 for all j ∈ J.

**Lemma 2 (twin swaps).** Let S be semi-magic and let i, i' be twins on J. For j, j' ∈ J put d = s_{ij'} − s_{ij}; then d ≠ 0 and also
d = s_{i'j} − s_{i'j'}. Swapping the entries of row i in columns j, j' gives an arrangement with the same row sums and with
γ = d(e_j − e_{j'}). Swapping instead in row i' gives γ = −d(e_j − e_{j'}). Swaps in different rows, or in disjoint column pairs of
the same row, involve disjoint cells. So any combination of them gives row sums M and γ equal to the sum of the individual effects.

*Proof.* Immediate. s_{i'j} − s_{i'j'} = (N+1−s_{ij}) − (N+1−s_{ij'}) = d. ∎

Permuting the columns of a semi-magic square keeps it semi-magic and keeps twin relations (with J permuted). So we may place any
chosen disjoint column pairs at adjacent positions.

### 3.2 Squares with many twin rows

**Lemma 3 (even n).** Let n = 2m with m even (n ≡ 0 mod 4, n ≥ 4) or m odd with m ≥ 7 (n ≡ 2 mod 4, n ≥ 14). Then there is a semi-magic
square of order n in which rows r and m+r are twins on all columns, for every 0 ≤ r < m.

*Proof.* Work with *weights*. The value v has weight w = |2v − (N+1)|, an odd number in {1,3,…,N−1}. Each weight w belongs to exactly
two values (N+1 ± w)/2, which are complements. Index the weights by x = (w−1)/2 ∈ {0,…,2m^2−1}. It suffices to partition the index
set into m *rows* R_0,…,R_{m−1} of size n and to give signs σ_x ∈ {±1} such that Σ_{x∈R_r} σ_x w_x = 0 for every r. Then fill row r (in any
order) with the values (N+1+σ_x w_x)/2, x ∈ R_r, and row m+r with their complements in the same columns. Every value 1..N occurs exactly once.
Row r has sum n(N+1)/2 + ½Σσw = M, row m+r has sum n(N+1) − M = M, and each column has sum m(N+1) = M.

A *domino* is a pair of consecutive indices {x, x+1}. Its weights differ by 2, so with signs (+,−) or (−,+) it contributes ∓2.

* m even: use the dominoes {2t, 2t+1}, t < m^2. Row r gets m of them, with alternating sign patterns; the contributions cancel because m is even.
* m odd ≥ 7: row r receives three things.
  1. The *quadruple* {4r,…,4r+3}, with weights 8r+1, 8r+3, 8r+5, 8r+7 and signs (+,+,+,−). It contributes 16r+2.
  2. The *pair* {α_r, β_r} with α_r = 5m−1−r and β_r = 5m+7r, and signs (+,−). It contributes (2α_r+1) − (2β_r+1) = −2(8r+1).
  3. m−3 dominoes (an even number) with alternating sign patterns.

  The quadruples fill [0, 4m−1] and the α's fill [4m, 5m−1]. The β's are 5m, 5m+7, …, 12m−7; consecutive β's leave gaps of exactly 6
  indices, and the tail [12m−6, 2m^2−1] has even length 2m^2−12m+6 ≥ 0 because m ≥ 7. So the remaining indices split into
  3(m−1) + (m^2−6m+3) = m(m−3) dominoes, as required. ∎

(The case n = 6, 10 is not needed: the paper already settles n ≤ 13.)

**Lemma 4 (interval sums).** If I is a set of consecutive integers and 1 ≤ k ≤ |I|, then the sums of the k-subsets of I are exactly the
integers between the sum of the k smallest and the sum of the k largest elements of I.

*Proof.* If a k-subset X is not the top one, some x ∈ X has x+1 ∈ I \ X. Replacing x by x+1 raises the sum by 1. Starting from the
bottom subset we reach every intermediate sum. ∎

**Lemma 5 (one border; odd order).** Let n = 2m+1 with m ≥ 4, N = n^2, c = (N+1)/2, and let T be a semi-magic square of order n−2 with
values 1,…,(n−2)^2. Then there is a semi-magic square S of order n with:

* inner block S_{ij} = T_{i−1,j−1} + 2n−2 for 1 ≤ i, j ≤ n−2;
* rows 0 and n−1 twins on the inner columns 1,…,n−2;
* columns 0 and n−1 "twins" on the inner rows (s_{i0} + s_{i,n−1} = N+1).

*Proof.* The border uses the 4m complementary pairs {p, N+1−p}, p = 1,…,4m = 2n−2. Let A = 4m and B = 4m−2.

* Corners: s_{00} = N+1−A, s_{n−1,n−1} = A, s_{0,n−1} = B, s_{n−1,0} = N+1−B.
* Let P = [2m, 4m] \ {A, B} (2m−1 elements) and Q = [1, 2m−1] (2m−1 elements). We have ΣP − ΣQ = 4m^2 − 4m + 2.
* Choose an m-subset T_+ of the interval I = [2m, 4m−3] ⊂ P and an (m−1)-subset T_− of Q with ΣT_+ − ΣT_− = c − A + B = 2m^2 + 2m − 1.
  By Lemma 4, ΣT_+ ranges over all integers in [m(5m−1)/2, m(7m−5)/2] and ΣT_− over all integers in [m(m−1)/2, 3m(m−1)/2]. So
  the difference takes every integer in [m^2+m, 3m^2−2m], which contains 2m^2+2m−1 when m ≥ 4.
* Inner top row: the values N+1−p (p ∈ T_+) and p (p ∈ T_−), in any order. Inner bottom row: the complements, in the same columns.
* Inner left column: the values N+1−p (p ∈ P∖T_+) and p (p ∈ Q∖T_−). Inner right column: the complements, in the same rows.

Checks:

* Top row sum: (m+1)(N+1) − A − ΣT_+ + B + ΣT_− = (m+1)·2c − (c − A + B) − A + B = (2m+1)c = M.
* Left column sum: (m+1)(N+1) − A − B − Σ(P∖T_+) + Σ(Q∖T_−). This equals M iff Σ(P∖T_+) − Σ(Q∖T_−) = c − A − B. That is
  automatic, since it equals (ΣP − ΣQ) − (c − A + B) = 4m^2−4m+2 − (2m^2+2m−1) = 2m^2−6m+3 = c − A − B.
* The bottom row and right column sum to n(N+1) − M = M.
* Each inner row is (n−2)(N+1)/2 + (N+1) = M, using M(n−2) + (n−2)(2n−2) = (n−2)(N+1)/2. The same holds for each inner column.
* Every value occurs exactly once. ∎

**Corollary 6 (odd n, concentric).** For odd n ≥ 9 there is a semi-magic square of order n such that for each
ℓ = 0,1,…,(n−9)/2 the rows ℓ and n−1−ℓ are twins on the columns ℓ+1,…,n−2−ℓ.

*Proof.* Start from any 7×7 magic square (e.g. de la Loubère's). Apply Lemma 5 successively for the orders 9, 11, …, n. Every
earlier border is shifted by a constant and stays inside, and the shift preserves twin relations: (a+s)+(b+s) = N'+1 when
a+b = N+1 and s = (N'−N)/2. ∎

`constructions.py` implements Lemmas 3, 5 and Corollary 6 literally and verifies the output exactly for all 7 ≤ n ≤ 150 (n ≠ 10).

### 3.3 The box-principle lower bound

Fix n as in Lemma 3 or Corollary 6.

* Even n: column pairs (2q, 2q+1), q = 0,…,Q−1 with Q = n/2. Each pair is covered by R_q = n/2 twin pairs.
* Odd n: column pairs (2q+1, 2q+2), q = 0,…,Q−1 with Q = (n−3)/2. Pair q is covered by the twin pairs of the layers
  ℓ ≤ min(2q, n−4−2q, (n−9)/2), so R_q = min(2q, n−4−2q, (n−9)/2) + 1.

**Theorem B.** If K ≥ 2 satisfies
  Π_{q<Q} (⌈R_q/2⌉ + 1)  >  Π_{r=0}^{K−2} ( (N−1)·Σ_{q<Q} R_q·C(q,r) + 1 ),        (★)
then there is an arrangement with all row sums M(n), γ ≠ 0 and (t−1)^K | P_γ. It satisfies the degree-(K−1) conditions and is not
semi-magic, so k*(n) ≥ K.

*Proof.*

1. *A large family of attainable coefficients.* For each q let d_{q,1},…,d_{q,R_q} be the twin differences of Lemma 2 for the column
   pair q (nonzero integers, |d| ≤ N−1). At least ⌈R_q/2⌉ of them have the same sign. Their partial sums, together with 0, form a
   set F_q of ⌈R_q/2⌉+1 distinct sub-multiset sums. Each element of F_q lies in an interval of length W_q = Σ_i|d_{q,i}| ≤ R_q(N−1).
2. *Moments.* For g = (g_q) ∈ Π_q F_q put μ_r(g) = Σ_q g_q C(q,r), 0 ≤ r ≤ K−2. Then μ_r(g) lies in an integer interval of length
   Σ_q W_q C(q,r), so the moment vector takes at most the right-hand side of (★) values.
3. *Collision.* By (★) and the box principle there are g ≠ g' with μ(g) = μ(g').
4. *Realisation.* For each q, g_q − g'_q = Σ_{I∖I'} d − Σ_{I'∖I} d, where g_q = Σ_I d and g'_q = Σ_{I'} d. Apply the row-i swap for
   twin pairs in I∖I' and the twin-row swap for those in I'∖I (Lemma 2; all cells are disjoint). The result has row sums M, i.e. ρ = 0, and
   γ = Σ_q (g_q − g'_q)(e_{j_q} − e_{j_q+1}), where j_q = 2q (even n) or 2q+1 (odd n).
5. *Divisibility.* Then P_γ(t) = t^{j_0}(1−t)·G(t^2) with G(u) = Σ_q (g_q − g'_q)u^q ≠ 0. Since Σ_q (g_q−g'_q)C(q,r) = 0 for r ≤ K−2,
   (u−1)^{K−1} | G (Lemma 0), hence (t^2−1)^{K−1} | G(t^2), and so (t−1)^K | P_γ. Also γ ≠ 0 because G ≠ 0. ∎

**Corollary 7.** liminf_{n→∞} k*(n)/√n ≥ √2. Together with Theorem A:
  (√2 − o(1))·√n ≤ k*(n) ≤ (2√(πe) + o(1))·√(n log n).

*Proof.* Let K − 1 = k = ⌊α√n⌋ with α < √2 fixed.

*Right side of (★).* Σ_{q<Q} C(q,r) = C(Q, r+1) ≤ C(n, r+1), R_q ≤ n and N ≤ n^2, so each factor is ≤ n^4·C(n, r+1). Hence
log RHS ≤ 4k log n + Σ_{s=1}^k (s log n − log s!).
Using log s! ≥ s log s − s and Σ_{s≤k} s log s ≥ (k^2/2)log k − k^2/4, this is
log RHS ≤ (k(k+1)/2) log n − (k^2/2) log k + O(k^2 + k log n) = (α^2/4)·n log n + O(n).

*Left side of (★).*
* Even n: log LHS = (n/2)·log(⌈n/4⌉+1) = (n/2) log n − O(n).
* Odd n: R_q ≥ min(q+1, Q−q, (n−9)/2) for all q < Q. Hence log LHS ≥ Σ_q log min(q+1, Q−q, (n−9)/2) − O(n) ≥ 2 log(⌊Q/2⌋!) − O(n) = (n/2) log n − O(n), by Stirling.

Since α^2/4 < 1/2, (★) holds for all large n. (Even n ≡ 2 mod 4 with n ≥ 14, n ≡ 0 mod 4 and odd n ≥ 9 are all covered.) ∎

*Numerics for (★)* (`pigeonhole.py`, exact integers; "generic" = (★) exactly as stated; "exact-d" = the same argument with the actual
F_q = all distinct sub-multiset sums and the actual W_q of the explicit squares, which is equally rigorous):

| n | 14 | 20 | 26 | 38 | 50 | 74 | 98 | 150 | 200 | 400 | 1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (★) generic | 2 | 2 | 3 | 3 | 4 | 6 | 7 | 10 | 12 | 18 | 32 |
| exact-d | 4 | 5 | 7 | 9 | 11 | 14 | 17 | 23 | – | – | – |
| √n | 3.7 | 4.5 | 5.1 | 6.2 | 7.1 | 8.6 | 9.9 | 12.2 | 14.1 | 20 | 31.6 |

The convergence to √2·√n is slow. For moderate n the exact computations of §4 are much stronger. `pigeonhole_demo.py` carries
out the box-principle construction explicitly (random choices, birthday collision) for n = 14, 15 and checks the resulting arrangement in exact arithmetic.

**Remark (Open Question 2).** The paper's heuristic "if the smallest vectors were alternating binomial vectors … k*(n) = O(log n)" is false.
Corollary 7 gives k*(n) ≥ (√2 − o(1))√n. Concretely, k*(40) = 26 (§4) while 2^{k} ≳ n^3 would suggest k ≈ 16.

---------------------------------------------------------------------------------------------------------

## 4. Exact values of k*(n) for 14 ≤ n ≤ 40, and upper bounds to n = 165

*Method.*

* **Upper bound.** k*(n) ≤ k+1 as soon as Λ_{n,k+1} contains no nonzero vector satisfying F1 and F2 (then γ = 0, and ρ = 0 by
  transposition). The lattice is LLL-reduced (exact, SymPy) and searched by an exact Schnorr–Euchner enumeration (Gram–Schmidt in
  `Fraction`s, `lattice.py`). It visits every lattice vector with ‖γ‖_2^2 ≤ n^5(n^2−1)/12, and every vector passing F2 is in this
  ball (§0). Correctness of the enumerator was checked against brute force (`test_enum.py`). For 14 ≤ n ≤ 30 the F1-only version
  was cross-checked with an independent floating-point MILP (`crosscheck_milp.py`, HiGHS), with full agreement.
* **Lower bound.** Take a vector γ ∈ Λ_{n,k} \ {0} passing F1–F2 (the enumeration's shortest candidates). Find an arrangement with
  all row sums M and column deviations γ by steepest descent and simulated annealing (`realise.py`, `anneal.c`, `anneal2.c`). Every
  arrangement found is re-verified independently (`verify_witnesses.py`). It is a permutation of 1..N with ρ = 0, column
  deviations γ, Σ_j x_j^m γ_j = 0 for m ≤ k (exact rationals), and the degree-(k+1) column condition fails.

| n | k*(n) | n−k*(n) | max\|γ_j\| of witness | bound n^2(n−1)/2 |
|---|---|---|---|---|
| 14 | 12 | 2 | 297 | 1274 |
| 15 | 13 | 2 | 572 | 1575 |
| 16 | 14 | 2 | 1001 | 1920 |
| 17 | 15 | 2 | 2002 | 2312 |
| 18 | 15 | 3 | 1430 | 2754 |
| 19 | 16 | 3 | 2860 | 3249 |
| 20 | 16 | 4 | 1794 | 3800 |
| 21 | 17 | 4 | 3094 | 4410 |
| 22 | 17 | 5 | 2210 | 5082 |
| 23 | 18 | 5 | 3638 | 5819 |
| 24 | 18 | 6 | 2380 | 6624 |
| 25 | 19 | 6 | 4522 | 7500 |
| 26 | 19 | 7 | 2736 | 8450 |
| 27 | 20 | 7 | 4541 | 9477 |
| 28 | 21 | 7 | 8892 | 10584 |
| 29 | 21 | 8 | 6405 | 11774 |
| 30 | 22 | 8 | 11737 | 13050 |
| 31 | 22 | 9 | 9330 | 14415 |
| 32 | 23 | 9 | 14881 | 15872 |
| 33 | 23 | 10 | 11799 | 17424 |
| 34 | 23 | 11 | 9177 | 19074 |
| 35 | 24 | 11 | 18147 | 20825 |
| 36 | 24 | 12 | 14766 | 22680 |
| 37 | 25 | 12 | 24150 | 24642 |
| 38 | 25 | 13 | 16515 | 26714 |
| 39 | 26 | 13 | 26520 | 28899 |
| 40 | 26 | 14 | 22233 | 31200 |

All 27 witnesses (arrangements and γ) are in `kstar_witnesses.json`.

Observations:

* k*(n) = n−2 exactly for 14 ≤ n ≤ 17. The level n−2 stops being needed at n = 18.
* For n = 26 the sup-norm test F1 alone is not enough: Λ_{26,19} contains vectors with |γ_j| ≤ 8450, but none passes F2.
* In every case 14 ≤ n ≤ 40 the column-feasibility tests F1–F2 were the only obstruction: the first F1–F2-feasible lattice vector at the critical level was realisable with ρ = 0. (Observation, not a theorem.)

*Rigorous upper bounds k*(n) ≤ U(n) for n > 40 from the same enumeration* (`upper_scan.py`, `upper_scan_14_160.json`; the scan
was still running at the time of writing, so see `kstar_table.md` for the range completed): Examples: U(50) = 30, U(80) = 39, U(100) = 45. These are upper bounds only; we did not search for witnesses beyond n = 40.

---------------------------------------------------------------------------------------------------------

## 5. What is *not* proved

* The order of k*(n). Between √n and √(n log n) we cannot decide. The upper-bound method (integrality + size) cannot go below
  order √n (§2, remark). The lower-bound method loses nothing in order, so the open question is whether realisability or some
  finer arithmetic of permutations forces more.
* Whether k*(n) is monotone in n.
* Whether F1–F2 are the only obstructions in general.
* Lemma 3 for n = 6, 10 (not needed).
* Explicit constants valid for *all* n in Corollary 7. The theorem form (★) is explicit and checkable for each n, but the clean
  statement is only asymptotic. (★) was evaluated only at the n listed in the table.

## 6. Files

| file | content |
|---|---|
| `constructions.py` | Lemmas 3, 5, Cor. 6 (explicit squares with twin rows) + exact verification |
| `pigeonhole.py`, `pigeonhole_bounds.json`, `pigeonhole_demo.py` | Theorem B numerics; explicit box-principle witness |
| `lattice.py`, `test_enum.py` | exact LLL + enumeration of Λ_{n,k}; brute-force test |
| `exact_kmax.py`, `upper_scan.py`, `upper_scan_*.json`, `below_n_minus_2.py` | rigorous upper bounds via F1–F2 |
| `realise.py`, `realise_c.py`, `anneal.c`, `anneal2.c`, `kstar_exact.py`, `hard_cases.py` | witness search |
| `kstar_witnesses.json`, `verify_witnesses.py` | the 27 witnesses n = 14..40 and their exact verification |
| `crosscheck_milp.py` | floating-point MILP cross-check (not used for any claim) |
| `lit/BEK1999.pdf`, `lit/BEK1999.txt` | Borwein–Erdélyi–Kós paper |
| `kstar_table.md` | tables |
| `paperB_kstar_section.tex` | recommended LaTeX for paper B |
