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
W, H = 6.5, 7.2
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
ZS = 0.30                                    # drawn thickness of one unit of height
def pile(zv):
    a = abs(zv); k = int(np.floor(a)); return [1.0] * k + ([0.5] if a - k > 0 else [])
for zv in z1.ravel(): assert abs(sum(pile(zv)) - abs(zv)) < 1e-12          # pile height = |z|
P1 = coords(S1)
for lines in (z1, z1.T):                                                    # every row/column: up = down
    for r in lines: assert abs(sum(v for v in r if v > 0) + sum(v for v in r if v < 0)) < 1e-12
axp = A(0.0, 0.62, 3.8, 2.65, projection='3d')
style3d(axp, elev=30, azim=-55); axp.set_zlim(-2.4, 2.6); axp.set_box_aspect((1, 1, 0.72), zoom=1.1); axp.computed_zorder = False
cam = np.array([np.cos(np.radians(-55)), np.sin(np.radians(-55))]); depth = lambda k: P1[k, :2] @ cam
Rr = 0.42
for k in sorted([k for k in range(16) if P1[k, 2] < 0], key=depth):
    x, y, z = P1[k]; zz = 0.0
    for q, d in enumerate(pile(z)):
        disc(axp, x, y, zz - d * ZS, zz, Rr, BLUE, shade(BLUE, 0.5), dark=1.0 if q % 2 == 0 else 0.93); zz -= d * ZS
checkerboard(axp)
for k in sorted([k for k in range(16) if P1[k, 2] > 0], key=depth):
    x, y, z = P1[k]; zz = 0.0
    for q, d in enumerate(pile(z)):
        disc(axp, x, y, zz, zz + d * ZS, Rr, VERM, shade(VERM, 0.5), dark=1.0 if q % 2 == 0 else 0.93); zz += d * ZS
axp.scatter([0], [0], [0], s=55, color='#E4002B', edgecolor='k', linewidths=0.8, depthshade=False, zorder=50)
axp.text(0.12, -0.05, 0.05, '$O$', fontsize=11, color='#E4002B', weight='bold', zorder=60, path_effects=HALO, ha='left', va='bottom')
T(0.1, 0.1, "(a)  piles of checkers: D\u00fcrer's square", fontsize=9.5, weight='bold', va='top')
T(0.1, 0.38, 'pile height $=|z_{ij}|$ (one disc = height $1$);\nup (orange) $z>0$, down (blue) $z<0$ from the board', fontsize=7.8, va='top', color='#333333')
T(1.75, 3.2, r'every row and column: height piled up = height piled down' + '\n' + r'(top row: $7.5+4.5=5.5+6.5$)', fontsize=7.8, ha='center', va='top', color='#333333')

# (b) grid coloured by height with row and column sums
ax = A(4.05, 0.85, 2.45, 2.0)
grid(ax, z1, [[f'{v:+.1f}' for v in r] for r in z1], fs=8.5)
for i in range(n): ax.text(n + 0.15, i + .5, r'$\rho_%d=0$' % i, va='center', fontsize=8.5)
for j in range(n): ax.text(j + .5, n + 0.2, r'$\gamma_%d=0$' % j, ha='center', va='top', fontsize=8.5, rotation=0)
ax.set_xlim(0, n + 1.75); ax.set_ylim(n + .9, -0.1)
T(3.85, 0.1, "(b)  heights $z_{ij}$", fontsize=9.5, weight='bold', va='top')
T(3.85, 0.38, 'row sums $\\rho_i$, column sums $\\gamma_j$', fontsize=7.8, va='top', color='#333333')
cax = A(4.2, 2.85, 1.4, 0.07)
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5]); cb.ax.tick_params(labelsize=7, length=2)

# (c) lever: forces z_ij at positions x_j
axl = A(0.1, 3.95, 3.9, 1.3); axl.set_xlim(-2.5, 2.5); axl.set_ylim(-1.95, 1.0); axl.axis('off')
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
T(0.1, 3.55, r'(c)  the heights as forces on a lever', fontsize=9.5, weight='bold', va='top')
T(0.1, 3.83, r'arrow = height $z_{ij}$ at position $x_j$ (up $+$, down $-$)', fontsize=7.8, va='top', color='#333333')
T(5.15, 4.45, r'$\sum z\,x=\sum_j x_j\gamma_j=0$', ha='center', va='center', fontsize=10.5,
         bbox=dict(boxstyle='round,pad=0.35', fc='#F4F1EC', ec='#999999', lw=0.6))
T(5.15, 5.0, 'each column balances,\nso the whole lever balances', ha='center', va='center', fontsize=8, color='#333333')

# (d) mixed moment for two magic squares
T(0.1, 5.45, r'(d)  the mixed moment $\sum z\,xy$ is not forced: two magic squares', fontsize=9.5, weight='bold', va='top')
CM2 = LinearSegmentedColormap.from_list('bv2', [BLUE, '#9CC6E3', '#F4F1EC', '#F2B27A', VERM])
N2 = Normalize(-30, 30)
for S, zz, tot, off in ((S1, z1, m1, 0.0), (S2, z2, m2, 3.2)):
    a1 = A(0.15 + off, 5.95, 1.1, 1.1); grid(a1, zz, [[str(v) for v in r] for r in S], fs=8)
    a2 = A(1.5 + off, 5.95, 1.1, 1.1); prod = zz * X * Y
    grid(a2, prod, [[f'{v:+.0f}'.replace('+0', '0') if abs(v) >= 0.5 else '0' for v in r] for r in prod], cmap=CM2, norm=N2, fs=7.5)
    a1.set_title('square $S$', fontsize=8, pad=2); a2.set_title(r'$z\,x\,y$ per cell', fontsize=8, pad=2)
    T(2.75 + off, 6.5, r'$\sum z\,xy$' + '\n' + (r'$=0$' if tot == 0 else rf'$={tot:+.0f}$'), fontsize=11, va='center', ha='left',
             weight='bold', color='k' if tot == 0 else WARN)
fig.savefig(f'{FIGDIR}/fig_moments.pdf'); print('ok')
