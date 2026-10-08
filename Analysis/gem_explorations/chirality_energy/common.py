import sys, os
sys.path.insert(0, '/Users/kylemathewson/magicGem/paper_A_gems/anc')
import numpy as np
from fractions import Fraction
from scipy.spatial import ConvexHull
from gem_geometry import scaled_points

SQ = np.loadtxt('/Users/kylemathewson/magicGem/paper_A_gems/anc/squares880.txt', dtype=int).reshape(880, 4, 4)

def hull_int(P):
    """P: (k,3) int array (doubled coords). Returns (vol6 int [6*volume in doubled units], nverts) or (0,None) if degenerate.
    Exact integer volume from qhull triangulation (|det| sum from a vertex)."""
    P = np.asarray(P, dtype=np.int64)
    if np.linalg.matrix_rank((P - P[0]).astype(float)) < 3:
        return 0, 0
    h = ConvexHull(P.astype(float))
    ref = P[h.vertices[0]]
    A = P[h.simplices] - ref            # (m,3,3)
    # integer determinants via object-free int64 (values small)
    det = (A[:,0,0]*(A[:,1,1]*A[:,2,2]-A[:,1,2]*A[:,2,1])
          -A[:,0,1]*(A[:,1,0]*A[:,2,2]-A[:,1,2]*A[:,2,0])
          +A[:,0,2]*(A[:,1,0]*A[:,2,1]-A[:,1,1]*A[:,2,0]))
    return int(np.abs(det).sum()), len(h.vertices)

def vol_real(vol6):   # undo doubling: V = vol6/6/8
    return Fraction(vol6, 48)
