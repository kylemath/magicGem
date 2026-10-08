"""Shared helpers for the gem figures (matplotlib, vector PDF, Okabe-Ito colour-blind-safe palette)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gem_geometry import exact_hull
FIGDIR = os.path.join(HERE, '..', 'figures'); os.makedirs(FIGDIR, exist_ok=True)
OI = dict(black='#000000', orange='#E69F00', sky='#56B4E9', green='#009E73', yellow='#F0E442',
          blue='#0072B2', verm='#D55E00', purple='#CC79A7')
plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'pdf.fonttype': 42, 'ps.fonttype': 42,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.6})
SQ = np.loadtxt(os.path.join(HERE, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
DURER = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])

def face_cycle(P, fv, normal):
    pts = np.array([P[v] for v in fv], float); c = pts.mean(0)
    nrm = np.array(normal, float); nrm /= np.linalg.norm(nrm)
    e1 = pts[0] - c; e1 -= nrm * (e1 @ nrm); e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
    return pts[np.argsort(np.arctan2((pts - c) @ e2, (pts - c) @ e1))]

def style3d(ax, n=4, elev=20, azim=-62, zl=None):
    N = n * n; lim = (n - 1) / 2 + 0.5
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-(N - 1) / 2 - 0.5, (N - 1) / 2 + 0.5)
    ax.set_box_aspect((1, 1, 1.25)); ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()

def draw_faces(ax, h, P, colors=None, alpha=0.16, default=OI['blue'], lw=0.5):
    keys = list(h['faces'].keys()); polys = [face_cycle(P, h['faces'][k], k[:3]) for k in keys]
    fc = [default] * len(keys); al = [alpha] * len(keys)
    if colors:
        for idx, (c, a) in colors.items(): fc[idx] = c; al[idx] = a
    for poly, c, a in zip(polys, fc, al):
        ax.add_collection3d(Poly3DCollection([poly], facecolor=c, edgecolor=OI['blue'], linewidths=lw, alpha=a, zorder=2))
    return keys, polys
