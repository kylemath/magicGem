import sys, json, time; sys.dont_write_bytecode=True
import numpy as np
from multiprocessing import Pool
from hulllib import *

def work(args):
    n,cnt,seed,audit=args
    rng=np.random.default_rng(seed)
    N=n*n
    i,j=np.divmod(np.arange(N),n)
    X=2*j-(n-1); Y=(n-1)-2*i
    out=[]; deg=0; mism=0; n_aud=0; ext_ok=0
    for r in range(cnt):
        s=rng.permutation(N)+1
        P=np.stack([X,Y,2*s-(N+1)],1)
        try:
            v=qh_vertices(P)
        except QhullError:
            deg+=1; continue
        out.append(len(v))
        # points with s=1 and s=N must be vertices (unique z-extremes)
        sv=set(v.tolist())
        assert int(np.argmin(s)) in sv and int(np.argmax(s)) in sv
        ext_ok+=1
        if r<audit:
            n_aud+=1
            ev=exact_vertices(P)
            if set(ev.tolist())!=sv: mism+=1
    return n,out,deg,mism,n_aud,ext_ok

if __name__=='__main__':
    plan={}
    for n in range(3,17):
        plan[n]=100000 if n<=10 else 20000
    jobs=[]
    chunk=2500
    for n,tot in plan.items():
        for c in range(tot//chunk):
            jobs.append((n,chunk,n*100000+c,100))
    t=time.time()
    res={}
    with Pool(16) as p:
        for n,out,deg,mism,na,eo in p.imap_unordered(work,jobs):
            d=res.setdefault(n,dict(V=[],deg=0,mism=0,aud=0,extok=0))
            d['V']+=out; d['deg']+=deg; d['mism']+=mism; d['aud']+=na; d['extok']+=eo
    summ={}
    for n in sorted(res):
        V=np.array(res[n]['V']); N=n*n
        summ[n]=dict(samples=len(V),degenerate=res[n]['deg'],mean=float(V.mean()),sd=float(V.std(ddof=1)),min=int(V.min()),max=int(V.max()),
                     frac=float(V.mean()/N),qhull_vs_exact_mismatches=res[n]['mism'],audited=res[n]['aud'],
                     hist=np.bincount(V).tolist(),sem=float(V.std(ddof=1)/np.sqrt(len(V))))
        print(n,{k:summ[n][k] for k in ['samples','degenerate','mean','sd','min','max','frac','qhull_vs_exact_mismatches','audited']},flush=True)
    json.dump(summ,open('random_perm_hulls.json','w'))
    print('time',time.time()-t)
