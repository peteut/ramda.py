from .internal import _curry2, _curry3, _equals, _identical


__all__ = ["clamp", "equals", "eq_props", "identical", "prop_eq", "gt"]


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


@_curry3
def prop_eq(name, val, obj):
    return _equals(val, obj[name])


@_curry3
def eq_props(prop, obj1, obj2):
    return equals(obj1[prop], obj2[prop])


@_curry2
def gt(a, b):
    return a > b
