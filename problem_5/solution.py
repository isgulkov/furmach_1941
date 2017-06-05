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
    print bal[:8]
    print brick[:8]
    print d2[:8]
    print d3[:8]
    print d4[:8]
    print dist[:8]
    print floor[:8]
    print price[:8]
    print totsp[:8]
    print walk[:8]

