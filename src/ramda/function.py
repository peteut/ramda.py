import inspect
from .internal import _curry1, _curry2, _curry_n, _arity, _concat, _identity, \
    _check_for_method, _pipe, _reduce


__all__ = ["always", "curry_n", "identity", "always", "tail", "pipe"]




@_curry2
def curry_n(length, fn):
    if length == 1:
        return _curry1(fn)
    return _arity(length, _curry_n(length, [], fn))


identity = _curry1(_identity)


@_curry1
def always(val):
    return lambda *_: val


@_curry1
@_check_for_method("tail")
def tail(xs):
    return xs[1:]


def pipe(*args):
    if len(args) == 0:
        raise ValueError("pipe requires at least one argument")
    return _arity(len(inspect.signature(args[0]).parameters),
                  _reduce(_pipe, args[0], tail(args)))
