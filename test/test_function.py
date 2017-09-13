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


def describe_map():

    @pytest.fixture
    def times2():
        return lambda x: x * 2

    @pytest.fixture
    def add1():
        return lambda x: x + 1

    @pytest.fixture
    def dec():
        return lambda x: x - 1

    def it_maps_simple_functions_over_arrays(times2):
        eq(R.map(times2, [1, 2, 3, 4]), [2, 4, 6, 8])

    def it_maps_over_objects(dec):
        eq(R.map(dec, {}), {})
        eq(R.map(dec, {"x": 4, "y": 5, "z": 6}), {"x": 3, "y": 4, "z": 5})

    def it_interprets_function_as_a_functor():
        f = lambda a: a - 1
        g = lambda b: b * 2
        h = R.map(f, g)
        eq(h(10), (10 * 2) - 1)

    def it_composes(times2, dec):
        mdouble = R.map(times2)
        mdec = R.map(dec)
        eq(mdec(mdouble([10, 20, 30])), [19, 39, 59])

    def it_is_curried(add1):
        inc = R.map(add1)
        eq(inc([1, 2, 3]), [2, 3, 4])

    def it_correctly_reports_the_arity_of_curried_versions(add1):
        inc = R.map(add1)
        eq(get_arity(inc), 1)


def describe_pipe():

    def it_is_a_variadic_function():
        eq(inspect.isfunction(R.pipe), True)
        eq(inspect.getargspec(R.pipe).args, [])

    def it_performs_left_to_right_function_composition():
        f = R.pipe(lambda x, base: int(x, base), R.multiply, R.map)

        eq(len(inspect.signature(f).parameters), 2)
        eq(f("10", 10)([1, 2, 3]), [10, 20, 30])
        eq(f("10", 2)([1, 2, 3]), [2, 4, 6])

    def it_throws_if_given_no_arguments():
        with pytest.raises(ValueError,
                           message="pipe requires at least one argument"):
            R.pipe()

    def it_can_be_applied_to_one_argument():
        f = lambda a, b, c: [a, b, c]
        g = R.pipe(f)
        eq(len(inspect.signature(g).parameters), 3)
        eq(g(1, 2, 3), [1, 2, 3])
