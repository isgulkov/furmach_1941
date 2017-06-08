import numpy as np
import scipy.cluster.vq as vq
from matplotlib import pyplot as plt, gridspec

from os import system, path

from jinja2 import Template

def _render_template(template_vars):
    template_path = path.join(path.dirname(__file__), 'output_template.md')

    with open(template_path, mode='r') as f:
        template = Template(f.read().decode('utf-8'))

    return template.render(**template_vars)

CLUSTER_COLORS = ('r', 'g', 'b', 'm', )

def pr07((xs, ys, ), var_number):
    template_vars = {}

    template_vars['var_number'] = var_number

    data = np.column_stack((xs, ys, )).astype('float')

    figure_filenames = []

    for n_clusters in [2, 3, 4]:
        centroids, __ = vq.kmeans(data, n_clusters)

        idx, __ = vq.vq(data, centroids)

        plt.figure()

        for i in xrange(n_clusters):
            plt.plot(
                data[idx == i, 0],
                data[idx == i, 1],
                'o',
                markersize=2,
                color=CLUSTER_COLORS[i],
                )

        plt.plot(centroids[:,0], centroids[:,1], '*', color='black', markersize=10)

        plt.title("%d clusters" % (n_clusters, ))
        plt.tight_layout()

        figure_filenames.append("~figure%02d.png" % (len(figure_filenames), ))

        plt.savefig(figure_filenames[-1], dpi=300)

        system("open ./%s" % figure_filenames[-1])


    template_vars['figure_urls'] = figure_filenames

    # print _render_template(template_vars).encode('utf-8')

