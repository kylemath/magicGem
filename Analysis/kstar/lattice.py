"""Lattice Lambda_{n,k} = { gamma in Z^n : (t-1)^{k+1} | sum_j gamma_j t^j }  (rank r = n-k-1).

Basis: shifts t^i (t-1)^{k+1}, i=0..r-1.  We LLL-reduce (exact, sympy) and then run an exact
Schnorr-Euchner enumeration (Fraction arithmetic for Gram-Schmidt) of all lattice vectors with
||gamma||_2^2 <= R2, keeping track of the minimum sup-norm.  If R2 = n*B^2 the enumeration is a proof
that no nonzero vector with ||gamma||_inf <= B exists (any such vector has ||gamma||_2^2 <= n B^2).
"""
from fractions import Fraction
from math import comb, isqrt
from sympy.polys.matrices import DomainMatrix
from sympy import ZZ


def basis(n, k):
    K = k + 1
    c = [(-1) ** (K - l) * comb(K, l) for l in range(K + 1)]
    r = n - K
    B = []
    for i in range(r):
        v = [0] * n
        for l, cl in enumerate(c):
            v[i + l] = cl
        B.append(v)
    return B


def lll(B):
    if len(B) <= 1:
        return [list(b) for b in B]
    M = DomainMatrix([[ZZ(x) for x in row] for row in B], (len(B), len(B[0])), ZZ)
    R = M.lll()
    return [[int(x) for x in row] for row in R.to_Matrix().tolist()]


def gso(B):
    """exact Gram-Schmidt: returns mu (lower-tri Fractions) and bstar norms^2 (Fractions)"""
    r = len(B)
    dot = lambda u, v: sum(a * b for a, b in zip(u, v))
    Bs = []
    mu = [[Fraction(0)] * r for _ in range(r)]
    nn = []
    for i in range(r):
        v = [Fraction(x) for x in B[i]]
        for j in range(i):
            mu[i][j] = Fraction(dot(B[i], Bs[j])) / nn[j] if nn[j] else Fraction(0)
            v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
        Bs.append(v)
        nn.append(dot(v, v))
    return mu, nn


def enumerate_short(B, R2, callback, limit=None):
    """Enumerate all nonzero integer combinations x with ||sum x_i B_i||^2 <= R2 (exact), up to sign.
    callback(x, vec) -> may return True to stop.  Returns number of vectors visited."""
    r = len(B)
    mu, nn = gso(B)
    R2 = Fraction(R2)
    x = [0] * r
    count = [0]
    n = len(B[0])

    def rec(i, partial):
        # partial: sum_{j>i} contribution  = squared length of projection orthogonal to b_0..b_i  (levels > i)
        # centre c_i = - sum_{j>i} x_j mu[j][i]
        ci = -sum(x[j] * mu[j][i] for j in range(i + 1, r))
        rem = R2 - partial
        if rem < 0:
            return False
        # |x_i - ci|^2 nn[i] <= rem
        if nn[i] == 0:
            return False
        rad2 = rem / nn[i]
        # integer range
        lo = ci - Fraction(isqrt(int(rad2) + 1) + 1)
        from math import floor, ceil
        xs = []
        a = floor(ci) - (isqrt(int(rad2) + 1) + 1)
        b = ceil(ci) + (isqrt(int(rad2) + 1) + 1)
        for xi in range(a, b + 1):
            d = (xi - ci)
            if d * d * nn[i] <= rem:
                xs.append(xi)
        for xi in xs:
            x[i] = xi
            newp = partial + (xi - ci) ** 2 * nn[i]
            if i == 0:
                if any(x):
                    # sign normalisation: first nonzero from the top positive
                    top = next(t for t in range(r - 1, -1, -1) if x[t])
                    if x[top] > 0:
                        vec = [sum(x[t] * B[t][j] for t in range(r)) for j in range(n)]
                        count[0] += 1
                        if callback(list(x), vec):
                            return True
                        if limit and count[0] > limit:
                            raise RuntimeError("limit")
            else:
                if rec(i - 1, newp):
                    return True
        x[i] = 0
        return False

    rec(r - 1, Fraction(0))
    return count[0]


def min_supnorm(n, k, bound):
    """Return (minimum sup-norm among nonzero vectors with sup-norm <= bound, witness) or (None, None)
    if there is none.  Exact."""
    B = lll(basis(n, k))
    best = [None, None]

    def cb(x, vec):
        s = max(abs(v) for v in vec)
        if s <= bound and (best[0] is None or s < best[0]):
            best[0], best[1] = s, vec
        return False

    cnt = enumerate_short(B, n * bound * bound, cb)
    return best[0], best[1], cnt


def lll_best_sup(n, k):
    B = lll(basis(n, k))
    return min(max(abs(v) for v in b) for b in B), B
