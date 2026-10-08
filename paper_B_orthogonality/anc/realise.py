"""Realise a prescribed column-deviation vector gamma (sum 0) by an arrangement with all row sums M(n).
Start: explicit semi-magic square (constructions.construct, or Siamese/other for small n); moves: swaps
within a row (row sums invariant).  Greedy steepest descent on sum_j (colsum_j - M - gamma_j)^2 with random
kicks.  Any returned arrangement is checked exactly by check()."""
import random
import numpy as np
from constructions import construct, siamese

def start_square(n):
    try:
        s,_=construct(n); return [row[:] for row in s]
    except AssertionError:
        pass
    # fallback: any arrangement with equal row sums: pair complements in rows for even n, Siamese for odd
    if n%2==1: return siamese(n)
    raise ValueError(n)

def check(s, gamma, rho=None):
    n=len(s); N=n*n; M=n*(N+1)//2
    assert sorted(v for r in s for v in r)==list(range(1,N+1))
    rows=[sum(r)-M for r in s]; cols=[sum(s[i][j] for i in range(n))-M for j in range(n)]
    return cols==list(gamma) and (rho is None or rows==list(rho))

def realise(gamma, seed=0, maxit=200000):
    n=len(gamma); N=n*n; M=n*(N+1)//2
    rng=random.Random(seed)
    S=np.array(start_square(n),dtype=np.int64)
    target=M+np.array(gamma,dtype=np.int64)
    e=S.sum(axis=0)-target
    it=0
    while it<maxit:
        it+=1
        if not e.any():
            return S.tolist()
        # for every pair (j,jp) and row i: d=S[i,jp]-S[i,j]; new e_j=e_j+d, e_jp=e_jp-d
        D=S[:,None,:]-S[:,:,None]          # D[i,j,jp]=S[i,jp]-S[i,j]
        ej=e[None,:,None]; ejp=e[None,None,:]
        gain=ej**2+ejp**2-(ej+D)**2-(ejp-D)**2
        idx=np.unravel_index(np.argmax(gain),gain.shape)
        if gain[idx]>0:
            i,j,jp=idx
            d=D[i,j,jp]
            S[i,j],S[i,jp]=S[i,jp],S[i,j]
            e[j]+=d; e[jp]-=d
        else:
            # random kick: a few random row swaps
            for _ in range(rng.randint(1,3)):
                i=rng.randrange(n); j,jp=rng.sample(range(n),2)
                d=S[i,jp]-S[i,j]
                S[i,j],S[i,jp]=S[i,jp],S[i,j]
                e[j]+=d; e[jp]-=d
    return None

if __name__=="__main__":
    import sys,json
    n=int(sys.argv[1])
    from math import comb
    g=[(-1)**j*comb(n-1,j) for j in range(n)]
    s=realise(g)
    print(s is not None and check(s,g,[0]*n))
