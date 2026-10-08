# Exact variances of the random energies: a symbolic proof

Companion to `variance_proof.py` (sympy + exact `Fraction` checks; output in `variance_proof.log`,
`variance_proof_results.json`). Runtime ~95 s, most of it the 9! enumeration.

**Result.** The four closed forms in Paper B, App. B, eq. (var_low) (= `anc/variance_fits.json`) are
**correct for every $n\ge3$**, and the derivation below proves them without interpolation. The asymptotic
claims also hold, and the next terms are
$\Var(\Elow)=\frac{n^8}{5184}-\frac{41n^6}{64800}+O(n^5)$ (the $n^7$ coefficient is $0$) and
$\Var(\Efull)=\frac{n^3}{36}-\frac{n^2}{18}-\frac{7n}{180}+O(1)$, for both parities.

---

## 1. Set-up

$N=n^2$. Let $v_k=k-\frac{N+1}2$ ($k=1,\dots,N$), and write $p_r=\sum_k v_k^r$, so that
$p_1=p_3=0$ and
$$p_2=\frac{N(N^2-1)}{12},\qquad p_4=\frac{N(N^2-1)(3N^2-7)}{240}.$$
A uniformly random arrangement gives $z_c=v_{\pi(c)}$ with $\pi$ uniform. For test functions
$\varphi_1,\dots,\varphi_K$ put $a_k=(\varphi_k-\bar\varphi_k)/N\in\mathbb R^N$, so that
$T_k=\Cov(\varphi_k,Z)=a_k^{\top}z$ and
$$E=\sum_k T_k^2=z^{\top}Az,\qquad A=\sum_k a_ka_k^{\top},\qquad A\mathbf 1=0 .$$
$\Elow$ uses $\varphi\in\{X,Y,\mathbf 1_{D_m},\mathbf 1_{D_a}\}$ and $\Efull$ uses the $2n+2$ line indicators.

## 2. Fourth moments of a random permutation

For pairwise distinct cells $c_1,\dots,c_k$ and exponents $\lambda_1,\dots,\lambda_k$,
$\E\prod_j z_{c_j}^{\lambda_j}=M_\lambda/(N)_k$, where $(N)_k=N(N-1)\cdots(N-k+1)$ and
$M_\lambda=\sum_{i_1,\dots,i_k\ \text{distinct}}\prod_j v_{i_j}^{\lambda_j}$. Möbius inversion on the
lattice of set partitions of $\{1,\dots,k\}$ gives $M_\lambda=\sum_\tau\prod_{B\in\tau}(-1)^{|B|-1}(|B|-1)!\,p_{\lambda(B)}$
with $\lambda(B)=\sum_{j\in B}\lambda_j$. With $p_1=0$:
$$
m_4=\frac{p_4}{N},\quad m_{31}=\frac{-p_4}{(N)_2},\quad m_{22}=\frac{p_2^2-p_4}{(N)_2},\quad
m_{211}=\frac{2p_4-p_2^2}{(N)_3},\quad m_{1111}=\frac{3p_2^2-6p_4}{(N)_4}.
$$
Here $m_\pi=\E[z_az_bz_cz_d]$ for $(a,b,c,d)$ whose equality pattern is exactly the set partition $\pi$ of the
positions $\{1,2,3,4\}$. It depends only on the block sizes of $\pi$. Also $\E[z_a^2]=p_2/N$ and
$\E[z_az_b]=-p_2/(N(N-1))$ for $a\ne b$.

## 3. The second moment of a quadratic form (general lemma)

**Lemma.** Let $A$ be symmetric with $A\mathbf 1=0$, $v$ any vector with $\sum v=0$, $N\ge4$, and $z$ a uniformly
random permutation of $v$. Then
$$\E[z^\top Az]=\frac{p_2}{N-1}\operatorname{tr}A,\qquad
\E[(z^\top Az)^2]=c_{22}\big((\operatorname{tr}A)^2+2\operatorname{tr}A^2\big)+c_4\sum_aA_{aa}^2,$$
$$c_{22}=\frac{(N^2-3N+3)p_2^2-N(N-1)p_4}{N(N-1)(N-2)(N-3)},\qquad
c_4=\frac{N(N+1)p_4-3(N-1)p_2^2}{(N-1)(N-2)(N-3)} .$$

*Proof.* $\E[z^\top Az]=\sum_aA_{aa}\frac{p_2}{N}-\sum_{a\ne b}A_{ab}\frac{p_2}{N(N-1)}$, and
$\sum_{a\ne b}A_{ab}=-\operatorname{tr}A$ because the row sums vanish. For the second moment,
$\E[(z^\top Az)^2]=\sum_{a,b,c,d}A_{ab}A_{cd}\,m_{\pi(a,b,c,d)}$. Let $S^{=}(\pi)$ be the sum of $A_{ab}A_{cd}$ over
tuples with equality pattern exactly $\pi$, and let $S^{\ge}(\sigma)=\sum_{\pi\ge\sigma}S^{=}(\pi)$ be the sum over
tuples satisfying (at least) the equalities of $\sigma$. Möbius inversion in $\Pi_4$ gives
$$\E[(z^\top Az)^2]=\sum_\pi m_\pi S^{=}(\pi)=\sum_\sigma S^{\ge}(\sigma)\,c(\sigma),\qquad
c(\sigma)=\sum_{\pi\le\sigma}\mu(\pi,\sigma)\,m_\pi .$$
$S^{\ge}(\sigma)$ is an unrestricted sum. If $\sigma$ has a singleton block, that index occurs in exactly one
factor $A_{\cdot\cdot}$, and summing over it gives a row sum, which is $0$. The partitions of $\{1,2,3,4\}$ with no
singleton are $12|34$, $13|24$, $14|23$ and $1234$, with
$S^{\ge}=(\operatorname{tr}A)^2$, $\operatorname{tr}A^2$, $\operatorname{tr}A^2$ and $\sum_aA_{aa}^2$.
Next, $c(12|34)=m_{22}-2m_{211}+m_{1111}$ and $c(13|24)=c(14|23)$ is given by the same expression. Also
$c(1234)=m_4-4m_{31}-3m_{22}+12m_{211}-6m_{1111}$, using $\mu(\pi,\hat1)=(-1)^{|\pi|-1}(|\pi|-1)!$.
Substituting §2 gives $c_{22}$ and $c_4$. $\square$

For $v=$ the centred values $1,\dots,N$ the poles cancel:
$$c_{22}=\frac{N(N^2-1)(5N+6)}{720},\qquad c_4=-\frac{N^2(N+1)^2}{120},\qquad \frac{p_2}{N-1}=\frac{N(N+1)}{12},$$
and therefore
$$\boxed{\ \Var(z^\top Az)=-\frac{N(N+1)(2N+3)}{360}(\operatorname{tr}A)^2+\frac{N(N^2-1)(5N+6)}{360}\operatorname{tr}A^2-\frac{N^2(N+1)^2}{120}\sum_aA_{aa}^2\ }$$
*Check.* The lemma was verified by enumerating all $N!$ permutations for random integer double-centred $A$ and
random centred $v$ with $N=4,\dots,7$, including $p_3\neq0$.

## 4. The invariants

Let $G_{kl}=\Cov(\varphi_k,\varphi_l)$ be the population covariance over the cells and
$h_c=\sum_k a_{k,c}^2$. Then
$$\operatorname{tr}A=\frac1N\operatorname{tr}G,\qquad \operatorname{tr}A^2=\|M^\top M\|_F^2=\frac1{N^2}\sum_{k,l}G_{kl}^2,\qquad
\sum_aA_{aa}^2=\sum_c h_c^2 .$$
Write $\varepsilon=[n\text{ odd}]$, the number of cells on both diagonals. This is the only place where parity
enters. Facts: $\Var X=\Var Y=\frac{n^2-1}{12}$, a line has $\Var\mathbf 1_L=\frac{n-1}{n^2}$, and two distinct lines
meeting in $m$ cells have covariance $\frac mN-\frac1{n^2}$. So row–column, row–diagonal and column–diagonal pairs
have covariance $0$, two rows (or two columns) have $-\frac1{n^2}$, and the two diagonals have
$\frac{\varepsilon}{N}-\frac1{n^2}$. $X$ and $Y$ are uncorrelated with each other and with the diagonals. For a
line, $(\mathbf 1_L(c)-\frac1n)^2=\frac1{n^2}+(1-\frac2n)\mathbf 1_L(c)$. The cell sums used are
$\sum_c x_c^2=\frac{n^2(n^2-1)}{12}$, $\sum_c x_c^4=\frac{n^2(n^2-1)(3n^2-7)}{240}$,
$\sum_c x_c^2y_c^2=\big(\frac{n(n^2-1)}{12}\big)^2$, $\sum_{c\in D}x_c^2=\sum_{c\in D}y_c^2=\frac{n(n^2-1)}{12}$ for
either diagonal $D$, $\sum_c(d_m+d_a)=2n$ and $\sum_c(d_m+d_a)^2=2n+2\varepsilon$.

**$\Elow$.** $N^2h_c=x_c^2+y_c^2+\frac2{n^2}+(1-\frac2n)(d_m+d_a)(c)$.

| | $n$ odd | $n$ even |
|---|---|---|
| $\operatorname{tr}A$ | $\frac{(n-1)(n^3+n^2+12)}{6n^4}$ | same |
| $\operatorname{tr}A^2$ | $\frac{(n-1)^2(n^6+2n^5+n^4+144)}{72n^8}$ | $\frac{n^8-2n^6+n^4+144n^2-288n+288}{72n^8}$ |
| $\sum A_{aa}^2$ | $\frac{(n-1)(7n^7+7n^6-13n^5+107n^4+240n^2-720n+720)}{180n^{10}}$ | $\frac{7n^8-20n^6+120n^5-107n^4+240n^3-1320n^2+2880n-2160}{180n^{10}}$ |

**$\Efull$.** $N^2h_c=\frac{2n+2}{n^2}+(1-\frac2n)(2+d_m(c)+d_a(c))$, and
$\sum_{k,l}G_{kl}^2=(2n+2)\frac{(n-1)^2}{n^4}+\frac{2n(n-1)}{n^4}+\frac{2(1-\varepsilon)}{n^4}$.

| | $n$ odd | $n$ even |
|---|---|---|
| $\operatorname{tr}A$ | $\frac{2(n^2-1)}{n^4}$ | same |
| $\operatorname{tr}A^2$ | $\frac{2(n-1)(n^2+n-1)}{n^8}$ | $\frac{2(n^3-2n+2)}{n^8}$ |
| $\sum A_{aa}^2$ | $\frac{2(n-1)(2n-1)(n^2+2n-2)}{n^{10}}$ | $\frac{2(2n^4+n^3-10n^2+12n-6)}{n^{10}}$ |

*Check.* All six (×2 parities) invariants equal those computed from the explicit $N\times N$ matrices for
$n=3,\dots,25$.

## 5. Closed forms (Theorem)

Substituting §4 into the boxed formula with $N=n^2$ gives the following, for all $n\ge3$:
$$\E[\Elow]=\frac{(n-1)(n^2+1)(n^3+n^2+12)}{72n^2},\qquad \E[\Efull]=\frac{n^4-1}{6n^2},$$
$$
\Var(\Elow)=\begin{cases}\dfrac{(n-1)(n^2+1)P_o(n)}{129600\,n^6}& n\text{ odd}\\[2mm]
\dfrac{(n^2+1)P_e(n)}{129600\,n^4}& n\text{ even}\end{cases}\qquad
\Var(\Efull)=\begin{cases}\dfrac{(n-1)(n^2+1)Q_o(n)}{180\,n^6}& n\text{ odd}\\[2mm]
\dfrac{(n-2)(n^2+1)Q_e(n)}{180\,n^5}& n\text{ even}\end{cases}
$$
$$
\begin{aligned}
P_o&=25n^{11}+25n^{10}-82n^9-82n^8-9n^7-1209n^6+3738n^5-5862n^4+2160n^3-2880n^2-4320n+4320,\\
P_e&=25n^{10}-107n^8+73n^6-1200n^5+4947n^4-9600n^3+13782n^2-13680n+10080,\\
Q_o&=5n^6-5n^5-17n^4+11n^3-24n^2+18n+6,\\
Q_e&=5n^5-12n^3+12n^2-23n+12 .
\end{aligned}
$$
These are identical (sympy `simplify(difference)=0`) to the paper's expressions. The denominators
$129600n^6$, $180n^6$, … come from $360\cdot360$, the $n^{-10}$ in the invariants and $N^4=n^8$ in $c_{22},c_4$,
after cancellation. The referee's question "why exactly these denominators" is answered by the derivation.

*Suggested text for the paper (replacing the interpolation sentence).* For any symmetric $A$ with zero row sums
and $z$ a uniformly random arrangement of the centred values,
$\Var(z^\top Az)=-\frac{N(N+1)(2N+3)}{360}(\operatorname{tr}A)^2+\frac{N(N^2-1)(5N+6)}{360}\operatorname{tr}A^2-\frac{N^2(N+1)^2}{120}\sum_aA_{aa}^2$.
This follows by Möbius inversion over the equality patterns of a cell quadruple, where only the four
patterns without singletons survive because $A\mathbf1=0$. With $A=\sum_ka_ka_k^\top$ the three invariants are the
explicit rational functions above, depending on parity only through the centre cell shared by the diagonals.

## 6. Check table (exact)

| $n$ | $\Var(\Elow)$ | $\Var(\Efull)$ | sources agreeing |
|---|---|---|---|
| 3 | 1532/2187 | 398/2187 | formula; full $9!$ enumeration (this script); paper |
| 4 | 14093/1440 | 527/640 | formula; paper App. B |
| 5 | 5060614/78125 | 457132/234375 | formula; paper json |
| 6 | 136773793/466560 | 75221/19440 | formula; paper json |
| 7 | 1096104470/1058841 | 776870/117649 | formula; paper json |
| 8 | 226094635/73728 | 171483/16384 | formula; paper json |
| 3–45 | all | all | formula = paper expressions at every $n$ (`variance_proof_results.json`, key `table`) |

## 7. Asymptotics (paper's claims hold)

- $\Var(\Elow)=\frac{n^8}{5184}-\frac{41n^6}{64800}+O(n^5)$ for both parities. The claim $n^8/5184+O(n^7)$ holds,
  and the error is in fact $O(n^6)$.
- $\Var(\Efull)=\frac{n^3}{36}-\frac{n^2}{18}-\frac{7n}{180}+O(1)$ for both parities. The claim $n^3/36+O(n^2)$ holds.

## 8. Hoeffding's condition (referee C2)

Hoeffding, *A combinatorial central limit theorem*, Ann. Math. Statist. 22 (1951) 558–566, **Theorem 3**,
uses $S_N=\sum_{i}c_N(i,\pi(i))$ and
$d_N(i,j)=c_N(i,j)-\frac1N\sum_gc_N(g,j)-\frac1N\sum_hc_N(i,h)+\frac1{N^2}\sum_{g,h}c_N(g,h)$. Its condition is that
for $r=3,4,\dots$
$$\lim_{N\to\infty}\frac{\frac1N\sum_{i,j}d_N(i,j)^r}{\big(\frac1N\sum_{i,j}d_N(i,j)^2\big)^{r/2}}=0 ,$$
and then $(S_N-\E S_N)/\sqrt{\Var S_N}\Rightarrow N(0,1)$. The form with $|d_N|^r$ is equivalent: for even $r$
the two coincide, and the odd absolute ratios are bounded by the geometric mean of the neighbouring even ones
(Cauchy–Schwarz). The precise wording should be checked against the original. I could not re-read it here, but
the "ratio $\to0$" form is the standard citation, and the referee is right that $O(\cdot)$ is wrong.
In the product case $c_N(i,j)=a_ib_j$ (Hoeffding's Theorem 4, generalising Wald–Wolfowitz and Noether), the ratio is
$N^{1-r/2}\kappa_r(a)\kappa_r(b)$ with $\kappa_r$ the standardised $r$-th moment, and the condition is
$N^{1-r/2}\kappa_r(a)\kappa_r(b)\to0$.

**Corrected sentence for §2.3:** "…gives asymptotic normality of $\sum_ic_N(i,\pi(i))$ provided that, for every
integer $r\ge3$, $N^{-1}\sum_{i,j}|d_N(i,j)|^r\big/\big(N^{-1}\sum_{i,j}d_N(i,j)^2\big)^{r/2}\to0$ as $N\to\infty$…;
for product arrays $c_N(i,j)=a_ib_j$ the ratio is $N^{1-r/2}\kappa_r(a)\kappa_r(b)$."

**The Corollary 5.2 proof is correct under the precise condition.** The same "is $O(\ldots)$" phrasing also
appears in the proof itself (computations.tex, the line beginning "Hoeffding's theorem … asserts asymptotic
normality provided that …"), so it should be fixed there too, not only in §2.3. The argument then goes through:
- $\kappa_r(z)\to\int_{-1/2}^{1/2}|u|^r du/(1/12)^{r/2}$, which is $O(1)$.
- For an indicator of $n$ cells, $\kappa_r\sim p^{1-r/2}$ with $p=1/n$, so $\kappa_r=O(n^{r/2-1})$.
- $\kappa_r(X)=O(1)$.
- Hence the ratio is $O(n^2\cdot n^{-r}\cdot n^{r/2-1})=O(n^{1-r/2})=O(N^{1/2-r/4})\to0$ for every $r\ge3$.
- Combinations: Minkowski bounds the numerator, and the denominator is $\alpha^\top R_n\alpha$ with
  $R_n\to I$, since the only nonzero correlation is $-1/(n-1)$ for even $n$.
- Cramér–Wold then gives $N(0,I_4)$. Continuous mapping plus Slutsky applies because the diagonal weights satisfy
  $\Sigma_{33}/\Sigma_{11}=12(n-1)/(n^2(n^2-1))\to0$.
- This gives $\Elow/(2\Sigma_{11})\Rightarrow\chi^2_2/2=\mathrm{Exp}(1)$ with $2\Sigma_{11}=(n^4-1)/72\sim\E\Elow$.

The proof only applies Hoeffding to fixed combinations of 4 statistics, so it is valid. A minor point: say
"for each fixed $\alpha\neq0$".

## 9. Gaussian-mixture heuristic (referee C4)

The Gaussian mixture $\sum_jw_j\chi^2_{1}$ has variance $2\operatorname{tr}\Sigma_n^2=2\big(\frac{N(N+1)}{12}\big)^2\operatorname{tr}A^2$.

At $n=3$:

| energy | Gauss sd | exact sd | sd ratio | variance ratio |
|---|---|---|---|---|
| $\Efull$ | 0.86860 | 0.42660 | 2.04 | 0.2412 |
| $\Elow$ | 1.17121 | 0.83696 | — | 0.5107 |

The table values (0.869, 1.171) and the remark's ratios are correct. **The referee is right:** for $\Efull$ at $n=3$
the mixture overstates the s.d. by a factor $2.04$, and the clause "not a failure of the Gaussian approximation as
such" should be deleted.

The exact formula also explains the slow convergence:
- $\Var/\Var_{\rm Gauss}=1-\frac2n-\frac{7}{5n^2}+O(n^{-3})$ for $\Efull$.
- $\Var/\Var_{\rm Gauss}=1-\frac{82}{25n^2}+O(n^{-3})$ for $\Elow$.
- In both cases the deficit comes from the negative $(\operatorname{tr}A)^2$ and $\sum A_{aa}^2$ terms of the lemma.
- Exact ratios for $n=3,\dots,8$: $0.241,0.453,0.560,0.640,0.692,0.734$ ($\Efull$) and $0.511,0.761,0.857,0.904,0.931,0.948$ ($\Elow$), matching Remark 5.3.
