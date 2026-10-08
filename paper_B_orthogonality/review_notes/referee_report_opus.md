# Referee report

**Manuscript:** "Magic squares as orthogonality conditions on a height function", K. E. Mathewson (25 pp., `paperB.pdf`, compiled 8 Oct 2026)
**Sources consulted:** `main.tex`, `sections/*.tex`, rendered PDF pages. I re-verified by brute force the $n=3$ numbers (760, 4224, 72, 8, 24,192 arrangements with $I=60$, both means $40/27$, variances $398/2187$ and $1532/2187$). I also checked every displayed matrix by hand: the row, column and diagonal sums of the witnesses in Remark 3.3, Theorem 3.15, Theorem 4.1(d) and Appendix C; the values $\Sigma z_cx_cy_c=60$, $\Sigma y_i^2\rho_i=-28$, and $3.38+2.81+15.06=21.25$ in Fig. 1. All of them are correct.

---

## 1. Summary of the claims

The paper centres the entries of an $n\times n$ arrangement of $1,\dots,N=n^2$ to a function $z$ on a centred grid. It then observes that the semi-magic and magic conditions say $z\perp W$, where $W$ is the $2n$-dimensional span of the centred row, column and diagonal indicators. It defines two "energies": $E_{\rm full}$ (the sum of squared line-sum deviations divided by $N^2$) and a four-term $E_{\rm low}$. The paper uses this setup for five groups of statements:

1. A "moment hierarchy". Orthogonality to $x^m,y^m$ for $m\le k$ is equivalent to semi-magic for real $z$ iff $k\ge n-1$ (a Vandermonde fact). For permutations the threshold $k^*(n)$ is $\le n-2$ once $n\ge 14$, and equals $n-1$ for $3\le n\le 13$ by computer-found witnesses. Loly's moment-of-inertia invariance is re-derived, and its null distribution under a random arrangement is computed.
2. "Balance" statements. All separable moments $\sum z\,a(x)$, $\sum z\,b(y)$ vanish for semi-magic squares, mixed moments do not, there is a Cauchy–Schwarz bound for the centre of mass, and unit-vector sums do not vanish.
3. Exact means of $E_{\rm low}$ and $E_{\rm full}$ for a uniform arrangement, "exact" variances, and the limit law $E_{\rm low}/\mathbb E E_{\rm low}\to{\rm Exp}(1)$.
4. A single-swap formula $N^2\Delta E_{\rm full}=d^2m+2d(u(a)-u(b))$, so magic squares are strict local minima with gap $\ge 2/N^2$.
5. The count $|L_4|=14{,}639{,}440$ of $4\times4$ arrangements with $E_{\rm low}=0$, obtained by meet-in-the-middle enumeration, plus a Gaussian local-limit heuristic for $|L_n|$.

The paper has 22 numbered results, 13 remarks and 5 tables.

## 2. Recommendation

- **Electronic J. Combinatorics / Experimental Mathematics: reject in present form.** Almost all numbered results are definitional restatements, standard linear algebra, or one-line applications of the Wald–Wolfowitz and Hoeffding theorems. The only genuinely combinatorial theorem (Theorem 3.15) is weak relative to what is already available from the literature on polynomials with bounded integer coefficients vanishing to high order at 1 (Section 4.1 below). That literature essentially answers the paper's own open question 2, and contradicts the heuristic offered there.
- **Mathematics Magazine / The Mathematical Gazette (Loly's venue) / College Math. J.: major revision.** A note of about 8–12 pages could be acceptable there. It would keep the hierarchy, the permutation threshold reframed through the Prouhet–Tarry–Escott / Littlewood-type connection, the null distribution of Loly's invariant, the exact means, and the $L_4$ count. It would drop or compress the balance, unit-vector, local-search and Monte Carlo material.
- **If the author can prove two-sided bounds for $k^*(n)$** (an upper bound $O(\sqrt{n\log n})$ via Borwein–Erdélyi–Kós, and a lower bound of order $\sqrt{n/\log n}$ via a realisability lemma), that would be a short paper of genuine interest. It would be suitable for EJC or Integers. That result does not exist in the current manuscript.

---

## 3. Triviality / novelty: verdict for every numbered item

Legend: **T** = trivial (immediate from definitions); **S** = standard/folklore; **M** = modest (routine, possibly not in print); **Sub** = substantive.

| # (page) | Statement | Verdict | Justification |
|---|---|---|---|
| Def 1.1 (p1) | arrangement, magic, semi-magic | — | Standard. |
| Def 2.1 (p3) | centred coordinates, "height function" | — | Also repeated verbatim at the start of §3 (p4). "Height function" has a fixed and different meaning in combinatorics (Thurston/Conway height functions of tilings). Consider "centred value function" or simply "$z$". |
| Lemma 3.1 (p4) | means, variances, $\mathrm{Cov}(\mathbf 1_L,Z)=\delta_L/N$ | **T** | Variance of a discrete uniform distribution, plus the definition of covariance. |
| Def 3.2 (p5) | $E_{\rm full}$, $E_{\rm low}$ | — | $N^2E_{\rm full}=\sum_L\delta_L^2$ is the standard sum-of-squared-deviations objective of Monte Carlo and annealing searches for magic squares (e.g. Pinn & Wieczerkowski 1998; see §10). The novelty implied by giving it a name and a covariance dress is nil. |
| Rem 3.3 (p5) | $E_{\rm low}$ does not characterise magic squares for $n\ge4$; witness | **T** + example | The dimension count $4<2n$ already holds for $n=3$ (see §5, item C3). The witness is a useful example. |
| Prop 3.4 (p5) | $D_4$-invariance of energies | **T** | Lines map to lines. |
| Rem 3.5 (p5) | why all $2n+2$ lines | **T** | Fine as a sentence, not as a remark. |
| Lemma 3.6 (p6) | structure and dimension of $W$ ($\dim W=2n$) | **S** | Equivalent to the classical fact that real $n\times n$ magic squares form a space of dimension $n^2-2n$ ($n\ge3$); see Ward (1980) and Stanley EC1 §4.6. Should be cited, not proved at length. |
| Lemma 3.7 (p6) | "projection lemma" | **T/S** | Orthogonal projection onto row-functions is "replace by row means". Part (2) is the formula for projection onto a 2-dimensional span with its Gram matrix. Calling this a "lemma" with a name inflates it. Merge with Lemma 3.6. |
| Lemma 3.8 (p6) | zero set of energies | **T** | The author concedes this (Rem 3.9). Part (3) adds nothing beyond the definitions plus a computation. |
| Rem 3.9 (p7) | "what the projection lemma does and does not say" | — | Defensive; see §6. Delete and fold one sentence into the introduction. |
| Def 3.10 (p7) | degree-$k$ conditions | — | Fine. |
| Prop 3.11 (p8) | moment hierarchy: (a) moments of functions of one index; (b) Vandermonde; (c) binomial vector via finite differences | **S** | (a) is Fubini. (b) and (c) are textbook: the vector $((-1)^j\binom{k+1}{j})_j$ annihilates polynomials of degree $\le k$. The author already says "we claim no novelty". Keep as a lemma of at most 6 lines. |
| Cor 3.12 (p8) | $E_{\rm low}$ = degree-1 truncation | **T** | Restates the definition. |
| Cor 3.13 (p9) | Loly's invariant from the hierarchy | **S** (Loly 2004) | The identity $I=\sum x_j^2\gamma_j+\sum y_i^2\rho_i+\text{const}$ is Loly's own derivation, as the author notes. The observation that one scalar condition is weaker than two is immediate. The count 24,192 vs 72 for $n=3$ is a nice illustration (verified). |
| Cor 3.14 (p9) | null mean and variance of $I(S)$ | **M** | One application of Wald–Wolfowitz (a linear permutation statistic). Probably not in print, and pleasant, but a 3-line computation. Currently placed **before** the result it uses (Prop 5.1); move it after. |
| Thm 3.15 (p10) | $k^*(n)\le n-2$ for $n\ge14$; $k^*(3)=2$, $k^*(4)=3$ | **M** (proof is a simple bounding trick) | The argument is: the orthogonal complement of the polynomials of degree $\le n-2$ is spanned by the binomial vector; integrality gives $\gamma=t v$; then compare the central binomial coefficient with the trivial column-sum bound $n^2(n-1)/2$. Correct (§5), but crude. The Borwein–Erdélyi–Kós theorem (§4.1) gives $k^*(n)=O(\sqrt{n\log n})$ at once, which makes "$\le n-2$" a very weak statement. The exact crossover $n=14$ for the specific level $k=n-2$ is the only genuinely new information. |
| Rem 3.16 (p10) | witnesses $k^*(n)=n-1$, $5\le n\le13$ | **M** (computational) | Realising $\gamma=v$ at $n=13$ (central entry 924 against the bound 1014) is the most interesting computation in the paper. It deserves a description of the search and of how close to the bound it gets. |
| Rem 3.17 (p10) | $E_{\rm low}=0\Leftrightarrow$ magic for $n=3$ | **M** (computational) | Stated as an enumeration fact plus "happen to force $t=u=0$". A two-line human proof via the four lines through the centre should be given (or the claim downgraded). |
| Thm 3.18 (p11) | single-swap formula | **T** | Expand $(\delta+d)^2-\delta^2$ on at most six lines. This is the standard incremental ("delta") evaluation used in every local-search code for magic squares. It should not be a theorem, and should not be one of five headline contributions. |
| Lemma 3.19 (p11) | values of $m(a,b)$ | **T** | Counting lines through two cells. |
| Cor 3.20 (p11) | strict local minimality; $2/N^2\le\Delta_{\min}\le6/N^2$; $n=4$ distribution | **T** (1–2), computational (3) | "Strict local minimum" here means only that no two magic squares differ by a transposition. That holds because a swap of distinct values changes at least two line sums. The $\Theta(n^{-4})$ gap is an artefact of dividing an integer by $N^2$. The $\{2{:}432,3{:}420,4{:}28\}$ distribution is a harmless computation. |
| Rem 3.21 (p12) | swap formula for $E_{\rm low}$ | **T** | — |
| Rem 3.22 (p12) | product of inertia not fixed; 48 values over the 880 squares | **T** + computation | Duplicates Thm 4.1(d). Merge. |
| Thm 4.1 (p12) | "linear balance": $E_{\rm full}=0\iff z\perp\mathcal L$; separable moments vanish; mixed moments do not | **T** | (a) is Lemma 3.8 with constants added. (b)–(c) are Prop 3.11(a) again ($\sum_{ij}z_{ij}a(j)=\sum_j a(j)\gamma_j$). This *is* the definition of semi-magic, restated. (d) is one example plus enumeration; the $n=3$ point-symmetry argument is neat. Labelling this a "Theorem" is the clearest instance of overselling. |
| Thm 4.2 (p14) | $\lvert\sum z(x,y)\rvert^2\le N^2\frac{n(n^2-1)}{12}E_{\rm rc}$, sharp; bound for $\varphi\in W$ | **T** | One Cauchy–Schwarz inequality per coordinate. "Sharp" is just the Cauchy–Schwarz equality case. (c) is the extreme eigenvalues of a $2\times2$ Gram matrix; for odd $n$ the stated constant $n^2/(n-2)$ can be improved to $n^2/(n-1)$. The "numerical verification" on $9!$ and $3\times10^5$ arrangements of a proved inequality (p14) is unnecessary. |
| Prop 4.3 (p14) | unit-vector balance not implied | **T** | (a) is a hand computation for the Lo Shu (correct: $2(2-\sqrt2)\sqrt5$). (b) is trivial: the vertical component is $\sum z_c^2/\lvert v_c\rvert>0$. Nobody would expect a positive-definite sum to vanish, so this is a straw man. (c) restates Thm 4.1. |
| Rem 4.4 (p15) | reading of Prop 4.3 | — | Delete. |
| Rem 4.5 (p15) | gradient flow converges to $z_0-P_Wz_0$ | **T** | Linear algebra. The numerics are off-topic. |
| Rem 4.6 (p15) | multipole language | **T** | Restates Thm 4.1. "We make no claim beyond this algebraic correspondence." |
| Prop 5.1 (p17) | exact means; covariance structure; "exact" variances | **S** for means, **gap** for variances | The means are traces of $\sigma_n^2G$, a direct application of Wald–Wolfowitz/Noether. Equivalently, $\mathbb E\delta_L^2=n\sigma_Z^2(N-n)/(N-1)$ (sampling without replacement) summed over lines, which is a one-line derivation. The variances are **not proved**: they are rational interpolants on $n\le45$ "verified" on more orders (§5, C1). |
| Cor 5.2 (p18) | joint CLT; $E_{\rm low}/\mathbb E\to{\rm Exp}(1)$ | **S** | A direct application of Hoeffding's combinatorial CLT plus Cramér–Wold. The ${\rm Exp}(1)$ is $\chi^2_2/2$ because two asymptotically independent normal coordinates dominate. Correct, but routine. The statement of Hoeffding's condition in §2.3 is wrong (§5, C2). |
| Rem 5.3 (p18) | Gaussian mixture is a heuristic for $E_{\rm full}$ | — | Contains a claim contradicted by Table 3 (§5, C4). |
| Prop 5.4 (p19) | $\lvert L_4\rvert=14{,}639{,}440$; breakdown; first-moment and diagonal classes | **M** (computational) | A reproducible number, well validated (brute-force agreement at $n=3$, semi-magic and magic counts at $n=4$, an independent combinatorial check of the diagonal class, Monte Carlo). Meet-in-the-middle is standard. "$D_4$ acts freely" holds for *all* arrangements, since entries are distinct, so it is trivial and should not be stated as a property of $L_4$. Worth an OEIS entry. |
| App. B (p25) | closed forms for variances | gap | See C1. |
| App. C (p25) | witness for $k^*(5)=4$ | — | Verified by hand. |

### What justifies publication

At most three items carry weight:

1. **Theorem 3.15 + Remark 3.16** (the permutation threshold and the witnesses up to $n=13$). Only this item if it is reframed and strengthened as in §4.1.
2. **Proposition 5.4** ($\lvert L_4\rvert$ and its breakdown): a clean, verified count.
3. **Corollary 3.14 + Proposition 5.1 (means)**: a small but pleasant probabilistic complement to Loly's invariant. Magic squares sit at the null mean of $I$, with zero fluctuation.

Everything else is reformulation, standard, or illustration.

### Overselling (abstract and introduction vs content)

- Abstract: "This viewpoint gives several exact results." Of items (i)–(v), item (ii) is Cauchy–Schwarz plus definitions. Item (iv) is a one-line expansion. Item (iii) is an application of classical theorems, with the variances obtained by interpolation rather than proof.
- Abstract (iii) and Intro item 3: "Exact mean and variance … with exact variances" is not supported; see C1.
- Intro item 2 calls the separable-moment statement "Balance of the signed mass" as if it were a structural result. It is $\sum_{ij}z_{ij}a(j)=\sum_ja(j)\gamma_j$.
- Intro item 4: "every magic square is a strict local minimum … for every $n$" sounds like a landscape theorem. It says only that no two magic squares differ by a transposition.
- Intro, p2: "To our knowledge … the swap formula … [is] new". A delta-evaluation of a sum of squares is not new in any meaningful sense. Remove it from the novelty claim.
- Paradoxically, the introduction and discussion also *undersell* with repeated disclaimers (§6). The net effect is a paper that claims five contributions and then apologises for each. Better: claim fewer and state them plainly.

---

## 4. Main mathematical comments

### 4.1 The permutation threshold is a Prouhet–Tarry–Escott / Littlewood-type problem; the open question is largely answered by known results

Let $P(t)=\sum_{j=0}^{n-1}\gamma_jt^j$. Since $\operatorname{span}\{x_j^m:m\le k\}=\operatorname{span}\{j^m:m\le k\}$, the degree-$k$ conditions on columns (together with $\sum\gamma_j=0$) are equivalent to $\sum_j\gamma_j j^m=0$ for $0\le m\le k$. That is in turn equivalent to $(t-1)^{k+1}\mid P(t)$. Integer vectors with this property are exactly the objects of the **Prouhet–Tarry–Escott problem**, and the order of vanishing at $1$ of polynomials with bounded coefficients is the subject of the **Littlewood-type results of Borwein, Erdélyi and Kós** (Proc. LMS 1999). The consequences are:

- **Upper bound.** Divide $P$ by its lowest nonzero term $\gamma_rt^r$. This gives constant term $1$ and coefficients bounded by $M_n=n^2(n-1)/2$. As I recall it, the Borwein–Erdélyi–Kós bound for polynomials with $\lvert a_0\rvert=1$ and $\lvert a_j\rvert\le M$ allows at most $c\sqrt{n(1+\log M)}$ zeros at $1$ (the author should check the exact hypotheses and statement). It then gives $k^*(n)\le C\sqrt{n\log n}$ for an absolute constant $C$. This is far stronger than $k^*(n)\le n-2$. Theorem 3.15 would then survive only as the exact statement "the level $n-2$ suffices iff $n\ge14$".
- **The heuristic in Open Question 2 (p22) is wrong in its premise.** The author writes that if the smallest vectors were alternating binomial vectors, "the comparison $2^k\gtrsim n^3$ would give $k^*(n)=O(\log n)$". But much smaller vectors are classical:
  - The Prouhet–Thue–Morse vector $((-1)^{s_2(j)})_{0\le j<2^{k+1}}$ has entries $\pm1$ and is orthogonal to all polynomials of degree $\le k$ (Prouhet 1851; Wright 1959).
  - More strongly, Borwein–Erdélyi–Kós construct $\{-1,0,1\}$ polynomials of degree $n$ with a zero of order $\gtrsim\sqrt{n/\log n}$ at 1.

  So the integrality-plus-bound method cannot prove anything better than $k^*(n)\lesssim\sqrt{n\log n}$. And if such small $\gamma$ can be realised by arrangements, then $k^*(n)\gtrsim\sqrt{n/\log n}$, which refutes the suggested $O(\log n)$.
- **What is needed for a real result** is a *realisability lemma*: every $\gamma\in\mathbb Z^n$ with $\sum\gamma_j=0$ and small $\lVert\gamma\rVert_\infty$ (say $\le$ a constant, or $\le cn^2$) is the column-deviation vector of an arrangement with all row sums $M(n)$. A plausible route: start from a suitable semi-magic square, then swap consecutive values lying in the same row. Each such swap shifts two column sums by $\pm1$ and fixes all row sums. The author's own randomised search realised binomial vectors with entries up to 924 at $n=13$, so realisability for small entries looks very likely. Together with BEK this would give $\sqrt{n/\log n}\lesssim k^*(n)\lesssim\sqrt{n\log n}$, which is a genuinely good theorem.

### 4.2 The "energy" and the local search are not new

The objective $\sum_L(\text{line sum}-M)^2$ has been used for decades as the cost function in Monte Carlo, parallel-tempering and annealing searches for magic squares (e.g. Pinn & Wieczerkowski 1998, who used it to *estimate the number* of $6\times6$ magic squares). The swap formula is the delta-evaluation used in such codes. §6.2 should cite this literature, and should either be removed or reduced to a sentence. Table 5 (steepest descent / annealing for $n\le6$) is not a contribution at this level.

### 4.3 The balance section (§4) is mostly redundant

Thm 4.1(b,c) is Prop 3.11(a). Thm 4.2 is Cauchy–Schwarz. Prop 4.3(b) is a sum of squares being positive. Table 1, the Spearman correlations, the gradient-flow remark and the "ring/top" reading belong, if anywhere, in the geometric companion paper A. I recommend compressing §4 to about half a page: one proposition listing which moments vanish, the $xy$ example, and the Lo Shu ring value if the author wants it.

### 4.4 Section 5 relies on Monte Carlo to "confirm" exact results

Table 3 compares exact means with $10^8$-sample Monte Carlo to five digits, for $n\le8$. In a mathematics paper, a proved formula does not need Monte Carlo confirmation. The table should keep only exact values (and, if the author insists, a single sentence about a sanity check). The "Gauss. std" and "KS" columns relate to a heuristic and could go to the supplementary files.

---

## 5. Correctness: gaps and errors

**C1. The "exact variances" are not proved (Prop 5.1, App. B, abstract (iii), Intro item 3).** The proof says the closed forms "were obtained by exact rational interpolation on $n=3,\dots,45$, verified on 5–11 further orders". Interpolation is a proof only if one first shows that, for each parity class, $n^{6}\,\mathrm{Var}(E)$ (or the appropriate denominator) is a polynomial in $n$ of known bounded degree. That is plausible: $\mathbb E E^2$ is a sum over equality patterns of cell quadruples, and the permutation moments are rational in $N$. But the argument must be written down, including why the denominators are exactly $129600n^6$, $180n^6$, etc. Otherwise, call them "conjectured closed forms, verified for $n\le 56$". Also print the polynomials in the paper. They have degree $\le 11$, so they fit, and "listed in the ancillary file" is not acceptable for a stated theorem.

**C2. Hoeffding's condition is misstated (§2.3, p3).** "for every integer $r\ge3$, $N^{-1}\sum_{i,j}\lvert d_N(i,j)\rvert^r$ is $O\bigl((N^{-1}\sum d_N^2)^{r/2}\bigr)$". As far as I recall, Hoeffding's sufficient condition requires that ratio to **tend to zero**, not merely to be bounded. With $O(\cdot)$ the condition is met by degenerate arrays, for which normality fails. The proof of Cor 5.2 actually verifies the $o(\cdot)$ version (ratio $=O(N^{1/2-r/4})\to0$), so only §2.3 needs fixing. Please check the exact form against Hoeffding (1951), Thm 3, or use Motoo's Lindeberg-type condition.

**C3. Remark 3.3 (p5), dimension argument.** "for $n\ge4$ the two cannot agree even before the permutation constraint is taken into account." The count $4<2n$ already holds for $n=3$ ($2n=6$), so at the level of real height functions the two never agree for any $n\ge3$. (Cor 3.12 says exactly this: "never for $n\ge3$".) The $n=3$ exception is purely a permutation phenomenon. Rewrite: "For every $n\ge3$ the four conditions are strictly weaker than the $2n$ magic conditions on real height functions. For permutations they coincide when $n=3$ (Remark 3.17) but not when $n=4$, as the following witness shows."

**C4. Remark 5.3 (p18) contradicts Table 3.** "the Kolmogorov distances 0.10 and 0.20 at $n=3$ are inflated by this discreteness and are not a failure of the Gaussian approximation as such." Table 3 shows the Gaussian-mixture standard deviation of $E_{\rm full}$ at $n=3$ is $0.869$ against the exact $0.4266$, a factor of 2. Remark 5.3 itself gives a variance ratio of $0.24$. That *is* a failure of the approximation. Delete the clause.

**C5. Wrong count for order 5 (§2.4, p3).** "There are 8 magic squares of order 3 …; 7,040 of order 4, forming 880 $D_4$-orbits …; and 275,305,224 of order 5." The figure 275,305,224 (Schroeppel 1973, reported by Gardner 1976) counts squares **up to rotation and reflection**. The total is $8\times275{,}305{,}224=2{,}202{,}441{,}792$. As written, the sentence mixes total counts (8, 7040) with an orbit count.

**C6. Table 2, row $B_{\rm lin}$ (p15).** The caption defines "Rank" as "the percentage of random arrangements with a **smaller** value than the mean over the magic squares". The magic mean of $B_{\rm lin}$ is $0$, so no random arrangement can have a smaller value, yet the table reports $0.03\%$. That figure is the fraction with value *equal* to 0. The text on p15 says the same thing differently ("lying below the 7.4% … quantiles"). Fix the definition to "$\le$", or report $0\%$.

**C7. "$D_4$ acts freely on [$L_4$]" (Prop 5.4).** True, but $D_4$ acts freely on the set of *all* arrangements: a nontrivial $g$ moves some cell, and the entries are distinct. State it as such, or drop it.

**C8. Thm 3.15 proof, induction step (p10).** "which equals 2 for $n$ even and $\frac{2n}{n+1}\ge\frac{28}{15}$ for odd $n\ge14$". The bound $28/15$ is the value at $n=14$, which is even. For odd $n\ge15$ the ratio is $\ge 30/16$. The inequality is still correct (since $30/16>28/15$), but write it as "$\frac{2n}{n+1}\ge\frac{15}{8}$ for odd $n\ge15$". Similarly, simplify $\frac{(n+1)^2}{n(n-1)}\le\frac{225}{182}$ by noting that it decreases in $n$. Otherwise the proof is correct. I checked $\binom{13}{6}=1716>1274$, and that $n=13$ fails ($924<1014$), consistent with Remark 3.16.

**C9. Thm 4.1(b) domain mismatch (p12).** "for all functions $a,b:\{0,\dots,n-1\}\to\mathbb R$ … $a(x_{ij})+b(y_{ij})$". The $x_{ij}$ are half-integers for even $n$ and are not in $\{0,\dots,n-1\}$. Write $a(j)+b(i)$, or let $a,b$ be defined on $\{x_0,\dots,x_{n-1}\}$.

**C10. Thm 4.2(c), constant (p14).** For odd $n$ the eigenvalues of $G$ are both $n-1$, so the constant can be $n/\sqrt{n-1}$. The proof uses $n-2$ for both parities. Either state it parity-dependently or note that the constant is not sharp for odd $n$.

**C11. Cor 3.20(3) wording (p11).** "The possible values of $N^2E_{\rm full}(S^{ab})$ are the integers $d^2m$ …" should be "lie in the set $\{d^2m\}$". Not every pair $(d,m)$ is realised (§5.3 reports 70 distinct values, not 75).

**C12. Remark 3.17 (p10).** "the two diagonal conditions combined with the permutation constraint happen to force $t=u=0$". A short proof is available and should replace the enumeration: the four lines through the centre cover every cell once and the centre four times. Otherwise state that this is computer-verified.

**C13. Fig. 4(b) colour-bar label (p20).** It reads "magic squares", but the heat map counts *swaps* (105,600 in total). Relabel it "number of swaps".

---

## 6. Tone

The paper alternates between overclaiming (theorem labels for trivialities, "exact" for interpolated formulas) and repeated apologetic disclaimers. Both should go. State results plainly, label them proportionately, and say once, in the introduction, what is classical.

| Location | Quoted text | Problem | Suggested replacement |
|---|---|---|---|
| Intro p2 | "This is a reformulation of the definition, not a theorem about magic squares (Remark 3.9); its value is that it makes certain questions natural, and the paper is organised around their answers." | defensive + rhetorical | "This reformulation is elementary; we use it to pose the questions treated below." |
| Intro p2 | "they are small statements about a classical object, and we make no claim that the energy reformulation by itself is a result." | apologetic | Delete. |
| Intro p2 | "To our knowledge the permutation refinement …, the exact moments and limit law …, the swap formula and the exact count for $n=4$ are new" | overclaims the swap formula and limit law | "To our knowledge Theorem 3.15, Corollary 3.14 and the count in Proposition 5.4 have not appeared before; the remaining statements are elementary consequences of classical results, which we include for completeness." |
| §3.1 p5 | "The word 'energy' is a label for these sums of squares and nothing more: no Hamiltonian is implied, and the temperature of the annealing … is a search parameter only." | defensive | "We call $E_{\rm full}$ and $E_{\rm low}$ energies, following the Monte Carlo literature [Pinn–Wieczerkowski]." |
| §3.1 p5 | "which we use constantly" | informal | "which we use throughout". |
| §3.1 p5 (Rem 3.5) | "is the price of invariance" | rhetorical | "is needed for $D_4$-invariance." |
| Rem 3.9 p7 | "it is not a theorem about magic squares, and we do not present it as one." | defensive, repeats intro | Delete the remark. |
| p8, after Prop 3.11 | "and we claim no novelty for them" | apologetic | "Parts (b) and (c) are standard (Vandermonde; finite differences)." |
| p9 | "change the picture in an interesting way." | promotional/informal | "…change the threshold, as follows." |
| Rem 3.17 p10 | "but for the 'wrong' reason … happen to force … Nothing of the sort survives for $n=4$" | informal, rhetorical | "…the equivalence for $n=3$ is due to the permutation constraint: … For $n=4$ it fails: …" |
| §5.3 p19 | "The gap spectrum is arithmetic, not 'banded'" | refers to an earlier draft or claim not in this paper (process leak) | "The set of gaps is $\{d^2m\}$; over the 105,600 swaps it takes 70 values from 2 to 980." |
| Rem 4.6 p16 | "We make no claim beyond this algebraic correspondence." | defensive | Delete. |
| Rem 5.3 p18 | "are not a failure of the Gaussian approximation as such" | defensive and false (C4) | Delete. |
| §6.1 p21 heading | "What the orthogonality viewpoint buys, and what it does not" | informal | "Scope of the orthogonality formulation". |
| §6.1 p21 | "What the viewpoint does not buy is equally clear." | rhetorical | Delete; begin with the next sentence. |
| §6.1 p21 | "it proves nothing about magic squares that the line sums do not already say, and we have not used it to count anything" | self-deprecating, repeated a third time | Delete (already in the introduction). |
| §6.1 p21 | "The low-mode energy is a poor proxy for the magic property" | informal | "For $n=4$ the zero set of $E_{\rm low}$ is about 2080 times larger than the set of magic squares." |
| §6.2 p21 | "so local search is cheap" | informal | "so each move can be evaluated in $O(1)$ time." |
| §6.2 p21 | "The experiment is small and the methods elementary; neither competes with … The energy is a search objective, not a counting tool." | apologetic | Delete, along with most of §6.2. |
| §5.1 p16 | "$E_{\rm low}$ is more rugged" | informal | "$E_{\rm low}$ has more local minima (344, of which 336 are non-magic)." |
| Table 5 caption p22 | "Full-scale data …; an independent rerun at reduced scale … gives success rates …, within sampling error of the table." | process detail | Move to the README. |
| Conclusion p22 | "We have treated this as a viewpoint, not a result" / "What remains is a small set of exact statements about a classical object" | apologetic and repetitive (fourth occurrence) | Replace the conclusion with two sentences stating the main results and the main open problem (the order of $k^*(n)$). |
| Intro p1 | "the paper is organised around their answers" | rhetorical | — (covered above) |
| Abstract | "Place the centred entries … as a height function" | imperative opening | "We regard the centred entries of an $n\times n$ arrangement as a function $z$ on the centred grid." |

**Voice.** The paper mostly uses "we". There is a stray "one cannot hope for more" (p13), and "one has" in theorem statements is fine. Keep "we" consistently and drop "one cannot hope".

**Process mentions.** "banded" (above). Also the LaTeX source carries comments such as `% \usepackage{cleveref} % Not available in basic TeX Live` and a hand-rolled `\Cref` macro. Clean these out before arXiv/journal submission, since the source is public on arXiv. cleveref *is* in TeX Live.

---

## 7. Language, notation and presentation

### 7.1 Notation overloads (all should be fixed)

- **$G$**: the $2\times2$ diagonal Gram matrix (Lemma 3.6/3.7, Thm 4.2), the Gram matrix of all test functions (Prop 5.1), and a coordinate function in Prop 4.3(c) ("$u_c=(F(x_c),G(y_c))$"). Rename the last to $(f_1(x_c),f_2(y_c))$, and the Prop 5.1 matrix to $\Gamma$.
- **$E$**: energies $E_{\rm full},E_{\rm low},E_{\rm rc}$, the shift operator in the proof of Prop 3.11(c) ("Writing $E$ for the shift"), and $\mathbb E$. Use $\tau$ or $\mathsf S$ for the shift.
- **$\Delta$**: forward difference (Prop 3.11), $\Delta E_{\rm full}$ (Thm 3.18) and $\Delta_{\min}$ (Cor 3.20).
- **$m$**: power index (Def 3.10), $m(a,b)$ (Thm 3.18), $m_{ab}$ moments (Rem 4.6), and "two lines meeting in $m$ cells" (proof of Prop 5.1).
- **$\delta$**: line deviation $\delta_L$, the vector $(\delta_m,\delta_a)$, Kronecker $\delta_{kk'}$ (Lemma 3.6(2)), and $\delta_{\rm mean}$ (Table 3).
- **$T$**: $T_a$ (unnormalised, §2.3), $T_\varphi=\mathrm{Cov}(\varphi,Z)$ (normalised, §5.2), and $T_1,\dots,T_4$ (uncentred sums, §5.4).
- **$\Sigma$**: $\Sigma_n$ (covariance of the covariances, §5.2) versus $\Sigma$ (covariance of $T_1,\dots,T_4$, §5.4), which have different scalings.
- **$\gamma,\rho$**: column and row *deviations* of $S$ (§3) versus column and row *sums* $\gamma_j(f),\rho_i(f)$ of a general $f$ (p8). These coincide only for $f=z(S)$. Acceptable, but note it once.
- **$D$** in eq. (17): "$\mathbb E\,\mathrm{Cov}(D,Z)^2$" uses $D$ undefined. Write $D_{\rm m}$ (or $D_{\rm a}$).
- **$C_j$** (p16, "$n\mathrm{Var}(C_j)$") versus $C_\ell$ elsewhere.
- **$\sigma_n^2$** is introduced inside Cor 3.14 (p9) and again in §5.2. Define it once.

### 7.2 Forward references and ordering

- Cor 3.14 (p9) uses Prop 5.1 (p17) and $\sigma_n^2$ from §5.2. Move Cor 3.14 into §5.2.
- Lemma 3.8(3) relies on Remark 3.17 and Prop 5.4 for its $n=3$/$n=4$ claims. Either move those claims out of the lemma or state them as examples.
- Label `sec:results` names the section "Computations". This is cosmetic, but rename the label.
- §6.2 "Local search" is a computation placed in the Discussion.

### 7.3 Specific sentences

- p1–2: the coordinates are defined three times (Intro, Def 2.1, start of §3). Keep only Def 2.1.
- p3, §2.1: "the companion paper A, *Magic Gems: A Polyhedral Framework for Magic Squares* (Mathewson, arXiv:2512.09170) [21], which studies the convex hull of these points, the symmetry classification of the 880 order-four hulls, and the hulls of Siamese squares. Nothing below uses the hull." This duplicates the introduction. Replace both with one sentence in the introduction: "The convex hull of the points $(x,y,z)$ is studied in [21] and is not used here."
- p2: "the count is a meet-in-the-middle enumeration and agrees with a Gaussian local-limit estimate to within 20%". "Agrees" is too strong for a factor of 0.80. Write "is $0.80$ times the Gaussian local-limit estimate".
- p5, Rem 3.5: "dropping them would give a function that is not $D_4$-invariant, because the reflection that maps column $n-1$ to column 0 would change it by $(\gamma_{n-1}^2-\gamma_0^2)/N^2$". Say which reflection, and that this holds whenever $\gamma_0^2\ne\gamma_{n-1}^2$.
- p6, Lemma 3.7(3): define $w_D$ before $Q$. The final clause "but $E_{\rm full}\ne\lVert P_Wz\rVert^2$ in general, because the centred indicators are not an orthonormal system" belongs in the text, not in the lemma.
- p9, Cor 3.13: the list "60, 340, 1300, 3885, 9800, 21840, 44280 for $n=3,\dots,9$" is padding. Delete it.
- p9, Cor 3.14: "29 values from 46 to 74" and "2.9% of arrangements have $I=340$" are fine, but say "exactly 2.9…%" or give the fraction.
- p10, Thm 3.15 title: "Integrality lowers the permutation threshold". The bound, not integrality alone, does the work. Suggest "A permutation threshold below $n-1$".
- p14: "Numerically, inequality (15) has no violation on all 9! arrangements …". Do not test a proved inequality numerically. Delete the sentence and the corresponding panel, Fig. 2(a).
- p15: "the mean over magic squares lying below the 7.4% (ring) and 2.4% (three-dimensional, horizontal) quantiles of the random distribution". Rephrase as "the magic mean lies at the 7.4th (resp. 2.4th) percentile of the random distribution".
- p16, §5.1: "Both energies have mean 40/27 (the coincidence is special to $n=3$: $\mathrm{Var}(X)=\frac{n^2-1}{12}$ equals $n\mathrm{Var}(C_j)=\frac{n-1}{n}$ only there)". Correct, but the parenthesis is hard to parse. Use "since $\mathbb E E_{\rm low}=\mathbb E E_{\rm full}$ iff $\frac{n^2-1}{12}=\frac{n-1}{n}$, i.e. $n=3$".
- p16: "modes 138/81 and 90/81, maxima 180/81 and 360/81, and 177 and 346 distinct values". These statistics carry no mathematical content. Drop them.
- p19, §5.3: "We verified the formula in exact rational arithmetic … on every one of the $880\cdot\binom{16}{2}=105{,}600$ single swaps". A proved one-line identity does not need verification on 105,600 instances. Keep only the gap distribution.
- p20–21: "Heuristically this fraction tends to zero: the four low-mode conditions cost a factor of order $\det(\Sigma)^{1/2}\propto n^{13}$, while a magic square requires $2n$ independent line conditions, each costing a further factor of order $n^{5/2}$." The second half ignores the correlations among line conditions and the lattice issues. Either cite a rigorous heuristic or rigorous result (Canfield–McKay type, or Kuperberg–Lovett–Peled), or soften it to "One expects …".
- p22, Open Q4: "apply verbatim to semi-magic, pandiagonal and Franklin squares". The semi-magic case is already treated (Lemma 3.8(2)). Remove "semi-magic".

### 7.4 Captions

- **Fig. 1** (p7): the caption does not say what $W^\perp\cap\mathbf 1^\perp$ is or why panel (b) is a "schematic", and it gives no dimensions. Add: "$W$ is the $2n$-dimensional span of the centred line indicators."
- **Fig. 2** (p16): panel (a) shows a proved inequality. Delete panel (a) (see above). Panel (b): "magic squares are smaller than typical but never zero". Replace "smaller than typical" with "concentrated at smaller values".
- **Fig. 3** (p19): the caption runs to 9 lines and repeats the text. Panel (c)'s "its standard deviation like $n^4/72$ as well (an exponential limit has unit coefficient of variation)" can be cut.
- **Fig. 4** (p20): fix the colour-bar label (C13). Panel (a)'s annotation arrows cross the bars.
- **Table 1** (p13): "ring / top". "Top" is undefined. The table is wide and hard to read and adds little. Delete it, or reduce it to two rows.
- **Table 3** (p18): see §4.4. Drop the MC columns.
- **Table 4** (p20): the caption contains a proof. That is acceptable, but put the argument in the text.

### 7.5 MSC and keywords

05B15 is "Orthogonal arrays, Latin squares, Room squares". Consider 05B20 or 00A08 (recreational mathematics) together with 60C05 and 60F05 (central limit theorems). Add "Prouhet–Tarry–Escott" as a keyword if §4.1 is adopted.

---

## 8. Structure and length

The 25 pages could become about 10–12 without loss:

- **Cut:** Rem 3.5, Rem 3.9, Rem 3.21, Rem 4.4, Rem 4.5, Rem 4.6, Table 1, Fig. 2(a), §4.2 (keep at most the Lo Shu computation as a remark), §6.2 and Table 5, the MC columns of Table 3, the "verification" paragraphs for proved identities (§5.3 first half, p14 numerical check), §5.1 descriptive statistics, and the conclusion's restatement.
- **Merge:** Lemmas 3.6–3.8 into one lemma; Thm 4.1 into Prop 3.11 (as a corollary listing the moments that vanish); Rem 3.22 with Thm 4.1(d); Thm 3.18, Lemma 3.19 and Cor 3.20 into a single remark.
- **Move:** Cor 3.14 after Prop 5.1; the meet-in-the-middle details and the hardware to an appendix (already done), but shorten them.
- **Expand:** Theorem 3.15 into a section on $k^*(n)$, using the PTE/BEK connection, the witnesses and the realisability question. Also expand the proof of the variance formulas, or downgrade them.

---

## 9. Ten most important changes (ranked)

1. **Reframe and strengthen the permutation threshold (Thm 3.15) via $(t-1)^{k+1}\mid\sum\gamma_jt^j$.** Cite Prouhet–Tarry–Escott and Borwein–Erdélyi–Kós; derive $k^*(n)=O(\sqrt{n\log n})$; and replace the incorrect $O(\log n)$ heuristic in Open Question 2. Ideally, prove a realisability lemma giving a matching lower bound up to logarithms.
2. **Either prove the variance closed forms** (state and justify a degree bound so that interpolation becomes a proof, and print the polynomials) **or stop calling them exact** in the abstract, introduction and Prop 5.1.
3. **Re-label results in proportion to their content.** Demote Thm 3.18, Thm 4.1, Thm 4.2, Lemma 3.7 and Prop 4.3 to lemmas or remarks. Remove the swap formula and the "balance" items from the headline contributions and from the novelty claim.
4. **Remove the defensive and apologetic sentences** (Rem 3.9, "nothing more", "we claim no novelty", "we make no claim", §6.1 paragraph 2, the conclusion). Replace them with one plain sentence in the introduction on what is classical.
5. **Cut §4.2, Table 1, Remark 4.5, §6.2/Table 5 and the Monte Carlo confirmation of proved formulas.** Target about 12 pages.
6. **Cite the prior use of $\sum_L\delta_L^2$ as a search/Monte Carlo objective** (Pinn–Wieczerkowski 1998, and others) and the classical dimension $n^2-2n$ of the space of real magic squares (Ward 1980; Stanley EC1).
7. **Fix the factual and statement errors:** the order-5 count (C5), the Hoeffding condition (C2), Remark 3.3's "$n\ge4$" (C3), Remark 5.3 vs Table 3 (C4), the Table 2 "rank" definition (C6), the Fig. 4(b) colour bar (C13), and the domain in Thm 4.1(b) (C9).
8. **Resolve the notation overloads** ($G$, $E$, $\Delta$, $m$, $\delta$, $T$, $\Sigma$, $D$) and remove the forward reference of Cor 3.14.
9. **Give a short human proof for Remark 3.17** ($E_{\rm low}=0\Rightarrow$ magic for $n=3$). Describe the search that produced the $k^*(n)$ witnesses (moves, objective, run time, how close $\max\lvert v_j\rvert$ is to the bound at $n=13$).
10. **Shorten the introduction and contributions list.** State the three results that matter in plain terms, and remove the double and triple definitions of the coordinates and of paper A.

---

## 10. Missing or imprecise literature

Items I am confident exist:

- **Prouhet–Tarry–Escott / Thue–Morse.**
  - E. M. Wright, "Prouhet's 1851 solution of the Tarry–Escott problem of 1910", *Amer. Math. Monthly* 66 (1959) 199–201.
  - J.-P. Allouche and J. Shallit, "The ubiquitous Prouhet–Thue–Morse sequence", in *Sequences and Their Applications* (Springer, 1999).
  - P. Borwein, *Computational Excursions in Analysis and Number Theory*, CMS Books in Mathematics, Springer, 2002 (chapters on PTE and Littlewood-type problems).
- **Order of vanishing at 1 of polynomials with bounded coefficients.** P. Borwein, T. Erdélyi and G. Kós, "Littlewood-type problems on $[0,1]$", *Proc. London Math. Soc.* (3) 79 (1999) 22–46. This is essential for Thm 3.15 and Open Question 2.
- **Dimension of the space of magic squares.** J. E. Ward III, "Vector spaces of magic squares", *Math. Mag.* 53 (1980) 108–111. Also R. P. Stanley, *Enumerative Combinatorics* Vol. 1 (2nd ed., 2012), §4.6, on magic squares and linear Diophantine equations.
- **Energy / Monte Carlo for magic squares.** K. Pinn and C. Wieczerkowski, "Number of magic squares from parallel tempering Monte Carlo", *Int. J. Mod. Phys. C* 9 (1998) 541–546. It uses the sum of squared line-sum deviations as an energy, and is directly relevant to Def 3.2, §6.2 and the $|L_n|$ heuristics.
- **Combinatorial CLT and refinements.**
  - G. E. Noether, "On a theorem by Wald and Wolfowitz", *Ann. Math. Statist.* 20 (1949) 455–458.
  - E. Bolthausen, "An estimate of the remainder in a combinatorial central limit theorem", *Z. Wahrsch. Verw. Gebiete* 66 (1984) 379–386. This gives a Berry–Esseen rate that would quantify Cor 5.2.
  - B. Motoo, "On the Hoeffding's combinatorial central limit theorem", *Ann. Inst. Statist. Math.* 8 (1957) 145–154 (Lindeberg-type condition).
- **Local limit / counting heuristics for permutations under linear constraints** (context for the $|L_n|$ estimate and Open Question 1):
  - E. R. Canfield and B. D. McKay, "Asymptotic enumeration of integer matrices with large equal row and column sums", *Combinatorica* 30 (2010) 655–680.
  - A. Barvinok, "What does a random contingency table look like?", *Combin. Probab. Comput.* 19 (2010) 517–539.
  - G. Kuperberg, S. Lovett and R. Peled, "Probabilistic existence of regular combinatorial structures", *Geom. Funct. Anal.* 27 (2017) 919–972.
  - S. Eberhard, F. Manners and R. Mrazović, "Additive triples of bijections, or the toroidal semiqueens problem", *J. Eur. Math. Soc.* 21 (2019) 441–463. A Fourier-analytic local limit for permutation statistics, of the same type as the $|L_n|$ heuristic.
- **"Height function" terminology clash.** W. P. Thurston, "Conway's tiling groups", *Amer. Math. Monthly* 97 (1990) 757–773. Cite it if the term is kept, or rename.
- **Precision of existing citations.**
  - The order-5 count should be attributed to R. Schroeppel (1973), as reported by Gardner (1976), and described as "up to symmetry".
  - Frénicle's list of the 880 squares (B. Frénicle de Bessy, *Des quarrez ou tables magiques*, 1693) should be cited directly if it is mentioned.
  - The `trump2012enumeration` entry is a web page; give its URL and access date.
