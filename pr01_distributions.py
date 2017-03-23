from scipy.stats import rv_continuous

from numpy import exp, sqrt

class DistVarik1(rv_continuous):
    def _cdf(self, x, *args):
        return 1 - exp(-exp(0.1 * x))

class DistVarik2(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - exp(-sqrt(x))
        else:
            return 0

class DistVarik3(rv_continuous):
    def _cdf(self, x, *args):
        if x <= 0:
            return 0.5 * exp(x)
        else:
            return 1 - 0.5 * exp(-x)

class DistVarik4(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - exp(1 - exp(x))
        else:
            return 0

class DistVarik5(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 2 ** (x + 1) / (1 + 2 ** x) - 1
        else:
            return 0

class DistVarik6(rv_continuous):
    def _cdf(self, x, *args):
        if x >= 0:
            return 1 - 1 / (1 + x ** 0.2)
        else:
            return 0

class DistVarik7(rv_continuous):
    def _cdf(self, x, *args):
        if x < 0:
            return 0
        else:
            return 1 - 2 ** (-(x ** 1.5))

class DistVarik8(rv_continuous):
    def _cdf(self, x, *args):
        return 1 - 3 ** (-(3 ** x))

class DistVarik9(rv_continuous):
    def _cdf(self, x, *args):
        if x <= 0:
            return 0
        elif x < 1:
            return (1 - exp(-x)) / (1 - exp(-1))
        else:
            return 1

class DistVarik10(rv_continuous):
    def _cdf(self, x, *args):
        if x > 1:
            return 1 - 1 / x
        else:
            return 0

def getDistByVarik(varik):
    return (DistVarik1,
        DistVarik2,
        DistVarik3,
        DistVarik4,
        DistVarik5,
        DistVarik6,
        DistVarik7,
        DistVarik8,
        DistVarik9,
        DistVarik10, )[varik - 1]
