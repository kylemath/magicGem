import numpy as np, itertools
from fractions import Fraction as F
# 1. Var(I) closed form vs direct Wald-Wolfowitz for n=3..8
for n in range(3,9):
    N=n*n; xs=np.array([j-(n-1)/2 for i in range(n) for j in range(n)]); ys=np.array([(n-1)/2-i for i in range(n) for j in range(n)])
    r2=xs**2+ys**2; vals=np.arange(1,N+1)
    var=F(1,N-1)*F(str(((r2-r2.mean())**2).sum()))*F(str(((vals-vals.mean())**2).sum()))
    cf=F(n**4*(n**4-1)*(n*n-4),1080)
    print(n, var, cf, var==cf)
# 2. n=4 Monte Carlo independent: mean, var, fraction at 340
rng=np.random.default_rng(7); n=4;N=16
xs=np.array([j-1.5 for i in range(4) for j in range(4)]); ys=np.array([1.5-i for i in range(4) for j in range(4)]); r2=xs**2+ys**2
M=4_000_000; tot=0; tot2=0; hit=0
for _ in range(4):
    P=np.argsort(rng.random((M,16)),axis=1)+1
    I=P@r2; tot+=I.sum(); tot2+=(I**2).sum(); hit+=(np.abs(I-340)<1e-9).sum()
S=4*M; mean=tot/S; var=tot2/S-mean**2
print("n=4 MC: mean",mean,"var",var,"exact 725.333; frac I=340:",hit/S)
