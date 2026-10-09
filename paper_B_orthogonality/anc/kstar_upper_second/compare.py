"""Compare the upper bounds U(n), 14<=n<=100, of the two independent implementations:
kstar_verify.py (../kstar_verify.json) and this folder's exact_kmax.py / lattice.py (upper_bounds_14_100.json).
Run: python3 compare.py"""
import json, os
h = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(h, 'upper_bounds_14_100.json')))
b = json.load(open(os.path.join(h, '..', 'kstar_verify.json')))['upper_bounds']
bad = [n for n in range(14, 101) if a[str(n)]['upper'] != b[str(n)]]
print('n = 14..100 compared:', 87, ' mismatches:', bad)
assert not bad
