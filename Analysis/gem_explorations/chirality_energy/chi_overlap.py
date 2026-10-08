"""Task 4b: chirality chi(P) = 1 - max_{R in SO(3), t} vol(P ∩ (R M P + t)) / vol(P), M = z-reflection (= complement map).
Numerical (upper bound on chi: optimiser gives a lower bound on overlap). Compared for each gem and its complement partner."""
import json, itertools, sys
from common import *
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import minimize, linprog
from scipy.spatial.transform import Rotation as Rot
from multiprocessing import Pool

def hull_halfspaces(V):
    h = ConvexHull(V)
    return h.equations.copy(), h   # rows (n, d): n.x + d <= 0

def cheb(H):
    A, b = H[:, :3], -H[:, 3]
    nrm = np.linalg.norm(A, axis=1)
    r = linprog([0,0,0,-1], A_ub=np.c_[A, nrm], b_ub=b, bounds=[(None,None)]*3+[(0,None)], method='highs')
    return (r.x[:3], r.x[3]) if r.status == 0 else (None, 0)

def inter_vol(H1, H2):
    H = np.vstack([H1, H2])
    c0 = None
    # quick interior guess handled by LP
    c, r = cheb(H)
    if c is None or r < 1e-9: return 0.0
    try:
        hs = HalfspaceIntersection(H, c)
        return ConvexHull(hs.intersections).volume
    except Exception:
        return 0.0

OCT = [Rot.from_matrix(np.array(m)) for m in
       {tuple(map(tuple, (np.array(p) * np.array(s)[:, None]).astype(int))) for p in itertools.permutations(np.eye(3, dtype=int)) for s in itertools.product([1,-1], repeat=3)}
       if np.linalg.det(np.array(m)) > 0]
assert len(OCT) == 24

def chi_of(Vh):
    """Vh: float vertex array (hull vertices) of P in doubled coords. Return (chi_hat, trace)."""
    c = Vh.mean(0)  # placeholder, replaced by solid centroid below
    h = ConvexHull(Vh); vol = h.volume
    # solid centroid
    cs = np.zeros(3)
    for s in h.simplices:
        T = np.vstack([Vh[h.vertices[0]], Vh[s]]); cs += abs(np.linalg.det(T[1:] - T[0])) / 6 * T.mean(0)
    cs /= vol
    P0 = Vh - cs
    M = np.diag([1.0, 1.0, -1.0])
    Q0 = P0 @ M.T
    H1 = h.equations.copy(); H1[:, 3] = -(H1[:, :3] @ cs) * 0 + (H1[:, 3] + H1[:, :3] @ cs)  # shift to centroid frame
    def ov(x):
        R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]
        Q = Q0 @ R.T + t
        H2 = ConvexHull(Q).equations
        return inter_vol(H1, H2) / vol
    starts = []
    for R in OCT:
        x = np.r_[R.as_rotvec(), 0, 0, 0]; starts.append((ov(x), x))
    starts.sort(key=lambda a: -a[0])
    best = starts[0]
    for v0, x0 in starts[:3]:
        r = minimize(lambda x: -ov(x), x0, method='Nelder-Mead', options=dict(xatol=1e-4, fatol=1e-7, maxiter=400, initial_simplex=np.vstack([x0] + [x0 + 0.15 * np.eye(6)[i] * (1 if i < 3 else 2) for i in range(6)])))
        if -r.fun > best[0]: best = (-r.fun, r.x)
    return 1 - best[0], starts[0][0]

def work(k):
    P = scaled_points(SQ[k]).astype(float)
    V = P[ConvexHull(P).vertices]
    chi, chi24 = chi_of(V)
    return k, chi, 1 - chi24

if __name__ == '__main__':
    with Pool(15) as p:
        out = p.map(work, range(880), chunksize=4)
    chi = np.array([o[1] for o in out]); chi24 = np.array([o[2] for o in out])
    geo = json.load(open('/Users/kylemathewson/magicGem/paper_A_gems/anc/results_geometry.json'))
    part = np.array(geo['complement_partner'])
    sym = json.load(open('/Users/kylemathewson/magicGem/paper_A_gems/anc/symmetry_880.json'))
    grp = np.array([s['group'] for s in sym])
    json.dump(dict(chi=chi.tolist(), chi_best_of_24_octahedral=chi24.tolist(), group=grp.tolist(), partner=part.tolist()), open('results_chi_overlap.json', 'w'))
    print('done')
