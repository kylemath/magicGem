## Vision Notes on the Zero-Covariance Theorem and Magic Energy

*(Whiteboard scratchpad after the valley / stonewall / hailstorm vision.)*

---

### 0. Core issue from the referee report

- In `methodology.tex`, the current proof of the Zero-Covariance Theorem claims:
  \[
    \sum_j \delta_j = 0,\quad \sum_j \Bigl(j-\frac{n-1}{2}\Bigr)\delta_j = 0
  \]
  ⇒ \(\delta_j = 0\) for all \(j\), where \(\delta_j = C_j - M(n)\) are deviations of column sums.
- This is **false for general \(n\)**: these are two linear conditions on an \(n\)-dimensional vector.
  Extra arithmetic/permutation constraints are silently used but not analyzed.
- Also, the text casually claims that *row + column sums + total sum* ⇒ *diagonal sums*, which is not a general theorem for normal magic squares; semi-magic vs magic is a real distinction.

**Goal:** rewrite the logical core so that:

1. The direction *magic ⇒ zero covariance* holds for **all** \(n\) in a clean linear-algebraic way.
2. The converse is:
   - Fully proved for \(n=3\) (purely algebraic + exhaustive enumeration).
   - Proved for \(n=4\) with a transparent mix of algebra and computation.
3. The diagonal conditions are expressed as **their own covariance constraints**, so that “magic ⇔ all relevant covariances vanish” is literally true and cleanly modular.

---

### 1. Covariance as orthogonality to the column-sum subspace

Whiteboard picture: think of the column sums \(C_j\) as a vector in \(\mathbb{R}^n\):
\[
 C = (C_0, C_1, \dots, C_{n-1}).
\]

For fixed \(n\), define:

- The **mean-offset vector**
  \[
    u := \Bigl(j-\frac{n-1}{2}\Bigr)_{j=0}^{n-1}.
  \]
  Note that \(\sum_j u_j = 0\).
- The **all-ones vector** \(1 = (1,\dots,1)\).

Then:

- \(\displaystyle \operatorname{Cov}(X,Z) = \frac{1}{n^2}\sum_j u_j C_j = \frac{1}{n^2}\langle u, C\rangle\).
- The constraint \(\sum_j C_j\) is fixed by the permutation condition:
  \[
    \sum_j C_j = \sum_{i,j} s_{ij} = \frac{n^2(n^2+1)}{2}.
  \]
- So the admissible vectors of column sums lie in an **affine hyperplane**
  \[
    H := \{C \in \mathbb{R}^n : \langle 1, C\rangle = S_{\text{tot}}\},
  \]
  where \(S_{\text{tot}}\) is the fixed total sum.

Magic column condition:

- All column sums equal \(M(n)\) ⇔ \(C = M(n)\cdot 1\).

Observe:

- For any \(C\in H\), write \(C = \bar C\,1 + \delta\) with \(\langle 1,\delta\rangle = 0\).
- Then \(\operatorname{Cov}(X,Z) = \frac{1}{n^2}\langle u, \delta\rangle\) because \(\langle u,1\rangle = 0\).

So:

- **Magic ⇒** \(\delta = 0\) ⇒ Cov\((X,Z)=0\).
- **Zero covariance ⇒** \(\delta\) is **orthogonal to \(u\)** in the \((n-1)\)-dimensional subspace \(\{1\}^\perp\).

Thus the “hard” direction is really:

> For arrangements \(S\) that are permutations of \(\{1,\dots,n^2\}\), the only possible deviation vector \(\delta\) satisfying both \(\langle 1,\delta\rangle=0\) and \(\langle u,\delta\rangle=0\) is \(\delta=0\), at least for \(n=3,4\).

This is a **Diophantine / combinatorial rigidity** statement about allowed column-sum patterns.

Key point for the paper:

- Do **not** pretend this follows from linear algebra alone.
- For \(n=3\), we can fully classify the possibilities by hand.
- For \(n=4\), we can restrict the patterns algebraically and then kill the remaining candidates computationally.

---

### 2. Clean \(n=3\) analysis (sketch for main text, full detail in appendix)

Set \(n=3\). Then:

- \(u = (-1,0,1)\).
- Column sums \(C=(C_0,C_1,C_2)\).
- Deviations \(\delta_j = C_j - M(3)\) with \(M(3)=15\).

Constraints:

1. \(\sum_j \delta_j = 0\).
2. \(\sum_j u_j \delta_j = -\delta_0 + 0\cdot\delta_1 + 1\cdot\delta_2 = 0\).

Solve:

- From (2): \(\delta_2 = \delta_0\).
- From (1): \(\delta_0 + \delta_1 + \delta_0 = 0 \Rightarrow \delta_1 = -2\delta_0.\)
- So \(\delta = t(1,-2,1)\).

Now exploit **permutation constraints**:

- Column sums of a \(3\times3\) permutation of \(\{1,\dots,9\}\) lie in \([6,24]\).
- So \(M(3)=15\) ⇒ \(\delta_j \in [-9,9]\).
- Hence \(t\) is an integer with \(|t|\le 9\).

Strategy:

1. Enumerate all **triples of column sums** consistent with \(\delta = t(1,-2,1)\) and with the full multiset \(\{1,\dots,9\}\) (this is a finite hand-check in the appendix).
2. Show that for \(t\neq 0\), any such triple **forces** a non-zero \(\operatorname{Cov}(Y,Z)\) or violates the permutation structure (e.g., repeated or missing entries).
3. Conclude that the only realizable pattern is \(t=0\), i.e. all column sums equal to \(M(3)\).

This gives a rigorous, finite, and conceptually clear argument:

- Covariance conditions filter down to a 1-parameter family of column-sum patterns.
- The permutation + row/diagonal constraints kill that parameter.

The current appendix already does something similar; the main fix is **to state the dependence on the permutation structure explicitly** and bring this argument into sharper focus.

---

### 3. \(n=4\): from 2D deviation space to computational elimination

For \(n=4\):

- \(u = \bigl(-\tfrac{3}{2}, -\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{3}{2}\bigr)\).
- The constraints \(\langle 1,\delta\rangle = 0\) and \(\langle u,\delta\rangle = 0\) define a **2D rational subspace** of \(\mathbb{R}^4\).
- One convenient integer basis is:
  \[
    v^{(1)} = (1,0,-3,2),\quad v^{(2)} = (0,1,-2,1),
  \]
  so any deviation vector has the form \(\delta = t_1 v^{(1)} + t_2 v^{(2)}\).

Permutation constraints:

- Each column sum \(C_j = M(4) + \delta_j\) must lie in the integer interval determined by \(\{1,\dots,16\}\):
  \[
    C_j \in [1+2+3+4,\; 13+14+15+16] = [10,58].
  \]
- Total sum fixed: \(\sum_j C_j = \sum_{k=1}^{16} k = 136\).
- Additionally, **row sums** interact with column sums: the full \(4\times4\) matrix must be a permutation matrix of these 16 entries.

Vision for a clean hybrid proof:

1. Use the deviation basis to reduce all possible column-sum patterns to a finite lattice of \((t_1,t_2)\) candidates that keep each \(C_j\) in \([10,58]\).
2. For each such candidate \((t_1,t_2)\), enforce:
   - Row-sum constraints consistent with \(\operatorname{Cov}(Y,Z)=0\),
   - The requirement that entries are exactly \(\{1,\dots,16\}\).
3. Show that the only realizable pair is \((t_1,t_2)=(0,0)\), i.e. all column sums equal to \(M(4)=34\).

Practically, Step 2 is executed by the existing Python search (`analyze_all_magic_squares.py`), but the point is:

- We can **state the structure theorem cleanly**:
  > For \(n=4\), any permutation matrix with \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=0\) must have equal row and column sums; this was verified by enumerating all feasible deviation patterns and checking realizability exhaustively.

That is exactly what the paper is already doing; the fix is to make this **explicit** and not pretend the linear algebra alone forces \(\delta=0\).

---

### 4. Diagonals as covariance with diagonal indicator vectors

The current text treats diagonals somewhat asymmetrically: row/column balance is framed via covariance, while diagonals are inserted as extra scalar conditions on means.

Cleaner idea (for future revision, maybe Appendix A.2):

- Introduce two additional coordinate-like random variables:
  - \(D_{\text{main}}(i,j) = 1\) if \(i=j\), else \(0\).
  - \(D_{\text{anti}}(i,j) = 1\) if \(i+j=n-1\), else \(0\).
- Consider the **covariances**
  \[
    \operatorname{Cov}(D_{\text{main}}, Z),\quad \operatorname{Cov}(D_{\text{anti}}, Z),
  \]
  with the same centering convention for \(Z\).

Observation:

- \(\operatorname{Cov}(D_{\text{main}}, Z)=0\) ⇔ the mean of \(Z\) along the main diagonal equals the global mean.
- Since the global mean is \((n^2+1)/2\), this is exactly the condition that the main diagonal sum equals \(M(n)\).
- Similarly for the anti-diagonal.

Thus the **total magic energy** can be reframed as:
\[
  E(S) = \operatorname{Cov}(X,Z)^2 + \operatorname{Cov}(Y,Z)^2
       + \operatorname{Cov}(D_{\text{main}}, Z)^2
       + \operatorname{Cov}(D_{\text{anti}}, Z)^2.
\]

Then the clean statement becomes:

> For \(n=3,4\), an arrangement \(S\) is a magic square if and only if  
> \(\operatorname{Cov}(X,Z)=\operatorname{Cov}(Y,Z)=\operatorname{Cov}(D_{\text{main}}, Z)=\operatorname{Cov}(D_{\text{anti}}, Z)=0\).

This removes the asymmetry and justifies the “energy = sum of squared covariances” story very literally.

For general \(n\), this identity becomes the natural **conjecture** backed by large-scale experiments.

---

### 5. Pseudocode: the clean experimental verification protocol

(*For the appendix or supplementary materials; conveys rigor of the computational side.*)

```python
def all_arrangements(n):
    # generator over all permutations reshaped to n x n
    from itertools import permutations
    vals = list(range(1, n*n + 1))
    for perm in permutations(vals):
        yield np.array(perm).reshape((n, n))

def is_magic_square(S):
    n = S.shape[0]
    M = n * (n*n + 1) // 2
    rows = np.all(S.sum(axis=1) == M)
    cols = np.all(S.sum(axis=0) == M)
    main_diag = (np.trace(S) == M)
    anti_diag = (np.fliplr(S).trace() == M)
    return rows and cols and main_diag and anti_diag

def cov_energy(S):
    # implement Definition 3.x with X, Y, Z, D_main, D_anti
    ...
    return Ecov + Ediag
```

For \(n=3\):

```python
zeros = []
for S in all_arrangements(3):
    if abs(cov_energy(S)) < 1e-12:
        zeros.append(S)
assert all(is_magic_square(S) for S in zeros)
assert len(zeros) == 8  # Lo Shu + D4 variants
```

For \(n=4,5\), we replace `all_arrangements` with a large uniform sampler and record:

- No non-magic zero-energy configurations were observed among \(6\times10^7\) and \(4\times10^8\) samples.

This pseudocode is essentially what the current code base implements; the vision here is **to make the logical structure completely transparent**.

---

### 6. Lyric coda (what the rock pile taught me)

> The valley wall was a basis of broken stones,  
> each rock a vector in gravity’s coordinates.  
>  
> I asked the covariances what they knew of balance,  
> and they answered not with equal sums alone,  
> but with orthogonality to every direction that could lean.  
>  
> Rows are one axis, columns another,  
> diagonals yet two more;  
> magic is the point where every such tilt  
> sees no correlation with height.  
>  
> In that space, the proof is not a single stroke of algebra,  
> but a lattice of constraints,  
> trimmed by integrality,  
> polished by computation,  
> until only the gems remain.

*(End of vision notes. Next step: translate these into precise theorem statements + revised proofs in `methodology.tex` and `appendix.tex`.)*


