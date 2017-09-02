class _Placeholder():
    pass


__ = _Placeholder()


def _is_placeholder(x):
    return id(x) == id(__)


def _curry1(fn):
    def f1(*args):
        if len(args) == 0:
            return f1
        else:
            a, = args
            return f1 if _is_placeholder(a) else fn(a)
    return f1


def _curry2(fn):
    def f2(*args):
        n_args = len(args)
        if n_args == 0:
            return f2
        elif n_args == 1:
            a, = args
            return f2 if _is_placeholder(a) else _curry1(lambda _b: fn(a, _b))
        else:
            a, b = args
            return f2 if _is_placeholder(a) and _is_placeholder(b) else \
                _curry1(lambda _a: fn(_a, b)) if _is_placeholder(a) else \
                _curry1(lambda _b: fn(a, _b)) if _is_placeholder(b) else \
                fn(a, b)
    return f2


def _curry3(fn):
    def f3(*args):
        n_args = len(args)
        if n_args == 0:
            return f3
        elif n_args == 1:
            a, = args
            return f3 if _is_placeholder(a) else \
                _curry2(lambda _b, _c: fn(a, _b, _c))
        elif n_args == 2:
            a, b = args
            return f3 if _is_placeholder(a) and _is_placeholder(b) else \
                _curry2(lambda _a, _c: fn(_a, b, _c)) if _is_placeholder(a) else \
                _curry2(lambda _b, _c: fn(a, _b, _c)) if _is_placeholder(b) else \
                _curry1(lambda _c: fn(a, b, _c))
        else:
            a, b, c = args
            return f3 \
                if _is_placeholder(a) and _is_placeholder(b) and _is_placeholder(c) else \
                _curry2(lambda _a, _b: fn(_a, _b, c)) \
                if _is_placeholder(a) and _is_placeholder(b) else \
                _curry2(lambda _a, _c: fn(_a, b, _c)) \
                if _is_placeholder(a) and _is_placeholder(c) else \
                _curry2(lambda _b, _c: fn(a, _b, _c)) \
                if _is_placeholder(b) and _is_placeholder(c) else \
                _curry1(lambda _a: fn(_a, b, c)) if _is_placeholder(a) else \
                _curry1(lambda _b: fn(a, _b, c)) if _is_placeholder(b) else \
                _curry1(lambda _c: fn(a, b, _c)) if _is_placeholder(c) else \
                fn(a, b, c)
    return f3
