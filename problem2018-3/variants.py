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
        (lambda: norm(0, 1), "$N(0,\ 1)$"),
        (lambda: uniform(0, 6), "$R(0,\ 6)$"),
        (lambda: expon(1), "$E(1)$"),
        (lambda: Var4Dist(), "$F_{\\xi_i} = \\frac{e^x}{1 + e^x}$"),
        (lambda: f(2, 3), "$F(2,\ 3)$"),
        (lambda: lognorm(0.7, 0.3 ** 2), "$\\ln N(0.7,\ 0.3^2)$"),
        (lambda: chi2(1), "$\\chi^2_1$"),
        (lambda: t(2), "$t_2$"),
        (lambda: Var9Dist(), "$F_{\\xi_i} = 1 - e^{-x^0.4},\\ x \\geq 0;\\ 0,\\ otherwise$"),
        (lambda: t(4), "$t_4$"),
    )[v - 1]
