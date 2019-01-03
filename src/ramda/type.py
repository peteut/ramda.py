from .internal import _curry1, _curry2, _curry3

__all__ = ["is_", "is_nil", "prop_is"]


@_curry2
def is_(ctor, val):
    return isinstance(val, ctor)


@_curry1
def is_nil(x):
    return x is None


@_curry3
def prop_is(type_, name, obj):
    return is_(type_, obj[name]) if name in obj else False
