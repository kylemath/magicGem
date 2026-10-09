"""Rigorous upper bounds k*(n) <= kmax(n)+1 by exact lattice enumeration (column feasibility tests F1,F2)."""
import json, sys, time
from multiprocessing import Pool
from exact_kmax import kmax
def one(n):
    t=time.time()
    k,vec,status,log=kmax(n,n-2,maxcount=50_000_000)
    return n,dict(kmax=k,status=status,upper=k+1,vec=vec,sec=round(time.time()-t,1))
if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    out={}
    with Pool(14) as p:
        for n,r in p.imap_unordered(one, range(lo,hi+1)):
            out[n]=r; print(n,"k*<=",r['upper'],r['status'],r['sec'],flush=True)
            json.dump(out,open(f"upper_scan_{lo}_{hi}.json","w"))
