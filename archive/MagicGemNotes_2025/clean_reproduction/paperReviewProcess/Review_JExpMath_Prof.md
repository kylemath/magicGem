# Review of "From Discrete Constraints to Continuous Geometry: A Comprehensive Analysis of Magic Squares"

**Referee:** Prof. Dr. [Redacted]  
**Affiliation:** Institute for Mathematics, ETH Zürich / Department of Mathematics, Princeton University  
**Journal:** Journal of Experimental Mathematics  
**Date:** December 1, 2025  

## Recommendation
**Accept with Minor Revisions**

---

## 1. General Assessment

This manuscript presents a novel and visually striking geometric analysis of $4 \times 4$ magic squares. By embedding these classical combinatorial objects into $\mathbb{R}^3$ and treating them as "Magic Gems" (convex hulls of point clouds), the author bridges the gap between discrete combinatorics and continuous geometric analysis.

The paper is ambitious, employing techniques from computational topology (persistent homology), optimal transport (Wasserstein/Earth Mover’s Distance), and manifold learning to characterize the space of solutions. The central contribution—the "Zero-Covariance Theorem"—provides a statistical-physics-flavored characterization of the magic constant constraints, which is then cleverly leveraged to formulate a continuous optimization algorithm.

I commend the author for the exceptional quality of the figures and the thoroughness of the "reproducibility package." It is rare to see a mathematics submission where the code is not only available but structured as a production-grade artifact. This aligns perfectly with the ethos of *Experimental Mathematics*.

However, while the results are compelling, the mathematical interpretation occasionally leans too heavily on physical metaphor ("balance", "gems") at the expense of rigorous algebraic clarity. The distinction between the discrete set of 880 solutions and the continuous manifold of the relaxed problem needs sharper delineation.

---

## 2. Major Comments

### 2.1. The Nature of the "Zero-Covariance" Characterization
The "Zero-Covariance Theorem" (Theorem 1.1) is the theoretical engine of this paper. It states that magic squares are characterized by zero covariance between position and value.
While this is a beautiful *physical* interpretation (analogous to a vanishing dipole moment in charge distribution), mathematically, this is a linear transformation of the standard magic sum constraints.
$$ \sum_j M_{ij} = S \iff \text{Row Sum Constraint} $$
The covariance condition is essentially ensuring that the "center of mass" of the values is located at the geometric center of the grid.
**Critique:** The author should explicitly show the algebraic equivalence between the standard linear constraints and the covariance formulation. Is it a bijection? Does it degenerate for singular matrices? A short proof or derivation in the appendix connecting $\sum M_{ij} = S$ directly to $Cov(X, Z) = 0$ would ground the physical intuition in solid algebra.

### 2.2. The "Manifold" vs. The Discrete Set
The paper discusses the "Magic Square Manifold" (Section 9.3). This terminology is slightly slippery. The set of $4 \times 4$ magic squares is a discrete set of 880 points (or $880 \times \text{symmetries}$).
The "manifold" referred to is likely the solution space of the *relaxed* continuous problem (matrices with real entries satisfying the sum constraints).
**Critique:** Please clarify formally what is meant by "manifold" here. Is it the affine subspace of $\mathbb{R}^{16}$ defined by the linear constraints? Or the variety defined by the covariance polynomials? If it's just the affine subspace, the topology is trivial (it's a vector space). The "rich structure" presumably comes from the *intersection* of this continuous space with the hypercube of valid ranges or the integer lattice. The topological analysis (persistent homology) is applied to the discrete points, but the optimization runs on the continuous relaxation. The text should rigorously distinguish between these two regimes.

### 2.3. Algorithmic Complexity and Comparison
The claimed $O(n^4 \log(1/\epsilon))$ complexity for the gradient-based generation is impressive compared to *naive* backtracking. However, the comparison to "exponential classical methods" sets a low bar.
**Critique:**
1.  **Comparison to SAT/CSP Solvers:** Modern constraint satisfaction solvers (e.g., Google OR-Tools, Gurobi) are extremely efficient at this scale. How does the gradient descent approach compare to a state-of-the-art CSP solver for $n=4$ or $n=5$?
2.  **Local Minima:** The gradient landscape of combinatorial relaxations is notoriously rugged. For $n=4$, it works 100% of the time. Does this hold for $n > 5$? The paper implies scalability, but "basins of attraction" often shrink exponentially with dimension. A brief comment on the limitations for larger $n$ is necessary to avoid overclaiming.

### 2.4. Reproducibility and Code Quality
I reviewed the provided codebase (`clean_reproduction/`). It is exemplary. The separation of `core.py`, `optimization.py`, and `features.py` is clean.
**Suggestion:** The `requirements.txt` should ideally specify version numbers (e.g., `numpy==1.21.0`) to ensure long-term reproducibility, as purely continuous integration can break with major library updates. The inclusion of a `setup.sh` is a nice touch for reviewers.

---

## 3. Minor Comments and Typos

1.  **Abstract:** "Convex hull volumes of $84.1 \pm 7.1$ cubic units." Please specify the normalization. Is the unit cube volume 1? Or is it based on the integer coordinates? The scale matters for reproducibility.
2.  **Section 1.1:** "balance perfectly." This implies torque balance. It would be helpful to mention that the "moment" is the first moment of the mass distribution.
3.  **Figure 3:** The histograms are excellent. The "21 distinct configurations" finding is a true "experimental math" gem. Have you checked if these classes correspond to the Dudeney groups or Frenicle index ranges? A cross-reference would be valuable.
4.  **Terminology:** "Magic Gem" is catchy, but "Magic Polytope" or "Magic Convex Hull" might be more standard. I do not mind "Gem" if defined clearly, as it adds flavor.
5.  **Topological Data Analysis:** The use of persistent homology on 880 points is valid. However, the claim of "multi-scale features" should be tempered. With only 880 points in high dimensions, the homology is sensitive to the metric chosen (Euclidean vs. Hamming?). Please specify the metric used for the TDA.

---

## 4. Conclusion

This is a high-quality submission that fits the scope of *Experimental Mathematics* perfectly. It uses computation to gain insight into a classical structure, offering new visualizations and a novel optimization angle. The "Zero-Covariance" perspective, while mathematically adjacent to existing spectral methods, offers a fresh "physical" intuition that is valuable.

With the clarifications on the mathematical rigor of the "manifold" and the "covariance equivalence," I enthusiastically recommend publication.

**Decision:** Accept with Minor Revisions.

