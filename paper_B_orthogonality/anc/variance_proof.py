"""Symbolic (non-interpolated) derivation of Var(E_low), Var(E_full) for a uniformly random
arrangement of 1..N on the n x n grid, N = n^2.  See variance_proof.md.

Steps
 1. General identity: for z a uniformly random permutation of a fixed vector v with sum 0 and
    a symmetric matrix A with zero row sums,
        E[(z^T A z)^2] = c22 * ((tr A)^2 + 2 tr(A^2)) + c4 * sum_a A_aa^2,
    with c22, c4 explicit in N, p2, p4 (p3 is allowed but drops out only if p1=0; we keep it).
    Derived here by Moebius inversion over the 15 set partitions of {1,2,3,4}.
 2. Invariants tr A, tr A^2, sum_a A_aa^2 of the two energies as polynomials in n
    (separately for n odd / even), derived in closed form from cell counts.
 3. Var(E) = E[E^2] - (E E)^2, simplified; compared with the closed forms stated in the paper (variance_fits.json).
 4. Independent checks: (i) identity of step 1 by full enumeration of all permutations for random
    integer A, v with N<=7; (ii) invariants of step 2 against explicit matrices for n=3..25;
    (iii) n=3 exhaustive 9! enumeration; (iv) the closed forms in variance_fits.json.
"""
import itertools, json, os, random, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy.utilities.iterables import multiset_partitions

N, p2, p3, p4, n = sp.symbols('N p2 p3 p4 n', positive=True)
P = {1: 0, 2: p2, 3: p3, 4: p4}           # power sums of v; p1 = 0 (centred)

# ---------------------------------------------------------------- step 1
def setparts(elems):
    return [tuple(tuple(b) for b in q) for q in multiset_partitions(list(elems))]

PARTS4 = setparts([0, 1, 2, 3])
assert len(PARTS4) == 15

def refines(pi, sigma):          # pi <= sigma : every block of pi inside a block of sigma
    return all(any(set(b) <= set(c) for c in sigma) for b in pi)

def mobius(pi, sigma):           # mu(pi, sigma) in the partition lattice
    # interval [pi,sigma] ~ product over blocks C of sigma of Pi_{k_C}, k_C = #blocks of pi in C
    r = 1
    for c in sigma:
        k = sum(1 for b in pi if set(b) <= set(c))
        r *= (-1) ** (k - 1) * sp.factorial(k - 1)
    return r

def falling(x, k):
    r = 1
    for i in range(k):
        r *= (x - i)
    return r

def M_distinct(lams):
    """sum over distinct indices i_1..i_k of prod v_{i_j}^{lam_j}, via Moebius from power sums."""
    k = len(lams)
    tot = 0
    for tau in setparts(range(k)):
        coef = 1
        for b in tau:
            coef *= (-1) ** (len(b) - 1) * sp.factorial(len(b) - 1)
        term = 1
        for b in tau:
            term *= P[sum(lams[j] for j in b)]
        tot += coef * term
    return sp.expand(tot)

def moment(pi):
    """E[z_a z_b z_c z_d] for indices with equality pattern exactly pi."""
    lams = [len(b) for b in pi]
    return M_distinct(lams) / falling(N, len(lams))

def c_sigma(sigma):
    return sp.simplify(sum(mobius(pi, sigma) * moment(pi) for pi in PARTS4 if refines(pi, sigma)))

C = {s: c_sigma(s) for s in PARTS4}
s12_34 = ((0, 1), (2, 3)); s13_24 = ((0, 2), (1, 3)); s14_23 = ((0, 3), (1, 2)); s1234 = ((0, 1, 2, 3),)
def key(s):
    return tuple(sorted(tuple(sorted(b)) for b in s))
Ck = {key(s): v for s, v in C.items()}
c22 = sp.factor(Ck[key(s12_34)]); assert sp.simplify(c22 - Ck[key(s13_24)]) == 0 and sp.simplify(c22 - Ck[key(s14_23)]) == 0
c4 = sp.factor(Ck[key(s1234)])

# second moment E[z_a z_b]
m2_eq = p2 / N; m2_ne = -p2 / (N * (N - 1))

def E2_general(trA, trA2, d2):
    return c22 * (trA ** 2 + 2 * trA2) + c4 * d2

def EE_general(trA):
    return p2 / (N - 1) * trA

# ---------------------------------------------------------------- check of step 1 by enumeration
def brute_check(Nn, trials=3, seed=1):
    rng = random.Random(seed)
    for _ in range(trials):
        v = [rng.randint(-5, 5) for _ in range(Nn)]
        s = sum(v); v = [Fr(x * Nn - s) for x in v]          # centre (scaled)
        B = [[rng.randint(-4, 4) for _ in range(Nn)] for _ in range(Nn)]
        B = [[B[i][j] + B[j][i] for j in range(Nn)] for i in range(Nn)]
        # double-centre so rows sum to zero
        rm = [Fr(sum(r), Nn) for r in B]; tm = Fr(sum(rm), Nn)
        A = [[B[i][j] - rm[i] - rm[j] + tm for j in range(Nn)] for i in range(Nn)]
        tot2 = Fr(0); tot1 = Fr(0); cnt = 0
        for perm in itertools.permutations(v):
            q = sum(A[i][j] * perm[i] * perm[j] for i in range(Nn) for j in range(Nn))
            tot1 += q; tot2 += q * q; cnt += 1
        trA = sum(A[i][i] for i in range(Nn))
        trA2 = sum(A[i][j] ** 2 for i in range(Nn) for j in range(Nn))
        d2 = sum(A[i][i] ** 2 for i in range(Nn))
        sub = {N: Nn, p2: sum(x ** 2 for x in v), p3: sum(x ** 3 for x in v), p4: sum(x ** 4 for x in v)}
        sub = {k: sp.Rational(val) if not isinstance(val, Fr) else sp.Rational(val.numerator, val.denominator) for k, val in sub.items()}
        pred2 = E2_general(sp.Rational(trA.numerator, trA.denominator), sp.Rational(trA2.numerator, trA2.denominator),
                           sp.Rational(d2.numerator, d2.denominator)).subs(sub)
        pred1 = EE_general(sp.Rational(trA.numerator, trA.denominator)).subs(sub)
        got2 = sp.Rational((tot2 / cnt).numerator, (tot2 / cnt).denominator)
        got1 = sp.Rational((tot1 / cnt).numerator, (tot1 / cnt).denominator)
        assert sp.simplify(pred2 - got2) == 0, (Nn, pred2, got2)
        assert sp.simplify(pred1 - got1) == 0
    return True

# ---------------------------------------------------------------- step 2: invariants
# values 1..N centred:
P2 = N * (N ** 2 - 1) / 12
P4 = N * (N ** 2 - 1) * (3 * N ** 2 - 7) / 240
P3 = 0

def invariants(which, parity):
    """tr A, tr A^2 (= ||A||_F^2), sum_c A_cc^2 as rational functions of n; parity in {'odd','even'}.
    A = sum_k a_k a_k^T, a_k = (phi_k - mean)/N.  e = [n odd] = #cells on both diagonals."""
    e = 1 if parity == 'odd' else 0
    NN = n ** 2
    # power sums of the centred coordinate x over the n x n grid
    Sx2 = n * (n ** 2 - 1) / 12                       # sum over j of x_j^2 (one row of n values)
    Sx4 = n * (n ** 2 - 1) * (3 * n ** 2 - 7) / 240
    # line indicator centred: u = 1 - 1/n on the line, -1/n off it
    if which == 'low':
        # Gram G (population covariances): Var X = Var Y = (n^2-1)/12, Var D = (n-1)/n^2,
        # Cov(Dm, Da) = e/N - 1/n^2 ; all others 0.  a_k.a_l = G_kl / N.
        vX = (n ** 2 - 1) / 12; vD = (n - 1) / n ** 2; cDD = sp.Rational(e) / NN - 1 / n ** 2
        trA = (2 * vX + 2 * vD) / NN
        trA2 = (2 * vX ** 2 + 2 * vD ** 2 + 2 * cDD ** 2) / NN ** 2
        # d2 = N^-4 sum_c h_c^2, h_c = x_c^2 + y_c^2 + u_m(c)^2 + u_a(c)^2
        # u^2 = 1/n^2 + (1-2/n) * 1_D.  Write h = x^2 + y^2 + 2/n^2 + (1-2/n)(dm+da).
        al = 2 / n ** 2; be = 1 - 2 / n
        # needed cell sums
        s_x4 = n * Sx4                          # sum_c x_c^4 (each x value appears n times)
        s_x2y2 = Sx2 ** 2                       # sum_c x^2 y^2
        s_x2 = n * Sx2                          # sum_c x^2
        s_x2_dm = Sx2                           # sum over main diagonal of x^2 (x runs over all n values once)
        # (x^2+y^2)^2 summed:
        S_q2 = 2 * s_x4 + 2 * s_x2y2
        S_q = 2 * s_x2
        S_q_D = 2 * 2 * s_x2_dm                 # sum_c (x^2+y^2)(dm+da): each diagonal gives 2*Sx2
        S_D = 2 * n                             # sum_c (dm+da)
        S_D2 = 2 * n + 2 * e                    # sum_c (dm+da)^2 = n + n + 2*[centre]
        S_h2 = S_q2 + al ** 2 * NN + be ** 2 * S_D2 + 2 * al * S_q + 2 * be * S_q_D + 2 * al * be * S_D
        d2 = S_h2 / NN ** 4
    else:
        L = 2 * n + 2
        vL = (n - 1) / n ** 2
        cDD = sp.Rational(e) / NN - 1 / n ** 2
        trA = L * vL / NN
        # Gram: rows block (1/n)(I - J/n): diag vL, off-diag -1/n^2 (n(n-1) ordered pairs), same cols;
        # row-col, row-diag, col-diag covariances 0; diag-diag cDD.
        sumG2 = L * vL ** 2 + 2 * n * (n - 1) * (1 / n ** 2) ** 2 + 2 * cDD ** 2
        trA2 = sumG2 / NN ** 2
        # h_c = sum_L u_L(c)^2 = (2n+2)/n^2 + (1-2/n) * (#lines through c),  #lines = 2 + dm + da
        al = L / n ** 2 + 2 * (1 - 2 / n); be = 1 - 2 / n
        S_D = 2 * n; S_D2 = 2 * n + 2 * e
        S_h2 = al ** 2 * NN + 2 * al * be * S_D + be ** 2 * S_D2
        d2 = S_h2 / NN ** 4
    return sp.simplify(trA), sp.simplify(trA2), sp.simplify(d2)

def variance(which, parity):
    trA, trA2, d2 = invariants(which, parity)
    sub = {p2: P2, p3: P3, p4: P4}
    E2 = E2_general(trA, trA2, d2).subs(sub).subs(N, n ** 2)
    E1 = EE_general(trA).subs(sub).subs(N, n ** 2)
    return sp.factor(sp.simplify(E2 - E1 ** 2)), sp.factor(sp.simplify(E1))

# ---------------------------------------------------------------- explicit-matrix checks
def test_functions(n_, which):
    cells = [(i, j) for i in range(n_) for j in range(n_)]
    h = Fr(n_ - 1, 2)
    fs = []
    dm = [1 if i == j else 0 for (i, j) in cells]
    da = [1 if i + j == n_ - 1 else 0 for (i, j) in cells]
    if which == 'low':
        fs = [[Fr(j) - h for (i, j) in cells], [Fr(i) - h for (i, j) in cells], dm, da]
    else:
        for k in range(n_):
            fs.append([1 if i == k else 0 for (i, j) in cells])
            fs.append([1 if j == k else 0 for (i, j) in cells])
        fs += [dm, da]
    NN = n_ * n_
    out = []
    for f in fs:
        m = Fr(sum(f), NN)
        out.append([(Fr(x) - m) / NN for x in f])
    return out

def explicit_invariants(n_, which):
    a = test_functions(n_, which); NN = n_ * n_
    diag = [sum(ak[c] ** 2 for ak in a) for c in range(NN)]
    trA = sum(diag)
    G = [[sum(ak[c] * al[c] for c in range(NN)) for al in a] for ak in a]
    trA2 = sum(g ** 2 for row in G for g in row)       # tr(A^2) = ||G||_F^2 with G Gram of the a_k
    d2 = sum(x ** 2 for x in diag)
    return trA, trA2, d2

def exhaustive_n3():
    n_ = 3; NN = 9
    res = {}
    for which in ('low', 'full'):
        a = test_functions(n_, which)
        s1 = Fr(0); s2 = Fr(0); cnt = 0
        for perm in itertools.permutations(range(1, 10)):
            z = [Fr(v) - 5 for v in perm]
            E = sum(sum(ak[c] * z[c] for c in range(NN)) ** 2 for ak in a)
            s1 += E; s2 += E * E; cnt += 1
        res[which] = (s1 / cnt, s2 / cnt - (s1 / cnt) ** 2)
    return res

if __name__ == '__main__':
    out = {}
    print('c22 =', c22); print('c4  =', c4)
    out['c22'] = str(c22); out['c4'] = str(c4)
    sub = {p2: P2, p3: P3, p4: P4}
    print('c22 (values 1..N) =', sp.factor(c22.subs(sub))); print('c4 (values 1..N) =', sp.factor(c4.subs(sub)))
    out['c22_perm'] = str(sp.factor(c22.subs(sub))); out['c4_perm'] = str(sp.factor(c4.subs(sub)))
    for Nn in (4, 5, 6, 7):
        brute_check(Nn, trials=2 if Nn < 7 else 1, seed=Nn)
    print('step-1 identity verified by full enumeration, N=4..7')
    paper = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'variance_fits.json')))
    forms = {}
    for which in ('low', 'full'):
        for par in ('odd', 'even'):
            V, M = variance(which, par)
            inv = invariants(which, par)
            forms[(which, par)] = V
            pe = sp.sympify(paper[which][par]['expr'], locals={'n': n})
            diff = sp.simplify(V - pe)
            lead = sp.limit(V / n ** (8 if which == 'low' else 3), n, sp.oo)
            print(f'{which} {par}: Var =', V)
            print('    invariants trA, trA2, d2 =', [sp.factor(x) for x in inv])
            print('    mean =', M, ' | Var - paper =', diff, ' | leading coeff =', lead)
            out[f'{which}_{par}'] = {'var': str(V), 'mean': str(M), 'trA': str(sp.factor(inv[0])),
                                     'trA2': str(sp.factor(inv[1])), 'd2': str(sp.factor(inv[2])),
                                     'minus_paper': str(diff), 'leading_coeff': str(lead)}
            # next-order term
            ser = sp.series(V.subs(n, 1 / sp.Symbol('t')), sp.Symbol('t'), 0, -(8 if which == 'low' else 3) + 3)
            out[f'{which}_{par}']['expansion_large_n'] = str(ser)
    # invariants vs explicit matrices
    for n_ in range(3, 26):
        par = 'odd' if n_ % 2 else 'even'
        for which in ('low', 'full'):
            ex = explicit_invariants(n_, which)
            sy = [x.subs(n, n_) for x in invariants(which, par)]
            assert all(sp.Rational(e.numerator, e.denominator) == s for e, s in zip(ex, sy)), (n_, which)
    print('invariants verified against explicit matrices, n=3..25')
    # table vs paper values n<=45 (values stored in json) and paper exprs
    table = []
    for n_ in range(3, 46):
        par = 'odd' if n_ % 2 else 'even'
        row = [n_]
        for which in ('low', 'full'):
            v = forms[(which, par)].subs(n, n_)
            pe = sp.sympify(paper[which][par]['expr'], locals={'n': n}).subs(n, n_)
            assert v == pe
            row.append(str(v))
        table.append(row)
    out['table'] = table
    print('closed forms equal paper expressions at n=3..45')
    ex3 = exhaustive_n3()
    print('n=3 exhaustive: low mean,var =', ex3['low'], ' full mean,var =', ex3['full'])
    assert ex3['low'][1] == Fr(1532, 2187) and ex3['full'][1] == Fr(398, 2187)
    assert forms[('low', 'odd')].subs(n, 3) == sp.Rational(1532, 2187)
    assert forms[('full', 'odd')].subs(n, 3) == sp.Rational(398, 2187)
    assert forms[('low', 'even')].subs(n, 4) == sp.Rational(14093, 1440)
    assert forms[('full', 'even')].subs(n, 4) == sp.Rational(527, 640)
    print('n=3 exhaustive and n=4 paper values confirmed')
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'variance_proof_results.json'), 'w'), indent=1)

# ---------------------------------------------------------------- compact form and Gaussian comparison
def compact_and_gauss():
    sub = {p2: P2, p3: P3, p4: P4}
    kA = sp.factor(c22.subs(sub) - (P2 / (N - 1)) ** 2)
    print('Var(z^T A z) = [', kA, '] (trA)^2 + [', sp.factor(2 * c22.subs(sub)), '] trA2 + [', sp.factor(c4.subs(sub)), '] d2')
    t = sp.Symbol('t')
    for which in ('low', 'full'):
        for par in ('odd', 'even'):
            trA, trA2, d2 = invariants(which, par)
            Vg = 2 * (P2 / (N - 1)) ** 2 * trA2           # Gaussian mixture: 2 tr(Sigma_n^2)
            Vg = sp.factor(Vg.subs(N, n ** 2))
            V = variance(which, par)[0]
            ratio = sp.factor(sp.simplify(V / Vg))
            vals = [round(float(ratio.subs(n, k)), 4) for k in range(3, 9) if (k % 2 == 1) == (par == 'odd')]
            print(f'{which} {par}: Var_gauss =', Vg)
            print('   exact/gauss ratio expansion:', sp.series(ratio.subs(n, 1 / t), t, 0, 3).removeO(), ' values:', vals)
            lead = 8 if which == 'low' else 3
            print('   Var expansion:', sp.expand(sp.series(V.subs(n, 1 / t), t, 0, -lead + 3).removeO().subs(t, 1 / n)))

if __name__ == '__main__':
    compact_and_gauss()
    for k in (3,):
        for which in ('low', 'full'):
            trA, trA2, d2 = invariants(which, 'odd')
            Vg = (2 * (P2 / (N - 1)) ** 2 * trA2).subs(N, n ** 2).subs(n, k)
            print(which, 'n=3 gauss sd =', float(sp.sqrt(Vg)), ' exact sd =', float(sp.sqrt(variance(which, 'odd')[0].subs(n, 3))))
