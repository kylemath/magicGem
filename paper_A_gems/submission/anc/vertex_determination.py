"""
vertex_determination.py -- how the vertex set of an order-four gem determines the square (Remark 5.5 of the paper).

For each of the 880 squares S (squares880.txt) let U be the set of cells whose points are not vertices of the gem.
The vertex set gives the entries on the other cells; the 10 line sums (= 34) give linear equations for the entries
on U, with 0/1 coefficient matrix A_U (lines x cells of U).  If rank A_U = |U| (exact rank) the entries on U, and so
S, are determined by linear algebra.  For the other squares we enumerate every magic completion: every way to put the
remaining entries on U with all line sums 34, and compute the exact hull of each completion T != S.
Asserted: 871 classes are linearly determined; the 9 others are listed; 4 of them have a second magic completion, and
for every such completion T the vertex set of G(T) differs from that of G(S), so that the vertex set of the gem
determines the square (among magic squares, and up to D4 by equivariance).  Writes vertex_determination.log.
"""
import os, sys, itertools
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull

SQ = [np.array(list(map(int, l.split()))).reshape(4, 4) for l in open(os.path.join(HERE, 'squares880.txt')) if l.strip()]
LINES = [[(i, j) for j in range(4)] for i in range(4)] + [[(i, j) for i in range(4)] for j in range(4)] \
    + [[(i, i) for i in range(4)], [(i, 3 - i) for i in range(4)]]
CELLS = [(i, j) for i in range(4) for j in range(4)]


def d4canon(S):
    T = S; best = None
    for _ in range(4):
        for X in (T, T.T):
            t = tuple(X.ravel()); best = t if best is None or t < best else best
        T = np.rot90(T)
    return best


IDX = {d4canon(S): k for k, S in enumerate(SQ)}
LOG = []


def log(s):
    print(s, flush=True); LOG.append(s)


def vert_map(S):
    h = exact_hull(S)
    return {CELLS[v]: int(S[CELLS[v]]) for v in h['vertices']}


lin, nonlin, ambiguous = 0, [], []
rank_deficit = {}
for k, S in enumerate(SQ):
    vm = vert_map(S)
    U = [c for c in CELLS if c not in vm]
    A = sp.Matrix([[1 if c in L else 0 for c in U] for L in LINES]) if U else sp.zeros(10, 0)
    r = A.rank() if U else 0
    if r == len(U):
        lin += 1
        continue
    rank_deficit[k] = (len(U), r)
    nonlin.append(k)
    rest = sorted(set(range(1, 17)) - set(vm.values()))
    comps = []
    for perm in itertools.permutations(rest):
        T = S.copy()
        for c, v in zip(U, perm):
            T[c] = v
        if all(sum(int(T[c]) for c in L) == 34 for L in LINES):
            comps.append(T)
    assert any((T == S).all() for T in comps)
    others = [T for T in comps if not (T == S).all()]
    for T in others:
        assert vert_map(T) != vm, (k, T)        # the alternative completion has a different gem vertex set
    if others:
        ambiguous.append(k)
        log(f'#{k}: |U| = {len(U)}, rank {r}; {len(others)} other magic completion(s) with the same entries on the '
            f'vertex cells: ' + '; '.join(f'#{IDX[d4canon(T)]} (rows {T.tolist()}, V = {len(exact_hull(T)["vertices"])})'
                                               for T in others) + f'; S = {S.tolist()}, V = {len(vm)}')
    else:
        log(f'#{k}: |U| = {len(U)}, rank {r}; S is the only magic completion; S = {S.tolist()}, V = {len(vm)}')
assert lin == 871 and len(nonlin) == 9 and len(ambiguous) == 4, (lin, nonlin, ambiguous)
log(f'linearly determined: {lin} of 880; not linearly determined: {len(nonlin)} {nonlin}; '
    f'with a second magic completion: {len(ambiguous)} {ambiguous}; every second completion has a different vertex set')
open(os.path.join(HERE, 'vertex_determination.log'), 'w').write('\n'.join(LOG) + '\n')
