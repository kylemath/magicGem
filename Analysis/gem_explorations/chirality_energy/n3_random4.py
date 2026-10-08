"""Task 6b/c: n=3 exhaustive (hull volume vs E_full) and 1e5 random order-4 permutations vs the 880 magic gems."""
import json, itertools, time
from common import *
from scipy.stats import spearmanr, pearsonr
import sys
sys.path.insert(0, '/Users/kylemathewson/magicGem/paper_B_orthogonality/anc')
from energies import all_energies
from multiprocessing import Pool

def init(n):
    global XY
    XY = scaled_points(np.arange(1, n*n+1).reshape(n, n))[:, :2]

def vol_batch(args):
    n, arrs = args
    XYn = scaled_points(np.arange(1, n*n+1).reshape(n, n))[:, :2]
    out = np.zeros((len(arrs), 2), dtype=np.int64)
    for i, a in enumerate(arrs):
        P = np.c_[XYn, 2 * a - (n*n + 1)]
        v, nv = hull_int(P)
        out[i] = (v, nv)
    return out

def run(n, arrs, procs=15, chunk=5000):
    chunks = [(n, arrs[i:i+chunk]) for i in range(0, len(arrs), chunk)]
    with Pool(procs) as p:
        return np.vstack(p.map(vol_batch, chunks))

if __name__ == '__main__':
    t = time.time()
    # ---- n=3 exhaustive
    perms = np.array(list(itertools.permutations(range(1, 10))), dtype=np.int64)
    VV = run(3, perms)
    vol3 = VV[:, 0] / 48.0 * 1.0; nv3 = VV[:, 1]
    En = all_energies(perms.reshape(-1, 3, 3))
    F3 = np.rint(En['E_full'] * 81).astype(int)   # N^2 E_full
    mag = F3 == 0
    degenerate = VV[:, 0] == 0
    res3 = dict(n_arrangements=len(perms), n_magic=int(mag.sum()), n_degenerate_flat=int(degenerate.sum()),
      spearman_vol_Efull_all=float(spearmanr(vol3, F3)[0]), pearson_vol_Efull_all=float(pearsonr(vol3, F3)[0]),
      spearman_vol_Efull_nondegenerate=float(spearmanr(vol3[~degenerate], F3[~degenerate])[0]),
      spearman_vol_Elow=float(spearmanr(vol3, En['E_low'])[0]),
      mean_vol_magic=float(vol3[mag].mean()), mean_vol_all=float(vol3.mean()),
      magic_vol_percentile_range=[float((vol3 < v).mean()) for v in (vol3[mag].min(), vol3[mag].max())],
      magic_volume_values=sorted(set(vol3[mag].tolist())), vol_quantiles_all=np.percentile(vol3,[1,25,50,75,99]).tolist(),
      mean_nv_magic=float(nv3[mag].mean()), mean_nv_all=float(nv3.mean()),
      spearman_nv_Efull=float(spearmanr(nv3, F3)[0]))
    # volume bin means vs F
    bins = np.quantile(F3, np.linspace(0, 1, 11)); bi = np.clip(np.searchsorted(bins, F3, side='right')-1, 0, 9)
    res3['mean_vol_by_Efull_decile'] = [float(vol3[bi == b].mean()) for b in range(10)]
    print('n=3', time.time()-t, json.dumps(res3, indent=1))
    # ---- order 4: random
    rng = np.random.default_rng(7)
    B = 100000
    arr = (np.argsort(rng.random((B, 16)), axis=1) + 1).astype(np.int64)
    VR = run(4, arr)
    volR = VR[:, 0] / 48.0; nvR = VR[:, 1]
    E = all_energies(arr.reshape(-1, 4, 4))
    FR = np.rint(E['E_full'] * 256).astype(int)
    geo = json.load(open('/Users/kylemathewson/magicGem/paper_A_gems/anc/results_geometry.json'))
    vol880 = np.array([float(Fraction(g['volume'])) for g in geo['per_gem']]); nv880 = np.array([g['f_vector'][0] for g in geo['per_gem']])
    # sanity: my fast volume equals the paper's exact volumes
    V880 = run(4, SQ.reshape(880, 16).astype(np.int64))
    assert np.allclose(V880[:, 0] / 48.0, vol880) and (V880[:, 1] == nv880).all()
    # also all 7040 magic squares (their volumes are the same as 880 up to D4, so skip)
    pct = lambda x, ref: float((ref < x).mean() + 0.5 * (ref == x).mean())
    mp = np.array([pct(v, volR) for v in vol880])
    res4 = dict(B=B, n_random_magic=int((FR == 0).sum()), random_vol_mean=float(volR.mean()), random_vol_sd=float(volR.std()),
      random_vol_quantiles_1_25_50_75_99=np.percentile(volR, [1,25,50,75,99]).tolist(),
      magic880_vol_mean=float(vol880.mean()), magic880_vol_sd=float(vol880.std()),
      magic880_vol_quantiles_1_25_50_75_99=np.percentile(vol880, [1,25,50,75,99]).tolist(),
      magic880_percentile_in_random_median=float(np.median(mp)), magic880_percentile_min=float(mp.min()), magic880_percentile_max=float(mp.max()),
      frac_magic_below_random_median=float((vol880 < np.median(volR)).mean()),
      random_nv_mean=float(nvR.mean()), random_nv_dist={int(k): int((nvR==k).sum()) for k in np.unique(nvR)},
      magic880_nv_mean=float(nv880.mean()), magic880_nv_dist={int(k): int((nv880==k).sum()) for k in np.unique(nv880)},
      spearman_vol_Efull=float(spearmanr(volR, FR)[0]), spearman_vol_Elow=float(spearmanr(volR, E['E_low'])[0]),
      pearson_vol_Efull=float(pearsonr(volR, FR)[0]),
      spearman_nv_Efull=float(spearmanr(nvR, FR)[0]), spearman_nv_vol=float(spearmanr(nvR, volR)[0]),
      mean_vol_by_Efull_decile=[float(volR[(FR >= lo) & (FR < hi)].mean()) for lo, hi in zip(np.quantile(FR, np.linspace(0,.9,10)), list(np.quantile(FR, np.linspace(.1,.9,9))) + [FR.max()+1])],
      dec_edges=np.quantile(FR, np.linspace(0,1,11)).tolist())
    # volume of random perms with low energy (F<=..): lowest-energy 1% vs rest
    lo = FR <= np.quantile(FR, .01)
    res4['mean_vol_lowest1pct_Efull'] = float(volR[lo].mean()); res4['mean_vol_rest'] = float(volR[~lo].mean())
    # sheer: volume of random vs "expected from z-variance": Spearman with Var of z is const; with sum|z - zbar|? skip
    # geometric explanation check: volume vs correlation of z with |x|,|y| radius (outer cells larger z spread)
    json.dump(dict(n3=res3, n4=res4), open('results_n3_random4.json', 'w'), indent=1)
    print(json.dumps(res4, indent=1))
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(14, 3.8))
    ax[0].hist(volR, bins=80, density=True, alpha=.6, label='1e5 random perms'); ax[0].hist(vol880, bins=40, density=True, alpha=.6, label='880 magic'); ax[0].set_xlabel('hull volume'); ax[0].legend()
    ax[1].hexbin(FR, volR, gridsize=50, bins='log', mincnt=1); ax[1].set_xlabel(r'$N^2E_{full}$ (n=4)'); ax[1].set_ylabel('hull volume')
    ax[1].scatter(np.zeros(880), vol880, s=3, c='r', alpha=.3)
    ax[2].hexbin(F3, vol3, gridsize=50, bins='log', mincnt=1); ax[2].set_xlabel(r'$N^2E_{full}$ (n=3)'); ax[2].set_ylabel('hull volume')
    plt.tight_layout(); plt.savefig('fig_volume_energy.png', dpi=130)
