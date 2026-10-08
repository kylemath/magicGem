"""Explicit semi-magic squares with many "twin" row pairs (complementary on a set of columns).

Twin row pair (i,i') on column set J: s[i][j] + s[i'][j] = N+1 for all j in J.
For two columns j,j' in J, swapping s[i][j]<->s[i][j'] changes (gamma_j,gamma_j') by (+d,-d),
swapping in row i' changes them by (-d,+d), where d = s[i][j'] - s[i][j]; all row sums unchanged.

Constructions (all exact integer arithmetic, verified by verify()):
  even_paired(n): n = 2m, every row pair (r, m+r) complementary on ALL columns.
                  m even: dominoes; m odd >= 7: dominoes + one 6-element gadget per row.
  odd_concentric(n): n odd >= 7: concentric bordered square around a 7x7 (Siamese) core,
                  borders of every odd order 9..n by the explicit rule border_odd();
                  layer l (rows l, n-1-l) is a twin pair on columns l+1..n-2-l.
"""
import itertools


def siamese(n):
    """de la Loubere magic square of odd order n, values 1..n^2."""
    s = [[0] * n for _ in range(n)]
    i, j = 0, n // 2
    for v in range(1, n * n + 1):
        s[i][j] = v
        ni, nj = (i - 1) % n, (j + 1) % n
        if s[ni][nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return s


# ---------------------------------------------------------------- even n
def even_paired(n):
    assert n % 2 == 0
    m = n // 2
    N = n * n
    # weights: odd numbers 1,3,...,N-1  (w = |2v-(N+1)|); index of weight w is (w-1)//2, 0..2m^2-1
    idx_rows = [[] for _ in range(m)]   # list of (index, sign) per row
    if m % 2 == 0:
        # dominoes {2t, 2t+1} (indices), t=0..m^2-1; row r gets m of them, half (+,-), half (-,+)
        doms = [(2 * t, 2 * t + 1) for t in range(m * m)]
        for r in range(m):
            for k in range(m):
                a, b = doms[r * m + k]
                sg = 1 if k % 2 == 0 else -1
                idx_rows[r] += [(a, sg), (b, -sg)]
    else:
        assert m >= 7, "n = 2 mod 4 handled for n >= 14 only"
        used = set()
        # quadruple Q_r = indices 4r..4r+3 (weights a,a+2,a+4,a+6 with a = 8r+1), signs + + + -  -> sum 2a
        for r in range(m):
            q = [4 * r, 4 * r + 1, 4 * r + 2, 4 * r + 3]
            idx_rows[r] += [(q[0], 1), (q[1], 1), (q[2], 1), (q[3], -1)]
            used.update(q)
        # nested pairs: alpha_{m-1} = 4m, beta_r = alpha_r + 8r + 1, alpha_{r-1} = alpha_r + 1
        alpha = {m - 1: 4 * m}
        for r in range(m - 1, 0, -1):
            alpha[r - 1] = alpha[r] + 1
        for r in range(m):
            a, b = alpha[r], alpha[r] + 8 * r + 1
            # weights w(a) = 2a+1, w(b) = 2b+1, w(b)-w(a) = 16r+2 = 2*(8r+1) = 2a_r ; signs: +w(a) - w(b) = -2a_r
            idx_rows[r] += [(a, 1), (b, -1)]
            used.update([a, b])
        assert max(used) <= 2 * m * m - 1
        rest = [x for x in range(2 * m * m) if x not in used]
        # rest splits into consecutive dominoes
        doms = []
        k = 0
        while k < len(rest):
            assert rest[k + 1] == rest[k] + 1, (n, rest[k], rest[k + 1])
            doms.append((rest[k], rest[k + 1]))
            k += 2
        assert len(doms) == m * (m - 3)
        for r in range(m):
            for k in range(m - 3):
                a, b = doms[r * (m - 3) + k]
                sg = 1 if k % 2 == 0 else -1
                idx_rows[r] += [(a, sg), (b, -sg)]
    s = [[0] * n for _ in range(n)]
    for r in range(m):
        row = idx_rows[r]
        assert len(row) == n
        for j, (ix, sg) in enumerate(row):
            w = 2 * ix + 1
            v = (N + 1 + sg * w) // 2
            s[r][j] = v
            s[m + r][j] = N + 1 - v
    twins = [((r, m + r), list(range(n))) for r in range(m)]
    return s, twins


# ---------------------------------------------------------------- odd n
def ksubset_with_sum(I, k, target):
    """k-subset of the sorted integer interval I (list of consecutive ints) with given sum, or None."""
    I = sorted(I)
    lo = sum(I[:k]); hi = sum(I[-k:])
    if not (lo <= target <= hi):
        return None
    # start from the k smallest; push the largest movable element up one step at a time (standard argument)
    sel = list(range(k))           # positions in I
    cur = lo
    L = len(I)
    while cur < target:
        # move highest element that can move by one
        for t in range(k - 1, -1, -1):
            limit = L - (k - t)
            if sel[t] < limit and (t == k - 1 or sel[t] + 1 < sel[t + 1]):
                sel[t] += 1
                cur += 1
                break
    return [I[p] for p in sel]


def border_odd(n):
    """Border data for odd order n = 2m+1, m >= 4.  Returns dict with corner values and inner top/left values
    (values in 1..n^2; bottom/right are complements)."""
    m = (n - 1) // 2
    assert m >= 4
    N = n * n
    c = (N + 1) // 2
    A, B = 4 * m, 4 * m - 2
    P = [p for p in range(2 * m, 4 * m + 1) if p not in (A, B)]     # positives (big values)
    Q = list(range(1, 2 * m))                                       # negatives (small values)
    assert len(P) == 2 * m - 1 and len(Q) == 2 * m - 1
    targetT = c - A + B
    I = [p for p in P if p <= 4 * m - 3]   # interval [2m, 4m-3]
    # choose T_neg (m-1 subset of Q) and T_pos (m subset of I) with sum(T_pos)-sum(T_neg) = targetT
    sol = None
    qlo = sum(Q[:m - 1]); qhi = sum(Q[-(m - 1):])
    for sneg in range(qlo, qhi + 1):
        tp = ksubset_with_sum(I, m, targetT + sneg)
        if tp is not None:
            tn = ksubset_with_sum(Q, m - 1, sneg)
            sol = (tp, tn)
            break
    assert sol is not None
    Tpos, Tneg = sol
    Lpos = [p for p in P if p not in Tpos]
    Lneg = [p for p in Q if p not in Tneg]
    big = lambda p: N + 1 - p
    top_inner = [big(p) for p in Tpos] + list(Tneg)
    left_inner = [big(p) for p in Lpos] + list(Lneg)
    return dict(tl=big(A), tr=B, top=top_inner, left=left_inner)


def bordered(inner, n, bd):
    """Place a semi-magic square `inner` of order n-2 (values 1..(n-2)^2) inside the border bd."""
    N = n * n
    sh = 2 * n - 2
    s = [[0] * n for _ in range(n)]
    for i in range(n - 2):
        for j in range(n - 2):
            s[i + 1][j + 1] = inner[i][j] + sh
    s[0][0] = bd['tl']; s[n - 1][n - 1] = N + 1 - bd['tl']
    s[0][n - 1] = bd['tr']; s[n - 1][0] = N + 1 - bd['tr']
    for j, v in enumerate(bd['top']):
        s[0][j + 1] = v; s[n - 1][j + 1] = N + 1 - v
    for i, v in enumerate(bd['left']):
        s[i + 1][0] = v; s[i + 1][n - 1] = N + 1 - v
    return s


def odd_concentric(n):
    assert n % 2 == 1 and n >= 7
    s = siamese(7)
    twins = []   # in coordinates of the current square
    cur = 7
    while cur < n:
        cur += 2
        bd = border_odd(cur)
        s = bordered(s, cur, bd)
        twins = [((a + 1, b + 1), [j + 1 for j in cols]) for (a, b), cols in twins]
        twins.append(((0, cur - 1), list(range(1, cur - 1))))
    return s, twins


def construct(n):
    if n % 2 == 0:
        return even_paired(n)
    return odd_concentric(n)


def verify(s, twins):
    n = len(s); N = n * n; M = n * (N + 1) // 2
    vals = sorted(v for row in s for v in row)
    assert vals == list(range(1, N + 1)), "not a permutation"
    assert all(sum(row) == M for row in s), "row sum"
    assert all(sum(s[i][j] for i in range(n)) == M for j in range(n)), "col sum"
    for (i, ip), cols in twins:
        for j in cols:
            assert s[i][j] + s[ip][j] == N + 1, ("twin", i, ip, j)
    return True


if __name__ == "__main__":
    import sys
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    for n in range(7, hi + 1):
        if n % 4 == 2 and n < 14:
            continue
        s, tw = construct(n)
        verify(s, tw)
    print("verified all constructions for 7<=n<=%d (n=10 excluded)" % hi)
