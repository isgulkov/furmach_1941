import numpy as np
from scipy.stats import rv_continuous


class Var4Dist(rv_continuous):
    def _cdf(self, x):
        return np.exp(x) / (1 + np.exp(x))


class Var9Dist(rv_continuous):
    def _cdf(self, x):
        return 0 if x < 0 else 1 - np.exp(-(x ** 0.4))


class InverseTxDist(object):
    def __init__(self):
        self.prv = uniform(0, 1)

        self.qfx = np.vectorize(self.qf)

    def qf(self, p):
        # Replace with quantile function manually solved for
        raise TypeError("Not implemented")

    def std(self):
        return None

    def rvs(self, size=()):
        return self.qfx(self.prv.rvs(size))


class Var4DistInverseTx(InverseTxDist):
    # About 750x faster than the rv_continuous version
    def __init__(self):
        super(Var4DistInverseTx, self).__init__()

    def qf(self, p):
        return np.log(- p / (p - 1))

    def std(self):
        # Empirical on 1.5M-sample
        return 1.813161003617862


class Var9DistInverseTx(InverseTxDist):
    def __init__(self):
        super(Var9DistInverseTx, self).__init__()

    def qf(self, p):
        return (-np.log(1 - p)) ** 2.5

    def std(self):
        # Empirical on 1.5M-sample
        return 10.364418217353347


from functools import partial
from scipy.stats import norm, uniform, expon, f, lognorm, chi2, bernoulli, t


def get_dist_by_variant_number(v):
    return (
        (partial(norm, 0, 1), "$N(0,\ 1)$"),
        (partial(uniform, 0, 6), "$R(0,\ 6)$"),
        (partial(expon, 1), "$E(1)$"),
        (Var4DistInverseTx, "$F_{\\xi_i} = \\frac{e^x}{1 + e^x}$"),
        (partial(f, 2, 3), "$F(2,\ 3)$"),
        (partial(lognorm, 0.7, 0.3 ** 2), "$\\ln N(0.7,\ 0.3^2)$"),
        (partial(chi2, 1), "$\\chi^2_1$"),
        (partial(t, 2), "$t_2$"),
        (Var9DistInverseTx, "$F_{\\xi_i} = 1 - e^{-x^0.4},\\ x \\geq 0;\\ 0,\\ otherwise$"),
        (partial(t, 4), "$t_4$"),
    )[v - 1]
