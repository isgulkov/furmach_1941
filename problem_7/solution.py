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

    fig = plt.figure(figsize=(6, 18, ))
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])

    plot_no = 0

    for n_clusters in [2, 3, 4]:
        centroids, __ = vq.kmeans(data, n_clusters)

        idx, __ = vq.vq(data, centroids)

        fig.add_subplot(gs[plot_no])
        plot_no += 1

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
    plt.savefig("~figure.png", dpi=300)

    system("open ./~figure.png")

    template_vars['figure_url'] = "~figure.png"

    # print _render_template(template_vars).encode('utf-8')

