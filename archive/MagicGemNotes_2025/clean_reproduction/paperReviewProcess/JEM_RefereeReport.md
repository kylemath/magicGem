# Referee Report – Journal of Experimental Mathematics

**Manuscript:** *From Discrete Constraints to Continuous Geometry: A Comprehensive Analysis of Magic Squares Through Covariance, Topology, and Optimization*  
**Author:** Kyle Elliott Mathewson  
**Venue:** Journal of Experimental Mathematics  
**Referee:** Professor of Mathematics, [Redacted], [Top European/Ivy Institution]  
**Date:** December 1, 2025  
**Manuscript version reviewed:** main.pdf (`file:///Users/kylemathewson/FreshMagicPaper/clean_reproduction/paper/main.pdf`)

---

## 1. Overview and Significance

This manuscript develops a geometric and analytic framework for studying magic squares, focusing primarily on the \(4 \times 4\) case but formulating many results for general \(n \times n\) squares. The core idea is to embed each square as a point cloud in \(\mathbb{R}^3\) via \((i,j,M_{ij})\), center it appropriately, and study the resulting “Magic Gem” polyhedron. Within this framework, the author identifies several geometric invariants (convex hull volume, angular statistics, point–type counts) and combines them with modern tools from optimal transport (Earth Mover’s Distance), manifold learning, and persistent homology to analyze the space of all 880 unique \(4 \times 4\) magic squares.

The main theoretical contribution is the **Zero-Covariance Theorem**, which states that a permutation of \(\{1,\dots,n^2\}\) arranged on an \(n \times n\) grid is a magic square if and only if four specific spatial–value covariances vanish: \(\operatorname{Cov}(X,Z)\), \(\operatorname{Cov}(Y,Z)\), \(\operatorname{Cov}(X+Y,Z)\), and \(\operatorname{Cov}(X-Y,Z)\). This recasts the classical linear constraints on row, column, and diagonal sums as a succinct geometric-statistical condition. Building on this, the author proposes and empirically validates a gradient-based algorithm for generating magic squares with complexity \(O(n^4 \log(1/\varepsilon))\), reporting substantial speedups over optimized backtracking for \(n=4\).

Overall, this is a **creative and substantial contribution** to the experimental and geometric study of magic squares. The revised manuscript is clearly written, visually compelling, and much more narratively coherent than many technical reports in this area. It is also unusually well-documented and reproducible, with a complete computational pipeline and web-based visualizations.

---

## 2. Main Contributions

- **Zero-Covariance Characterization:** Theorem 1.1 provides a clean equivalence between magicness and four vanishing covariances in the axial embedding. This result is both conceptually attractive and technically useful, as it provides a smooth objective function for optimization.
- **Geometric Taxonomy of Magic Gems:** The manuscript shows that the 880 unique \(4 \times 4\) magic squares fall into exactly 21 distinct convex-hull configurations, classified by the number of vertices, face points, and interior points. This is a nontrivial, concrete geometric classification that complements classical symmetry-based taxonomies.
- **Algorithmic Framework:** The author derives analytic gradients for the covariance-based objective and uses them to construct a gradient-descent method with \(O(n^2)\) per-iteration cost and overall complexity claimed to be \(O(n^4 \log(1/\varepsilon))\). Experiments demonstrate 100% success in finding magic squares from random initial permutations for \(n=4\), with large speedups over backtracking.
- **Topological and Metric Analysis:** Using EMD, manifold learning, and persistent homology, the paper argues that the space of magic gems forms a single connected manifold-like cluster in the ambient feature space, with strong separation from random permutations and perturbed near-magic squares.
- **Physical and Geometric Intuition:** The introduction—built around the stacked-coin checkerboard and balance metaphor—is particularly effective in motivating the geometric embedding and the covariance viewpoint. The “Magic Gem” terminology is evocative and used consistently.

These contributions are well aligned with the mission of *Journal of Experimental Mathematics*: the work is computationally grounded, explores structure via experiments, and leads to clear conjectures and further questions.

---

## 3. Major Comments and Suggestions

### 3.1. Scope and Sharpness of the Zero-Covariance Theorem

The Zero-Covariance Theorem is the conceptual centerpiece and is already presented clearly. There are, however, a few points where sharpening the mathematical framing would strengthen the result:

1. **Role of Permutations vs. General Arrays.** The theorem is stated for permutations of \(\{1,\dots,n^2\}\). It would help to state explicitly:
   - Whether the equivalence continues to hold for general real-valued arrays with distinct entries (or more generally, with arbitrary real entries subject to sum constraints).
   - Which parts of the proof genuinely use the permutation assumption (e.g., normalization, total sum, or distinctness), and which are purely linear-algebraic consequences of the magic-sum conditions.
   Clarifying this would make it easier for readers to see how the covariance characterization generalizes to related combinatorial objects (Latin squares, semi-magic squares, etc.).

2. **Connection to the Classical Linear System.** At some level, the magic property is equivalently a rank condition on the system of row/column/diagonal sum equations. The covariance conditions can be seen as a particular change of basis/normalization of this system. I suspect that there is a concise linear-algebraic statement along the lines of:
   > “The vanishing of the four covariances corresponds to the vanishing of the inner products of the value vector with four canonical spatial direction vectors; these span the same constraint subspace as the classical magic-sum equations.”
   Making this relationship explicit—even if briefly—would help situate the theorem relative to existing algebraic characterizations.

3. **Uniqueness of the Covariance Conditions.** The paper describes these four covariances as “natural” and “minimal,” but does not quite spell out in what sense they are minimal. Are there other independent choices of four linear functionals of the positions that would serve just as well? Is there a geometric reason why \(X\), \(Y\), \(X+Y\), and \(X-Y\) are canonical? A short remark addressing this (perhaps in the discussion) would be valuable.

### 3.2. Algorithmic Claims and Complexity Analysis

The gradient-based algorithm is one of the most intriguing aspects, and the complexity claim \(O(n^4 \log(1/\varepsilon))\) is potentially impactful. I have a few requests for clarification:

1. **Precise Statement of the Complexity Theorem.** At present, the complexity result is somewhat blended into the narrative. I would recommend formulating a self-contained theorem (or proposition) along the lines of:
   > “Under assumptions A–C on the step size schedule and the objective landscape, the gradient descent procedure converges to a configuration with covariance norm at most \(\varepsilon\) in at most \(C n^4 \log(1/\varepsilon)\) steps.”
   This should include an explicit definition of \(\varepsilon\): is it a bound on the Euclidean norm of the four covariances, on the maximum row/column/diagonal deviation, or something else?

2. **From Real-Valued Minimizers to Discrete Magic Squares.** The algorithm is phrased as gradient descent on a continuous relaxation, but the object of interest is a permutation matrix. The manuscript indicates that the method reliably returns exact magic squares (for \(n=4\)), but the mechanism of “re-discretization” is not fully formalized. Is there an explicit projection step onto the permutation group (e.g., via assignment solving), or is the algorithm constrained to permutations at all times (e.g., via structured moves)? Clarifying this is important both for correctness and for the complexity accounting.

3. **Behavior for Larger \(n\).** The experiments in the current version still focus primarily on \(n=4\). While I do not think it is necessary to provide exhaustive data for large \(n\), it would be very helpful to:
   - Report at least limited experiments for one or two larger sizes (say \(n=5\) or \(n=6\)), even if the enumeration is impossible, to see whether convergence remains robust or whether local minima become problematic.
   - Discuss qualitatively how the “ruggedness” of the covariance landscape is expected to scale with \(n\), and whether the empirical behavior at \(n=4\) is likely to generalize.

4. **Comparison to Other Continuous Approaches.** There is a small but nonzero literature on continuous relaxations of combinatorial problems (e.g., doubly stochastic relaxations for Latin squares, SDP-based methods). A short paragraph comparing your covariance-based objective to these more standard relaxations—for instance, emphasizing that yours is geometrically and physically motivated—would help readers place the algorithmic contribution in context.

### 3.3. Interpretation of the Geometric and Topological Results

The geometric and topological analyses are a delight to read, but I think the paper could be slightly more explicit about **what we learn** from each technique beyond “separation from random.”

1. **Convex Hull Configurations (21 Types).** The classification by \((V,F,I)\) is very nice, and Figure 3 (as described in the text) appears to communicate the diversity well. What is still slightly undersold is *why* these 21 configurations matter mathematically. For example:
   - Are certain configurations associated with particular symmetry types or known Dudeney classes?
   - Do the extreme configurations (e.g., with unusually large or small volume) correlate with any spectral or combinatorial invariants?
   Even a few short observations or conjectures would turn this from “taxonomy” into “structural insight.”

2. **Persistent Homology and Manifold Learning.** The persistent homology analysis shows that the magic gems form a single connected component with relatively simple higher-dimensional Betti structure, while random permutations look quite different. However, at the present scale (880 points in a fairly low-dimensional embedding), these tools can sometimes appear as overkill to skeptical readers.
   - I suggest adding one paragraph explicitly acknowledging the modest scale and emphasizing that the main value here is *qualitative characterization* (e.g., “the magic manifold is coherent and lacks spurious topological holes in this resolution”), rather than deep topological classification.
   - It may also help to mention the robustness of these conclusions across filtration parameters and embedding choices (e.g., stability of Betti barcodes under reasonable perturbations).

3. **Earth Mover’s Distance and Clustering.** The EMD analysis is compelling and ties naturally into the idea of “small deformations” between magic squares. To strengthen this section:
   - Clearly specify the ground metric and normalization used in the EMD (e.g., distances between cell positions, weighting by magnitude differences).
   - Explicitly relate the reported nearest-neighbor distance (\(0.021 \pm 0.011\)) to a baseline from random permutations or one-swap perturbations, perhaps via standardized effect sizes. Some of this appears to be present, but could be drawn out more clearly in the prose.

### 3.4. Structure, Emphasis, and Length

The revised manuscript already flows much better than the typical “list-like” technical report, and the introduction and conclusion are particularly well crafted. I have only minor structural suggestions:

1. **Spherical Harmonics Section.** The spherical harmonic decomposition is interesting and visually attractive but still slightly feels like an optional “extra.” You have made a commendable effort to connect it to rotational symmetries and spectral signatures, but the reader may still wonder: *what would we lose if this section were omitted?* A brief paragraph at the start or end of that section stating explicitly what new insight the harmonic spectrum provides—beyond what is already captured by simpler shape statistics—would help justify its inclusion.

2. **Results vs. Discussion Overlap.** Sections summarizing the geometric statistics (volumes, angles, EMD, manifold structure) and the later discussion sometimes repeat high-level messages (e.g., “magic squares form a single connected manifold,” “geometric invariants are tightly concentrated”). Consider whether you can slightly consolidate or cross-reference to reduce redundancy; this is not a major issue, but a modest trim could tighten the paper.

3. **Target Audience and Level of Detail.** The manuscript is admirably interdisciplinary, drawing on statistics, topology, and optimization. On a few occasions, however, the level of detail in side topics (e.g., technicalities of manifold learning algorithms) may exceed what is strictly necessary for a JEM audience. You might consider moving some lower-level algorithmic details to an appendix or to the code repository, keeping the main text focused on mathematical structure and experimental findings.

---

## 4. Minor Comments and Editorial Suggestions

- **Notation Consistency:**  
  Ensure that the symbols \((X,Y,Z)\), positional indices \((i,j)\), and random variables used in the covariance definitions are consistently distinguished. In particular, clarify early whether \(X\) and \(Y\) are treated as discrete random variables uniformly distributed over grid cells, or as deterministic coordinate functions with an implied averaging over cells.

- **Terminology – “Manifold”:**  
  You frequently refer to the “manifold” of magic squares. While this is heuristically apt and visually suggested by the embeddings, strictly speaking what we see is a finite point set lying near a low-dimensional subset. It may be worth inserting a brief caveat (e.g., “we use ‘manifold’ informally to describe the low-dimensional structure of the embedded point cloud”) to preempt nitpicking.

- **Historical Context:**  
  The introduction’s historical section is well written. You might consider explicitly citing Trump’s enumeration paper in connection with the exact count of 880, and perhaps add one or two sentences connecting your geometric invariants to classical invariants (e.g., magic sum, symmetry classes) so that readers see continuity with the older literature.

- **Numerical Values in Abstract and Conclusion:**  
  The abstract and conclusion report several quantitative results (e.g., hull volume \(84.1 \pm 7.1\), angular uniformity \(0.569 \pm 0.000\)). It would be helpful, perhaps in a short footnote or in the main text where these are first introduced, to indicate clearly:
  - the exact definition of each statistic,
  - whether the \(\pm\) denotes standard deviation, standard error, or a confidence interval.

- **Figures and Captions:**  
  The figures appear to be of high quality, and the new “hero” and configuration gallery figures are particularly effective. I have only two small suggestions:
  - In the gallery of 21 configurations, consider adding a compact legend or table mapping each configuration to its frequency among the 880 squares.
  - In the manifold/embedding figures, be explicit in the captions about whether each point represents a unique magic square or whether symmetry-related variants have been quotiented out.

- **Typos and Minor Style Issues:**  
  I noticed only a few very minor typographical issues (e.g., occasional missing hyphenation in “zero covariance” vs. “zero-covariance”). A final careful proofread should catch these.

---

## 5. Recommendation

In my view, this is **exactly the sort of work that *Journal of Experimental Mathematics* should publish**: it combines substantial computation, genuine mathematical insight, and clear exposition, and it opens up a new geometric angle on a classical discrete object. The Zero-Covariance Theorem and the geometric taxonomy of Magic Gems are, in my opinion, enduring contributions that others can build on. The algorithmic component, while still most convincingly demonstrated for \(n=4\), is promising and well motivated.

My recommendation is **accept with minor revisions**, primarily to (i) sharpen the formal statement and discussion of the algorithmic complexity result, (ii) clarify the scope and generality of the Zero-Covariance characterization, and (iii) slightly refine the interpretation of the topological and geometric analyses. These changes should not require substantial new computation or restructuring, but they will make the paper more robust and more broadly accessible to the journal’s readership.

Subject to these relatively modest revisions, I would be pleased to see this manuscript published in *Journal of Experimental Mathematics*.


