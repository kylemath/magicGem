import itertools
from lattice import basis, lll, enumerate_short
from math import comb
# brute force check of enumerate_short on small instances (count of vectors up to sign with ||v||^2<=R2)
import random
random.seed(1)
for (n,k,R2) in [(8,4,4000),(9,5,20000),(10,6,50000),(9,3,3000),(12,8,300000),(7,2,500)]:
    B=lll(basis(n,k)); r=len(B)
    # brute force over coefficient vectors in original (non-reduced) basis Q of t^i (t-1)^{k+1}:
    # any v=(t-1)^K Q with ||v||^2<=R2 has |Q coeffs| bounded: Q = v/(t-1)^K; use generous box via search
    seen=set()
    Borig=basis(n,k)
    X=0
    # find box by growing until no new vectors appear in two consecutive sizes
    prev=-1
    for X in range(1,40):
        cnt=0; s=set()
        for q in itertools.product(range(-X,X+1),repeat=r):
            if not any(q): continue
            v=tuple(sum(q[i]*Borig[i][j] for i in range(r)) for j in range(n))
            if sum(a*a for a in v)<=R2:
                s.add(max(v,tuple(-a for a in v)))
        if len(s)==prev and X>6: break
        prev=len(s)
        if r>=4 and X>8: break
    got=[]
    enumerate_short(B,R2,lambda x,v:(got.append(tuple(v)),False)[1])
    gs=set(max(v,tuple(-a for a in v)) for v in got)
    print(n,k,R2,"brute",len(s),"enum",len(gs),"match",gs==s,"subset",s<=gs, "enum dup-free", len(gs)==len(got))
