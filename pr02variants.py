from scipy.stats import norm, uniform, expon, bernoulli, f, chi2, t

class BaseDist:
    def __init__(self, theta):
        raise NotImplementedError()

    def rvs(self, size=None):
        return self._rv.rvs(size=size)

    @classmethod
    def from_mean(cls, mean):
        return cls(mean)

class DistVariant1(BaseDist):
    def __init__(self, theta):
        self._rv = norm(theta, 1)

class DistVariant2(BaseDist):
    def __init__(self, theta):
        self._rv = uniform(0, theta)

    @classmethod
    def from_mean(cls, mean):
        return cls(mean * 2)

class DistVariant3(BaseDist):
    def __init__(self, theta):
        self._rv = expon(theta)

    def rvs(self, size=None):
        return self._rv.rvs(size=size) - 1

class DistVariant4(BaseDist):
    def __init__(self, theta):
        self._bernoulli = bernoulli(0.1)
        self._theta = theta

    def rvs(self, size=None):
        return self._bernoulli.rvs(size=size) * self._theta

    @classmethod
    def from_mean(cls, mean):
        return cls(mean * 10)

class DistVariant5(BaseDist):
    def __init__(self, theta):
        self._f = f(2, 3)
        self._theta = theta

    def rvs(self, size=None):
        return self._f.rvs(size=size) + self._theta

    @classmethod
    def from_mean(cls, mean):
        return cls(mean - 3)

class DistVariant6(BaseDist):
    def __init__(self, theta):
        self._bernoulli = bernoulli(1 - theta)

    def rvs(self, size=None):
        return self._bernoulli.rvs(size=size) * 6

    @classmethod
    def from_mean(cls, mean):
        if x < 0 or x > 6:
            raise ValueError("Distribution of this form cannot have a mean outside [0; 6] (namely %d)" % (mean, ))

        return cls((6 - mean) / 6.0)

class DistVariant7(BaseDist):
    def __init__(self, theta):
        self._chi2 = chi2(theta)

    def rvs(self, size=None):
        return self._chi2.rvs(size=size) / 2.0

    @classmethod
    def from_mean(cls, mean):
        return cls(int(mean * 2))

class DistVariant8(BaseDist):
    def __init__(self, theta):
        self._t = t(2)
        self._theta = theta

    def rvs(self, size=None):
        return self._t.rvs(size=size) + self._theta

class DistVariant9(BaseDist):
    def __init__(self, theta):
        self._expon = expon(1)
        self._theta = theta

    def rvs(self, size=None):
        return self._expon.rvs(size=size) + self._theta

    @classmethod
    def from_mean(cls, mean):
        return cls(mean - 1)

class DistVariant10(BaseDist):
    def __init__(self, theta):
        self._t = t(4)
        self._theta = theta

    def rvs(self, size=None):
        return self._t.rvs(size=size) + self._theta

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
