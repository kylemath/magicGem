# Statements (z = s-(N+1)/2, N=n^2, x,y centred; W = span of the 2n+2 line indicators)

T1 (exact, linear balance). E_full(S)=0  <=>  z is orthogonal to W.  Hence for every phi in W, i.e.
phi = a(x) + b(y) + c1*1_Dm + c2*1_Da (any function of column index plus any of row index plus the diagonal indicators),
sum_ij z_ij phi_ij = 0. In particular sum z = 0 (constant = sum of rows), the mass-weighted centroid
sum z (x,y) = 0 (zero torque / zero centre-of-mass offset, any mass s or z since sum x = sum y = 0), and
sum z x^k = sum z y^k = 0 for all k. (Semi-magic suffices for everything except the diagonal indicators.)
For n=4 these are the only vanishing moments in general: sum z x y is NOT implied (magic 4x4: 0..60 observed).
Correction to naive intuition: sum z (x^2+y^2)=0 holds for magic squares (Loly's invariant, in paper) because x^2+y^2 = (x^2)+(y^2) is in W.

T2 (quantitative, robust). |sum z (x,y)|^2 = N^2 (Cov(X,Z)^2+Cov(Y,Z)^2) <= N^2 * n(n^2-1)/12 * E_rc,
E_rc = sum over rows and columns of Cov^2 (Cauchy-Schwarz with x = sum x_l C_l, sum x_l^2 = n(n^2-1)/12).
Hence B_lin <= N sqrt(n(n^2-1)/12 * E_full). Checked on 3e5 random 4x4: 0 violations, max ratio 0.998 (sharp).
So small E_full => small linear imbalance. Same style bound for any phi in W: |<z,phi>| <= ||phi|| * ||P_W z|| and
||P_W z||^2 <= C_n * E_full (equivalence of the Gram-weighted and plain forms on a finite-dim space; constant n-dependent).

T3 (failure for non-linear model). Unit-vector models B_u = |sum m_ij u(x_ij,y_ij,z_ij)|, u=v/|v|, are sums
sum_ij m_ij f(x_ij,y_ij[,z_ij]) with f not in W (f=x/sqrt(x^2+y^2+..) is not a sum of function of x and function of y,
and for the 3D unit model f also depends on z, so it is not even linear in z). Hence E_full = 0 does not imply B_u = 0.
n=3 magic squares: unit2D B = 2.6197 (all 8 equal by symmetry), unit3D xy 1.5279, fixed-height c=1: 1.1606 -- all nonzero;
the z-component of sum m u is bounded away from 0 (m=z: sum z^2/|v| > 0) so full 3D B can never vanish.
Positive exception: a unit model reduces to the linear one when u is linearised (|v| replaced by a constant r0:
u = v/r0, all T1 applies), which is the only exactly-true "projection to balance of vectors".

T4 (reflection symmetry, n odd). Every 3x3 magic square is point-symmetric (s_c + s_c' = N+1), so z is odd under
(x,y)->(-x,-y); then sum z f = 0 for every f EVEN under reflection; odd f (like x/r) survives. That is why unit-model B is
nonzero but equal for all 8 squares.
