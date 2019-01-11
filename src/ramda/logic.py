from .internal import _curry1, _curry2, _curry3, _arity
from .function import empty, curry_n
from .internal import _equals, _get_arity, _fix_arity
__all__ = ["all_pass", "any_pass", "lt", "if_else", "gt", "cond", "and_",
           "or_", "not_", "is_empty", "until", "when"]


@_curry1
def all_pass(preds):
    fixed_preds = [_fix_arity(p) for p in preds]
    return curry_n(max(map(_get_arity, preds)) if len(preds) else 1,
                   lambda *args: all(map(lambda p: p(*args), fixed_preds))
                   if len(preds) else True)


@_curry1
def any_pass(preds):
    fixed_preds = [_fix_arity(p) for p in preds]
    return curry_n(max(map(_get_arity, preds)) if len(preds) else 1,
                   lambda *args: any(map(lambda p: p(*args), fixed_preds))
                   if len(preds) else False)


@_curry2
def lt(a, b):
    return a < b


@_curry2
def gt(a, b):
    return a > b


@_curry3
def if_else(condition, on_true, on_false):
    return curry_n(
        max(map(_get_arity, [condition, on_true, on_false])),
        lambda *args: _fix_arity(on_true)(*args)
        if _fix_arity(condition)(*args) else _fix_arity(on_false)(*args))


@_curry1
def cond(pairs):
    arity = max(map(lambda p: _get_arity(p[0]), pairs), default=0)

    def do(*args):
        for pred, fn in pairs:
            if (pred(*args)):
                return fn(*args)
    return _arity(arity, do)


@_curry2
def and_(a, b):
    return a and b


@_curry2
def or_(a, b):
    return a or b


@_curry1
def not_(a):
    return not a


@_curry1
def is_empty(x):
    return x is not None and _equals(x, empty(x))


@_curry3
def until(pred, fn, init):
    val = init
    while not pred(val):
        val = fn(val)
    return val


@_curry3
def when(pred, when_true_fn, x):
    return when_true_fn(x) if pred(x) else x
