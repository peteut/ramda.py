from .internal import _curry2, _curry3, _equals, _identical


__all__ = ["clamp", "equals", "identical"]


@_curry3
def clamp(min, max, value):
    if min > max:
        raise ValueError(
            "min must not be greater than max in clamp(min, max, value)")
    return min if value < min else \
        max if value > max else \
        value


equals = _curry2(_equals)

identical = _curry2(_identical)
