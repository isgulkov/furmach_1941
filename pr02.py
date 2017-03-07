#coding: utf-8

from scipy.stats import rv_continuous, chi2
import numpy as np

from matplotlib import pyplot as plt, gridspec, mlab

def pr02():
    class DistVarik7(rv_continuous):
        def __init__(self):
            self._chi2 = chi2(6)

            super(DistVarik7, self).__init__()

        def _cdf(self, x, *args):
            return self._chi2.cdf(2 * x, *args)

    xi = DistVarik7()

    print str([xi.rvs() for i in xrange(10000)]).replace('[', '{').replace(']', '}')

    # Проверить гипотезу, что матожидание = 3, "с помощью обычной t-статистики"

    # Повторить 10000 раз

    

if __name__ == '__main__':
    pr02()

