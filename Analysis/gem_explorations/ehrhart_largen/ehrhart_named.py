import sys, json; sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/kylemathewson/magicGem/paper_A_gems/anc')
import numpy as np
from fractions import Fraction
from ehrhart import analyse, lattice_width
from siamese_util import siamese
import sympy as sp
res={}
lo=np.array([[2,7,6],[9,5,1],[4,3,8]])
dur=np.array([[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]])
def rep(name,S,tmax=5):
    r=analyse(S,tmax=tmax); w=lattice_width(r['V'],R=8)
    d=dict(L=r['L'],coef=[str(c) for c in r['coef']],h=r['h'],inter=r['inter'],bd=r['bd'],vol=str(r['vol_Q']),nverts=r['nverts'],width=w[0],f=list(r['h_exact']['f_vector']))
    res[name]=d; print(name,d,flush=True)
rep('LoShu',lo); rep('Durer',dur)
for n in [5,7,9,11,13]:
    rep(f'Siamese{n}',siamese(n),tmax=5)
json.dump(res,open('ehrhart_named.json','w'),indent=1)
# fit coefficients in n for Siamese n=5..13 (5 data points): try degree<=4 in n, check consistency using n=3? (Lo Shu is 8 vertices, excluded)
ns=[5,7,9,11,13]; n=sp.symbols('n')
fits={}
for k,name in enumerate(['c0','c1','c2','c3']):
    pts=[(m,Fraction(res[f'Siamese{m}']['coef'][k])) for m in ns]
    p=sp.interpolate([(a,sp.Rational(b.numerator,b.denominator)) for a,b in pts[:4]],n)  # cubic... use first 4 points
    # check at 5th
    ok=sp.simplify(p.subs(n,13)-sp.Rational(pts[4][1].numerator,pts[4][1].denominator))==0
    p5=sp.interpolate([(a,sp.Rational(b.numerator,b.denominator)) for a,b in pts],n)
    fits[name]=dict(deg3_from_first4=str(sp.factor(p)),deg3_predicts_13=bool(ok),interp_5pts=str(sp.factor(p5)),deg5=sp.degree(p5,n))
    print(name,fits[name])
json.dump(fits,open('siamese_ehrhart_fits.json','w'),indent=1)
