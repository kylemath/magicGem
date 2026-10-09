# Referee B checks: n=3 exhaustive -- Loly I distribution vs degree-2 class; mean/var of I; semi-magic implication.
import itertools, numpy as np
from fractions import Fraction
n=3;N=9
x=np.array([j-1 for i in range(3) for j in range(3)]); y=np.array([1-i for i in range(3) for j in range(3)])
r2=x**2+y**2
cnt_I60=0; cnt_deg2=0; cnt_semi=0; both=0; Is=[]
for p in itertools.permutations(range(1,10)):
    s=np.array(p); z=s-5.0
    I=int((s*r2).sum()); Is.append(I)
    S=s.reshape(3,3); semi=all(S.sum(0)==15) and all(S.sum(1)==15)
    deg2 = (x*z).sum()==0 and (y*z).sum()==0 and (x*x*z).sum()==0 and (y*y*z).sum()==0
    cnt_I60+= I==60; cnt_deg2+=deg2; cnt_semi+=semi; both += (I==60 and deg2)
Is=np.array(Is)
print("arrangements with I=60:",cnt_I60," degree-2:",cnt_deg2," semi-magic:",cnt_semi," I=60&deg2:",both)
print("mean I over all 9!:",Is.mean()," var:",Is.var()," predicted var N^2*sigma^2*Var(r2) =",81*Fraction(10,12)*Fraction(4,9), "sd",Is.std())
print("distinct I values:",len(set(Is)), "min",Is.min(),"max",Is.max())
