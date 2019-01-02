from .internal import _curry1, _curry2, _curry3, _curry_n, _arity
from .function import empty
from .relation import equals

__all__ = ["and_", "or_", "not_", "is_empty"]


@_curry3
def if_else(condition, on_true, on_false):
    return _curry_n(max(map(_arity, [condition, on_true, on_false])),
                    lambda *args: on_true(*args) if condition(*args) else
                    on_false(*args))


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
