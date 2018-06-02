
from os import system

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import kstest


class LCG:
    def __init__(self, init, a=113, b=10, m=10000):
        self._a, self._b, self._m = a, b, m

        if init >= m:
            raise ValueError("Initial state can't be greater than `m`")

        self._init = init
        self._current = init

    @property
    def description(self):
        return "$LCG(a=%d, b=%d, m=%d, z_0=%d)$" % (self._a, self._b, self._m, self._init, )

    @property
    def range(self):
        return (0, self._m)

    def reset(self):
        self._current = self._init

    def next(self):
        old = self._current

        self._current = (self._a * self._current + self._b) % self._m

        return old

    def get_sample(self, n, first=False):
        if first:
            saved_state = self._current
            self.reset()

        sample = [self.next() for _ in xrange(n)]

        if first:
            self._current = saved_state

        return sample


class SampleAnalysis:
    def _annotate_max_diff(self, ax, xs, fs, gs, g_is_step=True, s_format="$%.4f$"):
        x, f, g = xs[0], fs[0], gs[0]

        for i, (xx, fx, gx) in enumerate(zip(xs, fs, gs)[1:]):
            if abs(fx - gx) > abs(f - g):
                x, f, g = xx, fx, gx

            if g_is_step and abs(fx - gs[i]) > abs(f - g):
                x, f, g = xx, fx, gs[i]

        y_text = (f + g) / 2.0

        if x < 0.5:
            x_text = x + 0.1
            ha_text = 'left'
        else:
            x_text = x - 0.1
            ha_text = 'right'

        def draw_annotation(_y, _alpha):
            ax.annotate(
                s=s_format % abs(f - g),
                xy=(x, _y),
                xytext=(x_text, y_text),
                arrowprops=dict(arrowstyle='->', alpha=0.5, clip_on=False),
                ha=ha_text,
                va='center',
                alpha=_alpha
            )

        draw_annotation(f, 0.75)
        draw_annotation(g, 0.0)

        ax.plot([x, x], [f, g], 'b', alpha=0.25)

        ax.plot([x], [f], 'r.', ms=7.5)
        ax.plot([x], [g], 'b.', ms=7.5)


    def _draw_edf_vs_r01(self, ax):
        xs = sorted(self._xs_scaled)

        edf_values = [float(i) / len(xs) for i in xrange(1, len(xs) + 1)]

        cdf_values = [max(0.0, min(1.0, x)) for x in xs]

        if xs[0] > 0.0:
            for a in (xs, edf_values, cdf_values):
                a.insert(0, 0.0)

        if xs[-1] < 1.0:
            for a in (xs, edf_values, cdf_values):
                a.append(1.0)

        ax.set_xlim(
            min(0.0, xs[0]),
            max(1.0, xs[-1])
        )

        ax.set_ylim(-0.01, 1.01)

        ax.plot(xs, cdf_values, 'r', label="$F_{R(0; 1)}$")

        ax.step(xs, edf_values, 'b', where='post', label="EDF")

        self._annotate_max_diff(ax, xs, cdf_values, edf_values, s_format="$D_n = %.4f$")

        ax.legend(loc='best')

    def _draw_r01_kolm_smir(self, ax):
        ks_stat, p_value = kstest(self._xs_scaled, lambda x: x)

        reject = p_value < self.alpha

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax.annotate(
            s="  $D_n = %.4f$, $p = %.2f$ (%s at $\\alpha=%d\\%%$)" % (ks_stat, p_value, reject and "no fit" or "fits", int(self.alpha * 100), ),
            xy=(0, 0),
            xytext=(0, 0.5),
            textcoords='axes fraction',
            ha='left',
            va='center')

    @property
    def _xs_scaled(self):
        # TODO: don't scale here!
        x_max = 10000.0 #float(max(self.xs))
        x_min = 0 #min(self.xs)

        return [(x - x_min) / (x_max - x_min) for x in self.xs]

    def is_positive(self):
        return kstest(self._xs_scaled, lambda x: x)[1] < self.alpha

    def __init__(self, xs, description="", alpha=0.05):
        self.xs = xs
        self.description = description
        self.alpha = alpha

    def draw_on(self, (ax, bx, cx)):
        # TODO: find the range somewhere
        ax.hist(self.xs, bins=10, range=(0, 10000))
        ax.set_title(self.description)

        self._draw_edf_vs_r01(bx)

        self._draw_r01_kolm_smir(cx)


def display_results(prg, sizes=(100, 10000), find_examples=True):
    plt.rcParams['font.family'] = 'serif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    analyses = [
        SampleAnalysis(
            prg.get_sample(n, first=True),
            "First ${:d}$ states".format(n)
        ) for n in sizes
    ]

    if not analyses[0].is_positive():
        analyses.append(
            SampleAnalysis(
                prg.get_sample(100, first=True) * 5,
                "First $100$ states 5 times over"
            )
        )

    if analyses[-1].is_positive():
        pass # TODO: !

    fig = plt.figure(figsize=(5 * len(analyses), 8))

    fig.suptitle("Fitness of $R(0; 1)$ to samples from %s" % prg.description)

    gs = GridSpec(3, len(analyses), height_ratios=[6, 6, 1])
    all_axes = [fig.add_subplot(gs[i]) for i in xrange(3 * len(analyses))]

    for i, analysis in enumerate(analyses):
        analysis.draw_on(all_axes[i::len(analyses)])

    plt.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")


if __name__ == '__main__':
    prg = LCG(2456)

    display_results(prg, (100, 10000))

    # display_results(LCG(110, a=10, b=570, m=290))

