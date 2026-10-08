import numpy as np
from bv import *
rng=np.random.default_rng(1); n=4;N=16
x,y,L=geom(n); G=np.einsum('la,lb->ab',L,L)/N**2
dt=0.4/np.linalg.eigvalsh(G).max()
def B(z):
    r=np.sqrt(x**2+y**2); u=np.stack([x/r,y/r],1)
    return np.linalg.norm(np.einsum('c,cd->d',z,u))
def Bn(z):
    return B(z)/np.linalg.norm(z)
# W-perp projection of z0: endpoint; compare with magic squares and random z restricted to W-perp
M=magic4().astype(float)-8.5
print("magic unit2D B / |z|:",np.mean([Bn(m) for m in M]))
T=300;res0=[];res1=[];ep=[]
for s in range(200):
    z=rng.permutation(16)-7.5; z0=z.copy()
    for t in range(T): z=z-dt*2*np.einsum('ab,b->a',G,z); z-=z.mean()
    res0.append(Bn(z0)); res1.append(Bn(z)); ep.append(np.linalg.norm(z)/np.linalg.norm(z0))
print("random perm  B/|z|:",np.mean(res0)," after flow:",np.mean(res1)," |z| ratio:",np.mean(ep))
# random vectors in Wperp (Gaussian) baseline
w,V=np.linalg.eigh(G); K=V[:,w<1e-12]; print("dim W-perp:",K.shape[1])
print("random Gaussian in W-perp B/|z|:",np.mean([Bn(K@rng.normal(size=K.shape[1])) for _ in range(2000)]))
