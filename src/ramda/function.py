from .internal import _curry1, _curry2, _curry_n, _arity


@_curry2
def curry_n(length, fn):
    if length == 1:
        return _curry1(fn)
    return _arity(length, _curry_n(length, [], fn))
