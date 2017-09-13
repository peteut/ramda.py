import inspect
import collections
import copy
import functools
import builtins
from .internal import _curry1, _curry2, _curry3, _reduce, _dispatchable, \
    _check_for_method, _xall, _is_transformer, _step_cat, _xmap, _xfilter
from .function import curry_n


__all__ = ["adjust", "filter", "all", "map", "reduce", "into", "tail"]


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
@_dispatchable(["map"], _xmap)
def map(fn, functor):
    if isinstance(functor, collections.Callable):
        return curry_n(
            len(inspect.signature(functor).parameters),
            lambda *args: fn(functor(*args)))
    elif isinstance(functor, collections.Mapping):
        return functools.reduce(
            lambda acc, key: collections.ChainMap(acc, {key: fn(functor[key])}),
            functor.keys(), {})
    else:
        return [fn(x) for x in functor]


@_curry2
@_dispatchable(["filter"], _xfilter)
def filter(pred, filterable):
    if isinstance(filterable, collections.Mapping):
        def _fn(acc, key):
            if pred(filterable[key]):
                acc[key] = filterable[key]
            return acc
        return _reduce(_fn, {}, filterable.keys())
    return [x for x in filterable if pred(x)]


reduce = _curry3(_reduce)


@_curry3
def into(acc, xf, xs):
    if _is_transformer(acc):
        return _reduce(xf(acc), acc._transducer_init(), xs)
    return _reduce(xf(_step_cat(acc)), copy.copy(acc), xs)


@_curry1
@_check_for_method("tail")
def tail(xs):
    return xs[1:]
