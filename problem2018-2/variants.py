
from itertools import islice

class PRNG(object):
    def __init__(self, init):
        self._init = init
        self._current = init

    @property
    def description(self):
        raise TypeError("not implemented")

    def _state_repr(this, state):
        return state / 10000.0

    def _next_state(self, state):
        raise TypeError("not implemented")

    def next(self):
        v = self._state_repr(self._current)

        self._current = self._next_state(self._current)

        return v

    def reset(self):
        self._current = self._init

    def forever(self, first=False):
        if not first:
            while True:
                yield self.next()
        else:
            state = self._init

            while True:
                yield self._state_repr(state)

                state = self._next_state(state)


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

    def _next_state(self, state):
        return (self._a * state + self._b) % self._m


class MiddleSquare(PRNG):
    def __init__(self, init):
        super(MiddleSquare, self).__init__(init)

    @property
    def description(self, state):
        return "$MidSq(z_1=%d)$" % self._init

    def _next_state(self):
        return state ** 2 / 100 % 10000


class MiddleProduct(PRNG):
    def __init__(self, a_init, b_init):
        super(MiddleProduct, self).__init__((a_init, b_init))

    @property
    def description(self):
        return "$MidProd(z_1=%d, z_2=%d)$" % self._init

    def _next_state(self, (a, b)):
        return (b, a * b / 100 % 10000)

    def _state_repr(self, (a, b)):
        return b / 10000.0


def get_prng_by_variant_number(v):
    # return LCG(2456)
    # return MiddleSquare(1661)
    return MiddleProduct(8731, 1617)
