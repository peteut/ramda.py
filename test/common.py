import types
from ramda.internal import _get_arity

try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

get_arity = _get_arity


list_xf = types.SimpleNamespace(
    _transducer_init=lambda: [],
    _transducer_step=lambda acc, x: acc.append(x),
    _transducer_result=lambda x: x)


def _is_transformer(obj):
    print(obj)
    return isinstance(getattr(obj, "_transducer_step", None), Callable)
