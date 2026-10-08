import sys, itertools; sys.dont_write_bytecode=True
import numpy as np

def is_magic(S):
    S=np.asarray(S); n=S.shape[0]; M=n*(n*n+1)//2
    return (sorted(S.ravel().tolist())==list(range(1,n*n+1)) and (S.sum(0)==M).all() and (S.sum(1)==M).all()
            and np.trace(S)==M and np.trace(np.fliplr(S))==M)

def d4(S):
    out=[];T=np.asarray(S)
    for _ in range(4): out+=[T,T.T]; T=np.rot90(T)
    return out
def canon(S):
    return min(tuple(int(x) for x in V.ravel()) for V in d4(S))

def gen_siamese(n,start,step,brk):
    S=np.zeros((n,n),dtype=int); i,j=start; a,b=step; c,d=brk
    for k in range(1,n*n+1):
        S[i,j]=k
        ni,nj=(i+a)%n,(j+b)%n
        if S[ni,nj]: ni,nj=(i+c)%n,(j+d)%n
        if S[ni,nj] and k<n*n: return None
        i,j=ni,nj
    return S

def all_siamese_variants(n):
    """every (start, step, break) generalised de la Loubere fill that yields a magic square"""
    found={}
    cells=[(i,j) for i in range(n) for j in range(n)]
    vec=[(a,b) for a in range(n) for b in range(n) if (a,b)!=(0,0)]
    cnt=0
    for st in cells:
        for stp in vec:
            for br in vec:
                S=gen_siamese(n,st,stp,br)
                if S is None: continue
                cnt+=1
                if is_magic(S): found.setdefault(canon(S),(st,stp,br))
    return found,cnt

def siamese3():
    return gen_siamese(3,(0,1),(-1,1),(1,0))

def strachey6():
    """Strachey-type for n=6 (m=1): four copies of one oriented 3x3 Siamese square, offsets 0,9,18,27 in all 24 assignments,
    then swap ANY subset of the 9 cells of the left 3x3 block between top-left and bottom-left quadrants (512 subsets).
    Keeps those that are magic (the classical Strachey swap is one of the 512)."""
    uniq={tuple(T.ravel()):T for T in d4(siamese3())}
    res={}
    for B in uniq.values():
        for perm in itertools.permutations([0,9,18,27]):
            S=np.zeros((6,6),dtype=int)
            S[:3,:3]=B+perm[0]; S[3:,3:]=B+perm[1]; S[:3,3:]=B+perm[2]; S[3:,:3]=B+perm[3]
            for mask in range(512):
                T=S.copy()
                for c in range(9):
                    if mask>>c&1:
                        r,k=divmod(c,3); T[r,k],T[r+3,k]=S[r+3,k],S[r,k]
                if is_magic(T): res.setdefault(canon(T),T)
    return res

def lux6():
    """Conway's LUX for n=6: base 3x3 siamese, rows LLL/LLL/UUU... with swap; tile each base cell with 2x2 block of 4k-3..4k."""
    pat={'L':np.array([[4,1],[2,3]]),'U':np.array([[1,4],[2,3]]),'X':np.array([[1,4],[3,2]])}
    res={}
    for B in d4(siamese3()):
        for rows in (['LLL','LLL','UUU'],):
            let=[list(r) for r in rows]
            let[2][1],let[1][1]=let[1][1],let[2][1]     # swap centre U with the L above it
            S=np.zeros((6,6),dtype=int)
            for i in range(3):
                for j in range(3):
                    k=B[i,j]
                    S[2*i:2*i+2,2*j:2*j+2]=pat[let[i][j]]+4*(k-1)
            for T in d4(S):
                if is_magic(T): res.setdefault(canon(T),T)
    return res
if __name__=='__main__':
    for n in (5,7):
        f,c=all_siamese_variants(n) if n==5 else (None,None)
        if f is not None: print(n,'valid fills',c,'distinct magic up to D4:',len(f))
    s=strachey6(); print('strachey-type 6:',len(s))
    l=lux6(); print('LUX 6:',len(l))
