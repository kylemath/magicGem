#!/usr/bin/env python3
"""Generate the figures of the paper (vector PDF) into ../figures/.
   python3 make_figures.py [decomposition] [random] [kstar]     (default: these three; [swap] writes the supplementary anc/fig_swap_spectrum.pdf, [balance] an optional extra figure)
Needs: numpy, scipy, matplotlib, sympy; mc_hist.npz, mc_results.json, data_witnesses_variances.json, magic4_all7040.txt, kstar_verify.json."""
import itertools, json, math, os, sys
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle
import figstyle as fs
from figstyle import *

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', 'figures')
os.makedirs(FIG, exist_ok=True)


def line_indicators(n):
    j = np.tile(np.arange(n), n); i = np.repeat(np.arange(n), n)
    R = [(i == k) * 1.0 for k in range(n)]; C = [(j == k) * 1.0 for k in range(n)]
    D = [(i == j) * 1.0, (i + j == n - 1) * 1.0]
    return R, C, D


def projections(S):
    """Squared norms (normalised inner product (1/N) sum) of z's orthogonal pieces and line deviations."""
    n = S.shape[0]; N = n * n
    z = S.ravel() - (N + 1) / 2
    R, C, D = line_indicators(n)
    cen = lambda f: f - f.mean()
    def proj_sq(vs):
        B = np.array([cen(v) for v in vs]).T
        coef, *_ = np.linalg.lstsq(B, z, rcond=None)
        p = B @ coef
        return (p @ p) / N
    pR, pC, pD = proj_sq(R), proj_sq(C), proj_sq(D)
    tot = (z @ z) / N
    return dict(R=pR, C=pC, D=pD, rest=tot - pR - pC - pD, tot=tot,
                rho=S.sum(1) - n * (N + 1) // 2, gam=S.sum(0) - n * (N + 1) // 2,
                dm=int(np.trace(S)) - n * (N + 1) // 2, da=int(np.trace(S[:, ::-1])) - n * (N + 1) // 2)


EXAMPLE = np.array([[9, 4, 12, 3], [16, 1, 14, 7], [10, 15, 11, 8], [2, 5, 6, 13]])
DURER = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])


def fig_decomposition():
    fig = plt.figure(figsize=(TEXTWIDTH, 2.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.05, 1.05], wspace=0.28, left=0.01, right=0.99, top=0.88, bottom=0.14)
    # (a) grid with line deviations
    ax = fig.add_subplot(gs[0]); ax.set_aspect('equal'); ax.axis('off')
    S = EXAMPLE; n = 4; P = projections(S)
    z = S - 8.5
    for i in range(n):
        for j in range(n):
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=DIV(0.5 + z[i, j] / 17.0), ec='white', lw=1.2))
            ax.text(j + 0.5, n - 1 - i + 0.5, str(S[i, j]), ha='center', va='center', fontsize=8.5)
    for i in range(n):
        ax.text(n + 0.25, n - 1 - i + 0.5, '%+d' % P['rho'][i], ha='left', va='center', fontsize=7.5, color=DGREY)
    for j in range(n):
        ax.text(j + 0.5, -0.28, '%+d' % P['gam'][j], ha='center', va='top', fontsize=7.5, color=DGREY)
    ax.text(n + 0.25, n + 0.28, r'$\delta_{\rm a}=%d$' % P['da'], ha='left', va='center', fontsize=7.5, color=DGREY)
    ax.text(n + 0.25, -0.28, r'$\delta_{\rm m}=%d$' % P['dm'], ha='left', va='top', fontsize=7.5, color=DGREY)
    ax.annotate('', xy=(0, n), xytext=(n, 0), arrowprops=dict(arrowstyle='-', ls=(0, (2, 2)), color=DGREY, lw=0.6))
    ax.annotate('', xy=(0, 0), xytext=(n, n), arrowprops=dict(arrowstyle='-', ls=(0, (2, 2)), color=DGREY, lw=0.6))
    ax.set_xlim(-0.3, n + 2.1); ax.set_ylim(-1.3, n + 0.7)
    ax.text(n / 2 + 0.8, -0.95, 'column and row deviations', ha='center', va='top', fontsize=7, color=DGREY)
    ax.set_title(r'(a) $z$ and the line deviations $\delta_L$', loc='left', fontsize=8.5, x=-0.02)
    # (b) schematic
    ax = fig.add_subplot(gs[1]); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10.6); ax.set_aspect('equal')
    ax.add_patch(Polygon([(0.5, 2.2), (6.8, 2.2), (9.6, 4.8), (3.3, 4.8)], closed=True, fc='#dbeaf5', ec=BLUE, lw=0.8))
    O = np.array([5.0, 3.5])
    ax.plot([O[0], O[0]], [O[1], 9.4], color=DGREY, lw=0.8)
    ax.text(O[0] + 0.15, 9.3, r'$W^{\perp}\cap\mathbf{1}^{\perp}$', fontsize=8, ha='left', va='bottom')
    ax.text(O[0] + 0.15, 8.6, r'(dim $N\!-\!1\!-\!2n$)', fontsize=7, ha='left', va='bottom', color=DGREY)
    ax.text(1.0, 2.55, r'$W$ (dim $2n$)', fontsize=8, color=BLUE)
    tip = O + np.array([2.7, 4.3]); proj = O + np.array([2.7, 0.0])
    ax.annotate('', xy=proj, xytext=O, arrowprops=dict(arrowstyle='-|>', color=VERM, lw=1.3, shrinkA=0, shrinkB=0))
    ax.annotate('', xy=tip, xytext=O, arrowprops=dict(arrowstyle='-|>', color='black', lw=1.3, shrinkA=0, shrinkB=0))
    ax.plot([proj[0], tip[0]], [proj[1], tip[1]], color=DGREY, lw=0.7, ls=(0, (3, 2)))
    ax.text(tip[0] + 0.15, tip[1] + 0.1, r'$z$', fontsize=9.5)
    ax.text(proj[0] + 0.1, proj[1] - 0.62, r'$P_Wz$', fontsize=9, color=VERM)
    ax.text(proj[0] + 0.2, (proj[1] + tip[1]) / 2, r'$z-P_Wz$', fontsize=8, color=DGREY, va='center')
    ax.annotate('', xy=(O[0], 7.7), xytext=(O[0], O[1]), arrowprops=dict(arrowstyle='-|>', color=GREEN, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(O[0] - 0.2, 7.6, r'$z$ of a' + '\n' + r'magic square', fontsize=7, color=GREEN, ha='right', va='center')
    ax.text(5.0, 1.15, r'$W=W_R\oplus W_C\oplus W_D$', fontsize=8, ha='center')
    ax.text(5.0, 0.35, r'dims $n\!-\!1,\ n\!-\!1,\ 2$', fontsize=7, ha='center', color=DGREY)
    ax.set_title(r'(b) $z\perp W$ if and only if magic', loc='left', fontsize=8.5, x=-0.02)
    # (c) squared-norm decomposition
    ax = fig.add_subplot(gs[2])
    rows = [('example of (a)', projections(EXAMPLE)), (r'$\mathrm{D\ddot{u}rer}$', projections(DURER))]
    cols = [(r'$W_R$ (rows)', BLUE, 'R'), (r'$W_C$ (columns)', SKY, 'C'), (r'$W_D$ (diagonals)', ORANGE, 'D'), (r'complement', LGREY, 'rest')]
    for r, (lab, P) in enumerate(rows):
        left = 0
        for name, col, key in cols:
            v = P[key]
            ax.barh(1 - r, v, left=left, height=0.5, color=col, ec='white', lw=0.6, label=name if r == 0 else None)
            if v > 0.9:
                ax.text(left + v / 2, 1 - r, '%.2f' % v, ha='center', va='center', fontsize=6.5)
            left += v
    ax.set_yticks([1, 0]); ax.set_yticklabels(['example\nof (a)', r'$\mathrm{D\ddot{u}rer}$'+'\n(magic)'], fontsize=7.5)
    ax.set_xlabel(r'squared norm $\|z\|^2=21.25$')
    ax.set_xlim(0, 21.25); ax.set_ylim(-0.55, 2.1)
    ax.legend(loc='upper center', ncol=2, fontsize=6.8, handlelength=1.0, columnspacing=0.8, bbox_to_anchor=(0.45, 1.03))
    ax.set_title(r'(c) $\|z\|^2$ and the subspaces', loc='left', fontsize=8.5, x=-0.02)
    fig.savefig(os.path.join(FIG, 'fig_decomposition.pdf'))
    plt.close(fig)
    print('decomposition:', {k: round(v, 3) for k, v in projections(EXAMPLE).items() if k in ('R', 'C', 'D', 'rest', 'tot')},
          {k: round(v, 3) for k, v in projections(DURER).items() if k in ('R', 'C', 'D', 'rest', 'tot')})


def fig_swap():
    sys.path.insert(0, HERE)
    from balance_lib import magic4_reps
    from verify_numbers import incidence, F_of
    fig, axs = plt.subplots(1, 3, figsize=(TEXTWIDTH, 2.35), gridspec_kw=dict(width_ratios=[1.15, 1.05, 0.8], wspace=0.7))
    # (a) n=3 exhaustive distribution of N^2 E_full
    P = np.array(list(itertools.permutations(range(1, 10))), dtype=np.int64)
    F = F_of(P, 3)
    cnt = Counter(F.tolist()); xs = sorted(cnt)
    ax = axs[0]
    ax.bar(xs, [cnt[v] for v in xs], width=1.6, color=SKY, ec='none', label='other values')
    ax.bar([0], [cnt[0]], width=1.9, color=VERM, zorder=3, label='0: the 8 magic squares')
    ax.bar([2], [cnt[2]], width=1.9, color=ORANGE, zorder=3, label='2: 8 non-magic local minima')
    ax.set_yscale('log'); ax.set_xlim(-4, 184); ax.set_ylim(1, 3e7)
    ax.set_xlabel(r'$N^2E_{\rm full}=\sum_L\delta_L^2$'); ax.set_ylabel('number of arrangements')
    ax.legend(loc='upper right', fontsize=6.3, handlelength=1.0, borderaxespad=0.2, labelspacing=0.2)
    ax.set_title(r'$n=3$, all $9!$ arrangements', fontsize=8, loc='right')
    panel_label(ax, '(a)', x=-0.22)
    # (b) heat map of swap gaps by (d, m), n=4
    reps, _ = magic4_reps(os.path.join(HERE, 'magic4_all7040.txt'))
    A = incidence(4)
    cells = list(itertools.combinations(range(16), 2))
    mm = np.array([int(((A[:, a] - A[:, b]) != 0).sum()) for a, b in cells])
    H = np.zeros((15, 5), int)
    vals = Counter()
    for S in reps:
        S = S.astype(int)
        for k, (a, b) in enumerate(cells):
            d = abs(S[a] - S[b]); H[d - 1, mm[k] - 2] += 1; vals[d * d * mm[k]] += 1
    ax = axs[1]
    im = ax.imshow(np.where(H > 0, H, np.nan).T, origin='lower', aspect='auto', cmap='Blues', norm=matplotlib_lognorm(H))
    ax.set_xticks(range(0, 15, 2)); ax.set_xticklabels([str(d) for d in range(1, 16, 2)])
    ax.set_yticks(range(5)); ax.set_yticklabels(['2', '3', '4', '5', '6'])
    ax.set_xlabel(r'value difference $d$'); ax.set_ylabel(r'separating lines $\lambda$')
    ax.spines['top'].set_visible(True); ax.spines['right'].set_visible(True)
    ax.set_title(r'$n=4$: gap $d^2\lambda$', fontsize=8, loc='right')
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03); cb.ax.tick_params(labelsize=6.5)
    cb.set_label('number of swaps', fontsize=7)
    cb.outline.set_linewidth(0.4)
    panel_label(ax, '(b)', x=-0.22)
    # (c) minimum gap per square
    ax = axs[2]
    m4 = {2: 432, 3: 420, 4: 28}
    chk = Counter()
    for S in reps:
        S = S.astype(int)
        best = min(abs(S[a] - S[b]) ** 2 * mm[k] for k, (a, b) in enumerate(cells))
        chk[best] += 1
    assert dict(chk) == m4, chk
    ax.bar([2, 3, 4], [chk[2], chk[3], chk[4]], color=BLUE, width=0.62)
    for v in (2, 3, 4):
        ax.text(v, chk[v] + 12, str(chk[v]), ha='center', fontsize=7.5)
    ax.set_xticks([2, 3, 4]); ax.set_ylim(0, 520)
    ax.set_xlabel(r'smallest gap $g_{\min}(S)$'); ax.set_ylabel('magic squares')
    ax.set_title(r'$n=4$, 880 squares', fontsize=8, loc='right')
    panel_label(ax, '(c)', x=-0.28)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.9, bottom=0.2)
    fig.savefig(os.path.join(HERE, 'fig_swap_spectrum.pdf'))  # supplementary (anc/), not in the paper
    plt.close(fig)
    print('swap: distinct', len(vals), 'min', min(vals), 'max', max(vals), 'mins', dict(chk))


def matplotlib_lognorm(H):
    from matplotlib.colors import LogNorm
    return LogNorm(vmin=max(1, H[H > 0].min()), vmax=H.max())


def fig_random():
    import sympy as sp
    from theory import mean_energy_closed, weights_closed
    from density import mixture_pdf
    from energies import all_energies
    from exhaustive_n3 import all_perms_n3
    hist = np.load(os.path.join(HERE, 'mc_hist.npz'))
    mc = json.load(open(os.path.join(HERE, 'mc_results.json')))
    poly = json.load(open(os.path.join(HERE, 'data_witnesses_variances.json')))['variance_polynomials']
    nn = sp.symbols('n')
    fvar = {w: {p: sp.lambdify(nn, sp.sympify(poly[w][p]['expr']), 'math') for p in ('odd', 'even')} for w in ('low', 'full')}
    var_exact = lambda n, w: float(fvar[w]['odd' if n % 2 else 'even'](n))
    E3 = all_energies(all_perms_n3())
    COL = {3: BLUE, 5: VERM, 8: GREEN}
    fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, 2.4))
    bins_norm = np.linspace(0, 5, 61)
    for ax, key, which, title in ((axes[0], 'E_low', 'low', 'E_4'), (axes[1], 'E_full', 'full', 'E_{\\rm full}')):
        for n in (3, 5, 8):
            m = float(mean_energy_closed(n, which))
            if n == 3:
                dens, _ = np.histogram(E3[key] / m, bins=bins_norm, density=True); lab = r'$n=3$ (all $9!$)'
            else:
                h = hist['n%d_%s' % (n, key)]; edges = hist['n%d_edges_%s' % (n, which)] / m
                cum = np.concatenate([[0.0], np.cumsum(h)])
                dens = np.diff(np.interp(bins_norm, edges, cum)) / (h.sum() * (bins_norm[1] - bins_norm[0])); lab = r'$n=%d$ (MC, $10^8$)' % n
            ax.stairs(dens, bins_norm, color=COL[n], lw=0.9); ax.plot([], [], color=COL[n], lw=0.9, label=lab)
            xs = np.linspace(0.005, 5, 160)
            ax.plot(xs, mixture_pdf(xs * m, weights_closed(n, which)) * m, color=COL[n], lw=0.9, ls=(0, (2, 1.2)))
        if which == 'low':
            xs = np.linspace(0, 5, 200)
            ax.plot(xs, np.exp(-xs), color=DGREY, lw=0.8, ls=':', label=r'$\mathrm{Exp}(1)$')
        ax.plot([], [], color=DGREY, lw=0.9, ls=(0, (2, 1.2)), label=r'$\chi^2$ mixture')
        ax.set_xlim(0, 5 if which == 'low' else 2.5); ax.set_ylim(0, 1.25 if which == 'low' else 2.6)
        ax.set_xlabel(r'$%s/\mathbb{E}[%s]$' % (title, title)); ax.set_ylabel('density')
        ax.legend(loc='upper right', handlelength=1.6, labelspacing=0.25, borderaxespad=0.1, fontsize=6.8)
        ax.grid(True, color=LGREY, lw=0.5); ax.set_axisbelow(True)
    panel_label(axes[0], '(a)', x=-0.2); panel_label(axes[1], '(b)', x=-0.2)
    ax = axes[2]
    ns = list(range(3, 41))
    for which, col, lab in (('low', BLUE, r'$E_4$'), ('full', VERM, r'$E_{\rm full}$')):
        ax.plot(ns, [float(mean_energy_closed(n, which)) for n in ns], color=col, lw=1.0, label='mean ' + lab)
        ax.plot(ns, [var_exact(n, which) ** 0.5 for n in ns], color=col, lw=1.0, ls='--', label='std ' + lab)
        key = 'E_low' if which == 'low' else 'E_full'
        nm = [int(k) for k in mc]
        ax.plot(nm, [mc[str(n)][key]['mc_mean'] for n in nm], 'o', color=col, ms=3.0, mfc='white', mew=0.8)
        ax.plot(nm, [mc[str(n)][key]['mc_std'] for n in nm], 's', color=col, ms=2.8, mfc='white', mew=0.8)
    ax.plot([], [], 'o', color=DGREY, ms=3.0, mfc='white', mew=0.8, label='Monte Carlo')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xticks([3, 5, 10, 20, 40]); ax.set_xticklabels(['3', '5', '10', '20', '40']); ax.minorticks_off()
    ax.set_xlabel('$n$'); ax.set_ylabel('energy')
    ax.legend(loc='upper left', handlelength=1.8, borderaxespad=0.2, fontsize=6.8, labelspacing=0.25)
    ax.grid(True, color=LGREY, lw=0.5); ax.set_axisbelow(True)
    panel_label(ax, '(c)', x=-0.22)
    fig.subplots_adjust(left=0.065, right=0.99, top=0.92, bottom=0.2, wspace=0.34)
    fig.savefig(os.path.join(FIG, 'fig_random_energy.pdf'))
    plt.close(fig); print('random energy figure written')


def fig_balance():
    from balance_lib import functionals, magic4_reps
    reps, _ = magic4_reps(os.path.join(HERE, 'magic4_all7040.txt'))
    rng = np.random.default_rng(20240607)
    R = np.array([rng.permutation(16) + 1 for _ in range(300000)], float)
    fm = functionals(reps, 4); fr = functionals(R, 4)
    fig, axs = plt.subplots(1, 3, figsize=(TEXTWIDTH, 2.45), gridspec_kw=dict(wspace=0.42))
    # (a) T2 bound: scatter of lhs vs rhs on random permutations, n = 4 (subsample)
    ax = axs[0]
    k = rng.choice(len(R), 4000, replace=False)
    ax.scatter(fr['T2_rhs'][k], fr['T2_lhs'][k], s=2.0, color=BLUE, alpha=0.35, lw=0, rasterized=True)
    lim = [1, 2e4]
    ax.plot(lim, lim, color=VERM, lw=0.9)
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(*lim); ax.set_ylim(0.2, 2e4)
    ax.set_xlabel(r'bound $\frac{n(n^2-1)}{12}N^2E_{\rm rc}$'); ax.set_ylabel(r'$|\sum_c z_c(x_c,y_c)|^2$')
    ax.set_title(r'$n=4$, random permutations', fontsize=8, loc='right')
    ax.text(0.96, 0.08, 'bound', color=VERM, transform=ax.transAxes, ha='right', fontsize=7.5)
    panel_label(ax, '(a)', x=-0.28)
    # (b) unit-vector (ring) imbalance: magic vs random
    ax = axs[1]
    bins = np.linspace(0, 45, 31)
    ax.hist(fr['B_ring'], bins=bins, density=True, histtype='stepfilled', color=LGREY, ec=GREY, lw=0.6, label='random permutations')
    ax.hist(fm['B_ring'], bins=bins, density=True, histtype='step', color=VERM, lw=1.2, label='880 magic squares')
    ax.set_xlim(-1, 45); ax.set_xlabel(r'ring imbalance $B_{\rm ring}=|\sum_c z_c u_c|$'); ax.set_ylabel('density')
    ax.legend(loc='upper right', fontsize=6.8, handlelength=1.4)
    ax.text(0.98, 0.55, r'every magic square has' + '\n' + r'$B_{\rm lin}=0$ but $B_{\rm ring}>0$', transform=ax.transAxes, ha='right', fontsize=6.8, color=DGREY, va='top')
    ax.set_title(r'$n=4$', fontsize=8, loc='right')
    panel_label(ax, '(b)', x=-0.25)
    # (c) scatter linear vs ring
    ax = axs[2]
    ax.scatter(fr['B_lin'][k], fr['B_ring'][k], s=2.0, color=GREY, alpha=0.4, lw=0, rasterized=True, label='random')
    ax.scatter(fm['B_lin'], fm['B_ring'], s=5, color=VERM, lw=0, label='magic', zorder=3)
    ax.set_xlabel(r'$B_{\rm lin}=|\sum_c z_c(x_c,y_c)|$'); ax.set_ylabel(r'$B_{\rm ring}$')
    ax.set_xlim(-2, 90); ax.set_ylim(-1, 50)
    ax.legend(loc='upper left', fontsize=6.8, markerscale=2.5, handletextpad=0.2)
    panel_label(ax, '(c)', x=-0.25)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.92, bottom=0.2)
    fig.savefig(os.path.join(FIG, 'fig_balance.pdf'))
    plt.close(fig); print('balance figure written')


def lower_bound_34(n):
    """Largest K >= 2 for which the pigeonhole criterion (11) holds, or None (orders covered by Lemma 3.12 only)."""
    from math import comb
    if n % 2 == 0:
        h = n // 2
        if h % 2 == 1 and h < 7:
            return None
        r = [n // 2] * (n // 2)
    else:
        if n < 9:
            return None
        Q = (n - 3) // 2
        r = [min(2 * q, n - 4 - 2 * q, (n - 9) // 2) + 1 for q in range(Q)]
    N = n * n; lhs = 1
    for rq in r:
        lhs *= -(-rq // 2) + 1
    best = None; K = 2
    while True:
        rhs = 1
        for s in range(K - 1):
            rhs *= (N - 1) * sum(r[q] * comb(q, s) for q in range(len(r))) + 1
        if lhs > rhs:
            best = K; K += 1
        else:
            return best


def fig_kstar():
    """k*(n): exact values (n<=40), single-implementation upper bounds (41<=n<=100), Theorem (a) bound, n-1,
    the lower bound given by (11), and sqrt(2n)."""
    jp = os.path.join(HERE, 'kstar_verify.json')
    if os.path.exists(jp):
        d = json.load(open(jp))
    else:  # partial run: parse the log
        import re
        U = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'^(\d+) U\(n\) = (\d+)', open(os.path.join(HERE, 'kstar_verify.log')).read(), re.M)}
        d = {'upper_bounds': U, 'exact': {n: U[n] for n in U if n <= 40}}
    exact = {int(k): v for k, v in d['exact'].items()}
    for n in range(3, 14): exact[n] = n - 1
    up = {int(k): v for k, v in d['upper_bounds'].items() if int(k) > 40}
    fig, ax = plt.subplots(figsize=(0.72 * TEXTWIDTH, 2.25))
    nmax = max(up) if up else 40
    ns = np.arange(3, nmax + 1)
    ax.plot(ns, ns - 1, color=GREY, lw=0.9, ls='--', label=r'$n-1$ (real-valued $z$)')
    A = np.floor(np.sqrt(np.pi * np.e * (ns - 1) * np.log(ns ** 4 / 4.0)))
    ax.plot(ns, A, color=VERM, lw=1.0, label=r'upper bound $\lfloor\sqrt{\pi e(n-1)\log(n^4/4)}\rfloor$')
    lb = {n: lower_bound_34(n) for n in range(9, nmax + 1)}
    xl = [n for n in sorted(lb) if lb[n] is not None and lb[n] >= 2]
    ax.plot(xl, [lb[n] for n in xl], 's', color=GREEN, ms=2.4, mfc='white', mew=0.7, label=r'lower bound from the pigeonhole criterion')
    ax.plot(ns, np.sqrt(2 * ns), color=GREEN, lw=1.0, ls=':', label=r'$\sqrt{2n}$ (order of the lower bound)')
    xe = sorted(exact); ax.plot(xe, [exact[n] for n in xe], 'o', color=BLUE, ms=3.2, label=r'$k^*(n)$, exact')
    xu = sorted(up); ax.plot(xu, [up[n] for n in xu], 'o', color=BLUE, ms=3.2, mfc='white', mew=0.8, label=r'upper bound, computer-assisted (not certified)')
    ax.set_xlim(0, nmax + 2); ax.set_ylim(0, 0.62 * nmax)
    ax.set_xlabel('$n$'); ax.set_ylabel('degree $k$')
    ax.legend(loc='upper left', fontsize=6.6, handlelength=1.8, labelspacing=0.2)
    ax.grid(True, color=LGREY, lw=0.5); ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.17)
    fig.savefig(os.path.join(FIG, 'fig_kstar.pdf'))
    plt.close(fig); print('kstar figure written; (11) lower bounds:', {n: lb[n] for n in xl if n in (14, 20, 30, 40, 60, 80, 100)})


if __name__ == '__main__':
    todo = sys.argv[1:] or ['decomposition', 'random', 'kstar']
    if 'decomposition' in todo: fig_decomposition()
    if 'swap' in todo: fig_swap()
    if 'random' in todo: fig_random()
    if 'balance' in todo: fig_balance()
    if 'kstar' in todo: fig_kstar()
