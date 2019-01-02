from .internal import _curry2

__all__ = ["is_"]


@_curry2
def is_(ctor, val):
    return isinstance(val, ctor)
