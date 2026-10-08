"""Exact Var(E_low), Var(E_full) as rational functions of n (separately for odd / even n),
obtained by exact evaluation for many n (Moebius-inversion formula of theory.py) followed by
polynomial interpolation with verification on held-out orders.
Run: python3.9 fit_variance.py  -> variance_fits.json"""
import json, os, time
from fractions import Fraction as Fr
import sympy as sp
from theory import (_PARTS4, _finer_or_equal, _moebius, _pattern_moment, z_power_sums,
                    grid_functions, centered_coeffs, mean_energy_closed, variance_energy)

_COARSER = {sig: [tau for tau in _PARTS4 if _finer_or_equal(sig, tau)] for sig in _PARTS4}
_MOB = {(sig, tau): _moebius(sig, tau) for sig in _PARTS4 for tau in _COARSER[sig]}


def pair_second_moment(mixed, N, moments):
    """E[T_k^2 T_l^2] given mixed(alpha,beta) = sum_c a_k^alpha a_l^beta."""
    cache = {}
    def mx(al, be):
        if (al, be) not in cache:
            cache[(al, be)] = mixed(al, be)
        return cache[(al, be)]
    at = {}
    for tau in _PARTS4:
        val = Fr(1)
        for B in tau:
            al = sum(1 for i in B if i < 2)
            val *= mx(al, len(B) - al)
            if val == 0:
                break
        at[tau] = val
    tot = Fr(0)
    for sig in _PARTS4:
        tot += moments[sig] * sum(_MOB[(sig, tau)] * at[tau] for tau in _COARSER[sig])
    return tot


def moments_table(N):
    p2, p4 = z_power_sums(N)
    return {sig: _pattern_moment([len(b) for b in sig], N, p2, p4) for sig in _PARTS4}


def second_moment_low(n):
    N = n * n
    funcs = grid_functions(n, 'low')
    A = {k: centered_coeffs(v, N) for k, v in funcs.items()}
    mom = moments_table(N)
    tot = Fr(0)
    for k in A:
        for l in A:
            ak, al_ = A[k], A[l]
            mixed = lambda al, be: sum(ak[c] ** al * al_[c] ** be for c in range(N))
            tot += pair_second_moment(mixed, N, mom)
    return tot


def second_moment_full(n):
    """Pair types for the 2n+2 line indicators (|line|=n, mean 1/n), by intersection size m."""
    N = n * n
    p = Fr(1, n)
    mom = moments_table(N)
    def mixed_for(m):
        def mixed(al, be):
            # cells: in both (m), only k (n-m), only l (n-m), neither (N-2n+m)
            v = (m * (1 - p) ** al * (1 - p) ** be + (n - m) * (1 - p) ** al * (-p) ** be
                 + (n - m) * (-p) ** al * (1 - p) ** be + (N - 2 * n + m) * (-p) ** al * (-p) ** be)
            return v / Fr(N) ** (al + be)
        return mixed
    types = [  # (multiplicity of ordered pairs, intersection size)
        (2 * n + 2, n),            # same line
        (2 * n * (n - 1), 0),      # two distinct rows or two distinct cols
        (2 * n * n + 8 * n, 1),    # row-col, row-diag, col-diag (either order)
        (2, n % 2),                # main-anti diagonal pair
    ]
    assert sum(t[0] for t in types) == (2 * n + 2) ** 2
    return sum(mult * pair_second_moment(mixed_for(m), N, mom) for mult, m in types)


def exact_var(n, which):
    m1 = mean_energy_closed(n, which)
    m2 = second_moment_low(n) if which == 'low' else second_moment_full(n)
    return m2 - m1 * m1


def fit(values, max_deg=24):
    """values: dict n -> Fraction (single parity).  Find rational function P(n)/Q(n) with
    Q = n^7 (the falling-factorial denominators cancel exactly) by interpolation; verify on held-out points; simplify."""
    nn = sp.symbols('n')
    Q = nn ** 7
    ns = sorted(values)
    pts = [(sp.Integer(k), sp.Rational(values[k].numerator, values[k].denominator) * Q.subs(nn, k)) for k in ns]
    for deg in range(4, max_deg + 1):
        if deg + 1 + 3 > len(pts):
            break
        poly = sp.expand(sp.interpolate(pts[:deg + 1], nn))
        if all(poly.subs(nn, a) == b for a, b in pts[deg + 1:]):
            expr = sp.factor(sp.cancel(poly / Q))
            return expr, deg, len(pts) - deg - 1
    raise RuntimeError('no polynomial fit found')


def leading(expr):
    nn = sp.symbols('n')
    num, den = sp.fraction(sp.cancel(expr))
    return sp.Poly(num, nn).degree() - sp.Poly(den, nn).degree(), sp.LC(sp.Poly(num, nn)) / sp.LC(sp.Poly(den, nn))


if __name__ == '__main__':
    t0 = time.time()
    nn = sp.symbols('n')
    out = {}
    # consistency with the slow generic routine
    for n in (3, 4, 5, 6):
        for w in ('low', 'full'):
            assert exact_var(n, w) == variance_energy(n, w), (n, w)
    print('fast routines agree with generic routine for n=3..6')
    for which in ('low', 'full'):
        vals = {n: exact_var(n, which) for n in range(3, 46)}
        print(which, 'values computed', time.time() - t0)
        res = {}
        for parity, name in ((1, 'odd'), (0, 'even')):
            sub = {n: v for n, v in vals.items() if n % 2 == parity}
            expr, deg, nver = fit(sub)
            d, c = leading(expr)
            res[name] = {'expr': str(expr), 'latex': sp.latex(expr), 'numerator_degree_fitted': deg,
                         'verified_on_extra_points': nver, 'leading_order': str(d), 'leading_coeff': str(c),
                         'values': {str(n): str(v) for n, v in sub.items() if n <= 12}}
            print(which, name, expr, 'lead', d, c, 'verified on', nver)
        out[which] = res
    out['runtime_s'] = time.time() - t0
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, 'variance_fits.json'), 'w'), indent=1)
    print('done', time.time() - t0)
