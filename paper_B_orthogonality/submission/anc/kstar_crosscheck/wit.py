import json
from fractions import Fraction as F
from math import comb
d=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','kstar_witnesses.json')))
for key in sorted(d,key=int):
    r=d[key]; n=int(r['n']); S=r['square']; N=n*n; M=n*(N+1)//2
    flat=[v for row in S for v in row]
    assert len(S)==n and all(len(row)==n for row in S)
    assert sorted(flat)==list(range(1,N+1)), n
    rho=[sum(row)-M for row in S]; g=[sum(S[i][j] for i in range(n))-M for j in range(n)]
    # multiplicity at 1 via binomial moments (independent of x_j powers)
    def mult(v):
        m=0
        while m<n and sum(comb(j,m)*v[j] for j in range(n))==0: m+=1
        return m
    mg=mult(g); mr=mult(rho) if any(rho) else 99
    # degree-k conditions directly with powers of x_j=j-(n-1)/2 for k=claimed
    kc=int(r['kstar'])-1
    x=[F(2*j-(n-1),2) for j in range(n)]
    degk=all(sum(x[j]**m*g[j] for j in range(n))==0 for m in range(1,kc+1)) and all(sum(F(n-1-2*i,2)**m*rho[i] for i in range(n))==0 for m in range(1,kc+1))
    print(n,'claimed k*',r['kstar'],'mult_gamma',mg,'rho==0',not any(rho),'mult_rho',mr,'gamma!=0',any(g),'deg-(k*-1) holds',degk,'=>k*>=',mg, 'maxabs',max(map(abs,g)), 'gamma matches json', g==(r['gamma'] if isinstance(r['gamma'],list) else json.loads(r['gamma'])))
