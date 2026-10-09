#!/usr/bin/env python3.9
"""Independent re-derivations for Referee A (v5)."""
import itertools, math, sys
from fractions import Fraction as Fr
from collections import Counter
import numpy as np

def lines(n):
    L = []
    for k in range(n): L.append([(k, j) for j in range(n)])
    for l in range(n): L.append([(i, l) for i in range(n)])
    L.append([(i, i) for i in range(n)])
    L.append([(i, n - 1 - i) for i in range(n)])
    return L

def energies(S, n):
    N = n * n; M = n * (N + 1) // 2
    Ls = lines(n)
    N2Efull = sum((sum(S[i][j] for i, j in L) - M) ** 2 for L in Ls)
    # E_low: Cov(X,Z)^2+Cov(Y,Z)^2 + diag terms
    c = Fr(n - 1, 2)
    cx = sum((Fr(j) - c) * (S[i][j] - Fr(N + 1, 2)) for i in range(n) for j in range(n)) / N
    cy = sum((c - Fr(i)) * (S[i][j] - Fr(N + 1, 2)) for i in range(n) for j in range(n)) / N
    dm = sum(S[i][i] for i in range(n)) - M
    da = sum(S[i][n - 1 - i] for i in range(n)) - M
    Elow = cx ** 2 + cy ** 2 + Fr(dm * dm + da * da, N * N)
    return Fr(N2Efull, N * N), Elow

# ---------- A. exhaustive n=3 ----------
def exhaustive3():
    n = 3; N = 9
    full = {}; low = {}
    cells = [(i, j) for i in range(3) for j in range(3)]
    for p in itertools.permutations(range(1, 10)):
        S = [list(p[0:3]), list(p[3:6]), list(p[6:9])]
        ef, el = energies(S, 3)
        full[p] = ef; low[p] = el
    def stats(d):
        vals = list(d.values())
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        return mean, var, len(set(vals)), max(vals), Counter(vals).most_common(1)[0]
    print("n=3 Efull mean,var,#distinct,max,mode:", stats(full))
    print("n=3 Elow  mean,var,#distinct,max,mode:", stats(low))
    # local minima under single swaps
    def nmin(d):
        cnt = 0; nonmagic = 0
        for p, v in d.items():
            ismin = True
            for a in range(9):
                for b in range(a + 1, 9):
                    q = list(p); q[a], q[b] = q[b], q[a]
                    if d[tuple(q)] < v: ismin = False; break
                if not ismin: break
            if ismin:
                cnt += 1
                if v != 0: nonmagic += 1
        return cnt, nonmagic
    print("n=3 local minima Efull (total, nonmagic):", nmin(full))
    print("n=3 local minima Elow  (total, nonmagic):", nmin(low))
    print("zeros:", sum(1 for v in full.values() if v == 0), sum(1 for v in low.values() if v == 0))

# ---------- B. exact variance n=4 via line-pair enumeration ----------
def exact_var_full(n):
    N = n * n; M = n * (N + 1) // 2
    vals = list(range(1, N + 1))
    # E[delta_L^2 delta_L'^2] for |L cap L'| in {0,1,n}
    # delta over an ordered sample of distinct values; by symmetry use subsets
    from itertools import combinations
    def E_same():
        tot = Fr(0); cnt = 0
        for c in combinations(vals, n):
            d = sum(c) - M; tot += d ** 4; cnt += 1
        return tot / cnt
    def E_disjoint():
        tot = Fr(0); cnt = 0
        for c in combinations(vals, 2 * n):
            for a in combinations(c, n):
                b = tuple(v for v in c if v not in a)
                tot += (sum(a) - M) ** 2 * (sum(b) - M) ** 2; cnt += 1
        return tot / cnt
    def E_meet1():
        tot = Fr(0); cnt = 0
        for c in combinations(vals, 2 * n - 1):
            for s in c:
                rest = [v for v in c if v != s]
                for a in combinations(rest, n - 1):
                    b = tuple(v for v in rest if v not in a)
                    tot += (sum(a) + s - M) ** 2 * (sum(b) + s - M) ** 2; cnt += 1
        return tot / cnt
    es, ed, e1 = E_same(), E_disjoint(), E_meet1()
    Ls = lines(n)
    tot = Fr(0)
    for L1 in Ls:
        for L2 in Ls:
            k = len(set(L1) & set(L2))
            tot += {0: ed, 1: e1, n: es}[k]
    EE2 = tot / N ** 4
    EE = Fr(n ** 4 - 1, 6 * n * n)
    return EE2 - EE ** 2

def exact_var_low(n):
    """Var(E_low) by Monte Carlo-free exact enumeration is heavy; instead use the
    quadruple-pattern approach generically: E[(sum_c a_c z_pi(c))^2 (sum_c b_c z_pi(c))^2]."""
    N = n * n
    # test functions (centred, divided by N) as arrays over cells
    c = Fr(n - 1, 2)
    cells = [(i, j) for i in range(n) for j in range(n)]
    X = [(Fr(j) - c) / N for i, j in cells]
    Y = [(c - Fr(i)) / N for i, j in cells]
    Dm = [(Fr(1 if i == j else 0) - Fr(1, n)) / N for i, j in cells]
    Da = [(Fr(1 if i + j == n - 1 else 0) - Fr(1, n)) / N for i, j in cells]
    z = [Fr(v) - Fr(N + 1, 2) for v in range(1, N + 1)]
    # permutation moments: E[z_pi(c1) z_pi(c2) z_pi(c3) z_pi(c4)] depends on equality pattern
    p2 = sum(v ** 2 for v in z); p4 = sum(v ** 4 for v in z)
    # all odd power sums vanish (symmetric). Patterns: (4): p4/N ; (2,2) distinct cells:
    # E[z_a^2 z_b^2] = (p2^2 - p4)/(N(N-1)) ; (2,1,1): E[z_a^2 z_b z_c] with b!=c distinct from a:
    # sum over distinct a,b,c of z_a^2 z_b z_c = sum_a z_a^2 * sum_{b!=c, not a} z_b z_c
    # = sum_a z_a^2 [ (S1 - z_a)^2 - (p2 - z_a^2) ] with S1=0 => sum_a z_a^2 (z_a^2 - p2 + z_a^2) = 2p4 - p2^2
    # divided by N(N-1)(N-2)
    # (1,1,1,1): sum distinct z_a z_b z_c z_d = ... use e4 of elementary symmetric: 24 e4 ; e4 from Newton: with S1=0,S3=0:
    # e1=0,e2=-p2/2,e3=0 (p3=0), e4 = (e3 p1 - e2 p2 + e1 p3 - p4)/4 = (p2^2/2 - p4)/4
    E4 = p4 / N
    E22 = (p2 ** 2 - p4) / (N * (N - 1))
    E211 = (2 * p4 - p2 ** 2) / (N * (N - 1) * (N - 2))
    E31 = -p4 / (N * (N - 1))
    e4 = (p2 ** 2 / 2 - p4) / 4
    E1111 = 24 * e4 / (N * (N - 1) * (N - 2) * (N - 3))
    def Eprod(a, b):
        # E[(a.z_pi)^2 (b.z_pi)^2] = sum_{c1,c2,c3,c4} a1 a2 b3 b4 E[z z z z]
        tot = Fr(0)
        n_ = len(a)
        # group by pattern: iterate over all quadruples -- N^4 = 65536 for n=4, fine
        for c1 in range(n_):
            for c2 in range(n_):
                for c3 in range(n_):
                    for c4 in range(n_):
                        w = a[c1] * a[c2] * b[c3] * b[c4]
                        if w == 0: continue
                        s = {c1, c2, c3, c4}
                        k = len(s)
                        if k == 4: m = E1111
                        elif k == 1: m = E4
                        elif k == 2:
                            cnt = Counter([c1, c2, c3, c4])
                            m = E22 if sorted(cnt.values()) == [2, 2] else E31
                        else:  # k==3 -> pattern (2,1,1)
                            m = E211
                        tot += w * m
        return tot
    fs = [X, Y, Dm, Da]
    EE2 = sum(Eprod(a, b) for a in fs for b in fs)
    EE = Fr((n * n + 1) * (n ** 4 - n * n + 12 * n - 12), 72 * n * n)
    return EE2 - EE ** 2

def paper_var(n):
    if n % 2:
        Po = 25*n**11+25*n**10-82*n**9-82*n**8-9*n**7-1209*n**6+3738*n**5-5862*n**4+2160*n**3-2880*n**2-4320*n+4320
        Qo = 5*n**6-5*n**5-17*n**4+11*n**3-24*n**2+18*n+6
        return Fr((n-1)*(n*n+1)*Po, 129600*n**6), Fr((n-1)*(n*n+1)*Qo, 180*n**6)
    else:
        Pe = 25*n**10-107*n**8+73*n**6-1200*n**5+4947*n**4-9600*n**3+13782*n**2-13680*n+10080
        Qe = 5*n**5-12*n**3+12*n**2-23*n+12
        return Fr((n*n+1)*Pe, 129600*n**4), Fr((n-2)*(n*n+1)*Qe, 180*n**5)

# ---------- C. 4x4 magic squares, swaps, hulls ----------
def magic4():
    from itertools import combinations, permutations
    rows=[p for c in combinations(range(1,17),4) if sum(c)==34 for p in permutations(c)]
    res=[]
    for r0 in rows:
        s0=set(r0)
        for r1 in rows:
            if s0&set(r1): continue
            s1=s0|set(r1)
            for r2 in rows:
                if s1&set(r2): continue
                if r0[0]+r1[1]+r2[2]>=34 or r0[3]+r1[2]+r2[1]>=34: continue
                s2=s1|set(r2)
                r3=tuple(34-r0[j]-r1[j]-r2[j] for j in range(4))
                if set(r3)&s2 or len(set(r3))<4 or min(r3)<1 or max(r3)>16: continue
                if r0[0]+r1[1]+r2[2]+r3[3]!=34 or r0[3]+r1[2]+r2[1]+r3[0]!=34: continue
                res.append(r0+r1+r2+r3)
    return res

def d4_images(S, n):
    A = np.array(S).reshape(n, n)
    out = []
    for k in range(4):
        B = np.rot90(A, k); out.append(tuple(B.flatten())); out.append(tuple(B.T.flatten()))
    return out

def hull_data(S, n):
    from scipy.spatial import ConvexHull
    N = n*n
    pts = []
    for i in range(n):
        for j in range(n):
            pts.append((2*j-(n-1), (n-1)-2*i, 2*S[i*n+j]-(N+1)))  # doubled -> integers
    P = np.array(pts, dtype=float)
    h = ConvexHull(P)
    planes = {}
    for simp in h.simplices:
        p0, p1, p2 = [np.array(pts[k]) for k in simp]
        nrm = np.cross(p1-p0, p2-p0).astype(int)
        g = math.gcd(math.gcd(abs(int(nrm[0])), abs(int(nrm[1]))), abs(int(nrm[2])))
        nrm = nrm // g
        d = int(nrm @ p0)
        # orient outward: centroid (origin) must satisfy nrm.x < d
        if d < 0: nrm = -nrm; d = -d
        planes[(tuple(nrm), d)] = True
    F = len(planes)
    onplane = {k: set() for k in range(N)}
    for (nrm, d) in planes:
        for k, p in enumerate(pts):
            if np.array(nrm) @ np.array(p) == d: onplane[k].add((nrm, d))
    verts = [k for k in range(N) if len(onplane[k]) >= 3]
    V = len(verts)
    edges = set()
    for a in verts:
        for b in verts:
            if a < b and len(onplane[a] & onplane[b]) >= 2: edges.add((a, b))
    E = len(edges)
    vol = Fr(h.volume).limit_denominator(100) / 8
    return V, E, F, vol, verts, pts

def sectionC():
    allm = magic4()
    print("4x4 magic squares:", len(allm))
    seen = set(); reps = []
    for S in allm:
        if S in seen: continue
        imgs = d4_images(S, 4)
        for I in imgs: seen.add(I)
        reps.append(S)
    print("D4 classes:", len(reps))
    # min gap multiset
    Ls = lines(4)
    cells = [(i, j) for i in range(4) for j in range(4)]
    def m_ab(a, b):
        return sum(1 for L in Ls if ((a in L) != (b in L)))
    mg = Counter()
    for S in reps:
        best = None
        for a in range(16):
            for b in range(a+1, 16):
                d = abs(S[a]-S[b]); g = d*d*m_ab(cells[a], cells[b])
                best = g if best is None else min(best, g)
        mg[best] += 1
    print("min-gap multiset N^2*Dmin over 880:", dict(mg))
    # hulls
    fv = Counter(); Vc = Counter(); vols = []; hv_sets = []
    selfcomp = 0
    canon = {}
    for idx, S in enumerate(reps):
        for I in d4_images(S, 4): canon[I] = idx
    for idx, S in enumerate(reps):
        V, E, F, vol, verts, pts = hull_data(S, 4)
        fv[(V, E, F)] += 1; Vc[V] += 1; vols.append(vol)
        hv_sets.append(frozenset(tuple(pts[k]) for k in verts))
        comp = tuple(17 - v for v in S)
        if canon[comp] == idx: selfcomp += 1
    print("V distribution:", dict(sorted(Vc.items())))
    print("#f-vectors:", len(fv), " modal:", fv.most_common(3))
    print("volumes: min", min(vols), "max", max(vols), "mean", float(sum(vols)/len(vols)), "#distinct", len(set(vols)))
    print("self-complementary classes:", selfcomp)
    print("distinct hull-vertex point sets:", len(set(hv_sets)))
    # congruence classes via sorted squared-distance multiset of hull vertices, then exact check (brute force bijection)
    import itertools as it
    def dist_sig(fs):
        P = list(fs)
        return tuple(sorted(sum((a-b)**2 for a, b in zip(p, q)) for p, q in it.combinations(P, 2)))
    groups = {}
    for i, fs in enumerate(hv_sets): groups.setdefault((len(fs), dist_sig(fs)), []).append(i)
    print("distance-signature groups:", len(groups), " sizes:", Counter(len(g) for g in groups.values()))
    # named squares
    durer = (16,3,2,13,5,10,11,8,9,6,7,12,4,15,14,1)
    d802 = (5,10,11,8,16,3,2,13,4,15,14,1,9,6,7,12)
    for nm, S in [("Durer", durer), ("#802", d802)]:
        V, E, F, vol, _, _ = hull_data(S, 4); print(nm, (V, E, F), "vol", vol)
    losh = (2,7,6,9,5,1,4,3,8)
    V, E, F, vol, _, _ = hull_data(losh, 3); print("LoShu", (V, E, F), "vol", vol)
    return groups, hv_sets

# ---------- D. diagonal-only count n=4 ----------
def diag_count4():
    vals = range(1, 17)
    from itertools import combinations
    cnt = 0
    for a in combinations(vals, 4):
        if sum(a) != 34: continue
        rest = [v for v in vals if v not in a]
        for b in combinations(rest, 4):
            if sum(b) == 34: cnt += 1
    return cnt * 24 * 24 * math.factorial(8)

if __name__ == "__main__":
    what = sys.argv[1:] or ["A", "B", "C", "D"]
    if "A" in what: exhaustive3()
    if "B" in what:
        for n in (3, 4):
            vf = exact_var_full(n); vl = exact_var_low(n); pl, pf = paper_var(n)
            print(f"n={n}: Var(Efull) mine={vf} paper={pf} eq={vf==pf};  Var(Elow) mine={vl} paper={pl} eq={vl==pl}")
    if "C" in what: sectionC()
    if "D" in what: print("diagonal-only count n=4:", diag_count4())
