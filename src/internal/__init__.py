class _Placeholder():
    pass


__ = _Placeholder


def _is_placeholder(x):
    return isinstance(x, _Placeholder)


def _curry1(fn):
    def f1(*args):
        if len(args) == 0 or _is_placeholder(args[0]):
            return f1
        else:
            return fn(args[0])
    return fn


def _curry2(fn):
    def f2(*args):
        n_args = len(args)
        if n_args == 0:
            return f2
        elif n_args == 1:
            a = args[0]
            return _curry1(lambda _b: fn(a, b))
        else:
            a, b = args
            return f2 if all(_is_placeholder, args) else \
                lambda _a: fn(_a, b) if _is_placeholder(a) else \
                lambda _b: fn(a, _b) if _is_placeholder(b) else \
                fn(a, b)
    return f2
