#coding: utf-8

from scipy.stats import rv_continuous, chi2, ttest_1samp
import numpy as np

from matplotlib import pyplot as plt, gridspec, mlab

def pr02():
    class SuperDist:
        def __init__(self, n):
            self._chi2 = chi2(n)

        def rvs(self, size=None):
            return self._chi2.rvs(size=size) / 2.0

    xi = SuperDist(6)

    sample = [xi.rvs() for i in xrange(8)]

    print ttest_1samp(sample, 3)

    # Проверить гипотезу, что матожидание = 3, "с помощью обычной t-статистики"

    # Повторить 10000 раз

    # Вероятность отвержения H_0 для таких же распределений с матожиданиями от 1 до 5 с шагом 0.5

if __name__ == '__main__':
    pr02()

