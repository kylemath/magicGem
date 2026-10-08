"""Figure 1: (a) Duerer's square as a heat map of heights, (b) the 16 vectors from the centroid O, (c) their hull, the Magic Gem."""
from vecfig import *
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.5, foreground='white')]
S = DURER; n = 4; N = 16
h = exact_hull(S); P = coords(S)
assert np.allclose(P, h['P'] / 2.0) and abs(P.sum(0)).max() < 1e-12      # sum_ij p_ij = 0
assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all()
V = set(h['vertices'])
ZF = -9.2
fig = plt.figure(figsize=(6.5, 3.5))
ELEV, AZIM = 26, -48
def setup(ax):
    style3d(ax, elev=ELEV, azim=AZIM); ax.set_zlim(-9.4, 8.2); ax.set_box_aspect((1, 1, 1.05)); ax.computed_zorder = False
# (a) heat map of heights with the line sums outside
ax = fig.add_axes([0.0, 0.2, 0.33, 0.6]); ax.set_aspect('equal'); ax.axis('off'); ax.set_zorder(10)
Z = S - 8.5
for i in range(n):
    for j in range(n):
        c = CMAP(NORM(Z[i, j])); lum = np.mean(c[:3])
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=c, edgecolor='white', lw=2))
        ax.text(j + .5, i + .5, str(S[i, j]), ha='center', va='center', fontsize=13, weight='bold', color='white' if lum < 0.55 else '#222222')
for i in range(n):
    ax.text(n + 0.18, i + .5, '34', va='center', ha='left', fontsize=9, color='#333333')
for j in range(n):
    ax.text(j + .5, n + 0.18, '34', ha='center', va='top', fontsize=9, color='#333333')
ax.text(n + 0.18, -0.15, r'$\nearrow$ 34', ha='left', va='bottom', fontsize=8.5, color='#333333')
ax.text(n + 0.18, n + 0.18, r'$\searrow$ 34', ha='left', va='top', fontsize=8.5, color='#333333')
ax.set_xlim(-0.05, n + 1.4); ax.set_ylim(n + 0.9, -0.6)
fig.text(0.015, 0.965, "(a)  D\u00fcrer's square", fontsize=9.5, weight='bold', va='top')
fig.text(0.015, 0.905, 'entry $s$; colour = height $z=s-8.5$;\nevery line sums to $34$', fontsize=7.8, color='#444444', va='top')
# (b) vectors alone
ax = fig.add_axes([0.30, 0.09, 0.37, 0.76], projection='3d'); setup(ax)
floor(ax, ZF)
for k in range(N):
    drop(ax, P[k], ZF)
for k in np.argsort(P[:, 1]):   # far (small y) first
    pass
for k in np.argsort(-P[:, 1]):   # far (large y) first
    vec(ax, P[k], lw=2.2, dot=28)
for k in range(N):
    up = P[k, 2] > 0
    dx = {5: -0.55, 10: 0.45, 9: -0.4}.get(int(S.ravel()[k]), 0.0)
    ax.text(P[k, 0] + dx, P[k, 1], P[k, 2] + (1.15 if up else -1.15), str(S.ravel()[k]), fontsize=8, weight='bold',
            ha='center', va='bottom' if up else 'top', color=zcol_strong(P[k, 2]), zorder=20, path_effects=HALO)
ax.scatter([0], [0], [0], s=36, color='k', depthshade=False, zorder=30)
ax.text(-0.3, -0.2, -2.6, '$O$', fontsize=11, zorder=30, ha='right', path_effects=HALO)
fig.text(0.355, 0.965, '(b)  16 vectors from $O$', fontsize=9.5, weight='bold', va='top')
fig.text(0.355, 0.905, 'label = entry; above $O$ orange,\nbelow $O$ blue', fontsize=7.8, color='#444444', va='top')
# (c) the gem
ax2 = fig.add_axes([0.63, 0.09, 0.37, 0.76], projection='3d'); setup(ax2)
floor(ax2, ZF)
draw_faces(ax2, h, P, alpha=0.07, lw=0.6)
for k in range(N):
    vec(ax2, P[k], lw=1.5, alpha=0.9, dot=32 if k in V else 28, hollow=(k not in V))
ax2.scatter([0], [0], [0], s=36, color='k', depthshade=False, zorder=30)
ax2.text(-0.3, -0.2, -2.6, '$O$', fontsize=11, zorder=30, ha='right', path_effects=HALO)
fig.text(0.655, 0.965, '(c)  their hull: the Magic Gem', fontsize=9, weight='bold', va='top')
fig.text(0.655, 0.905, r'$\bullet$ vertex (12)    $\circ$ interior tip (4)', fontsize=7.8, color='#444444', va='top')
fig.text(0.66, 0.012, r'$\sum\,\vec{p}_{ij}=\vec{0}$ for every arrangement:  $O$ is the centroid of the 16 tips', ha='center', fontsize=9)
# shared colourbar
cax = fig.add_axes([0.05, 0.145, 0.22, 0.02])
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5])
cb.ax.tick_params(labelsize=7, length=2); cb.set_label('height $z=s-8.5$', fontsize=7.5, labelpad=1)
fig.savefig(f'{FIGDIR}/fig_vectors.pdf'); print('ok', len(V))
