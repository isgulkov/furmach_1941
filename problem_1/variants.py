from scipy.stats import rv_continuous

from numpy import exp, sqrt

class DistVariant1(rv_continuous):
    def _cdf(self, x, *args):
        return 1 - exp(-exp(0.1 * x))

class DistVariant2(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - exp(-sqrt(x))
        else:
            return 0

class DistVariant3(rv_continuous):
    def _cdf(self, x, *args):
        if x <= 0:
            return 0.5 * exp(x)
        else:
            return 1 - 0.5 * exp(-x)

class DistVariant4(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - exp(1 - exp(x))
        else:
            return 0

class DistVariant5(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 2 ** (x + 1) / (1 + 2 ** x) - 1
        else:
            return 0

class DistVariant6(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - 1 / (1 + x ** 0.2)
        else:
            return 0

class DistVariant7(rv_continuous):
    def _cdf(self, x, *args):
        if x < 0:
            return 0
        else:
            return 1 - 2 ** (-(x ** 1.5))

class DistVariant8(rv_continuous):
    def _cdf(self, x, *args):
        return 1 - 3 ** (-(3 ** x))

class DistVariant9(rv_continuous):
    def _cdf(self, x, *args):
        if x <= 0:
            return 0
        elif x < 1:
            return (1 - exp(-x)) / (1 - exp(-1))
        else:
            return 1

class DistVariant10(rv_continuous):
    def _cdf(self, x, *args):
        if x > 1:
            return 1 - 1 / x
        else:
            return 0

def get_dist_by_variant_number(v):
    return (DistVariant1,
        DistVariant2,
        DistVariant3,
        DistVariant4,
        DistVariant5,
        DistVariant6,
        DistVariant7,
        DistVariant8,
        DistVariant9,
        DistVariant10, )[v - 1]
