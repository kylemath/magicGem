"""Explain the volume~E link: det Cov(X,Y,Z) = VX*VY*VZ - VY Cov(X,Z)^2 - VX Cov(Y,Z)^2 exactly (X,Y uncorrelated on the grid).
Then compare the 880 magic gems with control populations having the same low-mode constraints."""
import json
from common import *
from n3_random4 import run
from scipy.stats import spearmanr
import sys
sys.path.insert(0, '/Users/kylemathewson/magicGem/paper_B_orthogonality/anc')
from energies import all_energies

def detcov(arr, n):
    N = n*n
    xs = np.tile(np.arange(n) - (n-1)/2, n).astype(float); ys = np.repeat((n-1)/2 - np.arange(n), n).astype(float)
    Z = arr.reshape(len(arr), N).astype(float); Z = Z - Z.mean(1, keepdims=True)
    M = np.stack([np.broadcast_to(xs, Z.shape), np.broadcast_to(ys, Z.shape), Z], axis=1)  # (B,3,N)
    C = np.einsum('bin,bjn->bij', M, M) / N
    return np.linalg.det(C), C

if __name__ == '__main__':
    rng = np.random.default_rng(11)
    # exact identity check
    arr = (np.argsort(rng.random((2000, 16)), axis=1) + 1)
    d, C = detcov(arr, 4)
    VX, VY, VZ = C[:,0,0], C[:,1,1], C[:,2,2]
    assert np.allclose(C[:,0,1], 0)
    assert np.allclose(d, VX*VY*VZ - VY*C[:,0,2]**2 - VX*C[:,1,2]**2)
    assert np.allclose(VZ, VZ[0])
    out = {'identity_detcov_checked_on': 2000}
    # random pop 1e5 volume vs detcov
    B = 100000
    arr = (np.argsort(rng.random((B, 16)), axis=1) + 1).astype(np.int64)
    V = run(4, arr)[:, 0] / 48.0; d, C = detcov(arr, 4); E = all_energies(arr.reshape(-1,4,4))
    Exy = E['cov_x']**2 + E['cov_y']**2
    out['random_spearman_vol_detcov'] = float(spearmanr(V, d)[0]); out['random_spearman_vol_Exy'] = float(spearmanr(V, Exy)[0])
    out['random_spearman_vol_Ediag'] = float(spearmanr(V, E['cov_dm']**2 + E['cov_da']**2)[0])
    out['random_spearman_vol_Efull_minus_Elow'] = float(spearmanr(V, E['E_full'] - E['E_low'])[0])
    # control populations: E_xy = 0 (tilt-free) and E_low = 0
    ctrl = []; 
    for rep in range(60):
        a = (np.argsort(rng.random((200000, 16)), axis=1) + 1).astype(np.int64)
        e = all_energies(a.reshape(-1,4,4))
        ok = (np.abs(e['cov_x']) < 1e-12) & (np.abs(e['cov_y']) < 1e-12)
        ctrl.append((a[ok], (np.abs(e['cov_dm']) < 1e-12)[ok] & (np.abs(e['cov_da']) < 1e-12)[ok], np.rint(e['E_full'][ok]*256).astype(int)))
    A = np.vstack([c[0] for c in ctrl]); LOW = np.concatenate([c[1] for c in ctrl]); FF = np.concatenate([c[2] for c in ctrl])
    VA = run(4, A)[:, 0] / 48.0
    geo = json.load(open('/Users/kylemathewson/magicGem/paper_A_gems/anc/results_geometry.json'))
    vol880 = np.array([float(Fraction(g['volume'])) for g in geo['per_gem']])
    pct = lambda x, ref: float((ref < x).mean() + 0.5 * (ref == x).mean())
    for name, mask in [('Exy=0', np.ones(len(A), bool)), ('Elow=0 (no tilt, diagonals ok)', LOW), ('Elow=0 and Efull>0 (nonmagic)', LOW & (FF > 0))]:
        ref = VA[mask]
        out[name] = dict(n=int(mask.sum()), mean=float(ref.mean()), sd=float(ref.std()), magic880_mean=float(vol880.mean()),
                         magic880_median_percentile=float(np.median([pct(v, ref) for v in vol880])),
                         mean_pct=float(np.mean([pct(v, ref) for v in vol880])), n_magic_in_sample=int((FF[mask] == 0).sum()))
    # within Exy=0: does Efull (row/col imbalance) correlate with volume?
    out['Exy=0: spearman_vol_Efull'] = float(spearmanr(VA, FF)[0])
    m = LOW; out['Elow=0: spearman_vol_Efull'] = float(spearmanr(VA[m], FF[m])[0]) if m.sum() > 10 else None
    # magic gems: correlation of volume with sigma etc is separate; here: variation of volume across 880 at fixed det Cov
    d880, _ = detcov(SQ.reshape(880, 16), 4); out['detcov_880_all_equal'] = bool(np.allclose(d880, d880[0]))
    # n=4 swap: Delta vol vs Delta detcov for the 100x120 swaps
    R = np.load('swaps_raw.npy'); 
    json.dump(out, open('results_inertia_control.json', 'w'), indent=1); print(json.dumps(out, indent=1))
    # swaps: delta detcov
    import itertools
    dd = []; dv = []
    for k in np.unique(R[:,0]):
        base = SQ[int(k)].ravel()
        for r in R[R[:,0]==k]:
            f = base.copy(); a, b = int(r[1]), int(r[2]); f[a], f[b] = f[b], f[a]
            dd.append(detcov(f[None], 4)[0][0] - d880[0]); dv.append(r[6]/48.0)
    out['swaps_spearman_dV_ddetcov'] = float(spearmanr(dv, dd)[0]); out['swaps_pearson_dV_ddetcov'] = float(np.corrcoef(dv, dd)[0,1])
    json.dump(out, open('results_inertia_control.json', 'w'), indent=1); print(out['swaps_spearman_dV_ddetcov'], out['swaps_pearson_dV_ddetcov'])
