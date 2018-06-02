from scipy.stats import rv_continuous, norm, uniform, expon, f, lognorm, chi2, bernoulli, t

from numpy import exp


class Var4Dist(rv_continuous):
    def _cdf(self, x):
        return exp(x) / (1 + exp(x))


class Var9Dist(rv_continuous):
    def _cdf(self, x):
        return 0 if x < 0 else 1 - exp(-(x ** 0.4))


def get_dist_by_variant_number(v):
    return (
        lambda: norm(0, 1),
        lambda: uniform(0, 6),
        lambda: expon(1),
        lambda: Var4Dist(),
        lambda: f(2, 3),
        lambda: lognorm(0.7, 0.3 ** 2),
        lambda: chi2(1),
        lambda: t(2),
        lambda: Var9Dist(),
        lambda: t(4), )[v - 1]
