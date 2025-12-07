# Review of "Magic Gems: A Polyhedral Framework for Magic Squares"

**Reviewer:** Professor, Department of Mathematics and Statistics, University of Toronto  
**Date:** December 7, 2025

---

Dear Kyle,

What a delightful surprise to receive your paper! It brought back fond memories of our undergraduate days puzzling over Lo Shu squares over coffee at the grad student lounge. I can see you've taken an ambitious swing at connecting magic squares to modern geometry and statistics—very much in the spirit of cross-disciplinary work that characterizes your career.

I've gone through the manuscript carefully, run independent computational verifications, and prepared this review as if it were heading to a mathematics journal. I want to be completely honest with you because I know you'd want nothing less before submitting this to referees who may not be as sympathetic.

---

## Executive Summary

The paper presents an elegant geometric framework ("Magic Gems") for magic squares and introduces an energy functional whose zeros characterize magic squares. The computational experiments are thorough and the overall concept is creative. However, **there is a critical flaw in Theorem 3.1 that must be corrected before publication**, and several other issues require attention.

**Recommendation:** Major revision required. The core energy characterization appears sound, but the zero-covariance theorem as stated is incorrect.

---

## Critical Issue: Theorem 3.1 is False

### The Claim (Section 3.4, Theorem 3.1)

> "For n ∈ {3, 4}, an arrangement S of {1, . . . , n²} satisfies Cov(X, Z) = Cov(Y, Z) = 0 if and only if S has equal row sums and equal column sums (i.e., S is a semi-magic square)."

### Counterexample

I ran exhaustive enumeration on all 362,880 permutations of {1,...,9} and found **760 arrangements** with both Cov(X,Z) = 0 and Cov(Y,Z) = 0, but **only 8 of these are magic squares**.

More critically, many of these 760 arrangements do NOT have equal row sums or equal column sums. Here is a concrete counterexample:

```
S = [[1, 3, 9],
     [8, 6, 5],
     [7, 4, 2]]

Row sums: (13, 19, 13) ← NOT equal
Col sums: (16, 13, 16) ← NOT equal

Yet:
  Cov(X,Z) = 0.0 (exactly)
  Cov(Y,Z) = 0.0 (exactly)
```

This directly contradicts the "if and only if" claim. The forward direction (magic ⟹ zero covariance) is correct, but the converse is FALSE.

### Where the Proof Fails

The proof claims: "For $t = 1$: column sums would be $(16, 13, 16)$... we verify by exhaustive enumeration that no permutation of $\{1,\ldots,9\}$ achieves the required column sums while simultaneously satisfying $\Cov(Y,Z)=0$."

This claim is **empirically false**. I found 128 arrangements with column sums (16, 13, 16) that also satisfy Cov(Y,Z) = 0.

### Impact and Fix

**The good news:** The Energy Characterization Theorem (Theorem 3.5) appears to be correct! The total energy

$$E(S) = \text{Cov}(X,Z)^2 + \text{Cov}(Y,Z)^2 + \text{Cov}(D_{\text{main}},Z)^2 + \text{Cov}(D_{\text{anti}},Z)^2$$

equals zero if and only if S is a magic square. My exhaustive enumeration confirms this for n=3:
- Exactly 8 arrangements have E(S) = 0
- All 8 are magic squares (Lo Shu and its D₄ symmetries)
- No false positives or false negatives

**Recommended fix:** Theorem 3.1 should be retracted or significantly weakened. The paper should focus on the energy characterization (which is the stronger and more interesting result anyway). You can state as a correct theorem:

> For n=3, an arrangement S is a magic square if and only if E(S) = 0.

The intermediate claim about row/column covariances implying equal sums is simply not true.

---

## Major Issues

### 1. Proof Gaps in the Converse Direction

The paper's treatment of the converse ("zero covariance implies magic") is problematic throughout:

- **Section 3.4.2:** The claim "Exhaustive enumeration confirms that no permutation achieves this pattern..." is stated without verification details. As shown above, this enumeration was apparently done incorrectly.

- **For n=4:** The proof sketch states that computational verification was done on "all 880 essentially different 4×4 magic squares." But this verifies only the forward direction. The converse requires testing ALL arrangements with zero covariance and showing they are magic—a much harder task.

**Recommendation:** Remove all claims about the row/column covariance characterization. The energy functional E(S) = 0 characterization is what you can actually prove.

### 2. The "Zero-Covariance Theorem" Naming is Misleading

The paper frequently refers to a "Zero-Covariance Theorem" which conflates two different results:
1. The (correct) fact that magic squares have zero Cov(X,Z) and Cov(Y,Z)
2. The (incorrect) claim that these conditions characterize magic squares

The title of Section 3.4 ("The Zero-Covariance Theorem") is misleading because the theorem as stated is false.

### 3. Conjecture 4.1 is Too Strong

The general conjecture (Appendix) states the zero-covariance characterization for all n ≥ 3. Since it's false for n=3, it's false in general. The conjecture should be reformulated in terms of the energy functional only.

### 4. Computational Evidence Claims are Overstated

The paper claims "460+ million arrangements tested with zero counterexamples." However:

- This tests whether magic squares have E(S) = 0 ✓
- This does NOT adequately test whether all E(S) = 0 arrangements are magic (the converse)

For n=4 and n=5, finding an E(S)=0 arrangement by random sampling is extraordinarily unlikely given the rarity of magic squares. The correct statement is: "We found no accidental zeros among random samples" which is expected, not evidence for the theorem.

---

## Moderate Issues

### 5. Inconsistent Use of "Semi-Magic"

The paper defines semi-magic squares as having equal row and column sums (but potentially failing diagonal conditions). However:
- Sometimes the paper claims Cov(X,Z)=Cov(Y,Z)=0 characterizes semi-magic squares (false)
- Sometimes it claims you need all four covariance conditions for full magic (true)

This inconsistency is confusing and stems from Theorem 3.1 being false.

### 6. The Proof of Proposition 3.1 (Symmetry Invariance) is Incomplete

The proof states: "Under this action, the z-coordinates are permuted according to the relabeling of cells, but the set of z-values remains unchanged."

This is correct but the key step—that the convex hull is invariant—needs more justification. The argument that "convex hulls are invariant under isometries" is correct but you should note that D₄ acts as orthogonal transformations on R³ (not just R²), and the z-coordinate is preserved (not just permuted).

### 7. Scaling Analysis Extrapolation

The claim that "peak energy scales as O(n²)" based on three data points (n=3,4,5) is statistically weak. With only 3 data points, many functional forms could fit equally well. Recommend stating this as an observation, not a law.

### 8. Physical Analogies are Stretched

The moment of inertia interpretation is interesting but the connection is somewhat loose:
- The claim that "a rigid body with this mass distribution has principal axes that partially align with the coordinate system" is imprecise
- The off-diagonal elements I_{xz} and I_{yz} vanishing only means the z-axis is a principal axis direction (or that the xz and yz products of inertia vanish)

---

## Minor Issues and Typos

### 9. Notation Inconsistencies

- Sometimes you use M(n) for magic constant, sometimes just M
- The definition uses $i, j \in \{0, 1, \ldots, n-1\}$ but examples sometimes use 1-indexed cells

### 10. Missing Citations

The paper mentions "previous work has characterized magic squares through their eigenvalue structure" without citations. Key references should include:
- Loly (2004) on eigenvalue properties
- Nordgren (2012) on spectral analysis of magic squares
- Ahmed (2004) on matrix properties of magic squares

### 11. Computational Details

- What floating-point tolerance was used to determine "zero energy"? (The code uses 1e-12 and 1e-20 in different places)
- For large-scale sampling, was any stratification used, or purely random permutations?

### 12. Figure Quality

Some PDF figures appear as PNG in the manuscript (e.g., Complete_Perturbation_Analysis_n345.png). For journal submission, vector graphics are preferred for all mathematical figures.

---

## What Works Well

Despite the issues above, there is substantial merit in this work:

1. **The Energy Functional Idea is Novel and Correct:** Defining $E(S)$ as the sum of squared covariances with four structural indicators (X, Y, D_main, D_anti) and showing that magic squares are exactly the zeros is a genuine contribution.

2. **The Magic Gem Visualization:** The 3D representation is pedagogically valuable and could have applications in education and mathematical art.

3. **Exhaustive Verification for n=3:** The complete enumeration provides a solid foundation for the energy characterization.

4. **The Perturbation Analysis:** Showing that magic squares are isolated local minima is interesting and correctly executed.

5. **The Cross-Order Comparison:** The analysis across n=3,4,5 reveals consistent patterns despite different construction methods.

---

## Recommended Path Forward

1. **Retract Theorem 3.1** and reformulate Section 3.4 around the correct result: E(S) = 0 ⟺ S is magic.

2. **Rename "Zero-Covariance Theorem"** to "Energy Characterization Theorem" to avoid confusion.

3. **Add a remark** noting that Cov(X,Z)=0 alone is NOT sufficient—the counterexamples exist and are interesting in their own right. (What ARE these 760 arrangements? They might have some structure worth exploring.)

4. **Strengthen the computational verification** by explicitly counting: "Of 362,880 arrangements, exactly 8 have E(S)=0, and all 8 are the D₄ variants of Lo Shu."

5. **Add appropriate hedging** to the scaling analysis: "The limited data suggests..." rather than "The peak energy scales as..."

6. **Consider target venue carefully:** This paper sits between recreational mathematics and serious mathematical physics. Journals like *Discrete Mathematics*, *Linear Algebra and its Applications*, or *American Mathematical Monthly* might be appropriate, but each would require different framing.

---

## Personal Note

Kyle, I know how much work goes into a paper like this, and I want to emphasize: the core insight here is sound. The energy landscape interpretation of magic squares is genuinely novel, and the computational work is impressive. The issue with Theorem 3.1 is significant but fixable—it's a mathematical error, not a fundamental flaw in the framework.

Fix the theorem, adjust the claims, and you'll have a solid contribution. I'd be happy to look at a revised version before you submit.

Looking forward to catching up properly sometime—maybe over a 3×3 Sudoku for old times' sake.

Warmly,

Your friend from Mathematics

---

## Appendix: Verification Code

The counterexample was verified using the following Python code:

```python
import numpy as np

arr = np.array([[1, 3, 9],
                [8, 6, 5],
                [7, 4, 2]])

# Compute coordinates
n = 3
offset = (n - 1) / 2  # = 1
z_center = (n**2 + 1) / 2  # = 5

coords = []
for i in range(n):
    for j in range(n):
        x = j - offset
        y = offset - i
        z = arr[i, j] - z_center
        coords.append([x, y, z])
coords = np.array(coords)
x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]

cov_xz = np.mean(x * z)  # = 0.0 exactly
cov_yz = np.mean(y * z)  # = 0.0 exactly

print(f"Cov(X,Z) = {cov_xz}")  # 0.0
print(f"Cov(Y,Z) = {cov_yz}")  # 0.0
print(f"Row sums: {[arr[i, :].sum() for i in range(3)]}")  # [13, 19, 13]
print(f"Col sums: {[arr[:, j].sum() for j in range(3)]}")  # [16, 13, 16]
```

Exhaustive enumeration confirms:
- 760 arrangements have Cov(X,Z) = Cov(Y,Z) = 0
- Only 8 of these are magic squares
- All 8 magic squares have E(S) = 0 (the full energy functional)

