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


def _concat(set1, set2):
    return set1 + set2


def _arity(n, fn):
    if n == 0:
        return lambda: fn()
    elif n == 1:
        return lambda a0=__: fn(a0)
    elif n == 2:
        return lambda a0=__, a1=__: fn(a0, a1)
    elif n == 3:
        return lambda a0=__, a1=__, a2=__: fn(a0, a1, a2)
    elif n == 4:
        return lambda a0=__, a1=__, a2=__, a3=__: fn(a0, a1, a2, a3)
    elif n == 5:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__: fn(a0, a1, a2, a3, a4)
    elif n == 6:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__, a5=__: \
            fn(a0, a1, a2, a3, a4, a5)
    elif n == 7:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__, a5=__, a6=__: \
            fn(a0, a1, a2, a3, a4, a5, a6)
    elif n == 8:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__, a5=__, a6=__, a7=__: \
            fn(a0, a1, a2, a3, a4, a5, a6, a7)
    elif n == 9:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__, a5=__, a6=__, a7=__, a8=__: \
            fn(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    elif n == 10:
        return lambda a0=__, a1=__, a2=__, a3=__, a4=__, a5=__, a6=__, a7=__, a8=__, a9=__: \
            fn(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)
    else:
        raise ValueError("First argument to _arity must be a non-negative "
                         "integer no greater than ten")


def _curry_n(length, received, fn):
    def _fn(*args):
        combined = []
        args_list = list(args)
        left = length
        while len(combined) < len(received) or len(args_list):
            if len(combined) < len(received) and \
                    (not _is_placeholder(received[len(combined)]) or
                     len(args_list) == 0):
                result = received[len(combined)]
            else:
                result = args_list.pop(-1)
            combined.append(result)
            if not _is_placeholder(result):
                left -= 1
        return fn(*combined) if left <= 0 else \
            _arity(left, _curry_n(length, combined, fn))
    return _fn


def _is_integer(x):
    return isinstance(x, int)
