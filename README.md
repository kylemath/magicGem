# Magic Gems: Geometry, Moments, and Mechanics of Lifted Magic Squares

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta · `kyle.mathewson@ualberta.ca`)

- **Interactive Mechanics & Physics Web Essay (Paper C Companion):** [https://kylemath.github.io/magicGem/](https://kylemath.github.io/magicGem/)
- **Interactive 3D Crystal Explorer (All 880 Order-4 Gems):** [https://kylemath.github.io/MagicGemWebpage/](https://kylemath.github.io/MagicGemWebpage/)
- **3D-Printable OpenSCAD/STL Models & Printable Papercraft Nets:** [https://github.com/kylemath/magicGemWeb](https://github.com/kylemath/magicGemWeb) · [3D & Papercraft Gallery](https://kylemath.github.io/magicGemWeb/3dModels/index.html)

---

## Overview

Placing an $n \times n$ magic square $S = (s_{ij})_{0 \le i,j < n}$ on the centered grid

$$x_j = j - \frac{n-1}{2}, \qquad y_i = \frac{n-1}{2} - i, \qquad z_{ij} = s_{ij} - \frac{n^2+1}{2}$$

lifts its $N = n^2$ entries into three-dimensional points $\mathbf{p}_{ij}(\lambda) = (x_j, y_i, \lambda z_{ij}) \in \mathbb{R}^3$. Their convex hull

$$\mathcal{G}_\lambda(S) := \operatorname{conv}\bigl\{\mathbf{p}_{ij}(\lambda) : 0 \le i,j < n\bigr\} \subset \mathbb{R}^3$$

is a polyhedral sculpture—the **Magic Gem** of $S$. This repository contains the complete LaTeX manuscripts, figure-generation scripts, exact rational verification suites (`fractions.Fraction`), and interactive web simulators for the three-paper *Magic Gems* series:

| Paper | Title & Directory | Compiled PDF | Exact Verification Suite |
| :--- | :--- | :--- | :--- |
| **Paper A** | *Magic Gems: Convex Hulls of Lifted Magic Squares* (`paper_A_gems/`, `arXiv:2512.09170`) | [`paperA.pdf`](paperA.pdf) | `python3 paper_A_gems/anc/verify_paper_a.py` |
| **Paper B** | *Bivariate Polynomial Moments and Prouhet–Tarry–Escott Identities of Semi-Magic Squares* (`paper_B_orthogonality/`) | [`paperB.pdf`](paperB.pdf) | `python3 paper_B_orthogonality/anc/verify_paper_b.py` |
| **Paper C** | *Mechanics and Balance of Magic Gems: Radial Vector Laws, Symmetric-Top Precession, Nested Core Inclusions, and Mirror-Twin Towers* (`paper_C_mechanics/`) | [`paperC.pdf`](paperC.pdf) | `python3 paper_C_mechanics/anc/verify_paper_c.py` |

---

## Repository Structure

```text
magicGem/
├── paperA.pdf                        # Compiled Manuscript — Paper A (Convex Hulls & Face Lattices)
├── paperB.pdf                        # Compiled Manuscript — Paper B (Polynomial Moments & PTE Hierarchy)
├── paperC.pdf                        # Compiled Manuscript — Paper C (Mechanics, Fabrication & Stacking)
├── index.html                        # Interactive Web Essay for Paper C (GitHub Pages root)
├── simulators.js                     # Interactive 2D/3D Physics, Wireframe, Papercraft & Tower Simulators
├── gems_data.js                      # Precomputed exact geometry & mechanics dataset for all 880 order-4 gems
├── paper_A_gems/                     # Paper A LaTeX sources, figures, and ancillary verification suite
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── anc/                          # squares880.txt, gem_geometry.py, verify_paper_a.py
├── paper_B_orthogonality/            # Paper B LaTeX sources, figures, and ancillary verification suite
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── anc/                          # verify_paper_b.py, make_figures_b.py
├── paper_C_mechanics/                # Paper C LaTeX sources, figures, web essay, and verification suite
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   ├── web/                          # Interactive web essay (index.html, simulators.js, gems_data.js)
│   └── anc/                          # verify_paper_c.py, make_figures_c.py, results_paper_c.json
└── web/                              # Mirror of the Paper C interactive web essay
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
