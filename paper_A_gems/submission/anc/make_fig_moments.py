"""Figure C: why the height-weighted axial moments vanish (row/column sums, lever picture) and the mixed moment sum z*x*y is not forced."""
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
fig = plt.figure(figsize=(6.5, 5.4))

def grid(ax, vals, texts, cmap=CMAP, norm=NORM, fs=9, tcol=None):
    ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect('equal'); ax.axis('off')
    for i in range(n):
        for j in range(n):
            v = vals[i, j]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=cmap(norm(v)), edgecolor='white', lw=1.5))
            lum = np.mean(cmap(norm(v))[:3])
            ax.text(j + .5, i + .5, texts[i][j], ha='center', va='center', fontsize=fs, weight='bold',
                    color='white' if lum < 0.55 else '#222222')

# (a) grid coloured by height with row and column sums
ax = fig.add_axes([0.015, 0.50, 0.40, 0.40])
grid(ax, z1, [[f'{v:+.1f}' for v in r] for r in z1], fs=8.5)
for i in range(n): ax.text(n + 0.15, i + .5, r'$\rho_%d=0$' % i, va='center', fontsize=8.5)
for j in range(n): ax.text(j + .5, n + 0.2, r'$\gamma_%d=0$' % j, ha='center', va='top', fontsize=8.5, rotation=0)
ax.set_xlim(0, n + 1.6); ax.set_ylim(n + .9, -0.1)
fig.text(0.015, 0.975, "(a)  heights $z_{ij}$ of Dürer's square", fontsize=9.5, weight='bold', va='top')
fig.text(0.015, 0.925, r'row sums $\rho_i$ and column sums $\gamma_j$ of the heights', fontsize=8, va='top', color='#333333')
cax = fig.add_axes([0.05, 0.475, 0.22, 0.014])
cb = fig.colorbar(ScalarMappable(NORM, CMAP), cax=cax, orientation='horizontal'); cb.set_ticks([-7.5, 0, 7.5]); cb.ax.tick_params(labelsize=7, length=2)

# (b) lever: forces z_ij at positions x_j
axl = fig.add_axes([0.46, 0.50, 0.52, 0.40]); axl.set_xlim(-2.5, 2.5); axl.set_ylim(-1.95, 1.0); axl.axis('off')
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
axl.text(0, 0.02, '', ha='center')
fig.text(0.46, 0.975, r'(b)  the heights as forces on a lever', fontsize=9.5, weight='bold', va='top')
fig.text(0.46, 0.925, r'arrow = height $z_{ij}$ at position $x_j$ (up $+$, down $-$)', fontsize=8, va='top', color='#333333')
fig.text(0.72, 0.425, r'$\sum z\,x=\sum_j x_j\gamma_j=0$', ha='center', va='top', fontsize=10.5,
         bbox=dict(boxstyle='round,pad=0.35', fc='#F4F1EC', ec='#999999', lw=0.6))
fig.text(0.72, 0.345, r'each column balances, so the whole lever balances', ha='center', va='top', fontsize=8, color='#333333')

# (c) mixed moment for two magic squares
fig.text(0.015, 0.305, r'(c)  the mixed moment $\sum z\,xy$ is not forced: two magic squares', fontsize=9.5, weight='bold', va='top')
CM2 = LinearSegmentedColormap.from_list('bv2', [BLUE, '#9CC6E3', '#F4F1EC', '#F2B27A', VERM])
N2 = Normalize(-30, 30)
pos = [0.02, 0.265, 0.51, 0.765]
for S, zz, tot, off in ((S1, z1, m1, 0.0), (S2, z2, m2, 0.495)):
    a1 = fig.add_axes([0.02 + off, 0.045, 0.16, 0.20]); grid(a1, zz, [[str(v) for v in r] for r in S], fs=8)
    a2 = fig.add_axes([0.205 + off, 0.045, 0.16, 0.20]); prod = zz * X * Y
    grid(a2, prod, [[f'{v:+.0f}'.replace('+0', '0') if abs(v) >= 0.5 else '0' for v in r] for r in prod], cmap=CM2, norm=N2, fs=7.5)
    fig.text(0.10 + off, 0.265, 'square $S$', ha='center', fontsize=8, va='bottom') if False else None
    a1.set_title('square $S$', fontsize=8, pad=2); a2.set_title(r'$z\,x\,y$ per cell', fontsize=8, pad=2)
    fig.text(0.385 + off, 0.145, r'$\sum z\,xy$' + '\n' + (r'$=0$' if tot == 0 else rf'$={tot:+.0f}$'), fontsize=11 if tot else 11, va='center', ha='left',
             weight='bold', color='k' if tot == 0 else WARN)
fig.savefig(f'{FIGDIR}/fig_moments.pdf'); print('ok')
