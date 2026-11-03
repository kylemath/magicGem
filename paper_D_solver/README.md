# Paper D: Can Physical Forces Find a Magic Square? Spectral Energy Landscapes, Window Entropies, and Interactive Relaxation Dynamics

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta · `kyle.mathewson@ualberta.ca`)  
**Compiled Manuscript:** [`../paperD.pdf`](../paperD.pdf) (20 pages, 7 figures, 8 tables)  
**arXiv Submission Archive:** [`../paperD_arxiv.tar.gz`](../paperD_arxiv.tar.gz)  
**Interactive Browser Laboratories:**
- [`../web/physicalSolver/index.html`](../web/physicalSolver/index.html) (Suite Landing Page)
- [`../web/physicalSolver/energy-decomposition.html`](../web/physicalSolver/energy-decomposition.html) (*Energy Decomposition & Window Entropy Explorer*)
- [`../web/physicalSolver/physics-lab.html`](../web/physicalSolver/physics-lab.html) (*Physical Magic Square Lab*)
- [`../web/physicalSolver/vector-physics.html`](../web/physicalSolver/vector-physics.html) (*Vector Force Field & Torque Simulator*)
- [`../web/physicalSolver/bubble-trinity.html`](../web/physicalSolver/bubble-trinity.html) (*Bubble Trinity & Multi-Exchange Auto-Settler Lab*)

---

## Summary of Main Results & Interactive Phenomena

1. **Why Balancing a Plate Is Not Enough: The Zero-Mean Spectrum and the Impostor Square $S_{\mathrm{low}}$ (Proposition 2.1, Remark 2.2):**
   - Using the Rook's-graph decomposition $L_n = L_{\mathrm{rc}} + D$ ($K_n \square K_n$ plus two main diagonals), restricting $L_n = A_n^\top A_n$ to the zero-mean hyperplane $\mathbf{1}^\perp$ via $\widetilde{L}_n = P_{\mathbf{1}^\perp} L_n P_{\mathbf{1}^\perp}$ confines the rank-$2$ diagonal perturbation inside $\ker(L_{\mathrm{rc}})$ and reduces the irrational roots $\lambda_\pm(n)$ to exact integers:
     - Even $n \ge 4$: $\operatorname{spec}(\widetilde{L}_n|_{\mathbf{1}^\perp}) = \{0^{[n^2-2n-1]}, (n-2)^{[1]}, n^{[2n-1]}\}$
     - Odd $n \ge 3$: $\operatorname{spec}(\widetilde{L}_n|_{\mathbf{1}^\perp}) = \{0^{[n^2-2n-1]}, (n-1)^{[2]}, n^{[2n-2]}\}$
   - By both the incidence trace identity $\operatorname{tr}(\widetilde{L}_n) = 2(n^2-1)$ and finite-population sampling without replacement, the mean eigenvalue of $\widetilde{L}_n$ on $\mathbf{1}^\perp$ is $\bar{\mu}(\widetilde{L}_n) = 2$ for every $n \ge 3$, yielding $\mathbb{E}[\mathcal{H}_{\mathrm{line}}(S)] = \frac{2}{3}n^2(n^4-1)$.
   - Enforcing linear dipole tilt balance $\langle X,Z\rangle = \langle Y,Z\rangle = 0$ and diagonal balance $R_{D_+} = R_{D_-} = 0$ constrains only a $4$-dimensional subspace of $\operatorname{im}(\widetilde{L}_n)$, leaving a $(2n-4)$-dimensional subspace of higher-degree polynomial row/column waves unconstrained (illustrated at $n=4$ by the impostor square $S_{\mathrm{low}}$ with $\mathcal{H}_{\mathrm{line}} = 1{,}584$).

2. **Inside the Magic Manifold: Window Entropies, Panmagic Quartets, and the 56 Octupole Zeros (Lemma 3.1, Proposition 3.2):**
   - For any even order $n = 2m$, vanishing of the $(2m-1)^2$ interior $2\times 2$ quartet sums ($W_{2\times 2}^{\mathrm{int}}(S) = 0$) on a magic square automatically forces all $4m - 1$ boundary-wrapping toroidal $2\times 2$ quartets to vanish ($W_{2\times 2}^{\mathrm{tor}}(S) = 0$).
   - On every order-$4$ magic square, $R_{D_\pm}(S) = 0 \implies Q_{\mathrm{inner}}(S) = -Q_{\mathrm{corner}}(S)$, reducing the 3D octupole twist to the **Concentric Shell Quadrupole Identity**:
     $$M_{xyz}(S) = -8\,Q_{\mathrm{corner}}(S) - 3\,Q_{\mathrm{edge}}(S).$$
     This proves that $M_{xyz}(S)$ vanishes on all $48$ Group III associative squares ($B_{\mathrm{comp}}=0$) plus exactly $8$ non-associative squares ($B_{\mathrm{comp}}=8$) in Group IX (`#200, #208, #390, #711`) and Group X (`#492, #494, #794, #811`) satisfying the coprime shell resonance $(Q_{\mathrm{corner}}, Q_{\mathrm{edge}}) = (-3k, 8k)$ at $k \in \{\pm 4, -8\}$.

3. **The $3\times 3$ Combination Lock: Why Pair and Triplet Swaps Get Trapped (Lemma 4.1, Theorem 4.2):**
   - Any $2$-cycle transposition $\tau_{ab}$ shifts $\mathcal{H}_{\mathrm{line}}(S)$ by $\Delta\mathcal{H}_{\mathrm{line}}(\tau_{ab}) = -2d(g_a - g_b) + c_{ab}d^2$ with $c_{ab} \in \{2,\dots,7\}$.
   - Across all $9! = 362{,}880$ permutations of $S_9$, besides the $8$ Lo Shu ground states ($\mathcal{H}_{\mathrm{line}}=0$), there exist **only $8$ spurious strict local minima** forming a single $D_4$ orbit $S_{\mathrm{trap}}^{(3)}$ at $\mathcal{H}_{\mathrm{line}}=8$.
   - Every single $2$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +4$) and every single $3$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +8$) on $S_{\mathrm{trap}}^{(3)}$ strictly increases energy, but **one and only one** disjoint $(2,2)$ double transposition—the synchronized row-preserving move $(6\leftrightarrow 7)(3\leftrightarrow 4)$, which crosses an intermediate single-swap saddle at $\mathcal{H}_{\mathrm{line}}^\ddagger = 12$ ($\Delta\mathcal{H}_{\mathrm{line}}^\ddagger = +4$)—unlocks the trap directly to the Lo Shu ground state, expanding the deterministic basin of $S_9$ from $74.53\%$ to **$100.00\%$**.

4. **Floating Bubbles vs. Multi-Exchange Local Search: Why $5\times 5$ Is Harder Than $10\times 10$ ($n=3\dots 10$, Section 5):**
   - Across all four *Bubble Trinity* presets (*I. Frozen Lattice*, *II. Slow Drift*, *III. Field Storm*, *IV. Centrifugal Balance*), neither greedy cell snapping nor exact $O(N^3)$ Hungarian minimum-weight bipartite projection of continuous 2D Gaussian-kernel trajectories reaches $\mathcal{H}_{\mathrm{line}}=0$ ($0\%$), because floating bubbles "cheat" by blending positive and negative heights across cell borders.
   - Combining $O(1)$ incremental $2$-exchange steepest descent, whole-row/column permutations, row/column-preserving $(2,2)$ plaquette moves, candidate-list $(2,2)$ swaps, and thresholded basin-hopping yields a **Multi-Exchange Iterated Local Search (ME-ILS)** algorithm that achieves **$100.0\%$ ground-state synthesis across all orders $n = 3, 4, 5, 6, 7, 8, 9, 10$** (up to $100! \approx 9.33\times 10^{157}$ states).
   - A fraction $f_{\mathrm{null}}(n) = \frac{n^2-2n-1}{(n-1)^2} = 1 - \frac{2}{(n-1)^2}$ ($97.5\%$ at $n=10$) of the $(n-1)^2$-dimensional line-preserving $(2,2)$ subspace lies in the exact magic nullspace $\ker(\widetilde{L}_n)$, explaining why mean restarts peak at $n=5$ ($8.03$) and drop to $3.34$ at $n=10$.

---

## Reproducing Paper D

```bash
# Run the complete verification and certification suite
python3 paper_D_solver/anc/verify_paper_d.py

# Regenerate all 7 publication figures (.pdf and .png)
python3 paper_D_solver/anc/make_figures_d.py

# Compile the LaTeX manuscript
cd paper_D_solver && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
