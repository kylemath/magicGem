# arXiv metadata, Paper B

**Title:** Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies

(Title changed from "Magic squares as orthogonality conditions on a height function": the main result is now the two-sided bound for the permutation threshold k*(n), and "height function" clashes with the established meaning of the term for tilings.)

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta)

**Primary category:** math.CO (Combinatorics)  **Cross-lists:** math.PR (Probability), math.NT (Number Theory)

**MSC 2020:** 05B20 (primary); 05A05, 11C08, 60C05, 60F05

**Comments:** 22 pages, 4 figures, 3 tables. Ancillary files (verification scripts, lattice enumeration, witness arrangements, symbolic variance derivation, figure scripts, C enumerator, data) in `anc/`. Companion paper: "Magic Gems: A Polyhedral Framework for Magic Squares" (arXiv:2512.09170).

**Abstract (plain text / TeX):**

We regard the centred entries of an $n\times n$ arrangement of $1,\dots,n^2$ as a function $z$ on the centred grid; the semi-magic and magic conditions say that $z$ is orthogonal to the centred row, column and diagonal indicators. Replacing the line indicators by the powers $x^m,y^m$ ($m\le k$) of the column and row coordinates gives the degree-$k$ moment conditions, which for real-valued $z$ are equivalent to equal row and column sums exactly when $k\ge n-1$. The permutation threshold $k^*(n)$ is the least $k$ for which the degree-$k$ conditions force every arrangement to be semi-magic. These conditions say that the column deviations are the coefficients of an integer polynomial divisible by $(t-1)^{k+1}$, which connects $k^*(n)$ with the Prouhet--Tarry--Escott problem and with the Littlewood-type problems of Borwein, Erd\'elyi and K\'os. We prove $(\sqrt2-o(1))\sqrt n\le k^*(n)\le\sqrt{\pi e\,(n-1)\log(n^4/4)}$, the lower bound by a box-principle construction inside semi-magic squares with many complementary pairs of rows, and we determine $k^*(n)$ for $n\le40$: $k^*(n)=n-1$ for $n\le13$, $k^*(n)=n-2$ for $14\le n\le17$, and $k^*(n)\le n-3$ for every $n\ge18$. For a uniformly random arrangement we prove an exact formula for the variance of a quadratic form with zero row sums in the centred entries. It gives closed forms for the mean and variance of the sum of squared line-sum deviations and of a four-term low-order energy; the latter, divided by its mean, converges in distribution to $\mathrm{Exp}(1)$. We also give the null distribution of Loly's moment-of-inertia invariant, and the exact number $14{,}639{,}440$ of $4\times4$ arrangements satisfying the four low-order conditions, of which $7{,}040$ are magic.

**Keywords:** magic squares, Prouhet--Tarry--Escott problem, polynomials with integer coefficients, permutation statistics, combinatorial central limit theorem, moment of inertia

**License suggestion:** CC BY 4.0 (author's choice).

**Package:** `paperB_arxiv.tar.gz` (flat TeX bundle: `main.tex`, `main.bbl`, `references.bib`, `sections/`, `figures/`, `anc/`). Builds with `pdflatex main; bibtex main; pdflatex main; pdflatex main` (basic TeX Live, no extra packages).

**Before upload (author):** check the date line (`\today`).
