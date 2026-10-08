from math import pi,e,log,sqrt,floor,isqrt
def A(n): return floor(sqrt(pi*e*(n-1)*log(n**4/4)))
fails=[n for n in range(3,1000001) if A(n)>n-3]
print('max n with A(n)>n-3:',max(fails),' A(165),A(166)=',A(165),A(166))
print([ (n,A(n)) for n in (14,40,50,100,113)])
# check 2sqrt(pi e) sqrt(n log n) >= A(n)
print(all(A(n)<=2*sqrt(pi*e)*sqrt(n*log(n)) for n in range(3,100000)), 2*sqrt(pi*e))
