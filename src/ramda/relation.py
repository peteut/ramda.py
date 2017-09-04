import math
from .internal import _curry2


__all__ = ["identical"]


@_curry2
def identical(a, b):
    if isinstance(a, float) and math.isnan(a):
        return math.isnan(b)
    return a == b
