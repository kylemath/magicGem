import sys, json; sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/kylemathewson/magicGem/paper_A_gems/anc')
from fractions import Fraction
from ehrhart import analyse
from siamese_util import siamese
import sympy as sp
res=json.load(open('ehrhart_named.json'))
for n in [15,17]:
    r=analyse(siamese(n),tmax=4)
    res[f'Siamese{n}']=dict(L=r['L'],coef=[str(c) for c in r['coef']],h=r['h'],inter=r['inter'],bd=r['bd'],vol=str(r['vol_Q']),nverts=r['nverts'])
    print(n,res[f'Siamese{n}'],flush=True)
json.dump(res,open('ehrhart_named.json','w'),indent=1)
n=sp.symbols('n'); ns=[5,7,9,11,13,15,17]; out={}
for k in range(4):
    pts=[(m,sp.Rational(res[f'Siamese{m}']['coef'][k])) for m in ns]
    best=None
    for deg in range(0,6):
        p=sp.interpolate(pts[:deg+1],n)
        if all(p.subs(n,a)==b for a,b in pts):
            best=(deg,str(sp.factor(p))); break
    out[f'c{k}']=best; print(k,best, 'points used',len(pts))
for nm,key in [('inter','inter'),('bd','bd')]:
    pts=[(m,sp.Integer(res[f'Siamese{m}'][key])) for m in ns]
    for deg in range(0,6):
        p=sp.interpolate(pts[:deg+1],n)
        if all(p.subs(n,a)==b for a,b in pts):
            out[nm]=(deg,str(sp.factor(p))); break
    print(nm,out.get(nm))
json.dump(out,open('siamese_ehrhart_fits.json','w'),indent=1)
