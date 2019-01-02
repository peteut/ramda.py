from .internal import _curry1, _curry2
from .function import empty
from .relation import equals

__all__ = ["and_", "or_", "not_", "is_empty"]


@_curry2
def and_(a, b):
    return a and b


@_curry2
def or_(a, b):
    return a or b


@_curry1
def not_(a):
    return not a


@_curry1
def is_empty(x):
    return x is not None and equals(x, empty(x))
