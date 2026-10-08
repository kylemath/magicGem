"""For each n, find exactly the largest k such that Lambda_{n,k} contains a nonzero vector gamma that passes
the necessary column-feasibility tests:
  (F1) |gamma_j| <= n^2(n-1)/2
  (F2) for every p: sum of the p largest gamma_j <= p n (N - p n)/2   (and symmetric for the p smallest)
Any vector in an arrangement satisfying the degree-k conditions passes F1,F2.  Exact enumeration."""
import sys, json, time
from lattice import lll, basis, enumerate_short

def feasible(vec, n):
    N=n*n; bnd=n*n*(n-1)//2
    if max(abs(v) for v in vec) > bnd: return False
    s=sorted(vec, reverse=True)
    acc=0; acc2=0
    for p in range(1,n+1):
        acc+=s[p-1]; acc2+=s[n-p]
        lim = p*n*(N-p*n)//2  # p n (N-pn)/2 is an integer? check parity below
        if 2*acc > p*n*(N-p*n): return False
        if -2*acc2 > p*n*(N-p*n): return False
    return True

def R2(n):
    # any gamma passing F2 is majorized by v_p = n(N-(2p-1)n)/2, so ||gamma||_2^2 <= sum v_p^2 = n^5(n^2-1)/12
    return -(-n**5*(n*n-1)//12)

def kmax(n, kstart, maxcount=2_000_000):
    bnd=n*n*(n-1)//2
    res={}
    for k in range(n-2, 0, -1):
        if k > kstart: 
            continue
        B=lll(basis(n,k))
        found=[None]
        def cb(x,vec):
            if feasible(vec,n):
                found[0]=vec; return True
            return False
        t=time.time()
        try:
            cnt=enumerate_short(B, R2(n), cb, limit=maxcount)
        except RuntimeError:
            return k, None, 'enumeration limit hit', res
        res[k]=dict(found=found[0], visited=cnt, sec=round(time.time()-t,2))
        if found[0] is not None:
            return k, found[0], 'ok', res
    return 0,None,'none',res

if __name__=="__main__":
    out={}
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    for n in range(lo,hi+1):
        k,vec,status,res=kmax(n,n-2)
        print(n,"kmax",k,status,"vec",vec, {kk:(v['visited'],v['sec']) for kk,v in res.items()},flush=True)
        out[n]=dict(kmax=k,status=status,vec=vec,log={kk:(v['visited'],v['sec']) for kk,v in res.items()})
    json.dump(out,open(f"exact_kmax_{lo}_{hi}.json","w"),indent=1)
