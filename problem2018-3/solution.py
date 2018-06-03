from os import system

import numpy as np

import matplotlib as mpl
from matplotlib import pyplot as plt, cm
from matplotlib.gridspec import GridSpec


class ResultsPlot:
    def __init__(self, dist_name, crit_names, dist_std=None):
        self.dist_name = dist_name
        self.crit_names = crit_names
        self.dist_std = dist_std
        self.results = []

    def _ith_color(self, i_crit):
        return cm.Set1(float(i_crit) / len(self.crit_names))

    def _display_false_positives(self, ax, fpos_rates):
        fpos_rates *= 100.0

        for i, rate in enumerate(fpos_rates):
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

        ax.set_xlim(-0.5, len(fpos_rates) - 0.5)
        ax.set_ylim(0.0, max(fpos_rates) * 1.5)

        ax.set_xticklabels(self.crit_names)
        ax.set_xticks(range(len(self.crit_names)))

        ax.set_ylabel("false pos. rate, $\\%%$")

        ax.legend(loc='best', prop={'size': 'x-small'})

    @classmethod
    def _display_derivative(cls, ax, xs, ys, c, name):
        ds = np.convolve(np.gradient(ys) / np.gradient(xs), [0.2, 0.2, 0.2, 0.2, 0.2], mode='same')

        d_line = ax.plot(xs, ds, color=c, linestyle=':', alpha=0.8, label="$\\frac{d}{dx} $" + name)

        i_max = np.argmax(ds)
        x, d = xs[i_max], ds[i_max]

        ax.axhline(d, color=c, linestyle='-.', alpha=0.8)
        ax.text(x, d, "${:.2f}$".format(d), va='bottom', ha='center', fontdict={'size': 'x-small'}, color=c)

        ax.set_ylim(-0.01, max(d * 1.1, ax.get_ylim()[1]))

        return d_line

    @classmethod
    def _display_sigma_scale(cls, ax, sigma, cx):
        for i in np.arange(cx[-1] / sigma + 0.5):
            i_sigma = sigma * (i + 1)

            ax.axvline(i_sigma, color='blue', alpha=0.07)
            ax.text(i_sigma, 50.0, " ${}\\sigma$".format(int(i + 1) if i != 0 else ""), va='center', ha='left', fontdict={'size': 'small'}, color='blue', alpha=0.25, zorder=100)

    def _display_powers(self, ax, cx, power_plots):
        power_plots *= 100.0

        f_lines = []
        df_lines = []

        d_ax = ax.twinx()

        for i, (rates, name) in enumerate(zip(power_plots, self.crit_names)):
            f_line = ax.plot(cx, rates, color=self._ith_color(i), marker='.', label=name)
            f_lines.append(f_line[0])

            df_line = self._display_derivative(d_ax, cx, rates, self._ith_color(i), name)
            df_lines.append(df_line[0])

        if self.dist_std is not None:
            self._display_sigma_scale(ax, self.dist_std, cx)

        d_ax.set_ylabel("$\\frac{d}{dc} $ true pos. rate, $\\frac{\\%}{\\Delta c}$")

        ax.set_title("Power", loc='left')

        ax.yaxis.grid()

        ax.set_xlim(min(cx), max(cx))
        ax.set_ylim(-1.0, 101.0)

        ax.set_xlabel("$c$")
        ax.set_ylabel("true pos. rate, $\\%%$")

        all_lines = [line for p in zip(f_lines, df_lines) for line in p]
        d_ax.legend(all_lines, [line.get_label() for line in all_lines], loc='lower right', prop={'size': 'x-small'}, markerscale=1.5)

    def add_result(self, sample_size, fpos_rates, cx, power_plots):
        self.results.append(
            (sample_size, fpos_rates, cx, power_plots)
        )

    def display_results(self):
        fig = plt.figure(figsize=(12, 12))

        fig.suptitle("Evaluating stat. power of two-sample EV equality tests on samples from {}{}".format(
            "$\\xi$" + ("$ \sim\ $" if '=' not in self.dist_name else ", "),
            self.dist_name
        ))

        gs = GridSpec(len(self.results), 2)

        for i, (sample_size, fpos_rates, cx, power_plots) in enumerate(self.results):
            ax_false_pos = fig.add_subplot(gs[i, 0])

            self._display_false_positives(ax_false_pos, fpos_rates)

            self._display_powers(
                fig.add_subplot(gs[i, 1]),
                cx,
                power_plots
            )

            left_loc = ax_false_pos.get_position()

            fig.text(
                left_loc.x0 / 2.0,
                (left_loc.y0 + left_loc.y1) / 2.0,
                "${:d}$".format(sample_size),
                ha='right'
            )

        return fig


class TwoSampleExperiment:
    def __init__(self, Dist, criteria, n_repeat=10000, alpha=0.05):
        self.Dist = Dist
        self.criteria = criteria
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

    def _create_sample_pairs(self, sample_size):
        return self.Dist().rvs(size=(self.n_repeat, 2, sample_size))

    def get_false_positives(self, sample_size):
        print "Calculating f.pos, n =", sample_size

        return self._rejection_rates(self._create_sample_pairs(sample_size))

    def get_powers(self, sample_size, cx):
        print "Calculating powers, n =", sample_size

        rate_plots = []

        for c in cx:
            sample_pairs = self._create_sample_pairs(sample_size)

            sample_pairs[:,1,:] += c

            rate_plots.append(
                self._rejection_rates(sample_pairs)
            )

        return np.transpose(rate_plots)


from scipy.stats import ttest_ind, ttest_rel, ranksums


def display_results(Dist, dist_name):
    e = TwoSampleExperiment(
        Dist,
        (
            ttest_ind,
            # ttest_rel,
            ranksums,
        ),
        n_repeat=100
    )

    plot = ResultsPlot(
        dist_name,
        (
            "Student (ind.)",
            # "Student (rel.)",
            "Wilcoxon",
        ),
        dist_std=Dist().std()
    )

    cx = np.concatenate([
        np.linspace(0.0, 1.0, num=10)[:-1],
        np.linspace(1.0, 4.0, num=10)
    ])

    for sample_size in (8, 50):
        fposx = e.get_false_positives(sample_size)
        powers = e.get_powers(sample_size, cx)

        plot.add_result(sample_size, fposx, cx, powers)

    plt.rcParams['font.family'] = 'serif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    fig = plot.display_results()

    fig.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")
