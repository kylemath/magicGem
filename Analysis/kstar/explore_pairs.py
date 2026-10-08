# For linear Latin-based semi-magic squares of odd order, look for row pairs whose
# column-sum vector c_j = s_ij + s_i'j has many equal pairs.
import itertools, collections, sys
def sq(n,a1,a2,b1,b2):
    return [[n*((a1*i+a2*j)%n)+((b1*i+b2*j)%n)+1 for j in range(n)] for i in range(n)]
for n in [5,7,9,11,13,15]:
    best=None
    S=sq(n,1,1,1,2)
    for i,ip in itertools.combinations(range(n),2):
        c=[S[i][j]+S[ip][j] for j in range(n)]
        cnt=collections.Counter(c)
        pairs=sum(v//2 for v in cnt.values())
        if best is None or pairs>best[0]: best=(pairs,i,ip,c)
    print(n,best[0],best[1:3],best[3])
