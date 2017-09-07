from fastnumbers import fast_real
from .internal import _curry1, _curry2, _is_integer
from .list import reduce

__all__ = ["add", "dec", "divide", "inc", "math_mod", "mean", "multiply",
           "negate", "product", "subtract", "sum"]


@_curry2
def add(a, b):
    try:
        return fast_real(a) + fast_real(b)
    except TypeError:
        return float('nan')


dec = add(-1)


@_curry2
def divide(a, b):
    return a / b


inc = add(1)


@_curry2
def math_mod(m, p):
    if not _is_integer(m):
        return
    if not _is_integer(p) or p < 1:
        return
    return m % p


@_curry1
def mean(xs):
    try:
        return sum(xs) / len(xs)
    except ZeroDivisionError:
        return float('nan')


@_curry2
def multiply(a, b):
    return a * b


@_curry1
def negate(n):
    return -n


product = reduce(multiply, 1)


@_curry2
def subtract(a, b):
    try:
        return fast_real(a) - fast_real(b)
    except TypeError:
        return float('nan')


sum = reduce(add, 0)
