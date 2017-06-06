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

    print _render_template(template_vars).encode('utf-8')

