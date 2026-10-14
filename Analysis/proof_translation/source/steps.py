# Step content for the proof translation page: Theorem 3.7(a) of Paper B.
# Each step: id, part, title, lean (file stem in Proofs/), tex, py, en (HTML), demo (JS demo id).

STEPS = [
dict(id="S0", part="Setup", title="The objects", lean="S0_Defs", demo="grid",
tex=r"""
An \emph{arrangement} of order $n$ fills the $n\times n$ grid with $1,\dots,N$, $N=n^2$, each once.
The magic constant is $M(n)=\tfrac{n(N+1)}{2}$.
The \emph{column deviations} are
$$\gamma_j=\sum_{i}s_{ij}-M(n),\qquad 0\le j\le n-1,$$
and $P_\gamma(t)=\sum_{j=0}^{n-1}\gamma_j t^j$.
$S$ satisfies the \emph{degree-$k$ conditions} if $\sum_{i,j}z_{ij}x_j^m=\sum_{i,j}z_{ij}y_i^m=0$ for $1\le m\le k$,
where $z_{ij}=s_{ij}-\tfrac{N+1}2$ and $x_j=j-\tfrac{n-1}2$.
$k^*(n)$ is the least $k$ such that the degree-$k$ conditions force all row and column sums to equal $M(n)$.
""",
py='''N = n * n
M = n * (N + 1) // 2

def column_deviations(S):          # S is an n x n list of rows
    return [sum(S[i][j] for i in range(n)) - M for j in range(n)]

def P(gamma, t):                    # P_gamma(t) = sum_j gamma_j t^j
    return sum(g * t**j for j, g in enumerate(gamma))

def degree_k_conditions(S, k):
    z = [[S[i][j] - (N + 1) / 2 for j in range(n)] for i in range(n)]
    x = [j - (n - 1) / 2 for j in range(n)]
    return all(sum(z[i][j] * x[j]**m for i in range(n) for j in range(n)) == 0
               and sum(z[i][j] * x[i]**m for i in range(n) for j in range(n)) == 0
               for m in range(1, k + 1))''',
en="""<p>An arrangement is any way of writing 1 to n² into the grid. It is <em>semi-magic</em> when every row and every column adds up to the same number M(n).</p>
<p>The column deviations γ record how far each column sum misses M(n). They always add up to 0, because the total of all entries is fixed. Semi-magic (for columns) means γ = 0.</p>
<p>The degree-k conditions are weaker tests: instead of checking every column sum, they check k weighted averages ("moments"). The question of the theorem is how many such moments you need before they force γ = 0 for every arrangement. That number is k*(n).</p>"""),

dict(id="S1a", part="Lemma 3.1: polynomial form", title="Column functions only see column sums", lean="S1a", demo="colfun",
tex=r"""
If $\varphi$ depends only on the column index, then
$$\sum_{i,j}\varphi(j)\,z_{ij}=\sum_j\varphi(j)\sum_i z_{ij}=\sum_j\varphi(j)\,\gamma_j .$$
""",
py='''def lhs(phi, z):   # sum over all n^2 cells
    return sum(phi[j] * z[i][j] for i in range(n) for j in range(n))

def rhs(phi, gamma):   # sum over the n columns only
    return sum(phi[j] * gamma[j] for j in range(n))

# lhs(phi, z) == rhs(phi, column_deviations(S)) for every phi''',
en="""<p>Swap the order of summation: first add down each column, then across. Since φ is the same for every cell in a column, it factors out of the column sum.</p>
<p>So any test that weights cells by their column alone (like x<sup>m</sup>) only sees the n numbers γ<sub>0</sub>,…,γ<sub>n−1</sub>, not the full arrangement. This is why the whole problem reduces to integer vectors γ.</p>"""),

dict(id="S1b", part="Lemma 3.1: polynomial form", title="Powers and binomials span the same space", lean="S1b", demo="basis",
tex=r"""
For $0\le m\le k$ the functions $j\mapsto x_j^m$ and $j\mapsto\binom{j}{m}$ are both bases of the polynomials of degree $\le k$ in $j$. Hence
$$\Bigl(\textstyle\sum_j x_j^m\gamma_j=0\ \ \forall m\le k\Bigr)\iff\Bigl(\textstyle\sum_j\binom{j}{r}\gamma_j=0\ \ \forall r\le k\Bigr).$$
""",
py='''from math import comb

def power_moments(gamma, k):
    return [sum((j - (n - 1) / 2)**m * g for j, g in enumerate(gamma)) for m in range(k + 1)]

def binomial_moments(gamma, k):
    return [sum(comb(j, r) * g for j, g in enumerate(gamma)) for r in range(k + 1)]

# The two lists are related by an invertible (triangular) change of basis,
# so one is all zero exactly when the other is.''',
en="""<p>Both families are "polynomials in the column index j of degree at most k". Any polynomial of degree ≤ k can be written in either family, so each power x<sup>m</sup> is a combination of the binomials C(j, r) with r ≤ m, and the other way round.</p>
<p>If all binomial moments vanish, every combination of them vanishes too, including each power moment; and conversely. The binomial version is the one that connects to polynomials in the next step.</p>"""),

dict(id="S1c", part="Lemma 3.1: polynomial form", title="Binomial moments are Taylor coefficients at t = 1", lean="S1c", demo="taylor",
tex=r"""
$$P_\gamma(t)=\sum_{r\ge0}B_r\,(t-1)^r,\qquad B_r=\sum_j\binom{j}{r}\gamma_j ,$$
because $t^j=(1+(t-1))^j=\sum_r\binom jr(t-1)^r$. Hence
$$B_0=\dots=B_k=0\iff (t-1)^{k+1}\mid P_\gamma(t).$$
So $S$ satisfies the degree-$k$ conditions iff $(t-1)^{k+1}$ divides $P_\gamma$ and $P_\rho$.
""",
py='''def taylor_at_1(gamma):
    # B_r = sum_j C(j, r) gamma_j are the coefficients of P in powers of (t - 1)
    return [sum(comb(j, r) * g for j, g in enumerate(gamma)) for r in range(len(gamma))]

def order_of_vanishing_at_1(gamma):
    B = taylor_at_1(gamma)
    K = 0
    while K < len(B) and B[K] == 0:
        K += 1
    return K          # (t-1)^K divides P_gamma, (t-1)^(K+1) does not''',
en="""<p>Expand each t<sup>j</sup> around t = 1 with the binomial theorem. Collecting terms, the coefficient of (t−1)<sup>r</sup> is exactly the binomial moment B<sub>r</sub>.</p>
<p>A polynomial is divisible by (t−1)<sup>k+1</sup> exactly when its first k+1 Taylor coefficients at 1 are zero. So "the degree-k conditions hold" becomes "P<sub>γ</sub> has a zero of order at least k+1 at t = 1". The rest of the proof bounds how high that order can be.</p>"""),

dict(id="S2a", part="Lemma 3.8: size of γ", title="Any p columns deviate by at most pn(N−pn)/2", lean="S2a", demo="major",
tex=r"""
The $pn$ cells in a set $J$ of $p$ columns hold distinct values, so their sum is at most the sum of the $pn$ largest values:
$$\sum_{j\in J}\sum_i s_{ij}\le \frac{pn(2N-pn+1)}{2}.$$
Subtracting $pM(n)=\tfrac{pn(N+1)}{2}$:
$$\Bigl|\sum_{j\in J}\gamma_j\Bigr|\le\frac{pn(N-pn)}{2}.$$
(The lower bound uses the $pn$ smallest values.)
""",
py='''def max_sum_of_m_distinct(m, N):     # N + (N-1) + ... + (N-m+1)
    return m * (2 * N - m + 1) // 2

def bound(p):
    return p * n * (N - p * n) / 2

# for every set J of p columns:
#   abs(sum(gamma[j] for j in J)) <= bound(p)''',
en="""<p>Columns can only be heavy by holding big numbers, and there are only so many big numbers. The best a set of p columns can do is hold the pn largest values N, N−1, …</p>
<p>Subtract what those columns would hold in a semi-magic square, p·M(n), and you get the most they can exceed it. The same argument with the smallest values bounds how far below they can fall.</p>"""),

dict(id="S2b", part="Lemma 3.8: size of γ", title="So ‖γ‖₁ ≤ N²/4 = n⁴/4", lean="S2b", demo="l1",
tex=r"""
Let $J$ be the set of columns with $\gamma_j>0$, $p=|J|$. Since $\sum_j\gamma_j=0$,
$$\|\gamma\|_1=2\sum_{j\in J}\gamma_j\le pn(N-pn)\le\frac{N^2}{4},$$
the last step by $ab\le\bigl(\tfrac{a+b}2\bigr)^2$ with $a=pn$, $b=N-pn$.
""",
py='''L = sum(abs(g) for g in gamma)
p = sum(1 for g in gamma if g > 0)
assert L == 2 * sum(g for g in gamma if g > 0)   # because sum(gamma) == 0
assert L <= p * n * (N - p * n) <= N * N / 4''',
en="""<p>Because the deviations add to zero, the positive ones and the negative ones have the same total, so the total size ‖γ‖₁ is twice the positive part.</p>
<p>The positive part is a sum over some p columns, which step S2a bounds. The product pn·(N−pn) is largest when the two factors are equal, giving N²/4. This single number, n⁴/4, is all the proof needs to know about arrangements.</p>"""),

dict(id="S3a", part="Lemma 3.9: order of vanishing", title="Integer polynomials have ∫ log|P| ≥ 0 on the circle", lean="S3a", demo="mahler",
tex=r"""
For nonzero $P\in\mathbb Z[t]$ with leading coefficient $a$ and roots $\alpha$, the Mahler measure is
$\mathcal M(P)=|a|\prod_\alpha\max(1,|\alpha|)\ge1$, and Jensen's formula gives
$$\log\mathcal M(P)=\int_{-1/2}^{1/2}\log\bigl|P(e^{2\pi i\theta})\bigr|\,d\theta .$$
Hence $\displaystyle\int_{-1/2}^{1/2}\log|P(e^{2\pi i\theta})|\,d\theta\ge0$.
""",
py='''import numpy as np

def mahler_measure(gamma):
    coeffs = np.trim_zeros(gamma, 'b')            # drop zero top coefficients
    roots = np.roots(coeffs[::-1])                # numpy wants highest degree first
    return abs(coeffs[-1]) * np.prod([max(1, abs(a)) for a in roots])

def mean_log_on_circle(gamma, samples=100000):
    theta = (np.arange(samples) + 0.5) / samples - 0.5
    z = np.exp(2j * np.pi * theta)
    return np.mean(np.log(abs(np.polyval(gamma[::-1], z))))

# mahler_measure(gamma) >= 1  and  mean_log_on_circle(gamma) == log(mahler_measure(gamma)) >= 0''',
en="""<p>This is the one deep input. An integer polynomial cannot be small all the way around the unit circle: on average (in the logarithmic sense) |P| is at least 1.</p>
<p>The reason: the average of log|P| on the circle equals log of the leading coefficient times the roots outside the circle (Jensen's formula), and the leading coefficient of an integer polynomial is at least 1 in size. The next steps show that a high-order zero at t = 1 would force |P| to be tiny on a large part of the circle, contradicting this.</p>"""),

dict(id="S3b", part="Lemma 3.9: order of vanishing", title="On the circle, |P(z)| ≤ L", lean="S3b", demo="circle",
tex=r"""
For $|z|=1$,
$$|P(z)|=\Bigl|\sum_j\gamma_jz^j\Bigr|\le\sum_j|\gamma_j|=\|\gamma\|_1=L .$$
""",
py='''L = sum(abs(g) for g in gamma)
# triangle inequality, |z^j| = 1 on the circle:
# abs(P(gamma, z)) <= L  for all z with abs(z) == 1''',
en="""<p>The triangle inequality: each term γ<sub>j</sub>z<sup>j</sup> has size |γ<sub>j</sub>| on the unit circle, so the sum has size at most the sum of the sizes.</p>
<p>This is the crude bound used away from t = 1. Near t = 1 the next step does much better.</p>"""),

dict(id="S3c", part="Lemma 3.9: order of vanishing", title="Near t = 1, a K-fold zero makes P tiny", lean="S3c", demo="near1",
tex=r"""
If $(t-1)^K\mid P$, Taylor's formula with integral remainder along $[1,z]$ gives, for $|z|\le1$,
$$|P(z)|\le\frac{|z-1|^K}{K!}\max_{|w|\le1}|P^{(K)}(w)|\le L\binom{n-1}{K}|z-1|^K,$$
since $|P^{(K)}(w)|\le\sum_j|\gamma_j|\,j(j-1)\cdots(j-K+1)\le L\,(n-1)\cdots(n-K)$.
""",
py='''from math import comb

def near_one_bound(gamma, K, z):
    n = len(gamma)
    L = sum(abs(g) for g in gamma)
    return L * comb(n - 1, K) * abs(z - 1)**K

# if order_of_vanishing_at_1(gamma) >= K:
#   abs(P(gamma, z)) <= near_one_bound(gamma, K, z) for all abs(z) <= 1''',
en="""<p>A polynomial with a K-fold zero at 1 starts like c·(z−1)<sup>K</sup>, so close to 1 it is very small. Taylor's theorem makes this exact: the size is at most |z−1|<sup>K</sup>/K! times the largest K-th derivative.</p>
<p>The K-th derivative of t<sup>j</sup> is at most j(j−1)…(j−K+1) on the disc, and j ≤ n−1, which gives L·C(n−1, K). The bigger K is, the faster the bound shrinks near 1.</p>"""),

dict(id="S3d", part="Lemma 3.9: order of vanishing", title="C(n−1, K) ≤ (e(n−1)/K)^K", lean="S3d", demo="binom",
tex=r"""
$$\binom{n-1}{K}\le\frac{(n-1)^K}{K!}\le\Bigl(\frac{e(n-1)}{K}\Bigr)^K,$$
using $K!\ge(K/e)^K$, which follows from $e^K=\sum_m K^m/m!\ge K^K/K!$.
""",
py='''from math import comb, e

def check(n, K):
    return comb(n - 1, K) <= (e * (n - 1) / K)**K''',
en="""<p>A standard estimate: choosing K things from n−1 is at most (n−1)<sup>K</sup>/K!, and K! is at least (K/e)<sup>K</sup> because one term of the series for e<sup>K</sup> is K<sup>K</sup>/K!.</p>
<p>Combined with S3c this gives |P(z)| ≤ L·(e(n−1)|z−1|/K)<sup>K</sup>: below 1 times L as soon as |z−1| < K/(e(n−1)).</p>"""),

dict(id="S3e", part="Lemma 3.9: order of vanishing", title="Chord ≤ arc: |e^{2πiθ} − 1| ≤ 2π|θ|", lean="S3e", demo="chord",
tex=r"""
$$|e^{2\pi i\theta}-1|=2|\sin\pi\theta|\le2\pi|\theta| .$$
With $\beta=\dfrac{2\pi e(n-1)}{K}$, steps S3b–S3d give, for $z=e^{2\pi i\theta}$,
$$\log|P(z)|\le\log L+K\log\min(1,\beta|\theta|).$$
""",
py='''from math import sin, pi, log, e

def log_bound(theta, L, n, K):
    beta = 2 * pi * e * (n - 1) / K
    return log(L) + K * log(min(1, beta * abs(theta)))''',
en="""<p>The straight-line distance from 1 to a point on the circle is shorter than the arc to it, which is 2π|θ|. Plugging that into S3d turns the bound into a function of the angle alone.</p>
<p>Take the better of the two bounds (S3b far from 1, S3c–S3d near 1): log|P| ≤ log L + K·log min(1, β|θ|). The min is 1 (so log is 0) away from 1, and negative near θ = 0.</p>"""),

dict(id="S3f", part="Lemma 3.9: order of vanishing", title="∫ log min(1, β|θ|) dθ = −2/β", lean="S3f", demo="integral",
tex=r"""
For $\beta\ge2$,
$$\int_{-1/2}^{1/2}\log\min(1,\beta|\theta|)\,d\theta=2\int_0^{1/\beta}\log(\beta\theta)\,d\theta=\frac2\beta\int_0^1\log u\,du=-\frac2\beta .$$
Here $\beta=2\pi e(n-1)/K\ge2\pi e>2$ because $K\le n-1$.
""",
py='''from math import log

def integral(beta, steps=10**6):
    h = 1 / steps
    return sum(log(min(1, beta * abs(-0.5 + (i + 0.5) * h))) for i in range(steps)) * h

# integral(beta) is approximately -2 / beta''',
en="""<p>The function is 0 except on the small window |θ| &lt; 1/β, where it is log(β|θ|). Substituting u = βθ turns that window into the interval [0, 1], and ∫₀¹ log u du = −1.</p>
<p>So the dip near θ = 0 has area exactly 2/β. We need β ≥ 2 so that the window fits inside [−1/2, 1/2]; it does because K ≤ n−1.</p>"""),

dict(id="S3g", part="Lemma 3.9: order of vanishing", title="Combine: K² ≤ πe(n−1) log L", lean="S3g", demo="combine",
tex=r"""
Integrating the bound of S3e over $\theta$ and using S3a and S3f:
$$0\le\int_{-1/2}^{1/2}\log|P(e^{2\pi i\theta})|\,d\theta\le\log L-\frac{2K}{\beta}=\log L-\frac{K^2}{\pi e(n-1)} .$$
Hence $K^2\le\pi e\,(n-1)\log\|\gamma\|_1$.
""",
py='''from math import pi, e, log

def lemma_holds(gamma):
    n = len(gamma)
    K = order_of_vanishing_at_1(gamma)
    L = sum(abs(g) for g in gamma)
    return K * K <= pi * e * (n - 1) * log(L)''',
en="""<p>Average the bound from S3e around the circle. The constant log L averages to log L, and the dip contributes K·(−2/β). By S3a the true average is at least 0.</p>
<p>So 0 ≤ log L − 2K/β, and 2K/β = K²/(πe(n−1)). A high-order zero at 1 costs a lot of "size": K can only be about √(n log L).</p>"""),

dict(id="S4a", part="Theorem 3.7(a)", title="The upper bound on k*(n)", lean="S4a", demo="theorem",
tex=r"""
Let $S$ satisfy the degree-$k$ conditions with $(k+1)^2>\pi e(n-1)\log(n^4/4)$.
If $\gamma\ne0$: $(t-1)^{k+1}\mid P_\gamma$ (S1c) and $\|\gamma\|_1\le n^4/4$ (S2b), so by S3g
$$(k+1)^2\le\pi e(n-1)\log\|\gamma\|_1\le\pi e(n-1)\log(n^4/4),$$
a contradiction. So $\gamma=0$; likewise $\rho=0$. Therefore
$$k^*(n)\le\Bigl\lfloor\sqrt{\pi e(n-1)\log(n^4/4)}\Bigr\rfloor .$$
""",
py='''from math import pi, e, log, sqrt, floor

def upper_bound(n):
    return floor(sqrt(pi * e * (n - 1) * log(n**4 / 4)))

# any arrangement satisfying the degree-k conditions with k >= upper_bound(n)
# has (k+1)^2 > pi*e*(n-1)*log(n^4/4), hence gamma == rho == 0: it is semi-magic''',
en="""<p>Put the pieces together. If an arrangement passes the degree-k test but is not semi-magic, then its γ (or ρ) is a nonzero integer vector with a zero of order k+1 at t = 1 (S1c) and size at most n⁴/4 (S2b). The lemma (S3g) says such a zero can have order at most √(πe(n−1)log(n⁴/4)).</p>
<p>So once k+1 exceeds that, no counterexample exists, and the degree-k test already forces semi-magic. That is the upper bound.</p>"""),

dict(id="S4b", part="Theorem 3.7(a)", title="Simplify: ≤ 2√(πe)·√(n log n)", lean="S4b", demo="simplify",
tex=r"""
For $n\ge3$, $(n-1)\log(n^4/4)<n\cdot4\log n$, so
$$k^*(n)\le\sqrt{\pi e(n-1)\log(n^4/4)}<2\sqrt{\pi e}\,\sqrt{n\log n}\approx5.84\sqrt{n\log n}.$$
""",
py='''from math import pi, e, log, sqrt

for n in range(3, 10**4):
    assert (n - 1) * log(n**4 / 4) < 4 * n * log(n)''',
en="""<p>A cleanup step: log(n⁴/4) = 4 log n − log 4 is less than 4 log n, and n−1 is less than n. So the bound grows like √(n log n).</p>
<p>The bound is far from tight for small n (k*(n) ≤ n−1 is better until n ≈ 166) but it shows k*(n) grows much more slowly than n.</p>"""),
]
