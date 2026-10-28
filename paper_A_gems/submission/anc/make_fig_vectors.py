"""Figure 1: (a) Duerer's Melencolia I (1514) with its magic square, balance scale, and 12-vertex polyhedron highlighted,
(b) Duerer's square as a heat map of heights, (c) the 16 vectors from the centroid O, (d) their hull, the 12-vertex Magic Gem."""
from vecfig import *
import matplotlib.patheffects as pe
import matplotlib.image as mpimg
HALO = [pe.withStroke(linewidth=2.5, foreground='white')]
S = DURER; n = 4; N = 16
h = exact_hull(S); P = coords(S)
assert np.allclose(P, h['P'] / 2.0) and abs(P.sum(0)).max() < 1e-12      # sum_ij p_ij = 0
assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all()
V = set(h['vertices'])
_, _inner, _bnd = classify_points(h); assert len(V) == 12 and len(_inner) == 4 and not _bnd     # Duerer: 12 vertices, 4 strictly interior points, no other
ZF = -9.2
fig = plt.figure(figsize=(7.2, 3.35))
ELEV, AZIM = 26, -48
def setup(ax):
    style3d(ax, elev=ELEV, azim=AZIM); ax.set_zlim(-9.4, 8.2); ax.set_box_aspect((1, 1, 1.05)); ax.computed_zorder = False

# (a) Melencolia I (1514) with highlights on the magic square, balance scale, and 12-vertex polyhedron
ax0 = fig.add_axes([0.005, 0.08, 0.225, 0.77]); ax0.axis('off')
img = mpimg.imread(os.path.join(HERE, 'melencolia_1514.jpg'))
H_img, W_img = img.shape[:2]
ax0.imshow(img, cmap='gray', vmin=0, vmax=255, aspect='equal')
# Highlight boxes: magic square, balance scale, Duerer's 12-vertex solid
boxes = [
    (728, 165, 168, 162, VERM, 'square'),
    (452, 72, 142, 275, OI['green'], 'scales'),
    (22, 395, 345, 348, BLUE, '12-vertex\npolyhedron'),
]
for (x0, y0, w0, h0, col, lab) in boxes:
    ax0.add_patch(Rectangle((x0, y0), w0, h0, fill=False, edgecolor='white', lw=2.2, zorder=4))
    ax0.add_patch(Rectangle((x0, y0), w0, h0, fill=False, edgecolor=col, lw=1.3, zorder=5))
ax0.text(812, 152, 'magic square', color=VERM, fontsize=6.5, weight='bold', ha='center', va='bottom', path_effects=HALO, zorder=6)
ax0.text(523, 62, 'scales', color=OI['green'], fontsize=6.5, weight='bold', ha='center', va='bottom', path_effects=HALO, zorder=6)
ax0.text(195, 755, "D\u00fcrer's solid ($V=12$)", color=BLUE, fontsize=6.5, weight='bold', ha='center', va='top', path_effects=HALO, zorder=6)
ax0.set_xlim(0, W_img); ax0.set_ylim(H_img, 0)
fig.text(0.01, 0.965, "(a)  Melencolia I (1514)", fontsize=8.8, weight='bold', va='top')
fig.text(0.01, 0.905, "D\u00fcrer's square, balance scale,\nand $12$-vertex polyhedron", fontsize=7.2, color='#444444', va='top')

# (b) heat map of heights with the line sums outside
ax = fig.add_axes([0.245, 0.21, 0.24, 0.58]); ax.set_aspect('equal'); ax.axis('off'); ax.set_zorder(10)
Z = S - 8.5
for i in range(n):
    for j in range(n):
        c = CMAP(NORM(Z[i, j])); lum = np.mean(c[:3])
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=c, edgecolor='white', lw=1.8))
        ax.text(j + .5, i + .5, str(S[i, j]), ha='center', va='center', fontsize=11, weight='bold', color='white' if lum < 0.55 else '#222222')
for i in range(n):
    ax.text(n + 0.18, i + .5, '34', va='center', ha='left', fontsize=8, color='#333333')
for j in range(n):
    ax.text(j + .5, n + 0.18, '34', ha='center', va='top', fontsize=8, color='#333333')
ax.text(n + 0.18, -0.15, r'$\nearrow$ 34', ha='left', va='bottom', fontsize=7.8, color='#333333')
ax.text(n + 0.18, n + 0.18, r'$\searrow$ 34', ha='left', va='top', fontsize=7.8, color='#333333')
ax.set_xlim(-0.05, n + 1.45); ax.set_ylim(n + 0.9, -0.6)
fig.text(0.25, 0.965, "(b)  D\u00fcrer's square", fontsize=8.8, weight='bold', va='top')
fig.text(0.25, 0.905, 'entry $s$; height $z=s-8.5$;\nevery line sums to $34$', fontsize=7.2, color='#444444', va='top')

# (c) vectors alone
ax = fig.add_axes([0.475, 0.08, 0.275, 0.76], projection='3d'); setup(ax)
floor(ax, ZF)
for k in range(N):
    drop(ax, P[k], ZF)
for k in np.argsort(-P[:, 1]):   # far (large y) first
    vec(ax, P[k], lw=2.0, dot=24)
for k in range(N):
    up = P[k, 2] > 0
    dx = {5: -0.55, 10: -0.25, 11: 0.35, 9: -0.4}.get(int(S.ravel()[k]), 0.0)
    ax.text(P[k, 0] + dx, P[k, 1], P[k, 2] + (1.15 if up else -1.15), str(S.ravel()[k]), fontsize=7.5, weight='bold',
            ha='center', va='bottom' if up else 'top', color=zcol_strong(P[k, 2]), zorder=20, path_effects=HALO)
ax.scatter([0], [0], [0], s=32, color='k', depthshade=False, zorder=30)
ax.text(-0.3, -0.2, -2.6, '$O$', fontsize=10, zorder=30, ha='right', path_effects=HALO)
fig.text(0.505, 0.965, '(c)  16 vectors from $O$', fontsize=8.8, weight='bold', va='top')
fig.text(0.505, 0.905, 'balanced at $O$; above $O$ orange,\nbelow $O$ blue', fontsize=7.2, color='#444444', va='top')

# (d) the gem
ax2 = fig.add_axes([0.73, 0.08, 0.275, 0.76], projection='3d'); setup(ax2)
floor(ax2, ZF)
draw_faces(ax2, h, P, alpha=0.07, lw=0.6)
for k in range(N):
    vec(ax2, P[k], lw=1.4, alpha=0.9, dot=28 if k in V else 24, hollow=(k not in V))
ax2.scatter([0], [0], [0], s=32, color='k', depthshade=False, zorder=30)
ax2.text(-0.3, -0.2, -2.6, '$O$', fontsize=10, zorder=30, ha='right', path_effects=HALO)
fig.text(0.75, 0.965, '(d)  their hull: the Magic Gem', fontsize=8.8, weight='bold', va='top')
fig.text(0.75, 0.905, r'$\bullet$ vertex (12)    $\circ$ interior (4)', fontsize=7.2, color='#444444', va='top')

# shared colourbar
cax = fig.add_axes([0.27, 0.145, 0.17, 0.02])
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5])
cb.ax.tick_params(labelsize=6.5, length=2); cb.set_label('height $z=s-8.5$', fontsize=7, labelpad=1)
fig.savefig(f'{FIGDIR}/fig_vectors.pdf', dpi=300, bbox_inches='tight', pad_inches=0.03); print('ok', len(V))
