from .internal import _curry1, _curry2

__all__ = ["is_", "is_nil"]


@_curry2
def is_(ctor, val):
    return isinstance(val, ctor)


@_curry1
def is_nil(x):
    return x is None
