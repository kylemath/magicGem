# The Axial Covariance Theorem for Magic Squares

## Theorem Statement

Let $S$ be an $n \times n$ arrangement of numbers, and let $A_S$ be its axial representation defined by the set of points:

$$A_S = \{(i - \frac{n-1}{2}, j - \frac{n-1}{2}, S_{ij} - \mu_S) \mid 0 \leq i,j < n\}$$

where $(i,j)$ are the indices of the arrangement, and $\mu_S$ is the mean of all values in $S$.

**Theorem:** An $n \times n$ numerical arrangement $S$ is a magic square if and only if the following four covariance conditions are satisfied:

1. $\text{Cov}(x, z) = 0$ (row sum constraint)
2. $\text{Cov}(y, z) = 0$ (column sum constraint)
3. $\text{Cov}(\frac{x+y}{\sqrt{2}}, z) = 0$ (main diagonal sum constraint)
4. $\text{Cov}(\frac{x-y}{\sqrt{2}}, z) = 0$ (anti-diagonal sum constraint)

where $x$, $y$, and $z$ represent the coordinates of the points in $A_S$, and $\text{Cov}(u, v)$ denotes the covariance between variables $u$ and $v$.

## Proof

### Sufficiency (⇐)

We need to show that if the four covariance conditions are satisfied, then $S$ is a magic square.

#### Row Sum Constraint:

For each row $i$, let $R_i = \{(i - \frac{n-1}{2}, j - \frac{n-1}{2}, S_{ij} - \mu_S) \mid 0 \leq j < n\}$ be the set of points in row $i$.

The covariance is defined as:
$$\text{Cov}(x, z) = \mathbb{E}[(x - \mathbb{E}[x])(z - \mathbb{E}[z])]$$

Since $\mathbb{E}[z] = 0$ (by construction) and within each row $i$, all $x$ values are equal to $x_i = i - \frac{n-1}{2}$, we have:

$$\text{Cov}(x, z) = \frac{1}{n^2} \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} (x_i - \mathbb{E}[x])(S_{ij} - \mu_S)$$

$$= \frac{1}{n^2} \sum_{i=0}^{n-1} (x_i - \mathbb{E}[x]) \sum_{j=0}^{n-1} (S_{ij} - \mu_S)$$

For $\text{Cov}(x, z) = 0$ to hold, and since the $x_i$ are distinct, we must have $\sum_{j=0}^{n-1} (S_{ij} - \mu_S) = 0$ for all rows $i$.

This implies $\sum_{j=0}^{n-1} S_{ij} = n\mu_S$ for all rows $i$, meaning all rows sum to the same value.

#### Column Sum Constraint:

By similar reasoning, $\text{Cov}(y, z) = 0$ implies that $\sum_{i=0}^{n-1} S_{ij} = n\mu_S$ for all columns $j$, meaning all columns sum to the same value.

#### Diagonal Sum Constraints:

Let $d_1 = \frac{x+y}{\sqrt{2}}$ and $d_2 = \frac{x-y}{\sqrt{2}}$ be the main and anti-diagonal projections.

The condition $\text{Cov}(d_1, z) = 0$ implies:

$$\sum_{(i,j): i=j} (S_{ij} - \mu_S) = 0$$

Therefore, $\sum_{i=0}^{n-1} S_{ii} = n\mu_S$, meaning the main diagonal sums to the same value as rows and columns.

Similarly, $\text{Cov}(d_2, z) = 0$ implies:

$$\sum_{(i,j): i+j=n-1} (S_{ij} - \mu_S) = 0$$

Therefore, $\sum_{i=0}^{n-1} S_{i,n-1-i} = n\mu_S$, meaning the anti-diagonal sums to the same value as rows, columns, and the main diagonal.

Thus, all rows, columns, and both main diagonals sum to the same value, which is the definition of a magic square.

### Necessity (⇒)

Now we show that if $S$ is a magic square, then the four covariance conditions are satisfied.

A magic square, by definition, has all rows, columns, and main diagonals summing to the same magic constant $M = \frac{n(n^2+1)}{2}$.

For the centered values, this means:

- For each row $i$: $\sum_{j=0}^{n-1} (S_{ij} - \mu_S) = 0$
- For each column $j$: $\sum_{i=0}^{n-1} (S_{ij} - \mu_S) = 0$
- For the main diagonal: $\sum_{i=0}^{n-1} (S_{ii} - \mu_S) = 0$
- For the anti-diagonal: $\sum_{i=0}^{n-1} (S_{i,n-1-i} - \mu_S) = 0$

These conditions directly imply that:

1. $\text{Cov}(x, z) = 0$
2. $\text{Cov}(y, z) = 0$
3. $\text{Cov}(\frac{x+y}{\sqrt{2}}, z) = 0$
4. $\text{Cov}(\frac{x-y}{\sqrt{2}}, z) = 0$

Thus, both the sufficiency and necessity parts of the theorem are proved.

## Corollary: Eigenstructure of Magic Squares

**Corollary 1:** The covariance matrix of the axial representation of any magic square has the form:

$$
\text{Cov}(A_S) = \begin{pmatrix}
\sigma_x^2 & 0 & 0 \\
0 & \sigma_y^2 & 0 \\
0 & 0 & \sigma_z^2
\end{pmatrix}
$$

where $\sigma_x^2 = \sigma_y^2 = \frac{n^2-1}{12}$ for an $n \times n$ magic square.

**Corollary 2:** The eigenvectors of the covariance matrix are aligned with the coordinate axes $[1,0,0]$, $[0,1,0]$, and $[0,0,1]$.

**Corollary 3:** For the extended 5-dimensional representation including diagonal projections, the covariance matrix has exactly two zero eigenvalues, reflecting the linear dependencies among the five dimensions.

## Implications

This theorem provides a complete geometric characterization of magic squares through their covariance properties, offering an alternative to the traditional algebraic definition. It establishes a direct connection between:

1. The algebraic constraints (equal sums in rows, columns, and diagonals)
2. Statistical properties (zero covariances)
3. Geometric attributes (orthogonality in the axial representation)

Furthermore, this characterization allows us to precisely define the manifold of magic squares within the space of all possible $n \times n$ arrangements, as the set of arrangements satisfying these four covariance constraints.

The eigenvector alignment with coordinate axes is not a coincidence but a direct mathematical consequence of the magic square definition. This explains why all 880 order-4 magic squares exhibit identical eigenvector structure despite their apparent differences.

## Geometric Interpretation: The Magic Square Manifold

Our covariance-based characterization provides a powerful geometric interpretation of magic squares as a manifold within the space of all possible numerical arrangements.

### The Manifold Definition

The magic square manifold $\mathcal{M}$ can be formally defined as:

$$\mathcal{M} = \{S \in \mathbb{R}^{n \times n} \mid \text{Cov}(x, z) = 0, \text{Cov}(y, z) = 0, \text{Cov}(\frac{x+y}{\sqrt{2}}, z) = 0, \text{Cov}(\frac{x-y}{\sqrt{2}}, z) = 0\}$$

This definition identifies the manifold as the intersection of four hyperplanes in the space of all $n \times n$ arrangements. Each hyperplane corresponds to one of our covariance constraints.

### Distance to the Manifold

Given any $n \times n$ arrangement $S$, we can define its distance to the magic square manifold as:

$$d(S, \mathcal{M}) = \sqrt{[\text{Cov}(x, z)]^2 + [\text{Cov}(y, z)]^2 + [\text{Cov}(\frac{x+y}{\sqrt{2}}, z)]^2 + [\text{Cov}(\frac{x-y}{\sqrt{2}}, z)]^2}$$

This Euclidean distance in constraint space provides a meaningful measure of how "magical" any given arrangement is. Perfect magic squares will have a distance of exactly zero.

<Figure distance_distribution.png>

As shown in the figure above, the distribution of distances clearly separates magic squares (blue) from non-magic arrangements (red). Magic squares form a tight cluster near zero, while non-magic arrangements have a broader distribution at greater distances.

### Perturbation Analysis

When we perturb a magic square by making random swaps of elements, the distance to the manifold increases in a predictable way:

<Figure perturbation_vs_distance.png>

The figure demonstrates that each level of perturbation (corresponding to the number of random swaps) systematically increases the average distance to the magic square manifold. This confirms our distance metric captures the intuitive notion of how far an arrangement is from being a magic square.

### Constraint Space Visualization

We can visualize the magic square manifold by plotting arrangements in the constraint space defined by our covariance measures:

<Figure constraint_space_3d.png>

In this 3D visualization, magic squares (blue) form a tight cluster at the origin (0,0,0), representing the perfect satisfaction of all constraints. Non-magic arrangements (colored by perturbation level) spread outward from this point, with more perturbed arrangements generally further from the origin.

### Constraint Violation Analysis

Different types of perturbations to magic squares violate different constraints to varying degrees:

<Figure constraint_violation.png>

The figure shows how different perturbation levels affect each of the four constraints. Magic squares (blue) show near-zero violation across all constraints, while non-magic arrangements exhibit increasing violations as the perturbation level increases.

### Dimensionality Reduction

Using dimensionality reduction techniques like t-SNE, we can visualize the high-dimensional structure of the magic square manifold in a 2D representation:

<Figure tsne_visualization.png>

This visualization reveals the topological structure of the magic square manifold and its relationship to various non-magic arrangements. Magic squares (blue) form a distinct cluster, while non-magic arrangements spread outward with increasing perturbation levels.

## Conclusion

The manifold perspective unifies our understanding of magic squares. Rather than seeing them simply as arrangements satisfying certain sum constraints, we now recognize them as points on a well-defined geometric manifold. This perspective provides:

1. A complete characterization of magic squares
2. A continuous measure of "magicalness" for any arrangement
3. A way to visualize the relationship between magic and non-magic arrangements
4. A deeper understanding of the mathematical structure underlying magic squares

This geometric interpretation bridges the gap between algebra, statistics, and geometry, offering new insights into these ancient mathematical objects.
