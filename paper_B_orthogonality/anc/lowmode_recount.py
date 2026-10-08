#!/usr/bin/env python3
"""Recount of the class L_4 and of Table 4, written independently of lowmode_enum.c (NumPy).

  python3 lowmode_recount.py L      |L_4| split by the number of rows with sum 34 (row margins of Table 4; ~2-3 min)
  python3 lowmode_recount.py XY     the class <x,z> = <y,z> = 0 only (6,697,177,424), split the same way
  python3 lowmode_recount.py ROW4   members of L_4 with all four row sums 34, by the number of columns with
                                    sum 34 (the row "4" of Table 4), by direct enumeration (seconds)

Modes L and XY: meet in the middle over the top two rows (cells 0..7) and bottom two rows (cells 8..15).  For each
8-set V of values placed in the top half and each of the 8! placements of V and of its complement, the partial
sums of U1 = sum j s_ij, U2 = sum i s_ij (and, in mode L, of the two diagonal sums) are packed into an integer key;
matching keys are counted with multiplicities.  Row sums are separable across the split, so each half is tagged
with its number of rows summing to 34.  By symmetry under transposition the column margins equal the row margins.
"""
import itertools, sys, time
from collections import Counter, defaultdict
import numpy as np


def mitm(diagonals=True):
    P = np.array(list(itertools.permutations(range(8))), dtype=np.int64)
    top = [(i, j) for i in (0, 1) for j in range(4)]; bot = [(i, j) for i in (2, 3) for j in range(4)]

    def coef(cells):
        d = 1 if diagonals else 0
        return np.array([[j for i, j in cells], [i for i, j in cells], [d * int(i == j) for i, j in cells],
                         [d * int(i + j == 3) for i, j in cells]], dtype=np.int64).T
    Ct, Cb = coef(top), coef(bot)
    Rt = np.array([[int(c[0] == r) for r in (0, 1)] for c in top]); Rb = np.array([[int(c[0] == r) for r in (2, 3)] for c in bot])
    tgt = np.array([204, 204, 34 if diagonals else 0, 34 if diagonals else 0]); base = np.array([1, 1000, 10 ** 6, 10 ** 9], dtype=np.int64)
    hist = np.zeros(5, dtype=np.int64); allv = np.arange(1, 17)

    def table(keys, tags):
        u, inv = np.unique(keys, return_inverse=True); M = np.zeros((len(u), 3), dtype=np.int64); np.add.at(M, (inv, tags), 1)
        return u, M
    for V in itertools.combinations(range(1, 17), 8):
        V = np.array(V); Vc = np.setdiff1d(allv, V)
        XA = V[P]; XB = Vc[P]
        ka = (XA @ Ct) @ base; kb = (tgt - XB @ Cb) @ base
        ta = ((XA @ Rt) == 34).sum(1); tb = ((XB @ Rb) == 34).sum(1)
        ua, MA = table(ka, ta); ub, MB = table(kb, tb)
        common, ia, ib = np.intersect1d(ua, ub, return_indices=True)
        if len(common) == 0:
            continue
        A = MA[ia]; B = MB[ib]
        for a in range(3):
            for b in range(3):
                hist[a + b] += int((A[:, a] * B[:, b]).sum())
    return hist


def row4():
    S4 = [c for c in itertools.combinations(range(1, 17), 4) if sum(c) == 34]
    parts = []

    def rec(rem, acc):
        if not rem:
            parts.append(acc); return
        for c in S4:
            if set(c) <= rem:
                rec(rem - set(c), acc + [c])
    rec(set(range(1, 17)), [])
    perms = {c: list(itertools.permutations(c)) for c in S4}

    def half(r0, r1, i0):
        d = defaultdict(list)
        for p in perms[r0]:
            for q in perms[r1]:
                dm = p[i0] + q[i0 + 1]; da = p[3 - i0] + q[2 - i0]
                u = sum(j * (p[j] + q[j]) for j in range(4))
                d[(dm, da, u)].append(tuple(p[j] + q[j] for j in range(4)))
        return d
    hist = Counter()
    for Pt in parts:
        top = half(Pt[0], Pt[1], 0); bot = half(Pt[2], Pt[3], 2)
        for (dm, da, u), L in top.items():
            M = bot.get((34 - dm, 34 - da, 204 - u))
            if not M:
                continue
            for a in L:
                for b in M:
                    hist[sum(1 for j in range(4) if a[j] + b[j] == 34)] += 1
    return len(parts), hist


if __name__ == '__main__':
    mode = (sys.argv[1:] or ['L'])[0].upper(); t0 = time.time()
    if mode in ('L', 'XY'):
        h = mitm(diagonals=(mode == 'L'))
        print(mode, 'members by number of rows with sum 34 (0..4):', h.tolist(), 'total', int(h.sum()), '(%.0f s)' % (time.time() - t0))
    elif mode == 'ROW4':
        npart, h = row4()
        print('ordered partitions of 1..16 into four 34-sets:', npart)
        print('L_4 with all rows 34, by number of columns with sum 34:', sorted(h.items()), 'total', sum(h.values()))
    else:
        sys.exit(__doc__)
