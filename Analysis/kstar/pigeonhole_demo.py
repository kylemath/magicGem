"""Demonstrate the box-principle mechanism concretely: random twin-swap choices, find two with equal
moments, build the arrangement and verify it satisfies the degree-(K-1) conditions without being semi-magic."""
import random, sys
from math import comb
from fractions import Fraction as F
from constructions import construct
n=int(sys.argv[1]); K=int(sys.argv[2])
s,twins=construct(n); N=n*n; M=n*(N+1)//2
j0=0 if n%2==0 else 1
pairs=[]
for q in range((n-j0)//2):
    j=j0+2*q
    if j+1>=n: break
    tp=[(i,ip) for (i,ip),cols in twins if j in cols and j+1 in cols]
    pairs.append((j,tp))
rng=random.Random(0); seen={}
while True:
    choice=tuple(tuple(rng.random()<0.5 for _ in tp) for j,tp in pairs)
    g=[sum(s[i][j+1]-s[i][j] for (i,ip),c in zip(tp,ch) if c) for (j,tp),ch in zip(pairs,choice)]
    key=tuple(sum(g[q]*comb(q,r) for q in range(len(g))) for r in range(K-1))
    if key in seen and seen[key][1]!=g: break
    seen[key]=(choice,g)
c2,g2=seen[key]
S=[row[:] for row in s]
for (j,tp),a,b in zip(pairs,choice,c2):
    for (i,ip),x,y in zip(tp,a,b):
        if x and not y: S[i][j],S[i][j+1]=S[i][j+1],S[i][j]        # +d
        if y and not x: S[ip][j],S[ip][j+1]=S[ip][j+1],S[ip][j]    # -d
gam=[sum(S[i][j] for i in range(n))-M for j in range(n)]
assert all(sum(r)==M for r in S) and sorted(v for r in S for v in r)==list(range(1,N+1))
x=[F(2*j-(n-1),2) for j in range(n)]
deg=max(k for k in range(0,n) if all(sum(x[j]**m*gam[j] for j in range(n))==0 for m in range(k+1)))
print("n",n,"samples",len(seen),"gamma",gam,"degree conditions hold up to k =",deg,"(target K-1 =",K-1,")")
