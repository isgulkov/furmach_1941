
class PRNG(object):
    def __init__(self, init):
        if not (0 <= init < 10000):
            raise ValueError(
                "Initial value {:d} out of [0; 10000) range".format(init)
            )

        self._init = init
        self._current = init

    @property
    def range(self):
        return (0, 10000)

    @property
    def description(self):
        raise ValueError("not implemented")

    def _next(self):
        raise ValueError("not implemented")

    def next(self):
        old = self._current

        self._current = self._next()

        return old / 10000.0

    def reset(self):
        self._current = self._init

    def get_sample(self, n, first=False):
        if first:
            saved_state = self._current
            self.reset()

        sample = [self.next() for _ in xrange(n)]

        if first:
            self._current = saved_state

        return sample


class LCG(PRNG):
    def __init__(self, init, a=113, b=10, m=10000):
        self._a, self._b, self._m = a, b, m

        super(LCG, self).__init__(init)

    @property
    def description(self):
        return "$LCG(a=%d, b=%d, m=%d, z_1=%d)$" % (self._a, self._b, self._m, self._init, )

    def _next(self):
        return (self._a * self._current + self._b) % self._m


class MiddleSquare(PRNG):
    def __init__(self, init):
        super(MiddleSquare, self).__init__(init)

    @property
    def description(self):
        return "$MidSq(z_1=%d)$" % self._init

    def _next(self):
        return self._current ** 2 / 100 % 10000


def get_prng_by_variant_number(v):
    # return LCG(2456)
    return MiddleSquare(1661)
