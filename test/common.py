from inspect import signature
import types
import collections


def get_arity(fn):
    return len(signature(fn).parameters)


list_xf = types.SimpleNamespace(
    _transducer_init=lambda: [],
    _transducer_step=lambda acc, x: acc.append(x),
    _transducer_result=lambda x: x)


def _is_transformer(obj):
    print(obj)
    return isinstance(getattr(obj, "_transducer_step", None), collections.Callable)
