import inspect
import collections
import functools
import builtins
from .internal import _curry2
from .function import curry_n


__all__ = ["map"]


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
