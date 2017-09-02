from ramda.internal import _curry2, __ as _


def eq(a, b):
    assert a == b


def describe_curry2():
    def it_supports_placeholder():
        f = lambda a, b: [a, b]
        g = _curry2(f)

        eq(g(1)(2), [1, 2])
        eq((1, 2), [1, 2])

        eq(g(_, 2)(1), [1, 2])
        eq(g(1, 2), [1, 2])

        eq(g(_, _)(1)(2), [1, 2])
        eq(g(_, _)(1, 2), [1, 2])
        eq(g(_, _)(_)(1, 2), [1, 2])
        eq(g(_, _)(_, 2)(1), [1, 2])
