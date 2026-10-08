import sys, json; sys.dont_write_bytecode=True
import numpy as np
from scipy import stats
from collections import Counter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from constructions import canon
from magic_hulls import load_sa, vinfo
R=json.load(open('random_perm_hulls.json')); M=json.load(open('magic_hulls.json'))
rep={}
# --- growth fits of E[V] for random perms
ns=np.array(sorted(int(k) for k in R)); N=ns**2; mu=np.array([R[str(n)]['mean'] for n in ns]); sem=np.array([R[str(n)]['sem'] for n in ns])
def fit(basis,name):
    A=np.stack([f(N) for f in basis],1)
    w=1/sem
    coef,*_=np.linalg.lstsq(A*w[:,None],mu*w,rcond=None)
    chi=(((A@coef-mu)/sem)**2).sum()
    return dict(name=name,coef=coef.tolist(),chi2=float(chi),dof=len(ns)-len(coef))
fits=[fit([lambda x:np.log(x)**2,lambda x:np.log(x),lambda x:1+0*x],'a ln^2 N + b ln N + c'),
      fit([lambda x:np.log(x),lambda x:1+0*x],'a ln N + b'),
      fit([lambda x:np.log(x)**2,lambda x:1+0*x],'a ln^2 N + b')]
# power law log-log
lc=np.polyfit(np.log(N),np.log(mu),1,w=mu/sem)
fits.append(dict(name='power law V ~ N^p',p=float(lc[0]),A=float(np.exp(lc[1]))))
# local exponent between consecutive
loc=[(int(ns[i]),int(ns[i+1]),float(np.log(mu[i+1]/mu[i])/np.log(N[i+1]/N[i]))) for i in range(len(ns)-1)]
rep['fits']=fits; rep['local_exponent']=loc
for f in fits: print(f)
print('local exponent',[ (a,b,round(e,3)) for a,b,e in loc])
# --- table
rows=[]
for n in range(3,9):
    r=R[str(n)]; row=dict(n=n,N=n*n,rand_mean=r['mean'],rand_sd=r['sd'],rand_sem=r['sem'],rand_frac=r['frac'],rand_samples=r['samples'])
    key={4:'EXACT4'}.get(n,f'SA{n}')
    if key in M:
        V=np.array(M[key]['V']); row.update(sa_label=key,sa_count=len(V),sa_mean=float(V.mean()),sa_sd=float(V.std(ddof=1)),sa_sem=float(V.std(ddof=1)/np.sqrt(len(V))),sa_frac=float(V.mean()/n**2),sa_min=int(V.min()),sa_max=int(V.max()))
        # two-sample tests: random sample reconstructed from hist
        rh=np.array(r['hist']); rv=np.repeat(np.arange(len(rh)),rh)
        row['t_z']=float((V.mean()-rv.mean())/np.sqrt(V.var(ddof=1)/len(V)+rv.var(ddof=1)/len(rv))) if n!=4 else None
        row['ks_p']=float(stats.ks_2samp(V,rv).pvalue)
        # chi-square-like total variation distance
        vs=max(rv.max(),V.max())+1
        a=np.bincount(V,minlength=vs)/len(V); b=np.bincount(rv,minlength=vs)/len(rv)
        row['tv_distance']=float(0.5*np.abs(a-b).sum())
    c=f'CONS{n}'
    if c in M:
        Vc=np.array(M[c]['V']); row.update(cons_count=len(Vc),cons_mean=float(Vc.mean()),cons_min=int(Vc.min()),cons_max=int(Vc.max()))
    rows.append(row)
rep['table']=rows
for r in rows: print({k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items()})
rep['siamese_V']=M['SIAM']
# --- bias check at n=4: raw SA frequency per class vs uniform over 880
sa=load_sa(4); cnt=Counter(canon(S) for S in sa)
SQ4=np.loadtxt('/Users/kylemathewson/magicGem/paper_A_gems/anc/squares880.txt',dtype=int).reshape(880,4,4)
from hulllib import grid_points, exact_vertices
Vof={canon(S):len(exact_vertices(grid_points(S))) for S in SQ4}
w=np.array([cnt[k] for k in Vof]); v=np.array([Vof[k] for k in Vof])
rep['bias_n4']=dict(draws=len(sa),classes_hit=len(cnt),uniform_mean=float(v.mean()),sa_weighted_mean=float((w*v).sum()/w.sum()),
  class_freq_min=int(w.min()),class_freq_max=int(w.max()),class_freq_cv=float(w.std()/w.mean()),
  chi2_uniform_p=float(stats.chisquare(w).pvalue))
print(rep['bias_n4'])
# V distribution tables n=4..8
rep['V_hist']={}
for n in range(4,9):
    key={4:'EXACT4'}.get(n,f'SA{n}')
    rep['V_hist'][n]=dict(magic=np.bincount(M[key]['V']).tolist(),random=R[str(n)]['hist'])
# mean number of cells with s in {1,N}: trivial. s=2,N-1 vertex fractions
rep['s2_vertex_frac']={k:M[k]['s2_vertex_frac'] for k in M if k!='SIAM'}
json.dump(rep,open('largen_report.json','w'),indent=1,default=str)
# --- plots
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
ax[0].errorbar(ns,mu,yerr=sem*5,fmt='o',label='random permutations (1e5 / 2e4 each)',color='C0')
xs=np.linspace(3,17,100); Ns=xs**2
c=fits[0]['coef']; ax[0].plot(xs,c[0]*np.log(Ns)**2+c[1]*np.log(Ns)+c[2],'-',color='C0',alpha=.6,label='fit a ln^2N+b lnN+c')
for key,lab,col in [('EXACT4','magic n=4 (all 880)','C3'),('SA5','magic SA','C2'),('SA6',None,'C2'),('SA7',None,'C2'),('SA8',None,'C2')]:
    n=int(key[-1]); V=np.array(M[key]['V']); ax[0].plot([n],[V.mean()],'s',color=col,label=lab,mfc='none',ms=9)
ax[0].plot([5,6,7],[M[f'CONS{n}']['V'] and np.mean(M[f'CONS{n}']['V']) for n in (5,6,7)],'^',color='C1',label='constructions (Siamese/Strachey/LUX)')
ax[0].plot(range(5,22,2),[M['SIAM'][str(n)] for n in range(5,22,2)],'x',color='k',label='Siamese gem V=12')
ax[0].set_xlabel('n (N=n^2 points)'); ax[0].set_ylabel('E[hull vertices]'); ax[0].legend(fontsize=7); ax[0].set_title('mean vertex count')
ax[1].semilogx(N,mu/N,'o-'); ax[1].set_xlabel('N=n^2'); ax[1].set_ylabel('E[V]/N'); ax[1].set_title('hull fraction')
plt.tight_layout(); plt.savefig('largen_growth.png',dpi=140)
fig,axs=plt.subplots(1,4,figsize=(14,3.3))
for a,n in zip(axs,[5,6,7,8]):
    key=f'SA{n}'; V=np.array(M[key]['V']); rh=np.array(R[str(n)]['hist']); rh=rh/rh.sum()
    bins=np.arange(0,max(len(rh),V.max()+1))
    a.bar(bins-0.2,np.bincount(V,minlength=len(bins))[:len(bins)]/len(V),0.4,label='magic (SA)')
    a.bar(bins+0.2,np.pad(rh,(0,len(bins)-len(rh)))[:len(bins)],0.4,label='random perm')
    a.axvline(12,color='k',ls=':'); a.set_title(f'n={n}'); a.set_xlim(8,max(V.max(),len(rh)-8) if n>5 else 28); a.set_xlabel('V')
axs[0].legend(fontsize=7); plt.tight_layout(); plt.savefig('largen_Vhist.png',dpi=140)
