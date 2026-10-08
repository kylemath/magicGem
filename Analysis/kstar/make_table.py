"""Regenerate kstar_table.md from kstar_witnesses.json, upper_scan_14_160.json, pigeonhole_bounds.json."""
import json
from math import pi, e, log, sqrt, floor
W=json.load(open("kstar_witnesses.json")); U=json.load(open("upper_scan_14_160.json")); P=json.load(open("pigeonhole_bounds.json"))
L=["# k*(n): exact values, rigorous upper bounds, lower bounds","",
"Exact values (14 ≤ n ≤ 40): upper bound by exact lattice enumeration (F1–F2), lower bound by a verified witness.",
"Upper bounds U(n) for n > 40: exact enumeration only (no witness search). A(n) = ⌊√(πe(n−1)log(n^4/4))⌋ is Theorem A.",
"LB(n) = Theorem B (★) generic / exact-d.","",
"| n | k*(n) | U(n) (enumeration) | A(n) (Theorem A) | LB generic | LB exact-d |","|---|---|---|---|---|---|"]
for n in sorted(set(map(int,U))|set(map(int,W))):
    k=W.get(str(n),{}).get('kstar'); u=U.get(str(n),{}).get('upper'); A=floor(sqrt(pi*e*(n-1)*log(n**4/4)))
    p=P.get(str(n),{})
    L.append(f"| {n} | {k if k else ''} | {u if u else ''} | {A} | {p.get('generic','')} | {p.get('exact','') or ''} |")
L+=["","Also: k*(n) ≤ n−3 for all 18 ≤ n ≤ 170 (`below_n_minus_2.py`, rank-2 lattices) and, by Theorem A, for all n ≥ 166.",
"Missing n in the U(n) column: enumeration not finished when the table was generated (`upper_scan.py` still running)."]
open("kstar_table.md","w").write("\n".join(L)+"\n")
print(len(L))
