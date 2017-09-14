import inspect
from .internal import _curry1, _curry2, _curry_n, _arity, _concat, _identity, \
    _pipe, _reduce


__all__ = ["always", "curry_n", "identity", "always", "pipe", "compose"]




@_curry2
def curry_n(length, fn):
    if length == 1:
        return _curry1(fn)
    return _arity(length, _curry_n(length, [], fn))


identity = _curry1(_identity)


@_curry1
def always(val):
    return lambda *_: val


def pipe(*args):
    from .list import tail

    if len(args) == 0:
        raise ValueError("pipe requires at least one argument")
    return _arity(len(inspect.signature(args[0]).parameters),
                  _reduce(_pipe, args[0], tail(args)))


def compose(*args):
    if len(args) == 0:
        raise ValueError("compose requires at least one argument")
    return pipe(*reversed(args))
