"""Figure A: Duerer's square as 16 vectors from the centroid O (left), and inside its Magic Gem (right)."""
from vecfig import *
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.5, foreground='white')]
S = DURER; n = 4; N = 16
h = exact_hull(S); P = coords(S)
assert np.allclose(P, h['P'] / 2.0) and abs(P.sum(0)).max() < 1e-12      # sum_ij p_ij = 0
V = set(h['vertices'])
ZF = -9.2
fig = plt.figure(figsize=(6.5, 3.9))
ELEV, AZIM = 26, -48
def setup(ax):
    style3d(ax, elev=ELEV, azim=AZIM); ax.set_zlim(-9.4, 8.2); ax.set_box_aspect((1, 1, 1.05)); ax.computed_zorder = False
# (a) vectors alone
ax = fig.add_axes([-0.02, 0.02, 0.54, 0.86], projection='3d'); setup(ax)
floor(ax, ZF)
for k in range(N):
    drop(ax, P[k], ZF)
for k in np.argsort(-P[:, 0] * np.sin(np.radians(AZIM)) * 0 + P[:, 1]):   # far (large y) first
    vec(ax, P[k], lw=2.4, dot=30)
for k in range(N):
    up = P[k, 2] > 0
    dx = {5: -0.55, 10: 0.45, 9: -0.4}.get(int(S.ravel()[k]), 0.0)
    ax.text(P[k, 0] + dx, P[k, 1], P[k, 2] + (1.15 if up else -1.15), str(S.ravel()[k]), fontsize=8.5, weight='bold',
            ha='center', va='bottom' if up else 'top', color=zcol_strong(P[k, 2]), zorder=20, path_effects=HALO)
ax.scatter([0], [0], [0], s=40, color='k', depthshade=False, zorder=30)
ax.text(-0.3, -0.2, -2.6, '$O$', fontsize=12, zorder=30, ha='right', path_effects=HALO)
fig.text(0.015, 0.93, '(a)  16 vectors from $O$', fontsize=9.5, weight='bold')
fig.text(0.015, 0.865, 'label = entry, colour = height $z$', fontsize=8, color='#444444')
# (b) the gem
ax2 = fig.add_axes([0.46, 0.02, 0.54, 0.86], projection='3d'); setup(ax2)
floor(ax2, ZF)
draw_faces(ax2, h, P, alpha=0.07, lw=0.6)
for k in range(N):
    vec(ax2, P[k], lw=1.6, alpha=0.9, dot=34 if k in V else 30, hollow=(k not in V))
ax2.scatter([0], [0], [0], s=40, color='k', depthshade=False, zorder=30)
ax2.text(-0.3, -0.2, -2.6, '$O$', fontsize=12, zorder=30, ha='right', path_effects=HALO)
fig.text(0.55, 0.93, '(b)  their hull: the Magic Gem', fontsize=9.5, weight='bold')
fig.text(0.55, 0.865, r'$\bullet$ vertex (12)    $\circ$ interior tip (4)', fontsize=8, color='#444444')
fig.text(0.5, 0.012, r'$\sum\,\vec{p}_{ij}=\vec{0}$ for every arrangement:  $O$ is the centroid of the 16 tips', ha='center', fontsize=9)
# colourbar
cax = fig.add_axes([0.39, 0.125, 0.22, 0.02])
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5])
cb.ax.tick_params(labelsize=7, length=2); cb.set_label('height $z=s-8.5$', fontsize=7.5, labelpad=1)
fig.savefig(f'{FIGDIR}/fig_vectors.pdf'); print('ok', len(V))
