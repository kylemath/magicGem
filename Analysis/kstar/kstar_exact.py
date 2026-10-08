"""Exact k*(n) for 14 <= n <= NMAX:
 upper: no nonzero vector of Lambda_{n,kmax+1} passes the column-feasibility tests (exact enumeration)
 lower: an explicit arrangement with all row sums M(n) and column deviations gamma in Lambda_{n,kmax}\{0}
        (degree-kmax conditions, not semi-magic), verified in exact integer arithmetic.
Writes kstar_witnesses.json."""
import sys, json, time
from math import comb
from lattice import lll, basis, enumerate_short
from exact_kmax import feasible, kmax
from realise import realise, check
from realise_c import realise_c

def candidates(n,k,bnd):
    B=lll(basis(n,k)); out=[]
    enumerate_short(B, n*bnd*bnd, lambda x,v:(out.append(v) if feasible(v,n) else None, False)[1])
    out.sort(key=lambda v:(max(abs(a) for a in v), sum(abs(a) for a in v)))
    return out

def moments_ok(g,k):
    # sum_j C(j,r) g_j = 0 for r=0..k  <=>  (t-1)^{k+1} | P_g  <=> degree-k conditions
    return all(sum(comb(j,r)*g[j] for j in range(len(g)))==0 for r in range(k+1))

if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    res={}
    try: res=json.load(open("kstar_witnesses.json"))
    except Exception: pass
    for n in range(lo,hi+1):
        t=time.time()
        bnd=n*n*(n-1)//2
        k,vec,status,log=kmax(n,n-2)
        assert status=='ok'
        cands=candidates(n,k,bnd)
        S=None
        for ci,g in enumerate(cands[:4]):
            for seed in range(2):
                S=realise(g,seed=seed,maxit=3000)
                if S is not None: break
            if S is None:
                S=realise_c(g)
            if S is not None: break
        ok = S is not None and check(S,g,[0]*n) and moments_ok(g,k) and not moments_ok(g,k+1)
        res[str(n)]=dict(n=n, kmax=k, kstar=(k+1 if ok else None), kstar_upper=k+1,
                        gamma=g if ok else None, supnorm=max(abs(a) for a in g) if ok else None,
                        bound=bnd, n_candidates=len(cands), square=S if ok else None,
                        upper_log={str(a):b for a,b in log.items() if True} if False else None)
        print(n,"k*<=",k+1,"witness" if ok else "NO WITNESS", "sup",res[str(n)]['supnorm'],"bound",bnd,
              "ncand",len(cands), round(time.time()-t,1),"s",flush=True)
        json.dump(res,open("kstar_witnesses.json","w"))
