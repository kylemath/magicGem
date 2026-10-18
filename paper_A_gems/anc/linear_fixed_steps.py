"""
linear_fixed_steps.py -- checks for Section sec:fixed-steps (linear squares with fixed steps).
  1. Lemma lem:fib-triangle: the integer hull of T_k = {x, y >= 0, F_{2k} x + F_{2k+1} y <= F_{2k+1}^2 - 1} has exactly
     the k+3 vertices O, P_0, ..., P_{k+1}, for k = 1..15 (exact 2D hull).
  2. Proposition prop:many-vertices for k = 1, 2, 3 at the least admissible prime n (7, 29, 173): the square is magic
     by its line sums, and the k+3 cells over the vertices of T_k are gem vertices (exact hull).
  3. Corollary cor:many-vertices at every prime 7 <= n < 120: the square of the proof is magic and its gem has the
     predicted k+3 vertex cells and at least ceil(ln n / (4 ln phi)) + 2 vertices (exact hull).
  4. Proposition prop:fixed-steps, examples (exact hulls of all n^2 points): the Siamese family is constant for odd
     5 <= n <= 61; u=(1,2), w=(1,3), alpha=beta=0 satisfies f(n) = f(n+6) for 101 <= n <= 112 (delta*L = 6);
     u=(1,3), w=(3,1), alpha=beta=0 satisfies f(n) = f(n+24) for 150 <= n <= 197 (delta*L = 24) and no smaller shift
     works on that window.
Usage: python3 linear_fixed_steps.py   (about 5 min).  Writes linear_fixed_steps.log.
"""
import sys, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull

log = []
def out(s):
    print(s, flush=True); log.append(s)

F = [0, 1]
while len(F) < 80: F.append(F[-1] + F[-2])
def Fz(t):  # Fibonacci numbers on all of Z: F_{-t} = (-1)^(t+1) F_t
    return F[t] if t >= 0 else (-1) ** (-t + 1) * F[-t]

def hull2d(pts):
    """vertices of the convex hull of integer points (collinear points dropped)"""
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def square(n, u, w, al, be):
    I, J = np.indices((n, n))
    return n * ((u[0] * I + u[1] * J + al) % n) + (w[0] * I + w[1] * J + be) % n + 1

def is_magic(S):
    n = S.shape[0]; N = n * n; M = n * (N + 1) // 2
    return (len(np.unique(S)) == N and (S.sum(0) == M).all() and (S.sum(1) == M).all()
            and int(np.trace(S)) == M and int(np.trace(S[:, ::-1])) == M)

def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** .5) + 1))

def vertex_cells(S):
    n = S.shape[0]; h = exact_hull(S)
    return tuple(h['f_vector']), {(v // n, v % n) for v in h['vertices']}

# 1. the Fibonacci triangle
for k in range(1, 16):
    a, b = F[2 * k], F[2 * k + 1]; R = b * b - 1
    # per column x the lattice points of T_k are (x, 0..floor((R - a x)/b)); the hull needs only the two ends
    pts = [(x, 0) for x in range(R // a + 1)] + [(x, (R - a * x) // b) for x in range(R // a + 1)]
    H = hull2d(pts)
    pred = {(0, 0)} | {(Fz(2 * i), b - Fz(2 * i - 1)) for i in range(k + 2)}
    assert len(H) == k + 3 and set(H) == pred, (k, H)
out('Lemma lem:fib-triangle: integer hull of T_k has exactly the k+3 predicted vertices for k = 1..15')

# 2. Proposition prop:many-vertices at the least admissible prime
def fib_square(k, n):
    a, b = F[2 * k], F[2 * k + 1]; R = b * b - 1
    assert is_prime(n) and n > max(b * b, 3 * b)
    return square(n, (a, b), (1, 3), n - 1 - R, 0), {(i, j) for (i, j) in
            [(0, 0)] + [(Fz(2 * t), b - Fz(2 * t - 1)) for t in range(k + 2)]}
for k in (1, 2, 3):
    b = F[2 * k + 1]; n = max(b * b, 3 * b) + 1
    while not is_prime(n): n += 1
    S, pred = fib_square(k, n)
    assert is_magic(S)
    f, vc = vertex_cells(S)
    assert pred <= vc
    out(f'Proposition prop:many-vertices, k={k}, n={n}: magic; the {k + 3} cells over the vertices of T_k are gem vertices; f = {f}')

# 3. Corollary cor:many-vertices
phi = (1 + 5 ** .5) / 2; rows = []
for n in range(7, 120):
    if not is_prime(n): continue
    bound = math.ceil(math.log(n) / (4 * math.log(phi))) + 2; k = bound - 3
    S, pred = fib_square(k, n)
    assert is_magic(S)
    f, vc = vertex_cells(S)
    assert pred <= vc and f[0] >= bound
    rows.append(f'{n}:{bound}/{f[0]}')
out('Corollary cor:many-vertices at every prime 7 <= n < 120 (n: bound/V): ' + ' '.join(rows))

# 4. eventual periodicity, examples
m_of = lambda n: (n - 1) // 2
fs = {n: vertex_cells(square(n, (1, 1), (1, 2), -m_of(n), -2 * m_of(n)))[0] for n in range(5, 62, 2)}
assert set(fs.values()) == {(12, 26, 16)}
out('Siamese family u=(1,1), w=(1,2), alpha=-m, beta=-2m: f = (12,26,16) for every odd 5 <= n <= 61')
for u, w, n0, D, reps in (((1, 2), (1, 3), 101, 6, 3), ((1, 3), (3, 1), 150, 24, 3)):
    fv = {n: vertex_cells(square(n, u, w, 0, 0))[0] for n in range(n0, n0 + D * reps)}
    bad = [n for n in fv if n + D in fv and fv[n] != fv[n + D]]
    assert not bad
    smaller = [d for d in range(1, D) if all(fv[n] == fv[n + d] for n in fv if n + d in fv)]
    Vs = [f[0] for f in fv.values()]
    out(f'u={u}, w={w}, alpha=beta=0: f(n) = f(n+{D}) for {n0} <= n <= {n0 + D * (reps - 1) - 1}; '
        f'V ranges over {min(Vs)}..{max(Vs)}; smaller shifts with the same property on the window: {smaller or "none"}')

open(os.path.join(HERE, 'linear_fixed_steps.log'), 'w').write('\n'.join(log) + '\n')
