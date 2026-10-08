"""
Exact theory for the energy of a uniformly random arrangement (uniform random
permutation of 1..N placed in the n x n grid).

Conventions:
  N = n^2,  x_ij = j-(n-1)/2,  y_ij = (n-1)/2-i,  z_ij = s_ij-(N+1)/2,
  Cov(phi,Z) = (1/N) sum_c (phi_c - mean phi) z_c.
  E_low  = Cov(X,Z)^2 + Cov(Y,Z)^2 + Cov(Dm,Z)^2 + Cov(Da,Z)^2
  E_full = sum_k Cov(R_k,Z)^2 + sum_l Cov(C_l,Z)^2 + Cov(Dm,Z)^2 + Cov(Da,Z)^2
           (symmetric: ALL n rows and ALL n columns, 2n+2 terms)

Everything here is exact rational arithmetic (fractions.Fraction).

Key facts used:
  * T_phi := Cov(phi,Z) = sum_c a_c z_{pi(c)},  a_c = (phi_c - mean phi)/N, is a linear
    permutation statistic.  E[T_phi] = 0 and (Hoeffding/Wald-Wolfowitz identity)
        Cov(T_phi, T_psi) = Var(Z) Cov_grid(phi,psi) / (N-1),
    where Cov_grid is the population covariance over the N cells and Var(Z) = (N^2-1)/12.
  * Fourth moments: E[prod_{i=1}^4 z_{pi(c_i)}] depends only on the equality pattern of
    (c_1..c_4); each pattern value is a polynomial in the power sums p2, p4 of z (p1=p3=0).
    Summing over cells with an *exact* pattern is done by Moebius inversion on the lattice
    of set partitions of {1,2,3,4} from the "at least as coarse" sums, which factor into
    mixed power sums of the a's.  This gives exact Var(E) for any list of test functions.
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import factorial
import numpy as np

# ----------------------------------------------------------------------------
# test functions on the grid (as exact Fractions, flattened row-major)
# ----------------------------------------------------------------------------

def grid_functions(n, which):
    """Return dict name -> list of N Fractions for the requested test functions.
    which in {'low','full'}"""
    N = n * n
    half = Fr(n - 1, 2)
    funcs = {}
    cells = [(i, j) for i in range(n) for j in range(n)]
    if which == 'low':
        funcs['X'] = [Fr(j) - half for i, j in cells]
        funcs['Y'] = [half - Fr(i) for i, j in cells]
        funcs['Dm'] = [Fr(int(i == j)) for i, j in cells]
        funcs['Da'] = [Fr(int(i + j == n - 1)) for i, j in cells]
    elif which == 'full':
        kmax = n
        for k in range(kmax):
            funcs[f'R{k}'] = [Fr(int(i == k)) for i, j in cells]
        for l in range(kmax):
            funcs[f'C{l}'] = [Fr(int(j == l)) for i, j in cells]
        funcs['Dm'] = [Fr(int(i == j)) for i, j in cells]
        funcs['Da'] = [Fr(int(i + j == n - 1)) for i, j in cells]
    else:
        raise ValueError(which)
    return funcs


def centered_coeffs(vals, N, scale=Fr(1)):
    """a_c = scale*(phi_c - mean phi)/N"""
    m = sum(vals) / N
    return [scale * (v - m) / N for v in vals]


def z_power_sums(N):
    """p2, p4 of z = s-(N+1)/2, s=1..N (p1 = p3 = 0 by symmetry)."""
    p2 = Fr(N * (N * N - 1), 12)
    p4 = Fr(N * (N * N - 1) * (3 * N * N - 7), 240)
    return p2, p4


def var_Z(N):
    return Fr(N * N - 1, 12)


# ----------------------------------------------------------------------------
# second moments: covariance matrix of the vector T = (Cov(phi_k, Z))_k
# ----------------------------------------------------------------------------

def gram_matrix(funcs, N):
    """Population covariance matrix over the grid, Cov_grid(phi_k, phi_l)."""
    names = list(funcs)
    m = {k: sum(funcs[k]) / N for k in names}
    G = [[sum((funcs[a][c] - m[a]) * (funcs[b][c] - m[b]) for c in range(N)) / N
          for b in names] for a in names]
    return names, G


def covariance_matrix_T(n, which):
    """Exact Sigma_T = Var(Z)/(N-1) * G  (Fractions)."""
    N = n * n
    funcs = grid_functions(n, which)
    names, G = gram_matrix(funcs, N)
    s2 = var_Z(N) / (N - 1)
    return names, [[s2 * g for g in row] for row in G]


def mean_energy(n, which):
    """E[E] = sum_k Var(T_k) = Var(Z)/(N-1) * trace(G)."""
    names, S = covariance_matrix_T(n, which)
    return sum(S[i][i] for i in range(len(names)))


def mean_energy_closed(n, which):
    """Closed forms (verified against mean_energy)."""
    N = n * n
    if which == 'low':
        return Fr(N + 1, 12) * (Fr(N - 1, 6) + Fr(2 * (n - 1), n * n))
    if which == 'full':
        return Fr(n ** 4 - 1, 6 * n * n)
    raise ValueError(which)


def weights_closed(n, which):
    """Eigenvalues of Sigma_T (weights of the limiting chi^2(1) mixture), closed form.
    Returns list of (weight: Fraction, multiplicity: int)."""
    N = n * n
    s2 = Fr(N + 1, 12)
    vD = Fr(n - 1, n * n)
    if n % 2 == 1:
        diag = [(s2 * vD, 2)]
    else:
        diag = [(s2 * Fr(1, n), 1), (s2 * Fr(n - 2, n * n), 1)]
    if which == 'low':
        return [(s2 * Fr(N - 1, 12), 2)] + diag
    if which == 'full':
        return [(s2 * Fr(1, n), 2 * (n - 1))] + diag
    raise ValueError(which)


def weights_numeric(n, which):
    """Eigenvalues of the exact Sigma_T computed numerically (any `which`)."""
    names, S = covariance_matrix_T(n, which)
    M = np.array([[float(x) for x in row] for row in S])
    ev = np.linalg.eigvalsh(M)
    return np.sort(ev)[::-1]


# ----------------------------------------------------------------------------
# exact variance of a sum of squared linear permutation statistics
# ----------------------------------------------------------------------------

def _set_partitions(elements):
    if not elements:
        yield []
        return
    first, rest = elements[0], elements[1:]
    for part in _set_partitions(rest):
        # put first in its own block
        yield [[first]] + part
        # or into an existing block
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]


_PARTS4 = [tuple(sorted(tuple(sorted(b)) for b in p)) for p in _set_partitions([0, 1, 2, 3])]


def _finer_or_equal(sigma, tau):
    """sigma <= tau in refinement order (every block of sigma inside a block of tau)."""
    return all(any(set(b).issubset(B) for B in tau) for b in sigma)


def _moebius(sigma, tau):
    """Moebius function of the partition lattice, sigma <= tau."""
    mu = 1
    for B in tau:
        m = sum(1 for b in sigma if set(b).issubset(B))
        mu *= (-1) ** (m - 1) * factorial(m - 1)
    return mu


def _pattern_moment(block_sizes, N, p2, p4):
    """E[prod z_{pi(c_i)}] for an exact equality pattern with given block sizes."""
    bs = tuple(sorted(block_sizes, reverse=True))
    ff = lambda b: Fr(np.prod([N - t for t in range(b)], dtype=object))  # falling factorial
    if bs == (4,):
        return p4 / ff(1)
    if bs == (3, 1):
        return -p4 / ff(2)
    if bs == (2, 2):
        return (p2 * p2 - p4) / ff(2)
    if bs == (2, 1, 1):
        return (2 * p4 - p2 * p2) / ff(3)
    if bs == (1, 1, 1, 1):
        return (3 * p2 * p2 - 6 * p4) / ff(4)
    raise ValueError(bs)


def second_moment_energy(n, which, funcs=None):
    """Exact E[E^2] for E = sum_k T_k^2, T_k = sum_c a_k(c) z_{pi(c)}."""
    N = n * n
    if funcs is None:
        funcs = grid_functions(n, which)
    names = list(funcs)
    A = {k: centered_coeffs(funcs[k], N) for k in names}
    p2, p4 = z_power_sums(N)
    # mixed power sums s[(k,l)][(alpha,beta)] = sum_c a_k^alpha a_l^beta
    # precompute per pair lazily
    moments = {sig: _pattern_moment([len(b) for b in sig], N, p2, p4) for sig in _PARTS4}
    coarser = {sig: [tau for tau in _PARTS4 if _finer_or_equal(sig, tau)] for sig in _PARTS4}
    mob = {(sig, tau): _moebius(sig, tau) for sig in _PARTS4 for tau in coarser[sig]}

    # For the sum over k,l we can group by the mixed power sums; do pairs directly.
    # Positions 0,1 carry a_k, positions 2,3 carry a_l.
    total = Fr(0)
    # cache of power sums
    pw = {}
    def mixed(k, l, al, be):
        key = (k, l, al, be)
        if key not in pw:
            ak, alv = A[k], A[l]
            pw[key] = sum((ak[c] ** al) * (alv[c] ** be) for c in range(N))
        return pw[key]

    def atleast(k, l, tau):
        val = Fr(1)
        for B in tau:
            al = sum(1 for i in B if i < 2)
            be = len(B) - al
            val *= mixed(k, l, al, be)
            if val == 0:
                return Fr(0)
        return val

    for k in names:
        for l in names:
            # exact(sigma) = sum_{tau >= sigma} mu(sigma,tau) atleast(tau)
            at = {tau: atleast(k, l, tau) for tau in _PARTS4}
            for sig in _PARTS4:
                ex = sum(mob[(sig, tau)] * at[tau] for tau in coarser[sig])
                total += moments[sig] * ex
    return total


def variance_energy(n, which):
    m1 = mean_energy(n, which)
    m2 = second_moment_energy(n, which)
    return m2 - m1 * m1


def gaussian_limit_variance(n, which):
    """2 * sum of squared weights (variance of the weighted chi^2 mixture)."""
    return 2 * sum(mult * w * w for w, mult in weights_closed(n, which))


# ----------------------------------------------------------------------------
# rational-function fitting in n (separately for odd and even n)
# ----------------------------------------------------------------------------

def fit_rational(values, denom_fn, deg):
    """Given dict n->Fraction, and known denominator denom_fn(n), interpolate numerator
    polynomial of degree deg on first deg+1 points, verify on the rest.  Returns sympy expr."""
    import sympy as sp
    nn = sp.symbols('n')
    ns = sorted(values)
    pts = [(k, values[k] * denom_fn(k)) for k in ns]
    use, check = pts[:deg + 1], pts[deg + 1:]
    poly = sp.interpolate([(sp.Integer(a), sp.Rational(b.numerator, b.denominator)) for a, b in use], nn)
    poly = sp.expand(poly)
    ok = all(poly.subs(nn, a) == sp.Rational(b.numerator, b.denominator) for a, b in check)
    return poly, ok


if __name__ == '__main__':
    import time
    t = time.time()
    for n in (3, 4, 5):
        for which in ('low', 'full'):
            print(n, which, mean_energy(n, which), mean_energy_closed(n, which),
                  float(variance_energy(n, which)), float(gaussian_limit_variance(n, which)))
    print('elapsed', time.time() - t)
