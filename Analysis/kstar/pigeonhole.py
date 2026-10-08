"""Rigorous lower bounds for k*(n) by the pigeonhole (box) principle over twin swaps.

Setting: base semi-magic square S with twin row pairs (i,i') on column sets J (constructions.py).
Pair adjacent columns (j_q, j_q+1), q = 0..Q-1, j_q = j0 + 2q.  For each q let D_q be the multiset of
d = s[i][j_q+1]-s[i][j_q] over the twin pairs whose column set contains both columns.
For any choice of subsets, g_q = sum of a sub-multiset of D_q; two choices g != g' with equal moments
mu_r = sum_q g_q C(q,r) (0<=r<=K-2) give an arrangement with rho = 0 and
gamma = sum_q (g_q-g'_q)(e_{j_q}-e_{j_q+1}),  P_gamma = t^{j0}(1-t) G(t^2),  (u-1)^{K-1} | G,
hence (t-1)^K | P_gamma, i.e. the degree-(K-1) conditions hold and gamma != 0:  k*(n) >= K.
Box principle: if prod_q V_q > prod_{r=0}^{K-2} (sum_q W_q C(q,r) + 1) such a pair exists, where
V_q = #distinct sub-multiset sums of D_q and W_q = sum |d| over D_q.
Two versions: 'exact' (V_q, W_q computed from the explicit square) and 'generic' (V_q >= ceil(R_q/2)+1,
W_q <= R_q (N-1), R_q = |D_q|), the latter being what the written proof uses.
"""
from math import comb, log, ceil
from constructions import construct


def pair_data(n):
    s, twins = construct(n)
    N = n * n
    if n % 2 == 0:
        j0 = 0
    else:
        j0 = 1
    Q = (n - j0) // 2
    D = []
    for q in range(Q):
        j = j0 + 2 * q
        if j + 1 >= n:
            break
        ds = [s[i][j + 1] - s[i][j] for (i, ip), cols in twins if j in cols and j + 1 in cols]
        D.append(ds)
    while D and not D[-1]:
        D.pop()
    return N, D


def subset_sum_count(ds):
    S = {0}
    for d in ds:
        S = S | {x + d for x in S}
    return len(S)


def best_K(V, W):
    """largest K with V > prod_{r=0}^{K-2} (sum_q W_q C(q,r)+1)   (exact integers; V = prod_q V_q)"""
    Q = len(W)
    K = 1
    acc = 1
    while True:
        r = K - 1  # adding moment r allows K+1
        span = sum(W[q] * comb(q, r) for q in range(Q))
        acc2 = acc * (span + 1)
        if V > acc2:
            acc = acc2
            K += 1
        else:
            return K


def bounds(n, exact=True):
    N, D = pair_data(n)
    if exact:
        logV = 1
        for ds in D: logV *= subset_sum_count(ds)
        W = [sum(abs(d) for d in ds) for ds in D]
    else:
        logV = 1
        for ds in D: logV *= (len(ds) + 1) // 2 + 1
        W = [len(ds) * (N - 1) for ds in D]
    return best_K(logV, W)


if __name__ == "__main__":
    import sys, json
    out = {}
    for n in list(range(14, 101)) + [120, 150, 200, 300, 400, 600, 1000]:
        if n % 4 == 2 and n < 14:
            continue
        kg = bounds(n, exact=False)
        ke = bounds(n, exact=True) if n <= 150 else None
        out[n] = dict(generic=kg, exact=ke)
        print(n, "generic K", kg, "exact-d K", ke, "sqrt(n)", round(n ** 0.5, 2), flush=True)
    json.dump(out, open("pigeonhole_bounds.json", "w"), indent=1)
