# Cover Letter — Paper D Submission

**Date:** November 2, 2026  
**Title:** *Can Physical Forces Find a Magic Square? Spectral Energy Landscapes, Window Entropies, and Interactive Relaxation Dynamics*  
**Author:** Kyle Elliott Mathewson (Faculty of Science, University of Alberta, Edmonton, AB, Canada · `kyle.mathewson@ualberta.ca`)  
**Target Venues:** *Journal of Mathematics and the Arts* / *The Mathematical Intelligencer* / *American Journal of Physics* / *Mathematics Magazine* / *Physica A*

---

Dear Editors,

Please find enclosed our manuscript, *"Can Physical Forces Find a Magic Square? Spectral Energy Landscapes, Window Entropies, and Interactive Relaxation Dynamics,"* which we submit for consideration for publication. This work forms the fourth installment of our *Magic Gems* series (following Papers I–III on polyhedral convex hulls, bivariate polynomial moments, and 3D rotational/structural mechanics), shifting the focus from the static geometry of known magic squares to an interactive exploration of what happens when we try to *find* a magic square by letting physical forces and local tile swaps relax a scrambled board. Accompanying the manuscript is an open-source suite of four browser-based interactive laboratories (`physicalSolver`: `energy-decomposition.html`, `physics-lab.html`, `vector-physics.html`, and `bubble-trinity.html`) designed for hands-on exploration by mathematicians, physicists, educators, and students.

Across the manuscript, we use clean, elementary linear algebra and combinatorics to explain five surprising phenomena that anyone playing with the interactive simulators encounters immediately:

First, in the *Energy Decomposition Explorer* (`energy-decomposition.html`), we ask whether balancing the macroscopic center-of-mass tilt and main diagonals of a square plate is enough to make it magic. Using the Rook's-graph-plus-diagonals decomposition of the magic-line operator $L_n = A_n^\top A_n$, we show (Proposition 2.1) that restricting $L_n$ to the zero-mean permutation hyperplane $\mathbf{1}^\perp$ via $\widetilde{L}_n = P_{\mathbf{1}^\perp} L_n P_{\mathbf{1}^\perp}$ decouples the constant mode and reduces the irrational eigenvalues $\lambda_\pm(n)$ to exact integers: $\{0^{[n^2-2n-1]}, (n-2)^{[1]}, n^{[2n-1]}\}$ for even $n \ge 4$ and $\{0^{[n^2-2n-1]}, (n-1)^{[2]}, n^{[2n-2]}\}$ for odd $n \ge 3$, with universal mean eigenvalue $\bar{\mu}(\widetilde{L}_n) = 2$ and exact random-permutation expectation $\mathbb{E}[\mathcal{H}_{\mathrm{line}}(S)] = \frac{2}{3}n^2(n^4-1)$. We then exhibit an explicit $4\times 4$ "impostor square" $S_{\mathrm{low}}$ (Remark 2.2) whose planar tilt and diagonals are completely balanced ($\langle X,Z\rangle = \langle Y,Z\rangle = R_{D_\pm} = 0$) yet whose higher-degree polynomial waves give $\mathcal{H}_{\mathrm{line}}(S_{\mathrm{low}}) = 1{,}584$.

Second, inside the magic ground-state manifold $\ker(\widetilde{L}_n)$ where all 1D line sums vanish, we use sliding $k\times k$ window entropies $\widetilde{H}_p(k)$ and $2\times 2$ quartet energies to quantify 2D texture and 3D Gem twist across all $880$ order-$4$ magic squares. We record (Lemma 3.1) why balancing the $(2m-1)^2$ interior $2\times 2$ blocks of any even-order magic square automatically forces all $4m-1$ boundary-wrapping toroidal $2\times 2$ blocks to balance, isolating the $48$ panmagic squares of Dudeney Group I at $n=4$. We then prove the Concentric Shell Quadrupole Identity (Proposition 3.2), $M_{xyz}(S) = -8\,Q_{\mathrm{corner}}(S) - 3\,Q_{\mathrm{edge}}(S)$, which resolves why $8$ non-associative squares in Groups IX and X join the $48$ associative squares of Group III to produce $56$ octupole-zero Gems via the coprime shell resonance $(Q_{\mathrm{corner}}, Q_{\mathrm{edge}}) = (-3k, 8k)$.

Third, in the *Physical Magic Square Lab* (`physics-lab.html`) and *Vector Force Field Simulator* (`vector-physics.html`), we explain why single-pair and triplet swaps get stuck on nearly magic boards. Applying the rank-$1$ transposition difference formula $\Delta\mathcal{H}_{\mathrm{line}}(\tau_{ab}) = -2d(g_a-g_b) + c_{ab}d^2$ ($c_{ab} \in \{2,\dots,7\}$, Lemma 4.1) across all $9! = 362{,}880$ permutations of $S_9$ (Theorem 4.2), we prove that besides the $8$ Lo Shu ground states ($\mathcal{H}_{\mathrm{line}}=0$), $S_9$ possesses only $8$ spurious strict local minima forming a single $D_4$ orbit $S_{\mathrm{trap}}^{(3)}$ at $\mathcal{H}_{\mathrm{line}}=8$. On $S_{\mathrm{trap}}^{(3)}$, every single $2$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +4$) and every single $3$-cycle ($\min\Delta\mathcal{H}_{\mathrm{line}} = +8$) strictly increases energy, but one and only one disjoint $(2,2)$ double swap—the synchronized row-preserving move $(6\leftrightarrow 7)(3\leftrightarrow 4)$—unlocks the trap directly to the Lo Shu ground state, expanding the deterministic ground-state basin of $S_9$ from $74.53\%$ to $100.00\%$.

Finally, in the flagship *Bubble Trinity Simulator* (`bubble-trinity.html`), we contrast continuous 2D floating bubbles against discrete multi-exchange local search across the four interactive presets (*Frozen Lattice*, *Slow Drift*, *Field Storm*, and *Centrifugal Balance*). We show that continuous 2D Gaussian-kernel bubbles "cheat" by parking on cell borders to blend positive and negative heights ($0\%$ discrete recovery even under exact $O(N^3)$ Hungarian bipartite matching), whereas our discrete Multi-Exchange Iterated Local Search (ME-ILS) engine achieves $100.0\%$ ground-state convergence across all orders $n = 3, 4, \dots, 10$ (up to $100! \approx 9.33\times 10^{157}$ states). Remarkably, $5\times 5$ requires more basin-hopping restarts ($8.03$) than $10\times 10$ ($3.34$), because the fraction of the semi-magic $(2,2)$ plaquette subspace that is orthogonal to both diagonals grows as $f_{\mathrm{null}}(n) = 1 - \frac{2}{(n-1)^2}$, reaching $97.5\%$ at $n=10$.

All mathematical proofs, exhaustive censuses, and numerical benchmarks are certified by the standalone Python script `verify_paper_d.py` and linked directly to the live browser laboratories.

Thank you for your consideration.

Sincerely,

**Kyle Elliott Mathewson, PhD**  
Professor, Faculty of Science  
University of Alberta  
`kyle.mathewson@ualberta.ca`
