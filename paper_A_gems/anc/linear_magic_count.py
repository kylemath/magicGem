"""
linear_magic_count.py -- the magic conditions on the parameters of linear squares (Proposition 6.1 of the paper),
    s(c) = n<u.c + alpha> + <w.c + beta> + 1,  c = (i,j),  u, w in Z_n^2,  alpha, beta in Z_n,  n odd,
and the number of D4-classes they give.

Claim (proved in the paper): s is a magic square iff
  (a) u1, u2, w1, w2 and det(u; w) = u1 w2 - u2 w1 are units mod n, and
  (b) for each digit (u, alpha) and (w, beta) and each diagonal: if the step sigma of the digit along the diagonal
      (u1+u2 on the main diagonal, u1-u2 on the anti-diagonal) is not a unit, d = gcd(sigma, n), then its offset
      tau (alpha, resp. alpha - u2) satisfies tau = (d-1)/2 mod d.
Writing r = u1/u2 (a unit), the number of admissible alpha is f(r) = n / (gcd(r+1,n) gcd(r-1,n)), so
  #squares = phi(n)^2 * sum over units r_u, r_w with r_u - r_w a unit of f(r_u) f(r_w),   #D4-classes = #squares / 8.
For n = p prime this is (p-1)^3 (p^3 - 6p^2 + 10p - 2) / 8.

This script counts the linear magic squares by brute force (actual line sums of the actual squares, bijectivity by
distinct entries) for odd n = 3..25, checks the criterion (a)-(b) square by square and the count formula, and compares
with the class counts of linear_squares.py (n = 5, 7, 9, 11).  Writes linear_magic_count.log.
"""
import os, sys, json, time, itertools
from math import gcd
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = []


def log(s):
    print(s, flush=True); LOG.append(s)


def formula(n):
    U = [r for r in range(1, n) if gcd(r, n) == 1]
    f = {r: n // (gcd(r + 1, n) * gcd(r - 1, n)) for r in U}
    tot = sum(f[a] * f[b] for a in U for b in U if gcd((a - b) % n, n) == 1)
    return len(U) ** 2 * tot


def units_ok(n, u1, u2, w1, w2):
    return all(gcd(a % n, n) == 1 for a in (u1, u2, w1, w2, u1 * w2 - u2 * w1))


def digit_ok(n, a1, a2, off):
    """condition (b) for one digit with coefficients (a1, a2) and offset off"""
    for sigma, tau in ((a1 + a2, off), (a1 - a2, off - a2)):
        d = gcd(sigma % n, n)
        if d > 1 and tau % d != (d - 1) // 2:
            return False
    return True


def criterion(n, u1, u2, w1, w2, al, be):
    return units_ok(n, u1, u2, w1, w2) and digit_ok(n, u1, u2, al) and digit_ok(n, w1, w2, be)


def brute(n):
    """number of (u, w, alpha, beta) giving a magic square, by computing the squares' line sums"""
    I, J = np.indices((n, n)); N = n * n; M = n * (N + 1) // 2
    ar = np.arange(n)
    cnt = 0
    for u1, u2, w1, w2 in itertools.product(range(n), repeat=4):
        A0 = (u1 * I + u2 * J) % n; B0 = (w1 * I + w2 * J) % n
        if len(np.unique(n * A0 + B0)) != N:          # not a bijection (independent of alpha, beta)
            assert not criterion(n, u1, u2, w1, w2, 0, 0)
            continue
        A = (A0[None] + ar[:, None, None]) % n          # A[alpha]
        B = (B0[None] + ar[:, None, None]) % n          # B[beta]
        def lines(X):                                  # (n_offsets, 2n+2) line sums
            return np.concatenate([X.sum(2), X.sum(1), np.trace(X, axis1=1, axis2=2)[:, None],
                                   np.trace(X[:, :, ::-1], axis1=1, axis2=2)[:, None]], 1)
        LA, LB = lines(A), lines(B)
        # line sums of s = n*A + B + 1 for every (alpha, beta)
        L = n * LA[:, None, :] + LB[None, :, :] + n
        ok = (L == M).all(2)
        crit = units_ok(n, u1, u2, w1, w2) * np.outer([digit_ok(n, u1, u2, a) for a in range(n)],
                                                       [digit_ok(n, w1, w2, b) for b in range(n)])
        assert (ok == crit).all(), (n, u1, u2, w1, w2)
        cnt += int(ok.sum())
    return cnt


ref = json.load(open(os.path.join(HERE, 'results_linear_squares.json')))
for n in range(3, 27, 2):
    t0 = time.time()
    b = brute(n); f = formula(n)
    assert b == f and b % 8 == 0, (n, b, f)
    line = f'n={n}: {b} linear magic squares = formula, {b // 8} D4-classes'
    if all(gcd(n, k) == 1 for k in range(2, n)):
        p = n; assert b // 8 == (p - 1) ** 3 * (p ** 3 - 6 * p ** 2 + 10 * p - 2) // 8; line += ' = (p-1)^3 (p^3-6p^2+10p-2)/8'
    if str(n) in ref:
        assert ref[str(n)]['classes'] == b // 8; line += ' = linear_squares.py'
    if n % 3 == 0:
        U = [r for r in range(1, n) if gcd(r, n) == 1]
        assert all((r - 1) % 3 == 0 or (r + 1) % 3 == 0 for r in U)
        line += '; 3 | n: every unit r has 3 | r-1 or 3 | r+1, so each digit has a diagonal with a non-unit step'
    line += f' ({time.time() - t0:.0f} s)'
    log(line)
log('criterion (a)-(b) agrees with the actual line sums for every parameter tuple, n = 3..25')
open(os.path.join(HERE, 'linear_magic_count.log'), 'w').write('\n'.join(LOG) + '\n')
