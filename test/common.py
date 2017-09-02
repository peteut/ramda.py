from inspect import signature


def get_arity(fn):
    return len(signature(fn).parameters)
