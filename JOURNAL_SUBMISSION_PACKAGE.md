# Journal Submission Package: Paper A & Paper B

- **Author:** Kyle Elliott Mathewson
- **Affiliation:** Faculty of Science, University of Alberta, Edmonton, Alberta, Canada
- **Email:** `kyle.mathewson@ualberta.ca`
- **Repository:** `https://github.com/kylemath/magicGem`
- **Submission Strategy:** Split across two independent journals matched to each paper's exact mathematical discipline to maximize acceptance probability, avoid simultaneous-submission referee fatigue, and secure **100% $0 APC Open Access** for both manuscripts.

---

## Executive Decision: The Optimal Journal Pairing

1. **Paper A (*Magic Gems: Convex Hulls of Lifted Magic Squares*) $\rightarrow$ *Experimental Mathematics* (Taylor & Francis)**
   - **Submission Portal:** `https://rp.tandfonline.com/submission/create?journalCode=UEXM`
   - **Manuscript PDF to Upload:** `/Users/fulkanjou/magicGem/paperA.pdf` (31 pages, 8 figures, 7 tables; format-free initial submission)
   - **Ancillary Code Archive (Optional Supplemental File):** `/Users/fulkanjou/magicGem/paperA_arxiv.tar.gz`
   - **Why This Maximizes Acceptance:** *Experimental Mathematics* is the flagship journal specifically dedicated to papers where rigorous proof and systematic computer experimentation work together. The exhaustive 880-square census, the discovery of the first interior-vertex failure (`#191`) at $n=4$, the $10^5$ Monte Carlo baseline, and the exact all-odd-$n$ Siamese theorems are tailor-made for its editorial mission.

2. **Paper B (*Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies*) $\rightarrow$ *Discrete Applied Mathematics* (Elsevier)**
   - **Submission Portal:** `https://www.editorialmanager.com/dam/`
   - **Manuscript PDF to Upload:** `/Users/fulkanjou/magicGem/paperB.pdf` (27 pages, 3 figures, 4 tables; "Your Paper, Your Way" format-free initial submission)
   - **Ancillary Code Archive (Optional Supplemental File):** `/Users/fulkanjou/magicGem/paperB_arxiv.tar.gz`
   - **Why This Maximizes Acceptance:** Weighting acceptance odds heavily while maintaining a respected, high-visibility mainstream journal makes *Discrete Applied Mathematics* the ideal home for Paper B (with *Advances in Applied Mathematics* as the immediate backup). *Discrete Applied Mathematics* regularly publishes algebraic and combinatorial theorems on magic squares, permutation matrices, Latin squares, and Prouhet–Tarry–Escott identities without the "pure algebraic combinatorics gatekeeping" of narrower journals, and your `@ualberta.ca` affiliation automatically qualifies for **100% APC-free Gold Open Access** under the University of Alberta CRKN–Elsevier agreement.

---

## Part 1: Paper A Submission Kit (*Experimental Mathematics*)

### 1.1 Portal Metadata Checklist
- **Journal:** *Experimental Mathematics* (Taylor & Francis, Journal Code: `UEXM`)
- **Article Type:** Original Article / Research Article
- **Title:** `Magic Gems: Convex Hulls of Lifted Magic Squares`
- **Running Head (Short Title):** `Magic Gems: Lifted Magic Squares`
- **MSC 2020 Classifications:** `52B10` (Primary); `05B15`, `52B05`, `52B15`, `68R05` (Secondary)
- **Keywords:** `magic squares`, `3D lattice polytopes`, `convex hull`, `f-vector`, `Siamese method`, `point-group symmetry`, `computational census`
- **Data Availability Statement (for portal box):**
  > All data, exhaustive order-4 census scripts, exact rational hull verifiers, and figure generation routines are openly available at `https://github.com/kylemath/magicGem` and archived as ancillary files with the arXiv preprint (`arXiv:2512.09170`).
- **Disclosure / Conflict of Interest Statement:**
  > The author reports there are no competing interests to declare.
- **Funding Statement:**
  > Natural Sciences and Engineering Research Council of Canada (NSERC).

### 1.2 Editor & Suggested Referee Picks (Paper A)

#### Requested Handling Editors (*Experimental Mathematics*)
1. **Prof. Alexander M. Kasprzyk** (Editor-in-Chief, *Experimental Mathematics*; University of Nottingham — `a.m.kasprzyk@nottingham.ac.uk`)
   - *Rationale:* World leader in the computational classification, census analysis, and combinatorial geometry of 3D lattice polytopes.
2. **Prof. Sergei Tabachnikov** (Editorial Board, *Experimental Mathematics*; Pennsylvania State University — `tabachni@math.psu.edu`)
   - *Rationale:* Deep expertise in discrete and recreational-adjacent geometry, polygons/polyhedra, and experimental geometry.

#### Suggested Referees (if requested by the Taylor & Francis portal)
1. **Prof. Jesús A. De Loera** (Department of Mathematics, University of California, Davis — `deloera@math.ucdavis.edu`)
   - *Expertise:* Polyhedral combinatorics, lattice polytopes, and the Birkhoff / magic square polytopes.
2. **Prof. Matthias Beck** (Department of Mathematics, San Francisco State University — `mattbeck@sfsu.edu`)
   - *Expertise:* Discrete geometry of magic and semimagic squares, lattice point enumeration, and convex polytopes.
3. **Prof. Günter M. Ziegler** (Institute of Mathematics, Freie Universität Berlin — `ziegler@math.fu-berlin.de`)
   - *Expertise:* 3-polytopes, $f$-vectors, Steinitz realizations, and symmetric lattice polytopes.
4. **Prof. Nikolai Yu. Zolotykh** (Lobachevsky State University of Nizhni Novgorod — `nikolai.zolotykh@itmm.unn.ru`)
   - *Expertise:* Vertex survival and convex hulls of shallow polynomial lifts of grids (directly cited in Section 5).

### 1.3 Cover Letter for Paper A (`cover_letter_paperA.txt`)

```text
October 28, 2026

Professor Alexander M. Kasprzyk
Editor-in-Chief, Experimental Mathematics
Taylor & Francis

Dear Professor Kasprzyk,

Please find enclosed our manuscript titled "Magic Gems: Convex Hulls of Lifted Magic Squares" (31 pages, 8 figures, 7 tables), which I am submitting for consideration for publication in Experimental Mathematics.

Every classical magic square S of order n defines a three-dimensional lattice polytope—its "magic gem" G(S)—obtained by lifting each grid cell (i, j) to a height proportional to its entry on a shallow circular paraboloid and taking the convex hull in R^3. While the combinatorial and polyhedral theory of the space of all magic squares (such as the Birkhoff polytope and Ehrhart polynomials of magic-square cones) has been extensively studied, the intrinsic three-dimensional polyhedral geometry of an individual magic square under a spatial lift has remained largely unexplored.

This manuscript combines exact computer experimentation with structural proofs brought to light by the census data:

1. Point-cloud mechanics and order-3 uniqueness: We prove that the discrete line-sum constraints alone force the centroid of the lifted point cloud to lie at the origin and render its horizontal inertia isotropic for every n >= 3. At n = 3, the unique Lo Shu square yields a 9-vertex, 14-face simplicial polyhedron of volume 81 and point group C_{2v}.
2. Exhaustive order-4 census and breakdown of vertex survival: Evaluating all 880 Frenicle-distinct order-4 magic squares alongside a 10^5-trial random permutation baseline reveals that magic gems have significantly larger volume than random permutation hulls, yet narrow f-vector diversity (only 13 combinatorial f-vectors across 423 distinct hull volumes). Crucially, n = 4 is the exact threshold where complete vertex survival breaks down: 148 of the 880 squares lose at least one lifted grid cell to the interior of the hull, beginning with Frenicle square #191. We prove a general paraboloid-lift comparison lemma explaining this breakdown via an upper-concave / lower-convex sandwich inequality.
3. Exact all-odd-n theorems for the Siamese (De la Loubere) gem: Guided by computational experiments for odd orders up to n = 31, we prove unconditionally that for every odd n >= 3 the Siamese magic gem retains all n^2 vertices on its boundary, decomposes into a five-terrace piecewise-affine upper surface over a stepped lower cradle, and admits closed-form face counts (f_0 = n^2, f_1 = 3n^2 - n - 5, f_2 = 2n^2 - n - 3) and exact rational volume Vol(G(S_n)) = (n^2 - 1)(3n^4 - n^2 - 6) / (12 sqrt(2)) (Proposition 6.5 and Theorem 6.13).

In the spirit of Experimental Mathematics, every census table, counterexample, and theorem verification is accompanied by a self-contained, zero-dependency Python ancillary suite (available at https://github.com/kylemath/magicGem and archived on arXiv as arXiv:2512.09170).

For complete transparency, a separate companion preprint by the author (submitted to a discrete mathematics venue) investigates an independent algebraic and probabilistic problem—higher-degree polynomial moments of magic squares via the Prouhet-Tarry-Escott problem, a degree-3 permutation threshold, and characteristic-function integrals—whereas the present manuscript is entirely self-contained and focuses on the 3D polyhedral geometry, face lattices, and exhaustive census of lifted magic squares.

This manuscript is original, is my sole work, has not been published previously, and is not under consideration for publication elsewhere. Thank you very much for your time and consideration.

Sincerely,

Kyle Elliott Mathewson, Ph.D.
Associate Professor, Faculty of Science
University of Alberta
Edmonton, Alberta, Canada
Email: kyle.mathewson@ualberta.ca
```

---

## Part 2: Paper B Submission Kit (*Discrete Applied Mathematics*)

### 2.1 Portal Metadata Checklist
- **Journal:** *Discrete Applied Mathematics* (Elsevier, Portal: `https://www.editorialmanager.com/dam/`)
- **Article Type:** Full Length Article (`FLA`)
- **Section / Category (if prompted):** Enumerative and Algebraic Combinatorics / Matrices and Graphs
- **Title:** `Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies`
- **MSC 2020 Classifications:** `05B15` (Primary); `05A05`, `11D72`, `15B51`, `60C05` (Secondary)
- **Keywords:** `magic squares`, `permutation matrices`, `Frobenius inner product`, `Prouhet-Tarry-Escott problem`, `Vandermonde matrix`, `circular variance`, `random permutations`
- **Open Access Selection:** Choose **Gold Open Access** upon acceptance — covered **100% ($0 APC)** via the University of Alberta CRKN–Elsevier Read & Publish institutional agreement (verify using `kyle.mathewson@ualberta.ca`).
- **Declaration of Competing Interest:**
  > The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

### 2.2 Editor & Suggested Referee Picks (Paper B)

#### Requested Handling Editors (*Discrete Applied Mathematics* / Elsevier)
1. **Prof. Endre Boros** (Editor-in-Chief, *Discrete Applied Mathematics*; Rutgers University — `endre.boros@rutgers.edu`)
   - *Rationale:* Oversees discrete structures, algebraic combinatorics, and matrix/polyhedral problems with efficient editorial triage.
2. *(If submitting to the alternative Elsevier venue **Advances in Applied Mathematics** instead)*: **Prof. Catherine H. Yan** (Co-Editor-in-Chief, *Advances in Applied Mathematics*; Texas A&M University — `cyan@math.tamu.edu`), specialist in enumerative/algebraic combinatorics and discrete probability.

#### Suggested Referees (Elsevier Editorial Manager requires 3–4 suggested reviewers)
1. **Prof. Michael J. Mossinghoff** (Center for Communications Research, Princeton / Davidson College — `mjmossinghoff@ Davidson.edu` / `m.mossinghoff@alumni.stanford.org`)
   - *Expertise:* Co-author of the foundational Borwein–Mossinghoff (2000) paper on the Prouhet–Tarry–Escott problem directly extended in Section 3.
2. **Prof. Persi Diaconis** (Department of Statistics and Mathematics, Stanford University — `diaconis@math.stanford.edu`)
   - *Expertise:* Moments of random permutation matrices, Frobenius inner products on $S_n$, and magic/Latin square asymptotics.
3. **Prof. Ian M. Wanless** (School of Mathematics, Monash University — `ian.wanless@monash.edu`)
   - *Expertise:* Combinatorics of matrices, Latin squares, magic squares, and permanents/moments over the symmetric group.
4. **Prof. Richard A. Brualdi** (Department of Mathematics, University of Wisconsin–Madison — `brualdi@math.wisc.edu`)
   - *Expertise:* Combinatorial matrix theory, permutation matrices, and doubly stochastic / magic matrices.

### 2.3 Cover Letter for Paper B (`cover_letter_paperB.txt`)

```text
October 28, 2026

Professor Endre Boros
Editor-in-Chief, Discrete Applied Mathematics
Elsevier

Dear Professor Boros,

Please find enclosed my manuscript titled "Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies" (27 pages, 3 figures, 4 tables), which I am submitting for consideration for publication as a Full Length Article in Discrete Applied Mathematics.

A classical magic square S of order n satisfies linear row, column, and main-diagonal sum constraints. A natural algebraic question is to determine how tightly these first-order line-sum constraints govern higher-degree polynomial moments of the form <P, K^(r)>_F = sum_{i,j} S_{i,j}^r K_{i,j} across spatial kernels K on the n x n grid.

This manuscript establishes a complete hierarchy of exact and probabilistic results for these higher-degree moments:

1. Equivalence with the Prouhet-Tarry-Escott (PTE) problem and the r = 2 circular identity: We show that the vanishing of centered higher-degree moments against arbitrary rank-1 row/column kernels is equivalent to the classical Prouhet-Tarry-Escott problem on the rows and columns of S. At degree r = 2, although individual row and column second moments vary across magic squares, we prove that for every magic square of every order n >= 3 the squared projections along any two orthogonal directions on the centered circle sum to the universal constant (1/12) n^2 (n^2 - 1)^2 (Theorem 3.2), reducing the 2 x 2 second-moment matrix to a two-dimensional dipole space parametrized by all 880 order-4 squares.
2. A sharp degree-3 permutation threshold on S_n: Restricting from general n x n magic squares to n x n permutation matrices P in S_n against the radial kernel R_{i,j} = (i - c)^2 + (j - c)^2, we prove via Vandermonde linear independence that the Frobenius inner product <P, R^r>_F is constant across all n! permutation matrices for every integer degree 0 <= r <= 3 (Proposition 4.1), with closed-form universal constants for all n, and fails to be invariant precisely at degree r = 4 as soon as n >= 3 (Theorem 4.3).
3. Continuous energy density for random assignments: Replacing grid-locked permutations with independent standard normal weights produces a continuous quadratic energy W_n whose probability density is expressed as a single convergent Fourier-Gil-Pelaez integral of the exact characteristic function, capturing the empirical order-n = 4 permutation spectrum within 3.6% and converging to N(0, 1) at rate O(n^{-1}).

For complete transparency, this manuscript is algebraically and probabilistically self-contained; a separate geometric preprint by the author (arXiv:2512.09170, submitted to an experimental geometry venue) investigates the three-dimensional convex hulls and face lattices of lifted magic squares, where only the elementary r = 1 centroid identity appears. There is no overlap in theorems, proofs, or figures between the two manuscripts. All verification scripts are publicly available at https://github.com/kylemath/magicGem.

This manuscript is original, is my sole work, has not been published previously, and is not under consideration for publication elsewhere. Thank you very much for considering this submission for Discrete Applied Mathematics.

Sincerely,

Kyle Elliott Mathewson, Ph.D.
Associate Professor, Faculty of Science
University of Alberta
Edmonton, Alberta, Canada
Email: kyle.mathewson@ualberta.ca
```


---

## Part 3: Paper C Submission Kit (*Journal of Mathematics and the Arts*)

### 3.1 Portal Metadata Checklist
- **Journal:** *Journal of Mathematics and the Arts* (Taylor & Francis, Journal Code: `TMAA`, Portal: `https://rp.tandfonline.com/submission/create?journalCode=TMAA`)
- **Article Type:** Research Article / Original Article
- **Title:** `Mechanics and Balance of Magic Gems: Radial Vector Laws, Symmetric-Top Precession, Nested Core Inclusions, and Mirror-Twin Towers`
- **Running Head (Short Title):** `Mechanics and Balance of Magic Gems`
- **Manuscript PDF to Upload:** `/Users/fulkanjou/magicGem/paperC.pdf` (28 pages, 7 figures, 5 tables)
- **Ancillary / Supplemental Archive:** `/Users/fulkanjou/magicGem/paperC_arxiv.tar.gz`
- **Interactive Companion & 3D Fabrication Gallery:** `https://github.com/kylemath/magicGem` and `https://kylemath.github.io/magicGemWeb/3dModels/index.html`
- **MSC 2020 Classifications:** `52B10` (Primary); `00A66`, `05B15`, `52B15`, `70E15`, `11J70` (Secondary)
- **Keywords:** `magic squares`, `polyhedral sculpture`, `3D printing and papercraft unfolding`, `Durer Melencolia I`, `rigid-body mechanics`, `convex layers`, `wireframe strut networks`
- **Open Access Selection:** Choose **Standard Subscription Track ($0 cost)** + Green Open Access on arXiv (`paperC_arxiv.tar.gz`) and `magicGemWeb` *(Note: UAlberta CRKN provides a 25% APC discount if optional Open Select Gold OA is chosen, whereas the subscription + arXiv Green OA route is 100% free at $0).*
- **Data Availability Statement (for portal box):**
  > All exact rational verification scripts (`anc/verify_paper_c.py`), machine-readable census data (`anc/results_paper_c.json`), figure generation scripts, interactive browser physics simulators (`web/index.html`), and OpenSCAD / papercraft 3D model generators are openly available at `https://github.com/kylemath/magicGem` and `https://github.com/kylemath/magicGemWeb`.
- **Disclosure / Conflict of Interest Statement:**
  > The author reports there are no competing interests to declare.
- **Funding Statement:**
  > Natural Sciences and Engineering Research Council of Canada (NSERC).

### 3.2 Editor & Suggested Referee Picks (Paper C)

#### Requested Handling Editors (*Journal of Mathematics and the Arts*)
1. **Prof. Joy Ko** (Editor-in-Chief, *Journal of Mathematics and the Arts*; Rhode Island School of Design — `jko01@risd.edu`)
   - *Rationale:* Leads JMA's mission bridging rigorous geometry, physical fabrication, folded nets, and mathematical art.
2. **Prof. Craig S. Kaplan** (Editorial Board & Former Editor-in-Chief, *Journal of Mathematics and the Arts*; University of Waterloo — `csk@uwaterloo.ca`)
   - *Rationale:* World authority on computational geometry, polyhedral design, symmetry, and ornamental/sculptural structures.
3. **Prof. Carlo H. Séquin** (Editorial Board, *Journal of Mathematics and the Arts*; University of California, Berkeley — `sequin@cs.berkeley.edu`)
   - *Rationale:* Pioneer in 3D-printed polyhedral sculptures, wireframe strut architectures, and geometric modeling.

#### Suggested Referees (if requested by the Taylor & Francis portal)
1. **Prof. George W. Hart** (Stony Brook University — `george@georgehart.com`)
   - *Expertise:* Polyhedral sculpture, 3D-printed wireframe and strut geometry, nested polyhedra, and mathematical art.
2. **Prof. Joseph O'Rourke** (Department of Computer Science and Mathematics, Smith College — `jorourke@smith.edu`)
   - *Expertise:* Co-author of *Geometric Folding Algorithms* (2007); leading authority on Dürer's problem, Shephard's conjecture, and non-overlapping polyhedral net unfoldings (directly cited in Section 4.4).
3. **Prof. Erik D. Demaine** (CSAIL, Massachusetts Institute of Technology — `edemaine@mit.edu`)
   - *Expertise:* Polyhedral folding/unfolding, discrete geometry, and physical mathematical sculptures.
4. **Prof. Peter D. Loly** (Department of Physics and Astronomy, University of Manitoba — `loly@cc.umanitoba.ca`)
   - *Expertise:* Author of the foundational papers on the moments of inertia and mechanics of magic squares (directly extended into 3D in Sections 2 and 3).

### 3.3 Cover Letter for Paper C (`cover_letter_paperC.txt`)
Saved at `/Users/fulkanjou/magicGem/paper_C_mechanics/cover_letter_paperC.txt` and `/Users/fulkanjou/magicGem/cover_letter_paperC.txt`.
