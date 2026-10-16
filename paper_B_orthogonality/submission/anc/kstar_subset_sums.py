#!/usr/bin/env python3
"""Pigeonhole criterion (Proposition 3.13 of the paper) with all subset sums, for n = 2h, h even (Proposition 3.14).

The square of Proposition 3.14(i): for 0 <= q, r < h, t = q*h + r, eps_q = (-1)^q,
    s[r][2q] = (N+1 + eps_q (4t+1))/2,  s[r][2q+1] = (N+1 - eps_q (4t+3))/2,  s[h+r][j] = N+1 - s[r][j].
Rows r and h+r are complementary on all columns; the swap difference in column pair q, row r, is
d_{q,r} = -2 eps_q (2qh + 2r + 1), and F_q is the set of subset sums of {d_{q,r}}_r.

python3 kstar_subset_sums.py        (about half a minute)
  * checks Proposition 3.14(i) (the square is semi-magic, rows complementary) for every even h <= 100;
  * checks the counting of Proposition 3.14(ii) for every even h <= 60 and 1 <= q < h: the sets E_k of k-subset
    sums with k = ceil(h/4) + j*ceil(h/(4q)) <= 3h/4 are disjoint intervals of an arithmetic progression, their
    number is >= q(2h-3)/(5h), and |F_q| >= 3qh(2h-3)/80 >= qh^2/40 (h >= 4);
  * prints the largest K with prod_q |F_q| > prod_{s<=K-2} ((N-1) sum_q r_q C(q,s) + 1) (exact |F_q|), next to the
    value from |F_q| >= ceil(r_q/2)+1 for the squares of Lemma 3.12 (lower_bound_34 in make_figures.py);
  * for that bound, the smallest even and odd n at which (11) gives K >= 2 (14 and 21) and K at n = 999, 1000, 1001.
Writes kstar_subset_sums.json (n -> K) for 8 <= n <= 200, 4 | n."""
import json, os, sys
from math import comb, log, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))


def block_square(n):
    h = n // 2; assert n % 4 == 0
    N = n * n; s = [[0] * n for _ in range(n)]
    for r in range(h):
        for q in range(h):
            t = q * h + r; e = 1 if q % 2 == 0 else -1
            a = (N + 1 + e * (4 * t + 1)) // 2; b = (N + 1 - e * (4 * t + 3)) // 2
            s[r][2 * q], s[r][2 * q + 1] = a, b
            s[h + r][2 * q], s[h + r][2 * q + 1] = N + 1 - a, N + 1 - b
    return s


def check_square(s):
    n = len(s); h = n // 2; N = n * n; M = n * (N + 1) // 2
    assert sorted(v for row in s for v in row) == list(range(1, N + 1))
    assert all(sum(row) == M for row in s) and all(sum(s[i][j] for i in range(n)) == M for j in range(n))
    assert all(s[r][j] + s[h + r][j] == N + 1 for r in range(h) for j in range(n))


def n_subset_sums(ds):
    """number of distinct subset sums of the integers ds (bitset)"""
    bits = 1
    for d in ds:
        bits = (bits << d) | bits if d > 0 else (bits << -d) | bits   # translate: same count as for |d|
    return bin(bits).count('1')


def criterion(n, F, r):
    """largest K >= 2 with prod |F_q| > prod_{s=0}^{K-2} ((N-1) sum_q r_q C(q,s) + 1), or None"""
    N = n * n; lhs = 1
    for f in F:
        lhs *= f
    best = None; K = 2
    while True:
        rhs = 1
        for s in range(K - 1):
            rhs *= (N - 1) * sum(r[q] * comb(q, s) for q in range(len(r))) + 1
        if lhs > rhs:
            best = K; K += 1
        else:
            return best


def F_sizes(n):
    s = block_square(n); h = n // 2
    return [n_subset_sums([s[r][2 * q + 1] - s[r][2 * q] for r in range(h)]) for q in range(h)]


def lower_bound_subset(n):
    """K given by Proposition 3.13 for the square of Proposition 3.14 (4 | n, n >= 8), exact |F_q|"""
    if n % 4 or n < 8:
        return None
    return criterion(n, F_sizes(n), [n // 2] * (n // 2))


def check_counting(h):
    for q in range(1, h):
        A = [2 * q * h + 2 * r + 1 for r in range(h)]
        F = n_subset_sums(A)
        s = -(-h // (4 * q)); k0 = -(-h // 4)
        ks = [k for k in range(k0, h + 1, s) if 4 * k <= 3 * h]
        E = [(2 * q * h * k + k * k, 2 * q * h * k + 2 * k * h - k * k) for k in ks]
        assert all(a[1] < b[0] for a, b in zip(E, E[1:]))
        lb = sum(k * (h - k) + 1 for k in ks)
        assert F >= lb and 5 * h * len(ks) >= q * (2 * h - 3)
        assert 80 * lb > 3 * q * h * (2 * h - 3) and 3 * (2 * h - 3) >= 2 * h


if __name__ == '__main__':
    for h in range(2, 101, 2):
        check_square(block_square(2 * h))
    print('Proposition (i): semi-magic with complementary rows for all even h <= 100')
    for h in range(4, 61, 2):
        check_counting(h)
    print('Proposition (ii): counting checked for all even 4 <= h <= 60, 1 <= q < h')
    sys.path.insert(0, HERE)
    from make_figures import lower_bound_34
    out = {}
    for n in range(8, 201, 4):
        out[n] = lower_bound_subset(n)
        if n in (16, 20, 24, 28, 32, 40, 48, 60, 64, 80, 100, 120, 160, 200):
            F = F_sizes(n)
            print(n, 'K (|F_q| >= ceil(r_q/2)+1) =', lower_bound_34(n), '  K (all subset sums) =', out[n],
                  '  K/sqrt(n) = %.3f' % (out[n] / sqrt(n)) if out[n] else '',
                  '  sum log|F_q| / (n log n) = %.3f' % (sum(map(log, F)) / (n * log(n))))
    # the count |F_q| >= ceil(r_q/2)+1 for the squares of Lemma 3.12: smallest even / odd n with K >= 2, and n near 1000
    lb = {n: lower_bound_34(n) for n in range(5, 121)}
    first_even = min(n for n in lb if n % 2 == 0 and (lb[n] or 0) >= 2)
    first_odd = min(n for n in lb if n % 2 == 1 and (lb[n] or 0) >= 2)
    print('|F_q| >= ceil(r_q/2)+1: (11) first gives K >= 2 at n = %d (even n) and n = %d (odd n)' % (first_even, first_odd))
    print('  K at n = 14, 100:', lower_bound_34(14), lower_bound_34(100), '; at n = 999, 1000, 1001:',
          lower_bound_34(999), lower_bound_34(1000), lower_bound_34(1001))
    json.dump({str(k): v for k, v in out.items()}, open(os.path.join(HERE, 'kstar_subset_sums.json'), 'w'), indent=0)
