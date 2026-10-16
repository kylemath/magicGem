# Literature check for the referee's finding B1 (and B5), 16 October 2026

Normalisations used throughout. A column-deviation vector is gamma in Z^n, P_gamma(t) = sum_{j<n} gamma_j t^j
(degree <= n-1). The degree-k conditions say (t-1)^{k+1} | P_gamma, so the relevant quantity is the
multiplicity K = k+1 of the zero at 1. Lemma 3.8 of the paper (column feasibility) gives
|gamma_j| <= n^2(n-1)/2 (height H <= n^3/2), ||gamma||_1 <= N^2/4 = n^4/4 and ||gamma||_2^2 <= n^5(n^2-1)/12.
Writing P_gamma = t^r Q with Q(0) != 0, Q has integer coefficients, so |Q(0)| >= 1 and |lead Q| >= 1.

## Sources actually read

| item | how verified | what was read |
|---|---|---|
| P. Borwein, T. Erdelyi, G. Kos, Littlewood-type problems on [0,1], Proc. London Math. Soc. (3) 79 (1999) 22-46 | author PDF people.tamu.edu/~terdelyi/papers-online/PLMS.pdf (already cited as BEK1999) | Thms 2.1, 2.3, 2.4, 2.7, 2.8 and Theorem A (Section 4), page images checked |
| P. Borwein, T. Erdelyi, G. Kos, The multiplicity of the zero at 1 of polynomials with constrained coefficients, Acta Arith. 159 (2013), no. 4, 387-395, doi:10.4064/aa159-4-7 | IMPAN page, Crossref, author PDF zeros12_rev.pdf | abstract, Thms 2.1-2.2, lemmas |
| T. Erdelyi, Coppersmith-Rivlin type inequalities and the order of vanishing of polynomials at 1, Acta Arith. 172 (2016), no. 3, 271-284, doi:10.4064/aa8129-11-2015 (arXiv:1406.2560) | IMPAN page, arXiv PDF | abstract, Thms 2.1-2.2, references |
| F. Amoroso, Polynomials with prescribed vanishing at roots of unity, Boll. Un. Mat. Ital. B (7) 9 (1995), no. 4, 1021-1042 | IRIS Torino record hdl 2318/1944843 (author manuscript), citation in a Cambridge reference list | Section 1 (Mignotte's bounds as quoted), Theorems 1 and 2, Prop. 1 (page images checked) |
| M. Mignotte, Estimations elementaires effectives sur les nombres algebriques, in Journees Arithmetiques 1980 (J. V. Armitage, ed.), LMS Lecture Note Ser. 56, CUP 1982, pp. 364-371 | Cambridge Core table of contents of LMS LN 56 | NOT read; its result is known to me only as quoted by Amoroso (1995), Section 1. Amoroso's reference list gives pp. 24-34, Cambridge Core gives 364-371; I used Cambridge Core |
| E. Bombieri, J. D. Vaaler, Polynomials with low height and prescribed vanishing, in Analytic Number Theory and Diophantine Problems (Stillwater 1984), Progr. Math. 70, Birkhauser 1987, 53-73, doi:10.1007/978-1-4612-4816-3_3 | Crossref (pages 53-73), SpringerProfessional abstract | abstract only (paywalled); content as described by Amoroso (1995) |
| P. Erdos, P. Turan, On the distribution of roots of polynomials, Ann. of Math. (2) 51 (1950) 105-119 | scan users.renyi.hu/~p_erdos/1950-08.pdf | pp. 105-106: statement of Schur's inequality (1.4) and Theorem I |
| I. Schur, Untersuchungen uber algebraische Gleichungen, Sitzungsber. Preuss. Akad. Wiss., Phys.-Math. Kl. (1933) 403-428 | bibliographic data from the reference lists of Erdos-Turan (1950) and BEK (1999) | NOT read; statement taken from Erdos-Turan (1950) and BEK (1999) |
| "Mignotte 1980, Some inequalities about univariate polynomials" (SYMSAC '81) | not located in full text | not read; I found nothing connecting it to zeros at 1, so it is not cited |

## Statements (exact, as read)

* **Schur's inequality** (Erdos-Turan 1950, (1.4), attributed to Schur 1933, "with the best possible constant 4"):
  if f(x) = a_0 + ... + a_n x^n has R real roots, then R^2 <= 4n log P, P = (|a_0|+...+|a_n|)/sqrt|a_0 a_n|.
  BEK 1999, Theorem A (Section 4): m positive real roots => m^2 <= 2n log P. (This follows from the
  real-root form applied to f(x^2), which has degree 2n, the same P, and 2m real roots.)
* **Mignotte** (as quoted by Amoroso 1995, Section 1): for 0 < r < N and V(r,N) the rational polynomials of
  degree < N vanishing at 1 to order >= r, with h = logarithmic height,
  (1/4) r^2/N - log N <= min_{G in V(r,N), G != 0} h(G) <= (1/2) r(r+1)/(N-r) log N + r log 4/(N-r).
  The lower bound "was a consequence of an old theorem of Schmidt and Schur about the number of real zeros"
  and the upper bound came from Siegel's lemma. Amoroso's proof of his Prop. 1 shows h(G) = log max|g_l| for
  primitive integer G; for every integer G != 0, h(G) <= log max|g_l|.
* **Amoroso 1995**, Theorem 1: N^{-1} h(G) >= ((c-eps)/2)(r/N)^2 (1+o(1)), c = sum_{s>=1} s!/(2s-1)! = 1.38844...,
  as N,r -> infinity with r/N -> 0 and sqrt(N log N)/r -> 0. Theorem 2: there is G != 0 in V(r,N) with
  N^{-1} h(G) <= (1/4)(r/N)^2 log(N/r)(1+o(1)), as N,r -> infinity, r/N -> 0, sqrt(N/log N)/r -> 0.
* **Bombieri-Vaaler 1987** (per Amoroso): recover Mignotte's upper bound by their geometry-of-numbers Siegel
  lemma (with a family of N-r independent small polynomials), lower bound by "automatic vanishing" at p-th
  roots of unity.
* **BEK 1999**, Thm 2.1: every p = sum_{j<=n} a_j x^j, |a_j| <= 1, a_j in C, has at most c (n(1 - log|a_0|))^{1/2}
  zeros at 1 (c absolute, unspecified). Thm 2.3: for each n there is such p with real coefficients having a
  zero at 1 of multiplicity at least min{(1/6)(n(1-log|a_0|))^{1/2} - 1, n}. Thm 2.8 (explicit constant): if
  |a_0| >= exp(-L^2) and |a_j| <= 1 for j > L^2, at most (44/7)(L+1) sqrt n + 5 zeros at 1. Thm 2.4: |a_0| = 1,
  |a_j| <= 1 => at most (16/7) sqrt n + 4 zeros at 1. Thm 2.7: some p with coefficients in {-1,0,1} has at least
  c sqrt(n/log(n+1)) zeros at 1 (box principle); the authors add that closing the gap between sqrt(n/log n) and
  sqrt n "looks quite difficult".
* **BEK 2013**: kappa_inf(n,L) = largest k with (x-1)^k | P, P != 0 of degree <= n, |a_0| >= L max_{j>=1}|a_j|,
  a_j in C. Thm 2.1: c_1 sqrt(n/L) - 1 <= kappa_inf(n,L) <= c_2 sqrt(n/L) for L >= 1/2. The abstract recalls
  the earlier (BEK 1999) result min{(1/6) sqrt(n(1-log L)) - 1, n} <= kappa_inf(n,L) <= min{c_3 sqrt(n(1-log L)), n}
  for L in (0,1]. Thm 2.2: kappa_2 analogues.
* **Erdelyi 2016**, Thms 2.1-2.2: for all 1 <= p <= inf and L in (0,1/2], c_3 min{sqrt(n(-log L)), n} <=
  kappa_p(n,L) <= c_4 min{sqrt(n(-log L)), n} + 4 with c_3 = 2/7, c_4 = 13 (kappa_p: |a_0| >= L ||(a_1..a_n)||_p);
  for L > 1/2 orders sqrt n (c L)^{-q/2} (p > 1) and sqrt(n(1-L)) (p = 1). Lower-bound polynomials have real
  coefficients (Lemmas 3.2-3.4).

## Verdicts on the referee's claims

1. *"Mignotte's lower bound on height gives Lemma 3.8 / Theorem 3.7(a), possibly with a better constant
   (about 4 sqrt(n log n) vs 2 sqrt(pi e))."* **Confirmed** (via Amoroso's quotation). With h(G) <= log max|gamma_j|
   <= log(n^2(n-1)/2): K^2 <= 4n log(n^3(n-1)/2), i.e. K <= (4+o(1)) sqrt(n log n), against the paper's
   2 sqrt(pi e) = 5.84. In fact the source of Mignotte's bound, Schur's inequality, gives more: applied to Q(t^2)
   (degree 2d <= 2(n-1), P <= ||gamma||_1 <= n^4/4, 2K real roots) it gives K^2 <= 2(n-1) log(n^4/4), i.e.
   K <= (2 sqrt 2 + o(1)) sqrt(n log n) = 2.83 sqrt(n log n). So the paper's Lemma (Jensen, constant pi e) is
   strictly weaker than a 1933 result. Sanity check: the inequality m^2 <= 2d log(||g||_1/sqrt|a_0 a_d|) holds,
   with ratio at most 0.78, on 603 LLL-reduced vectors of Lambda_{n,k} (8 <= n <= 40), on the 27 witnesses
   14 <= n <= 40 (ratio <= 0.76) and on (t-1)^m (t+1)^j (scratch script, not in anc/).
   Crossovers. Old bound floor(sqrt(pi e (n-1) log(n^4/4))): < n-1 for all n >= 164 (first n: 164), <= n-3 from
   166, < n-3 from 169; at n = 100 it is 120 (> n-1). New bound floor(sqrt(2(n-1) log(n^4/4))): < n-1 from n = 24,
   <= n-3 from 27, < n-3 from n = 30 (all n up to 10^6 checked); values 32 at n = 40, 58 at n = 100 (computed
   upper bound 45). So the referee's "n >~ 166" is right for the old constant (exact: 164 for beating n-1).
2. *"Siegel-lemma upper bounds give lattice vectors of order about sqrt(24 n), beating the paper's sqrt 12
   footnote."* **Partly correct.** Plain pigeonhole/Siegel (Mignotte's upper bound as rewritten by Amoroso,
   (1/2)(r/N)^2 log(N/r), and the paper's footnote) give (sqrt 12 - o(1)) sqrt n. The constant sqrt 24 needs
   Amoroso's Theorem 2 (BV Siegel lemma plus his lower bounds): with N = n, r = alpha sqrt n, h(G) <=
   (alpha^2/8 + o(1)) log n, which is < log(n^3/4) for alpha < sqrt 24 and n large; such G has ||G||_1 <= n^4/4 and
   satisfies every inequality (10) of the paper (|sum_J| <= p max|g| <= p n(N-pn)/2 for p <= n/2, and by
   complement for p > n/2). Hence the lattice-feasibility threshold U(n) >= (sqrt 24 - o(1)) sqrt n. (Asymptotic
   only; the o(1) is not explicit.)
3. *"Open question 1 is the known log gap."* **Confirmed.** For integer polynomials of degree < N with height
   e^h, the lower and upper bounds for the minimal height (Mignotte 1982, Bombieri-Vaaler 1987, Amoroso 1995)
   differ by a factor log(N/r); in the regime h ~ 3 log n relevant here this is exactly sqrt n versus
   sqrt(n log n). Amoroso's Thm 1 (lower bound with constant c/2) needs r >> sqrt(N log N), i.e. h >> log N,
   so it does not apply here. BEK 1999 state the height-1 analogue of the gap (sqrt(n/log n) vs sqrt n) as open.
4. *"BEK 2013 / Erdelyi 2016 show kappa ~ sqrt(n(1 - log L)) is sharp for complex/real coefficients, so the
   Jensen route cannot beat sqrt(n log n) without integrality."* **Partly correct.** The sharpness for
   L in (0,1] is BEK 1999 (Thms 2.1, 2.3), quoted in BEK 2013's abstract; BEK 2013 itself treats L >= 1, which
   is not our regime. Erdelyi 2016 Thms 2.1-2.2 do give the sharp order sqrt(n(-log L)) for L <= 1/2 with
   explicit constants (2/7 and 13) in every l^p normalisation, including l^1, the paper's. Conclusion that holds:
   the Jensen argument uses integrality only through |a_0| >= 1 (or |lead| >= 1), and real polynomials with
   |a_0| = 1, |a_j| <= H vanish to order >= (1/6) sqrt(n(1 + log H)) - 1 at 1 (BEK 1999 Thm 2.3 rescaled), so no
   argument of that type can give o(sqrt(n log n)) for H = n^{O(1)}. (Schur's bound uses |a_0 a_d| >= 1; I did not
   find a statement of its sharpness for that class with both ends integral, so I do not claim it.)
5. Amoroso citation: the referee's "Boll. UMI ~1990" is wrong in the year: Boll. Un. Mat. Ital. B (7) 9 (1995).
   Erdelyi's and BEK's [A-90] is a different Amoroso paper (Ann. Inst. Fourier 40 (1990), integer transfinite
   diameter), not used here.

## B5 sources

| item | verified | used for |
|---|---|---|
| H. E. Daniels, The relation between measures of correlation in the universe of sample permutations, Biometrika 33(2) (1944) 129-135, doi:10.1093/biomet/33.2.129 | Crossref, OUP landing page (full text paywalled); content as described by Zou, Xu, Ding, Han (arXiv:2601.20018, Example 1.2) | "generalized correlation coefficient" sum_{ij} c_ij a_ij under permutations |
| A. R. Bloemena, Sampling from a Graph, Mathematical Centre Tracts 2, Mathematisch Centrum, Amsterdam, 1964 | NYPL and CAVAL catalogue records; scan of the third printing (1976) at ir.cwi.nl/pub/13031/13031D.pdf (contents, Sect. 1.1, Thm. 4.1.1 read in OCR) | Sect. 1.1: x_B = sum m_ij x_ij^(B), the (weighted) number of joins of a graph between r_1 randomly chosen black points; Thm 4.1.1: under non-free sampling (x_B - E x_B)/sigma(x_B) tends to N(0,1) under growth conditions. Cited as: asymptotic normality of the number of edges joining randomly sampled points |
| L. Zhao, Z. Bai, C.-C. Chao, W.-Q. Liang, Error bound in a central limit theorem of double-indexed permutation statistics, Ann. Statist. 25(5) (1997) 2210-2227, doi:10.1214/aos/1069362395 | Crossref with abstract | Berry-Esseen bound via Stein's method for double-indexed permutation statistics |
| A. D. Barbour, L. H. Y. Chen, The permutation distribution of matrix correlation statistics, in Stein's Method and Applications, Lect. Notes Ser. Inst. Math. Sci. Natl. Univ. Singap. 5, Singapore Univ. Press / World Scientific, 2005, 223-245, doi:10.1142/9789812567673_0015 | Crossref; description in Reinert-Rollin (Ann. Probab. 2009, arXiv:0711.1082, Section 4.3) | exchangeable-pair (Stein) normal approximation for matrix correlation (QAP) statistics |
| Barbour-Eagleson, Chen-Fang | not verified (Crossref search failed; Chen-Fang concerns the single-indexed statistic) | not cited |

Variance ratio: tau_3^2/tau_1^2 = sigma^2 ||1~_D||^2 / (sigma^2 ||x~||^2) = ((n-1)/n^2) / ((n^2-1)/12)
= 12/(n^2(n+1)): **confirmed**. The diagonal share of E[E_4] is 12/(n^3+n^2+12): 0.25 (n=3), 0.074 (n=5),
0.020 (n=8).

## Second round

| item | verified | used for |
|---|---|---|
| P. Borwein, M. J. Mossinghoff, Polynomials with height 1 and prescribed vanishing at 1, Experimental Math. 9(3) (2000) 425-433, doi:10.1080/10586458.2000.10504419 | Crossref; abstract as quoted by a web search of the Project Euclid page; OEIS A059753 | abstract: minimal degree d(m) of a {-1,0,1} polynomial with a zero of order m at 1, determined for m <= 10 (all extremal polynomials), m = 11, 12 among certain symmetric polynomials, examples for m <= 21. Cited in Section 3.2 beside BEK Thm 2.7 |
