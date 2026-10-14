PRELUDE = '''# Shared setup: runs before every step's code.
from math import comb, e, pi, log, sqrt, floor, sin, cos, exp

# The order-5 witness of Appendix C (all row sums 65, not semi-magic)
S = [[1, 22, 11, 24, 7], [23, 3, 12, 2, 25], [18, 6, 19, 17, 5],
     [4, 21, 14, 10, 16], [20, 9, 15, 8, 13]]
n = len(S); N = n * n; M = n * (N + 1) // 2

def column_deviations(S):
    return [sum(row[j] for row in S) - M for j in range(len(S))]

def order_of_vanishing_at_1(gamma):
    B = [sum(comb(j, r) * g for j, g in enumerate(gamma)) for r in range(len(gamma))]
    K = 0
    while K < len(B) and B[K] == 0:
        K += 1
    return K

def P(gamma, t):
    return sum(g * t**j for j, g in enumerate(gamma))

# The n = 14 witness's column deviations (k*(14) = 12)
GAMMA14 = __G14__
'''

RUNS = {
"S0": '''gamma = column_deviations(S)
rho = [sum(row) - M for row in S]
print("M(n) =", M)
print("column deviations gamma =", gamma, " sum =", sum(gamma))
print("row deviations rho      =", rho)

def degree_k_conditions(S, k):
    z = [[S[i][j] - (N + 1) / 2 for j in range(n)] for i in range(n)]
    x = [j - (n - 1) / 2 for j in range(n)]
    cols = all(abs(sum(z[i][j] * x[j]**m for i in range(n) for j in range(n))) < 1e-9 for m in range(1, k + 1))
    rows = all(abs(sum(z[i][j] * x[i]**m for i in range(n) for j in range(n))) < 1e-9 for m in range(1, k + 1))
    return cols and rows

for k in range(1, n):
    print("degree-%d conditions hold:" % k, degree_k_conditions(S, k))''',
"S1a": '''phi = [2, -1, 0, 1, 3]          # any weights, one per column; try your own
z = [[v - (N + 1) // 2 for v in row] for row in S]
gamma = column_deviations(S)

lhs = sum(phi[j] * z[i][j] for i in range(n) for j in range(n))   # 25 terms
rhs = sum(phi[j] * gamma[j] for j in range(n))                      # 5 terms
print("cell-by-cell sum:", lhs)
print("column sum      :", rhs)
print("equal:", lhs == rhs)''',
"S1b": '''gamma = column_deviations(S)    # (1, -4, 6, -4, 1)
c = (n - 1) / 2
for m in range(n):
    power = sum((j - c)**m * g for j, g in enumerate(gamma))
    binom = sum(comb(j, m) * g for j, g in enumerate(gamma))
    print("m = %d   power moment = %8.2f   binomial moment = %4d" % (m, power, binom))
# Both columns are zero for m = 0..3 and nonzero at m = 4.''',
"S1c": '''for gamma in [column_deviations(S), GAMMA14]:
    B = [sum(comb(j, r) * g for j, g in enumerate(gamma)) for r in range(len(gamma))]
    K = order_of_vanishing_at_1(gamma)
    print("n =", len(gamma), " Taylor coefficients at 1:", B[:K + 2], "...")
    print("   (t-1)^%d divides P_gamma, so the degree-%d conditions hold" % (K, K - 1))
    # check: P(t) equals the Taylor sum at a random point
    t = 0.37
    print("   P(t) =", round(P(gamma, t), 9), " Taylor sum =", round(sum(b * (t - 1)**r for r, b in enumerate(B)), 9))''',
"S2a": '''from itertools import combinations
worst = 0
for p in range(1, n + 1):
    bound = p * n * (N - p * n) / 2
    for J in combinations(range(n), p):
        dev = sum(sum(S[i][j] for i in range(n)) - M for j in J)
        assert abs(dev) <= bound
    print("p = %d: bound pn(N-pn)/2 = %6.1f" % (p, bound))
print("every set J of columns satisfies the bound")''',
"S2b": '''for gamma in [column_deviations(S), GAMMA14]:
    m = len(gamma); NN = m * m
    L = sum(abs(g) for g in gamma)
    p = sum(1 for g in gamma if g > 0)
    print("n = %d: ||gamma||_1 = %d = 2 * %d,  pn(N-pn) = %d,  N^2/4 = %d"
          % (m, L, sum(g for g in gamma if g > 0), p * m * (NN - p * m), NN * NN // 4))''',
"S3a": '''import cmath
gamma = [5, -3, 0, 2, -7, 3]      # any nonzero integer vector; try your own

def mean_log_on_circle(gamma, samples=20000):
    total = 0.0
    for i in range(samples):
        theta = (i + 0.5) / samples - 0.5
        z = cmath.exp(2j * pi * theta)
        total += log(abs(sum(g * z**j for j, g in enumerate(gamma))))
    return total / samples

print("average of log|P| on the unit circle:", round(mean_log_on_circle(gamma), 4))
print("leading coefficient:", gamma[-1], " so log|a| =", round(log(abs(gamma[-1])), 4))
print("Jensen: the average is log|a| plus log|alpha| for each root outside the circle, so it is >= 0")''',
"S3b": '''import cmath
gamma = GAMMA14
L = sum(abs(g) for g in gamma)
biggest = max(abs(P(gamma, cmath.exp(2j * pi * i / 4000))) for i in range(4000))
print("L =", L, "  max |P(z)| on the circle =", round(biggest, 2), "  <= L:", biggest <= L)''',
"S3c": '''import cmath
gamma = GAMMA14
m = len(gamma); L = sum(abs(g) for g in gamma)
K = order_of_vanishing_at_1(gamma)
ok = True
for i in range(1, 2000):
    z = cmath.exp(2j * pi * (i / 2000 - 0.5))
    if abs(P(gamma, z)) > L * comb(m - 1, K) * abs(z - 1)**K * (1 + 1e-9):
        ok = False
print("K =", K, "  bound L*C(n-1,K)*|z-1|^K holds on the circle:", ok)
z = cmath.exp(2j * pi * 0.01)
print("at theta = 0.01: |P(z)| =", "%.3g" % abs(P(gamma, z)),
      "  bound =", "%.3g" % (L * comb(m - 1, K) * abs(z - 1)**K))''',
"S3d": '''bad = [(m, K) for m in range(2, 120) for K in range(1, m)
       if comb(m - 1, K) > (e * (m - 1) / K)**K]
print("checked n < 120, all K: counterexamples =", bad)''',
"S3e": '''worst = max(abs(2 * sin(pi * t)) - 2 * pi * abs(t)
            for t in [i / 1000 - 0.5 for i in range(1001)])
print("max of chord - arc over theta in [-1/2, 1/2]:", worst, "(<= 0)")''',
"S3f": '''def integral(beta, steps=20000):
    h = 1 / steps
    return sum(log(min(1, beta * abs(-0.5 + (i + 0.5) * h))) for i in range(steps)) * h

for beta in [2, 5, 2 * pi * e]:
    print("beta = %.3f   integral = %.6f   -2/beta = %.6f" % (beta, integral(beta), -2 / beta))''',
"S3g": '''for gamma in [column_deviations(S), GAMMA14]:
    m = len(gamma)
    K = order_of_vanishing_at_1(gamma)
    L = sum(abs(g) for g in gamma)
    print("n = %2d: K^2 = %4d  <=  pi*e*(n-1)*log L = %.1f : %s"
          % (m, K * K, pi * e * (m - 1) * log(L), K * K <= pi * e * (m - 1) * log(L)))''',
"S4a": '''def upper_bound(n):
    return floor(sqrt(pi * e * (n - 1) * log(n**4 / 4)))

for m in [5, 14, 40, 100, 166, 169, 1000]:
    print("n = %4d: k*(n) <= %4d   (n - 1 = %d)" % (m, upper_bound(m), m - 1))''',
"S4b": '''bad = [m for m in range(3, 5000) if not (m - 1) * log(m**4 / 4) < 4 * m * log(m)]
print("n with (n-1) log(n^4/4) >= 4 n log n, for 3 <= n < 5000:", bad)
print("2*sqrt(pi*e) =", 2 * sqrt(pi * e))''',
}
