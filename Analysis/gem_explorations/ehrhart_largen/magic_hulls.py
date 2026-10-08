import sys, json, glob, time; sys.dont_write_bytecode=True
import numpy as np
from collections import Counter
from multiprocessing import Pool
from hulllib import *
from constructions import *
sys.path.insert(0,'/Users/kylemathewson/magicGem/paper_A_gems/anc')
from siamese_util import siamese

def load_sa(n):
    arr=[]
    for f in sorted(glob.glob(f'sa_out/sa_n{n}_*.txt')):
        a=np.loadtxt(f,dtype=int,ndmin=2)
        if a.size: arr.append(a)
    return np.concatenate(arr).reshape(-1,n,n)

def vinfo(S):
    S=np.asarray(S); n=S.shape[0]; N=n*n
    assert is_magic(S)
    P=grid_points(S)
    ev=exact_vertices(P)
    qv=set(qh_vertices(P).tolist())
    ok=(set(ev.tolist())==qv)
    flat=S.ravel()
    ev=set(ev.tolist())
    c1=int(np.argmax(flat==1)); cN=int(np.argmax(flat==N)); c2=int(np.argmax(flat==2)); cN1=int(np.argmax(flat==N-1))
    assert c1 in ev and cN in ev
    return len(ev), ok, (c2 in ev), (cN1 in ev)

def dedup(arr):
    seen={}
    for S in arr:
        seen.setdefault(canon(S),S)
    return list(seen.values())

def runset(name,sqs):
    with Pool(16) as p: r=p.map(vinfo,sqs,chunksize=200)
    V=np.array([x[0] for x in r])
    return dict(name=name,count=len(sqs),V=V.tolist(),qh_exact_mismatch=int(sum(1 for x in r if not x[1])),
                s2_vertex_frac=float(np.mean([x[2] for x in r])),sN1_vertex_frac=float(np.mean([x[3] for x in r])))

if __name__=='__main__':
    out={}
    # constructions
    cons={}
    f5,c5=all_siamese_variants(5); cons[5]=[np.array(k).reshape(5,5) for k in f5]
    f7={}
    # n=7: restrict to start cells in one orbit-agnostic sweep (all starts), steps/breaks 48x48 -> 113k fills
    f7,c7=all_siamese_variants(7); cons[7]=[np.array(k).reshape(7,7) for k in f7]
    cons[6]=list(strachey6().values())+list(lux6().values())
    cons[3]=[siamese(3)]; cons[4]=[]
    print({n:len(v) for n,v in cons.items()},'valid siamese-type fills n=5,7:',c5,c7,flush=True)
    SQ4=np.loadtxt('/Users/kylemathewson/magicGem/paper_A_gems/anc/squares880.txt',dtype=int).reshape(880,4,4)
    for n in [4,5,6,7,8]:
        try: sa=load_sa(n)
        except Exception as e: print('no sa',n,e); continue
        d=dedup(sa)
        print(n,'SA raw',len(sa),'distinct up to D4',len(d),flush=True)
        out[f'SA{n}']=runset(f'SA{n}',d); out[f'SA{n}']['raw']=len(sa)
        if cons.get(n): out[f'CONS{n}']=runset(f'CONS{n}',cons[n])
    out['EXACT4']=runset('EXACT4',list(SQ4))
    out['SIAM']={n:vinfo(siamese(n))[0] for n in range(3,22,2)}
    for k,v in out.items():
        if k!='SIAM':
            V=np.array(v['V']); print(k,'count',v['count'],'mean',V.mean(),'sd',V.std(ddof=1) if len(V)>1 else 0,'min',V.min(),'max',V.max(),'mismatch',v['qh_exact_mismatch'],'s2 vertex',v['s2_vertex_frac'])
    json.dump(out,open('magic_hulls.json','w'))
