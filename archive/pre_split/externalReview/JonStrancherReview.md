### Referee report for *“Magic Gems: A Polyhedral Framework for Magic Squares”*

*(Prepared in a referee-style tone from the perspective of a mathematician/statistician; I am an AI system and not a real Stanford faculty member.)*

### Summary (what the paper tries to do)
The manuscript introduces “Magic Gems”: embed an \(n\times n\) normal magic square as a centered 3D point cloud \((x_{ij},y_{ij},z_{ij})\) with \(z\) equal to centered cell values, and take the convex hull as a polyhedron. The paper then emphasizes a statistical viewpoint: classical line-sum constraints manifest as vanishing covariances between “position” and “value”. Building on this, the authors define an “energy” \(E\) as a sum of squared covariances and interpret magic squares as “ground states”/isolated minima in an energy landscape. The paper includes large computational experiments and many figures.

### Overall evaluation
- **Overall interest**: The geometric embedding (“topography” viewpoint) is visually appealing and pedagogically effective. The covariance language is a nice bridge between combinatorics and elementary statistics/linear algebra.
- **However**: **The central “energy characterization” claim as currently formulated is false for \(n\ge 4\)**. In particular, **there exist non-magic \(4\times4\) permutations with \(E=0\)** under the paper’s definition. This undermines the main theorem’s extension beyond \(n=3\) and requires substantial revision of claims in the abstract/introduction/methodology/results/discussion/conclusion.
- **Recommendation to the editor**: **Major revision**. I would encourage resubmission after the authors (i) correct the central claim, (ii) either redefine the energy so that an “iff” theorem holds for all \(n\) (with proof), or explicitly reframe \(E\) as a relaxation/heuristic that defines a larger class than magic squares, and (iii) revise the computational narrative accordingly.

### Major issue 1: The proposed energy \(E\) does **not** characterize magic squares for \(n\ge 4\)
In `sections/methodology.tex` the energy is defined as
\[
E(S)=\Cov(X,Z)^2+\Cov(Y,Z)^2+\Cov(D_{\mathrm{main}},Z)^2+\Cov(D_{\mathrm{anti}},Z)^2,
\]
with \(X,Y\) the (centered) coordinate functions and \(D\) diagonal indicators. The paper asserts (in multiple places, sometimes implicitly) that “\(E(S)=0\) is equivalent to \(S\) being magic” (proved by exhaustive enumeration for \(n=3\), then conjectured/claimed by sampling for \(n=4,5\)).

**This equivalence fails already for \(n=4\).** Here is an explicit counterexample (a permutation of \(\{1,\dots,16\}\)):

\[
S=\begin{pmatrix}
9&4&12&3\\
16&1&14&7\\
10&15&11&8\\
2&5&6&13
\end{pmatrix}.
\]

- The magic constant is \(M(4)=34\).
- Diagonal sums are correct: main diagonal \(9+1+11+13=34\), anti-diagonal \(3+14+15+2=34\).
- But **row sums** are \(28,38,44,26\) and **column sums** are \(37,25,43,31\), so **this is not a magic square**.
- Under the manuscript’s coordinate/covariance definitions (and also under the project’s implementation `src.analysis.compute_total_magic_energy_v2`), one has
  - \(\Cov(X,Z)=\Cov(Y,Z)=\Cov(D_{\mathrm{main}},Z)=\Cov(D_{\mathrm{anti}},Z)=0\), hence **\(E(S)=0\)**.

So: **\(E=0\) defines a strictly larger set than magic squares for \(n=4\)**, and therefore Conjecture~\(\ref{conj:general}\) in the Appendix (as stated) is false.

#### Why this failure is structurally unavoidable
The issue is not “bad luck”; it is a linear-algebraic degree-of-freedom problem.
- \(\Cov(X,Z)=0\) is one linear constraint on the vector of column sums (a weighted sum of deviations). It is **not** equivalent to “all column sums equal”. For \(n\ge 4\) there is an \((n-2)\)-dimensional family of column-sum deviation patterns consistent with \(\Cov(X,Z)=0\) (the Appendix itself notes this phenomenon).
- Likewise \(\Cov(Y,Z)=0\) is only one constraint on row sums.
- Adding the two diagonal constraints gives only two further linear conditions.

Thus, for \(n\ge 4\), it is expected that there are many non-magic permutations satisfying these four constraints.

### Major issue 2: The paper’s narrative repeatedly overstates “iff” claims
Even if the authors keep the present \(E\), the manuscript must revise language that implies a full characterization. Examples:
- **Abstract**: it is mostly careful (the \(n=3\) exhaustive “iff” is stated), but it suggests “strong evidence that this characterization extends”. Given the \(n=4\) counterexample above, that sentence cannot stand as-is.
- **Methodology section** around the energy definition: statements like “An arrangement achieves zero energy precisely when it is uncorrelated with all four directions—the definition of a magic square” are incorrect for \(n\ge 4\).
- **Conclusion** currently says “an arrangement … is a magic square **if and only if** the covariance between spatial position and assigned value vanishes.” Earlier sections explicitly show \(\Cov(X,Z)=\Cov(Y,Z)=0\) is insufficient; and even the full \(E\) is insufficient for \(n=4\).

These should be rewritten with sharp quantifiers:
- “Magic \(\Rightarrow\) these covariances vanish” (true, and easy).
- “For \(n=3\), the common zeros of the four covariances are exactly the 8 magic squares” (true, by enumeration).
- “For \(n\ge 4\), the common zeros include magic squares but also additional configurations; understanding these additional zeros is an open direction” (true).

### Major issue 3: What to do now (two viable revision paths)
I see two constructive ways forward.

#### Path A (recommended): Redefine the energy so the main theorem becomes true for all \(n\)
If the editorial goal is an **honest “characterization” theorem**, the energy must encode **all** row and column equalities, not just one linear combination.

A clean covariance-based fix that stays close to your narrative:
- Let \(R_k(i,j)=\mathbf{1}\{i=k\}\) be the indicator of row \(k\) and \(C_\ell(i,j)=\mathbf{1}\{j=\ell\}\) the indicator of column \(\ell\).
- Then \(\Cov(R_k,Z)=0\) is equivalent to “row \(k\) has the correct mean (hence correct sum)”, and similarly for columns.

Define
\[
E_{\mathrm{full}}(S)=\sum_{k=0}^{n-1}\Cov(R_k,Z)^2+\sum_{\ell=0}^{n-1}\Cov(C_\ell,Z)^2+\Cov(D_{\mathrm{main}},Z)^2+\Cov(D_{\mathrm{anti}},Z)^2.
\]
(You can drop one row and one column indicator because of linear dependence, i.e. use \(k=0,\dots,n-2\) and \(\ell=0,\dots,n-2\).)

Then the key theorem becomes:
- **Theorem (all \(n\))**: For an arrangement of \(\{1,\dots,n^2\}\), \(E_{\mathrm{full}}(S)=0\) iff \(S\) is a (normal) magic square.
- Proof is immediate from the equivalence between each covariance and the corresponding line-sum constraint.

This revision would remove the need for probabilistic “evidence” to support an “iff” claim. Computations could then focus on the genuinely interesting parts: geometry of the convex hull, distribution of hull invariants across equivalence classes, perturbation gaps, etc.

A variation that retains the “moment / polynomial” feel: use an orthogonal basis \(p_m\) on \(\{0,\dots,n-1\}\) and require \(\Cov(p_m(X),Z)=0\) for all \(m=1,\dots,n-1\) (and similarly for \(Y\)). This turns your current \(X,Y\) condition into the **first** moment constraint in a complete set.

#### Path B: Keep the current \(E\) but reframe as a relaxation defining a larger class
If the authors feel strongly about having a 4-term “minimal” energy, then the paper should:
- Explicitly rename it (e.g., **“first-moment covariance energy”**) and state up front that it is **not** equivalent to being magic for \(n\ge 4\).
- Study the set \(\{S: E(S)=0\}\) as a new combinatorial object: how large is it, how is it structured, does it intersect semi-magic sets, etc.
- Reinterpret some claims: magic squares are *among* the global minima, but not the only ones.

This path is viable, but it changes the central message and would require careful editorial framing.

### Major issue 4: Computational evidence and “no counterexamples” claims
The manuscript currently uses random sampling to suggest there are no non-magic \(E\approx 0\) configurations for \(n=4,5\). Given the explicit \(4\times4\) counterexample above, the sampling argument should be revised:
- Random sampling is not a reliable tool for a converse statement when solutions may live in an extremely sparse arithmetic subset.
- The table in `sections/results.tex` already reports a nonzero “zero-energy fraction” for \(n=4,5\) (with a numerical threshold). These should not be dismissed as “artifacts” without inspecting the actual near-zero samples.
- At minimum, the authors should add a step: whenever \(E < \varepsilon\), explicitly test all line sums and classify the configuration (magic / semi-magic / diagonal-correct only / etc.).

### Comments on the geometric “Magic Gem” component
The convex-hull construction is attractive, but at present the *mathematical payload* of the polyhedron seems secondary relative to the covariance discussion:
- Most theorems/propositions concern covariance and do not use the convex hull.
- Hull volume and hull-vertex counts are reported, but the paper itself observes that these are not extreme among random arrangements.

Suggestions to strengthen the “polyhedral framework” aspect:
- Clarify what structure is genuinely **polyhedral** (faces/adjacency types, f-vectors, symmetry groups of the hull, stability of hull under perturbations, classification of hull types across equivalence classes).
- If the aim is classification: is the map “\(D_4\)-equivalence class \(\to\) Magic Gem (convex hull up to rigid motion)” injective? If not, how degenerate is it?
- Consider emphasizing the embedding as a discrete surface / height function, and use the convex hull as one of several shape descriptors rather than *the* defining object.

### Figures and captions (high-level review)
Overall, the figures are polished and informative. The main concern is **density**: several are 9-panel composites with long, interpretive captions.

- **Construction/symmetry figure (`fig02_combined_construction_symmetries.pdf`)**
  - Strong pedagogical figure.
  - Caption is long but helpful; consider adding explicit panel labels (a,b,c,...) embedded in the graphic for quick cross-reference.

- **Energy landscape figure (`figures/energy_landscapes_comparison.png`)**
  - Visually compelling; log-scale histograms communicate rarity well.
  - Suggestions:
    - Add panel letters and ensure axis-font sizes remain legible at journal column width.
    - The red dashed \(E=0\) line is good; consider an inset zoom near \(E\approx 0\) for \(n=4,5\) to discuss “near-zero” events transparently.
    - Be cautious interpreting the “entropy” of a binned histogram as “ruggedness”; it is binning-dependent.

- **Perturbation analysis figure (`Complete_Perturbation_Analysis_n345.png`)**
  - The idea is excellent and the plot is strong.
  - This is likely too dense for print as a single figure; consider splitting into (i) distributions + scaling, and (ii) population scatter + summary table.

- **Scaling summary figure (`Figure7_ScalingSummary.png`)**
  - Clear layout.
  - The quadratic fit and reporting \(R^2=1\) with only three points is statistically misleading (any quadratic will fit 3 points perfectly). You do mention this caveat in the text; I would still remove the \(R^2\) box or soften the visual emphasis.

- **Captions**
  - Many captions contain conclusions (“strong evidence”, “novel finding”, “scale-invariant”). In Experimental Mathematics, I would encourage moving interpretive claims into the main text and keeping captions more descriptive.

### Writing/notation/exposition suggestions
- **Define covariance precisely once**: whether you use \(\frac{1}{N}\) or \(\frac{1}{N-1}\) scaling is not central, but consistency helps.
- **Be careful with “position”**: you use numeric coordinates \(X,Y\) (first moment). If you adopt Path A above (row/col indicators), the story becomes cleaner and the “iff” theorem becomes correct.
- **Avoid over-physical metaphors where claims are mathematical**: the “ground state / basin of attraction” language is fine as intuition, but should not replace precise statements.
- **Quantify sampling**: list seeds, exact \(\varepsilon\) thresholds for “near-zero”, and the number of near-zero samples inspected.

### Minor points (quick fixes)
- In `sections/results.tex` early discussion mentions a “mean energy \(\approx 2.5\)” for \(n=3\), but the later table/plots report mean \(\approx 4.44\). Please reconcile.
- You force many figures with `[H]`. That often harms LaTeX float placement; consider standard `[t]`/`[htbp]` unless there is a strong reason.
- When giving counts for \(4\times4\) and \(5\times5\) magic squares/equivalence classes, please cite a definitive source.

### Bottom line
This project has real strengths—especially the visualization and the clean “covariance as balance” viewpoint. But for journal publication, the central “energy characterization” must be corrected.

If the authors adopt **Path A** (energy based on a full row/column indicator basis), they can produce an **honest, general, provable** characterization for all \(n\), and then the computational/visual sections become supporting evidence and exploration rather than a substitute for correctness.

If the authors instead keep the 4-term energy, the paper should be reframed as proposing a **coarse statistical relaxation** whose zero set strictly contains the magic squares, and then the interesting question becomes: what is that larger zero set, and how does it relate to known combinatorial classes?
