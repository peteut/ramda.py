import inspect
import pytest
import ramda as R
from ramda.shared import eq
from .common import get_arity


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


@pytest.mark.skip()
def describe_add_index():
    @pytest.fixture
    def map_indexed():
        return R.add_index(R.map)

    def describe_unary_functions_like_map():
        # def times2(x) = lambda x: x * 2
        # add_index_param = lambda x, idx: x + idx
        pass

    def it_works_just_like_a_normal_map(map_indexed):
        eq(map_indexed(lambda x: x * 2, [1, 2, 3, 4]), [2, 4, 6, 8])


def describe_pipe():
    def it_is_a_variadic_function():
        eq(inspect.isfunction(R.pipe), True)
        eq(inspect.getargspec(R.pipe).args, [])

    def it_performs_left_to_right_function_composition():
        f = R.pipe(lambda x, base: int(x, base), R.multiply, R.map)

        eq(get_arity(f), 2)
        eq(f("10", 10)([1, 2, 3]), [10, 20, 30])
        eq(f("10", 2)([1, 2, 3]), [2, 4, 6])

    def it_throws_if_given_no_arguments():
        with pytest.raises(ValueError,
                           message="pipe requires at least one argument"):
            R.pipe()

    def it_can_be_applied_to_one_argument():
        f = lambda a, b, c: [a, b, c]
        g = R.pipe(f)
        eq(get_arity(g), 3)
        eq(g(1, 2, 3), [1, 2, 3])


def describe_compose():
    def is_a_variadic_function():
        eq(inspect.isfunction(R.compose), True)
        eq(inspect.getargspec(R.compose).args, [])

    def it_performs_right_to_left_function_composition():
        f = R.compose(R.map, R.multiply, lambda x, base: int(x, base))

        eq(get_arity(f), 2)
        eq(f("10", 10)([1, 2, 3]), [10, 20, 30])
        eq(f('10', 2)([1, 2, 3]), [2, 4, 6])

    def it_throws_if_given_no_arguments():
        with pytest.raises(ValueError,
                           message="compose requires at least one argument"):
            R.compose()

    def it_can_be_applied_to_one_argument():
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

    def it_return_a_function_with_correct_arity(concat2):
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
