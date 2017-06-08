import numpy as np
from matplotlib import pyplot as plt, gridspec

from os import system, path

from jinja2 import Template

def _render_template(template_vars):
    template_path = path.join(path.dirname(__file__), 'output_template.md')

    with open(template_path, mode='r') as f:
        template = Template(f.read().decode('utf-8'))

    return template.render(**template_vars)

def pr07((xs, ys, ), var_number):
    template_vars = {}

    template_vars['var_number'] = var_number

    template_vars['xs'] = xs
    template_vars['ys'] = ys

    print _render_template(template_vars).encode('utf-8')

