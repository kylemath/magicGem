"""Figure: three gems (centrally symmetric / half-turn symmetric / no symmetry) with a symmetry-related facet pair highlighted."""
from gemfig import *
from gem_geometry import classify_points
from isolib import isometries, element_type
sym = __import__('json').load(open(os.path.join(HERE, 'symmetry_880.json')))
CASES = [('Ci', 174, '(a) centrally symmetric\n(isometry $\\mathbf{p}\\mapsto-\\mathbf{p}$)'),
         ('C2', None, '(b) self-complementary\n(half-turn about the dashed axis)'),
         ('C1', None, '(c) generic\n(no non-trivial isometry)')]
def pick(group, vcount=12):
    for r in sym:
        if r['group'] == group and r['f_vector'][0] == vcount and r['index'] > 100: return r['index']
CASES[1] = (CASES[1][0], pick('C2'), CASES[1][2]); CASES[2] = (CASES[2][0], pick('C1'), CASES[2][2])
fig = plt.figure(figsize=(6.5, 3.0))
for col, (grp, idx, title) in enumerate(CASES):
    S = DURER if idx == 174 else SQ[idx]
    if idx == 174: S = DURER
    h = exact_hull(S); P = h['P'] / 2.0; V = h['vertices']
    ax = fig.add_axes([col / 3 - 0.01, 0.14, 0.35, 0.80], projection='3d')
    keys = list(h['faces'].keys()); fsets = [h['faces'][k] for k in keys]
    iso = isometries(h['P'][V]); colors = {}; pairs = None
    if grp != 'C1':
        perm, R = [x for x in iso if element_type(x[1]) != 'E'][0]
        pos = {v: t for t, v in enumerate(V)}
        img = lambda f: frozenset(V[perm[pos[v]]] for v in f)
        # choose the largest face (by number of vertices, then area) that is moved
        cand = [(len(f), t) for t, f in enumerate(fsets) if img(f) != f]
        cand.sort(key=lambda a: -a[0]); t0 = cand[0][1]; t1 = fsets.index(img(fsets[t0]))
        colors = {t0: (OI['orange'], 0.65), t1: (OI['green'], 0.65)}
    keys, polys = draw_faces(ax, h, P, colors=colors, alpha=0.10, lw=0.45)
    ax.scatter(P[V, 0], P[V, 1], P[V, 2], s=7, color=OI['blue'], depthshade=False)
    _, inner, bnd = classify_points(h)        # strictly interior points: red discs; boundary non-vertex points: orange squares
    if inner: ax.scatter(P[inner, 0], P[inner, 1], P[inner, 2], s=7, color=OI['verm'], depthshade=False)
    if bnd: ax.scatter(P[bnd, 0], P[bnd, 1], P[bnd, 2], s=12, color=OI['orange'], marker='s', edgecolors='k', linewidths=0.4, depthshade=False)
    if grp == 'Ci':
        c0, c1 = polys[t0].mean(0), polys[t1].mean(0)
        ax.plot(*zip(c0, c1), color='k', lw=0.8, ls='--'); ax.scatter([0], [0], [0], s=12, color='k', depthshade=False)
    if grp == 'C2':
        w, vv = np.linalg.eigh(R); a = vv[:, np.argmin(abs(w - 1))]
        ax.plot(*zip(-2.6 * a, 2.6 * a), color='k', lw=0.9, ls='--')
    style3d(ax, elev=20, azim=-64)
    fig.text(col / 3 + 1 / 6, 0.07, title, ha='center', va='center', fontsize=8)
    sq = '\n'.join(' '.join(f'{v:2d}' for v in r) for r in S)
    fig.text(col / 3 + 0.02, 0.93, sq, fontsize=6.5, family='monospace', va='top')
    fig.text(col / 3 + 0.31, 0.93, f'$V={h["f_vector"][0]}$, $F={h["f_vector"][2]}$, $|{{\\rm Iso}}|={len(iso)}$', fontsize=7, ha='right', va='top')
fig.savefig(f'{FIGDIR}/fig_symmetry.pdf'); print('ok', [c[1] for c in CASES])
