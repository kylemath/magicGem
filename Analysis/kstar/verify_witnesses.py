"""Independent exact verification of kstar_witnesses.json: for each n the stored arrangement
 - is a permutation of 1..n^2, all row sums M(n), column deviations gamma != 0,
 - satisfies the degree-k conditions sum_j x_j^m gamma_j = 0, 1<=m<=k (x_j = j-(n-1)/2, exact Fractions),
   rows trivially (rho=0), and violates the degree-(k+1) column condition;
so k*(n) >= k+1.  Combined with the enumeration (upper bound k*(n) <= k+1) this gives k*(n)=k+1."""
import json
from fractions import Fraction as F
d=json.load(open("kstar_witnesses.json"))
rows=[]
for key in sorted(d,key=int):
    r=d[key]; n=r['n']; k=r['kmax']; S=r['square']; N=n*n; M=n*(N+1)//2
    assert S is not None, n
    assert sorted(v for row in S for v in row)==list(range(1,N+1))
    assert all(sum(row)==M for row in S)
    g=[sum(S[i][j] for i in range(n))-M for j in range(n)]
    assert g==r['gamma'] and any(g)
    x=[F(2*j-(n-1),2) for j in range(n)]
    assert all(sum(x[j]**m*g[j] for j in range(n))==0 for m in range(0,k+1))
    assert sum(x[j]**(k+1)*g[j] for j in range(n))!=0
    rows.append((n,k+1,max(map(abs,g)),n*n*(n-1)//2))
print("n  k*(n)  max|gamma_j|  bound n^2(n-1)/2")
for t in rows: print(*t)
print("all",len(rows),"witnesses verified")
