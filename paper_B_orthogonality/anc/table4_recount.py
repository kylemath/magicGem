#!/usr/bin/env python3
"""Recount of the remaining entries of Table 4, written independently of lowmode_enum.c (NumPy; ~17 min).

  python3 table4_recount.py

Counts N(i,j) = #{S in L_4 : row i and column j both sum to 34} for i, j in {0, 1} (the other rows and columns
follow by the symmetries of L_4), by a meet-in-the-middle over the top two rows and the bottom two rows in which
the partial sum of column j is appended to the matching key.  With r(S), c(S) the numbers of rows and columns of S
with sum 34, sum_{S in L_4} r(S)c(S) = 4 (N00 + N01 + N10 + N11) by the symmetry i -> 3-i, j -> 3-j; given the
row "4" of Table 4 (lowmode_recount.py ROW4: a(1,4) = 9,336, a(4,4) = 7,040) this determines the cell a(1,1):
  sum r c = a(1,1) + 2*4*a(1,4) + 16*a(4,4).
Also printed: |L_4| and the numbers R0, R1 of members with row 0, resp. row 1, summing to 34 (and C0, C1 for columns).
"""
import itertools, time
import numpy as np

perms = np.array(list(itertools.permutations(range(8))), dtype=np.int16)
cells = [(r, c) for r in range(2) for c in range(4)]


def coef(rowoff):
    rows = np.array([r + rowoff for r, c in cells]); cols = np.array([c for r, c in cells])
    return np.stack([cols, rows, (rows == cols).astype(int), (rows + cols == 3).astype(int)]).T  # U1..U4 per cell


CT, CB = coef(0), coef(2)
colmask = [np.array([c == j for r, c in cells], int) for j in range(4)]
rowmask = [np.array([r == i for r, c in cells], int) for i in range(2)]
target = np.array([204, 204, 34, 34]); OFF = 512; BASE = 1024


def pack(M):
    M = M + OFF
    return (((M[:, 0] * BASE + M[:, 1]) * BASE + M[:, 2]) * BASE + M[:, 3]) * BASE + M[:, 4]


def cnt(top, bot):
    bot = np.sort(bot)
    return int((np.searchsorted(bot, top, 'right') - np.searchsorted(bot, top, 'left')).sum())


tot = dict(L=0, R0=0, R1=0, N00=0, N01=0, N10=0, N11=0, C0=0, C1=0)
t0 = time.time(); allv = np.arange(1, 17)
for V in itertools.combinations(range(1, 17), 8):
    V = np.array(V); W = np.setdiff1d(allv, V)
    a = V[perms].astype(np.int64); b = W[perms].astype(np.int64)
    uA = a @ CT; uB = target - (b @ CB)
    z = np.zeros((len(a), 1), np.int64)
    colA = [(a @ colmask[j])[:, None] for j in range(2)]
    colB = [(34 - b @ colmask[j])[:, None] for j in range(2)]
    kA = pack(np.hstack([uA, z])); kB = pack(np.hstack([uB, z]))
    r = [(a @ rowmask[i]) == 34 for i in range(2)]
    tot['L'] += cnt(kA, kB); tot['R0'] += cnt(kA[r[0]], kB); tot['R1'] += cnt(kA[r[1]], kB)
    for j in range(2):
        kAj = pack(np.hstack([uA, colA[j]])); kBj = np.sort(pack(np.hstack([uB, colB[j]])))
        tot['C%d' % j] += cnt(kAj, kBj)
        for i in range(2):
            tot['N%d%d' % (i, j)] += cnt(kAj[r[i]], kBj)
print(tot, 'time %.0f s' % (time.time() - t0))
S = 4 * (tot['N00'] + tot['N01'] + tot['N10'] + tot['N11'])
print('sum_S r(S)c(S) =', S, ' a(1,1) =', S - 8 * 9336 - 16 * 7040)
