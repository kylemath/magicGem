"""Cross-check (floating-point MILP, HiGHS via scipy) of the enumeration: at level k = kmax(n)+1, is there a
nonzero gamma in Lambda_{n,k} with |gamma_j| <= n^2(n-1)/2 (test F1 only)?  Compared with the exact
enumeration restricted to F1."""
import json, numpy as np
from math import comb
from scipy.optimize import milp, LinearConstraint, Bounds
from lattice import lll, basis, enumerate_short
from exact_kmax import kmax

def milp_exists(n,k,bnd):
    K=k+1; r=n-K; c=[(-1)**(K-l)*comb(K,l) for l in range(K+1)]
    T=np.zeros((n,r))
    for i in range(r):
        for l,cl in enumerate(c): T[i+l,i]=cl
    for i0 in range(r):
        lb=np.full(r,-np.inf); ub=np.full(r,np.inf); lb[:i0]=0; ub[:i0]=0; lb[i0]=1
        res=milp(c=np.zeros(r),constraints=[LinearConstraint(T,-bnd,bnd)],integrality=np.ones(r),bounds=Bounds(lb,ub))
        if res.status==0:
            q=np.round(res.x).astype(int); v=[int(sum(q[i]*T[j,i] for i in range(r))) for j in range(n)]
            if max(map(abs,v))<=bnd and any(v): return v
    return None

def enum_F1(n,k,bnd):
    B=lll(basis(n,k)); hit=[None]
    def cb(x,v):
        if max(map(abs,v))<=bnd: hit[0]=v; return True
        return False
    enumerate_short(B,n*bnd*bnd,cb); return hit[0]

for n in range(14,31):
    bnd=n*n*(n-1)//2
    k,_,_,_=kmax(n,n-2)
    for kk in (k+1,k):
        if kk>n-2: continue
        a=milp_exists(n,kk,bnd); b=enum_F1(n,kk,bnd)
        print(n,"level",kk,"MILP:",a is not None,"enum(F1):",b is not None,flush=True)
