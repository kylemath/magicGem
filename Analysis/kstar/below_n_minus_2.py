"""k*(n) <= n-3 for 18 <= n <= 170: Lambda_{n,n-3} (rank 2) has no nonzero vector passing F1-F2 (exact enumeration)."""
from lattice import lll, basis, enumerate_short
from exact_kmax import feasible, R2
bad=[]
for n in range(18,171):
    B=lll(basis(n,n-3)); hit=[None]
    enumerate_short(B,R2(n),lambda x,v:(hit.__setitem__(0,v) if feasible(v,n) else None, hit[0] is not None)[1])
    if hit[0] is not None: bad.append(n)
print("n in [18,170] where level n-3 is NOT excluded:",bad)
