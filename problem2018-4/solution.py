from os import system

import numpy as np

from matplotlib import pyplot as plt, cm, ticker
from matplotlib.gridspec import GridSpec
from scipy.stats import rankdata

import pandas as pd


def get_corr_matrices(f_corr, vx, f_pair=None):
    rs = np.diag(np.ones(len(vx)))
    p_values = np.diag(np.ones(len(vx)))

    for i, one in enumerate(vx):
        for j, another in enumerate(vx[i:]):
            a, b = one, another

            if f_pair is not None:
                a, b = f_pair(one, another)

            for vs, v in zip((rs, p_values), f_corr(a, b)):
                vs[i, i + j] = vs[i + j, i] = v

    return rs, p_values


def draw_corr_matrix(ax, column_names, rs, annotations=None, title="", fig=None):
    ax.set_title(title, y=1.075)

    ax.margins(0.1, 0)

    rs = rs.copy()
    np.fill_diagonal(rs, 0.0)

    im = ax.imshow(rs, cmap=cm.bwr, aspect='auto', clim=(-1.0, 1.0))
    # im = ax.imshow(rs, cmap=cm.bwr, aspect=1 / 1.1, clim=(-1.0, 1.0))

    if fig is not None:
        fig.colorbar(im, ax=ax, ticks=[-1, 0, 1])

    if isinstance(annotations, str) and annotations == 'max absolute':
        rs_mabs = rs.flat[np.absolute(rs).argmax()]

        annotations = np.array([["max." if r == rs_mabs else "" for r in rs_row] for rs_row in rs])

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

    ax.set_xticks(range(len(column_names)))
    ax.set_xticklabels(column_names)

    ax.set_yticks(range(len(column_names)))
    ax.set_yticklabels(column_names)

def remove_outliers_both(xs, ys, n_sigma=1.0):
    not_outliers = np.logical_and(*(np.absolute(vs - vs.mean()) < n_sigma * vs.std() for vs in (xs, ys)))

    return [np.extract(not_outliers, vs).astype(float) for vs in (xs, ys)]

def draw_scatter_with_linefit(ax, xs, ys):
    scatter = ax.scatter(xs, ys, s=5.0, label="")

    rho = np.corrcoef(xs, ys)[0, 1]

    a, b = np.polyfit(xs, ys, 1)
    xs_fit = np.linspace(*ax.get_xlim(), num=10)

    ax.plot(xs_fit, a * xs_fit + b, alpha=0.75, label="$\\rho = {:.2f}$".format(rho))

def draw_scatter(ax, xs, ys, x_label="", y_label="", title="", f_remove_outliers=None):
    ax.set_title(title)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    draw_scatter_with_linefit(ax, xs, ys)

    if f_remove_outliers is not None:
        draw_scatter_with_linefit(ax, *f_remove_outliers(xs, ys))

    ax.legend(loc='best')


from scipy.stats import pearsonr, spearmanr


def display_results(csv_path):
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'

    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['xtick.color'] = '#545454'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    plt.rcParams['ytick.color'] = '#545454'

    fig = plt.figure(figsize=(20, 10))

    fig.suptitle("Comparison of Pearson and Spearman $\\rho$ on a dataset")

    gs = GridSpec(2, 5, width_ratios=[10, 1, 10, 10, 10])

    df = pd.read_csv(csv_path).select_dtypes(include=['number'])

    col_names = df.columns[1:]  # Remove the first `n` column
    cols = [df[col] for col in col_names]

    (rs_p, ps_p) = get_corr_matrices(pearsonr, cols)
    (rs_s, ps_s) = get_corr_matrices(spearmanr, cols)

    def get_p_text(p):
        return (
            "${}\\%$".format(
                "0.1" if p < 0.001 else
                "1" if p < 0.01 else
                "5"
            ) if p < 0.5 else ""
        )

    draw_corr_matrix(fig.add_subplot(gs[0, 0]), col_names, rs_p, annotations=np.vectorize(get_p_text)(ps_p), title="$\\rho_{Pearson}$")

    draw_corr_matrix(fig.add_subplot(gs[1, 0]), col_names, rs_s, annotations=np.vectorize(get_p_text)(ps_s), title="$\\rho_{Spearman}$")

    p_s_diff = rs_p - rs_s

    draw_corr_matrix(fig.add_subplot(gs[0, 2]), col_names, p_s_diff, annotations='max absolute', title="$\\rho_{Pearson} - \\rho_{Spearman}$")

    col_a, col_b = (
        col_names[i] for i in np.unravel_index(np.absolute(p_s_diff).argmax(), p_s_diff.shape)
    )

    xs, ys = (df[col] for col in (col_a, col_b))

    draw_scatter(fig.add_subplot(gs[0, 3]), rankdata(xs), rankdata(ys), x_label=col_a, y_label=col_b, title="")

    draw_scatter(fig.add_subplot(gs[0, 4]), xs, ys, x_label=col_a, y_label=col_b, title="...exclude $\\pm 1\\sigma$ outliers", f_remove_outliers=remove_outliers_both)

    rs_p_noout, _ = get_corr_matrices(pearsonr, cols, remove_outliers_both)
    rs_s_noout, _ = get_corr_matrices(spearmanr, cols, remove_outliers_both)

    p_s_diff_noout = rs_p_noout - rs_s_noout

    draw_corr_matrix(fig.add_subplot(gs[1, 2]), col_names, p_s_diff_noout, annotations='max absolute', title="$\\rho_{Pearson, (-\\sigma, \\sigma)} - \\rho_{Spearman, (-\\sigma, \\sigma)}$")

    col_a, col_b = (
        col_names[i] for i in np.unravel_index(np.absolute(p_s_diff_noout).argmax(), p_s_diff_noout.shape)
    )

    xs, ys = (df[col] for col in (col_a, col_b))

    pi, dor = remove_outliers_both(xs, ys)

    draw_scatter(fig.add_subplot(gs[1, 3]), rankdata(pi), rankdata(dor), x_label=col_a, y_label=col_b, title="")

    draw_scatter(fig.add_subplot(gs[1, 4]), *remove_outliers_both(xs, ys), x_label=col_a, y_label=col_b)

    fig.subplots_adjust(left=0.05, right=0.95, wspace=0.25)

    fig.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")
