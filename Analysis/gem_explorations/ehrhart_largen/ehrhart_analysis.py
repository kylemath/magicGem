import json, sys, numpy as np
sys.dont_write_bytecode=True
from collections import Counter, defaultdict
from fractions import Fraction
ANC='/Users/kylemathewson/magicGem/paper_A_gems/anc'
E=json.load(open('ehrhart_880.json')); G=json.load(open(ANC+'/results_geometry.json'))
R={}
poly=[tuple(e['coef']) for e in E]; hv=[tuple(e['h']) for e in E]; fv=[tuple(e['f']) for e in E]; vol=[e['vol'] for e in E]
typ=[G['per_gem'][k]['combinatorial_type'] for k in range(880)]
R['n']=880
R['distinct_ehrhart_polys']=len(set(poly)); R['distinct_hvec']=len(set(hv)); R['distinct_L_values_t1to3']=len(set(tuple(e['L'][:4]) for e in E))
R['distinct_f']=len(set(fv)); R['distinct_types']=len(set(typ)); R['distinct_vol']=len(set(vol))
R['distinct_(vol,f)']=len(set(zip(vol,fv)))
R['distinct_(vol,type)']=len(set(zip(vol,typ)))
# is Ehrhart poly determined by (volume, boundary lattice pts, interior)? -> (c3, c2, c1) free; L(1)=sum -> poly determined by (vol, c2, L1)
# invariants
R['c2_distinct']=len(set(e['coef'][2] for e in E))
R['L1_range']=(min(e['L'][1] for e in E),max(e['L'][1] for e in E))
R['inter_dist']=sorted(Counter(e['inter'] for e in E).items())
R['bd_dist']=sorted(Counter(e['bd'] for e in E).items())
R['h1_range']=(min(h[1] for h in hv),max(h[1] for h in hv)); R['h2_range']=(min(h[2] for h in hv),max(h[2] for h in hv))
# boundary pts: expect 16 point-set boundary >= vertices etc
R['h_all_nonneg_int']=all(min(h)>=0 for h in hv)
# Stanley: h0+h1 >= h2+h3?? For d=3: h1 <= h2 ... general Stanley: h_0+..+h_i <= h_s + ... + h_{s-i}, s=deg
# s = largest i with h_i != 0 = 3 here. Check: h3<=h1 ; h3+h2? Hatchings: h_0+h_1+..+h_i <= h_s+h_{s-1}+...+h_{s-i}  (i=0..floor(s/2)) ... use Stanley: h_s+...+h_{s-i} <= h_1+...+h_{i+1}
stan=all(h[3]<=h[1] and h[3]+h[2]<=h[1]+h[2]  for h in hv)
R['Hibi_h3_le_h1_hmm']=all(h[3]<=h[1] for h in hv)
R['Stanley_h3+h2<=h1+h2 (i.e. h3<=h1)']=stan
# Hibi: h1 <= h2 for s=3? (h_1 <= h_{d-1} when interior nonempty: h_1<=h_{d-1}?) For d=3: h1<=h2 (Hibi).  Check
R['Hibi_h1<=h2']=all(h[1]<=h[2] for h in hv)
R['h3<=h1']=all(h[3]<=h[1] for h in hv)
# Is h a function of f-vector?
byf=defaultdict(set); byt=defaultdict(set); byv=defaultdict(set)
for k in range(880): byf[fv[k]].add(hv[k]); byt[typ[k]].add(hv[k]); byv[vol[k]].add(hv[k])
R['f->h not function: #f with >1 h']=sum(1 for v in byf.values() if len(v)>1)
R['type->h not function: #types with >1 h']=sum(1 for v in byt.values() if len(v)>1)
R['vol->h: #vols with >1 h']=sum(1 for v in byv.values() if len(v)>1)
# Ehrhart equivalence classes vs congruence classes
cong=G  # complement partner => congruence classes (616 classes = complement orbits)
cp=G['complement_partner']
cls={}
for k in range(880): cls[k]=min(k,cp[k])
classes=defaultdict(list)
for k in range(880): classes[cls[k]].append(k)
# complement orbit => same Ehrhart poly? (z->-z lattice-preserving up to translation, should be)
R['complement_same_poly']=all(poly[k]==poly[cp[k]] for k in range(880))
R['n_congruence_classes']=len(classes)
bypoly=defaultdict(set)
for k in range(880): bypoly[poly[k]].add(cls[k])
R['n_poly_with_>1_congruence_class']=sum(1 for v in bypoly.values() if len(v)>1)
R['max_classes_per_poly']=max(len(v) for v in bypoly.values())
R['largest_poly_class_sizes']=sorted((sum(len(classes[c]) for c in v) for v in bypoly.values()),reverse=True)[:10]
R['poly_class_size_hist']=sorted(Counter(len(v) for v in bypoly.values()).items())
# same-poly same-vertex-count? same f?
R['poly_class_with_different_f']=sum(1 for p in bypoly if len({fv[k] for k in range(880) if poly[k]==p})>1)
R['poly_class_with_different_type']=sum(1 for p in bypoly if len({typ[k] for k in range(880) if poly[k]==p})>1)
# width
R['width_dist']=sorted(Counter(e['width'] for e in E).items())
# Dürer and where
dur=[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
def canon(S):
    S=np.array(S);V=[]
    T=S
    for _ in range(4): V+= [T,T.T]; T=np.rot90(T)
    return min(tuple(int(x) for x in v.ravel()) for v in V)
cd=canon(dur); 
for e in E:
    if canon(e['square'])==cd: R['durer']=dict(idx=e['idx'],coef=e['coef'],h=e['h'],L=e['L'][:5],inter=e['inter'],bd=e['bd'],vol=e['vol'],f=e['f'],width=e['width'])
# correlations: h1 vs vertex count etc.
import math
vc=np.array([f[0] for f in fv]); h1=np.array([h[1] for h in hv]); h2=np.array([h[2] for h in hv]); h3=np.array([h[3] for h in hv]); vv=np.array([float(Fraction(v)) for v in vol])
R['corr(h3,vol)']=float(np.corrcoef(h3,vv)[0,1]); R['corr(c2,vol)']=float(np.corrcoef([float(Fraction(e['coef'][2])) for e in E],vv)[0,1])
R['h3_range']=(int(h3.min()),int(h3.max()))
R['n_h3_eq_0']=int((h3==0).sum())
# is c1 in some set? denominators
R['c1_denoms']=sorted(Counter(Fraction(e['coef'][1]).denominator for e in E).items())
R['c2_denoms']=sorted(Counter(Fraction(e['coef'][2]).denominator for e in E).items())
R['vol_denoms']=sorted(Counter(Fraction(e['vol']).denominator for e in E).items())
# is polynomial determined by (vol, bd lattice pts)? 
R['distinct (vol,bd)']=len(set(zip(vol,[e['bd'] for e in E])))
R['distinct (vol,L1)']=len(set(zip(vol,[e['L'][1] for e in E])))
R['distinct (vol,inter)']=len(set(zip(vol,[e['inter'] for e in E])))
# Ehrhart eq. but different volume impossible; classes sharing poly list a few
ex=[(p,sorted(v)) for p,v in bypoly.items() if len(v)>1][:3]
R['examples_same_poly_diff_class']=[(p,[classes[c][0] for c in v]) for p,v in ex]
json.dump(R,open('ehrhart_summary.json','w'),indent=1,default=str)
for k,v in R.items(): print(k,':',v)
