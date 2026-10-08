"""Part D: figures (vector PDF)."""
import json, os, sys
from fractions import Fraction
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gem_geometry import exact_hull
from siamese_util import siamese

ROOT = '/Users/kylemathewson/magicGem'
SQ = np.load(f'{ROOT}/Analysis/data/magic_squares_880 (1).npy')
R = json.load(open(f'{HERE}/results_geometry.json'))

plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
                     'pdf.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#888888', 'xtick.color': '#555555', 'ytick.color': '#555555',
                     'axes.labelcolor': '#222222'})
BAR = '#3b6fb6'      # single hue for magnitude bars
FACE = '#5b8ed6'
EDGE = '#1f3f73'
INNER = '#b0433a'


def face_cycle(P, face_vertices, normal):
    """cyclic order of a facet's vertices (convex polygon) for rendering"""
    pts = np.array([P[v] for v in face_vertices], float)
    c = pts.mean(0)
    nrm = np.array(normal, float); nrm /= np.linalg.norm(nrm)
    e1 = pts[0] - c; e1 -= nrm * (e1 @ nrm); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nrm, e1)
    ang = np.arctan2((pts - c) @ e2, (pts - c) @ e1)
    return pts[np.argsort(ang)]


def render_gem(ax, S, title=None, elev=22, azim=-55, annotate=True):
    S = np.asarray(S); n = S.shape[0]; N = n * n
    h = exact_hull(S)
    P = h['P'] / 2.0  # back to paper coordinates
    polys = [face_cycle(P, f, key[:3]) for key, f in h['faces'].items()]
    coll = Poly3DCollection(polys, facecolor=FACE, edgecolor=EDGE, linewidths=0.6, alpha=0.28)
    ax.add_collection3d(coll)
    hv = set(h['vertices'])
    inner = [k for k in range(N) if k not in hv]
    ax.scatter(P[list(hv), 0], P[list(hv), 1], P[list(hv), 2], s=14, c=EDGE, depthshade=False, zorder=5)
    if inner:
        ax.scatter(P[inner, 0], P[inner, 1], P[inner, 2], s=9, c=INNER, depthshade=False, zorder=5)
    lim = (n - 1) / 2 + 0.3
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-(N - 1) / 2 - 0.5, (N - 1) / 2 + 0.5)
    ax.set_box_aspect((1, 1, 1.1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    ax.grid(False)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.line.set_color('#aaaaaa'); axis.pane.set_edgecolor('#dddddd')
    V, E, F = h['f_vector']
    if title:
        ax.set_title(title, pad=2)
    if annotate:
        ax.text2D(0.5, -0.01, f"$f=({V},{E},{F})$, $V/N={V}/{N}$\nvolume ${h['volume']}$",
                  transform=ax.transAxes, fontsize=8, va='top', ha='center')
    return h


# ------------------------------------------------------------------ Figure 1
fig = plt.figure(figsize=(6.5, 5.0))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.25], hspace=0.15, wspace=0.45)

# (a) vertex counts
ax = fig.add_subplot(gs[0, 0])
vc = {int(k): v for k, v in R['vertex_count_distribution'].items()}
ks = sorted(vc)
ax.bar(ks, [vc[k] for k in ks], color=BAR, width=0.8)
for k in ks:
    ax.text(k, vc[k] + 5, str(vc[k]), ha='center', va='bottom', fontsize=8, color='#222222')
ax.set_xlabel('hull vertices $V$'); ax.set_ylabel('number of squares')
ax.set_xticks(ks); ax.set_xticklabels([str(k) for k in ks], fontsize=7); ax.set_ylim(0, 430)
ax.set_title('(a) hull vertex count', loc='left')

# (b) volumes
ax = fig.add_subplot(gs[0, 1])
vols = []
for k, v in R['volume_distribution'].items():
    vols += [float(Fraction(k))] * v
ax.hist(vols, bins=np.arange(57, 99, 2), color=BAR, edgecolor='white', linewidth=0.5)
ax.set_xlabel('volume of gem'); ax.set_ylabel('number of squares')
ax.set_title('(b) volume (155 distinct values)', loc='left')
ax.axvline(float(Fraction(R['volume_min'])), color='#555555', lw=0.6, ls=':')
ax.axvline(float(Fraction(R['volume_max'])), color='#555555', lw=0.6, ls=':')
ax.text(float(Fraction(R['volume_min'])) + 0.5, ax.get_ylim()[1] * 0.92, f"min {R['volume_min']}", fontsize=8)
ax.text(float(Fraction(R['volume_max'])) - 0.5, ax.get_ylim()[1] * 0.92, f"max {R['volume_max']}", fontsize=8, ha='right')

# (c) combinatorial type sizes
ax = fig.add_subplot(gs[0, 2])
ts = {int(k): v for k, v in R['combinatorial_type_size_distribution'].items()}
sizes = sorted(ts)
x = np.arange(len(sizes))
ax.bar(x, [ts[s] for s in sizes], color=BAR, width=0.8)
for xi, s in zip(x, sizes):
    ax.text(xi, ts[s] + 3, str(ts[s]), ha='center', va='bottom', fontsize=7, color='#222222')
ax.set_xticks(x); ax.set_xticklabels([str(s) for s in sizes], fontsize=7, rotation=90)
ax.set_xlabel('squares per combinatorial type'); ax.set_ylabel('number of types')
ax.set_title(f"(c) {R['n_combinatorial_types']} combinatorial types", loc='left')
ax.set_ylim(0, 230)

# (d) extreme gems
k8 = R['extremes']['eight_vertex'][1]['index']   # the (8,14,8) gem: smallest f-vector
k16 = R['extremes']['sixteen_vertex'][0]['index']
# choose the 16-vertex gem with the largest volume for a clear picture
k16 = max(R['extremes']['sixteen_vertex'], key=lambda e: float(Fraction(e['volume'])))['index']
ax = fig.add_subplot(gs[1, 0], projection='3d')
render_gem(ax, SQ[k8], title=f'(d) $V=8$ (square #{k8})')
ax = fig.add_subplot(gs[1, 1], projection='3d')
render_gem(ax, SQ[k16], title=f'(e) $V=16$ (square #{k16})')
ax = fig.add_subplot(gs[1, 2], projection='3d')
kmax = R['extremes']['max_volume']['index']
render_gem(ax, SQ[kmax], title=f'(f) max volume (square #{kmax})')
fig.savefig(f'{HERE}/fig_gem_geometry_880.pdf', bbox_inches='tight')
print('wrote fig_gem_geometry_880.pdf; gems shown:', k8, k16, kmax)
print(SQ[k8]); print(SQ[k16]); print(SQ[kmax])

# ------------------------------------------------------------------ Figure 2: cross order
LOSHU = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
DURER = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
SIAM5 = siamese(5)
fig = plt.figure(figsize=(6.5, 2.7))
for col, (S, name) in enumerate([(LOSHU, 'Lo Shu ($n=3$)'), (DURER, "Dürer ($n=4$)"), (SIAM5, 'Siamese ($n=5$)')]):
    ax = fig.add_subplot(1, 3, col + 1, projection='3d')
    h = render_gem(ax, S, title=f'({"abc"[col]}) {name}')
    print(name, h['f_vector'], h['volume'])
fig.subplots_adjust(wspace=0.05, left=0.02, right=0.98, top=0.92, bottom=0.08)
fig.savefig(f'{HERE}/fig_gems_cross_order.pdf', bbox_inches='tight')
print('wrote fig_gems_cross_order.pdf')
