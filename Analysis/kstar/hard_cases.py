import json, sys, time
from realise_c import realise_c
from kstar_exact import candidates, moments_ok
from exact_kmax import kmax
from realise import check
res=json.load(open("kstar_witnesses.json"))
for n in map(int, sys.argv[1:]):
    k,_,_,_=kmax(n,n-2); bnd=n*n*(n-1)//2
    g=candidates(n,k,bnd)[0]
    t=time.time()
    sq=realise_c(g, seeds=range(48), iters=3_000_000_000, T0s=(15,25,40))
    ok = sq is not None and check(sq,g,[0]*n) and moments_ok(g,k) and not moments_ok(g,k+1)
    print(n,"OK" if ok else "fail", round(time.time()-t),flush=True)
    if ok:
        res[str(n)].update(kstar=k+1,gamma=g,supnorm=max(map(abs,g)),square=sq)
        json.dump(res,open("kstar_witnesses.json","w"))
