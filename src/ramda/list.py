import inspect
import collections
import functools
import builtins
from .internal import _curry2, _curry3, _reduce, _dispatchable, _xall
from .function import curry_n


__all__ = ["adjust", "all", "map", "reduce"]


@_curry3
def adjust(fn, idx, xs):
    if idx >= len(xs) or idx < -len(xs):
        return xs
    start = len(xs) if idx < 0 else 0
    _idx = start + idx
    _xs = xs[:]
    _xs[_idx] = fn(xs[_idx])
    return _xs


@_curry2
@_dispatchable(["all"], _xall)
def all(fn, xs):
    return builtins.all(map(fn, xs))


@_curry2
def map(fn, functor):
    if inspect.isfunction(functor):
        return curry_n(
            len(inspect.signature(functor).parameters),
            lambda *args: fn(functor(*args)))
    elif isinstance(functor, collections.Mapping):
        return functools.reduce(
            lambda acc, key: collections.ChainMap(acc, {key: fn(functor[key])}),
            functor.keys(), {})
    else:
        return list(builtins.map(fn, functor))


reduce = _curry3(_reduce)
