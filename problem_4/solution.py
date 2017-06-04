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

def pr04_part1((x2s, x3s, x4s, ys, ), var_number):
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

    result = _render_template(template_vars)

    print result.encode('utf-8')


    # plt.scatter(x3s, ys, s=5.0)

    # plt.legend()
    # plt.savefig("~figure.png")

    # system("open ./~figure.png")
