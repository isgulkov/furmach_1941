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

def _save_and_show_plot(price, x_matrix, beta_vector, filename="~figure.png"):
    fig = plt.figure(figsize=(10, 5, ))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    price_hats = np.dot(x_matrix, beta_vector)

    fig.add_subplot(gs[0])

    plt.scatter(price_hats, [price[i] - price_hats[i] for i in xrange(len(price))], s=5.0)
    plt.title("Residues with respect to fitted price")
    plt.xlabel("$\\widehat{price}$")
    plt.ylabel("$price - \\widehat{price}$")

    fig.add_subplot(gs[1])

    plt.hist(price_hats, int(len(price_hats) / np.log(len(price_hats))), normed=True)
    plt.title("Residues")
    plt.xlabel("$price - \\widehat{price}$")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)

    system("open ./%s" % (filename, ))

def pr05((bal, brick, d2, d3, d4, dist, floor, price, totsp, walk, ), var_number):
    template_vars = {}

    template_vars['var_number'] = var_number

    y_vector = np.array(price)

    x_matrix = np.array([
        np.ones(len(price)),
        totsp,
        dist,
        walk,
        d2,
        d3,
        d4,
        bal,
        brick,
        floor,
        ]).transpose()

    # Linear model
    beta_vector, residues, rank, s = np.linalg.lstsq(x_matrix, y_vector)

    template_vars['linear_betas'] = beta_vector

    _save_and_show_plot(price, x_matrix, beta_vector, "~figure01.png")

    print _render_template(template_vars).encode('utf-8')

