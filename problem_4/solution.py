import numpy as np
from scipy import stats
from matplotlib import pyplot as plt, gridspec

from os import system, path

from jinja2 import Template

def _render_template(template_vars):
    template_path = path.join(path.dirname(__file__), 'output_template.md')

    with open(template_path, mode='r') as f:
        template = Template(f.read().decode('utf-8'))

    return template.render(**template_vars)

def pr04((x2s, x3s, x4s, ys, ), var_number):
    y_vector = np.array(ys)

    x_matrix = np.array([
        np.ones(len(x2s)),
        x2s,
        x3s,
        x4s,
        ]).transpose()

    template_vars = {}

    template_vars['var_number'] = var_number

    # Find least-squares solution for X * beta = y
    beta_vector, residues, rank, s = np.linalg.lstsq(x_matrix, y_vector)

    template_vars['beta_hats'] = beta_vector.tolist()

    # Calculate RSS for the regression model
    overall_rss = sum(map(lambda x: x, residues))

    template_vars['overall_rss'] = overall_rss

    # Calculate ESS for the regression model
    yhats = np.dot(x_matrix, beta_vector) # estimates

    ys_mean = sum(ys) / len(ys) # mean estimate

    overall_ess = sum(map(lambda yhat: (yhat - ys_mean)**2, yhats))

    template_vars['overall_ess'] = overall_ess

    # Calculate F value for the regression model
    k = 4
    n = len(ys)

    template_vars['overall_f'] = (overall_ess / (k - 1)) / (overall_rss / (n - k))

    # Calculate F critical value for the regression model
    template_vars['overall_f_crit'] = stats.f.ppf(0.95, k - 1, n - k)

    # Calculate t critical value for individual coefficients
    template_vars['coef_t_crit'] = stats.t.ppf(0.95, n - k)

    # Calculate coefficient sigmas
    # NOTE: copied straight from Drankow's repo. No slightest idea how any of this works, but the results match
    chiselka = overall_rss / (n - k)
    matrasik = np.linalg.inv(np.dot(x_matrix.transpose(), x_matrix))
    huyasik = np.dot(chiselka, matrasik)
    coef_variances = [huyasik[i][i] for i in xrange(4)]

    coef_t_vals = [beta_vector[i] / coef_variances[i] ** 0.5 for i in xrange(4)]

    # Calculate coefficient t values
    template_vars['coef_t_vals'] = coef_t_vals

    # Calculate restricted RSS with \beta_3 and \beta_4 coefs set to zero
    restricted34_x_matrix = np.array([
        np.ones(len(x2s)),
        x2s,
        ]).transpose()

    restricted34_beta_vector = beta_vector[:2]

    restricted34_yhats = np.dot(restricted34_x_matrix, restricted34_beta_vector)

    restricted34_rss = sum([(restricted34_yhats[i] - ys[i])**2 for i in xrange(len(ys))])

    template_vars['restricted34_rss'] = restricted34_rss

    # Calculate restricted F value and F critical calue
    template_vars['restricted34_f'] = ((restricted34_rss - overall_rss) / 2) / (overall_rss / (n - k))

    template_vars['restricted34_f_crit'] = stats.f.ppf(0.95, 2, n - k)

    # Calculate correlations for x's
    xs_corr = {
        '23': stats.pearsonr(x2s, x3s)[0],
        '24': stats.pearsonr(x2s, x4s)[0],
        '34': stats.pearsonr(x3s, x4s)[0],
        }

    template_vars['xs_corr'] = xs_corr

    # Draw graphs for ridge regression coefficients
    ls = []
    betas_ridge = ([], [], [], [], )

    for l in np.arange(0.0, 2.0001, 0.1):
        ls.append(l)

        beta_ridge_vector = np.dot(
            np.linalg.inv(
                np.dot(
                    x_matrix.transpose(),
                    x_matrix
                    )
                + l * np.identity(4)
                ),
            np.dot(
                x_matrix.transpose(),
                y_vector
                )
            )

        for i in xrange(4):
            betas_ridge[i].append(beta_ridge_vector[i])

    fig = plt.figure(figsize=(14, 10, ))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

    fig.suptitle("Ridge regression coeffitients with respect to $\\lambda$")

    for i in xrange(4):
        fig.add_subplot(gs[i / 2, i % 2])

        plt.plot(ls, betas_ridge[i], 'r', label="$\\widehat{\\beta_%d}_{ridge}$" % (i + 1, ))
        plt.xticks(ls, rotation='vertical')

        plt.legend()

        # plt.tight_layout()

    plt.savefig("~figure.png")

    system("open ./~figure.png")

    template_vars['figure_path'] = "~figure.png"

    result = _render_template(template_vars)

    print result.encode('utf-8')
