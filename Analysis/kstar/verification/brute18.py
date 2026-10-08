import numpy as np
from math import comb
n=18;K=16;N=n*n;Bd=n*n*(n-1)//2
c=np.array([(-1)**(K-l)*comb(K,l) for l in range(K+1)],dtype=np.int64)
v0=np.zeros(n,np.int64);v0[:K+1]=c; v1=np.zeros(n,np.int64);v1[1:K+2]=c
hits=0
a=np.arange(-Bd,Bd+1,dtype=np.int64)
for b in range(0,Bd+1):
    G=a[:,None]*v0[None,:]+b*v1[None,:]
    ok=np.abs(G).max(1)<=Bd
    if b==0: ok&=(a>0)
    hits+=ok.sum()
print('n=18 level 15: nonzero gamma (up to sign) with F1:',hits)
