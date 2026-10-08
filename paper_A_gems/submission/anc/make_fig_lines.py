"""Figure B: heights cancel along every line of Duerer's square; contrast with a non-magic swap."""
from vecfig import *
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.2, foreground='white')]
S = DURER; n = 4
S2 = S.copy(); S2[0, 1], S2[1, 0] = S[1, 0], S[0, 1]            # swap 3 and 5 (non-magic)
LINES = {'row': ('top row', [(0, j) for j in range(4)]),
         'col': ('left column', [(i, 0) for i in range(4)]),
         'diag': ('main diagonal', [(i, i) for i in range(4)]),
         'anti': ('anti-diagonal', [(i, 3 - i) for i in range(4)])}
order = ['row', 'col', 'diag', 'anti']
ZF = -9.4
def dev(Sq, cells): return sum(Sq[c] for c in cells) - 34
# ---- numbers (checked) ----
for k in order:
    assert dev(S, LINES[k][1]) == 0
print('swap 3<->5 deviations:', {k: dev(S2, LINES[k][1]) for k in order})
fig = plt.figure(figsize=(6.5, 7.0))
W = 0.215; xs = [0.05 + 0.238 * c for c in range(4)]

def panel3d(rect, Sq, cells, title):
    ax = fig.add_axes(rect, projection='3d'); style3d(ax, elev=22, azim=-52)
    ax.set_zlim(-9.6, 8.4); ax.set_box_aspect((1, 1, 1.15)); ax.computed_zorder = False
    P = coords(Sq); idx = [i * n + j for i, j in cells]
    floor(ax, ZF, fc='#F0F0F0', ec='#C8C8C8')
    for (i, j) in cells:                                           # highlight the cells of the line
        x0, y0 = j - 1.5 - .5, 1.5 - i - .5
        ax.add_collection3d(Poly3DCollection([[(x0, y0, ZF), (x0 + 1, y0, ZF), (x0 + 1, y0 + 1, ZF), (x0, y0 + 1, ZF)]],
                            facecolor='#9A9A9A', edgecolor='#555555', linewidths=0.6, alpha=0.75, zorder=1))
    for k in range(16):
        if k in idx: continue
        ax.plot([0, P[k, 0]], [0, P[k, 1]], [0, P[k, 2]], color='#C4C4C4', lw=0.7, zorder=2)
        ax.scatter(*P[k], s=6, color='#B0B0B0', depthshade=False, zorder=3)
    for k in idx:
        vec(ax, P[k], lw=2.3, dot=22)
        up = P[k, 2] > 0
        ax.text(P[k, 0], P[k, 1], P[k, 2] + (1.3 if up else -1.3), str(Sq.ravel()[k]), fontsize=8.5, weight='bold',
                ha='center', va='bottom' if up else 'top', color=zcol_strong(P[k, 2]), zorder=20, path_effects=HALO)
    tot = P[idx].sum(0)
    ax.scatter([0], [0], [0], s=22, color='k', depthshade=False, zorder=10)
    fig.text(rect[0] + rect[2] / 2, rect[1] + rect[3] + 0.002, title, fontsize=9, weight='bold', va='bottom', ha='center')
    return ax, tot

def panel_stack(rect, Sq, cells, failed, first=False):
    ax = fig.add_axes(rect)
    z = np.array([Sq[c] - 8.5 for c in cells]); s = np.cumsum(z); st = np.concatenate([[0], s[:-1]])
    for j in range(4):
        c = zcol_strong(z[j])
        ax.bar(j, z[j], bottom=st[j], width=0.62, color=c, alpha=0.92, edgecolor='k', lw=0.5)
        if abs(z[j]) >= 5: ax.text(j, st[j] + z[j] / 2, f'{z[j]:+.1f}', ha='center', va='center', fontsize=7.5, color='white', weight='bold', rotation=90)
        if j < 3: ax.plot([j + 0.31, j + 0.69], [s[j]] * 2, color='k', lw=0.7, ls=':')
    ax.axhline(0, color='k', lw=0.9)
    ax.set_xlim(-0.55, 5.5); ax.set_ylim(-10.5, 10.5)
    ax.set_xticks(range(4)); ax.set_xticklabels([str(Sq[c]) for c in cells], fontsize=9, weight='bold'); ax.tick_params(axis='x', length=0, pad=1)
    ax.set_yticks([-7.5, 0, 7.5]); ax.set_yticklabels(['$-7.5$', '$0$', '$+7.5$'] if first else [], fontsize=7.5)
    if first: ax.set_ylabel('height $z$', fontsize=8, labelpad=1)
    ax.patch.set_alpha(0)
    for sp in ('top', 'right', 'bottom') + (() if first else ('left',)): ax.spines[sp].set_visible(False)
    if not first: ax.tick_params(axis='y', length=0)
    if failed:
        ax.annotate('', xy=(3.95, s[-1]), xytext=(3.95, 0), arrowprops=dict(arrowstyle='-', color=WARN, lw=3.0, shrinkA=0, shrinkB=0))
        ax.plot([3.31, 4.1], [s[-1]] * 2, color=WARN, lw=1.0, ls=':')
        ax.text(4.2, s[-1] / 2, rf'$\delta={s[-1]:+.0f}$', color=WARN, fontsize=10.5, weight='bold', va='center', ha='left')
        pass
    else:
        ax.annotate('', xy=(3.95, 0), xytext=(3.95, s[2]), arrowprops=dict(arrowstyle='->', color='k', lw=1.1, shrinkA=0, shrinkB=0))
        pass
    return ax

BLK = [0.99, 0.5]
def block(top, Sq, head, fails):
    fig.text(0.02, top, head, fontsize=10.5, weight='bold', va='top')
    for c, k in enumerate(order):
        name, cells = LINES[k]
        panel3d([xs[c] - 0.015, top - 0.255, W + 0.01, 0.195], Sq, cells, name)
        z = np.array([Sq[cc] - 8.5 for cc in cells]); d = int(round(z.sum()))
        panel_stack([xs[c] + 0.03, top - 0.395, W - 0.0, 0.125], Sq, cells, d != 0, first=(c == 0))
        xb = np.mean([cc[1] - 1.5 for cc in cells]) * 4; yb = np.mean([1.5 - cc[0] for cc in cells]) * 4
        if d == 0:
            t = r'$\sum z=0$' + '\n' + rf'$\sum\vec p=({xb:g},{yb:g},0)$'
            col = 'k'
        else:
            t = rf'$\sum z={d:+d}\neq0$' + '\n' + rf'$\sum\vec p=({xb:g},{yb:g},{d:+d})$'
            col = WARN
        fig.text(xs[c] + 0.14, top - 0.43, t, ha='center', va='top', fontsize=8.5, color=col)
block(BLK[0], S, "Magic: Dürer's square", False)
block(BLK[1], S2, r"Not magic: Dürer's square with $3$ and $5$ swapped", True)
fig.savefig(f'{FIGDIR}/fig_lines.pdf'); print('ok')
