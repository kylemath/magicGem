import numpy as np, itertools, sys
def geom(n):
    j=np.tile(np.arange(n),n); i=np.repeat(np.arange(n),n)
    x=j-(n-1)/2; y=(n-1)/2-i
    L=[]
    for k in range(n): L.append((i==k)*1.)
    for k in range(n): L.append((j==k)*1.)
    L.append((i==j)*1.); L.append((i+j==n-1)*1.)
    return x,y,np.array(L)
def funcs(S,n):
    """S: (m,N) arrays of values 1..N. returns dict of functionals + E."""
    N=n*n; x,y,L=geom(n); z=S-(N+1)/2
    E=(np.einsum('mc,lc->ml',z,L)**2).sum(1)/N**2           # E_full in Cov units
    out={'E':E}
    lin=np.stack([np.einsum('mc,c->m',z,x),np.einsum('mc,c->m',z,y)],1)
    out['lin_|sum z(x,y)|']=np.linalg.norm(lin,axis=1)
    out['cross_sum z xy']=np.abs(np.einsum('mc,c->m',z,x*y))
    out['inertia_sum z(x2+y2)']=np.abs(np.einsum('mc,c->m',z,x**2+y**2))  # Loly-type (centred z)
    r=np.sqrt(x**2+y**2); rr=np.where(r>0,r,1)
    uh=np.stack([x/rr,y/rr],1)*(r>0)[:,None]
    for name,m in (('z',z),('s',S)):
        out[f'unit2D_m={name}']=np.linalg.norm(np.einsum('mc,cd->md',m,uh),axis=1)
        v=np.stack([x,y],0)  # 3D unit with z as height (scale 1)
        nrm=np.sqrt(x**2+y**2+z**2); nrm=np.where(nrm>0,nrm,1)
        B3=np.stack([(m*x/nrm).sum(1),(m*y/nrm).sum(1),(m*z/nrm).sum(1)],1)
        out[f'unit3D_m={name}_full']=np.linalg.norm(B3,axis=1)
        out[f'unit3D_m={name}_xy']=np.linalg.norm(B3[:,:2],axis=1)
        for c in (1.0,):
            nr=np.sqrt(x**2+y**2+c**2)  # fixed height direction (cell-position unit vectors)
            out[f'fixedc{c}_m={name}']=np.linalg.norm(np.stack([(m*x/nr).sum(1),(m*y/nr).sum(1)],1),axis=1)
    return out
def magic4():
    A=np.loadtxt('all7040.txt',dtype=int)
    seen={};
    for a in A:
        g=a.reshape(4,4); forms=[]
        for k in range(4):
            r=np.rot90(g,k); forms+= [tuple(r.ravel()),tuple(r.T.ravel())]
        seen[min(forms)]=1
    return np.array(list(seen.keys()))
