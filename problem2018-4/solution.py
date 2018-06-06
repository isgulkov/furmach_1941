from os import system

import numpy as np

from matplotlib import pyplot as plt, cm, colors  # TODO: remove cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import rankdata

import pandas as pd


def get_corr_matrices(f_corr, vx):
    rs = np.diag(np.ones(len(vx)))
    p_values = np.diag(np.ones(len(vx)))

    for i, one in enumerate(vx):
        for j, another in enumerate(vx[i:]):
            for vs, v in zip((rs, p_values), f_corr(one, another)):
                vs[i, i + j] = vs[i + j, i] = v

    return rs, p_values


def draw_corr_matrix(ax, column_names, rs, annotations=None, title="", fig=None):
    ax.set_title(title, y=1.1)

    ax.margins(0.1, 0)

    rs = rs.copy()
    np.fill_diagonal(rs, 0.0)

    # im = ax.imshow(rs, cmap=cm.bwr, aspect='auto', clim=(-1.0, 1.0))
    im = ax.imshow(rs, cmap=cm.bwr, aspect=1 / 1.1, clim=(-1.0, 1.0))

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)

    if fig is not None:
        fig.colorbar(im, ax=ax, ticks=[-1, 0, 1])

    for i in xrange(len(column_names)):
        for j in xrange(len(column_names)):
            if i == j:
                continue

            ax.text(
                i, j, "${:.2f}$".format(rs[i, j]), va='center', ha='center', fontdict={'size': 'small'}
            )

            if annotations is not None:
                ax.text(
                    i + 0.45, j - 0.45, annotations[i, j], va='top', ha='right', alpha=0.5, fontdict={'size': 'xx-small'}
                )

    ax.xaxis.tick_top()
    # ax.tick_params('x', rotation=45.0)

    ax.set_xticks(range(len(column_names)))
    ax.set_xticklabels(column_names)

    ax.set_yticks(range(len(column_names)))
    ax.set_yticklabels(column_names)

def draw_scatter(ax, xs, ys, x_label="", y_label="", title="", c='black'):
    ax.set_title(title)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.scatter(xs, ys, s=5.0, c=c, label="")

    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))

    a, b = np.polyfit(xs, ys, 1)
    xs_fit = np.linspace(min(xs), max(xs), num=10)

    rho = np.corrcoef(xs, ys)[0, 1]

    ax.plot(xs_fit, a * xs_fit + b, alpha=0.75, c=c, label="$\\rho = {:.2f}$".format(rho))

    ax.legend(loc='best')

def remove_outliers_both(xs, ys, n_sigma=1.0):
    not_outliers = np.logical_and(*(np.absolute(vs - vs.mean()) < n_sigma * vs.std() for vs in (xs, ys)))

    return [np.extract(not_outliers, vs).astype(float) for vs in (xs, ys)]


from scipy.stats import pearsonr, spearmanr


def display_results(csv_path):
    df = pd.read_csv(csv_path).select_dtypes(include=['number'])

    col_names = df.columns[1:]  # Remove the first `n` column
    cols = [df[col] for col in col_names]

    (rs_p, ps_p) = get_corr_matrices(pearsonr, cols)
    (rs_s, ps_s) = get_corr_matrices(spearmanr, cols)


    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    fig = plt.figure(figsize=(10, 12))

    def get_p_text(p):
        return (
            "${}\\%$".format(
                "0.1" if p < 0.001 else
                "1" if p < 0.01 else
                "5"
            ) if p < 0.5 else ""
        )

    draw_corr_matrix(plt.subplot(3, 2, 1), col_names, rs_p, annotations=np.vectorize(get_p_text)(ps_p), title="$\\rho_{Pearson}$", fig=fig)

    draw_corr_matrix(plt.subplot(3, 2, 3), col_names, rs_s, annotations=np.vectorize(get_p_text)(ps_s), title="$\\rho_{Spearman}$", fig=fig)

    p_s_diff = rs_p - rs_s

    draw_corr_matrix(plt.subplot(3, 2, 5), col_names, p_s_diff, title="$\\rho_{Pearson} - \\rho_{Spearman}$", fig=fig)

    col_a, col_b = (
        col_names[i] for i in np.unravel_index(np.absolute(p_s_diff).argmax(), p_s_diff.shape)
    )

    xs, ys = (df[col] for col in (col_a, col_b))

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    draw_scatter(plt.subplot(3, 2, 2), xs, ys, x_label=col_a, y_label=col_b, title="", c=colors[0])

    draw_scatter(plt.subplot(3, 2, 4), *remove_outliers_both(xs, ys, n_sigma=1.0), x_label=col_a, y_label=col_b, title="with outliers removed", c=colors[1])

    draw_scatter(plt.subplot(3, 2, 6), rankdata(xs), rankdata(ys), x_label=col_a, y_label=col_b, title="ranks", c=colors[2])

    fig.subplots_adjust(hspace=0.3)

    fig.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")
