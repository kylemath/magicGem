# independent implementation of the twin-row squares (Lemma 3 even n, Lemma 5/Cor 6 odd n)
from itertools import combinations
def check_semimagic(S):
    n=len(S);N=n*n;M=n*(N+1)//2
    assert sorted(v for r in S for v in r)==list(range(1,N+1))
    assert all(sum(r)==M for r in S) and all(sum(S[i][j] for i in range(n))==M for j in range(n))
def even(n):
    m=n//2;N=n*n
    rows=[[] for _ in range(m)]  # list of (index x, sign)
    if m%2==0:
        for t in range(m*m):
            r=t//m; s=1 if (t%m)%2==0 else -1
            rows[r]+= [(2*t,s),(2*t+1,-s)]
    else:
        assert m>=7
        used=set()
        for r in range(m):
            rows[r]+= [(4*r,1),(4*r+1,1),(4*r+2,1),(4*r+3,-1)]
            a=5*m-1-r; b=5*m+7*r; rows[r]+=[(a,1),(b,-1)]
            used|={4*r,4*r+1,4*r+2,4*r+3,a,b}
        rest=[x for x in range(2*m*m) if x not in used]
        doms=[]
        i=0
        while i<len(rest):
            assert rest[i+1]==rest[i]+1; doms.append(rest[i]); i+=2
        assert len(doms)==m*(m-3)
        for r in range(m):
            for q in range(m-3):
                x=doms[r*(m-3)+q]; s=1 if q%2==0 else -1
                rows[r]+=[(x,s),(x+1,-s)]
    S=[[0]*n for _ in range(n)]
    for r in range(m):
        assert len(rows[r])==n
        for j,(x,s) in enumerate(rows[r]):
            w=2*x+1; v=(N+1+s*w)//2
            S[r][j]=v; S[m+r][j]=N+1-v
    check_semimagic(S)
    for r in range(m): assert all(S[r][j]+S[m+r][j]==N+1 for j in range(n))
    return S
def subset_with_sum(I,k,target):
    # greedy: start with k smallest, increase (Lemma 4)
    X=list(I[:k]); s=sum(X)
    if not (s<=target<=sum(I[-k:])): return None
    # raise elements from the top
    Iset=set(I)
    while s<target:
        for idx in range(k-1,-1,-1):
            if X[idx]+1 in Iset and X[idx]+1 not in X:
                X[idx]+=1; s+=1; break
        else: return None
    return X
def border(T):
    n=len(T)+2; m=(n-1)//2; N=n*n; c=(N+1)//2; A=4*m; B=4*m-2
    S=[[0]*n for _ in range(n)]
    for i in range(n-2):
        for j in range(n-2): S[i+1][j+1]=T[i][j]+2*n-2
    S[0][0]=N+1-A; S[n-1][n-1]=A; S[0][n-1]=B; S[n-1][0]=N+1-B
    P=[p for p in range(2*m,4*m+1) if p not in (A,B)]; Q=list(range(1,2*m))
    I=list(range(2*m,4*m-2)); target=c-A+B
    Tp=Tm=None
    for sm in range(m*(m-1)//2, 3*m*(m-1)//2+1):
        Tm=subset_with_sum(Q,m-1,sm)
        if Tm is None: continue
        Tp=subset_with_sum(I,m,target+sm)
        if Tp is not None: break
    assert Tp is not None and sum(Tp)-sum(Tm)==target
    top=[N+1-p for p in Tp]+list(Tm)
    left=[N+1-p for p in P if p not in Tp]+[p for p in Q if p not in Tm]
    assert len(top)==n-2 and len(left)==n-2
    for j in range(n-2): S[0][j+1]=top[j]; S[n-1][j+1]=N+1-top[j]
    for i in range(n-2): S[i+1][0]=left[i]; S[i+1][n-1]=N+1-left[i]
    check_semimagic(S); return S
def odd(n):
    # de la Loubere 7x7
    k=7;S=[[0]*k for _ in range(k)];i,j=0,k//2
    for v in range(1,k*k+1):
        S[i][j]=v; ni,nj=(i-1)%k,(j+1)%k
        if S[ni][nj]: ni,nj=(i+1)%k,j
        i,j=ni,nj
    check_semimagic(S)
    while len(S)<n: S=border(S)
    N=n*n
    for l in range((n-9)//2+1):
        assert all(S[l][j]+S[n-1-l][j]==N+1 for j in range(l+1,n-1-l)),(n,l)
    return S
ok=[]
for n in range(4,121,4): even(n); ok.append(n)
for n in range(14,121,4): even(n); ok.append(n)
for n in range(9,122,2): odd(n); ok.append(n)
print('verified twin squares for',len(ok),'orders up to 121:',sorted(ok)[:12],'...')
