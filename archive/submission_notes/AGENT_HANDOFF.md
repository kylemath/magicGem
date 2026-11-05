# Agent Handoff: Magic Gems Trilogy & Paper C Submission State

**Last Updated:** November 2, 2026 (`commit` on `main` & `split-papers-a-b`)
**Author:** Kyle Elliott Mathewson (`kyle.mathewson@ualberta.ca`, Faculty of Science, University of Alberta)
**Main Repository:** `https://github.com/kylemath/magicGem` (Live GitHub Pages: `https://kylemath.github.io/magicGem/`)
**Companion 3D Repository:** `https://github.com/kylemath/magicGemWeb` (`https://kylemath.github.io/magicGemWeb/3dModels/index.html`)

---

## 1. Trilogy Status Overview

1. **Paper A (`paper_A_gems/`):** *Magic Gems: Convex Hulls of Lifted Magic Squares*
   - **Status:** Submitted to *Experimental Mathematics* (Taylor & Francis) and live on arXiv (`2512.09170v2`).
   - **Compiled PDF & Tarball:** `paperA.pdf` (31 pages), `paperA_arxiv.tar.gz`.

2. **Paper B (`paper_B_orthogonality/`):** *Bivariate Polynomial Moments and Prouhet–Tarry–Escott Identities of Semi-Magic Squares*
   - **Status:** Submitted to *Discrete Applied Mathematics* (Elsevier) and arXiv.
   - **Compiled PDF & Tarball:** `paperB.pdf` (27 pages), `paperB_arxiv.tar.gz`.

3. **Paper C (`paper_C_mechanics/`):** *Balance in Inequality: Testing the Physical Equilibrium, Precession, and Structural Stability of Magic Gems*
   - **Status:** **Submitted & Resubmitted to *Journal of Mathematics and the Arts* (Taylor & Francis, Submission ID `263584067`, Nov 5, 2026) in Taylor & Francis Standard APA-7 reference style.**
   - **Compiled PDF:** `paperC.pdf` (and `paper_C_mechanics/main.pdf`, **23 pages**, 7 multi-panel figures, 5 tables, 0 LaTeX warnings, 0 overfull boxes, formatted in Taylor & Francis Standard APA-7 author-date citation and reference list style).
   - **arXiv & Journal Upload Packages:** `paperC_arxiv.tar.gz`, `paperC_arxiv.zip`, and `paperC_jma_source.zip` (also in `paper_C_mechanics/`), containing `main.tex`, `main.bbl`, `references.bib`, `sections/*.tex`, `figures/*.pdf`, and `anc/` (`verify_paper_c.py`, `make_figures_c.py`, `results_paper_c.json`, `squares880.txt`).
   - **Cover Letter:** `cover_letter_paperC.txt` (and `paper_C_mechanics/cover_letter_paperC.txt`).
   - **Submission Metadata & Suggested Editors/Referees:** `JOURNAL_SUBMISSION_PACKAGE.md` (Part 3) and `submit.html`.

---

## 2. Immediate Task for the Agent on This Machine: Submit Paper C to arXiv & TMAA

Use browser automation (Computer Use / Chrome DevTools MCP) to step through the two submissions for **Paper C** and pause at the final "Submit" button on each portal for the user's confirmation:

### Step A: Submit Paper C to arXiv (`https://arxiv.org/submit`)
1. Start a new submission at `https://arxiv.org/submit`.
2. **License:** `CC BY 4.0` (or `arXiv.org perpetual, non-exclusive license`).
3. **Primary Category:** `math.MG` (Metric Geometry).
4. **Cross-List Categories:** `math.CO` (Combinatorics) and `physics.class-ph` (Classical Physics).
5. **Upload File:** Upload `paperC_arxiv.tar.gz` from the repository root (`<repo>/paperC_arxiv.tar.gz`).
   - Mark `anc/verify_paper_c.py`, `anc/make_figures_c.py`, `anc/results_paper_c.json`, and `anc/squares880.txt` as ancillary files if not automatically placed in the `anc/` directory by arXiv's tar extractor.
   - Verify that arXiv's TeX compiler produces the 23-page PDF cleanly.
6. **Metadata Fields:**
   - **Title:** `Balance in Inequality: Testing the Physical Equilibrium, Precession, and Structural Stability of Magic Gems`
   - **Authors:** `Kyle Elliott Mathewson`
   - **Abstract (`1,895` chars, `< 1,920` limit):**
     ```tex
     A magic square is a combinatorial paradigm of balance in inequality: its $n^2$ entries $\{1,\dots,n^2\}$ are strictly distinct, yet every row, column, and main diagonal sums to the same constant $\mu_n=n(n^2+1)/2$. Lifting the centred grid cells into $\mathbb{R}^3$ as radial vectors $\mathbf{p}_{ij}(\lambda)=(x_j,y_i,\lambda z_{ij})$ and taking their convex hull---the Magic Gem $\mathcal{G}_\lambda(S)$---raises a central mechanical question: when does combinatorial line-sum equality suffice for physical equilibrium in three dimensions, and when a nonlinear physical realization breaks that balance, how can an opposing inequality restore it? We test this principle across all $880$ order-four magic squares across four progressive regimes. For radial spokes from the origin $O$, natural vector lengths balance identically, whereas trimming spokes to unit length breaks equilibrium on all $832$ non-associative squares in 3D and on every square in 2D, where the irrational ring-radius ratio $r_2/r_1=\sqrt{5}$ bounds the resultant below by the Pell convergent $9/4\approx\sqrt{5}$. By length--weight duality, balance is restored via positive tip weights $\mathbf{w}^*>\mathbf{0}$ on $S^2$ or power-law spoke scaling ($r^{\alpha^*}$ in 2D and cubic vertical vanishing $(\mathbf{V}_3)_z=0$ in 3D). In 3D rotation, equal point masses make every semi-magic square an axisymmetric top with spherical-top transition $\lambda_{\mathrm{iso}}=(n^2+1)^{-1/2}$, whereas entry masses $m_{ij}=s_{ij}$ expose the quadrupole $Q_{xy}=\sum z_{ij}x_jy_i$, triggering $180^\circ$ Dzhanibekov flips on $824$ squares. Passing to the uniform solid hull $\mathcal{G}_0(S)$ shifts the centroid off $O$ on $829$ squares; re-engaging the opposing inner core $\mathcal{G}_1(S)$ restores balance via two-density inclusions, nested wireframes, or the complete $K_{n^2}$ strut network, while all $880$ hulls unfold into non-overlapping nets with $f_0-1$ glue tabs. Finally, $\lambda=1/5$ stabilizes $74.5\%$ of all gem facets on a table, and alternating $\mathcal{G}_\lambda(S)$ with its mirror twin $\mathcal{G}_\lambda(r^2\overline{S})=-\mathcal{G}_\lambda(S)$ locks chiral blocks into a vertical tower.
     ```
   - **Comments:** `23 pages, 7 figures, 5 tables. Ancillary files include exact rational verification script (anc/verify_paper_c.py) and complete order-4 census archive (anc/results_paper_c.json). Interactive 3D visual essay and STL/papercraft studio at https://kylemath.github.io/magicGem/ and https://kylemath.github.io/magicGem/3dModels/index.html`
   - **MSC-class:** `52B10 (Primary); 05B15, 70E15, 00A66 (Secondary)`

---

### Step B: Submit Paper C to *Journal of Mathematics and the Arts* (`TMAA`)
1. Open `https://rp.tandfonline.com/submission/create?journalCode=TMAA`.
2. **Article Type:** Research Article / Original Article.
3. **Files to Upload:**
   - Main Manuscript PDF: `<repo>/paperC.pdf` (or upload the LaTeX source files from `paper_C_mechanics/` if preferred; Taylor & Francis supports format-free PDF initial submission).
   - Supplemental / Ancillary File: `<repo>/paperC_arxiv.tar.gz`.
   - Cover Letter: `<repo>/cover_letter_paperC.txt` (or paste into the cover letter box).
4. **Metadata Fields:**
   - **Title:** `Balance in Inequality: Testing the Physical Equilibrium, Precession, and Structural Stability of Magic Gems`
   - **Short Title / Running Head:** `Balance in Inequality: Mechanics of Magic Gems`
   - **Abstract:** Same as above (can also be copied with one click from `<repo>/submit.html`).
   - **Keywords:** `magic squares; convex polyhedra; Albrecht Durer; centre of mass; rigid-body precession; Dzhanibekov effect; polyhedral nets; mathematical sculpture`
   - **MSC 2020:** `52B10, 05B15, 70E15, 00A66`
   - **Open Access Option:** Select **Standard Subscription Track ($0 APC)** + Green OA on arXiv.
   - **Funding:** `Natural Sciences and Engineering Research Council of Canada (NSERC).`
   - **Competing Interests:** `The author reports there are no competing interests to declare.`
   - **Data Availability Statement:** `All exact rational verification scripts (anc/verify_paper_c.py), machine-readable census data (anc/results_paper_c.json), figure generation scripts, interactive browser physics simulators (web/index.html), and OpenSCAD / papercraft 3D model generators are openly available at https://github.com/kylemath/magicGem and https://kylemath.github.io/magicGem/3dModels/index.html.`
   - **Suggested Editors / Referees (if prompted):**
     - Editors: Prof. Joy Ko (`jko01@risd.edu`), Prof. Craig S. Kaplan (`csk@uwaterloo.ca`), Prof. Carlo H. Séquin (`sequin@cs.berkeley.edu`).
     - Referees: Prof. George W. Hart (`george@georgehart.com`), Prof. Joseph O'Rourke (`jorourke@smith.edu`), Prof. Henry Segerman (`segerman@math.okstate.edu`).

---

## 3. Interactive Web Ecosystem (Already Deployed & Verified)
- **Paper C Interactive Visual Essay:** `https://kylemath.github.io/magicGem/` (`index.html` & `simulators.js`)
- **3D Fabrication, STL & Papercraft Studio (All 880 Squares + Reference STLs + OpenSCAD):** `https://kylemath.github.io/magicGem/3dModels/index.html` (`3dModels/index.html`, `3dModels/studio.js`, `3dModels/squares880.js`, mirrored to `magicGemWeb`)
- **One-Click Submission Copy/Download Helper:** `https://kylemath.github.io/magicGem/submit.html` (`submit.html`)
