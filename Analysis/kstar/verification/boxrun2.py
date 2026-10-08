import sys
exec(open('boxr.py').read().split('for n,k in')[0])
import json
w=json.load(open('/Users/kylemathewson/magicGem/Analysis/kstar/kstar_witnesses.json'))
for n in range(14,24):
    k=int(w[str(n)]['kstar']); run(n,k)
for n in (14,15,18,19,21):   # positive controls at level k*-1
    k=int(w[str(n)]['kstar'])-1; run(n,k)
