import pytest
from ramda.internal import __ as _, _curry2, _curry3, _arity
from ramda.shared import eq
from .common import get_arity


def describe_curry2():
    def it_supports_placeholder():
        f = lambda a, b: [a, b]
        g = _curry2(f)

        eq(g()(1, 2), [1, 2])
        eq(g(1)(2), [1, 2])
        eq(g(1, 2), [1, 2])

        eq(g(_, 2)(1), [1, 2])
        eq(g(1, _)(2), [1, 2])

        eq(g(_, _)(1)(2), [1, 2])
        eq(g(_, _)(1, 2), [1, 2])
        eq(g(_, _)(_)(1, 2), [1, 2])
        eq(g(_, _)(_, 2)(1), [1, 2])


def describe_curry3():
    def it_supports_placeholder():
        f = lambda a, b, c: [a, b, c]
        g = _curry3(f)

        eq(g()(1, 2, 3), [1, 2, 3])
        eq(g(1)(2)(3), [1, 2, 3])
        eq(g(1)(2, 3), [1, 2, 3])
        eq(g(1, 2)(3), [1, 2, 3])

        eq(g(1, 2, 3), [1, 2, 3])

        eq(g(_, 2, 3)(1), [1, 2, 3])
        eq(g(1, _, 3)(2), [1, 2, 3])
        eq(g(1, 2, _)(3), [1, 2, 3])

        eq(g(1, _, _)(2)(3), [1, 2, 3])
        eq(g(_, 2, _)(1)(3), [1, 2, 3])
        eq(g(_, _, 3)(1)(2), [1, 2, 3])

        eq(g(1, _, _)(2, 3), [1, 2, 3])
        eq(g(_, 2, _)(1, 3), [1, 2, 3])
        eq(g(_, _, 3)(1, 2), [1, 2, 3])

        eq(g(1, _, _)(_, 3)(2), [1, 2, 3])
        eq(g(_, 2, _)(_, 3)(1), [1, 2, 3])
        eq(g(_, _, 3)(_, 2)(1), [1, 2, 3])

        eq(g(_, _, _)(_, _)(_)(1, 2, 3), [1, 2, 3])
        eq(g(_, _, _)(1, _, _)(_, _)(2, _)(_)(3), [1, 2, 3])


def describe_arity():
    def it_supports_up_to_10_parameters():
        f = lambda *args: args

        eq(get_arity(_arity(0, f)), 0)
        eq(get_arity(_arity(1, f)), 1)
        eq(get_arity(_arity(2, f)), 2)
        eq(get_arity(_arity(3, f)), 3)
        eq(get_arity(_arity(4, f)), 4)
        eq(get_arity(_arity(5, f)), 5)
        eq(get_arity(_arity(6, f)), 6)
        eq(get_arity(_arity(7, f)), 7)
        eq(get_arity(_arity(8, f)), 8)
        eq(get_arity(_arity(9, f)), 9)
        eq(get_arity(_arity(10, f)), 10)
        with pytest.raises(ValueError):
            _arity(11, f)
