# exact: for 18<=n<=170, level n-3: gamma=(t-1)^{n-2}(a+bt). Find all nonzero (a,b) with |gamma_j|<=B (F1), then test F2.
from math import comb
from fractions import Fraction as Fr
import sys
sys.path.insert(0,'.')
from milp_ub import F12
def cdiv(p,q): return -((-p)//q)
res=[]
for n in range(14,171):
    K=n-2; B=n*n*(n-1)//2
    c=[(-1)**(K-l)*comb(K,l) for l in range(K+1)]
    col=lambda j:(c[j] if 0<=j<=K else 0, c[j-1] if 0<=j-1<=K else 0)  # gamma_j = a*col0 + b*col1
    # bound b using two middle strips: solve linear system, |b| <= B(|u0|+|v0|)/|det|
    j=K//2; (p,q),(r,s)=col(j),col(j+1); det=p*s-q*r
    bmax=(B*(abs(p)+abs(r)))//abs(det)+1
    hits=[]
    for b in range(0,bmax+1):
        lo,hi=-B,B
        for jj in range(n):
            u,v=col(jj)
            if u==0:
                if abs(v*b)>B: lo,hi=1,0
                continue
            # |u a + v b| <= B
            L,H=(-B-v*b),(B-v*b)
            if u>0: lo=max(lo,cdiv(L,u)); hi=min(hi,H//u)
            else: lo=max(lo,cdiv(H,u)); hi=min(hi,L//u)
        for a in range(lo,hi+1):
            if b==0 and a<=0: continue
            g=[a*col(jj)[0]+b*col(jj)[1] for jj in range(n)]
            hits.append((a,b,F12(g,n)))
    res.append((n,len(hits),sum(h[2] for h in hits)))
print('n, #F1-feasible nonzero (up to sign), #F1F2-feasible at level n-3:')
print([r for r in res if r[1]])
print('n>=18 with F1F2-feasible at level n-3:',[r[0] for r in res if r[0]>=18 and r[2]])
