# Peer Review: Journal of Experimental Mathematics

**Manuscript:** "From Discrete Constraints to Continuous Geometry: A Comprehensive Analysis of Magic Squares Through Covariance, Topology, and Optimization"

**Author:** Kyle Elliott Mathewson, University of Alberta

**Reviewer:** [Anonymous]  
**Affiliation:** Department of Mathematics, [Redacted European Institution]  
**Areas of Expertise:** Combinatorial Geometry, Algebraic Topology, Discrete Optimization  
**Date:** December 1, 2025

---

## I. Summary

This manuscript proposes a geometric framework for analyzing $4 \times 4$ magic squares by embedding them as point clouds in $\mathbb{R}^3$ via the map $(i, j) \mapsto (i, j, M_{ij})$. The central theoretical claim is the **Zero-Covariance Theorem** (Theorem 1.1), which asserts that a permutation of $\{1, \ldots, 16\}$ arranged in a $4 \times 4$ grid forms a magic square if and only if four specific spatial-value covariances vanish. The author leverages this reformulation to develop gradient-based optimization algorithms and applies tools from computational topology (persistent homology), optimal transport (Earth Mover's Distance), and manifold learning to characterize the space of all 880 unique magic squares.

---

## II. General Assessment

This is an ambitious and creative piece of work that attempts to bridge classical recreational mathematics with modern geometric and topological machinery. The central insight—that the discrete magic sum constraints translate to continuous covariance conditions—is genuinely elegant and, if correct, provides a novel perspective on a classical problem.

However, I have significant reservations about the mathematical rigor of key claims, the appropriateness of certain analytical tools given the problem scale, and the generalizability of the results beyond $n=4$. The paper reads more like an enthusiastic exploration than a rigorous mathematical treatise. With substantial revision, particularly in strengthening the proofs and tempering some claims, this could become a valuable contribution to experimental mathematics.

**Recommendation: Major Revision Required**

---

## III. Major Concerns

### 3.1. The Zero-Covariance Theorem: Proof Deficiencies

The Zero-Covariance Theorem is the paper's cornerstone, yet its proof (as presented in the manuscript) falls short of the rigor expected in a mathematics journal.

**Specific Issues:**

1. **Forward direction (magic ⇒ zero covariance):** The argument that equal row/column/diagonal sums imply vanishing covariances is straightforward linear algebra, and this direction appears correct. However, the proof should be written out explicitly rather than summarized.

2. **Reverse direction (zero covariance ⇒ magic):** This is the non-trivial direction, and the manuscript does not provide a complete proof. The claim that four vanishing covariances *suffice* to guarantee magic structure requires careful argument. In particular:
   
   - The covariance conditions are stated for generic $(X, Y, Z)$ random variables, but a magic square requires *specific* integer values $\{1, \ldots, 16\}$.
   - The conditions $\text{Cov}(X, Z) = 0$ and $\text{Cov}(Y, Z) = 0$ alone do not imply equal row/column sums—they imply that the *weighted average* position equals the unweighted average. The author conflates these.
   - The diagonal covariance conditions similarly need careful treatment.

3. **Permutation constraint:** The theorem statement says "a permutation matrix $M$ of integers $\{1, 2, \ldots, n^2\}$"—but this phrasing is imprecise. A permutation matrix is a $0$-$1$ matrix; the author presumably means a permutation of integers arranged in a matrix. This imprecision propagates through the proof.

**Required Action:** Provide a complete, line-by-line proof of Theorem 1.1 with explicit treatment of the integer constraint. The reverse direction should be stated as a separate lemma with its own proof.

### 3.2. Complexity Claims Require Formal Analysis

The paper claims that the gradient-based generation algorithm achieves $O(n^4 \log(1/\epsilon))$ complexity, representing a dramatic improvement over exponential backtracking. This is an extraordinary claim that requires extraordinary evidence.

**Issues:**

1. **Convergence guarantees are absent.** Gradient descent on a non-convex landscape (which this surely is) does not guarantee convergence to a global minimum. The paper reports 100% success rate for $n=4$, but this is empirical—not a proof of polynomial-time solvability.

2. **The complexity analysis conflates several distinct quantities:**
   - Per-iteration cost (which may indeed be $O(n^4)$)
   - Number of iterations to convergence (not rigorously bounded)
   - Probability of finding a valid integer solution (not analyzed)

3. **The claim effectively asserts P = NP for magic square generation.** While magic square decision is not known to be NP-complete, the generation problem for large $n$ is computationally hard. A polynomial-time algorithm with provable guarantees would be a major result requiring substantial proof infrastructure.

**Required Action:** Either provide rigorous convergence analysis with formal complexity bounds, or substantially temper the claims to "empirically efficient" rather than "polynomial time."

### 3.3. Topological Analysis on Small Point Clouds

The application of persistent homology to point clouds of size $N = 16$ is methodologically questionable.

**Issues:**

1. **Sample size concerns:** Persistent homology is designed for point cloud data where the number of points is large relative to the ambient dimension. With only 16 points in $\mathbb{R}^3$, the Vietoris-Rips complex has at most $\binom{16}{k}$ $k$-simplices, severely limiting the topological features that can be detected.

2. **Interpretation difficulties:** The paper reports Betti numbers and persistence diagrams, but it's unclear what these mean geometrically for such sparse data. A convex hull of 16 points has at most a few "holes" by construction—this is geometry, not topology in the classical sense.

3. **Comparison with random matrices:** The claim that persistent homology distinguishes magic squares from random arrangements may simply reflect differences in *geometry* (convex hull shape) rather than meaningful *topological* differences.

**Required Action:** Either justify the use of persistent homology for small point clouds with references to the TDA literature on sample complexity, or reframe this section as "geometric feature analysis" rather than "topological analysis."

### 3.4. Generalizability Beyond $n = 4$

The entire analysis is restricted to $4 \times 4$ magic squares. While the theoretical framework purports to generalize, no evidence is provided that:

1. The 21-configuration classification has analogues for larger $n$
2. The optimization landscape remains benign for $n \geq 5$
3. The manifold structure (clustering, connectivity) persists at larger scales

Given that there are 275,305,224 essentially different $5 \times 5$ magic squares, the computational claims become much harder to verify.

**Required Action:** Include at least preliminary analysis of $n = 5$ magic squares, or explicitly acknowledge that all results are specific to $n = 4$ with unknown generalizability.

---

## IV. Moderate Concerns

### 4.1. The "21 Configurations" Classification

The paper claims that all 880 magic squares fall into exactly 21 distinct geometric configurations. While intriguing, this classification raises questions:

1. **Is this genuinely novel?** Convex hull vertex counting for magic square embeddings may have been explored in the literature. The paper should clarify whether this specific classification is new.

2. **Mathematical significance:** What does this classification tell us mathematically? Is there a relationship to the classical Frenicle classes or the symmetry groups?

3. **Stability under perturbation:** How does the classification behave if we consider approximate magic squares or perturbations?

### 4.2. Physical Metaphor vs. Mathematical Content

The paper leans heavily on the "balance" metaphor—stacked coins, teeter-totters, physical equilibrium. While pedagogically useful, this metaphor sometimes substitutes for rigorous mathematics.

**Example:** Section 1.2 states that "the magic sum property ensures that this weighted grid would remain perfectly balanced when supported at its center point." This is intuitive but not precise. The balance of a rigid body depends on moments of inertia, not just weighted sums. The author should either develop this physical analogy rigorously (computing the actual inertia tensor and showing it has special properties for magic squares) or use it only as motivation, not as mathematical content.

### 4.3. Earth Mover's Distance: Justification and Alternatives

The use of EMD (Wasserstein-1 distance) for comparing magic squares is interesting but needs better justification:

1. **Why EMD over other metrics?** The paper states that EMD "respects both spatial and numerical aspects," but so do many other metrics (e.g., Frobenius norm on the centered matrices, Procrustes distance on point clouds).

2. **Normalization issues:** The EMD computation normalizes point clouds to $[0,1]^3$. This loses information about scale differences between squares.

3. **Computational cost:** EMD requires solving an optimal transport problem. For comparing all $\binom{880}{2}$ pairs, this is expensive. Was this actually computed, or were approximations used?

### 4.4. Eigenvalue Claims

Section 5 and the Results section reference eigenvalue ratios (e.g., $\lambda_3/\lambda_1 = 17$) as "constraints" on magic squares. However:

1. These eigenvalues appear to be computed from the *covariance matrix* of the embedded point cloud, which is a second-moment statistic.

2. The claim that "eigenvalue constraints eliminate many potential integer configurations" is not substantiated. How many? By what mechanism?

3. The connection between covariance eigenvalues and the enumeration count (880) remains speculative.

---

## V. Minor Issues

### 5.1. Notation and Terminology

- "Permutation matrix" (Theorem 1.1) should be "permutation arrangement" or "permutation matrix representation"
- "Stratified manifold" is used loosely; the space of 880 discrete points is not technically a manifold
- "Magic Gem" is evocative terminology but should be formally defined before use

### 5.2. Figure Quality

The figures are generally well-produced, but:

- Figure 3 (21 configurations gallery) referenced in the text but not visible in my copy—ensure all figures are included
- Some axis labels are too small for print reproduction
- The color scheme should be verified for colorblind accessibility

### 5.3. Statistical Reporting

- Table 1: "Cohen's $d$ = ---" for magic squares is undefined, not meaningful (no variance in the comparison group)
- The KS test $p$-value "$< 10^{-100}$" should be reported as "numerically zero" or "effectively zero"—such extreme values are computational artifacts
- Bootstrap confidence intervals are mentioned but not shown

### 5.4. Literature Gaps

The paper omits several relevant references:

- Andrews (1960) on magic squares and Latin squares
- Beck and Zaslavsky on hyperplane arrangements (potentially relevant to the constraint manifold interpretation)
- Recent work on algebraic combinatorics of magic squares

### 5.5. Reproducibility

The paper mentions code availability but does not include a persistent identifier (DOI) or repository link. For reproducibility, this should be provided.

---

## VI. Technical Corrections

1. **Equation (1), Section 4:** The definition $\phi(M) = \{(i, j, M_{ij}) \mid 0 \leq i, j \leq n-1\}$ uses 0-indexing, but the magic square definition uses values $\{1, \ldots, n^2\}$. Clarify indexing conventions.

2. **Section 5.1:** The "correlation dimension method" formula should include the limit notation properly—currently the rendering is unclear.

3. **Section 7:** The claim of "$O(n^2)$ per-iteration complexity" contradicts the earlier "$O(n^4)$ complexity" claim. Clarify which operations achieve which complexity.

4. **Algorithm 1:** The pseudocode uses $H.\text{vertices}$ without defining the ConvexHull data structure. Provide specifications.

---

## VII. Strengths Worth Acknowledging

Despite the above criticisms, the paper has genuine merits:

1. **Original perspective:** The geometric embedding and covariance characterization provide fresh insight into a classical problem. Even if the proof needs tightening, the observation itself is valuable.

2. **Comprehensive empirical analysis:** The generation of 300,000+ samples for hypothesis testing is thorough. The perfect separation of magic squares at zero covariance is a striking empirical result.

3. **Interdisciplinary synthesis:** The paper successfully bridges combinatorics, geometry, topology, and optimization. This synthesis, even if imperfect, opens avenues for future research.

4. **Visualization:** The "Magic Gem" visualization and the hero figure effectively communicate geometric intuition.

5. **Reproducibility infrastructure:** The provision of complete code and data (modulo DOI) supports open science.

---

## VIII. Recommendations for Revision

### Essential (Must Address)

1. Provide a complete, rigorous proof of Theorem 1.1 (Zero-Covariance Theorem), separating forward and reverse directions with explicit treatment of integer constraints.

2. Either prove convergence and complexity bounds for the gradient descent algorithm, or reframe claims from "polynomial time" to "empirically efficient."

3. Justify the use of persistent homology on 16-point clouds, or reframe as geometric analysis.

4. Explicitly state the scope limitation to $n = 4$ throughout, and discuss (even speculatively) generalizability.

### Strongly Recommended

5. Clarify the mathematical content of the "balance" metaphor—either develop it rigorously or use only as motivation.

6. Justify EMD over alternative metrics, and report computational details.

7. Connect the 21-configuration classification to existing magic square taxonomy (Frenicle, symmetry groups).

8. Add missing references and provide persistent repository identifier.

### Optional but Beneficial

9. Include preliminary $n = 5$ results if computational resources permit.

10. Consider splitting the optimization/algorithmic content into a companion paper if length becomes an issue.

---

## IX. Summary and Recommendation

This manuscript presents an intriguing geometric perspective on magic squares with a potentially elegant central theorem. However, the current presentation lacks the mathematical rigor expected for publication in the Journal of Experimental Mathematics. The Zero-Covariance Theorem requires a complete proof, the complexity claims need formal justification, and several analytical choices (persistent homology on small samples, physical metaphors as mathematical content) need reconsideration.

I believe the core ideas are sound and publishable, but the execution requires significant revision. With careful attention to the major concerns outlined above, this could become a valuable contribution that opens new directions at the intersection of combinatorics and geometry.

**Recommendation: Major Revision**

The author should:
1. Address all "Essential" items before resubmission
2. Substantially address "Strongly Recommended" items
3. Consider "Optional" items as space permits

I would be willing to review a revised version of this manuscript.

---

**Signed:**

*Prof. [Anonymous]*  
*Department of Mathematics*  
*[Redacted European Institution]*

---

## Appendix: Detailed Comments by Section

### Introduction (Sections 1.1–1.6)

- Section 1.1: The opening metaphor is effective. "Magic Gem" is memorable terminology.
- Section 1.3: Historical review is adequate but brief. Consider citing Trump (2001) with more detail on computational verification.
- Section 1.4: Theorem 1.1 is clearly stated but proof is deferred too long. Consider adding a proof sketch.
- Section 1.6: Definitions are good; EMD definition could specify that this is Wasserstein-1.

### Methods (Section 3)

- Section 3.1: Embedding justification is reasonable. Comparison with alternatives is helpful.
- Section 3.2: EMD implementation details are sufficient. Note the $O(n^3)$ cost of Hungarian algorithm.
- Section 3.4: Persistent homology methodology is standard, but applicability to $N=16$ is questionable.
- Section 3.5: Statistical validation framework is solid.

### Results (Section 5)

- Table on hull configurations is useful. Correlation values (e.g., $r = 0.72$) should include confidence intervals.
- Section 5.7: The enumeration discussion is speculative. The approximate calculation yielding 880 is suggestive but not rigorous.

### Covariance Proof (Section 6)

- This is the critical section. The proof needs complete reconstruction.

### Discussion (Section 8)

- Section 8.1 (Alternative Hypotheses): Well-executed empirical analysis. This is the paper's strongest evidence for the zero-covariance characterization.
- Section 8.5: Connections to algebraic geometry and group theory are interesting but underdeveloped.

### Conclusion (Section 9)

- Well-written synthesis. Appropriately acknowledges limitations and future directions.

