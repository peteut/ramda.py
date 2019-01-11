import inspect
import collections
import builtins
from .internal import _curry1, _curry2, _curry_n, _arity, _identity, \
    _pipe, _reduce, _is_array, _is_string, _is_object, _concat

__all__ = ["ap", "always", "curry_n", "curry", "converge", "empty", "identity", "always",
           "pipe", "compose", "invoker", "n_ary", "lift_n", "lift"]


def _get_arity(fn):
    return len(inspect.signature(fn).parameters)


@_curry1
def always(val):
    return lambda *_: val


@_curry2
def ap(apply_f, apply_x):
    from .list import map

    if isinstance(getattr(apply_f, "ap", None), collections.Callable):
        return apply_f.ap(apply_x)
    if isinstance(apply_f, collections.Callable):
        return lambda x: apply_f(x)(apply_x(x))

    print(apply_f, apply_x)
    return _reduce(
        lambda acc, f: _concat(acc, map(f, apply_x)), [], apply_f)


@_curry2
def curry_n(length, fn):
    if length == 1:
        return _curry1(fn)
    return _arity(length, _curry_n(length, [], fn))


@_curry1
def curry(fn):
    return curry_n(_get_arity(fn), fn)


@_curry2
def converge(after, fns):
    def call_fn(fn, args):
        return fn(*args[: _get_arity(fn)])

    @curry_n(builtins.max([_get_arity(fn) for fn in fns], default=0))
    def fn(*args):
        return after(*[call_fn(fn, args) for fn in fns])
    return fn


@_curry1
def empty(x):
    if isinstance(getattr(x, "empty", None), collections.Callable):
        return x.empty()
    elif isinstance(x, collections.Callable):
        return lambda _: None
    elif _is_array(x):
        return []
    elif _is_string(x):
        return ""
    elif _is_object(x):
        return {}


identity = _curry1(_identity)


def pipe(*args):
    from .list import tail

    if len(args) == 0:
        raise ValueError("pipe requires at least one argument")
    return _arity(_get_arity(args[0]),
                  _reduce(_pipe, args[0], tail(args)))


@_curry2
def pluck(p, xs):
    pass


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


@_curry2
def n_ary(n, fn):
    if n == 0:
        return lambda: fn()
    elif n == 1:
        return lambda a0=None: fn(a0)
    elif n == 2:
        return lambda a0=None, a1=None: fn(a0, a1)
    elif n == 3:
        return lambda a0=None, a1=None, a2=None: fn(a0, a1, a2)
    elif n == 4:
        return lambda a0=None, a1=None, a2=None, a3=None: fn(a0, a1, a2, a3)
    elif n == 5:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None: fn(a0, a1, a2, a3, a4)
    elif n == 6:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None, a5=None: \
            fn(a0, a1, a2, a3, a4, a5)
    elif n == 7:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None, a5=None, a6=None: \
            fn(a0, a1, a2, a3, a4, a5, a6)
    elif n == 8:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None, a5=None, a6=None, \
            a7=None: fn(a0, a1, a2, a3, a4, a5, a6, a7)
    elif n == 9:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None, a5=None, a6=None, \
            a7=None, a8=None: fn(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    elif n == 10:
        return lambda a0=None, a1=None, a2=None, a3=None, a4=None, a5=None, a6=None, \
            a7=None, a8=None, a9=None: fn(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)
    raise ValueError(
        "First argument to nAry must be a non-negative integer no greater than ten")


@_curry2
def lift_n(arity, fn):
    from .list import map

    lifted = curry_n(arity, fn)
    return curry_n(
        arity,
        lambda *args: _reduce(ap, map(lifted, args[0]), args[1:]))


@_curry1
def lift(fn):
    return lift_n(_get_arity(fn), fn)
