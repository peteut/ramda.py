import inspect
import types
import collections
import pytest
import ramda as R
from ramda.shared import eq
from .common import get_arity


def describe_ap():
    @pytest.fixture
    def mult2():
        return lambda x: x * 2

    @pytest.fixture
    def plus3():
        return lambda x: x + 3

    def it_interprets_a_as_an_applicative(mult2, plus3):
        eq(R.ap([mult2, plus3], [1, 2, 3]), [2, 4, 6, 4, 5, 6])

    def it_interprets_fn_as_an_applicative():
        def f(r):
            return lambda a: r + a

        def g(r):
            return r * 2

        h = R.ap(f, g)
        eq(h(10), 10 + (10 * 2))
        eq(R.ap(R.add)(g)(10), 10 + (10 * 2))

    def it_displatches_to_the_passed_objects_ap_method():
        obj = types.SimpleNamespace(ap="called ap with {}".format)
        eq(R.ap(obj, 10), obj.ap(10))

    def it_is_curried(mult2, plus3):
        val = R.ap([mult2, plus3])
        eq(isinstance(val, collections.Callable), True)


def describe_apply():
    def it_applies_fn_to_arg_list():
        eq(R.apply(max, [1, 2, 3, -99, 42, 6, 7]), 42)

    def it_is_curried():
        eq(R.apply(max)([1, 2, 3, -99, 42, 6, 7]), 42)


def describe_curry_n():
    @pytest.fixture
    def source():
        def _source(*args):
            a, b, c = args
            return a * b * c
        return _source

    def it_accepts_an_arity(source):
        curried = R.curry_n(3, source)
        eq(curried(1)(2)(3), 6)
        eq(curried(1, 2)(3), 6)
        eq(curried(1)(2, 3), 6)
        eq(curried(1, 2, 3), 6)

    def it_can_be_partially_applied(source):
        curry3 = R.curry_n(3)
        curried = curry3(source)
        eq(get_arity(curried), 3)
        eq(curried(1)(2)(3), 6)
        eq(curried(1, 2)(3), 6)
        eq(curried(1)(2, 3), 6)
        eq(curried(1, 2, 3), 6)


def describe_curry():
    def it_curries_a_single_value():
        f = R.curry(lambda a, b, c, d: (a + b * c) / d)
        g = f(12)
        eq(g(3, 6, 2), 15)

    def it_curries_multiple_values():
        f = R.curry(lambda a, b, c, d: (a + b * c) / d)
        g = f(12, 3)
        eq(g(6, 2), 15)
        h = f(12, 3, 6)
        eq(h(2), 15)

    def it_allows_further_currying_of_a_curried_fn():
        f = R.curry(lambda a, b, c, d: (a + b * c) / d)
        g = f(12)
        eq(g(3, 6, 2), 15)
        h = g(3)
        eq(h(6, 2), 15)
        eq(g(3, 6)(2), 15)

    def it_properly_reports_the_length_of_the_curried_fn():
        f = R.curry(lambda a, b, c, d: (a + b * c) / d)
        eq(get_arity(f), 4)
        g = f(12)
        eq(get_arity(g), 3)
        h = g(3)
        eq(get_arity(h), 2)
        eq(get_arity(g(3, 6)), 1)

    def it_supports_R___placeholder():
        def f(a, b, c):
            return [a, b, c]

        g = R.curry(f)
        _ = R.__

        eq(g(1)(2)(3), [1, 2, 3])
        eq(g(1)(2, 3), [1, 2, 3])
        eq(g(1, 2)(3), [1, 2, 3])
        eq(g(1, 2, 3), [1, 2, 3])

        eq(g(_, 2, 3)(1), [1, 2, 3])
        eq(g(1, _, 3)(2), [1, 2, 3])
        eq(g(1, 2, _)(3), [1, 2, 3])

        eq(g(1, _, _)(2)(3), [1, 2, 3])
        eq(g(_, 2, _)(1)(3), [1, 2, 3])
        eq(g(_, _, 3)(1)(2), [1, 2, 3])

        eq(g(1, _, _)(2, 3), [1, 2, 3])
        eq(g(_, 2, _)(1, 3), [1, 2, 3])
        eq(g(_, _, 3)(1, 2), [1, 2, 3])

        eq(g(1, _, _)(_, 3)(2), [1, 2, 3])
        eq(g(_, 2, _)(_, 3)(1), [1, 2, 3])
        eq(g(_, _, 3)(_, 2)(1), [1, 2, 3])

        eq(g(_, _, _)(_, _)(_)(1, 2, 3), [1, 2, 3])
        eq(g(_, _, _)(1, _, _)(_, _)(2, _)(_)(3), [1, 2, 3])


@pytest.mark.skip()
def describe_add_index():
    @pytest.fixture
    def map_indexed():
        return R.add_index(R.map)

    def describe_un_ary_fns_like_map():
        # def times2(x) = lambda x: x * 2
        # add_index_param = lambda x, idx: x + idx
        pass

    def it_works_just_like_a_normal_map(map_indexed):
        eq(map_indexed(lambda x: x * 2, [1, 2, 3, 4]), [2, 4, 6, 8])


def describe_converge():
    @pytest.fixture
    def mult():
        return lambda a, b: a * b

    @pytest.fixture
    def f1(mult):
        return R.converge(mult, [lambda a: a,
                                 lambda a: a])

    @pytest.fixture
    def f2(mult):
        return R.converge(mult,
                          [lambda a: a,
                           lambda a, b: b])

    @pytest.fixture
    def f3(mult):
        return R.converge(mult,
                          [lambda a: a,
                           lambda a, b, c: c])

    def it_passes_the_results_of_applying_the_args_individually_to_two_separate_fns_into_a_single_one(mult):  # noqa
        # mult(add1(2), add3(2)) = mult(3, 5) = 3 * 15
        eq(R.converge(mult, [R.add(1), R.add(3)])(2), 15)

    def it_returns_a_fn_with_the_length_of_the_longest_arg(f1, f2, f3):
        eq(get_arity(f1), 1)
        eq(get_arity(f2), 2)
        eq(get_arity(f3), 3)

    def it_returns_a_curried_fn(f2, f3):
        eq(f2(6)(7), 42)
        eq(get_arity(f3(R.__)), 3)

    def it_works_with_empty_fns_list():
        fn = R.converge(lambda: 0, [])
        eq(get_arity(fn), 0)
        eq(fn(), 0)


@pytest.fixture
def just():
    class Just:
        def __init__(self, x):
            self.value = x
    return Just


def describe_empty():
    def it_dispatches_to_empty_method(just):
        class Nothing:
            pass
        Nothing.empty = staticmethod(lambda: Nothing())

        class Just(just):
            @staticmethod
            def empty():
                return Nothing()

        eq(isinstance(R.empty(Nothing()), Nothing), True)
        eq(isinstance(R.empty(Just(123)), Nothing), True)

    def it_dispatches_to_empty_fn_on_constructor(just):
        class Nothing:
            pass
        Nothing.empty = staticmethod(lambda: Nothing())

        class Just(just):
            @staticmethod
            def empty():
                return Nothing()

        eq(isinstance(R.empty(Nothing()), Nothing), True)
        eq(isinstance(R.empty(Just(123)), Nothing), True)

    def it_returns_empty_array_given_array():
        eq(R.empty([1, 2, 3]), [])

    def it_returns_empty_object_given_object():
        eq(R.empty({"x": 1, "y": 2}), {})

    def it_returns_empty_string_given_string():
        eq(R.empty("abc"), "")


def describe_pipe():
    def it_is_a_variadic_fn():
        eq(inspect.isfunction(R.pipe), True)
        eq(inspect.getargspec(R.pipe).args, [])

    def it_performs_left_to_right_fn_composition():
        f = R.pipe(lambda x, base: int(x, base), R.multiply, R.map)

        eq(get_arity(f), 2)
        eq(f("10", 10)([1, 2, 3]), [10, 20, 30])
        eq(f("10", 2)([1, 2, 3]), [2, 4, 6])

    def it_throws_if_given_no_args():
        with pytest.raises(ValueError,
                           message="pipe requires at least one arg"):
            R.pipe()

    def it_can_be_applied_to_one_arg():
        f = lambda a, b, c: [a, b, c]
        g = R.pipe(f)
        eq(get_arity(g), 3)
        eq(g(1, 2, 3), [1, 2, 3])


def describe_compose():
    def is_a_variadic_fn():
        eq(inspect.isfunction(R.compose), True)
        eq(inspect.getargspec(R.compose).args, [])

    def it_performs_right_to_left_fn_composition():
        f = R.compose(R.map, R.multiply, lambda x, base: int(x, base))

        eq(get_arity(f), 2)
        eq(f("10", 10)([1, 2, 3]), [10, 20, 30])
        eq(f("10", 2)([1, 2, 3]), [2, 4, 6])

    def it_throws_if_given_no_args():
        with pytest.raises(ValueError,
                           message="compose requires at least one arg"):
            R.compose()

    def it_can_be_applied_to_one_arg():
        f = lambda a, b, c: [a, b, c]
        g = R.compose(f)
        eq(get_arity(g), 3)
        eq(g(1, 2, 3), [1, 2, 3])


def describe_invoker():
    @pytest.fixture
    def concat2():
        return R.invoker(2, "concat")

    @pytest.fixture
    def add2():
        return R.invoker(1, "__add__")

    def it_return_a_fn_with_correct_arity(concat2):
        eq(get_arity(concat2), 3)

    def it_calls_the_method_on_the_object(add2):
        eq(add2([3, 4], [1, 2]), [1, 2, 3, 4])

    def it_throws_a_descriptive_type_error_if_method_does_not_exist():
        with pytest.raises(TypeError,
                           message="None does not habve a method named \"foo\""):
            R.invoker(0, "foo")(None)

        with pytest.raises(TypeError,
                           message="[1, 2, 3] does not have a method named \"foo\""):
            R.invoker(0, "foo")([1, 2, 3])

        with pytest.raises(TypeError,
                           message="[1, 2, 3] does not have a method named \"length\""):
            R.invoker(0, "length")([1, 2, 3])

    def it_curries_the_method_call(add2):
        eq(add2()([3, 4])([1, 2]), [1, 2, 3, 4])
        eq(add2([3, 4])([1, 2]), [1, 2, 3, 4])


def describe_n_ary():
    @pytest.fixture
    def to_array():
        return lambda *args: list(args)

    def it_turns_multiple_arg_fn_into_a_nullary_one(to_array):
        fn = R.n_ary(0, to_array)
        eq(get_arity(fn), 0)
        # eq(fn(1, 2, 3), [])

    def it_turns_multiple_arg_fn_into_a_ternary_one(to_array):
        fn = R.n_ary(3, to_array)
        eq(get_arity(fn), 3)
        # eq(fn(1, 2, 3, 4), [1, 2, 3])
        eq(fn(1), [1, None, None])

    def it_creates_fns_of_arity_less_than_or_equal_to_ten(to_array):
        fn = R.n_ary(10, to_array)
        eq(get_arity(fn), 10)
        eq(fn(*R.range(0, 10)), R.range(0, 10))

    def it_throws_if_n_is_greater_than_ten():
        with pytest.raises(ValueError,
                           message="First arg to n_ary must be a non-negative "
                           "integer no greater than ten"):
            R.n_ary(11, lambda: None)


def describe_lift_n():
    @pytest.fixture
    def add_n():
        return lambda *args: R.reduce(lambda a, b: a + b, 0, args)

    @pytest.fixture
    def add3():
        return lambda a, b, c: a + b + c

    @pytest.fixture
    def add_n3(add_n):
        return R.lift_n(3, add_n)

    @pytest.fixture
    def add_n4(add_n):
        return R.lift_n(4, add_n)

    @pytest.fixture
    def add_n5(add_n):
        return R.lift_n(5, add_n)

    def it_returna_a_fn(add3):
        eq(isinstance(R.lift_n(3, add3), collections.Callable), True)

    def it_limits_a_variadic_fn_to_the_specified_arity(add_n3):
        eq(add_n3([1, 10], [2], [3]), [6, 15])

    def it_can_lift_fns_of_any_arity(add_n3, add_n4, add_n5):
        eq(add_n3([1, 10], [2], [3]), [6, 15])
        eq(add_n4([1, 10], [2], [3], [40]), [46, 55])
        eq(add_n5([1, 10], [2], [3], [40], [500, 1000]), [546, 1046, 555, 1055])

    def it_is_curried(add_n):
        f4 = R.lift_n(4)
        eq(isinstance(f4, collections.Callable), True)
        eq(f4(add_n)([1], [2], [3], [4, 5]), [10, 11])

    def it_interprets_list_as_a_functor(add_n3):
        eq(add_n3([1, 2, 3], [10, 20], [100, 200, 300]),
           [111, 211, 311, 121, 221, 321, 112, 212, 312, 122, 222, 322,
            113, 213, 313, 123, 223, 323])
        eq(add_n3([1], [2], [3]), [6])
        eq(add_n3([1, 2], [10, 20], [100, 200]), [111, 211, 121, 221, 112, 212, 122, 222])

    def it_interprets_fn_as_a_functor(add_n3):
        converged_on_int = add_n3(R.add(2), R.multiply(3), R.subtract(4))
        converged_on_bool = R.lift_n(2, R.and_)(R.gt(R.__, 0), R.lt(R.__, 3))
        eq(isinstance(converged_on_int, collections.Callable), True)
        eq(isinstance(converged_on_bool, collections.Callable), True)
        eq(converged_on_int(10), (10 + 2) + (10 * 3) + (4 - 10))
        eq(converged_on_bool(0), (0 > 0) and (0 < 3))
        eq(converged_on_bool(1), (1 > 0) and (1 < 3))
        eq(converged_on_bool(2), (2 > 0) and (2 < 3))
        eq(converged_on_bool(3), (3 > 0) and (3 < 3))


def describe_lift():
    @pytest.fixture
    def add3():
        return R.curry(lambda a, b, c: a + b + c)

    @pytest.fixture
    def add4():
        return R.curry(lambda a, b, c, d: a + b + c + d)

    @pytest.fixture
    def add5():
        return R.curry(lambda a, b, c, d, e: a + b + c + d + e)

    @pytest.fixture
    def madd3(add3):
        return R.lift(add3)

    @pytest.fixture
    def madd4(add4):
        return R.lift(add4)

    @pytest.fixture
    def madd5(add5):
        return R.lift(add5)

    def it_returns_a_fn_if_called_with_just_a_fn():
        eq(isinstance(R.lift(R.add), collections.Callable), True)

    def it_produces_a_cross_product_of_list_values(madd3):
        eq(madd3([1, 2, 3], [1, 2], [1, 2, 3]),
           [3, 4, 5, 4, 5, 6, 4, 5, 6, 5, 6, 7, 5, 6, 7, 6, 7, 8])
        eq(madd3([1], [2], [3]), [6])
        eq(madd3([1, 2], [3, 4], [5, 6]), [9, 10, 10, 11, 10, 11, 11, 12])

    def it_can_lift_fns_of_any_arity(madd3, madd4, madd5):
        eq(madd3([1, 10], [2], [3]), [6, 15])
        eq(madd4([1, 10], [2], [3], [40]), [46, 55])
        eq(madd5([1, 10], [2], [3], [40], [500, 1000]), [546, 1046, 555, 1055])


def describe_flip():
    @pytest.fixture
    def f():
        return lambda a, b, c: " ".join([a, b, c])

    def it_returns_a_fn_which_inverts_the_first_two_args_to_the_supplied_fn(f):
        g = R.flip(f)
        eq(f("a", "b", "c"), "a b c")
        eq(g("a", "b", "c"), "b a c")

    def it_returns_a_curried_fn(f):
        g = R.flip(f)("a")
        eq(g("b", "c"), "b a c")


@pytest.mark.skip()
def describe_juxt():
    @pytest.fixture
    def hello():
        return lambda _: "hello"

    @pytest.fixture
    def bye():
        return lambda _: "bye"

    def it_works_with_no_fns_and_no_values():
        eq(R.juxt([])(), [])

    def it_works_with_no_fns_and_some_values():
        eq(R.juxt([])(2, 3), [])

    def it_works_with_1_fn_and_no_values(hello):
        eq(R.juxt([hello])(), ["hello"])

    def it_works_with_1_fn_and_1_value():
        eq(R.juxt([R.add(3)])(2), [5])

    def it_works_with_1_fn_and_some_values():
        eq(R.juxt([R.multiply])(2, 3), [6])

    def it_works_with_some_fns_and_no_values(hello, bye):
        eq(R.juxt([hello, bye])(), ["hello", "bye"])

    def it_works_with_some_fns_and_1_value():
        eq(R.juxt([R.multiply(2), R.add(3)])(2), [4, 5])

    def it_works_with_some_fns_and_some_values():
        eq(R.juxt([R.add, R.multiply])(2, 3), [5, 6])

    def it_retains_the_highest_arity(true):
        t = R.always(True)
        f = R.juxt([R.n_ary(1, t), R.n_ary(3, t), R.n_ary(2, t)])
        eq(f.length, 3)

    def it_returns_a_curried_function():
        eq(R.juxt([R.multiply, R.add])(2)(3), [6, 5])


def describe_of():
    def it_returns_its_arg_as_a_list():
        eq(R.of(100), [100])
        eq(R.of([100]), [[100]])
        eq(R.of(None), [None])
        eq(R.of([]), [[]])
