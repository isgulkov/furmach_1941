
from matplotlib import pyplot as plt, gridspec
from scipy.stats import kstest
from os import system


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


def annotate_max_diff(xs, fs, gs, g_is_step=True, s_format="$%.4f$"):
    x, f, g = xs[0], fs[0], gs[0]

    for i, (xx, fx, gx) in enumerate(zip(xs, fs, gs)[1:]):
        if abs(fx - gx) > abs(f - g):
            x, f, g = xx, fx, gx

        if g_is_step and abs(fx - gs[i]) > abs(f - g):
            x, f, g = xx, fx, gs[i]

    y_text = (f + g) / 2.0

    text_on_the_right = x < 0.5

    if text_on_the_right:
        x_text = x + 0.1
    else:
        x_text = x - 0.1

    for is_top_one in (True, False):
        plt.annotate(
            s=s_format % abs(f - g),
            xy=(x, is_top_one and f or g),
            xytext=(x_text, y_text),
            arrowprops=dict(arrowstyle='->', alpha=0.5, clip_on=False),
            ha=text_on_the_right and 'left' or 'right',
            va='center',
            alpha=is_top_one and 0.75 or 0.0)

    plt.plot([x, x], [f, g], 'b', alpha=0.25)

    plt.plot([x], [f], 'r.', ms=7.5)
    plt.plot([x], [g], 'b.', ms=7.5)


def draw_edf_vs_r01(xs):
    xs = sorted(xs)

    edf_values = [float(i) / len(xs) for i in xrange(1, len(xs) + 1)]

    cdf_values = [max(0.0, min(1.0, x)) for x in xs]

    if xs[0] > 0.0:
        for a in (xs, edf_values, cdf_values):
            a.insert(0, 0.0)

    if xs[-1] < 1.0:
        for a in (xs, edf_values, cdf_values):
            a.append(1.0)

    plt.xlim(
        min(0.0, xs[0]),
        max(1.0, xs[-1])
        )

    plt.ylim(
        -0.01 if xs[0] < 0.0 else 0.0,
        1.01 if xs[-1] > 1.0 else 1.0
        )
    
    plt.plot(xs, cdf_values, 'r', label="$F_{R(0; 1)}$")

    plt.step(xs, edf_values, 'b', where='post', label="EDF")

    annotate_max_diff(xs, cdf_values, edf_values, s_format="$D_n = %.4f$")

    plt.legend(loc='best')


def draw_r01_kolm_smir(xs, alpha=0.05):
    ks_stat, p_value = kstest(xs, lambda x: x)

    reject = p_value < alpha

    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_visible(False)
    cur_axes.axes.get_yaxis().set_visible(False)

    plt.annotate(
        s="  $D_n = %.4f$, $p = %.2f$ (%s at $\\alpha=%d\\%%$)" % (ks_stat, p_value, reject and "no fit" or "fits", int(alpha * 100), ),
        xy=(0, 0),
        xytext=(0, 0.5),
        textcoords='axes fraction',
        ha='left',
        va='center')


def scaled(xs, (x_min, x_max)):
    x_max = float(x_max)

    return [(x - x_min) / x_max for x in xs]


def display_results(samples, prg, ):
    plt.rcParams['font.family'] = 'serif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    fig = plt.figure(figsize=(5 * len(samples), 8))

    fig.suptitle("Fitness of $R(0; 1)$ to samples from %s" % prg.description)

    gs = gridspec.GridSpec(3, len(samples), height_ratios=[6, 6, 1])

    for i, (xs, description) in enumerate(samples):
        fig.add_subplot(gs[i])

        plt.hist(xs, bins=10, range=prg.range)
        plt.title(description)

        xs_scaled = scaled(xs, prg.range)

        fig.add_subplot(gs[i + len(samples)])

        draw_edf_vs_r01(xs_scaled)

        fig.add_subplot(gs[i + 2 * len(samples)])

        draw_r01_kolm_smir(xs_scaled)

    # plt.tight_layout(pad=2.5, rect=[0.0, 0.0, 1.0, 0.97])

    plt.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")


if __name__ == '__main__':
    prg = LCG(2456)

    samples = []

    for n in (100, 10000):
        samples.append(
            ([prg.next() for _ in xrange(n)], "First ${:d}$ states".format(n))
            )

        prg.reset()

    samples.append(
        ([prg.next() for _ in xrange(100)] * 5, "First $100$ states 5 times over")
        )

    display_results(samples, prg)

    # display_results(LCG(110, a=10, b=570, m=290))

