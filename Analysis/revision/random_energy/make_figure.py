"""fig_random_energy.pdf: (a) E_low/E[E_low] histograms (n=3 exact; n=5, 8 MC) with Gaussian-limit
densities; (b) same for E_full; (c) exact mean and std of E_low, E_full vs n (log-log) with MC points."""
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from theory import mean_energy_closed, weights_closed
from fit_variance import exact_var as variance_energy
from density import mixture_pdf
from energies import all_energies
from exhaustive_n3 import all_perms_n3

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {3: '#2a78d6', 5: '#eb6834', 8: '#1baf7a'}          # fixed categorical slots 1-3
C_LOW, C_FULL = '#2a78d6', '#eb6834'

plt.rcParams.update({'font.size': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 7,
                     'ytick.labelsize': 7, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
                     'pdf.fonttype': 42, 'font.family': 'sans-serif'})


def main():
    hist = np.load(os.path.join(HERE, 'mc_hist.npz'))
    mc = json.load(open(os.path.join(HERE, 'mc_results.json')))
    perms = all_perms_n3()
    E3 = all_energies(perms)

    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.35))
    bins_norm = np.linspace(0, 5, 61)
    for ax, key, which, title in ((axes[0], 'E_low', 'low', r'(a) $E_{\mathrm{low}}$'),
                                  (axes[1], 'E_full', 'full', r'(b) $E_{\mathrm{full}}$')):
        for n in (3, 5, 8):
            m = float(mean_energy_closed(n, which))
            if n == 3:
                e = E3[key] / m
                dens, _ = np.histogram(e, bins=bins_norm, density=True)
                lab = f'$n=3$ (exact, all $9!$)'
            else:
                h = hist[f'n{n}_{key}']; edges = hist[f'n{n}_edges_{which}'] / m
                # rebin onto bins_norm by linear redistribution (edges are fine: 400 bins)
                centers = 0.5 * (edges[:-1] + edges[1:])
                dens, _ = np.histogram(centers, bins=bins_norm, weights=h)
                dens = dens / (h.sum() * (bins_norm[1] - bins_norm[0]))
                lab = f'$n={n}$ (MC, $10^8$)'
            ax.stairs(dens, bins_norm, color=COL[n], lw=0.9, label=lab, baseline=None)
            xs = np.linspace(0.005, 5, 160)
            pdf = mixture_pdf(xs * m, weights_closed(n, which)) * m
            ax.plot(xs, pdf, color=COL[n], lw=0.9, ls=(0, (2, 1.2)), alpha=0.9)
        if which == 'low':
            xs = np.linspace(0, 5, 200)
            ax.plot(xs, np.exp(-xs), color='#52514e', lw=0.7, ls=':', label=r'$n\to\infty$: Exp(1)')
        ax.set_xlim(0, 5 if which == 'low' else 2.5)
        ax.set_ylim(0, 1.25 if which == 'low' else 2.1)
        ax.set_xlabel(r'$E/\mathbb{E}[E]$')
        ax.set_ylabel('density')
        ax.set_title(title, loc='left', fontsize=8)
        ax.plot([], [], color='#52514e', lw=0.9, ls=(0, (2, 1.2)), label='Gaussian-limit law')
        ax.legend(frameon=False, handlelength=1.6, borderaxespad=0.1, loc='upper right', labelspacing=0.25)

    ax = axes[2]
    ns_c = list(range(3, 41))
    for which, col, lab in (('low', C_LOW, r'$E_{\mathrm{low}}$'), ('full', C_FULL, r'$E_{\mathrm{full}}$')):
        mean = [float(mean_energy_closed(n, which)) for n in ns_c]
        std = [float(variance_energy(n, which)) ** 0.5 for n in ns_c]
        ax.plot(ns_c, mean, color=col, lw=1.0, label=f'mean {lab}')
        ax.plot(ns_c, std, color=col, lw=1.0, ls='--', label=f'std {lab}')
        key = 'E_low' if which == 'low' else 'E_full'
        ns_mc = [int(k) for k in mc]
        ax.plot(ns_mc, [mc[str(n)][key]['mc_mean'] for n in ns_mc], 'o', color=col, ms=3.2, mfc='white', mew=0.8)
        ax.plot(ns_mc, [mc[str(n)][key]['mc_std'] for n in ns_mc], 's', color=col, ms=3.0, mfc='white', mew=0.8)
    ax.plot([], [], 'o', color='#52514e', ms=3.2, mfc='white', mew=0.8, label='Monte Carlo')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xticks([3, 5, 10, 20, 40]); ax.set_xticklabels(['3', '5', '10', '20', '40'])
    ax.set_xlabel('$n$'); ax.set_ylabel('energy')
    ax.set_title('(c) exact moments', loc='left', fontsize=8)
    ax.text(11, float(mean_energy_closed(11, 'low')) * 3.5, r'mean $\sim n^4/72$', fontsize=7, color=C_LOW)
    ax.text(17, float(mean_energy_closed(17, 'full')) * 2.2, r'mean $\sim n^2/6$', fontsize=7, color=C_FULL)
    ax.text(17, float(variance_energy(17, 'full')) ** 0.5 * 0.33, r'std $\sim n^{3/2}/6$', fontsize=7, color=C_FULL)
    ax.legend(frameon=False, loc='upper left', handlelength=1.8, borderaxespad=0.2, ncol=1)
    for a in axes:
        a.grid(True, color='#e6e5e2', lw=0.5)
        a.set_axisbelow(True)
    fig.tight_layout(w_pad=1.0)
    fig.savefig(os.path.join(HERE, 'fig_random_energy.pdf'))
    fig.savefig(os.path.join(HERE, 'fig_random_energy.png'), dpi=200)
    print('figure written')


if __name__ == '__main__':
    main()
