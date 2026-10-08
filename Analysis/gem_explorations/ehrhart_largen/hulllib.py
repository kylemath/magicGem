import sys; sys.dont_write_bytecode=True
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial import QhullError

def grid_points(S):
    """doubled integer coordinates (x,y,z) = 2p, as in gem_geometry.scaled_points"""
    S=np.asarray(S,dtype=np.int64); n=S.shape[0]; N=n*n
    i,j=np.divmod(np.arange(N),n)
    return np.stack([2*j-(n-1),(n-1)-2*i,2*S.ravel()-(N+1)],1)

def qh_vertices(P):
    return ConvexHull(P.astype(float)).vertices

def exact_vertices(P):
    """exact extreme points (integer arithmetic) using qhull only to propose facets.
    Raises AssertionError if qhull facets are inconsistent with exact arithmetic."""
    N=len(P)
    H=ConvexHull(P.astype(float))
    s=H.simplices
    p0,p1,p2=P[s[:,0]],P[s[:,1]],P[s[:,2]]
    nrm=np.cross(p1-p0,p2-p0)
    g=np.gcd.reduce(np.abs(nrm),axis=1)
    ok=g>0
    nrm=nrm[ok]//g[ok,None]; p0=p0[ok]
    d=-(nrm*p0).sum(1)
    val=nrm@P.sum(0)+d*N
    flip=val>0
    nrm[flip]*=-1; d[flip]*=-1
    pl=np.unique(np.concatenate([nrm,d[:,None]],1),axis=0)
    vals=P@pl[:,:3].T+pl[:,3]
    assert (vals<=0).all()
    cnt=(vals==0).sum(1)
    return np.nonzero(cnt>=3)[0]
