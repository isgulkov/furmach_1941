import numpy as np

from matplotlib import pyplot as plt, gridspec

from os import system

def pr04_part1((x2s, x3s, x4s, ys, )):
    y_vector = np.array(ys)
    
    x_matrix = np.array([
        np.ones(len(x2s)),
        x2s,
        x3s,
        x4s,
        ]).transpose()

    # Find least-squares solution for X * beta = y
    beta_vector, residues, rank, s = np.linalg.lstsq(x_matrix, y_vector)

    print "Regression got estimated as:"
    print "\ty = %.2f + %.2f x_2 + %.2f x_3 + %.2f x_4" % tuple(beta_vector.tolist())

    plt.scatter(x3s, ys, s=5.0)

    plt.legend()
    plt.savefig("~figure.png")

    system("open ./~figure.png")
