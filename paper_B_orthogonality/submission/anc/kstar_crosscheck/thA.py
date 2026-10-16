# Range of Theorem 3.7(a): A(n) = floor(sqrt(2(n-1) log(n^4/4))) (Schur's bound, Lemma 3.9 of the paper).
from math import log, sqrt, floor
def A(n): return floor(sqrt(2*(n-1)*log(n**4/4)))
for name, cond in (('A(n) < n-1', lambda n: A(n) < n-1), ('A(n) <= n-3', lambda n: A(n) <= n-3), ('A(n) < n-3', lambda n: A(n) < n-3)):
    fails = [n for n in range(3, 1000001) if not cond(n)]
    print(name, 'for all n >= %d (up to 10^6)' % (max(fails) + 1))
print([(n, A(n)) for n in (14, 24, 27, 30, 40, 50, 100)])
# check 2 sqrt 2 sqrt(n log n) >= A(n)
print(all(A(n) <= 2*sqrt(2)*sqrt(n*log(n)) for n in range(3, 1000001)), 2*sqrt(2))
