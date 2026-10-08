# arXiv metadata, Paper B

**Title:** Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies

(Title changed from "Magic squares as orthogonality conditions on a height function": the main result is now the two-sided bound for the permutation threshold k*(n), and "height function" clashes with the established meaning of the term for tilings.)

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta)

**Primary category:** math.CO (Combinatorics)  **Cross-lists:** math.PR (Probability), math.NT (Number Theory)

**MSC 2020:** 05B20 (primary); 05A05, 11C08, 60C05, 60F05

**Comments:** 23 pages, 3 figures, 4 tables. Ancillary files (verification scripts, lattice enumeration, witness arrangements, symbolic variance derivation, figure scripts, C enumerator, independent recounts, a certificate for the lattice computations, data) in `anc/`. Companion paper: "Magic Gems: A Polyhedral Framework for Magic Squares" (arXiv:2512.09170).

**Abstract (plain text / TeX):**

An $n\times n$ arrangement of $1,\dots,n^2$ is semi-magic if all its row and column sums are equal. If they are, then $\sum_{i,j}s_{ij}j^m=M(n)\sum_jj^m$ and $\sum_{i,j}s_{ij}i^m=M(n)\sum_ii^m$ for every $m$; for real matrices the converse needs these moment identities up to $m=n-1$. For arrangements fewer suffice. Let the permutation threshold $k^*(n)$ be the least $k$ such that every arrangement satisfying them for $m=1,\dots,k$ is semi-magic. In terms of the column-sum deviations $\gamma$ these conditions say that $\sum_j\gamma_jt^j$ is divisible by $(t-1)^{k+1}$, which links $k^*(n)$ to the Prouhet--Tarry--Escott problem and to work of Borwein, Erd\'elyi and K\'os on integer polynomials with a zero of high order at $1$. We prove $(\sqrt2-o(1))\sqrt n\le k^*(n)\le\sqrt{\pi e\,(n-1)\log(n^4/4)}$; the lower bound uses semi-magic squares with many pairs of complementary rows and the pigeonhole principle. Explicit arrangements together with short proofs give $k^*(n)=n-1$ for $3\le n\le13$ and $k^*(n)=n-2$ for $14\le n\le17$, and we prove $k^*(n)\le n-3$ for all $n\ge18$; with computer assistance we determine $k^*(n)$ for all $n\le40$. We also treat uniformly random arrangements: specialising the classical variance formula for quadratic assignment statistics, we give the exact mean and variance of the sum of squared line-sum deviations and of a four-term energy $E_4$ formed from the first moments and the two diagonals, show that $E_4$ divided by its mean converges in distribution to $\mathrm{Exp}(1)$, give the mean and variance of Loly's moment-of-inertia invariant, and count the $14{,}639{,}440$ arrangements of order $4$ with $E_4=0$, of which $7{,}040$ are magic.

**Keywords:** magic squares, Prouhet--Tarry--Escott problem, polynomials with integer coefficients, permutation statistics, combinatorial central limit theorem, moment of inertia

**License suggestion:** CC BY 4.0 (author's choice).

**Package:** `paperB_arxiv.tar.gz` (flat TeX bundle: `main.tex`, `main.bbl`, `references.bib`, `sections/`, `figures/`, `anc/`). Builds with `pdflatex main; bibtex main; pdflatex main; pdflatex main` (basic TeX Live, no extra packages).

**Before upload (author):** check the date line (`\today`).

**Title (author decision pending):** a shorter alternative is "Moments of line sums of magic squares: a permutation threshold and random line-sum energies".
