"""energy_zeros_count.py -- exact numbers of arrangements of order 4
  (1) whose first moments sum_ij z_ij x_j and sum_ij z_ij y_i vanish: the second family of Table tab:magic-vs-random;
  (2) whose first moments vanish and whose two diagonals sum to 34, i.e. the zeros of the four-term energy of
      version 4 (item (v) of "Changes from earlier versions"; every magic square is one of them).
Meet in the middle over the top two rows (cells 0..7) and the bottom two rows (cells 8..15): for each 8-set V of
values in the top half and each of the 8! placements of V and of its complement, the partial sums of
sum_ij j s_ij (target 204), sum_ij i s_ij (target 204) and, for (2), of the two diagonals (target 34 each) are packed
into an integer key, and matching keys are counted with multiplicities.  The digits of a key differ from the target
by less than 1000 in absolute value, so equal keys mean equal partial sums.
Usage: python3 energy_zeros_count.py   (about 3 min).  Writes energy_zeros_count.log; expected totals
6,697,177,424 and 14,639,440.
"""
import itertools, os, time, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FACT16 = 20_922_789_888_000

P = np.array(list(itertools.permutations(range(8))), dtype=np.int64)
top = [(i, j) for i in (0, 1) for j in range(4)]
bot = [(i, j) for i in (2, 3) for j in range(4)]
allv = np.arange(1, 17)


def count(diagonals):
    def coef(cells):
        rows = [[j for i, j in cells], [i for i, j in cells]]
        if diagonals:
            rows += [[int(i == j) for i, j in cells], [int(i + j == 3) for i, j in cells]]
        return np.array(rows, dtype=np.int64).T
    Ct, Cb = coef(top), coef(bot)
    tgt = np.array([204, 204, 34, 34][:Ct.shape[1]], dtype=np.int64)
    base = np.array([1, 1000, 10 ** 6, 10 ** 9][:Ct.shape[1]], dtype=np.int64)
    total = 0
    for V in itertools.combinations(range(1, 17), 8):
        V = np.array(V); Vc = np.setdiff1d(allv, V)
        ua, ca = np.unique((V[P] @ Ct) @ base, return_counts=True)
        ub, cb = np.unique((tgt - Vc[P] @ Cb) @ base, return_counts=True)
        _, ia, ib = np.intersect1d(ua, ub, assume_unique=True, return_indices=True)
        total += int((ca[ia] * cb[ib]).sum())
    return total


log = []
t0 = time.time()
xy = count(False)
assert xy == 6_697_177_424, xy
log.append(f'arrangements of order 4 with vanishing first moments: {xy} of 16!, one in {FACT16 / xy:.1f} '
           f'({time.time() - t0:.0f} s)')
print(log[-1], flush=True)

t0 = time.time()
total = count(True)
assert total == 14_639_440, total
# the 7040 magic squares (all7040_dudeney.tsv) are distinct and all satisfy the four conditions
rows = list(csv.reader(open(os.path.join(HERE, 'all7040_dudeney.tsv')), delimiter='\t'))[1:]
Q = np.array([[int(v) for v in r[3:19]] for r in rows]).reshape(-1, 4, 4)
J = np.arange(4)
assert len(Q) == len({q.tobytes() for q in Q}) == 7040
assert ((Q.sum(1) == 34).all() and (Q.sum(2) == 34).all()
        and ((Q * J[None, None, :]).sum((1, 2)) == 204).all() and ((Q * J[None, :, None]).sum((1, 2)) == 204).all()
        and (np.trace(Q, axis1=1, axis2=2) == 34).all() and (Q[:, J, 3 - J].sum(1) == 34).all())
expected = 60_000_000 * (total - 7040) / FACT16
log.append(f'arrangements of order 4 with vanishing first moments and both diagonals summing to 34: {total} of 16!, '
           f'7040 of them magic; expected number of non-magic ones among 6*10^7 uniform samples {expected:.1f} '
           f'({time.time() - t0:.0f} s)')
print(log[-1])
open(os.path.join(HERE, 'energy_zeros_count.log'), 'w').write('\n'.join(log) + '\n')
