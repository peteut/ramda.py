import inspect
import collections
from .internal import _curry1, _curry2, _curry_n, _arity, _identity, \
    _pipe, _reduce


__all__ = ["always", "curry_n", "identity", "always", "pipe", "compose",
           "invoker"]


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


@_curry2
def invoker(arity, method):
    def fn(*args):
        target = args[arity] if len(args) > arity else None
        if target and isinstance(getattr(target, method, None), collections.Callable):
            return getattr(target, method)(*args[:arity])
        raise TypeError("{} does not have a method named \"{}\"".format(
            target, method))

    return curry_n(arity + 1, fn)
