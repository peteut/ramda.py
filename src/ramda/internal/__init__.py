import collections
import types
import functools
import builtins
import math


class _Placeholder():
    pass


__ = _Placeholder()


def _assign(target, *args):
    return functools.reduce(lambda acc, obj: acc.update(obj) or acc, args, target)


def _keys(obj):
    return obj.keys() if isinstance(obj, collections.Mapping) else \
        [idx for idx in range(len(obj))] if isinstance(obj, collections.Sequence) else \
        []


def _identical(a, b):
    if isinstance(a, float) and math.isnan(a):
        return isinstance(b, float) and math.isnan(b)
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    return id(a) == id(b)


def _has(prop, obj):
    try:
        return prop in obj if isinstance(obj, collections.Mapping) else \
            obj[prop] and True
    except IndexError:
        return False


def _equals(a, b, stack_a=[], stack_b=[]):
    if _identical(a, b):
        return True
    if type(a) != type(b):
        return False
    if a is None or b is None:
        return False
    if isinstance(getattr(a, "equals", None), collections.Callable) or \
            isinstance(getattr(b, "equals", None), collections.Callable):
        return isinstance(getattr(a, "equals", None), collections.Callable) and \
            a.equals(b) and \
            isinstance(getattr(b, "equals", None), collections.Callable) and \
            b.equals(a)
    if isinstance(a, (int, float, str)):
        if not (type(a) == type(b) and _identical(a, b)):
            return False
    if isinstance(a, collections.Callable) and isinstance(b, collections.Callable):
        return id(a) == id(b)
    keys_a = _keys(a)
    if len(keys_a) != len(_keys(b)):
        return False
    for item_a, item_b in builtins.reversed(builtins.list(builtins.zip(stack_a, stack_b))):
        if id(item_a) == id(a):
            return id(item_b) == id(b)
    stack_a.append(a)
    stack_b.append(b)
    for key in keys_a:
        if not (_has(key, b) and _equals(b[key], a[key], stack_a, stack_b)):
            return False
    stack_a.pop()
    stack_b.pop()
    return True


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
                result = args_list.pop(0)
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

    def _method_reduce(xf, acc, obj, method_name):
        return xf._transducer_result(
            getattr(obj, method_name)(xf._transducer_step, acc))

    if isinstance(fn, collections.Callable):
        fn = _xwrap(fn)

    if isinstance(xs, collections.Mapping) and isinstance(
            getattr(xs, "reduce", None), collections.Callable):
        return _method_reduce(fn, acc, xs, "reduce")

    if isinstance(xs, collections.Iterable):
        return _iterable_reduce(fn, acc, xs)

    raise ValueError("reduce: xs must be an iterable")


def _reduced(x):
    return x if x and getattr(x, "_transducer_reduced", False) else \
        types.SimpleNamespace(_transducer_value=x, _transducer_reduced=True)


def _force_reduced(x):
    return types.SimpleNamespace(_transducer_value=x, _transducer_reduced=True)


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
            return super().result(result)

        def _transducer_step(self, result, input):
            if not self.f(input):
                self.all = False
                result = _reduced(self.xf._transducer_step(result, False))
            return result

    return _Xall(f, xf)


@_curry2
def _xany(f, xf):
    class _Xany(_XFBase):
        def __init__(self, f, xf):
            self.xf = xf
            self.f = f
            self.any = False

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            if not self.any:
                result = self.xf._transducer_step(result, False)
            return super().result(result)

        def _transducer_step(self, result, input):
            if self.f(input):
                self.any = True
                result = _reduced(self.xf._transducer_step(result, True))
            return result

    return _Xany(f, xf)


@_curry2
def _xmap(f, xf):
    class _XMap(_XFBase):
        def __init__(self, f, xf):
            self.xf = xf
            self.f = f

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            return self.xf._transducer_step(result, self.f(input))

    return _XMap(f, xf)


@_curry2
def _xfilter(f, xf):
    class _XFilter(_XFBase):
        def __init__(self, f, xf):
            self.xf = xf
            self.f = f

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            if self.f(input):
                return self.xf._transducer_step(result, input)
            return result

    return _XFilter(f, xf)


def _is_transformer(obj):
    return isinstance(
        getattr(obj, "_transducer_step", None), collections.Callable)


def _identity(x):
    return x


@_curry3
def _dispatchable(method_names, xf, fn):
    def _fn(*args):
        if len(args) == 0:
            return fn()
        obj = args[-1]
        for method_name in method_names:
            if isinstance(getattr(obj, method_name, None), collections.Callable):
                return getattr(obj, method_name)(*args[:-1])
        if _is_transformer(obj):
            transducer = xf(*args[:-1])
            return transducer(obj)
        return fn(*args)
    return _fn


def _step_cat(obj):
    _step_cat_array = types.SimpleNamespace(
        _transducer_init=lambda: [],
        _transducer_step=lambda a, b: a.append(b) or a,
        _transducer_result=_identity)

    _step_cat_string = types.SimpleNamespace(
        _transducer_init=lambda: "",
        _transducer_step=lambda a, b: a + str(b),
        _transducer_result=_identity)

    _step_cat_obj = types.SimpleNamespace(
        _transducer_init=lambda: {},
        _transducer_step=lambda result, input: _assign(
            result, dict([input[:2]]) if not isinstance(
                input, collections.Mapping) else input),
        _transducer_result=_identity)

    if _is_transformer(obj):
        return obj
    elif isinstance(obj, collections.Mapping):
        return _step_cat_obj
    elif isinstance(obj, str):
        return _step_cat_string
    elif isinstance(obj, collections.Iterable):
        return _step_cat_array

    raise ValueError("Cannot create transformer for {}".format(obj))


@_curry2
def _check_for_method(method_name, fn):
    def _fn(*args):
        if len(args) == 0:
            return fn()
        obj = args[-1]
        if not hasattr(obj, method_name) or \
                not isinstance(getattr(obj, method_name), collections.Callable):
            return fn(*args)
        return getattr(obj, method_name)(*args[:-1])
    return _fn


def _pipe(f, g):
    return lambda *args: g(f(*args))


@_curry2
def _xtake(n, xf):
    class _XTake(_XFBase):
        def __init__(self, n, xf):
            self.xf = xf
            self.n = n
            self.i = 0

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            self.i += 1
            ret = result if self.n == 0 else self.xf._transducer_step(
                result, input)
            return _reduced(ret) if self.n >= 0 and self.i >= self.n else ret

    return _XTake(n, xf)


@functools.partial(_curry_n, 4, [])
def _xreduce_by(value_fn, value_acc, key_fn, xf):
    class _XReduceBy(_XFBase):
        def __init__(self, value_fn, value_acc, key_fn, xf):
            self.value_fn = value_fn
            self.value_acc = value_acc
            self.key_fn = key_fn
            self.xf = xf
            self.inputs = {}

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            for key, value in self.inputs.items():
                result = self.xf._transducer_step(result, value)
                if getattr(result, "_transducer_reduced", False):
                    result = result._transducer_value
                    break
            self.inputs = None
            return super().result(result)

        def _transducer_step(self, result, input):
            key = self.key_fn(input)
            self.inputs[key] = self.inputs.get(key, [key, self.value_acc])
            self.inputs[key][1] = self.value_fn(self.inputs[key][1], input)
            return result

    return _XReduceBy(value_fn, value_acc, key_fn, xf)


@_curry2
def _xaperture(n, xf):
    class _XAperture(_XFBase):
        def __init__(self, n, xf):
            self.xf = xf
            self.full = False
            self.acc = collections.deque([], n)

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            self.acc = None
            return self.xf._transducer_result(result)

        def _transducer_step(self, result, input):
            self.store(input)
            return self.xf._transducer_step(result, self.get_copy()) \
                if self.full else result

        def store(self, input):
            self.acc.append(input)
            if len(self.acc) == self.acc.maxlen:
                self.full = True

        def get_copy(self):
            return list(self.acc)

    return _XAperture(n, xf)


def _aperture(n, xs):
    idx = 0
    limit = len(xs) - (n - 1)
    acc = []
    while idx < limit:
        acc.append(xs[idx: idx + n])
        idx += 1
    return acc


def _make_flat(recursive):
    def flatt(xs):
        result = []
        for item in xs:
            if isinstance(item, collections.Sequence):
                value = flatt(item) if recursive else item
                result += value
            else:
                result.append(item)
        return result
    return flatt


def _xcat(xf):
    class _PreservingReduced(_XFBase):
        def __init__(self, xf):
            self.xf = xf

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return self.xf._transducer_result(result)

        def _transducer_step(self, result, input):
            ret = self.xf._transducer_step(result, input)
            return _force_reduced(ret) if getattr(ret, "_transducer_reduced", False) \
                else ret

    class _XCat(_XFBase):
        def __init__(self, xf):
            self.rxf = _PreservingReduced(xf)

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return self.rxf._transducer_result(result)

        def _transducer_step(self, result, input):
            return _reduce(self.rxf, result, [input]) \
                if not isinstance(input, collections.Sequence) \
                else _reduce(self.rxf, result, input)

    return _XCat(xf)


@_curry2
def _xchain(f, xf):
    from ..list import map

    return map(f, _xcat(xf))


def _index_of(xs, a, idx):
    for idx, item in enumerate(xs[idx:], idx):
        if _equals(item, a):
            return idx
    return -1


def _contains(a, xs):
    return _index_of(xs, a, 0) >= 0


@_curry2
def _xdrop(n, xf):
    class _XDrop(_XFBase):
        def __init__(self, n, xf):
            self.xf = xf
            self.n = n

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            if self.n > 0:
                self.n -= 1
                return result
            return self.xf._transducer_step(result, input)

    return _XDrop(n, xf)


@_curry2
def _xdrop_last(n, xf):
    class _XDropLast(_XFBase):
        def __init__(self, n, xf):
            self.xf = xf
            self.n = n
            self.full = False
            self.acc = collections.deque([], n)

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            if self.full:
                result = self.xf._transducer_step(result, self.acc[0])
            self.store(input)
            return result

        def store(self, input):
            self.acc.append(input)
            if len(self.acc) == self.acc.maxlen:
                self.full = True

    return _XDropLast(n, xf)


@_curry2
def _xdrop_last_while(fn, xf):
    class _XDropLastWhile(_XFBase):
        def __init__(self, fn, xf):
            self.f = fn
            self.xf = xf
            self.retained = []

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            self.retained = None
            return super().result(result)

        def _transducer_step(self, result, input):
            return self.retain(result, input) if self.f(input) else \
                self.flush(result, input)

        def flush(self, result, input):
            result = _reduce(
                self.xf._transducer_step, result, self.retained)
            self.retained = []
            return self.xf._transducer_step(result, input)

        def retain(self, result, input):
            self.retained.append(input)
            return result

    return _XDropLastWhile(fn, xf)


@_curry2
def _xdrop_repeats_with(pred, xf):
    class _XDropRepeatsWith(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf
            self.last_value = None
            self.seen_first_value = False

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            same_as_last = False
            if not self.seen_first_value:
                self.seen_first_value = True
            elif self.pred(self.last_value, input):
                same_as_last = True
            self.last_value = input
            return result if same_as_last else self.xf._transducer_step(
                result, input)

    return _XDropRepeatsWith(pred, xf)


@_curry2
def _xdrop_while(pred, xf):
    class _XDropWhile(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return super().result(result)

        def _transducer_step(self, result, input):
            if self.pred:
                if self.pred(input):
                    return result
                else:
                    self.pred = None
            return self.xf._transducer_step(result, input)

    return _XDropWhile(pred, xf)


@_curry2
def _xfind(pred, xf):
    class _XFind(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf
            self.found = False

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            if not self.found:
                result = self.xf._transducer_step(result, None)
            return self.xf._transducer_result(result)

        def _transducer_step(self, result, input):
            if self.pred(input):
                self.found = True
                result = _reduced(self.xf._transducer_step(result, input))
            return result

    return _XFind(pred, xf)


@_curry2
def _xfind_index(pred, xf):
    class _XFindIndex(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf
            self.idx = -1
            self.found = False

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            if not self.found:
                result = self.xf._transducer_step(result, -1)
            return self.xf._transducer_result(result)

        def _transducer_step(self, result, input):
            self.idx += 1
            if self.pred(input):
                self.found = True
                result = _reduced(self.xf._transducer_step(result, self.idx))
            return result

    return _XFindIndex(pred, xf)


@_curry2
def _xfind_last(pred, xf):
    class _XFindLast(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf
            self.last = None

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return self.xf._transducer_result(
                self.xf._transducer_step(result, self.last))

        def _transducer_step(self, result, input):
            if self.pred(input):
                self.last = input
            return result

    return _XFindLast(pred, xf)


@_curry2
def _xfind_last_index(pred, xf):
    class _XFindLastIndex(_XFBase):
        def __init__(self, pred, xf):
            self.pred = pred
            self.xf = xf
            self.idx = -1
            self.last_idx = -1

        def _transducer_init(self):
            return super().init()

        def _transducer_result(self, result):
            return self.xf._transducer_result(
                self.xf._transducer_step(result, self.last_idx))

        def _transducer_step(self, result, input):
            self.idx += 1
            if self.pred(input):
                self.last_idx = self.idx
            return result

    return _XFindLastIndex(pred, xf)
