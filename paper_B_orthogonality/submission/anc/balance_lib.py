"""Balance functionals of Section `Balance of the signed mass` (exact definitions).

Cells are flattened row-major; x=j-(n-1)/2, y=(n-1)/2-i, z=s-(N+1)/2, N=n^2.
Models (masses are always the signed heights z_c):
  linear     : B_lin  = |sum_c z_c (x_c, y_c)|
  ring       : B_ring = |sum_c z_c u_c|,  u_c=(x_c,y_c)/r_c  (u_c=0 at the centre cell, n odd)
  3D unit    : u_c=v_c/|v_c|, v_c=(x_c,y_c,z_c) (u_c=0 if v_c=0); B_3D^xy = horizontal part of sum z_c u_c,
               V = vertical part = sum z_c^2/|v_c|  (>0 for every arrangement).
"""
import numpy as np


def geometry(n):
    j = np.tile(np.arange(n), n); i = np.repeat(np.arange(n), n)
    x = j - (n - 1) / 2; y = (n - 1) / 2 - i
    L = np.zeros((2 * n + 2, n * n))
    for k in range(n):
        L[k] = (i == k); L[n + k] = (j == k)
    L[2 * n] = (i == j); L[2 * n + 1] = (i + j == n - 1)
    return x, y, L


def functionals(S, n):
    """S: (B,N) array of arrangements (values 1..N).  Returns dict of arrays of length B."""
    N = n * n
    x, y, L = geometry(n)
    z = S - (N + 1) / 2.0
    dev = np.einsum('bc,lc->bl', z, L)
    out = {'E_full': (dev ** 2).sum(1) / N ** 2,
           'E_rc': (dev[:, :2 * n] ** 2).sum(1) / N ** 2}
    zx = np.einsum('bc,c->b', z, x); zy = np.einsum('bc,c->b', z, y)
    out['B_lin'] = np.hypot(zx, zy)
    out['lin_x'] = zx; out['lin_y'] = zy
    out['P_xy'] = np.abs(np.einsum('bc,c->b', z, x * y))
    out['I_dev'] = np.abs(np.einsum('bc,c->b', z, x ** 2 + y ** 2))
    r = np.hypot(x, y); rr = np.where(r > 0, r, 1.0)
    ux = np.where(r > 0, x / rr, 0.0); uy = np.where(r > 0, y / rr, 0.0)
    out['B_ring'] = np.hypot(np.einsum('bc,c->b', z, ux), np.einsum('bc,c->b', z, uy))
    nrm = np.sqrt(x[None, :] ** 2 + y[None, :] ** 2 + z ** 2)
    nz = np.where(nrm > 0, nrm, 1.0)
    bx = (z * x[None, :] / nz).sum(1); by = (z * y[None, :] / nz).sum(1)
    bz = (z * z / nz).sum(1)
    out['B_3D_xy'] = np.hypot(bx, by); out['V_3D'] = bz
    out['B_3D'] = np.sqrt(bx ** 2 + by ** 2 + bz ** 2)
    # T2 bound
    out['T2_lhs'] = zx ** 2 + zy ** 2
    out['T2_rhs'] = N ** 2 * n * (n * n - 1) / 12.0 * out['E_rc']
    return out


def magic4_reps(path):
    A = np.loadtxt(path, dtype=np.int64)
    seen = {}
    for a in A:
        g = a.reshape(4, 4); forms = []
        for k in range(4):
            r = np.rot90(g, k); forms += [tuple(r.ravel()), tuple(r.T.ravel())]
        seen[min(forms)] = 1
    return np.array(sorted(seen.keys()), dtype=float), A.astype(float)
