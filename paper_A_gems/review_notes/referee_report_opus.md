# Referee report

**Manuscript:** "Magic Gems: A Polyhedral Framework for Magic Squares", K. E. Mathewson (21 pp., `paperA.pdf`, sources `main.tex`, `sections/*.tex`, ancillary `anc/`).

**Recommendation:** **Major revision** at *Experimental Mathematics*. As it stands the paper would not be competitive at *Electronic J. Combinatorics* or *Discrete & Computational Geometry*: only one result holds for every order and is not immediate, and that result is presented as a Proposition. A shortened version (about 10 pp, Sections 2–4 condensed, Siamese theorem as the centrepiece, census as one table) would also suit *Mathematics Magazine* or *The Mathematical Intelligencer*.

---

## 0. Summary of the paper's claims

To an arrangement $S$ of $1,\dots,n^2$ on the $n\times n$ grid the paper attaches the points $\mathbf p_{ij}=(x_{ij},y_{ij},z_{ij})$ (centred cell, centred entry) and their convex hull, the "Magic Gem" $\mathcal G(S)$. The paper:

- (Sec. 2–3) records elementary facts. $\sum\mathbf p_{ij}=0$ for every arrangement. $S$ is semi-magic iff $\sum z\varphi(x)=\sum z\varphi(y)=0$ for all $\varphi$. Loly's moment-of-inertia invariant follows. $\sum zxy$ is not forced. Two remarks cover the inertia tensor and the covariance determinant.
- (Sec. 4) shows that the complement acts as the reflection $z\mapsto-z$, and that only $r^2,h,v$ can realise self-complementarity. For $n=4$ it determines by computer the isometry group of each of the 880 gems ($C_i$ for the 48 associative squares, $C_2$ for the 304 of Dudeney group VI, trivial otherwise). It also gives facet-orbit and parity statements and a Brunn–Minkowski asymmetry measure $\sigma$.
- (Sec. 5) tabulates the 880 order-4 gems: $V\in[8,16]$, 39 $f$-vectors, 352 combinatorial types, 155 volumes, 616 congruence classes (= complement orbits) and 554 Ehrhart polynomials. It proves that every gem lies in a fixed box and that corner and side-extreme points are always vertices. It proves, with computer verification of polynomial inequalities in $m$, that the Siamese square of every odd order $n\ge5$ has a gem with $f=(12,26,16)$.
- (Sec. 6) gives numerical mean vertex counts for random and annealed magic squares up to $n=10$ and lists open questions.

---

## 1. Triviality, novelty and correctness

### 1.1 Result-by-result verdicts

| Item | Verdict | Justification |
|---|---|---|
| Lemma 2.2 (means, variances, line sums) | **Trivial** | Centring, plus the variance of an arithmetic progression. (3) restates the definition of magic. |
| Prop. 2.4 ($D_4$-invariance) | **Trivial** | Relabelling cells by a grid symmetry applies the same planar isometry to the points. No specialist would accept it as a numbered proposition; make it one sentence. |
| Prop. 3.1 (centroid) | **Trivial, and the "interior" claim is false as stated** | The sum vanishes by centring. The interior claim fails for coplanar arrangements; see 1.3(a). |
| Prop. 3.2 (height-weighted moments) | **Trivial (a restatement of semi-magic)** | The functions $\varphi(x)$, $\varphi(y)$ on the grid span exactly the row and column indicators, so (1)–(2) say "row and column sums vanish" in another basis. (3) is one example. The diagonals never appear, so this is *not* "what magic means" (see Tone). The hypothesis $n\ge3$ is unnecessary for (1)–(2). |
| Cor. 3.3 (Loly's invariant) | **Known** (Loly 2004, Math. Gaz. 88) | The paper says so. One line from 3.2. |
| Rem. 3.4 (inertia tensor of the unit-mass set) | **Trivial/standard** | Contains, unused, the key to a general symmetry theorem (see 1.2). |
| Rem. 3.5 (covariance determinant) | **Trivial algebra plus out-of-scope numerics** | The volume/Spearman statistics on random arrangements are the companion paper's subject (the Introduction says so). |
| Lemma 4.1 (complement = mirror image) | **Trivial** | $z\mapsto -z$. |
| Prop. 4.2 (which $g$ can complement) | **Elementary/folklore** | $g^2=\mathrm{id}$ plus fixed-cell counting. "Self-complementary of odd order ⇒ associative" is folklore. For $n=4$ the content is implicit in Dudeney's complementary-pair patterns. Correct, but the proof's chain "$g\overline S=\overline{gS}=S$, so $g^2S=\overline{\overline S}=S$" is garbled (see §3). |
| Thm. 4.3 (isometry groups, $n=4$) | **Modest; most of it is trivial for all $n$** | The 48/304/528 split is Dudeney's classical partition (groups III, VI, rest). 616 = 48+304+528/2 is orbit counting. The point-set equality $\mathrm{Iso}(\{\mathbf p_{ij}\})=\{\mathrm{id}\}\cup\{\iota_g\}$ holds for every semi-magic square of every order by a two-line covariance argument (1.2). Only $\mathrm{Iso}(V)\subseteq\mathrm{Iso}(\{\mathbf p\})$ for $n=4$ needs the computer. Calling this a Theorem while the Siamese result is a Proposition inverts the paper's priorities. |
| Table 1 | **Data** | |
| Prop. 4.4 (facet orbits) | **Trivial plus data** | (1) An involution without fixed points pairs facets. (2) A facet is fixed iff its normal is on the axis. (3) Vertex orbits have size 2. The counts (282/18/4 etc.) are tabulated data. The sentence about $F$ and $-F$ being congruent by a planar rotation "although the point reflection … is improper" adds nothing and confuses. |
| Prop. 4.5 (parity for associative squares) | **Trivial, and false as stated** | Counting fixed points of an involution. Counterexample in 1.3(b). |
| Rem. 4.6 (classes, pandiagonal) | **Classical facts plus data** | Group I = the 48 pandiagonal squares (Dudeney). No associative pandiagonal square exists at order 4 (classical). |
| Rem. 4.7 (central-symmetry defect $\sigma$) | **Standard** | $\sigma\ge1$ with equality iff centrally symmetric is the lower half of the Rogers–Shephard inequality (Brunn–Minkowski). The companion upper bound $\mathrm{vol}(K-K)\le\binom{6}{3}\mathrm{vol}K$, i.e. $\sigma\le 5/2$, is not mentioned. "$\sigma=1$ exactly for the 48 associative gems" is a corollary of Thm 4.3, not independent information. The range $[1057/1018,145/88]$ is data. |
| Table 2 (f-vectors/types/volumes) | **Data**, useful as a census | The "352 types" partition is a coarsening of the complement-orbit partition (combinatorial type is invariant under $z\mapsto-z$). That explains the 93 singleton types (all self-complementary) and the 201 doubletons (mostly mirror pairs). Say so instead of remarking that "352 = 352 is numerical only". |
| Prop. 5.1 (class → gem) | (1) **Ill-posed**; (2) **trivial at point-set level for all $n$, computation at hull level** | (1) "The 880 hull-vertex sets are pairwise distinct (as subsets of $\mathbb R^3$)" depends on which representative of each $D_4$-class is chosen. The invariant statement is (2). "Not even as full 16-point sets" follows for all $n$ from the covariance argument in 1.2. |
| Prop. 5.2 (bounding box, forced vertices) | **Trivial/standard** | (1)–(2) are immediate. (3)–(4) are the standard fact that a point lifted over a vertex of the base polygon, or extreme in height over an edge of the base polygon, is a vertex of the lifted hull (faces of the projection pull back). Worth keeping as a lemma because it frames the Siamese theorem (below), but not as a headline result. |
| Sec. 5.3 (554 Ehrhart polynomials) | **Data, of doubtful relevance** | The lattice structure of $Q=\mathcal G+(\frac12,\frac12,\frac12)$ has no magic-square meaning. For lattice 3-polytopes, $L_Q$ is equivalent to (volume, lattice-normalised surface area, number of lattice points), so "554 polynomials" says these three numbers separate 554 of 616 classes. The section also invites confusion with the classical Ehrhart theory of *counting* magic squares cited in the Introduction. Recommend cutting it or reducing it to one sentence. Interpolating from $t\le3$ suffices (Ehrhart's theorem); the checks at $t=4,5,6$ are redundant. |
| Prop. 5.3 (Siamese gems have 12 vertices) | **Modest to substantive: the paper's one genuine all-$n$ theorem** | The closed form $s=n\langle i+j-m\rangle+\langle i+2j-2m\rangle+1$ is classical (de la Loubère's method is the "linear/cyclic" construction $nA+B+1$ with $A,B$ orthogonal cyclic Latin squares). The affine shear to five layers is a nice idea. The proof is sound in structure (see 1.3(d)). Read with Prop. 5.2, it says **the Siamese gem has no unforced vertices**: its 12 vertices are exactly the 4 corners and the 8 side extremes. State it that way; it is the most quotable result in the paper. |
| Table 4 (vertex growth) | **Numerical data** | Uncontrolled sampling bias for $n\ge5$ (acknowledged). The row "magic" is mislabelled for $n\ge5$, where it is the annealed sample. Random-arrangement statistics are announced in the Introduction as belonging to the companion paper. |

### 1.2 A general symmetry theorem the author has the ingredients for

Remark 3.4 and Lemma 2.2 already show that for any semi-magic $S$ the covariance matrix of the $N$ points is $\Sigma=\mathrm{diag}(a,a,c)$, with $a=(n^2-1)/12\ne c=(n^4-1)/12$. Any isometry $A$ of a finite set fixes its centroid (here the origin) and satisfies $A\Sigma A^{\top}=\Sigma$. So $A$ preserves the eigenspaces, i.e. the $(x,y)$-plane and the $z$-axis, and $A=\mathrm{diag}(B,\pm1)$. $B$ permutes the grid, so $B\in D_4$. The sign $+$ forces $BS=S$, hence $B=\mathrm{id}$. The sign $-$ forces $\overline S=BS$. Hence, **for every semi-magic square of every order $n\ge2$**:

- $\mathrm{Iso}(\{\mathbf p_{ij}\})=\{\mathrm{id}\}$ or $\{\mathrm{id},\iota_g\}$, the latter iff $S$ is self-complementary;
- the point sets of two semi-magic squares are congruent iff $T\in D_4S\cup D_4\overline S$. The same argument applies with $A\Sigma_SA^\top=\Sigma_T=\Sigma_S$.

This makes the point-set halves of Thm 4.3 and Prop 5.1(2) one-paragraph theorems for all $n$. It also answers Open Question 2 at the point-set level. What remains open, and is genuinely interesting, is whether $\mathrm{Iso}(V)$ (equivalently $\mathrm{Iso}(\mathcal G)$) can be strictly larger than $\mathrm{Iso}(\{\mathbf p\})$ when some points are not vertices. A specialist would expect the author to prove the easy general statement and to isolate the hard residual one.

### 1.3 Errors and gaps

**(a) Prop. 3.1 is false as stated ("for every arrangement … $\mathbf 0$ lies in the interior of $\mathcal G(S)$").**
- The proof asserts that "the points span $\mathbb R^3$ since the positions do and the heights are not all equal". That does not follow: if $z$ is an affine function of $(x,y)$ the points are coplanar.
- Counterexample: the row-by-row arrangement $s_{ij}=ni+j+1$ gives $z=x-ny$, a planar point set. For $n=3$, $S=\begin{smallmatrix}1&2&3\\4&5&6\\7&8&9\end{smallmatrix}$, $\operatorname{rank}\{\mathbf p_{ij}\}=2$ (checked numerically). The gem is a parallelogram and $\mathbf 0$ is not in its topological interior.
- Fix: add the hypothesis "the points are not coplanar". This holds for every semi-magic square: an affine $z=\alpha x+\beta y$ with zero row and column sums forces $\alpha=\beta=0$. Alternatively, exclude the 8 $D_4$-images of the row-by-row arrangement after checking that these are the only planar cases.

**(b) Prop. 4.5 is false as stated.** The same $S$ is associative ($s_c+s_{c'}=10$) with $n=3$ odd. Its topological interior is empty, so $I=0\not\equiv n\pmod 2$. The proof's appeal to Prop. 3.1 is the failing step. Fix as in (a) (e.g. "Let $S$ be associative and semi-magic"). The terminology of strictly interior / boundary non-vertex points also needs a full-dimensional hull.

**(c) Prop. 5.1(1) is not well defined** (representative-dependent); see the table. Delete it or replace it by "no two distinct $D_4$-classes have vertex sets related by an element of $D_4\times\langle\rho\rangle$", which is (2).

**(d) Siamese proof, Step 1.**
- The induction needs two facts it does not state. First, each run of $n$ entries fills an entire broken diagonal $\{i+j\equiv\text{const}\}$, so the up-right move is blocked exactly when $n\mid k$. Second, the cell below is then empty, since it lies on the next, unused broken diagonal. One sentence each.
- Steps 2–3 are correct in structure. $P\subseteq\Phi(\mathcal G)\subseteq Q$, facets closed under adjacency give $P=Q$, and three independent tight normals make each $v_k$ a vertex.
- The verification consists of 12×16 linear forms evaluated at explicit points with coefficients polynomial in $m$, plus the layer-polygon vertices. This is small enough to print as a table of slack polynomials. That would remove the "computer-assisted" label, which overstates what the computer contributes.
- The caption of Fig. 9 says "the shapes of the layers do not depend on $n$ except through scale". This is imprecise: $T=\mathrm{conv}\{(-m,m),(-1,m),(-m,1)\}$ has offsets that do not scale, and the layer heights are $\pm(n+1),\pm1,0$. Say "the combinatorics of the layer polygons do not depend on $m\ge2$".

**(e) "Height-weighted centroid"** (Prop. 3.2(2), Introduction): the signed masses $z_{ij}$ have total mass $0$, so there is no centroid. $\sum z\,(x,y)=0$ is the vanishing of the *dipole moment*, which is exactly Rogers–Loly's multipole language. Rename it.

**(f) Open Question 1** says "so every symmetric gem of order five is centrally symmetric". This presupposes the answer to Open Question 2: it is true for the point set (1.2), not yet proved for the hull.

**(g) Exact-hull certification (Appendix A).** "Facet planes are recovered from an initial Quickhull triangulation … Euler's relation … is checked". Euler's relation is a weak certificate. State explicitly that every point is verified to satisfy every integer facet inequality, and that the facet complex is closed (each edge in exactly two facets). Only then is the floating-point seed irrelevant.

### 1.4 What is genuinely new, and the framing

The new object is the hull of the *lifted grid* $\{(c,z_c)\}$ for a single square. This is a regular-subdivision construction: the lower and upper faces of $\mathcal G(S)$ project to the regular subdivisions of the $n\times n$ grid induced by the height vectors $z$ and $-z$. The vertical facets are the 1-dimensional analogues over the four sides. A specialist would see this immediately. The paper never mentions it, even though it already calls $z$ a "height function". In that language:

- non-vertex points are the grid points unused by both regular subdivisions;
- the forced-vertex proposition is the standard statement that vertices of the base configuration, and side extremes, are always used;
- the combinatorial type is determined by the cones of the secondary fan containing $z$ and $-z$, so classifying the 880 types becomes "which secondary cones does the magic subspace $W=\{z:\ \text{all line sums }0\}$ meet at permutation points";
- complementation swaps the upper and lower subdivisions.

This is what would *earn* the phrase "polyhedral framework". At present the title is oversold. The paper gives one construction, a list of elementary facts, one census at $n=4$ and one family theorem. Nothing in it is a framework in the sense of machinery that produces results for general $n$.

Relation to the cited literature:
- Birkhoff/Stanley/Ehrhart/Beck–Zaslavsky/Ahmed–De Loera–Hemmecke treat squares as lattice points of one polytope. The gem is a different object, and the Introduction says so correctly.
- Loly and Rogers–Loly already contain all of Section 3 in substance (moments, inertia, multipoles), as the Introduction concedes ("elementary and implicit in that work").
- The genuinely new content is (i) the order-4 census of hull combinatorics, symmetry and congruence, and (ii) the Siamese theorem.

### 1.5 What would make a stronger paper

1. Prove the general point-set symmetry/congruence theorem (1.2) and state Thm 4.3 as "for $n=4$, no gem has an isometry beyond those of its point set".
2. Recast via regular subdivisions/secondary fans (De Loera–Rambau–Santos), at least as a remark with the dictionary above.
3. Generalise the Siamese theorem to *all linear (cyclic) squares* $s=n\langle a\cdot c+\alpha\rangle+\langle b\cdot c+\beta\rangle+1$: the same shear gives boundedly many layers with $n$-independent combinatorics. A uniform bound on $V$ for all linear constructions, or a classification of their gem types, would be a real theorem. The paper's Open Question 3 already gestures at it.
4. Order 5. The author says the exact computation for all 275,305,224 squares "is feasible". If so, do it (or for the associative and pandiagonal subclasses). The census would then go from one data point to two, and the conjectures in Section 6 could be tested.
5. Asymptotics of $\mathbb E[V]$. For random arrangements the heights are close to i.i.d. over the grid. By analogy with Bárány–Buchta ($\mathbb E f_0\sim c\log^{2}N$ for $N$ uniform points in a 3-polytope), one expects $\mathbb E[V]=\Theta(\log^2 n)$, so the vertex fraction tends to $0$. Open Question 3 ("bounded away from zero?") is therefore almost certainly answered in the negative already for random arrangements. Rephrase it as a growth-rate question and compare Table 4 with $\log^2 n$.

### 1.6 Abstract and Introduction against the content

- Abstract: "We show that $\sum\mathbf p_{ij}=\mathbf 0$ for every arrangement" presents a centring identity as a result. Cut it, or move it to the body as a caution.
- Abstract: "the magic-specific consequences are the height-weighted moments": they are consequences of the *row and column* sums only. Write "semi-magic". The diagonal conditions are not captured by any $\sum z\varphi(x)$ or $\sum z\varphi(y)$.
- Abstract: "Every gem lies in a box that depends only on $n$" is trivial and should not appear in an abstract.
- Abstract: "and the 880 gems have 554 distinct Ehrhart polynomials" is data with no stated significance.
- Abstract: "155 volumes" should read "155 distinct volumes".
- Introduction, item 3: "no two gems have the same vertex set" is ill-posed (1.3(c)).
- Introduction: "The symmetry classification, the exact geometry … and the Siamese theorem are new." Be precise: the symmetry *partition* is Dudeney's; what is new is that the hull has no extra isometries.
- Introduction, first paragraph: "constructions for every order have been known for centuries". There is no magic square of order 2; write "every order $n\ge3$".

---

## 2. Tone

| Location | Quote | Problem | Proposed replacement |
|---|---|---|---|
| Sec. 1, "What is and is not new" | "we state and prove them in the gem's coordinates because the geometric picture invites misreadings of them." | Defensive; alludes to unnamed misreadings (earlier versions?). | "We record them in the coordinates of the gem for later use." |
| Sec. 3 title | "Balance: what the vectors from the centroid do and do not say" | Defensive, rhetorical. | "Moments of the point set" |
| Sec. 3 paragraph title | "Height-weighted balance is what magic means." | Promotional and inaccurate (semi-magic only; diagonals absent). | "Row and column sums as moment conditions" |
| Sec. 3, after Prop. 3.1 | "This is a consequence of centring the coordinates and carries no information about $S$; in particular it does not distinguish magic squares from arbitrary arrangements." | Belabours a triviality. The same point is made again in Def. 2.1, the Introduction, Remark 3.5 and Sec. 6. | Say it once, in one clause, after Def. 2.1. |
| Def. 2.1 | "Every centroid or moment statement in this paper refers to the full set of $N$ points …, and not to the solid $\mathcal G(S)$." | Meta-statement inside a definition; defensive. | Move to a single sentence after the definition, or delete. |
| Sec. 1, item 1 | "so the unweighted statement 'the vectors balance about the centroid' carries no information about $S$; it concerns all $n^2$ points, including those that are not vertices, not the solid hull." | Fourth repetition; scare quotes. | Delete. |
| Rem. 3.5 | "This concerns the point set, not its hull." / "numerical statements about samples only." | Repetitive hedging. | Delete both. State sample sizes once. |
| Sec. 5.1 | "(the hash was already exact: no hash class had to be split)" | Process detail. | Delete. |
| Sec. 5.1 | "we use his groups only as a classical reference partition" | Defensive. | Delete. |
| Sec. 5.1 | "Part (2) is the only failure of injectivity, and it is the expected one" | Informal. | "The only coincidences are those forced by Lemma 4.1." |
| Sec. 5.1 | "The coincidence $352=\#\{\text{types}\}=\#\{\text{self-complementary squares}\}$ is numerical only" | Draws attention to a non-fact. | Delete, or replace with the structural explanation (types are unions of complement orbits). |
| Sec. 5.4 | "This is a theorem, with a short computer-assisted proof." | Fourth-wall, defensive; contradicts the label "Proposition". | Delete. Label the result "Theorem 5.x". |
| Sec. 5.1 | "for $n\ge6$ exact counts are, to the author's knowledge, not available" | Voice switch ("the author" vs "we" elsewhere). | "for $n\ge6$ only estimates are known [Pinn–Wieczerkowski; Trump]". Check whether an exact order-6 count has recently appeared. |
| Sec. 5.1 | "D\"urer's own gem is centrally symmetric" | Informal. | "The gem of Dürer's square is centrally symmetric". |
| Sec. 6, first paragraph | "The vector picture is exact but easily over-read" | Defensive; rhetorical. | Delete. |
| Sec. 6, first paragraph | "What the hull does see is symmetry: … this accounts for all the symmetry there is" | Rhetorical flourish. | "For $n=4$ every isometry of a gem comes from self-complementarity (Theorem 4.3)." |
| Sec. 6 | "This is a statement about the samples only" | Repeated hedge. | Keep one precise caveat about sampling bias; delete the rest. |
| Sec. 1 | paragraph heading "The picture." | Informal. | "The construction." |
| Sec. 1 | "What is and is not new." | Informal heading. | "Relation to previous work." |
| `main.tex` comments | "% T1 fontenc removed: basic TeX Live has no cm-super …", "% Not available in basic TeX Live" | Process remarks in public arXiv source. | Remove. Use the real `cleveref`/`natbib` (both are on arXiv's TeX Live) instead of the hand-rolled `\Cref`. |

Voice is otherwise consistently "we". The single "the author's knowledge" is the only exception.

---

## 3. Language and presentation

### 3.1 Notation clashes (several serious)

- $\rho$: the row sums $\rho_i$ (Sec. 3) and the reflection $\rho(x,y,z)=(x,y,-z)$ (Sec. 4). Rename the reflection $\tau$ or $R_z$.
- $V$: the number of vertices (Terminology, tables) and the vertex set (Thm 4.3, "$\operatorname{Iso}(V)$"). Use $\operatorname{vert}\mathcal G$ for the set.
- $F$: a facet and the number of facets in the same sentence (Prop. 4.4(1): "every facet $F$ … the facets form $F/2$ antipodal pairs. Here $F\in\{12,\dots\}$").
- $I$: the strictly interior count, $I(S)$ (moment of inertia, Cor. 3.3) and $I_{jk}$ (inertia tensor).
- $B$: the boundary count, $B_n$ (box) and $B$ (bottom layer triangle, Sec. 5.4).
- $L$: a line $L$ (Sec. 2), $L_S(t)$ (Ehrhart) and the affine part $L(x,y)$ (Siamese proof).
- $M$: $M(n)$ (magic constant) and the parallelogram layer $M$.
- $c$: a cell $c$, $c=(n^2+1)/2$ (Prop. 5.3) and $\Sigma_{zz}=:c$ (Rem. 3.5).
- $m$: the signed mass $m_{ij}$ (Sec. 3) and $m=(n-1)/2$ (Sec. 5.4).
- $T$ (top triangle) vs. $t$ (transpose); $D$ (layer) vs. $D_4$.
- "$\operatorname{Iso}(X)$ for a finite set $X$" is defined and then applied to the solid $\mathcal G$. Define it for arbitrary subsets.

### 3.2 Terminology consistency

The paper alternates between "vertex", "hull vertex", "hull-vertex count", "extreme point", "points … extreme", "hull fraction" (undefined; it means $V/N$) and "hull-vertex sets". Fix "vertex" and "vertex fraction $V/N$" once in Sec. 2 and use only those. Similarly "order four" / "order-four" / "order-4" / "order $4$" are mixed (Sec. 5.1 title "order-4", Table 1 caption "order-four"); pick one. "Combinatorial type" is defined twice (Sec. 5.1 and App. A).

### 3.3 Specific sentences

- Sec. 4, Prop. 4.2 proof: "Applying $g$ to $\overline S=gS$ gives $g\overline S=\overline{gS}=S$, so $g^2S=\overline{\overline S}=S$". Replace with: "Since complementation commutes with $g$, $g^2S=g\overline S=\overline{gS}=\overline{\overline S}=S$."
- Thm 4.3: "the $832$ gems of the cases (2) and (3) are chiral" should read "the 832 gems in cases (2) and (3) are chiral".
- Prop. 5.1 title "[class $\to$ gem]" is not a title. Use "Injectivity and congruence".
- Sec. 5.2: "At most four points are strictly interior, while one gem has $I=0$, $B=6$." The "while" relates nothing. Write "$I\le4$ for every gem; the largest value of $B$ is $6$ (one gem)."
- Sec. 5.1: "Euler's relation holds for all 880 gems." This reads like a result. Move it to Appendix A as a consistency check.
- Sec. 5.1: "the multiset of facet sizes … is determined by the $f$-vector in every case". Say this is an observation for these 880 gems, not a general fact.
- Prop. 3.2(2): "(for $\varphi(t)=t^k$, all $k\ge0$; for $k=1$ the height-weighted centroid is the origin)". Nested parentheses, and "centroid" is wrong (1.3(e)).
- Lemma 2.2(2): "empirical variances" should state the normalisation ($1/N$).
- Square numbers (#45, #54, #124, #593, …) are used from p. 8 on, but the numbering is defined only in Appendix A ("numbered $0,\dots,879$ in the order of `anc/squares880.txt`"). Define it at first use and say which ordering it is (Frénicle standard form?). Better still, give the square itself whenever a number is cited.
- Inline `\smallmatrix` squares (Fig. 4 caption; Sec. 5.2, square #593) are illegible at print size. Display them.
- Sec. 3, paragraph before Fig. 4: "In panel a the entries themselves are piles of checkers …; every row and column carries 34 checkers, so the horizontal centre of mass … lies over the centre $O$ … Hence each column of heights has zero total mass" is one overloaded paragraph that repeats the caption. Cut it to one sentence.
- Table 3, lower part: the columns are $k=0,1,2,3,4,6$, so $k=5$ is missing and the $k=6$ column for $I$ is an empty 0. Add $k=5$ or explain.
- Table 2, "volumes" row: the column entries sum to 329, not to the "all" value 155, because volumes recur across $V$. Say so in the caption.
- Table 4: label the row "magic (annealed sample)" for $n\ge5$; the dashes for $n=9,10$ need a footnote.
- Fig. 4(d): "(rounded to integers)". Rounded summands that "sum to 0" is sloppy (e.g. $-16.875\to-17$). Print $8\,z\,x\,y$, which is an integer, instead.
- Appendix A: "Apple M4 Max (16 cores, 128 GB)" is irrelevant for exact computations. Keep the software versions and give run times instead.
- Bibliography:
  - `trump2012enumeration` has no year or access date.
  - The companion paper is "In preparation". Give an arXiv number or remove the dependence; the paper says it uses none of the companion's results, so the citation can simply be softened.
  - Add MSC codes (05B15, 52B05, 52B20, 52B15).

### 3.4 Structure, length, figures

- **Section 3 is about three pages, with two full figures, on facts that are trivial and known.** Compress it to at most one page: Lemma 2.2, one sentence on centring, and Prop. 3.2 as a remark with Loly's invariant. Move Remarks 3.4–3.5 to the companion paper, or delete them, keeping only the observation $\Sigma=\mathrm{diag}(a,a,c)$, which is needed for 1.2.
- Too many numbered items carry data: Prop. 4.4 counts, Rem. 4.6, Rem. 4.7 ranges, Prop. 5.1. Put the data in one census table and keep propositions for statements with proofs.
- Order: the Siamese theorem, the only all-$n$ theorem, is buried at the end of Section 5 as a Proposition. Promote it to Theorem and give it a section of its own, with Prop. 5.2 (forced vertices) as its preamble.
- Section 6 mixes recap, numerics belonging to the companion paper, and open questions. Keep only the open questions, rephrased as in 1.5.
- **Figures** (9 in total; 4–5 would suffice):
  - Fig. 1: keep (a) and (c). Panel (b) duplicates (c).
  - Fig. 2 (lines): illustrates a definition. Merge one row into Fig. 1 or cut.
  - Fig. 3: keep the top row (a–d). Rows e–l show eight congruent gems and illustrate a trivial proposition; cut them.
  - Fig. 4: panels (a) (checkers) and (c) (lever) are decorative. (d) is the only content and could be a two-line table.
  - Fig. 5: redundant with Fig. 4(c,d); cut.
  - Figs. 6 and 7: the same three squares in two renderings. Merge into one figure (gem plus point pairing).
  - Fig. 8: keep (histograms and extreme gems carry content).
  - Fig. 9: keep (essential to the Siamese proof).
- Captions: most stand alone, but several are too long and restate the text (Figs. 1, 3, 4). Fig. 6 caption, "(b) … has no other symmetry", should read "and no other symmetry".

---

## 4. Ten most important changes (ranked)

1. **Fix the false statements.** Prop. 3.1 (interior) and Prop. 4.5 (parity) fail for the coplanar associative row-by-row arrangement. Add a non-coplanarity/semi-magic hypothesis. Remove or repair the ill-posed Prop. 5.1(1).
2. **Prove the general point-set symmetry and congruence theorem** via $\Sigma=\mathrm{diag}(a,a,c)$, $a\ne c$ (1.2). Restate Thm 4.3 / Prop. 5.1(2) as "for $n=4$ the hull has no isometries beyond those of the point set".
3. **Promote the Siamese result to the main Theorem.** Phrase it as "the Siamese gem has no unforced vertices". Print the slack polynomials so the proof is checkable by hand, and close the small gap in Step 1.
4. **Connect to regular subdivisions/secondary fans** (De Loera–Rambau–Santos; Gelfand–Kapranov–Zelevinsky). That is the honest route to "polyhedral framework". Otherwise retitle (e.g. "The convex hull of a magic square").
5. **Cut Section 3 to about one page.** Drop "height-weighted centroid" (it is a dipole moment) and "what magic means" (it is semi-magic).
6. **Rewrite the abstract and Introduction claims.** Remove the centring identity, the box and the Ehrhart count from the abstract. Say "semi-magic". Credit Dudeney for the 48/304/528 partition and state precisely what is new.
7. **Remove or justify the Ehrhart section**, and move the random/annealed statistics (Rem. 3.5, Table 4) to the companion paper or reduce them to one paragraph. Rephrase Open Question 3 as a growth-rate question (cf. Bárány–Buchta).
8. **Strengthen the computational contribution.** Run the order-5 census (or the associative/pandiagonal order-5 subclasses), or generalise the Siamese theorem to all linear/cyclic constructions.
9. **Clean up notation and terminology**: $\rho$, $V$, $F$, $I$, $B$, $L$, $M$, $c$, $m$; "vertex/hull vertex/extreme point/hull fraction"; "order four/order-4".
10. **Halve the figures and remove process and defensive language** (Figs. 2, 3e–l, 4a–c, 5 cut; Figs. 6/7 merged; LaTeX comments; "This is a theorem …"; repeated "point set, not the solid" caveats).

---

## 5. Missing or imprecise literature

These are works I am confident exist and that bear directly on the paper:

- C. A. Rogers, G. C. Shephard, "The difference body of a convex body", *Arch. Math.* 8 (1957) 220–233. Two-sided bounds $2^d\le \mathrm{vol}(K-K)/\mathrm{vol}K\le\binom{2d}{d}$; the natural citation for Rem. 4.7.
- B. Grünbaum, "Measures of symmetry for convex sets", in *Convexity*, Proc. Sympos. Pure Math. 7, AMS (1963) 233–270. Background for $\sigma$ as a measure of asymmetry.
- J. A. De Loera, J. Rambau, F. Santos, *Triangulations: Structures for Algorithms and Applications*, Springer (2010); and I. M. Gelfand, M. M. Kapranov, A. V. Zelevinsky, *Discriminants, Resultants, and Multidimensional Determinants*, Birkhäuser (1994). Regular subdivisions induced by height functions and the secondary polytope, i.e. the framework the gem lives in.
- I. Bárány, C. Buchta, "Random polytopes in a convex polytope, independence of shape, and concentration of vertices", *Math. Ann.* 297 (1993) 467–497. Expected vertex counts $\sim c\log^{d-1}N$; relevant to Table 4 and Open Question 3.
- K. Pinn, C. Wieczerkowski, "Number of magic squares from parallel tempering Monte Carlo", *Int. J. Mod. Phys. C* 9 (1998) 541–546. Estimates for $n\ge6$, and a reference point for Monte Carlo sampling of magic squares (relevant to the annealing bias).
- B. Frénicle de Bessy, "Des quarrez ou tables magiques", in *Divers ouvrages de mathématique et de physique*, Paris (1693). The primary source for the 880, currently attributed only in words.
- S. de la Loubère, *Du Royaume de Siam* (1691; English trans. 1693). The primary source for the Siamese method, currently uncited.
- K. Ollerenshaw, D. S. Brée, *Most-Perfect Pandiagonal Magic Squares: Their Construction and Enumeration*, IMA (1998). For the pandiagonal statements in Rem. 4.6.
- W. Cook, M. Hartmann, R. Kannan, C. McDiarmid, "On integer points in polyhedra", *Combinatorica* 12 (1992) 27–37. Bounds on the vertex count of integer hulls, relevant if the Siamese argument is generalised to all linear constructions.

Imprecise citations:
- Dudeney's groups: specify the edition or table used. Numbering conventions differ between Dudeney's original and later reproductions (e.g. Trump's site).
- Loly 2004 is correctly cited for Cor. 3.3. The vanishing dipole moment $\sum z(x,y)=0$ is in Rogers–Loly's multipole papers, so cite them at Prop. 3.2 rather than only in the Introduction.
- The bibliography key `beck2010enumeration` carries year 2011 (cosmetic).
