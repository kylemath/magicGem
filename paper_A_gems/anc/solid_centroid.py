"""Number of order-4 gems whose solid centre of mass differs from the origin, and inner core gem statistics (Appendix C, Section 7)."""
import os, sys
from fractions import Fraction
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import scaled_points, exact_hull

S = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)

def exact_solid_centroid_2P(pts_int):
    h = ConvexHull(pts_int)
    p0 = [Fraction(int(pts_int[0, j]), 1) for j in range(3)]
    vol_tot = Fraction(0)
    mom = [Fraction(0), Fraction(0), Fraction(0)]
    for s in h.simplices:
        a = [Fraction(int(pts_int[s[0], j])) - p0[j] for j in range(3)]
        b = [Fraction(int(pts_int[s[1], j])) - p0[j] for j in range(3)]
        c = [Fraction(int(pts_int[s[2], j])) - p0[j] for j in range(3)]
        det = (a[0]*(b[1]*c[2] - b[2]*c[1])
             - a[1]*(b[0]*c[2] - b[2]*c[0])
             + a[2]*(b[0]*c[1] - b[1]*c[0]))
        v = abs(det)
        vol_tot += v
        for j in range(3):
            mom[j] += v * (4*p0[j] + a[j] + b[j] + c[j])
    return [mom[j] / (4 * vol_tot) for j in range(3)]

cnt = 0
dims = {0: 0, 1: 0, 2: 0, 3: 0}
c1_zero = 0
c1_opp = 0
for k in range(880):
    h = exact_hull(S[k]); P = h['P']
    c0 = exact_solid_centroid_2P(P)
    if any(x != 0 for x in c0):
        cnt += 1
    verts = set(h['vertices'])
    inner_idx = [i for i in range(16) if i not in verts]
    if not inner_idx:
        continue
    Q = P[inner_idx]
    rk = int(np.linalg.matrix_rank(Q - Q[0])) if len(Q) > 1 else 0
    dims[rk] += 1
    if rk == 3:
        c1 = exact_solid_centroid_2P(Q)
        if all(x == 0 for x in c1):
            c1_zero += 1
        else:
            cross = [c0[1]*c1[2]-c0[2]*c1[1], c0[2]*c1[0]-c0[0]*c1[2], c0[0]*c1[1]-c0[1]*c1[0]]
            dot = sum(c0[j]*c1[j] for j in range(3))
            if all(x == 0 for x in cross) and dot < 0:
                c1_opp += 1

assert cnt == 829 and dims == {3: 511, 2: 175, 1: 162, 0: 14} and c1_zero == 207 and c1_opp == 33
print('gems with solid centroid != origin:', cnt, 'of 880')
print('inner core gem dimensions (3D, 2D, 1D, 0D):', dims, 'total non-empty:', sum(dims.values()))
print('3D inner core gems with solid centroid == origin:', c1_zero, '; opposite collinear c0, c1:', c1_opp)
