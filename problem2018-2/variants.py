
from itertools import islice

class PRNG(object):
    def __init__(self, init):
        self._init = init
        self._current = init

    @property
    def description(self):
        raise TypeError("not implemented")

    def _int_repr(self, state):
        return state

    def _float_repr(self, state):
        return self._int_repr(state) / 10000.0

    def _state_repr(self, state, as_float=True):
        if as_float:
            return self._float_repr(state)
        else:
            return self._int_repr(state)

    def _next_state(self, state):
        raise TypeError("not implemented")

    def next(self, as_float=True):
        v = self._state_repr(self._current, as_float=as_float)

        self._current = self._next_state(self._current)

        return v

    def reset(self):
        self._current = self._init

    def iter(self, from_first=True, as_float=True):
        if not from_first:
            while True:
                yield self.next(as_float=as_float)
        else:
            state = self._init

            while True:
                yield self._state_repr(state, as_float=as_float)

                state = self._next_state(state)


    def get_sample(self, n, from_first=True, as_float=True):
        if from_first:
            saved_state = self._current
            self.reset()

        sample = [self.next(as_float=as_float) for _ in xrange(n)]

        if from_first:
            self._current = saved_state

        return sample


class LCG(PRNG):
    def __init__(self, init, a=113, b=10, m=10000):
        self._a, self._b, self._m = a, b, m

        super(LCG, self).__init__(init)

    @property
    def description(self):
        return "$LCG(a={}, b={}, m={}, z_1={})$".format(
            *("{:,d}".format(x).replace(',', '\\,') for x in (self._a, self._b, self._m, self._init))
        )

    def _next_state(self, state):
        return (self._a * state + self._b) % self._m

    def _float_repr(self, state):
        return float(state) / self._m


def middle_four(x):
    return x / 100 % 10000


class MiddleSquare(PRNG):
    def __init__(self, init):
        super(MiddleSquare, self).__init__(init)

    @property
    def description(self):
        return "$MidSq(z_1=%d)$" % self._init

    def _next_state(self, state):
        return middle_four(state ** 2)


class MiddleProduct(PRNG):
    def __init__(self, a_init, b_init):
        super(MiddleProduct, self).__init__((a_init, b_init))

    @property
    def description(self):
        return "$MidProd(z_1=%d, z_2=%d)$" % self._init

    def _next_state(self, (a, b)):
        return (b, middle_four(a * b))

    def _int_repr(self, (a, b)):
        return b


class PowerRemainderA(PRNG):
    def __init__(self, init):
        super(PowerRemainderA, self).__init__(init)

    @property
    def description(self):
        return "$PowerRemA(z_1=%d)$" % self._init

    def _next_state(self, state):
        return middle_four(int(state ** 2.5))


class PowerRemainderB(PRNG):
    def __init__(self, init):
        super(PowerRemainderB, self).__init__(init)

    @property
    def description(self):
        return "$PowerRemB(z_1=%d)$" % self._init

    def _next_state(self, state):
        return middle_four(int((state + 17) ** 2.2))


class PowerRemainderC(PRNG):
    def __init__(self, init):
        super(PowerRemainderC, self).__init__(init)

    @property
    def description(self):
        return "$PowerRemC(z_1=%d)$" % self._init

    def _next_state(self, state):
        return middle_four(int((state + 58) ** 1.6))


def get_prng_by_variant_number(v):
    return (
        MiddleSquare(1661),
        MiddleProduct(8731, 1617),
        LCG(2456),
        PowerRemainderA(1237),
        LCG(10 ** 9, a=16807, b=0, m=2147483647),
        MiddleSquare(1687),
        MiddleProduct(3308, 1949),
        PowerRemainderB(7724),
        LCG(2456),
        PowerRemainderC(4508), )[v - 1]
