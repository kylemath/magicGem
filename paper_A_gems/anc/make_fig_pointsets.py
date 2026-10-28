"""Figure 6 (lower half): the 16 points of three order-four squares as spheres on stems over the floor grid (height picture),
with the symmetry made visible: (d) antipodal pairs through O, (e) pairs exchanged by a half-turn about a horizontal axis, (f) no symmetry
(lower half of Figure 6; the upper half is fig_symmetry.pdf).
Same squares and viewpoint as fig_symmetry.pdf (Duerer, #124, #102)."""
from vecfig import *
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.2, foreground='white')]
ELEV, AZIM = 20, -64
ZF = -8.9
CASES = [(DURER, 'd', 'point reflection', r'$(x,y,z)\mapsto(-x,-y,-z)$', 'associative: Dürer'),
         (SQ[124], 'e', 'half-turn about axis', r'$(x,y,z)\mapsto(x,-y,-z)$', 'self-complementary: #124'),
         (SQ[102], 'f', 'no symmetry', '', 'generic: #102')]
PAIRCOL = ['#2E7D32', '#8E44AD', '#C2185B', '#00838F', '#6D4C41', '#7B8D00', '#455A64', '#E0A800']
RED = '#E4002B'
# ---- exact checks of the pairings drawn ----
def pts(S): return coords(S)
Pd, P124, P102 = [pts(c[0]) for c in CASES]
def pairs_of(P, f):
    """pair index k with the index of the image point f(P[k]); asserts that f is a fixed-point-free involution of the point set"""
    out = {}
    for k in range(len(P)):
        m = [l for l in range(len(P)) if np.allclose(P[l], f(P[k]))]
        assert len(m) == 1 and m[0] != k
        out[k] = m[0]
    assert all(out[out[k]] == k for k in out)
    return sorted({tuple(sorted((k, l))) for k, l in out.items()})
pairsA = pairs_of(Pd, lambda p: -p)
pairsB = pairs_of(P124, lambda p: np.array([p[0], -p[1], -p[2]]))
assert len(pairsA) == 8 and len(pairsB) == 8
for S in (SQ[102], DURER, SQ[124]): assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all() and np.trace(S) == 34 and np.trace(S[::-1]) == 34
for P, f in ((P102, lambda p: -p), (P102, lambda p: np.array([p[0], -p[1], -p[2]])), (P102, lambda p: np.array([-p[0], p[1], -p[2]]))):
    assert not all(any(np.allclose(q, f(p)) for q in P102) for p in P102)    # #102: none of the three candidate maps is a symmetry
fig = plt.figure(figsize=(6.5, 3.15))
cam = np.array([np.cos(np.radians(AZIM)), np.sin(np.radians(AZIM))])
for col, (S, let, name, formula, sub) in enumerate(CASES):
    P = coords(S)
    ax = fig.add_axes([col / 3 - 0.012, 0.13, 0.358, 0.72], projection='3d')
    style3d(ax, elev=ELEV, azim=AZIM); ax.set_zlim(-9.4, 8.4); ax.set_box_aspect((1, 1, 1.12), zoom=1.12); ax.computed_zorder = False
    floor(ax, ZF, fc='#EDEDED', ec='#B8B8B8')
    for p in P:                                              # stems
        ax.plot([p[0], p[0]], [p[1], p[1]], [ZF, p[2]], color='#9A9A9A', lw=0.7, zorder=2)
    if let == 'd':
        for pi, (k, l) in enumerate(pairsA):
            ax.plot(*zip(P[k], P[l]), color=PAIRCOL[pi], lw=1.1, zorder=3)
    if let == 'e':
        for pi, (k, l) in enumerate(pairsB):
            foot = np.array([P[k, 0], 0.0, 0.0])
            assert abs((P[k] - P[l]) @ np.array([1, 0, 0])) < 1e-12 and np.allclose((P[k] + P[l]) / 2, foot)   # midpoint on axis, segment perpendicular to it
            ax.plot(*zip(P[k], P[l]), color=PAIRCOL[pi], lw=1.1, zorder=3)
        ax.plot([-2.5, 2.5], [0, 0], [0, 0], color='k', lw=1.1, ls=(0, (4, 2.5)), zorder=4)
        ax.text(-2.5, 0, 0.4, 'axis', fontsize=7.5, ha='right', va='bottom', zorder=30, path_effects=HALO)
    order = np.argsort(P[:, :2] @ cam * -1)                   # far first
    for k in sorted(range(16), key=lambda k: (P[k, :2] @ cam)):
        c = zcol(P[k, 2]); ec = shade(c[:3], 0.55)
        ax.scatter(*P[k], s=72, facecolor=c, edgecolor=ec, linewidths=0.8, depthshade=False, zorder=5)
    ax.scatter([0], [0], [0], s=95, facecolor=RED, edgecolor='k', linewidths=0.9, depthshade=False, zorder=8)
    ax.text(0.0, -0.1, 1.0, '$O$', fontsize=9.5, color=RED, weight='bold', zorder=30, ha='left', va='bottom', path_effects=HALO)
    fig.text(col / 3 + 0.015, 0.975, f'({let})  {sub}', fontsize=8.5, weight='bold', va='top')
    fig.text(col / 3 + 0.015, 0.915, name + ('\n' + formula if formula else '\nonly the identity'), fontsize=7.8, color='#333333', va='top')
cax = fig.add_axes([0.37, 0.115, 0.26, 0.016])
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5])
cb.ax.tick_params(labelsize=7, length=2); cb.set_label('height $z=s-8.5$ (sphere colour)', fontsize=7.5, labelpad=1)
fig.savefig(f'{FIGDIR}/fig_pointsets.pdf'); print('ok', pairsA, pairsB)
