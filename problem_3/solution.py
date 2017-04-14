from scipy.stats import pearsonr, spearmanr

from matplotlib import pyplot as plt, gridspec

from os import system

def pr03((xs, ys, )):

    fig = plt.figure(figsize=(6, 7, ))
    gs = gridspec.GridSpec(2, 1, height_ratios=[6, 1])

    fig.add_subplot(gs[0])

    plt.scatter(xs, ys, s=5.0)

    fig.add_subplot(gs[1])

    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_visible(False)
    cur_axes.axes.get_yaxis().set_visible(False)

    cur_axes.axes.set_xlim(0, 1)
    cur_axes.axes.set_ylim(-3, 0)

    alpha = 0.05

    pearson_r, pearson_pvalue = pearsonr(xs, ys)
    pearson_corr_message = alpha < pearson_pvalue and "Corr." or "No corr."

    plt.text(0.05, -1, "$r = %.4f$ with $p = %e$ (%s at $\\alpha=0.05$)" % (pearson_r, pearson_pvalue, pearson_corr_message, ), clip_on=False)

    spearman_r, spearman_pvalue = spearmanr(xs, ys)
    spearman_corr_message = alpha < spearman_pvalue and "Corr." or "No corr."

    plt.text(0.05, -2, "$\\rho = %.4f$ with $p = %e$ (%s at $\\alpha=0.05$)" % (spearman_r, spearman_pvalue, spearman_corr_message, ), clip_on=False)

    r_spearman, p_spearman = spearmanr(xs, ys)

    plt.savefig("~figure.png", dpi=300)

    system("open ./~figure.png")
