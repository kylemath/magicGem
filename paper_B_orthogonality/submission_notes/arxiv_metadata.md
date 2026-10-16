# arXiv metadata, Paper B

**Title:** Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies

(Title chosen by the author: broad to specific, from moments of magic squares to the line-sum conditions, the permutation threshold and the random energies.)

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta)

**Primary category:** math.CO (Combinatorics)  **Cross-lists:** math.PR (Probability), math.NT (Number Theory)

**MSC 2020:** 05B20 (primary); 05A05, 11C08, 60C05, 60F05

**Comments:** 27 pages, 3 figures, 4 tables. Ancillary files (verification scripts, lattice enumeration, witness arrangements, symbolic variance derivation, figure scripts, C enumerator, independent recounts, a certificate for the lattice computations, witnesses beyond n = 40, data) in `anc/`. Companion paper: "Magic Gems: A Polyhedral Framework for Magic Squares" (arXiv:2512.09170). Prepared with extensive use of AI tools (Anthropic's Claude); see the statement "Use of AI systems" at the end of the paper. Computer-assisted bounds come with a certificate checkable by a short script in anc/.

**Abstract (plain text / TeX):**

An $n\times n$ arrangement of $1,\dots,n^2$ is semi-magic if all its row and column sums are equal. If they are, then $\sum_{i,j}s_{ij}j^m=M(n)\sum_jj^m$ and $\sum_{i,j}s_{ij}i^m=M(n)\sum_ii^m$ for every $m$; for real matrices the converse needs these moment identities up to $m=n-1$. For arrangements of order $n\ge14$ fewer suffice. Let the permutation threshold $k^*(n)$ be the least $k$ such that every arrangement satisfying them for $m=1,\dots,k$ is semi-magic. In terms of the column-sum deviations $\gamma$ these conditions say that $\sum_j\gamma_jt^j$ is divisible by $(t-1)^{k+1}$, which links $k^*(n)$ to the Prouhet--Tarry--Escott problem and to integer polynomials with a zero of high order at $1$. For such polynomials Schur's bound on real zeros gives $k^*(n)\le\sqrt{2(n-1)\log(n^4/4)}$, which improves on the elementary $k^*(n)\le n-3$ from $n=30$ on. Our main result is the converse direction: realising suitable $\gamma$ by swaps in semi-magic squares with many pairs of complementary rows, we prove $k^*(n)\ge(\sqrt2-o(1))\sqrt n$, and $k^*(n)\ge(\sqrt6-o(1))\sqrt n$ when $4\mid n$. Witness arrangements together with short proofs give $k^*(n)=n-1$ for $3\le n\le13$ and $k^*(n)=n-2$ for $14\le n\le17$, and we prove $k^*(n)\le n-3$ for all $n\ge18$; for $18\le n\le40$ we determine $k^*(n)$ with computer assistance. We also treat uniformly random arrangements: specialising the classical variance formula for quadratic assignment statistics, we give the exact mean and variance of the sum of squared line-sum deviations and of a four-term energy $E_4$ formed from the first moments and the two diagonals, show that $E_4$ divided by its mean converges in distribution to $\mathrm{Exp}(1)$, give the mean and variance of Loly's moment-of-inertia invariant, and count the $14{,}639{,}440$ arrangements of order $4$ with $E_4=0$, of which $7{,}040$ are magic.

**Keywords:** magic squares, Prouhet--Tarry--Escott problem, polynomials with integer coefficients, permutation statistics, combinatorial central limit theorem, moment of inertia

**License suggestion:** CC BY 4.0 (author's choice).

**Package:** `paperB_arxiv.tar.gz` (flat TeX bundle: `main.tex`, `main.bbl`, `references.bib`, `sections/`, `figures/`, `anc/`). Builds with `pdflatex main; bibtex main; pdflatex main; pdflatex main` (basic TeX Live, no extra packages).

**Before upload (author):** check the date line (`\today`).

