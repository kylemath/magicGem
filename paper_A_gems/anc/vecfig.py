"""Shared helpers for the vector-representation figures (A: vectors, B: lines, C: moments)."""
from gemfig import *
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle
from matplotlib.cm import ScalarMappable
BLUE, VERM, GREY = OI['blue'], OI['verm'], '#666666'
WARN = '#CC0099'            # warning colour (deviation) - magenta, distinct from blue/vermillion
ZMAX = 7.5
CMAP = LinearSegmentedColormap.from_list('bv', [BLUE, '#9CC6E3', '#F4F1EC', '#F2B27A', VERM])
NORM = Normalize(-ZMAX, ZMAX)
def zcol(z): return CMAP(NORM(z))
def zcol_strong(z):
    """saturated version for lines/text: sign colour, darker for larger |z|"""
    return VERM if z > 0 else BLUE

def coords(S):
    S = np.asarray(S); n = S.shape[0]
    x = np.array([[j - (n - 1) / 2 for j in range(n)] for i in range(n)], float)
    y = np.array([[(n - 1) / 2 - i for j in range(n)] for i in range(n)], float)
    z = S - (n * n + 1) / 2
    return np.stack([x.ravel(), y.ravel(), z.ravel()], 1)

def floor(ax, zf, n=4, fc='#EEEEEE', ec='#BBBBBB'):
    """faint grid of cells at height zf"""
    for i in range(n):
        for j in range(n):
            x0, y0 = j - (n - 1) / 2 - .5, (n - 1) / 2 - i - .5
            sq = [(x0, y0, zf), (x0 + 1, y0, zf), (x0 + 1, y0 + 1, zf), (x0, y0 + 1, zf)]
            ax.add_collection3d(Poly3DCollection([sq], facecolor=fc, edgecolor=ec, linewidths=0.5, alpha=0.45, zorder=0))

def vec(ax, p, lw=2.0, color=None, alpha=1.0, dot=26, hollow=False, zorder=5):
    c = color if color is not None else zcol_strong(p[2])
    ax.plot([0, p[0]], [0, p[1]], [0, p[2]], color=c, lw=lw, alpha=alpha, solid_capstyle='round', zorder=zorder)
    if hollow:
        ax.scatter(*p, s=dot, facecolor='white', edgecolor=c, linewidths=1.3, depthshade=False, zorder=zorder + 1)
    else:
        ax.scatter(*p, s=dot, color=c, edgecolor='k', linewidths=0.5, depthshade=False, zorder=zorder + 1)

def drop(ax, p, zf, color='#888888', lw=0.6):
    ax.plot([p[0], p[0]], [p[1], p[1]], [p[2], zf], color=color, lw=lw, ls=(0, (1.5, 2)), zorder=1)

def shade(c, f):
    """scale an RGB colour by f (f<1 darker)"""
    import matplotlib.colors as mc
    r = np.array(mc.to_rgb(c)); return tuple(np.clip(r * f, 0, 1))

def disc(ax, cx, cy, z0, z1, r, col, edge, nseg=28, zo=0, lw=0.5, dark=1.0):
    """thin cylinder (disc) between heights z0<z1 centred above (cx,cy); side + top + bottom"""
    t = np.linspace(0, 2 * np.pi, nseg + 1)
    xs, ys = cx + r * np.cos(t), cy + r * np.sin(t)
    polys, fcs = [], []
    for k in range(nseg):
        polys.append([(xs[k], ys[k], z0), (xs[k + 1], ys[k + 1], z0), (xs[k + 1], ys[k + 1], z1), (xs[k], ys[k], z1)])
        fcs.append(shade(col, dark * (0.86 + 0.14 * np.cos(0.5 * (t[k] + t[k + 1]) + 0.6))))
    top = list(zip(xs[:-1], ys[:-1], [z1] * nseg)); bot = list(zip(xs[:-1], ys[:-1], [z0] * nseg))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=fcs, edgecolors=fcs, linewidths=0.25, zorder=zo))
    ax.add_collection3d(Poly3DCollection([bot], facecolors=[shade(col, 0.9 * dark)], edgecolors=edge, linewidths=lw, zorder=zo))
    ax.add_collection3d(Poly3DCollection([top], facecolors=[shade(col, dark)], edgecolors=edge, linewidths=lw, zorder=zo))

def checkerboard(ax, n=4, thick=0.10, alpha=0.55, zo=0):
    """thin checkerboard slab centred on z=0 (semi-transparent)"""
    for i in range(n):
        for j in range(n):
            x0, y0 = j - (n - 1) / 2 - .5, (n - 1) / 2 - i - .5
            c = '#8F8A80' if (i + j) % 2 == 0 else '#FFFFFF'
            top = [(x0, y0, thick / 2), (x0 + 1, y0, thick / 2), (x0 + 1, y0 + 1, thick / 2), (x0, y0 + 1, thick / 2)]
            ax.add_collection3d(Poly3DCollection([top], facecolor=c, edgecolor='#888888', linewidths=0.5, alpha=alpha, zorder=zo))
    lim = n / 2
    for (a, b, c_, d) in [((-lim, -lim), (lim, -lim), 0, 0), ((lim, -lim), (lim, lim), 0, 0), ((lim, lim), (-lim, lim), 0, 0), ((-lim, lim), (-lim, -lim), 0, 0)]:
        side = [(a[0], a[1], -thick / 2), (b[0], b[1], -thick / 2), (b[0], b[1], thick / 2), (a[0], a[1], thick / 2)]
        ax.add_collection3d(Poly3DCollection([side], facecolor='#9A958A', edgecolor='#666666', linewidths=0.5, alpha=0.75, zorder=zo))
