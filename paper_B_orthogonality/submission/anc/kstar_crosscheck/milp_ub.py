# Independent cross-check of the upper bounds: MILP (HiGHS) over integer combinations of a reduced basis of
# Lambda_{n,k} = {gamma in Z^n : sum_j C(j,r) gamma_j = 0, r=0..k}, with F1 and F2 (all p, both sides, via LP duality).
import sys, json, numpy as np
from math import comb
from scipy.optimize import milp, LinearConstraint, Bounds
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix

def lattice_basis(n,k):
    # integer kernel basis of the (k+1) x n binomial-moment matrix, via Hermite/Smith-free route:
    # rows t^i (t-1)^{k+1}  (constructed here from the moment definition, then checked)
    K=k+1; r=n-K
    B=[[0]*n for _ in range(r)]
    for i in range(r):
        for l in range(K+1): B[i][i+l]=(-1)**(K-l)*comb(K,l)
    for b in B:
        assert all(sum(comb(j,s)*b[j] for j in range(n))==0 for s in range(K))
    # saturation check: lattice spanned = full kernel lattice iff gcd of maximal minors of B is 1;
    # B is in echelon form with leading entries (-1)^K -> unimodular-triangular, so it is saturated.
    D=DomainMatrix([[ZZ(x) for x in row] for row in B],(r,n),ZZ).lll()
    R=[[int(x) for x in row] for row in D.to_Matrix().tolist()]
    # verify R spans same lattice: R = U B with U integer unimodular
    U=Matrix(R)*Matrix(B).T*(Matrix(B)*Matrix(B).T).inv()
    assert all(x.is_integer for x in U) and abs(U.det())==1 and Matrix(R)==U*Matrix(B)
    return R

def exists(n,k):
    N=n*n; Bd=n*n*(n-1)//2
    R=np.array(lattice_basis(n,k),dtype=float); r=R.shape[0]
    if r==0: return None
    P=list(range(1,n))
    # variables: y (r ints), lam_p, mu_pj (upper side), lam2_p, mu2_pj (lower side)
    nv=r+2*(len(P)+len(P)*n)
    def idx_l(s,p): return r+s*(len(P)+len(P)*n)+(p-1)
    def idx_m(s,p,j): return r+s*(len(P)+len(P)*n)+len(P)+(p-1)*n+j
    A=[];lo=[];hi=[]
    for j in range(n):  # F1: |gamma_j|<=Bd
        row=np.zeros(nv); row[:r]=R[:,j]; A.append(row); lo.append(-Bd); hi.append(Bd)
    for s,sg in ((0,1),(1,-1)):
        for p in P:
            bp=p*n*(N-p*n)/2
            row=np.zeros(nv); row[idx_l(s,p)]=p
            for j in range(n): row[idx_m(s,p,j)]=1
            A.append(row); lo.append(-np.inf); hi.append(bp)
            for j in range(n):  # mu >= sg*gamma_j - lam
                row=np.zeros(nv); row[idx_m(s,p,j)]=1; row[idx_l(s,p)]=1; row[:r]=-sg*R[:,j]
                A.append(row); lo.append(0); hi.append(np.inf)
    A=np.array(A)
    integ=np.zeros(nv); integ[:r]=1
    for i0 in range(r):
        lb=np.full(nv,-np.inf); ub=np.full(nv,np.inf)
        lb[r:]=-np.inf
        for s in (0,1):
            for p in P:
                for j in range(n): lb[idx_m(s,p,j)]=0
        lb[:i0]=0; ub[:i0]=0; lb[i0]=1
        res=milp(c=np.zeros(nv),constraints=[LinearConstraint(A,lo,hi)],integrality=integ,bounds=Bounds(lb,ub),options={'time_limit':600})
        if res.status==0:
            y=np.round(res.x[:r]).astype(int)
            g=[int(sum(int(y[i])*int(R[i][j]) for i in range(r))) for j in range(n)]
            return g
        if res.status not in (2,):
            return 'status%d'%res.status
    return None

def F12(g,n):
    N=n*n
    if max(map(abs,g))>n*n*(n-1)//2: return False
    s=sorted(g,reverse=True)
    for p in range(1,n+1):
        if 2*sum(s[:p])>p*n*(N-p*n) or -2*sum(s[-p:])>p*n*(N-p*n): return False
    return True

if __name__=="__main__":
    ks=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','kstar_witnesses.json')))
    for n in map(int,sys.argv[1:]):
        kst=int(ks[str(n)]['kstar'])
        a=exists(n,kst)      # should be None (no feasible gamma at degree k*)
        b=exists(n,kst-1)    # should exist
        print(n,'k*',kst,'level k* feasible?',a,'| level k*-1 feasible vec found:',None if b is None or isinstance(b,str) else (F12(b,n),max(map(abs,b)))  ,flush=True)
