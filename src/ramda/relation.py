import math
from .internal import _curry2, _curry3


__all__ = ["clamp", "identical"]


@_curry3
def clamp(min, max, value):
    if min > max:
        raise ValueError(
            "min must not be greater than max in clamp(min, max, value)")
    return min if value < min else \
        max if value > max else \
        value


@_curry2
def identical(a, b):
    if isinstance(a, float) and math.isnan(a):
        return math.isnan(b)
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    return id(a) == id(b)
