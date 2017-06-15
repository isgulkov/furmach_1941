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

def _save_and_show_plot(price, x_matrix, beta_vector, filename="~figure.png", yvar_name="price", model_id=""):
    fig = plt.figure(figsize=(10, 5, ))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    fig.suptitle(model_id)

    price_hats = np.dot(x_matrix, beta_vector)

    fig.add_subplot(gs[0])

    plt.scatter(price_hats, [price[i] - price_hats[i] for i in xrange(len(price))], s=5.0)
    plt.title("Residues with respect to fitted price")
    plt.xlabel("$\\widehat{%s}$" % (yvar_name, ))
    plt.ylabel("$%s - \\widehat{%s}$" % (yvar_name, yvar_name, ))

    fig.add_subplot(gs[1])

    plt.hist(price_hats, int(len(price_hats) / np.log(len(price_hats))), normed=True)
    plt.title("Residues")
    plt.xlabel("$%s - \\widehat{%s}$" % (yvar_name, yvar_name, ))

    plt.savefig(filename, dpi=300)

    system("open ./%s" % (filename, ))

def _calculate_r2_adj(y_vector, x_matrix, beta_vector):
    y_hats = np.dot(x_matrix, beta_vector)

    y_mean = sum(y_vector) / len(y_vector)

    rss = sum([(y_vector[i] - y_hats[i])**2 for i in xrange(len(y_vector))])
    tss = sum([(y_vector[i] - y_mean)**2 for i in xrange(len(y_vector))])

    n = len(y_vector)
    k = x_matrix.shape[1]

    return 1.0 - (rss / (n - k)) / (tss / (n - 1))

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

    _save_and_show_plot(price, x_matrix, beta_vector, filename="~figure01.png", model_id="Linear model")

    template_vars['linear_plot_url'] = "~figure01.png"

    template_vars['linear_rss'] = residues
    template_vars['linear_r2'] = _calculate_r2_adj(y_vector, x_matrix, beta_vector)

    # Semilog model
    y_vector = np.log(y_vector)

    beta_vector, residues, rank, s = np.linalg.lstsq(x_matrix, y_vector)

    template_vars['semilog_betas'] = beta_vector

    _save_and_show_plot(np.log(price), x_matrix, beta_vector, filename="~figure02.png", yvar_name="\ln{price}",
        model_id="Semilog model")

    template_vars['semilog_plot_url'] = "~figure02.png"

    template_vars['semilog_rss'] = residues
    template_vars['semilog_r2'] = _calculate_r2_adj(y_vector, x_matrix, beta_vector)

    # Log model
    x_matrix = np.array([
        np.ones(len(price)),
        np.log(totsp),
        np.log(dist),
        walk,
        d2,
        d3,
        d4,
        bal,
        brick,
        floor,
        ]).transpose()

    beta_vector, residues, rank, s = np.linalg.lstsq(x_matrix, y_vector)

    template_vars['log_betas'] = beta_vector

    _save_and_show_plot(np.log(price), x_matrix, beta_vector, filename="~figure03.png", yvar_name="\ln{price}",
        model_id="Log model")

    template_vars['log_plot_url'] = "~figure03.png"

    template_vars['log_rss'] = residues
    template_vars['log_r2'] = _calculate_r2_adj(y_vector, x_matrix, beta_vector)

    example_xs = np.array([
        1,
        np.log(40),
        np.log(10),
        1,
        0,
        0,
        0,
        1,
        1,
        0
        ])

    template_vars['example_forecast'] = np.exp(np.dot(beta_vector, example_xs))

    print _render_template(template_vars).encode('utf-8')

