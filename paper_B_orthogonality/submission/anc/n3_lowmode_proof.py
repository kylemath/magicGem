"""Check of the proof of Lemma (n = 3: E_low = 0 implies magic), step by step,
against the enumeration of all 9! arrangements.

Centred entries z = s - 5 in {-4,...,4}; the cells are
    a b c
    d e f
    g h i.
Conditions (E_low = 0): column sums (t, -2t, t), row sums (u, -2u, u)
(the degree-1 conditions), both diagonal sums 0.

The proof shows: t + u = 3k, z_e = -2k, and with P = z_a - k, Q = z_c - k,
T = t - k, U = u - k (so T + U = k) the square is

    k+P      -T-P-Q   k+Q
    -U-P+Q   -2k      -U+P-Q
    k-Q      -T+P+Q   k-P

whence 4k^2 + 3(P^2+Q^2) + T^2 + U^2 = 30 (sum of squares = 60);
distinct corners force P, Q != 0 and |P| != |Q|, so P^2+Q^2 >= 5, and the
remaining arithmetic forces k = T = U = 0.

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
    print('E_low = 0          :', n_low, '(expect 8)')
    assert (n_deg1, n_diag, n_semi, n_low) == (760, 4224, 72, 8)

    # every arrangement with E_low = 0 is magic (all lines sum to 0)
    for z in low:
        cols, rows, dm, da = lines(z)
        assert set(cols) == {0} and set(rows) == {0}
    print('all 8 are magic: OK')

    # Step 1-2 (symbolic): parametrisation and the sum-of-squares identity.
    k, P, Q, T = sp.symbols('k P Q T', integer=True)
    U = k - T
    sq = [k + P, -T - P - Q, k + Q,
          -U - P + Q, -2 * k, -U + P - Q,
          k - Q, -T + P + Q, k - P]
    cols, rows, dm, da = lines(sq)
    t, u = T + k, U + k
    assert sp.simplify(cols[0] - t) == 0 and sp.simplify(cols[2] - t) == 0
    assert sp.simplify(cols[1] + 2 * t) == 0
    assert sp.simplify(rows[0] - u) == 0 and sp.simplify(rows[2] - u) == 0
    assert sp.simplify(rows[1] + 2 * u) == 0
    assert sp.simplify(dm) == 0 and sp.simplify(da) == 0
    assert sp.expand(sum(x ** 2 for x in sq)
                     - 2 * (4 * k ** 2 + 3 * (P ** 2 + Q ** 2) + T ** 2 + U ** 2)) == 0
    print('parametrisation satisfies the four conditions; sum of squares = '
          '2(4k^2+3(P^2+Q^2)+T^2+U^2): OK')

    # Step 1-2 (numeric): every arrangement satisfying the degree-1 conditions and
    # both diagonals (only the 8) has this form with integer k, P, Q, T.
    for z in low:
        cols, rows, _, _ = lines(z)
        tt, uu = cols[0], rows[0]
        assert (tt + uu) % 3 == 0
        kk = (tt + uu) // 3
        PP, QQ, TT = z[0] - kk, z[2] - kk, tt - kk
        UU = kk - TT
        rec = [kk + PP, -TT - PP - QQ, kk + QQ, -UU - PP + QQ, -2 * kk,
               -UU + PP - QQ, kk - QQ, -TT + PP + QQ, kk - PP]
        assert rec == z
        assert 4 * kk ** 2 + 3 * (PP ** 2 + QQ ** 2) + TT ** 2 + UU ** 2 == 30

    # Step 3 (arithmetic): integer solutions of 4k^2+3S+T^2+U^2 = 30 with T+U = k
    # and S = P^2+Q^2, P, Q != 0, |P| != |Q|: only k = T = U = 0, S = 10.
    sols = set()
    for kk, PP, QQ, TT in product(range(-3, 4), range(-9, 10), range(-9, 10), range(-9, 10)):
        UU = kk - TT
        if PP == 0 or QQ == 0 or abs(PP) == abs(QQ):
            continue
        if 4 * kk ** 2 + 3 * (PP ** 2 + QQ ** 2) + TT ** 2 + UU ** 2 == 30:
            sols.add((kk, TT, UU, PP ** 2 + QQ ** 2))
    print('integer solutions (k, T, U, P^2+Q^2):', sorted(sols))
    assert sols == {(0, 0, 0, 10)}

    # Without the distinctness of the corners there would be other solutions
    # (e.g. k = 2, P = 0), so that step is needed.
    extra = {(kk, TT) for kk, PP, QQ, TT in product(range(-3, 4), range(-9, 10),
                                                      range(-9, 10), range(-9, 10))
             if 4 * kk ** 2 + 3 * (PP ** 2 + QQ ** 2) + TT ** 2 + (kk - TT) ** 2 == 30}
    assert any(kk != 0 for kk, _ in extra)
    print('proof steps verified')


if __name__ == '__main__':
    main()
