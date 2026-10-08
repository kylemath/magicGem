"""Check of the proof of Proposition 5.1 (n = 3: E_4 = 0 if and only if magic), step by step,
against the enumeration of all 9! arrangements.  Variable names follow the paper.

Centred entries z = s - 5 in {-4,...,4}; the cells are
    a b c
    d e f
    g h i.
Conditions (E_4 = 0): column sums gamma = (xi, -2xi, xi), row sums rho = (eta, -2eta, eta)
(the degree-1 conditions), both diagonal sums 0.

The proof shows: xi + eta = 3kappa, e = -2kappa, and with a' = a - kappa, c' = c - kappa,
xi' = xi - kappa, eta' = eta - kappa (so xi' + eta' = kappa) the square is

    kappa+a'        -xi'-a'-c'   kappa+c'
    -eta'-a'+c'     -2kappa      -eta'+a'-c'
    kappa-c'        -xi'+a'+c'   kappa-a'

whence 4kappa^2 + 3(a'^2+c'^2) + xi'^2 + eta'^2 = 30 (sum of squares = 60);
distinct corners force a', c' != 0 and |a'| != |c'|, so a'^2+c'^2 >= 5, and the
remaining arithmetic forces kappa = xi' = eta' = 0.

In the code: kap = kappa, ap = a', cp = c', xp = xi', ep = eta'.

Run: python3 n3_lowmode_proof.py   (about 10 s)
"""
from itertools import permutations, product
import sympy as sp


def lines(z):
    a, b, c, d, e, f, g, h, i = z
    cols = (a + d + g, b + e + h, c + f + i)
    rows = (a + b + c, d + e + f, g + h + i)
    return cols, rows, a + e + i, c + e + g


def main():
    n_deg1 = n_diag = n_low = n_semi = 0
    low = []
    for p in permutations(range(1, 10)):
        z = [v - 5 for v in p]
        cols, rows, dm, da = lines(z)
        deg1 = cols[0] == cols[2] and rows[0] == rows[2]   # sum x z = sum y z = 0
        diag = dm == 0 and da == 0
        n_deg1 += deg1
        n_diag += diag
        n_semi += set(cols) == {0} and set(rows) == {0}   # degree-2 conditions
        if deg1 and diag:
            n_low += 1
            low.append(z)
    print('degree-1 conditions:', n_deg1, '(expect 760)')
    print('both diagonals     :', n_diag, '(expect 4224)')
    print('degree-2 (semi-magic):', n_semi, '(expect 72)')
    print('E_4 = 0            :', n_low, '(expect 8)')
    assert (n_deg1, n_diag, n_semi, n_low) == (760, 4224, 72, 8)

    # every arrangement with E_4 = 0 is magic (all lines sum to 0)
    for z in low:
        cols, rows, dm, da = lines(z)
        assert set(cols) == {0} and set(rows) == {0}
    print('all 8 are magic: OK')

    # Step 1-2 (symbolic): parametrisation and the sum-of-squares identity.
    kap, ap, cp, xp = sp.symbols('kappa ap cp xp', integer=True)
    ep = kap - xp
    sq = [kap + ap, -xp - ap - cp, kap + cp,
          -ep - ap + cp, -2 * kap, -ep + ap - cp,
          kap - cp, -xp + ap + cp, kap - ap]
    cols, rows, dm, da = lines(sq)
    xi, eta = xp + kap, ep + kap
    assert sp.simplify(cols[0] - xi) == 0 and sp.simplify(cols[2] - xi) == 0
    assert sp.simplify(cols[1] + 2 * xi) == 0
    assert sp.simplify(rows[0] - eta) == 0 and sp.simplify(rows[2] - eta) == 0
    assert sp.simplify(rows[1] + 2 * eta) == 0
    assert sp.simplify(dm) == 0 and sp.simplify(da) == 0
    assert sp.expand(sum(x ** 2 for x in sq)
                     - 2 * (4 * kap ** 2 + 3 * (ap ** 2 + cp ** 2) + xp ** 2 + ep ** 2)) == 0
    print('parametrisation satisfies the four conditions; sum of squares = '
          '2(4kappa^2+3(a\'^2+c\'^2)+xi\'^2+eta\'^2): OK')

    # Step 1-2 (numeric): every arrangement satisfying the degree-1 conditions and
    # both diagonals (only the 8) has this form with integer kappa, a', c', xi'.
    for z in low:
        cols, rows, _, _ = lines(z)
        xi_, eta_ = cols[0], rows[0]
        assert (xi_ + eta_) % 3 == 0
        kk = (xi_ + eta_) // 3
        A, C, X = z[0] - kk, z[2] - kk, xi_ - kk
        E = kk - X
        rec = [kk + A, -X - A - C, kk + C, -E - A + C, -2 * kk,
               -E + A - C, kk - C, -X + A + C, kk - A]
        assert rec == z
        assert 4 * kk ** 2 + 3 * (A ** 2 + C ** 2) + X ** 2 + E ** 2 == 30

    # Step 3 (arithmetic): integer solutions of 4kappa^2+3S+xi'^2+eta'^2 = 30 with xi'+eta' = kappa
    # and S = a'^2+c'^2, a', c' != 0, |a'| != |c'|: only kappa = xi' = eta' = 0, S = 10.
    sols = set()
    for kk, A, C, X in product(range(-3, 4), range(-9, 10), range(-9, 10), range(-9, 10)):
        E = kk - X
        if A == 0 or C == 0 or abs(A) == abs(C):
            continue
        if 4 * kk ** 2 + 3 * (A ** 2 + C ** 2) + X ** 2 + E ** 2 == 30:
            sols.add((kk, X, E, A ** 2 + C ** 2))
    print("integer solutions (kappa, xi', eta', a'^2+c'^2):", sorted(sols))
    assert sols == {(0, 0, 0, 10)}

    # Without the distinctness of the corners there would be other solutions
    # (e.g. kappa = 2, a' = 0), so that step is needed.
    extra = {(kk, X) for kk, A, C, X in product(range(-3, 4), range(-9, 10),
                                                 range(-9, 10), range(-9, 10))
             if 4 * kk ** 2 + 3 * (A ** 2 + C ** 2) + X ** 2 + (kk - X) ** 2 == 30}
    assert any(kk != 0 for kk, _ in extra)
    print('proof steps verified')


if __name__ == '__main__':
    main()
