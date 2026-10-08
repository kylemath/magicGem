import numpy as np
def siamese(n):
    assert n % 2 == 1
    S = np.zeros((n, n), dtype=int)
    i, j = 0, n // 2
    for k in range(1, n * n + 1):
        S[i, j] = k
        ni, nj = (i - 1) % n, (j + 1) % n
        if S[ni, nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return S
def siamese_closed_form(n):
    m=(n-1)//2
    return np.array([[n*((i+j-m)%n)+((i+2*j-2*m)%n)+1 for j in range(n)] for i in range(n)])
def zeta_points(n):
    """points (x,y,zeta) of the affinely transformed Siamese gem"""
    m=(n-1)//2; pts=[]
    for i in range(n):
        for j in range(n):
            x=j-m; y=m-i
            pts.append((x,y,-n*((x-y+m)//n) - ((2*x-y+m)//n)))
    return np.array(pts)
