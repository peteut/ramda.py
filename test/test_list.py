import types
import pytest
import ramda as R
from ramda.shared import eq
from .common import list_xf, get_arity


def describe_adjust():

    @pytest.fixture
    def xs():
        return [0, 1, 2, 3]

    def it_applies_the_given_function_to_the_value_at_the_given_index_of_the_supplied_array():
        eq(R.adjust(R.add(1), 2, [0, 1, 2, 3]), [0, 1, 3, 3])

    def it_offsets_negative_indexes_from_the_end_of_the_array():
        eq(R.adjust(R.add(1), -3, [0, 1, 2, 3]), [0, 2, 2, 3])

    def it_returns_the_original_array_if_the_supplied_index_is_out_of_bounds(xs):
        eq(R.adjust(R.add(1), 4, xs), xs)
        eq(R.adjust(R.add(1), -5, xs), xs)

    def it_does_not_mutate_the_original_array(xs):
        eq(R.adjust(R.add(1), 2, xs), [0, 1, 3, 3])
        eq(xs, [0, 1, 2, 3])

    def it_curries_the_arguments():
        eq(R.adjust(R.add(1))(2)([0, 1, 2, 3]), [0, 1, 3, 3])


def describe_into():

    @pytest.fixture
    def add():
        return R.add

    @pytest.fixture
    def is_odd():
        return lambda b: b % 2 == 1

    @pytest.fixture
    def add_xf():
        return types.SimpleNamespace(
            _transducer_init=R.always(0),
            _transducer_step=R.add,
            _transducer_result=R.identity)

    def it_transduces_into_arrays(add, is_odd):
        eq(R.into([], R.map(add(1)), [1, 2, 3, 4]), [2, 3, 4, 5])
        eq(R.into([], R.filter(is_odd), [1, 2, 3, 4]), [1, 3])
        # eq(R.into([], R.compose(R.map(add(1)), R.take(2)), [1, 2, 3, 4]), [2, 3])

    def it_transduces_into_strings(add, is_odd):
        eq(R.into("", R.map(add(1)), [1, 2, 3, 4]), "2345")
        eq(R.into("", R.filter(is_odd), [1, 2, 3, 4]), "13")
        # eq(R.into("", R.compose(R.map(add(1)), R.take(2)), [1, 2, 3, 4]), "23")

    def it_transduces_into_objects():
        eq(R.into({}, R.identity, [["a", 1], ["b", 2]]), {"a": 1, "b": 2})
        eq(R.into({}, R.identity, [{"a": 1}, {"b": 2, "c": 3}]),
           {"a": 1, "b": 2, "c": 3})

    def it_dispatches_to_objects_that_implement_reduce_function(add, is_odd):
        obj = {"x": [1, 2, 3], "reduce": lambda *_: "override"}
        eq(R.into([], R.map(add(1)), obj), "override")
        eq(R.into([], R.filter(is_odd), obj), "override")


def describe_all():

    @pytest.fixture
    def even():
        return lambda n: n % 2 == 0

    @pytest.fixture
    def T():
        return lambda *_: True

    @pytest.fixture
    def is_false():
        return lambda x: x is False

    @pytest.fixture
    def into_array():
        return R.into([])

    def it_returns_true_if_all_elements_satisfy_the_predicate(even, is_false):
        eq(R.all(even, [2, 4, 6, 8, 10, 12]), True)
        eq(R.all(is_false, [False, False, False]), True)

    def it_returns_false_if_any_element_fails_to_satisfy_the_predicate(even):
        eq(R.all(even, [2, 4, 6, 8, 9, 10]), False)

    def it_returns_true_into_array_if_all_elements_satisfy_the_predicate(
            even, is_false, into_array):
        eq(into_array(R.all(even), [2, 4, 6, 8, 10, 12]), [True])
        eq(into_array(R.all(is_false), [False, False, False]), [True])

    def it_returns_true_for_an_empty_list(T):
        eq(R.all(T, []), True)

    def it_works_with_more_complex_objects():
        xs = [{"x": "abc"}, {"x": "ade"}, {"x": "fghiajk"}]
        len_3 = lambda o: len(o["x"]) == 3
        has_a = lambda o: o["x"].find("a") > -1
        eq(R.all(len_3, xs), False)
        eq(R.all(has_a, xs), True)

    def it_dispatches_when_given_a_transformer_in_list_position(even):
        eq(R.all(even, list_xf).all, True)
        eq(R.all(even, list_xf).f, even)
        eq(R.all(even, list_xf).xf, list_xf)

    def it_is_curried(even):
        test = lambda n: even(n)
        eq(R.all(test)([2, 4, 6, 7, 8, 10]), False)


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


def describe_filter():

    @pytest.fixture
    def even():
        return lambda n: n % 2 == 0

    def it_reduces_an_array_to_those_matching_a_filter(even):
        eq(R.filter(even, [1, 2, 3, 4, 5]), [2, 4])

    def it_returns_an_empty_array_if_no_element_matches():
        eq(R.filter(lambda x: x > 100, [1, 9, 99]), [])

    def it_returns_an_empty_array_if_asked_to_filter_an_empty_array():
        eq(R.filter(lambda x: x > 100, []), [])

    def it_filters_objects():
        positive = lambda x: x > 0
        eq(R.filter(positive, {}), {})
        eq(R.filter(positive, {"x": 0, "y": 0, "z": 0}), {})
        eq(R.filter(positive, {"x": 1, "y": 0, "z": 0}), {"x": 1})
        eq(R.filter(positive, {"x": 1, "y": 2, "z": 0}), {"x": 1, "y": 2})
        eq(R.filter(positive, {"x": 1, "y": 2, "z": 3}), {"x": 1, "y": 2, "z": 3})

    def it_dispatches_to_passed_in_non_Array_object_with_a_filter_method():
        f = {"filter": lambda f: f("called f.filter")}
        eq(R.filter(R.identity, f), "called f.filter")

    def it_is_curried(even):
        only_even = R.filter(even)
        eq(only_even([1, 2, 3, 4, 5, 6, 7]), [2, 4, 6])


def describe_tail():

    def it_returns_the_tail_of_an_ordered_collection():
        eq(R.tail([1, 2, 3]), [2, 3])
        eq(R.tail([2, 3]), [3])
        eq(R.tail([3]), [])
        eq(R.tail([]), [])

        eq(R.tail("abc"), "bc")
        eq(R.tail("bc"), "c")
        eq(R.tail("c"), "")
        eq(R.tail(""), "")

    def it_throws_if_applied_to_null_or_undefined():
        with pytest.raises(TypeError):
            R.tail(None)
