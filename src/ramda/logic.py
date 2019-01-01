from .internal import _curry1
from .function import empty
from .relation import equals

__all__ = ["is_empty"]


@_curry1
def is_empty(x):
    return x is not None and equals(x, empty(x))
