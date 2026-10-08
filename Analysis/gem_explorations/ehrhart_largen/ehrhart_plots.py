import json, numpy as np, sys; sys.dont_write_bytecode=True
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from fractions import Fraction
E=json.load(open('ehrhart_880.json'))
h=np.array([e['h'] for e in E]); vol=np.array([float(Fraction(e['vol'])) for e in E]); V=np.array([e['f'][0] for e in E])
fig,ax=plt.subplots(1,3,figsize=(13,3.8))
sc=ax[0].scatter(vol,h[:,3],c=V,cmap='viridis',s=10); ax[0].set_xlabel('volume'); ax[0].set_ylabel('h*_3 = interior lattice points'); plt.colorbar(sc,ax=ax[0],label='hull vertices')
ax[1].scatter(h[:,1],h[:,2],c=V,cmap='viridis',s=10); ax[1].set_xlabel('h*_1 = L(1)-4'); ax[1].set_ylabel('h*_2')
ax[2].hist([e['bd'] for e in E],bins=40); ax[2].set_xlabel('boundary lattice points of Q')
plt.tight_layout(); plt.savefig('ehrhart_hstar.png',dpi=140)
