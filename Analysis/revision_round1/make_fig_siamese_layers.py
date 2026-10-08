"""Siamese layer figure (round 1, RefB point 15): (a) the five lattice polygons T,U,M,D,B in the (x,y) plane
for n=9 with the twelve vertex cells marked; (b) the affinely reduced gem Phi(G(S)) = conv{(x,y,zeta)} with its
16 facets.  Uses zeta_points from Analysis/revision/gem_geometry/siamese_util.py.  Vector PDF, 6.5 x 2.5 in."""
import os, sys
import numpy as np
from itertools import combinations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, f'{ROOT}/Analysis/revision/gem_geometry')
from siamese_util import zeta_points, siamese_closed_form, siamese

plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'pdf.fonttype': 42, 'mathtext.fontset': 'cm'})
n = 9; m = (n - 1) // 2
assert (siamese(n) == siamese_closed_form(n)).all()
pts = zeta_points(n)                     # (x, y, zeta), integers
zeta = pts[:, 2]
levels = [n + 1, 1, 0, -1, -(n + 1)]
names = {n + 1: 'T', 1: 'U', 0: 'M', -1: 'D', -(n + 1): 'B'}
cols = {n + 1: '#b0433a', 1: '#e0904a', 0: '#3b6fb6', -1: '#6aa36a', -(n + 1): '#7a4fa0'}
assert sorted(set(zeta.tolist())) == sorted(levels)

# the twelve vertices (Proposition: v_1..v_12 in (x,y,zeta))
V = [(-m, m, n + 1), (-1, m, n + 1), (-m, 1, n + 1), (-m, 0, 1), (-m, -m, 0), (0, -m, 0), (0, m, 0), (m, m, 0),
     (m, 0, -1)]
V += [tuple(-np.array(V[0])), tuple(-np.array(V[2])), tuple(-np.array(V[1]))]
V = np.array(V)

# exact hull of the integer points: merge coplanar qhull triangles by their integer plane equation
hull = ConvexHull(pts.astype(float))
planes = {}
for simp in hull.simplices:
    p0, p1, p2 = pts[simp]
    nrm = np.cross(p1 - p0, p2 - p0).astype(np.int64)
    g = np.gcd.reduce(np.abs(nrm)); nrm //= g
    d = -int(nrm @ p0)
    if nrm @ pts.mean(0) + d > 0:
        nrm, d = -nrm, -d
    planes.setdefault((tuple(nrm), d), set()).update(simp.tolist())
faces = {}
for (nrm, d), s in planes.items():
    on = [k for k in range(len(pts)) if int(np.array(nrm) @ pts[k]) + d == 0]
    faces[(nrm, d)] = on
hv = sorted(int(k) for k in hull.vertices)
assert len(faces) == 16 and len(hv) == 12, (len(faces), len(hv))
assert {tuple(pts[k]) for k in hv} == {tuple(v) for v in V}


def cyc(P):
    c = P.mean(0); nrm = np.cross(P[1] - P[0], P[2] - P[0]).astype(float); nrm /= np.linalg.norm(nrm)
    e1 = P[0] - c; e1 = e1 - nrm * (e1 @ nrm); e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
    return P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]


fig = plt.figure(figsize=(6.5, 2.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.0], wspace=0.35, left=0.06, right=0.99, top=0.9, bottom=0.08)

# (a) layers in the plane
ax = fig.add_subplot(gs[0, 0])
for lv in levels:
    sel = pts[zeta == lv]
    ax.scatter(sel[:, 0], sel[:, 1], s=14, c=cols[lv], edgecolors='none', zorder=3,
               label=f'{names[lv]}: $\\zeta={lv:+d}$' if lv != 0 else f'{names[lv]}: $\\zeta=0$')
    if len(sel) >= 3:
        hh = ConvexHull(sel[:, :2].astype(float))
        poly = sel[hh.vertices, :2]
        ax.add_patch(plt.Polygon(poly, closed=True, fill=False, edgecolor=cols[lv], lw=0.9, zorder=2))
ax.scatter(V[:, 0], V[:, 1], s=70, facecolors='none', edgecolors='k', linewidths=0.8, zorder=4)
for k, v in enumerate(V):
    dx, dy = (0.42, 0.42)
    ax.text(v[0] + dx, v[1] + dy, f'$v_{{{k+1}}}$', fontsize=6.5, ha='left', va='bottom', zorder=5)
ax.set_xlim(-m - 0.8, m + 1.3); ax.set_ylim(-m - 0.8, m + 1.3); ax.set_aspect('equal')
ax.set_xticks(range(-m, m + 1)); ax.set_yticks(range(-m, m + 1))
ax.tick_params(labelsize=6, length=2); ax.set_xlabel('$x$', labelpad=1); ax.set_ylabel('$y$', labelpad=1)
ax.legend(frameon=False, fontsize=6.5, loc='upper left', bbox_to_anchor=(1.01, 1.0), handletextpad=0.2, borderaxespad=0.0, labelspacing=0.3)
ax.set_title(f'(a) the five layers, $n={n}$ ($m={m}$)', loc='left')

# (b) the reduced polytope
ax = fig.add_subplot(gs[0, 1], projection='3d')
polys = [cyc(pts[f].astype(float)) for f in faces.values()]
ax.add_collection3d(Poly3DCollection(polys, facecolor='#5b8ed6', edgecolor='#1f3f73', linewidths=0.6, alpha=0.25))
for lv in levels:
    sel = pts[zeta == lv]
    ax.scatter(sel[:, 0], sel[:, 1], sel[:, 2], s=6, c=cols[lv], depthshade=False)
ax.scatter(V[:, 0], V[:, 1], V[:, 2], s=16, c='k', depthshade=False)
for k, v in enumerate(V):
    ax.text(v[0], v[1], v[2] + 0.5, f'$v_{{{k+1}}}$', fontsize=6)
ax.set_xlim(-m - .5, m + .5); ax.set_ylim(-m - .5, m + .5); ax.set_zlim(-n - 1.5, n + 1.5)
ax.set_box_aspect((1, 1, 1.1)); ax.view_init(elev=18, azim=-52)
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([-(n + 1), 0, n + 1]); ax.tick_params(labelsize=6)
ax.set_zlabel('$\\zeta$', labelpad=-4); ax.grid(False)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.fill = False; axis.pane.set_edgecolor('#dddddd')
ax.set_title('(b) $\\Phi(G(S))$: 12 vertices, 16 facets', loc='left')

out = f'{ROOT}/arxiv_submission/figures/fig_siamese_layers.pdf'
fig.savefig(out); fig.savefig(f'{HERE}/fig_siamese_layers.png', dpi=130)
print('wrote', out, '| faces', len(faces), 'vertices', len(hv), 'face sizes', sorted(len(f) for f in faces.values()))
