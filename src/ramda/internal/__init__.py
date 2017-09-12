import inspect
import collections
import types


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


def _xwrap(fn):
    class _XWrap():
        def __init__(self, fn):
            self.f = fn

        @staticmethod
        def _transducer_init():
            raise NotImplementedError("init not implemented in Xwrap")

        @staticmethod
        def _transducer_result(acc):
            return acc

        def _transducer_step(self, acc, x):
            return self.f(acc, x)

    return _XWrap(fn)


def _reduce(fn, acc, xs):
    def _iterable_reduce(xf, acc, iterable):
        for step in iterable:
            acc = xf._transducer_step(acc, step)
            if acc and getattr(acc, "_transducer_reduced", False):
                acc = acc._transducer_value
                break
        return xf._transducer_result(acc)

    if inspect.isfunction(fn):
        fn = _xwrap(fn)

    if isinstance(xs, collections.Iterable):
        return _iterable_reduce(fn, acc, xs)

    raise ValueError("reduce: xs must be an iterable")


def _reduced(x):
    return x if x and getattr(x, "_transducer_reduced", None) else \
        types.SimpleNamespace(_transducer_value=x, _transducer_reduced=True)


class _XFBase():
    def init(self):
        return self.xf._transducer_init()

    def result(self, result):
        return self.xf._transducer_result(result)


@_curry2
def _xall(f, xf):
    class _Xall(_XFBase):
        def __init__(self, f, xf):
            self.xf = xf
            self.f = f
            self.all = True

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            if self.all:
                result = self.xf._transducer_step(result, True)
            return self.xf._transduer_result(result)

        def _transducer_step(self, result, input):
            if not self.f(input):
                self.all = False
                result = _reduced(self._transducer_step(result, False))
            return result
    return _Xall(f, xf)


def _is_transformer(obj):
    return inspect.isfunction(getattr(obj, "_transducer_step", None))


@_curry3
def _dispatchable(method_names, xf, fn):
    def _fn(*args):
        if len(args) == 0:
            return fn()
        obj = args[-1]
        if not isinstance(obj, collections.Iterable):
            for method_name in method_names:
                if getattr(obj, method_name, None):
                    return getattr(obj, method_name)(obj, *args[:1])
        if _is_transformer(obj):
            transducer = xf(*args[:1])
            return transducer(obj)
        return fn(*args)
    return _fn
