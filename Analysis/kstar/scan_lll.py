from lattice import lll_best_sup
import sys
for n in range(14, 41):
    bnd = n*n*(n-1)//2
    row=[]
    kfirst=None
    for k in range(n-2, 0, -1):
        s,_ = lll_best_sup(n,k)
        if s <= bnd:
            kfirst=k; break
    print(n, "bound", bnd, "largest k with LLL vector <= bound:", kfirst, "sup", s, flush=True)
