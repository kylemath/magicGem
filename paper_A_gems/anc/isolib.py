"""Exact isometry-group computation for finite point sets in R^3 (used by symmetry_880.py and the figure scripts)."""
import numpy as np
from collections import Counter

def isometries(P):
    """All isometries of the finite point set P (integer array, rows = points) as permutations.
    Exact: an isometry of R^3 preserving a set that affinely spans R^3 is determined by its action;
    we enumerate bijections of P determined by the images of an affine basis and verify that the
    resulting permutation preserves ALL integer squared distances."""
    k = len(P); P = np.asarray(P, dtype=np.int64)
    Q = k * P - P.sum(0)                      # centroid at origin, integers
    G = Q @ Q.T                               # Gram matrix (exact ints)
    # choose three linearly independent vectors
    basis = []
    for i in range(k):
        cand = basis + [i]
        if np.linalg.matrix_rank(Q[cand].astype(float)) == len(cand):
            basis = cand
        if len(basis) == 3: break
    assert len(basis) == 3, 'point set is degenerate'
    b = basis
    Binv = np.linalg.inv(Q[b].astype(float))  # Q[b] @ R^T = images
    perms = []
    cands = [[a for a in range(k) if G[a, a] == G[b[t], b[t]]] for t in range(3)]
    for a0 in cands[0]:
        for a1 in cands[1]:
            if G[a0, a1] != G[b[0], b[1]]: continue
            for a2 in cands[2]:
                if G[a0, a2] != G[b[0], b[2]] or G[a1, a2] != G[b[1], b[2]]: continue
                R = (Binv @ Q[[a0, a1, a2]].astype(float)).T      # orthogonal matrix, maps Q[b[t]] -> Q[a_t]
                img = (R @ Q.T).T
                idx = {tuple(q): t for t, q in enumerate(Q.tolist())}
                perm = []
                ok = True
                for q in img:
                    r = np.rint(q).astype(np.int64)
                    if np.abs(q - r).max() > 1e-7 or tuple(r.tolist()) not in idx: ok = False; break
                    perm.append(idx[tuple(r.tolist())])
                if not ok or len(set(perm)) != k: continue
                perm = np.array(perm)
                if not np.array_equal(G[np.ix_(perm, perm)], G): continue   # exact distance check
                perms.append((perm, R))
    return perms

def element_type(R):
    d = int(round(np.linalg.det(R))); t = float(np.trace(R))
    return {(1, 3): 'E', (1, -1): 'C2', (1, 0): 'C3', (1, 1): 'C4', (1, 2): 'C6',
            (-1, -3): 'i', (-1, 1): 's', (-1, -1): 'S4', (-1, 0): 'S6', (-1, -2): 'S3'}.get((d, int(round(t))), '?')

def group_name(types):
    c = Counter(types); o = sum(c.values())
    improper = sum(v for k, v in c.items() if k in ('i', 's', 'S4', 'S6', 'S3'))
    if o == 1: return 'C1'
    if o == 2: return {'C2': 'C2', 'i': 'Ci', 's': 'Cs'}[[k for k in c if k != 'E'][0]]
    if o == 4:
        if c['i'] == 1 and c['C2'] == 1 and c['s'] == 1: return 'C2h'
        if c['C2'] == 3: return 'D2'
        if c['C2'] == 1 and c['s'] == 2: return 'C2v'
        if c['S4'] == 2 and c['C2'] == 1: return 'S4'
        if c['C4'] == 2: return 'C4'
    if o == 8:
        if c['C2'] == 3 and c['i'] == 1 and c['s'] == 3: return 'D2h'
    return f'order{o}:' + ','.join(f'{k}{v}' for k, v in sorted(c.items()))

