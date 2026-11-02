## Referee Report on “Magic Gems: A Polyhedral Framework for Magic Squares”

Manuscript: `[Magic Gems: A Polyhedral Framework for Magic Squares]` ([manuscript PDF](file:///Users/kylemathewson/magicGem/output/magic_gems.pdf))  
Journal: *Experimental Mathematics*

### 1. Summary and overall assessment

The manuscript introduces **Magic Gems**, a geometric representation of magic squares as point clouds in \(\mathbb{R}^3\) together with their convex hulls, and develops an associated **covariance-based energy functional** whose zeros are intended to characterize magic squares.  The authors prove a *Zero-Covariance Theorem* in which (for \(n=3,4\)) vanishing covariances \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=0\) are claimed to be equivalent to the magic square property, and they define an energy \(E(S)\) combining these covariances with diagonal constraints.  Extensive computations (exhaustive for \(n=3\), very large random samples for \(n=4,5\)) are used to explore the “energy landscape” on the permutation space and to support a conjectural extension to all \(n\).

Conceptually, this is an appealing and well-motivated piece of work: it connects classical combinatorial objects (magic squares) with convex geometry, covariance matrices, and physical analogies (moment of inertia, energy landscapes).  The computational component is substantial and in the spirit of *Experimental Mathematics*, and the exposition is generally clear and engaging.  However, in its current form there are **important issues in the logical structure of the main theorems, and in the distinction between proved results and conjectural statements**, as well as some over-strong wording about what the computations establish.  I believe the paper is potentially publishable in *Experimental Mathematics* after a **substantial revision** that (i) carefully separates theorem from conjecture, (ii) repairs or removes a flawed argument in the proof of the Zero-Covariance Theorem, and (iii) tightens some of the exposition and experimental claims.

Subject to these revisions, I would be inclined to recommend publication.

### 2. Mathematical correctness and logical structure

#### 2.1 Zero-Covariance Theorem and diagonal conditions

In `introduction.tex` and especially `methodology.tex`, the **Zero-Covariance Theorem** (Theorem~\ref{thm:zero_covariance}) is stated as:

- For \(n\in\{3,4\}\), an arrangement \(S\) of \(\{1,\dots,n^2\}\) is a magic square *if and only if* \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=0\).

However, the written proof in `methodology.tex` is not fully correct as it stands:

- The derivation that **magic \(\Rightarrow\) zero covariance** is sound: starting from equal row and column sums, the authors deduce \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=0\).  This part is clear and correct.
- For the converse (**zero covariance \(\Rightarrow\) equal column sums**), the reduction to an equation involving column sums \(C_j\) and deviations \(\delta_j=C_j-M(n)\) is fine, but the argument concluding that all \(\delta_j\) vanish is incorrect in the current text.  Lines 169–180 of `methodology.tex` assert, in effect, that from
  \[
     \sum_j \delta_j = 0,\qquad \sum_j \bigl(j-\tfrac{n-1}{2}\bigr)\delta_j = 0
  \]
  one can conclude \(\delta_j=0\) for all \(j\), but this is not true for general \(n\): these are just two linear constraints on an \(n\)-dimensional vector.  The fact that the \(\delta_j\) are realized as column sums of a permutation of \(\{1,\dots,n^2\}\) imposes further arithmetic constraints, but these are not analyzed in the main proof.
- Moreover, even if one could show from covariance that all row and column sums equal \(M(n)\), the manuscript then claims that the **diagonal conditions follow automatically** from row/column sums and the fixed total sum
  (see lines 182–184 of `methodology.tex` and the similar sentence in `appendix.tex`).  I am not aware of a general argument that for normal magic squares (\(1,\dots,n^2\)) and \(n\ge 4\), equal row and column sums force equal diagonal sums; indeed, in the general literature one distinguishes *semi-magic* squares (rows and columns only) from fully magic ones.  At minimum, this implication should either be proved carefully for \(n=3,4\) (possibly using the permutation constraints) or replaced by an explicit appeal to computation.

The appendix (`appendix.tex`) gives a more careful order-by-order discussion (Steps 4–5), and for \(n=3\) and \(n=4\) the authors **do** rely on a mixture of algebraic reductions and exhaustive / large-scale verification.  This is perfectly acceptable in an experimental-mathematics paper, but the logic needs to be made transparent:

- In the main body, I strongly recommend **rephrasing Theorem~\ref{thm:zero_covariance}** so that:
  - The direction “magic square \(\Rightarrow\) \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=0\)” is stated and proved for **all** \(n\ge 3\) (this is already fine).
  - The converse direction is:
    - Either restricted explicitly to \(n=3\) and \(n=4\) and proved *via* the detailed appendix plus exhaustive / large-scale search; or  
    - Moved entirely into the appendix as a theorem for \(n=3,4\) with a clear statement that the general case is conjectural.
- Anywhere that the text currently suggests that equal row/column sums *automatically* imply diagonal sums (for the normal magic-squares setting) should be revised.  If a proof exists for \(n=3,4\) using your covariance formulation, it would be good to present it explicitly; otherwise, I would treat the *diagonal* part as a separate, computationally verified statement.

At present, a reader could be misled into thinking that the “if and only if” characterization has a fully algebraic proof for \(n=3,4\) and a near-proof for general \(n\), whereas in fact the reverse direction rests crucially on computational checks and on additional diagonal conditions (as you clearly recognize in Conjecture~\ref{conj:general}).

#### 2.2 Energy Characterization Theorem

In `methodology.tex`, the **Energy Characterization** (Theorem~\ref{thm:energy_char}) asserts that for an arrangement \(S\) of \(\{1,\dots,n^2\}\),
\[
E(S) = 0 \quad\Longleftrightarrow\quad S\ \text{is a magic square},
\]
where \(E\) combines the covariance and diagonal energy terms.  The proof explicitly invokes Theorem~\ref{thm:zero_covariance} and then uses diagonal means to conclude that both diagonals sum to \(M(n)\).

Given the issues noted above:

- As written, Theorem~\ref{thm:energy_char} is **fully justified only in those cases where you have actually proved the zero-covariance characterization**, i.e. currently \(n=3,4\) and only with some reliance on computation.
- For general \(n\), this equivalence is exactly what is restated as Conjecture~\ref{conj:general} in `appendix.tex`.  To avoid logical circularity and overstatement, I recommend:
  - Downgrading Theorem~\ref{thm:energy_char} to a **proposition** explicitly restricted to \(n=3,4\) (or to \(n=3\) if you prefer purely exhaustive arguments); and
  - Making it explicit in the main text that for general \(n\), the statement “\(E(S)=0\) if and only if \(S\) is magic” is **conjectural**, with Conjecture~\ref{conj:general} the precise formulation.

This is mostly a matter of presentation and honesty about what is rigorously established vs. empirically supported, but it is important for a mathematics audience.

#### 2.3 Other mathematical points

- The background material in `background.tex` and the geometric constructions in `methodology.tex` are mathematically sound and clearly explained.  The connections to convex hulls, the moment of inertia tensor, and covariance are correct and nicely tied together.
- The enumerative data for magic squares of size \(3,4,5\) (number of squares, equivalence classes, probabilities, etc.) in `background.tex` and `appendix.tex` appear consistent with the known literature.  It would be helpful to ensure that the standard enumeration references are cited explicitly (for example, the known counts for \(4\times4\) and \(5\times5\) magic squares).
- In `results.tex`, some numerical values seem slightly inconsistent:
  - Earlier you emphasize a minimum perturbation gap of \(\Delta_3=0.0988\) for \(n=3\), but later the scaling discussion around lines 377–381 mentions a gap “approximately 0.02” for \(n=3\).  These numbers should be reconciled.
  - Table~\ref{tab:landscape_stats} reports a “zero-energy fraction” for \(n=4,5\) despite the text saying that no zero-energy configurations were observed.  If this “fraction” is a smoothing or binning artifact rather than a literal count of zero-energy samples, please clarify; otherwise it may confuse readers.

Overall, aside from the main logical issue around the zero-covariance and energy characterizations, the mathematics appears careful and correct.

### 3. Computational experiments and “Experimental Mathematics” aspects

The computational component is a strong point of the paper.  The authors implement the framework in Python, use NumPy/SciPy/Matplotlib, and explore:

- Exhaustive enumeration of all \(9!=362{,}880\) arrangements for \(n=3\).
- Large-scale random sampling for \(n=4\) (60 million permutations) and \(n=5\) (400 million permutations).
- Complete single-swap perturbation analysis for all \(n=3\) and \(n=4\) magic squares, and a representative set of \(n=5\) squares.

These experiments convincingly illustrate:

- That magic squares indeed sit at **energy zero** and are **isolated local minima** in the covariance energy landscape, at least in all tested cases.
- Scaling behavior of energy distributions (peak energy approximately quadratic in \(n\)), the behavior of perturbation gaps, and the rarity of magic squares in the permutation space.

However, some of the **interpretive language is too strong** given that all evidence for \(n\ge 4\) is necessarily empirical:

- Phrases like “definitively confirming that magic squares are isolated local minima” and “definitively confirming that these are the only zero-energy configurations” overstate what can be concluded from finite sampling, even when that sampling is very extensive.  I recommend rephrasing throughout to emphasize **“strong numerical evidence,” “no counterexamples found in 460+ million sampled configurations,”** etc., which is both accurate and still quite compelling.
- In several places you describe magic squares as the **“unique ground states”** of the energy functional.  Strictly speaking, there are many magic squares (and many equivalence classes), so “unique” here really means something like “all ground states are magic squares, and conversely”; it might be clearer to say: “the set of ground states (zero-energy configurations) coincides with the set of magic squares” and then distinguish what is proven from what is conjectural.
- The “landscape entropy” used as a measure of distributional complexity is an interesting idea, but I did not see a precise **definition** in the text segments provided.  Since *Experimental Mathematics* readers will include both analysts and combinatorialists, I suggest explicitly defining how this entropy is computed (e.g., Shannon entropy of a histogram over discrete energy bins) the first time it appears.

Regarding reproducibility and alignment with the journal’s ethos:

- You indicate in `appendix.tex` that “source code for all analyses and figures is available in the supplementary materials.”  This is excellent and aligns well with the journal’s encouragement to share programs and data.  According to the *Experimental Mathematics* submission guidelines on the EMIS site (`https://www.emis.de/journals/EM/expmath/submission.html?utm_source=openai`), programs themselves are not printed but can be provided as supplementary material or via an author-maintained web page.  It would be good to:
  - Specify a stable URL (or DOI-backed repository) where the code and data will reside, and
  - Briefly describe the structure of the code (e.g., which scripts reproduce each major figure) in the appendix or a short README for reproducibility.

### 4. Exposition, tone, and structure

The paper is generally well written, and I found many of the explanations in `discussion.tex` and `conclusion.tex` both clear and engaging.  That said, a few improvements would make the manuscript more concise and mathematically focused:

- **Tone and metaphors.**  Physical analogies (energy landscapes, balls rolling to local minima, “stones at the bottom of valleys”) are effective and suitable for *Experimental Mathematics*, but they are sometimes repeated at length.  For example, the “needle in a haystack” metaphor for the rarity of magic squares appears in multiple places.  I would suggest pruning a few of these repetitions to keep the narrative tight.
- **Length and redundancy.**  `discussion.tex` is quite extensive.  Some subsections (e.g., “Magic Squares as Ground States” and “The Rarity of Magic Configurations”) restate similar points in slightly different language.  Condensing these sections by about 20–30% would likely improve readability without sacrificing content.
- **Clarity of terminology.**  The term “Magic Gem” sometimes refers to the **convex hull** of the point cloud, sometimes to the point cloud itself, and sometimes to the combination of both.  It would help to fix a precise convention (e.g., “Magic Gem” = convex hull; “Magic Gem point cloud” = the set of points) and adhere to it.
- **Statistical language.**  When discussing covariance distributions and “probability densities,” be mindful of the discrete nature of the sample space.  You already handle this reasonably well, but occasionally phrases like “density near zero energy is essentially zero” could be sharpened by referring explicitly to empirical histograms or sample frequencies.

Overall, the exposition is quite strong; these suggestions are primarily about polishing and tightening rather than major rewrites.

### 5. Conformity to *Experimental Mathematics* submission guidelines

Based on the journal’s submission instructions on the EMIS site (`https://www.emis.de/journals/EM/expmath/submission.html?utm_source=openai`), I would highlight the following points:

- **Abstract length.**  The guidelines request an abstract of **at most 150 words** in the article’s language (with an English translation if the article is not in English).  The current abstract in `abstract.tex` is noticeably longer than 150 words.  I recommend preparing a more concise abstract (ideally 120–150 words) that focuses on:
  - The Magic Gem construction;
  - The zero-covariance characterization;
  - The energy functional and major computational findings.
- **Title page and author information.**  The guidelines require a title page with title, postal addresses, affiliations, and email addresses for all authors.  Please check that your LaTeX source (outside the provided section files) complies with this.
- **Language and style.**  The manuscript is written in clear English and mostly meets the journal’s demands for clarity and conciseness.  After trimming the abstract and a few repetitive passages, it should fit comfortably within the stylistic expectations.
- **References.**  The guidelines ask for full bibliographic information (author, title, journal, volume, year, pages).  I have not seen `references.bib`, but given the importance of classical results on magic squares and enumerations, please ensure:
  - All numerical facts (numbers of magic squares, equivalence classes, etc.) are supported by references.
  - Recent connections to eigenvalue problems, statistical mechanics, or related frameworks are properly cited where mentioned in `introduction.tex` and `discussion.tex`.
- **Supplementary materials.**  The journal encourages posting tables, programs, and data sets on an author-maintained site and providing the URL with the final files.  Since your work revolves around substantial computation, it would be highly appropriate to:
  - Package your Python code and data used to generate the figures and tables as supplementary material.
  - Include a short note in the appendix describing these resources.

Addressing these points should ensure smooth handling by the journal’s production process.

### 6. Specific suggestions for improvement

Below is a consolidated list of concrete revisions I recommend:

- **Theoretical clarity**
  - Rewrite Theorem~\ref{thm:zero_covariance} to separate:
    - The general direction “magic \(\Rightarrow\) zero covariance,” and
    - The converse for \(n=3,4\), explicitly justified via the appendix and computations.
  - Remove or correct the flawed linear-algebra argument around lines 169–180 of `methodology.tex` and replace it with a precise statement of what is proved algebraically and what is verified computationally.
  - Clarify the role of diagonal constraints: either prove, for each of \(n=3,4\), that zero covariance forces the diagonal sums to be \(M(n)\), or explicitly state that this has been checked computationally and is an empirical fact rather than a purely algebraic consequence.
  - Restrict Theorem~\ref{thm:energy_char} to the range of \(n\) for which you have a genuine proof; move the general-\(n\) statement into Conjecture~\ref{conj:general} (or vice versa) so there is no duplication or contradiction.

- **Experimental claims**
  - Systematically soften language like “definitively confirming,” “unique ground states,” etc., in `results.tex`, `discussion.tex`, and `conclusion.tex`.  Replace with phrases such as “our computations provide strong evidence that …” and “in all of the 460+ million arrangements tested, we observed no counterexamples to …”.
  - Explicitly define “landscape entropy” when it first appears, including the formula used.
  - Reconcile numerical discrepancies (e.g., the minimum perturbation gap for \(n=3\)) and ensure that all reported numbers match those in `stats.tex`.

- **Exposition and structure**
  - Shorten the abstract to comply with the journal’s 150-word guideline.
  - Consider trimming `discussion.tex` by removing or merging paragraphs that repeat the same intuition (energy wells, rarity, needle-in-a-haystack analogies).
  - Fix the terminology around “Magic Gem” vs. point cloud vs. convex hull so a reader always knows which object is meant.
  - Ensure that each multi-panel figure is clearly described in the text and that captions remain legible at the journal’s print size (some of the 9-panel figures may benefit from being split or slightly simplified).

- **Bibliographic and supplementary materials**
  - Check that all classical and recent references on magic squares, convex polytopes, and covariance-based characterizations are properly cited, in the format requested by *Experimental Mathematics*.
  - Provide a stable URL or repository for the code and data (e.g., a GitHub repository with a tagged release, mirrored to a long-term archive such as Zenodo), and mention this in the appendix and cover letter.

### 7. Recommendation

In summary, I find the Magic Gem framework conceptually interesting and well suited to *Experimental Mathematics*, and I am impressed by the scope of the computational exploration.  The main concern is the current presentation of the zero-covariance and energy characterizations, which needs to be brought into alignment with what is actually proved versus what is conjectured and numerically supported.  Once those logical issues are corrected and the exposition is streamlined and aligned with the journal’s guidelines, I would be happy to see this paper published.

My recommendation is **acceptance after major revision**, with particular attention to the points outlined above.


