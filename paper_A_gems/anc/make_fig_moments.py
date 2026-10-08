"""Figure 4: Duerer's square as piles of checkers on a checkerboard; every row and column carries 34 checkers, so the centre of mass
of all the checkers lies over the centre O of the board."""
from vecfig import *
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrow, Polygon
n = 4
X = np.array([[j - 1.5 for j in range(n)] for i in range(n)]); Y = np.array([[1.5 - i] * n for i in range(n)])
S1 = DURER
def z_of(S): return S - 8.5
# ---- exact checks ----
S = S1
assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all() and np.trace(S) == 34 and np.trace(S[::-1]) == 34
assert abs((z_of(S) * X).sum()) < 1e-12 and abs((z_of(S) * Y).sum()) < 1e-12
W, H = 3.9, 2.95
fig = plt.figure(figsize=(W, H))
def A(x, ytop, w, h, **kw):
    """axes from inch coordinates (x from left, ytop from top, width, height)"""
    return fig.add_axes([x / W, 1 - (ytop + h) / H, w / W, h / H], **kw)
def T(x, y, s, **kw):
    """figure text at inch coordinates (y from top)"""
    return fig.text(x / W, 1 - y / H, s, **kw)
def grid(ax, vals, texts, cmap=CMAP, norm=NORM, fs=9, tcol=None):
    ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect('equal'); ax.axis('off')
    for i in range(n):
        for j in range(n):
            v = vals[i, j]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=cmap(norm(v)), edgecolor='white', lw=1.5))
            lum = np.mean(cmap(norm(v))[:3])
            ax.text(j + .5, i + .5, texts[i][j], ha='center', va='center', fontsize=fs, weight='bold',
                    color='white' if lum < 0.55 else '#222222')

# (a) piles of checkers: one disc = height 1 (last disc = half), up = orange, down = blue, board = plane z=0, O = centre
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.5, foreground='white')]
ZS = 0.075                                    # drawn thickness of one checker
P1 = coords(S1)
cnt = S1                                     # the pile on cell (i,j) has s_ij checkers
assert cnt.sum(0).tolist() == [34] * 4 and cnt.sum(1).tolist() == [34] * 4           # 34 checkers in every row and column
assert (cnt.ravel() * P1[:, 0]).sum() == 0 and (cnt.ravel() * P1[:, 1]).sum() == 0     # centre of mass of the checkers lies over O
assert P1[:, 0].sum() == 0 and P1[:, 1].sum() == 0
axp = A(0.2, 0.6, 3.6, 2.0, projection='3d')
style3d(axp, elev=48, azim=-80); axp.set_zlim(-0.1, 1.6); axp.set_box_aspect((1, 1, 0.45), zoom=1.2); axp.computed_zorder = False
checkerboard(axp, alpha=0.9)
cam = np.array([np.cos(np.radians(-80)), np.sin(np.radians(-80))]); depth = lambda k: P1[k, :2] @ cam
Rr = 0.38
for k in sorted(range(16), key=depth):
    x, y, z = P1[k]; col = CMAP(NORM(cnt.ravel()[k] - 8.5))[:3]    # same colour mapping as panels (b)-(d)
    for q in range(int(cnt.ravel()[k])):
        disc(axp, x, y, 0.05 + q * ZS, 0.05 + (q + 1) * ZS, Rr, col, shade(col, 0.5), dark=1.0 if q % 2 == 0 else 0.93, nseg=20, lw=0.35)
for k in range(16):
    axp.text(P1[k, 0], P1[k, 1], 0.05 + cnt.ravel()[k] * ZS + 0.01, str(cnt.ravel()[k]), fontsize=6.5, weight='bold', ha='center', va='center', zorder=40, path_effects=[pe.withStroke(linewidth=1.8, foreground='white')])
axp.scatter([0], [0], [0.06], s=55, color='#E4002B', edgecolor='k', linewidths=0.8, depthshade=False, zorder=50)
axp.text(-0.08, 0.08, 0.1, '$O$ ', fontsize=11, color='#E4002B', weight='bold', zorder=60, path_effects=HALO, ha='left', va='bottom')
T(0.1, 0.1, "checkers on a checkerboard", fontsize=9.5, weight='bold', va='top')
T(0.1, 0.38, 'cell $(i,j)$ carries $s_{ij}$ checkers (number and\ncolour = the entry $s_{ij}$)', fontsize=7.8, va='top', color='#333333')
T(1.95, 2.62, r'$34$ checkers in every row and column;' + '\n' + r'so the centre of mass of all the checkers lies over $O$', fontsize=7.8, ha='center', va='top', color='#333333')

cbp = fig.colorbar(ScalarMappable(Normalize(1, 16), CMAP), cax=A(0.12, 0.95, 0.08, 1.1), orientation='vertical')
cbp.set_ticks([1, 8, 16]); cbp.ax.tick_params(labelsize=7, length=2); cbp.set_label('entry $s$', fontsize=7.5, labelpad=1)
fig.savefig(f'{FIGDIR}/fig_moments.pdf'); print('ok')
