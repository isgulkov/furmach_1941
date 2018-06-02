from functools import partial

from scipy.stats import rv_continuous, norm, uniform, expon, f, lognorm, chi2, bernoulli, t

import numpy as np


class Var4Dist(rv_continuous):
    def _cdf(self, x):
        return np.exp(x) / (1 + np.exp(x))


class Var4Dist:
    # About 2.5x faster than the rv_continuous version
    def __init__(self):
        self.xrv = uniform(-10, 20)
        self.yrv = uniform(0, 0.25)

    def pdf(self, x):
        return np.exp(x) / (1 + np.exp(x)) - np.exp(2 * x) / (1 + np.exp(x)) ** 2

    def rv(self):
        while True:
            x = self.xrv.rvs()
            y = self.yrv.rvs()

            if y < self.pdf(x):
                return x

    def rvs(self, size=1):
        n = np.product(size)

        return np.array([self.rv() for i in xrange(n)]).reshape(size)


class Var4DistInverseTx:
    # About 750x faster than the rv_continuous version
    def __init__(self):
        self.prv = uniform(0, 1)

        self.qfx = np.vectorize(self.qf)

    def qf(self, p):
        # Quantile function manually solved for
        return np.log(- p / (p - 1))

    def rvs(self, size=()):
        return self.qfx(self.prv.rvs(size))


class RvsWrapper:
    def __init__(self, f):
        self.f = f

    def rvs(self, size=None):
        return self.f(size=size)


class Var9Dist(rv_continuous):
    def _cdf(self, x):
        return 0 if x < 0 else 1 - np.exp(-(x ** 0.4))


def get_dist_by_variant_number(v):
    return (
        (lambda: norm(0, 1), "$N(0,\ 1)$"),
        (lambda: uniform(0, 6), "$R(0,\ 6)$"),
        (lambda: expon(1), "$E(1)$"),
        (lambda: Var4DistInverseTx(), "$F_{\\xi_i} = \\frac{e^x}{1 + e^x}$"),
        (lambda: f(2, 3), "$F(2,\ 3)$"),
        (lambda: lognorm(0.7, 0.3 ** 2), "$\\ln N(0.7,\ 0.3^2)$"),
        (lambda: chi2(1), "$\\chi^2_1$"),
        (lambda: t(2), "$t_2$"),
        (lambda: Var9Dist(), "$F_{\\xi_i} = 1 - e^{-x^0.4},\\ x \\geq 0;\\ 0,\\ otherwise$"),
        (lambda: t(4), "$t_4$"),
    )[v - 1]
