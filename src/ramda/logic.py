from .internal import _curry1, _curry2, _curry3, _curry_n, _arity
from .function import empty, _get_arity
from .internal import _equals

__all__ = ["all_pass", "any_pass", "cond", "and_", "or_", "not_",
           "is_empty", "when"]


@_curry1
def all_pass(preds):
    return _curry_n(max(map(_get_arity, preds)),
                    lambda *args: all(map(lambda pred: pred(*args), preds)))


@_curry1
def any_pass(preds):
    return _curry_n(max(map(_get_arity, preds)),
                    lambda *args: any(map(lambda pred: pred(*args), preds)))


@_curry3
def if_else(condition, on_true, on_false):
    return _curry_n(
        max(map(_get_arity, [condition, on_true, on_false])),
        lambda *args: on_true(*args) if condition(*args) else
        on_false(*args))


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
def when(pred, when_true_fn, x):
    return when_true_fn(x) if pred(x) else x
