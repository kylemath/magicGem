# Paper D: Spectral Energy Landscapes, Multiscale Window Entropies, and Continuous Bubble Relaxation of Magic Squares

**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta · `kyle.mathewson@ualberta.ca`)  
**Compiled Manuscript:** [`../paperD.pdf`](../paperD.pdf) (23 pages, 7 figures, 8 tables)  
**arXiv Submission Archive:** [`../paperD_arxiv.tar.gz`](../paperD_arxiv.tar.gz)  
**Interactive Companion Suite:** [`../web/physicalSolver/bubble-trinity.html`](../web/physicalSolver/bubble-trinity.html) & [`../web/physicalSolver/index.html`](../web/physicalSolver/index.html)

---

## Summary of Main Results

1. **Spectral Rationalization & Universal Ensemble Mean (Theorems 2.1–2.2, Proposition 2.3):**
   - While the unprojected line-incidence Laplacian $L_n = A_n^\top A_n$ on $\mathbb{R}^{n^2}$ exhibits irrational eigenvalues $\lambda_\pm(n)$ from the coupling between the constant vector $\mathbf{1}$ and the two main diagonals, restricting $L_n$ to the zero-mean hyperplane $\mathbf{1}^\perp$ via $\widetilde{L}_n = P_{\mathbf{1}^\perp} L_n P_{\mathbf{1}^\perp}$ collapses the entire spectrum into exact integers:
     - Even $n \ge 4$: $\operatorname{spec}(\widetilde{L}_n|_{\mathbf{1}^\perp}) = \{0^{[n^2-2n-1]}, (n-2)^{[1]}, n^{[2n-1]}\}$
     - Odd $n \ge 3$: $\operatorname{spec}(\widetilde{L}_n|_{\mathbf{1}^\perp}) = \{0^{[n^2-2n-1]}, (n-1)^{[2]}, n^{[2n-2]}\}$
   - By the incidence trace identity $\operatorname{tr}(\widetilde{L}_n) = 2(n^2-1)$, the mean eigenvalue of $\widetilde{L}_n$ on $\mathbf{1}^\perp$ is **identically $\bar{\mu}(\widetilde{L}_n) = 2$** for every $n \ge 3$, yielding the exact random-permutation expectation $\mathbb{E}[\mathcal{H}_{\mathrm{line}}(S)] = \frac{2}{3}n^2(n^4-1)$.
   - Enforcing 3D dipole orthogonality $\langle X,Z\rangle = \langle Y,Z\rangle = 0$ and diagonal balance $R_{D_+} = R_{D_-} = 0$ constrains only a $4$-dimensional subspace of $\operatorname{im}(\widetilde{L}_n)$, leaving a $(2n-4)$-dimensional zero-mean optical-phonon residual subspace exemplified at $n=4$ by $S_{\mathrm{low}}$ ($\mathcal{H}_{\mathrm{line}} = 1{,}584$).

2. **Even-Order Quartet Equivalence & Concentric Shell Quadrupole Identity (Theorem 3.1, Proposition 3.2):**
   - For any even order $n = 2m$, vanishing of the $(2m-1)^2$ interior $2\times 2$ quartet sums ($W_{2\times 2}^{\mathrm{int}}(S) = 0$) on a magic square automatically forces all $4m - 1$ boundary-wrapping toroidal $2\times 2$ quartets to vanish ($W_{2\times 2}^{\mathrm{tor}}(S) = 0$).
   - On every order-$4$ magic square, $R_{D_\pm}(S) = 0 \implies Q_{\mathrm{inner}}(S) = -Q_{\mathrm{corner}}(S)$, reducing the 3D octupole moment to the **Concentric Shell Quadrupole Identity**:
     $$M_{xyz}(S) = -8\,Q_{\mathrm{corner}}(S) - 3\,Q_{\mathrm{edge}}(S).$$
     This explains why $M_{xyz}(S)$ vanishes on all $48$ Group III associative squares ($B_{\mathrm{comp}}=0$) plus exactly $8$ non-associative squares ($B_{\mathrm{comp}}=8$) in Group IX (`#200, #208, #390, #711`) and Group X (`#492, #494, #794, #811`) satisfying the coprime resonance $(Q_{\mathrm{corner}}, Q_{\mathrm{edge}}) = (-3k, 8k)$ at $k \in \{\pm 4, -8\}$.

3. **Combinatorial Swap Landscape & Unique Spin-Ice $(2,2)$ Escape (Proposition 4.1, Theorem 4.2):**
   - Any $2$-cycle transposition $\tau_{ab}$ shifts $\mathcal{H}_{\mathrm{line}}(S)$ by $\Delta\mathcal{H}_{\mathrm{line}}(\tau_{ab}) = -2d(g_a - g_b) + c_{ab}d^2$ with $c_{ab} \in \{2,\dots,7\}$.
   - Across all $9! = 362{,}880$ permutations of $S_9$, besides the $8$ Lo Shu ground states ($\mathcal{H}_{\mathrm{line}}=0$), there exist **only $8$ spurious strict local minima** forming a single $D_4$ orbit $S_{\mathrm{trap}}^{(3)}$ at $\mathcal{H}_{\mathrm{line}}=8$.
   - Every single $2$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +4$) and every single $3$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +8$) on $S_{\mathrm{trap}}^{(3)}$ strictly increases energy, but **one and only one** disjoint $(2,2)$ double transposition—the row-preserving Pauling spin-ice loop $(6\leftrightarrow 7)(3\leftrightarrow 4)$, which crosses an intermediate single-swap saddle at $\mathcal{H}_{\mathrm{line}}^\ddagger = 12$ ($\Delta\mathcal{H}_{\mathrm{line}}^\ddagger = +4$)—tunnels directly to the Lo Shu ground state, expanding the deterministic basin of $S_9$ from $74.53\%$ to **$100.00\%$**.

4. **Bubble-Trinity Langevin Dynamics, 7-Tier Physical Ablation & Floppy-Mode Dimensional Relief (Section 5):**
   - Neither greedy cell snapping nor exact $O(N^3)$ Hungarian minimum-weight bipartite projection of continuous Bubble-Trinity trajectories reaches $\mathcal{H}_{\mathrm{line}}=0$ ($0\%$), because $\mathcal{H}_{\mathrm{ind}}(t)$ reduces energy via convex amplitude averaging inside the interior of the Birkhoff polytope.
   - Combining $O(1)$ incremental Kawasaki $2$-cycle steepest descent, crystallographic slip-plane glide, Pauling spin-ice line-preserving $(2,2)$ loops, Weaire–Rivier $T1$ / Falk–Langer Eshelby quadrupolar $(2,2)$ moves, and Wales–Doye / GroEL chaperonin re-anchored basin-hopping yields a **Re-Anchored Hierarchical Multi-Cycle Settler** that achieves **$100.0\%$ ground-state synthesis across all orders $n = 3, 4, 5, 6, 7, 8$**.
   - Proves that a fraction $f_{\mathrm{null}}(n) = \frac{n^2-2n-1}{(n-1)^2} = 1 - \frac{2}{(n-1)^2}$ ($95.9\%$ at $n=8$) of the $(n-1)^2$-dimensional line-preserving $(2,2)$ subspace lies in the exact magic nullspace $\ker(\widetilde{L}_n)$, explaining the **Maxwell–Calladine Floppy-Mode Dimensional Relief Phenomenon**.

---

## Reproducing Paper D

```bash
# Run the complete verification and certification suite (~40s)
python3 paper_D_solver/anc/verify_paper_d.py

# Regenerate all 7 publication figures (.pdf and .png)
python3 paper_D_solver/anc/make_figures_d.py

# Compile the LaTeX manuscript
cd paper_D_solver && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
