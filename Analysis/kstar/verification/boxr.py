import sys, itertools
from math import comb, prod
from sympy import Matrix
sys.path.insert(0,'.')
from milp_ub import F12
def cdiv(p,q): return -((-p)//q)
def run(n,k,go=True):
    K=k+1; r=n-K; B=n*n*(n-1)//2
    c=[(-1)**(K-l)*comb(K,l) for l in range(K+1)]
    G=[[c[j-i] if 0<=j-i<=K else 0 for i in range(r)] for j in range(n)]  # gamma_j = sum_i G[j][i] y_i
    best=None
    for j0 in range(0,n-r+1):
        Ms=Matrix([G[j] for j in range(j0,j0+r)])
        if Ms.det()==0: continue
        Mi=Ms.inv()
        rng=[int(B*sum(abs(Mi[i,l]) for l in range(r)))+1 for i in range(r)]
        size=prod(2*x+1 for x in rng[1:])
        if best is None or size<best[0]: best=(size,rng)
    size,rng=best
    print(n,k,'rank',r,'box for y1..',rng[1:],'size',size,flush=True)
    if not go: return
    hits=[]
    for ys in itertools.product(*[range(-x,x+1) for x in rng[1:]]):
        lo,hi=-rng[0],rng[0]
        for j in range(n):
            u=G[j][0]; v=sum(G[j][i]*ys[i-1] for i in range(1,r))
            if u==0:
                if abs(v)>B: lo,hi=1,0; break
                continue
            L,H=-B-v,B-v
            if u>0: lo=max(lo,cdiv(L,u)); hi=min(hi,H//u)
            else: lo=max(lo,cdiv(H,u)); hi=min(hi,L//u)
            if lo>hi: break
        for a in range(lo,hi+1):
            y=(a,)+ys
            if not any(y): continue
            g=[sum(G[j][i]*y[i] for i in range(r)) for j in range(n)]
            hits.append(F12(g,n))
    print('  F1-feasible nonzero (both signs):',len(hits),' F1F2-feasible:',sum(hits),flush=True)
for n,k in [(20,16),(20,15),(19,16),(21,17),(22,17),(26,19),(26,18)]:
    run(n,k,go=False)
