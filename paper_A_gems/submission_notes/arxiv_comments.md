# arXiv metadata and notes for the replacement of arXiv:2512.09170 (for the author only; nothing here is in the paper)

Title (unchanged): Magic Gems: A Polyhedral Framework for Magic Squares
Replacement version: v5 (cross-list suggestion: math.CO primary; math.MG, math-ph optional).

## Suggested arXiv "Comments" field
20 pages, 8 figures; ancillary files (code and data) included. Replacement version: substantially rewritten; the orthogonality, moment-threshold and random-energy material is now in a companion paper (Mathewson, "Magic squares as orthogonality conditions: the permutation moment threshold and random line-sum energies").

## Suggested abstract (plain text, < 1920 characters)
To an n x n magic square we attach the n^2 points (x, y, z) in R^3, where (x, y) is the position of a cell measured from the centre of the grid and z is its entry minus the mean entry; their convex hull is the Magic Gem. Its lower and upper faces are the regular subdivisions of the grid induced by the entries and by their negatives. For the Siamese (de la Loubere) square of every odd order n >= 5 we prove that the gem has exactly the twelve vertices that the boundary of the grid forces (the four corners and, on each side, the cells of the smallest and largest entry), with f-vector (12,26,16) and isometry group {+-id}; the proof reduces to checking the signs of a table of polynomials in m = (n-1)/2. For the 880 magic squares of order four we compute all gems exactly, by computer: no gem has an isometry that its point set lacks; 48 gems are centrally symmetric, 304 have a single half-turn symmetry and 528 have none; the vertex set determines the square; and the gems form 616 congruence classes and 352 combinatorial types. A short covariance argument shows that, for semi-magic squares of every order, the point set has a non-trivial isometry exactly when the square equals its complement up to rotation and reflection. Other linear magic squares can have many more vertices: up to 18, 25, 31 and 36 for orders 5, 7, 9 and 11.

## Candid list: what v4 (and the intermediate v5 draft) got wrong or overstated
(Items 4-7 concern the intermediate v5 draft in arxiv_submission/ and were verified by computation/proof. Items 1-3 and 8 are taken from the old sources' own statements and the coordinator brief; check them against the posted v4 text before quoting.)
1. v4 Table 2 reported "typical" hull sizes (16 vertices for n=5, volume 95.0 for n=4). The exact order-4 values are 8-16 vertices (modal 12, 380/880), mean volume 84.05; order-5 hull sizes are not "16 typical" (Siamese 5 has 12).
2. v4 hardware statement was inaccurate; the paper now states the actual machine/software.
3. The "vectors from the centroid / unit-vector balance" reading: sum p_ij = 0 holds for ALL arrangements (it is just centring); v4's suggestion that it is magic-specific, and that it describes the solid hull, was wrong. Unit-vector balance models do not follow from the line conditions.
4. The draft claimed that the order-5 count 275,305,224 is the number of ALL squares and that there are 34,413,153 orbits. Wrong: 275,305,224 is already the number of essentially different squares (OEIS A006052; total 8 x that = 2,202,441,792). Fixed.
5. Draft claim "self-complementary => improper isometry of order 2 or 4, vertex orbits of size 2 or 4": wrong. For even n the complement element g is r^2, h or v (never a diagonal reflection or quarter-turn, since g^2 = id and g has no fixed cell). Only the 48 associative squares (g = r^2) have an improper isometry (inversion); the other 304 have a PROPER half-turn about a horizontal axis. Vertex orbits and facet orbits have size 2 (facets also size 1 for facets normal to the axis); never 4. Also, the claim "gem of self-complementary square is mirror-symmetric" is false for these 304: they are chiral.
6. Draft claim "every Dudeney group with more than 8 members spans at least four vertex counts": false (group X spans 3). Corrected to "at least three".
7. Draft Prop. on mixed moments was stated for n >= 3; it is false for n = 3 (all order-3 squares have sum z xy = 0, as they are associative). Now stated for n = 4, with the structural reason (associative => sum z xy = 0; 48 of the 56 vanishing classes).
8. Companion-paper material (energy statistics, v4 numbers) was corrected in paper B; consult its notes for those items.

## Verified numbers carried over (re-derived in this round by exact computation)
|P_xy|: 48 distinct values, 56 classes with value 0, max 60 (also over all 7040 squares: 48 values, 56 classes). 880 gems: V counts 7,10,103,80,380,106,162,14,18 (V=8..16); 39 f-vectors; 352 types; 155 volumes (58 to 292/3); 880 distinct hull-vertex sets; 616 congruence classes = complement orbits; Siamese f = (12,26,16) for n=5..21 (direct hulls) and symbolic proof for all m>=2. Lo Shu/Duerer/Siamese-5 volumes 18, 92, 830/3.

## Unverified / softened attributions
Lo Shu "Chinese tradition" (no date claimed); Frenicle's list "published 1693" (standard attribution, not independently checked here); Schroeppel 1973 via Gardner, Sci. Am. 234(1):118 (Jan 1976) (confirmed by web search of citations, text of the column itself not read); no enumeration claim for n>=6.
