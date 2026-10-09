"""Number of order-4 gems whose solid centre of mass differs from the origin (supplementary; the paper's moment statements concern the point set, Section 3)."""
import os, sys
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import scaled_points
S = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
cnt = 0
for k in range(880):
    P = scaled_points(S[k]) / 2.0; h = ConvexHull(P); c = np.zeros(3); v = 0
    for s in h.simplices:
        a, b, cc = P[s]; vol = abs(np.linalg.det(np.array([a, b, cc]))) / 6; v += vol; c += vol * (a + b + cc) / 4
    if np.abs(c / v).max() > 1e-9: cnt += 1
print('gems with solid centroid != origin:', cnt, 'of 880')
