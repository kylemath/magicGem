# Ancillary Verification Suite for Paper C

This directory (`anc/`) contains the exact-arithmetic verification and figure-generation scripts for:

**Mechanics and Balance of Magic Gems: Radial Vector Laws, Symmetric-Top Precession, Nested Core Inclusions, and Mirror-Twin Towers**  
Kyle Elliott Mathewson (*University of Alberta*)

## Files

- `verify_paper_c.py`: Self-contained exact verification script (using `fractions.Fraction`, `numpy`, and `scipy`) that verifies every theorem, proposition, and numerical table in Sections 2–5 and Appendix A:
  - Order-3 radial resultant formula and exact unit-vector norm $4\sqrt{5}-2\sqrt{10}\approx2.619717$.
  - Order-4 Three-Ring Decomposition ($R_{\mathrm{in}}, R_{\mathrm{mid}}, R_{\mathrm{out}}$), non-vanishing ring dipoles, collinear ring ratios ($408/880$), and the Diophantine Pell minimum $18\sqrt{10}/5-8\sqrt{2}\approx0.070491$ attained on `#70, #76, #121, #188, #452, #459, #490, #574`.
  - 3D unit-sphere parity dichotomy ($48/880$ associative squares).
  - Universal point-mass symmetric-top inertia law, entry-weighted ($m_{ij}=s_{ij}$) quadrupole splitting $I_{1,2}=170\mp|Q_{xy}(S)|$ ($56$ axisymmetric classes), and exact rational simplex integration of the continuous polyhedral inertia tensor $I_{\mathrm{solid}}(\mathcal G(S))$ over all $880$ gems.
  - Classification of the $51$ naturally balanced gems (`#86, #739, #756` + $48$ associative), recursive Chazelle onion-peeling depths ($18$ depth-1, $842$ depth-2, $20$ depth-3), the $33$ two-density "diamond-in-a-diamond" balanced gems ($+2$ lighter/cavity cores `#123` and `#54`), and the $477$ inner-cone point-balancable gems.
  - Ball-and-rod wireframes $G(\mathcal G_0)\cup G(\mathcal G_1)$, complete $120$-rod networks $K_{16}$ (`magicGem_v2.stl`, proving $\Sigma_{\mathrm{rods}}=\frac{29}{45}\Sigma(\lambda)$ for equal-mass rods and $2.7\times$–$3.6\times$ centroid drift reduction for length-weighted rods), composite balance of $158$ Group VI wireframes ($\lambda=1$) and $164$ ($\lambda=0.20$) via rod diameter ratio $d_1/d_0$, and unfolded 2D papercraft cutout nets with topological glue-tab invariant $N_{\mathrm{tabs}}=f_1-(f_2-1)=f_0-1\in[7,15]$ and non-overlapping BFS unfoldings across all $880/880$ gems.
  - Resting gravitational stability census across all $14,824$ facets at $\lambda=1.0$ ($6,378$ stable, $43.0\%$) and $\lambda=0.20$ ($11,044$ stable, $74.5\%$), same-gem parallel facet pairs ($124/880$), and the $48$ vertically centered mirror-twin tower gems ($17$ knight's-move square gems with $A_{xy}=5$, led by `#763`).
- `results_paper_c.json`: Complete JSON archive output by `verify_paper_c.py`.
- `make_figures_c.py`: Generates all six multi-panel vector PDF figures (`../figures/fig_origin_vectors_3d.pdf`, `fig_ring_vectors.pdf`, `fig_precession_dynamics.pdf`, `fig_nested_diamonds.pdf`, `fig_wireframes_and_nets.pdf`, `fig_mirror_stacking.pdf`).

## Reproducing all results and figures

```bash
python3 verify_paper_c.py
python3 make_figures_c.py
```
