from os import system

import numpy as np

import matplotlib as mpl
from matplotlib import pyplot as plt, cm
from matplotlib.gridspec import GridSpec


class Experiment:
    def __init__(self, Dist, dist_name, criteria, crit_names, sample_sizes=(8, 50), n_repeat=10000, alpha=0.05):
        self.Dist = Dist
        self.dist_name = dist_name
        self.criteria = criteria
        self.crit_names = crit_names
        self.sample_sizes = sample_sizes
        self.n_repeat = n_repeat
        self.alpha = alpha

    def _rejection_rates(self, sample_pairs):
        nx_reject = np.zeros(len(self.criteria))

        print "Counting rejections on", sample_pairs.shape[0], "samples..."

        for a_sample, b_sample in sample_pairs:
            for i, crit in enumerate(self.criteria):
                _, p_value = crit(a_sample, b_sample)

                if p_value < self.alpha:
                    nx_reject[i] += 1

            if i % 100 == 0:
                print i

        return nx_reject / sample_pairs.shape[0]

    def _ith_color(self, i_crit):
        return cm.Set1(float(i_crit) / len(self.criteria))

    def _create_sample_pairs(self, sample_size):
        return self.Dist().rvs(size=(self.n_repeat, 2, sample_size))

    def _display_false_positives(self, ax, sample_size):
        rej_rx = self._rejection_rates(self._create_sample_pairs(sample_size))

        rej_rx *= 100.0

        for i, rate in enumerate(rej_rx):
            bar_rect = ax.bar([i], [rate], 0.8, align='center', color=self._ith_color(i), label=self.crit_names[i])[0]

            ax.text(
                bar_rect.get_x() + bar_rect.get_width() / 2.,
                1.05 * bar_rect.get_height(),
                "${:.2f}\\%%$".format(rate),
                ha='center',
                va='bottom'
            )

        ax.set_title("False positives", loc='left')

        ax.yaxis.grid()

        ax.set_xlim(-0.5, len(self.criteria) - 0.5)
        ax.set_ylim(0.0, max(rej_rx) * 1.5)

        ax.set_xticklabels(self.crit_names)
        ax.set_xticks(range(len(self.crit_names)))

        ax.set_ylabel("false pos. rate, $\\%%$")

        ax.legend(loc='best', prop={'size': 'x-small'})

    def _display_powers(self, ax, sample_size, cx=np.arange(0.0, 4.01, 0.5)):
        rej_rxs = []

        for c in cx:
            sample_pairs = self._create_sample_pairs(sample_size)

            sample_pairs[:,1,:] += c

            rej_rxs.append(
                self._rejection_rates(sample_pairs)
            )

        rej_rxs = np.transpose(rej_rxs) * 100.0

        for i, (rej_rx, name) in enumerate(zip(rej_rxs, self.crit_names)):
            ax.plot(cx, rej_rx, color=self._ith_color(i), marker='.', label=name)

        d_ax = ax.twinx()

        for i, (rej_rx, name) in enumerate(zip(rej_rxs, self.crit_names)):
            dcx = (cx[1:] - cx[:-1])
            drej_rx = (rej_rx[1:] - rej_rx[:-1]) / dcx

            d_ax.plot(cx[:-1] + 0.5 * dcx, drej_rx, color=self._ith_color(i), linestyle=':', alpha=0.5, label="$\\frac{d}{dc}$" + name)

        ax.set_title("Power", loc='left')

        ax.yaxis.grid()

        ax.set_xlim((min(cx), max(cx)))
        ax.set_ylim((-1.0, 101.0))

        ax.set_xlabel("$c$")
        ax.set_ylabel("true pos. rate, $\\%%$")

        ax.legend(loc='best', prop={'size': 'x-small'})

    def display_results(self):
        fig = plt.figure(figsize=(12, 12))

        fig.suptitle("Evaluating stat. power of two-sample EV equality tests on samples from {}{}".format(
            "$\\xi$" + ("$ \sim\ $" if '=' not in self.dist_name else ", "),
            self.dist_name
        ))

        gs = GridSpec(len(self.sample_sizes), 2)

        for i, sample_size in enumerate(self.sample_sizes):
            print "Sample size", sample_size

            ax_false_pos = fig.add_subplot(gs[i, 0])

            self._display_false_positives(ax_false_pos, sample_size)

            self._display_powers(
                fig.add_subplot(gs[i, 1]),
                sample_size,
                cx=np.concatenate([
                    np.linspace(0.0, 1.0, num=10)[:-1],
                    np.linspace(1.0, 3.01, num=10)
                ])
            )

            left_loc = ax_false_pos.get_position()

            fig.text(
                left_loc.x0 / 2.0,
                (left_loc.y0 + left_loc.y1) / 2.0,
                "${:d}$".format(sample_size),
                ha='right'
            )

        return fig


from scipy.stats import ttest_ind, ttest_rel, ranksums


def display_results(Dist, dist_name):
    plt.rcParams['font.family'] = 'serif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    fig = Experiment(
        lambda: Dist(),
        dist_name,
        (
            ttest_ind,
            # ttest_rel,
            ranksums,
        ),
        (
            "Student (ind.)",
            # "Student (rel.)",
            "Wilcoxon",
        ),
        sample_sizes=(8, 50),
        n_repeat=100
    ).display_results()

    fig.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")
