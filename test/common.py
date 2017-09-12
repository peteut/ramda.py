from inspect import signature
import types


def get_arity(fn):
    return len(signature(fn).parameters)


list_xf = types.SimpleNamespace(
    _transducer_init=lambda: [],
    _transducer_step=lambda acc, x: acc.append(x),
    _transducer_result=lambda x: x)
