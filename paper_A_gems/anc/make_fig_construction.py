"""Figure 3: construction of the Magic Gem of the Lo Shu: (a) square, (b) centred cells and heights, (c) point set, (d) gem.
Vector PDF, 6.5 in wide; hull faces from the exact hull code gem_geometry.py."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIGDIR = os.path.join(HERE, '..', 'figures'); os.makedirs(FIGDIR, exist_ok=True)

from gem_geometry import exact_hull

plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'pdf.fonttype': 42, 'mathtext.fontset': 'cm'})
FACE, EDGE, PT, STEM = '#5b8ed6', '#1f3f73', '#1f3f73', '#777777'
LOSHU = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])


def face_cycle(P, fv, normal):
    pts = np.array([P[v] for v in fv], float); c = pts.mean(0)
    nrm = np.array(normal, float); nrm /= np.linalg.norm(nrm)
    e1 = pts[0] - c; e1 -= nrm * (e1 @ nrm); e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
    return pts[np.argsort(np.arctan2((pts - c) @ e2, (pts - c) @ e1))]


def style3d(ax, n, N, elev=24, azim=-58):
    lim = (n - 1) / 2 + 0.4
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-(N - 1) / 2 - 0.5, (N - 1) / 2 + 0.5)
    ax.set_box_aspect((1, 1, 1.15)); ax.view_init(elev=elev, azim=azim)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([]); ax.grid(False)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False; axis.line.set_color('#aaaaaa'); axis.pane.set_edgecolor('#dddddd')


def points(S):
    n = S.shape[0]; N = n * n
    return np.array([[j - (n - 1) / 2, (n - 1) / 2 - i, S[i, j] - (N + 1) / 2] for i in range(n) for j in range(n)])


def draw_gem(ax, S, labels=False, alpha=0.3):
    n = S.shape[0]; N = n * n
    h = exact_hull(S); P = h['P'] / 2.0
    polys = [face_cycle(P, f, key[:3]) for key, f in h['faces'].items()]
    ax.add_collection3d(Poly3DCollection(polys, facecolor=FACE, edgecolor=EDGE, linewidths=0.5, alpha=alpha))
    hv = sorted(h['vertices']); inner = [k for k in range(N) if k not in hv]
    ax.scatter(P[hv, 0], P[hv, 1], P[hv, 2], s=12, c=PT, depthshade=False)
    if inner:
        ax.scatter(P[inner, 0], P[inner, 1], P[inner, 2], s=8, c='#b0433a', depthshade=False)
    if labels:
        for k in range(N):
            ax.text(P[k, 0], P[k, 1], P[k, 2] + 0.35, str(int(S.ravel()[k])), fontsize=6, ha='center')
    style3d(ax, n, N)
    return h


def draw_square(ax, S, title, cell=True):
    n = S.shape[0]
    ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect('equal'); ax.axis('off')
    for i in range(n):
        for j in range(n):
            ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, facecolor='#eef3fb', edgecolor='#555555', lw=0.6))
            ax.text(j + 0.5, n - 1 - i + 0.5, str(S[i, j]), ha='center', va='center', fontsize=9)
    ax.set_title(title, loc='left', pad=2)


fig = plt.figure(figsize=(6.5, 1.75))
gs = fig.add_gridspec(1, 4, wspace=0.12, left=0.01, right=0.99, top=0.88, bottom=0.02)

# (a) the Lo Shu
ax = fig.add_subplot(gs[0, 0]); draw_square(ax, LOSHU, '(a) Lo Shu $S$')
# (b) centred grid
ax = fig.add_subplot(gs[0, 1]); n = 3
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_aspect('equal'); ax.axis('off')
for i in range(n):
    for j in range(n):
        xx, yy = j - 1, 1 - i
        ax.add_patch(plt.Rectangle((xx - .5, yy - .5), 1, 1, facecolor='white', edgecolor='#555555', lw=0.6))
        ax.text(xx, yy + 0.12, f'({xx},{yy})', ha='center', va='center', fontsize=6.5)
        ax.text(xx, yy - 0.22, f'$z={LOSHU[i,j]-5}$', ha='center', va='center', fontsize=6.5, color='#1f3f73')
ax.annotate('', xy=(1.65, -1.55), xytext=(-1.55, -1.55), arrowprops=dict(arrowstyle='->', lw=0.6))
ax.annotate('', xy=(-1.55, 1.65), xytext=(-1.55, -1.55), arrowprops=dict(arrowstyle='->', lw=0.6))
ax.text(1.55, -1.45, '$x$', fontsize=7); ax.text(-1.45, 1.5, '$y$', fontsize=7)
ax.set_title('(b) centred cells, $z_{ij}=s_{ij}-5$', loc='left', pad=2)
# (c) heights as stems
ax = fig.add_subplot(gs[0, 2], projection='3d')
P = points(LOSHU)
segs = [[(p[0], p[1], 0), (p[0], p[1], p[2])] for p in P]
ax.add_collection3d(Line3DCollection(segs, colors=STEM, linewidths=0.8))
ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=12, c=PT, depthshade=False)
for k, p in enumerate(P):
    ax.text(p[0], p[1], p[2] + 0.45, str(int(LOSHU.ravel()[k])), fontsize=6, ha='center')
gx, gy = np.meshgrid([-1.5, -.5, .5, 1.5], [-1.5, -.5, .5, 1.5])
ax.plot_wireframe(gx, gy, np.zeros_like(gx), color='#bbbbbb', lw=0.4)
style3d(ax, 3, 9); ax.set_title('(c) the point set', loc='left', pad=2)
# (d) hull
ax = fig.add_subplot(gs[0, 3], projection='3d')
h = draw_gem(ax, LOSHU)
V, E, F = h['f_vector']
ax.set_title(f'(d) gem, $f=({V},{E},{F})$', loc='left', pad=2)

assert h['f_vector'] == (8, 16, 10) and h['volume'] == 18
outpdf = f'{FIGDIR}/fig_construction.pdf'
fig.savefig(outpdf)
print('wrote', outpdf)
