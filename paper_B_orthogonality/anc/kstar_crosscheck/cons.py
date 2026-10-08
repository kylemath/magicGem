import sys
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..'))
from constructions import construct
bad=[]
for n in list(range(7,80))+[101,150]:
    if n in (8,): pass
    if n%2==0 and n%4==2 and n<14: continue
    try: s,tw=construct(n)
    except Exception as ex: print('construct fail',n,ex); continue
    N=n*n;M=n*(N+1)//2
    ok=sorted(v for r in s for v in r)==list(range(1,N+1)) and all(sum(r)==M for r in s) and all(sum(s[i][j] for i in range(n))==M for j in range(n))
    # independent twin claim per Lemma 3 / Cor 6
    if n%2==0:
        m=n//2; tok=all(s[r][j]+s[m+r][j]==N+1 for r in range(m) for j in range(n))
    else:
        tok=all(s[l][j]+s[n-1-l][j]==N+1 for l in range(0,(n-9)//2+1) for j in range(l+1,n-1-l)) if n>=9 else True
    if not (ok and tok): bad.append((n,ok,tok))
print('constructions bad:',bad)
