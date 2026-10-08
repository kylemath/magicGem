"""Figure 4: height-weighted moments: (a) piles of checkers on a checkerboard, (b) heights with row/column sums, (c) lever picture, (d) the mixed moment sum z*x*y is not forced."""
from vecfig import *
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrow, Polygon
n = 4
X = np.array([[j - 1.5 for j in range(n)] for i in range(n)]); Y = np.array([[1.5 - i] * n for i in range(n)])
S1 = DURER; S2 = SQ[45]                          # P_xy = 0 (associative) and |P_xy| = 60
def z_of(S): return S - 8.5
# ---- exact checks ----
z1, z2 = z_of(S1), z_of(S2)
for S in (S1, S2):
    assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all() and np.trace(S) == 34 and np.trace(S[::-1]) == 34
    assert abs((z_of(S) * X).sum()) < 1e-12 and abs((z_of(S) * Y).sum()) < 1e-12
m1, m2 = (z1 * X * Y).sum(), (z2 * X * Y).sum()
print('sum z x y: Durer', m1, ' square #45', m2, S2.tolist()); assert m1 == 0 and m2 == 60
W, H = 6.5, 6.25
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
T(0.1, 0.1, "(a)  checkers on a checkerboard", fontsize=9.5, weight='bold', va='top')
T(0.1, 0.38, 'cell $(i,j)$ carries $s_{ij}$ checkers (number and\ncolour = the entry $s_{ij}$)', fontsize=7.8, va='top', color='#333333')
T(1.95, 2.62, r'$34$ checkers in every row and column;' + '\n' + r'their centre of mass lies over $O$ ($\sum s\,x=\sum s\,y=0$)', fontsize=7.8, ha='center', va='top', color='#333333')

cbp = fig.colorbar(ScalarMappable(Normalize(1, 16), CMAP), cax=A(0.12, 0.95, 0.08, 1.1), orientation='vertical')
cbp.set_ticks([1, 8, 16]); cbp.ax.tick_params(labelsize=7, length=2); cbp.set_label('entry $s$', fontsize=7.5, labelpad=1)
# (b) grid coloured by height with row and column sums
ax = A(4.05, 0.75, 2.45, 1.75)
grid(ax, z1, [[f'{v:+.1f}' for v in r] for r in z1], fs=8.5)
for i in range(n): ax.text(n + 0.15, i + .5, r'$\rho_%d=0$' % i, va='center', fontsize=8.5)
for j in range(n): ax.text(j + .5, n + 0.2, r'$\gamma_%d=0$' % j, ha='center', va='top', fontsize=8.5, rotation=0)
ax.set_xlim(0, n + 1.75); ax.set_ylim(n + .9, -0.1)
T(3.85, 0.1, "(b)  heights $z_{ij}$", fontsize=9.5, weight='bold', va='top')
T(3.85, 0.38, 'row sums $\\rho_i$, column sums $\\gamma_j$', fontsize=7.8, va='top', color='#333333')
cax = A(4.2, 2.62, 1.4, 0.06)
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5]); cb.ax.tick_params(labelsize=7, length=2)

# (c) lever: forces z_ij at positions x_j
axl = A(0.1, 3.5, 3.9, 1.15); axl.set_xlim(-2.5, 2.5); axl.set_ylim(-1.95, 1.0); axl.axis('off')
axl.plot([-2.2, 2.2], [0, 0], color='k', lw=3, solid_capstyle='butt', zorder=3)
axl.add_patch(Polygon([[-0.17, -0.0], [0.17, 0.0], [0, -0.30]], closed=True, facecolor='#444444', edgecolor='k', zorder=4))
for j in range(n):
    xj = j - 1.5
    axl.add_patch(Rectangle((xj - 0.43, -1.05), 0.86, 1.95, facecolor='#F1EFEA', edgecolor='none', zorder=0))
    for i in range(n):
        v = z1[i, j]; dx = (i - 1.5) * 0.17
        c = zcol_strong(v)
        axl.add_patch(FancyArrow(xj + dx, 0, 0, v / 7.5 * 0.8, width=0.045, head_width=0.11, head_length=0.09, length_includes_head=True,
                                 color=c, lw=0, zorder=5))
    axl.text(xj, -1.0, rf'$x_{j}={xj:+.1f}$', ha='center', va='top', fontsize=8)
    axl.text(xj, -1.45, rf'$\gamma_{j}=0$', ha='center', va='top', fontsize=8.5, weight='bold')
T(0.1, 3.05, r'(c)  the heights as forces on a lever', fontsize=9.5, weight='bold', va='top')
T(0.1, 3.33, r'arrow = height $z_{ij}$ at position $x_j$ (up $+$, down $-$)', fontsize=7.8, va='top', color='#333333')
T(5.15, 3.95, r'$\sum z\,x=\sum_j x_j\gamma_j=0$', ha='center', va='center', fontsize=10.5,
         bbox=dict(boxstyle='round,pad=0.35', fc='#F4F1EC', ec='#999999', lw=0.6))
T(5.15, 4.4, 'each column balances,\nso the whole lever balances', ha='center', va='center', fontsize=8, color='#333333')

# (d) mixed moment for two magic squares
T(0.1, 4.7, r'(d)  the mixed moment $\sum z\,xy$ is not forced: two magic squares', fontsize=9.5, weight='bold', va='top')
CM2 = LinearSegmentedColormap.from_list('bv2', [BLUE, '#9CC6E3', '#F4F1EC', '#F2B27A', VERM])
N2 = Normalize(-30, 30)
for S, zz, tot, off in ((S1, z1, m1, 0.0), (S2, z2, m2, 3.2)):
    a1 = A(0.15 + off, 5.15, 0.95, 0.95); grid(a1, zz, [[str(v) for v in r] for r in S], fs=8)
    a2 = A(1.45 + off, 5.15, 0.95, 0.95); prod = zz * X * Y
    grid(a2, prod, [[f'{v:+.0f}'.replace('+0', '0') if abs(v) >= 0.5 else '0' for v in r] for r in prod], cmap=CM2, norm=N2, fs=7.5)
    a1.set_title('square $S$', fontsize=8, pad=2); a2.set_title(r'$z\,x\,y$ per cell', fontsize=8, pad=2)
    T(2.6 + off, 5.62, r'$\sum z\,xy$' + '\n' + (r'$=0$' if tot == 0 else rf'$={tot:+.0f}$'), fontsize=11, va='center', ha='left',
             weight='bold', color='k' if tot == 0 else WARN)
fig.savefig(f'{FIGDIR}/fig_moments.pdf'); print('ok')
