import numpy as np, itertools, json
from bv import *
from scipy.stats import spearmanr
rng=np.random.default_rng(0)
rep=[]
# n=3 exhaustive
P=np.array(list(itertools.permutations(range(1,10))),float)
f=funcs(P,3); E=f['E']; mag=E<1e-12
semi=None
rep.append(f"n=3: {len(P)} perms, magic (E=0): {mag.sum()}")
for k,v in f.items():
    if k=='E':continue
    rho=spearmanr(E,v)[0]
    rep.append(f"  {k:28s} magic: min={v[mag].min():.4f} max={v[mag].max():.4f} | all mean={v.mean():.3f} min={v.min():.4f} | frac of perms with B<=max_magic={np.mean(v<=v[mag].max()+1e-12):.4f} | spearman(E,B)={rho:.3f}")
np.save('n3_E.npy',E); n3=f
# n=4
M=magic4().astype(float); rep.append(f"n=4: found {len(M)} magic squares")
R=np.array([rng.permutation(16)+1 for _ in range(300000)],float)
fm=funcs(M,4); fr=funcs(R,4)
rep.append(f"  E magic max={fm['E'].max():.2e}; random E mean={fr['E'].mean():.3f}, min={fr['E'].min():.4f}, frac random E=0: {np.mean(fr['E']<1e-12):.2e}")
for k in fm:
    if k=='E':continue
    a,b=fm[k],fr[k]
    rep.append(f"  {k:28s} magic mean={a.mean():.4f} (min {a.min():.4f} max {a.max():.4f}) | random mean={b.mean():.3f} p5={np.percentile(b,5):.3f} | frac random<= magic mean={np.mean(b<=a.mean()):.4f}, <=magic max={np.mean(b<=a.max()):.4f}")
# random semi-magic-ish: fraction of random with B exactly 0 for lin
rep.append(f"  random with lin B==0: {np.mean(fr['lin_|sum z(x,y)|']<1e-9):.2e}")
# theorem check: |sum z(x,y)|^2 <= N^2 * n(n^2-1)/12 * E_rc  (n=4)  ; compare with E_full
x,y,L=geom(4); N=16; n=4
z=R-(N+1)/2; Erc=(np.einsum('mc,lc->ml',z,L[:8])**2).sum(1)/N**2
lhs=np.einsum('mc,c->m',z,x)**2+np.einsum('mc,c->m',z,y)**2; rhs=N**2*n*(n**2-1)/12*Erc
rep.append(f"  theorem |sum z(x,y)|^2 <= N^2 n(n^2-1)/12 E_rc: violations={np.sum(lhs>rhs+1e-9)}, max ratio={np.max(lhs/np.maximum(rhs,1e-12)):.3f}")
# corr over random n=4
for k in fr:
    if k=='E':continue
    rep.append(f"  corr(E,{k}) random n=4: spearman={spearmanr(fr['E'][:100000],fr[k][:100000])[0]:.3f}")
# continuous gradient flow
def flow(z0,n,T=60,dt=None):
    x,y,L=geom(n);N=n*n
    G=L.T@L/N**2  # E=z^T G z, grad=2Gz
    w=np.linalg.eigvalsh(G).max(); dt=0.4/w
    # project onto centred space (E has no kernel issue; also keep sum 0)
    z=z0.copy(); tr=[]
    for t in range(T):
        zz=z[None]; S=zz+(N+1)/2
        f=funcs(S,n); tr.append([f['E'][0]]+[f[k][0] for k in f if k!='E'])
        z=z-dt*2*np.einsum('ab,b->a',G,z); z-=z.mean()
    return np.array(tr),[k for k in f if k!='E']
tr_all=[];
for s in range(60):
    p=rng.permutation(16)+1.; z0=p-8.5
    tr,names=flow(z0,4,T=150); tr_all.append(tr)
tr_all=np.array(tr_all); mean=tr_all.mean(0)
rep.append("gradient flow n=4 (60 random perm starts), mean over runs at t=0 and t=199 (E, then B's):")
for i,nm in enumerate(['E']+names): rep.append(f"  {nm:28s} t0={mean[0,i]:.4f} tEnd={mean[-1,i]:.5f}")
# baseline: projection of random z onto W-perp is the endpoint; compare with magic discrete
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,3,figsize=(15,4))
ax[0].scatter(n3['E'][::7],n3['lin_|sum z(x,y)|'][::7],s=2,alpha=.3,label='linear |Σz(x,y)|')
ax[0].scatter(n3['E'][::7],n3['unit2D_m=z'][::7],s=2,alpha=.3,label='unit2D, m=z')
ax[0].scatter(n3['E'][::7],n3['unit3D_m=z_xy'][::7],s=2,alpha=.3,label='unit3D xy, m=z')
ax[0].set_xlabel('E_full'); ax[0].set_ylabel('B'); ax[0].set_title('n=3 exhaustive (every 7th perm)'); ax[0].legend(markerscale=5)
for k in ['lin_|sum z(x,y)|','unit2D_m=z','unit3D_m=z_xy','fixedc1.0_m=z']:
    ax[1].hist(fr[k],bins=80,histtype='step',density=True,label=k+' random')
    ax[1].hist(fm[k],bins=20,histtype='step',density=True,linestyle='--',label=k+' magic')
ax[1].set_title('n=4: B for 880 magic (dashed) vs 3e5 random'); ax[1].legend(fontsize=5); ax[1].set_xlabel('B')
for i,nm in enumerate(['E']+names):
    if nm in('E','lin_|sum z(x,y)|','unit2D_m=z','unit3D_m=z_xy','fixedc1.0_m=z','cross_sum z xy'):
        ax[2].semilogy(tr_all[:,:,i].mean(0)+1e-12,label=nm)
ax[2].set_title('n=4 projected gradient flow of E_full (mean of 60)'); ax[2].set_xlabel('step'); ax[2].legend(fontsize=6)
plt.tight_layout(); plt.savefig('balance_overview.png',dpi=110)
open('results.txt','w').write("\n".join(rep)); print("\n".join(rep))
