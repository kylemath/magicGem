# arXiv metadata, Paper B

**Title:** Magic squares as orthogonality conditions on a height function

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta)

**Primary category:** math.CO (Combinatorics)  **Cross-list:** math.PR (Probability)

**MSC 2020:** 05B15 (primary); 60C05, 11B75

**Comments:** 25 pages, 4 figures, 5 tables. Ancillary files (verification scripts, figure scripts, C enumerator, data) in `anc/`. Companion paper: "Magic Gems: A Polyhedral Framework for Magic Squares".

**Abstract (plain text / TeX):**

Place the centred entries of an $n\times n$ magic square as a height function $z$ over the centred cell grid. The magic conditions are then the orthogonality of $z$ to a $2n$-dimensional space $W$ of centred line indicators. This viewpoint gives several exact results. (i) A moment hierarchy: orthogonality to $x^m,y^m$ for $m\le k$ is equivalent to equal row and column sums exactly when $k\ge n-1$ for real heights, whereas for permutations of $1,\dots,n^2$ integrality lowers the threshold to at most $n-2$ for every $n\ge14$. (ii) Balance of the signed mass $z$: $z\perp W$ forces every separable moment, including Loly's moment-of-inertia invariant, to vanish; for an arbitrary arrangement the centre-of-mass offset is bounded by the line-sum energy with a sharp constant; balance of unit vectors is not implied (exact values for the eight $3\times3$ squares). (iii) Exact mean and variance of the energy of a uniformly random arrangement, with a limit law. (iv) An exact single-swap formula, giving strict local minimality of every magic square and gaps $d^2m/n^4$. (v) The exact number 14,639,440 of $4\times4$ arrangements satisfying four low-order conditions, of which 7,040 are magic.

**Keywords:** magic squares, orthogonality, permutation statistics, moment of inertia, local search

**License suggestion:** CC BY 4.0 (author's choice).

**Package:** `paperB_arxiv.tar.gz` (flat TeX bundle: `main.tex`, `main.bbl`, `references.bib`, `sections/`, `figures/`, `anc/`). Builds with `pdflatex main; bibtex main; pdflatex main; pdflatex main` (basic TeX Live, no extra packages).

**Before upload (author):** replace the companion-paper reference in `references.bib` by the arXiv identifier once available; check the date line (`\today`).
