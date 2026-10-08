import subprocess
from concurrent.futures import ThreadPoolExecutor
from realise import start_square, check
def _run(args, inp):
    return subprocess.run(args,input=inp,capture_output=True,text=True).stdout
def realise_c(gamma, rho=None, seeds=range(16), iters=None, T0s=(20,50)):
    n=len(gamma); S=start_square(n)
    if rho is None: rho=[0]*n
    if iters is None: iters=(1_000_000_000 if n>=26 else 100_000_000)
    inp=" ".join(str(v) for r in S for v in r)+"\n"+" ".join(map(str,gamma))+"\n"+" ".join(map(str,rho))+"\n"
    jobs=[(["./anneal2",str(n),str(sd),str(iters),str(T0)]) for sd in seeds for T0 in T0s]
    with ThreadPoolExecutor(8) as ex:
        for out in ex.map(lambda a:_run(a,inp), jobs):
            if not out.startswith("FAIL"):
                v=list(map(int,out.split())); sq=[v[i*n:(i+1)*n] for i in range(n)]
                if check(sq,gamma,rho): return sq
    return None
