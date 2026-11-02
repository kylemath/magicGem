# Magic Gems: Geometry, Moments, and Mechanics of Lifted Magic Squares

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta · `kyle.mathewson@ualberta.ca`)

## Interactive Web Applications & Studios

| Web Application | Live URL (GitHub Pages) | Repository Path | Description |
| :--- | :--- | :--- | :--- |
| **Paper C Interactive Mechanics Essay** | [kylemath.github.io/magicGem/](https://kylemath.github.io/magicGem/) | [`index.html`](index.html) | Interactive 2D/3D radial spoke balance, Dzhanibekov precession, nested cores, wireframes, nets & chiral towers |
| **3D Fabrication, STL & Papercraft Studio** | [kylemath.github.io/magicGem/3dModels/](https://kylemath.github.io/magicGem/3dModels/index.html) | [`3dModels/index.html`](3dModels/index.html) | All 880 order-4 Magic Gems: live STL, OpenSCAD (`.scad`), and foldable SVG papercraft generator |
| **880 Order-4 Crystal Gallery** | [kylemath.github.io/magicGem/web/explorer880/](https://kylemath.github.io/magicGem/web/explorer880/) · [(Mirror)](https://kylemath.github.io/MagicGemWebpage/) | [`web/explorer880/index.html`](web/explorer880/index.html) | Interactive 3D browser of all 880 Frenicle $4 \times 4$ Magic Gems |
| **Magic Gems Explorer & 4×4 Catalogue** | [kylemath.github.io/magicGem/web/app/](https://kylemath.github.io/magicGem/web/app/) · [(Mirror)](https://kylemath.github.io/magicGemWeb/) | [`web/app/index.html`](web/app/index.html) | Multi-tab Three.js & Plotly explorer for $n = 3, 4, 5$ magic squares and [`catalogue4x4.html`](web/app/catalogue4x4.html) |
| **Magic Square Physical Solver Suite** | [kylemath.github.io/magicGem/web/physicalSolver/](https://kylemath.github.io/magicGem/web/physicalSolver/) · [(Mirror)](https://kylemath.github.io/magicSquare_physicalSolver/) | [`web/physicalSolver/index.html`](web/physicalSolver/index.html) | Interactive Bubble Trinity, Energy Decomposition, Vector Physics & Physics Lab simulators |

---

## Overview

Placing an $n \times n$ magic square $S = (s_{ij})_{0 \le i,j < n}$ on the centered grid

$$x_j = j - \frac{n-1}{2}, \qquad y_i = \frac{n-1}{2} - i, \qquad z_{ij} = s_{ij} - \frac{n^2+1}{2}$$

lifts its $N = n^2$ entries into three-dimensional points $\mathbf{p}_{ij}(\lambda) = (x_j, y_i, \lambda z_{ij}) \in \mathbb{R}^3$. Their convex hull

$$\mathcal{G}_\lambda(S) := \operatorname{conv}\bigl\{\mathbf{p}_{ij}(\lambda) : 0 \le i,j < n\bigr\} \subset \mathbb{R}^3$$

is a polyhedral sculpture—the **Magic Gem** of $S$. This repository is the canonical monorepo containing the complete LaTeX manuscripts, figure-generation scripts, exact rational verification suites (`fractions.Fraction`), interactive web simulators, and historical research archives for the three-paper *Magic Gems* series:

| Paper | Title & Directory | Venues & Status | Compiled PDF | Exact Verification Suite |
| :--- | :--- | :--- | :--- | :--- |
| **Paper A** | *Magic Gems: Convex Hulls of Lifted Magic Squares* (`paper_A_gems/`) | `arXiv:2512.09170` · *Experimental Mathematics* (`263179413`) | [`paperA.pdf`](paperA.pdf) | `python3 paper_A_gems/anc/verify_paper_a.py` |
| **Paper B** | *Bivariate Polynomial Moments and Prouhet–Tarry–Escott Identities of Semi-Magic Squares* (`paper_B_orthogonality/`) | arXiv (`submit/8306568`) · *Discrete Applied Mathematics* | [`paperB.pdf`](paperB.pdf) | `python3 paper_B_orthogonality/anc/verify_paper_b.py` |
| **Paper C** | *Balance in Inequality: Testing the Physical Equilibrium, Precession, and Structural Stability of Magic Gems* (`paper_C_mechanics/`) | arXiv (`submit/8319388`) · *Journal of Mathematics and the Arts* (`263584067`) | [`paperC.pdf`](paperC.pdf) | `python3 paper_C_mechanics/anc/verify_paper_c.py` |

---

## Repository Structure

```text
magicGem/
├── paperA.pdf                        # Compiled Manuscript — Paper A (Convex Hulls & Face Lattices)
├── paperB.pdf                        # Compiled Manuscript — Paper B (Polynomial Moments & PTE Hierarchy)
├── paperC.pdf                        # Compiled Manuscript — Paper C (Mechanics, Fabrication & Stacking)
├── paperA_arxiv.tar.gz               # Self-contained arXiv upload archive for Paper A
├── paperB_arxiv.tar.gz               # Self-contained arXiv upload archive for Paper B
├── paperC_arxiv.tar.gz               # Self-contained arXiv upload archive for Paper C
├── index.html                        # Interactive Web Essay for Paper C (GitHub Pages root)
├── simulators.js                     # Interactive 2D/3D Physics, Wireframe, Papercraft & Tower Simulators
├── gems_data.js                      # Precomputed exact geometry & mechanics dataset for all 880 order-4 gems
├── 3dModels/                         # 880-Square 3D Fabrication, STL, OpenSCAD & Papercraft Studio
├── web/                              # Consolidated interactive web applications
│   ├── explorer880/                  # 880 Order-4 Crystal Gallery (consolidated from MagicGemWebpage)
│   ├── app/                          # Multi-tab Magic Gems Web App & 4x4 Catalogue (from magicGemWeb)
│   └── physicalSolver/               # Physical Solver, Bubble Trinity & Energy Lab (from magicSquare_physicalSolver)
├── paper_A_gems/                     # Paper A LaTeX sources, figures, and ancillary verification suite
├── paper_B_orthogonality/            # Paper B LaTeX sources, figures, and ancillary verification suite
├── paper_C_mechanics/                # Paper C LaTeX sources, figures, web essay, and verification suite
├── Analysis/                         # Shared computational scripts, Lean 4 proofs, and census datasets
└── archive/                          # Historical 2025 research archives (magicSquare, MagicGemNotes, pre-split drafts)
```

---

## Reproducing All Verification Suites & Figures

Every theorem, census count, and extremal example across Papers A, B, and C is certified in exact integer and rational arithmetic (`fractions.Fraction`):

```bash
# Install dependencies (NumPy, SciPy, Matplotlib)
pip install -r requirements.txt

# Verify Paper A (Convex Hulls, Face Lattices, All-Odd-n Siamese Hulls)
python3 paper_A_gems/anc/verify_paper_a.py

# Verify Paper B (Bivariate Polynomial Moments & Prouhet-Tarry-Escott Identities)
python3 paper_B_orthogonality/anc/verify_paper_b.py

# Verify Paper C (Radial Vector Laws, Precession, Nested Cores, Wireframes/Nets & Stacking)
python3 paper_C_mechanics/anc/verify_paper_c.py

# Regenerate all 7 publication figures for Paper C
python3 paper_C_mechanics/anc/make_figures_c.py
```

---

## License

MIT License
