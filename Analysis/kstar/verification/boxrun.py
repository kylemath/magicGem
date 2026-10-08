import sys; sys.argv=['x']
exec(open('boxr.py').read().split('for n,k in')[0])
import json
w=json.load(open('/Users/kylemathewson/magicGem/Analysis/kstar/kstar_witnesses.json'))
for n in range(14,30):
    k=int(w[str(n)]['kstar'])
    run(n,k,go=False)
