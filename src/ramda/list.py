import inspect
import collections
import copy
import functools
import itertools
import builtins
import fastnumbers
from .internal import _curry1, _curry2, _curry3, _reduce, _dispatchable, \
    _check_for_method, _xall, _is_transformer, _step_cat, _xmap, _xfilter, \
    _xtake, _curry_n, _xreduce_by, _reduced, _xany, _xaperture, _aperture, \
    _concat, _make_flat, _xchain, _contains, _xdrop, _xdrop_last, _xdrop_last_while, \
    _xdrop_repeats_with, _equals
from .function import curry_n


__all__ = ["adjust", "filter", "all", "any", "concat", "map", "reduce", "into", "tail", "take",
           "reduce_by", "reduced", "reduce_right", "aperture", "append", "chain", "contains",
           "drop", "drop_last", "drop_last_while", "drop_repeats_with", "drop_repeats",
           "nth", "head"]


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
@_dispatchable(["any"], _xany)
def any(fn, xs):
    return builtins.any(map(fn, xs))


@_curry2
def concat(a, b):
    if isinstance(a, collections.Sequence):
        if isinstance(b, collections.Sequence):
            return a + b
        raise TypeError("{} is not an array".format(b))
    if hasattr(a, "concat"):
        return a.concat(b)
    raise TypeError("{} does not have a method named \"concat\"".format(a))


@_curry2
@_dispatchable(["map"], _xmap)
def map(fn, functor):
    if isinstance(functor, collections.Callable):
        return curry_n(
            len(inspect.signature(functor).parameters),
            lambda *args: fn(functor(*args)))
    elif isinstance(functor, collections.Mapping):
        return functools.reduce(
            lambda acc, key: acc.update({key: fn(functor[key])}) or acc,
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


@_curry2
@_dispatchable(["take"], _xtake)
def take(n, xs):
    n = fastnumbers.fast_int(n, -1)
    return xs[:] if n < 0 else xs[:n]


@functools.partial(_curry_n, 4, [])
@_dispatchable([], _xreduce_by)
def reduce_by(value_fn, value_acc, key_fn, xs):
    def _fn(acc, elt):
        key = key_fn(elt)
        acc[key] = value_fn(acc.get(key, copy.copy(value_acc)), elt)
        return acc
    return _reduce(_fn, {}, xs)


reduced = _curry1(_reduced)


@_curry3
def reduce_right(fn, acc, xs):
    return _reduce(lambda value, acc: fn(acc, value), acc, reversed(xs))


aperture = _curry2(_dispatchable([], _xaperture)(_aperture))


@_curry2
def append(el, xs):
    return _concat(xs, [el])


@_curry2
@_dispatchable(["chain"], _xchain)
def chain(fn, monad):
    if isinstance(monad, collections.Callable):
        return lambda x: fn(monad(x))(x)
    return _make_flat(False)(map(fn, monad))


contains = _curry2(_contains)


@_curry2
@_dispatchable(["drop"], _xdrop)
def drop(n, xs):
    return xs[builtins.max(0, n):]


@_curry2
@_dispatchable([], _xdrop_last)
def drop_last(n, xs):
    return take(len(xs) - n if n < len(xs) else 0, xs)


@_curry2
@_dispatchable([], _xdrop_last_while)
def drop_last_while(fn, xs):
    drop = len([None for _ in itertools.takewhile(fn, builtins.reversed(xs))])
    to = len(xs) - drop
    return xs[:to]


@_curry2
@_dispatchable([], _xdrop_repeats_with)
def drop_repeats_with(pred, xs):
    return functools.reduce(
        lambda acc, x: acc.append(x) or acc if not pred(x, acc[-1]) else acc,
        xs, [xs[0]]) if len(xs) else []


drop_repeats = _curry1(_dispatchable(
    [], _xdrop_repeats_with(_equals), drop_repeats_with(_equals)))


@_curry2
def nth(offset, xs):
    try:
        return xs[offset]
    except IndexError:
        return "" if isinstance(xs, str) else None


head = nth(0)
