import types
import inspect
import pytest
import ramda as R
from ramda.shared import eq
from .common import list_xf, get_arity, _is_transformer


@pytest.fixture
def T():
    return lambda *_: True


@pytest.fixture
def is_odd():
    return lambda b: b % 2 == 1


@pytest.fixture
def into_array():
    return R.into([])


@pytest.fixture
def not_equal():
    return lambda a, b: id(a) is not id(b)


@pytest.fixture
def just():
    class Just:
        def __init__(self, x):
            self.value = x

        def equals(self, x):
            return isinstance(x, Just) and R.equals(x.value, self.value)

    return Just


@pytest.fixture
def even():
    return lambda n: isinstance(n, (int, float)) and n % 2 == 0


@pytest.fixture
def is_str():
    return lambda x: isinstance(x, str)


@pytest.fixture
def gt100():
    return lambda x: isinstance(x, (int, float)) and x > 100


@pytest.fixture
def x_gt100():
    def _pred(o):
        try:
            return o["x"] > 100
        except:
            pass
    return _pred


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
    def add_xf():
        return types.SimpleNamespace(
            _transducer_init=R.always(0),
            _transducer_step=R.add,
            _transducer_result=R.identity)

    def it_transduces_into_arrays(add, is_odd):
        eq(R.into([], R.map(add(1)), [1, 2, 3, 4]), [2, 3, 4, 5])
        eq(R.into([], R.filter(is_odd), [1, 2, 3, 4]), [1, 3])
        eq(R.into([], R.compose(R.map(add(1)), R.take(2)), [1, 2, 3, 4]), [2, 3])

    def it_transduces_into_strings(add, is_odd):
        eq(R.into("", R.map(add(1)), [1, 2, 3, 4]), "2345")
        eq(R.into("", R.filter(is_odd), [1, 2, 3, 4]), "13")
        eq(R.into("", R.compose(R.map(add(1)), R.take(2)), [1, 2, 3, 4]), "23")

    def it_transduces_into_objects():
        eq(R.into({}, R.identity, [["a", 1], ["b", 2]]), {"a": 1, "b": 2})
        eq(R.into({}, R.identity, [{"a": 1}, {"b": 2, "c": 3}]),
           {"a": 1, "b": 2, "c": 3})

    def it_dispatches_to_objects_that_implement_reduce(add, is_odd):
        obj = {"x": [1, 2, 3], "reduce": lambda *_: "override"}
        eq(R.into([], R.map(add(1)), obj), "override")
        eq(R.into([], R.filter(is_odd), obj), "override")

    def it_is_curried(add, into_array):
        add2 = R.map(add(2))
        result = into_array(add2)
        eq(result([1, 2, 3, 4]), [3, 4, 5, 6])

    def it_allows_custom_transformer(add_xf, add):
        into_sum = R.into(add_xf)
        add2 = R.map(add(2))
        result = into_sum(add2)
        eq(result([1, 2, 3, 4]), 18)

    def it_correctly_reports_the_arity_of_curried_versions(add):
        sum = R.into([], R.map(add))
        eq(get_arity(sum), 1)


def describe_all():
    @pytest.fixture
    def is_false():
        return lambda x: x is False

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


def describe_any():
    def it_returns_true_if_any_element_satisfies_the_predicate(is_odd):
        eq(R.any(is_odd, [2, 4, 6, 8, 10, 11, 12]), True)

    def it_returns_false_if_all_elements_fails_to_satisfy_the_predicate(is_odd):
        eq(R.any(is_odd, [2, 4, 6, 8, 10, 12]), False)

    def it_returns_true_into_array_if_any_element_satisfies_the_predicate(
            is_odd, into_array):
        eq(into_array(R.any(is_odd), [2, 4, 6, 8, 10, 11, 12]), [True])

    def it_returns_false_into_array_if_all_elements_fails_to_satisfy_the_predicate(
            is_odd, into_array):
        eq(into_array(R.any(is_odd), [2, 4, 6, 8, 10, 12]), [False])

    def it_works_with_more_complex_objects():
        people = [{"first": "Paul", "last": "Grenier"},
                  {"first": "Mike", "last": "Hurley"},
                  {"first": "Will", "last": "Klein"}]
        alliterative = lambda person: person["first"][0] == person["last"][0]
        eq(R.any(alliterative, people), False)
        people.append({"first": "Scott", "last": "Sauyet"})
        eq(R.any(alliterative, people), True)

    def it_can_use_a_configurable_function():
        teens = [{"name": "Alice", "age": 14},
                 {"name": "Betty", "age": 18},
                 {"name": "Cindy", "age": 17}]
        at_least = lambda age: lambda person: person["age"] >= age
        eq(R.any(at_least(16), teens), True)
        eq(R.any(at_least(21), teens), False)

    def it_returns_false_for_an_empty_list():
        eq(R.any(T, []), False)

    def it_returns_false_into_array_for_an_empty_list(into_array):
        eq(into_array(R.any(T), []), [False])

    def it_dispatches_when_given_a_transformer_in_list_position(is_odd):
        eq(R.any(is_odd, list_xf).any, False)
        eq(R.any(is_odd, list_xf).f, is_odd)
        eq(R.any(is_odd, list_xf).xf, list_xf)

    def it_is_curried(is_odd):
        test = lambda n: is_odd(n)
        eq(R.any(test)([2, 4, 6, 7, 8, 10]), True)


def describe_concat():
    @pytest.fixture
    def z1():
        ns = types.SimpleNamespace(x="z1")
        ns.concat = lambda that: " ".join([ns.x, that.x])
        return ns

    @pytest.fixture
    def z2():
        return types.SimpleNamespace(x="z2")

    def it_adds_combines_the_elements_of_the_two_lists():
        eq(R.concat(["a", "b"], ["c", "d"]), ["a", "b", "c", "d"])
        eq(R.concat([], ["c", "d"]), ["c", "d"])

    def it_works_on_strings():
        eq(R.concat("foo", "bar"), "foobar")
        eq(R.concat("x", ""), "x")
        eq(R.concat("", "x"), "x")
        eq(R.concat("", ""), "")

    def it_delegates_to_non_String_object_with_a_concat_method_as_second_param(z1, z2):
        eq(R.concat(z1, z2), "z1 z2")

    def it_is_curried():
        conc123 = R.concat([1, 2, 3])
        eq(conc123([4, 5, 6]), [1, 2, 3, 4, 5, 6])
        eq(conc123(["a", "b", "c"]), [1, 2, 3, "a", "b", "c"])

    def it_is_curried_like_a_binary_operator_that_accepts_an_initial_placeholder():
        append_bar = R.concat(R.__, "bar")
        eq(inspect.isfunction(append_bar), True)
        eq(append_bar("foo"), "foobar")

    def it_throws_if_attempting_to_combine_an_array_with_a_non_array():
        with pytest.raises(TypeError):
            R.concat([1], 2)

    def it_throws_if_not_an_array_String_or_object_with_a_concat_method():
        with pytest.raises(TypeError):
            R.concat({}, {})


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


def describe_take():
    def it_takes_only_the_first_n_elements_from_a_list():
        eq(R.take(3, ["a", "b", "c", "d", "e", "f", "g"]), ["a", "b", "c"])

    def it_returns_only_as_many_as_the_array_can_provide():
        eq(R.take(3, [1, 2]), [1, 2])
        eq(R.take(3, []), [])

    def it_returns_an_equivalent_list_if_n_is_lt_0():
        eq(R.take(-1, [1, 2, 3]), [1, 2, 3])
        eq(R.take(float("-inf"), [1, 2, 3]), [1, 2, 3])

    def it_never_returns_the_input_array(not_equal):
        xs = [1, 2, 3]

        eq(not_equal(R.take(3, xs), xs), True)
        eq(not_equal(R.take(float("inf"), xs), xs), True)
        eq(not_equal(R.take(-1, xs), xs), True)

    def it_can_operate_on_strings():
        eq(R.take(3, "Ramda"), "Ram")
        eq(R.take(2, "Ramda"), "Ra")
        eq(R.take(1, "Ramda"), "R")
        eq(R.take(0, "Ramda"), "")

    def it_handles_zero_correctly():
        eq(R.into([], R.take(0), [1, 2, 3]), [])

    def it_steps_correct_number_of_times(mocker):
        spy = types.SimpleNamespace(spy=R.identity)
        mocker.spy(spy, "spy")

        R.into([], R.compose(R.map(spy.spy), R.take(2)), [1, 2, 3])
        eq(spy.spy.call_count, 2)

    def it_transducer_called_for_every_member_of_list_if_n_is_lt_0(mocker):
        spy = types.SimpleNamespace(spy=R.identity)
        mocker.spy(spy, "spy")

        R.into([], R.compose(R.map(spy.spy), R.take(-1)), [1, 2, 3])
        eq(spy.spy.call_count, 3)


def describe_reduce_by():
    @pytest.fixture
    def sum_values():
        return lambda acc, obj: acc + obj["val"]

    @pytest.fixture
    def by_type():
        return lambda x: x["type"]

    @pytest.fixture
    def sum_input():
        return [
            {"type": "A", "val": 10},
            {"type": "B", "val": 20},
            {"type": "A", "val": 30},
            {"type": "A", "val": 40},
            {"type": "C", "val": 50},
            {"type": "B", "val": 60}]

    def it_splits_the_list_into_groups_according_to_the_grouping_function():
        grade = lambda score: "F" if score < 65 else "D" if score < 70 else "C" if score < 80 \
            else "B" if score < 90 else "A"
        students = [
            {"name": "Abby", "score": 84},
            {"name": "Brad", "score": 73},
            {"name": "Chris", "score": 89},
            {"name": "Dianne", "score": 99},
            {"name": "Eddy", "score": 58},
            {"name": "Fred", "score": 66},
            {"name": "Gillian", "score": 91},
            {"name": "Hannah", "score": 78},
            {"name": "Irene", "score": 85},
            {"name": "Jack", "score": 69}]
        by_grade = lambda student: grade(student.get("score", -1))
        collect_names = lambda acc, student: acc.append(student["name"]) or acc

        eq(R.reduce_by(collect_names, [], by_grade, students), {
            "A": ["Dianne", "Gillian"],
            "B": ["Abby", "Chris", "Irene"],
            "C": ["Brad", "Hannah"],
            "D": ["Fred", "Jack"],
            "F": ["Eddy"]})

    def it_returns_an_empty_object_if_given_an_empty_array(sum_values, by_type):
        eq(R.reduce_by(sum_values, 0, by_type, []), {})

    def it_is_curried(sum_input, sum_values, by_type):
        reduce_to_sums_by = R.reduce_by(sum_values, 0)
        sum_by_type = reduce_to_sums_by(by_type)
        eq(sum_by_type(sum_input), {"A": 80, "B": 80, "C": 50})

    def it_correctly_reports_the_arity_of_curried_versions(sum_values, by_type):
        inc = R.reduce_by(sum_values, 0)(by_type)
        eq(get_arity(inc), 1)

    def it_can_act_as_a_transducer(sum_values, by_type, sum_input):
        reduce_to_sums_by = R.reduce_by(sum_values, 0)
        sum_by_type = reduce_to_sums_by(by_type)
        eq(R.into(
            {},
            R.compose(sum_by_type, R.map(R.adjust(R.multiply(10), 1))),
            sum_input),
            {"A": 800, "B": 800, "C": 500})


def describe_reduced():
    @pytest.fixture
    def stop_if_gte_10():
        def _fn(acc, v):
            result = acc + v
            if result >= 10:
                result = R.reduced(result)
            return result
        return _fn

    def it_wraps_a_value():
        v = {}
        eq(R.reduced(v)._transducer_value, v)

    def it_flags_value_as_reduced():
        eq(R.reduced({})._transducer_reduced, True)

    def it_short_circuits_reduce(stop_if_gte_10):
        eq(R.reduce(stop_if_gte_10, 0, [1, 2, 3, 4, 5]), 10)


def describe_reduce_right():
    @pytest.fixture
    def avg():
        return lambda a, b: (a + b) / 2

    def it_folds_lists_in_the_right_order():
        eq(R.reduce_right(lambda a, b: a + b, "", ["a", "b", "c", "d"]), "abcd")

    def it_folds_subtract_over_arrays_in_the_right_order():
        eq(R.reduce_right(lambda a, b: a - b, 0, [1, 2, 3, 4]), -2)

    def it_folds_simple_functions_over_arrays_with_the_supplied_accumulator(avg):
        eq(R.reduce_right(avg, 54, [12, 4, 10, 6]), 12)

    def it_returns_the_accumulator_for_an_empty_array(avg):
        eq(R.reduce_right(avg, 0, []), 0)

    def it_is_curried(avg):
        something = R.reduce_right(avg, 54)
        rcat = R.reduce_right(R.concat, "")
        eq(something([12, 4, 10, 6]), 12)
        eq(rcat(["1", "2", "3", "4"]), "1234")

    def it_correctly_reports_the_arity_of_curried_versions(avg):
        something = R.reduce_right(avg, 0)
        eq(get_arity(something), 1)


def describe_aperture():
    @pytest.fixture
    def seven_ls():
        return [1, 2, 3, 4, 5, 6, 7]

    def it_creates_a_list_of_n_tuples_from_a_list(seven_ls):
        eq(R.aperture(1, seven_ls), [[1], [2], [3], [4], [5], [6], [7]])
        eq(R.aperture(2, seven_ls), [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])
        eq(R.aperture(3, seven_ls), [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]])
        eq(R.aperture(4, [1, 2, 3, 4]), [[1, 2, 3, 4]])

    def it_returns_an_empty_list_when_n_gt_list_length(seven_ls):
        eq(R.aperture(6, [1, 2, 3]), [])
        eq(R.aperture(1, []), [])

    def it_is_curried(seven_ls):
        pairwise = R.aperture(2)
        eq(pairwise(seven_ls), [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])

    def it_can_act_as_a_transducer(seven_ls):
        eq(R.into([], R.aperture(2), seven_ls), [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])


def describe_append():
    def it_adds_the_element_to_the_end_of_the_list():
        eq(R.append("z", ["x", "y"]), ["x", "y", "z"])
        eq(R.append(["a", "z"], ["x", "y"]), ["x", "y", ["a", "z"]])

    def it_works_on_empty_list():
        eq(R.append(1, []), [1])

    def it_is_curried():
        eq(inspect.isfunction(R.append(4)), True)
        eq(R.append(1)([4, 3, 2]), [4, 3, 2, 1])


def describe_chain():
    @pytest.fixture
    def add1():
        return lambda x: [x + 1]

    @pytest.fixture
    def dec():
        return lambda x: [x - 1]

    @pytest.fixture
    def times2():
        return lambda x: [x * 2]

    def it_maps_a_function_over_a_nested_list_and_returns_the_shallow_flattened_result(
            times2):
        eq(R.chain(times2, [1, 2, 3, 1, 0, 10, -3, 5, 7]), [2, 4, 6, 2, 0, 20, -6, 10, 14])
        eq(R.chain(times2, [1, 2, 3]), [2, 4, 6])

    def it_does_not_flatten_recursively():
        f = lambda xs: [xs[0]] if len(xs) else []
        eq(R.chain(f, [[1], [[2], 100], [], [3, [4]]]), [1, [2], 3])

    def it_maps_a_function_into_a_shallow_flat_result(into_array, times2):
        eq(into_array(R.chain(times2), [1, 2, 3, 4]), [2, 4, 6, 8])

    def it_interprets_function_as_a_monad():
        h = lambda r: r * 2
        f = lambda a: lambda r: r + a
        bound = R.chain(f, h)
        # // (>>=) :: (r -> a) -> (a -> r -> b) -> (r -> b)
        # // h >>= f = \w -> f (h w) w
        eq(bound(10), (10 * 2) + 10)
        eq(R.chain(R.append, R.head)([1, 2, 3]), [1, 2, 3, 1])

    def it_dispatches_to_objects_that_implement_chain(add1):
        obj = {"x": 100}
        obj["chain"] = lambda f: f(obj["x"])
        eq(R.chain(add1, obj), [101])

    def it_dispatches_to_transformer_objects(add1):
        eq(_is_transformer(R.chain(add1, list_xf)), True)

    def it_composes(times2, dec):
        mdouble = R.chain(times2)
        mdec = R.chain(dec)
        eq(mdec(mdouble([10, 20, 30])), [19, 39, 59])

    def it_can_compose_transducer_style(times2, dec, into_array):
        mdouble = R.chain(times2)
        mdec = R.chain(dec)
        xcomp = R.compose(mdec, mdouble)
        eq(into_array(xcomp, [10, 20, 30]), [18, 38, 58])

    def it_is_curried(add1):
        flat_inc = R.chain(add1)
        eq(flat_inc([1, 2, 3, 4, 5, 6]), [2, 3, 4, 5, 6, 7])

    def it_correctly_reports_the_arity_of_curried_versions(add1):
        inc = R.chain(add1)
        eq(get_arity(inc), 1)


def describe_contains():
    def it_returns_true_if_an_element_is_in_a_list():
        eq(R.contains(7, [1, 2, 3, 9, 8, 7, 100, 200, 300]), True)

    def it_returns_false_if_an_element_is_not_in_a_list():
        eq(R.contains(99, [1, 2, 3, 9, 8, 7, 100, 200, 300]), False)

    def it_returns_false_for_the_empty_list():
        eq(R.contains(1, []), False)

    def it_has_r_equals_semantics(just):
        eq(R.contains(float("nan"), [float("nan")]), True)
        eq(R.contains(just([42]), [just([42])]), True)

    def it_is_curried():
        eq(inspect.isfunction(R.contains(7)), True)
        eq(R.contains(7)([1, 2, 3]), False)
        eq(R.contains(7)([1, 2, 7, 3]), True)

    def it_is_curried_like_a_binary_operator_that_accepts_an_initial_placeholdern():
        is_digit = R.contains(R.__, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        eq(inspect.isfunction(is_digit), True)
        eq(is_digit("0"), True)
        eq(is_digit("1"), True)
        eq(is_digit("x"), False)


def describe_drop():
    def it_skips_the_first_n_elements_from_a_list_returning_the_remainder():
        eq(R.drop(3, ["a", "b", "c", "d", "e", "f", "g"]), ["d", "e", "f", "g"])

    def it_returns_an_empty_array_if_n_is_too_large():
        eq(R.drop(20, ["a", "b", "c", "d", "e", "f", "g"]), [])

    def it_returns_an_equivalent_list_if_n_is_lte_0():
        eq(R.drop(0, [1, 2, 3]), [1, 2, 3])
        eq(R.drop(-1, [1, 2, 3]), [1, 2, 3])
        eq(R.drop(float("-inf"), [1, 2, 3]), [1, 2, 3])

    def it_never_returns_the_input_array(not_equal):
        xs = [1, 2, 3]

        eq(not_equal(id(R.drop(0, xs)), id(xs)), True)
        eq(not_equal(id(R.drop(-1, xs)), id(xs)), True)

    def it_can_operate_on_strings():
        eq(R.drop(3, "Ramda"), "da")
        eq(R.drop(4, "Ramda"), "a")
        eq(R.drop(5, "Ramda"), "")
        eq(R.drop(6, "Ramda"), "")

    def it_dispatches_when_given_a_transformer_in_list_position():
        drop3 = R.drop(3)
        eq(drop3(list_xf).n, 3)
        eq(drop3(list_xf).xf, list_xf)

    def it_can_act_as_a_transducer(into_array):
        drop3 = R.drop(3)
        eq(into_array(drop3, [1, 2, 3, 4]), [4])
        eq(into_array(drop3, [1, 2, 3]), [])


def describe_drop_last():
    def it_skips_the_last_n_elements_from_a_list_returning_the_remainder():
        eq(R.drop_last(3, ["a", "b", "c", "d", "e", "f", "g"]), ["a", "b", "c", "d"])

    def it_returns_an_empty_array_if_n_is_too_large():
        eq(R.drop_last(20, ["a", "b", "c", "d", "e", "f", "g"]), [])

    def it_returns_an_equivalent_list_if_n_is_lte_0():
        eq(R.drop_last(0, [1, 2, 3]), [1, 2, 3])
        eq(R.drop_last(-1, [1, 2, 3]), [1, 2, 3])
        eq(R.drop_last(float("-inf"), [1, 2, 3]), [1, 2, 3])

    def it_never_returns_the_input_array(not_equal):
        xs = [1, 2, 3]

        eq(not_equal(R.drop_last(0, xs), xs), True)
        eq(not_equal(R.drop_last(-1, xs), xs), True)

    def it_can_operate_on_strings():
        eq(R.drop_last(3, "Ramda"), "Ra")

    def it_is_curried():
        drop_last2 = R.drop_last(2)
        eq(drop_last2(["a", "b", "c", "d", "e"]), ["a", "b", "c"])
        eq(drop_last2(["x", "y", "z"]), ["x"])

    def it_dispatches_when_given_a_transformer_in_list_position():
        drop_last2 = R.drop_last(2)
        eq(drop_last2(list_xf).n, 2)
        eq(drop_last2(list_xf).full, False)
        eq(drop_last2(list_xf).xf, list_xf)

    def it_can_act_as_a_transducer(into_array):
        drop_last2 = R.drop_last(2)
        eq(into_array(drop_last2, [1, 2, 3, 4]), [1, 2])
        eq(into_array(drop_last2, []), [])


def describe_drop_last_while():
    def it_skips_elements_while_the_function_reports_true():
        eq(R.drop_last_while(lambda x: x >= 5, [1, 3, 5, 7, 9]), [1, 3])

    def it_returns_an_empty_list_for_an_empty_list():
        eq(R.drop_last_while(lambda _: False, []), [])
        eq(R.drop_last_while(lambda _: False, []), [])

    def it_starts_at_the_right_arg_and_acknowledges_none():
        sublist = R.drop_last_while(lambda x: x is not None, [1, 3, None, 5, 7])
        eq(len(sublist), 3)
        eq(sublist[0], 1)
        eq(sublist[1], 3)
        eq(sublist[2], None)

    def it_is_curried():
        drop_gt_7 = R.drop_last_while(lambda x: x > 7)
        eq(drop_gt_7([1, 3, 5, 7, 9]), [1, 3, 5, 7])
        eq(drop_gt_7([1, 3, 5]), [1, 3, 5])

    def it_can_act_as_a_transducer(into_array):
        drop_lt_7 = R.drop_last_while(lambda x: x < 7)
        eq(into_array(drop_lt_7, [1, 3, 5, 7, 9, 1, 2]), [1, 3, 5, 7, 9])
        eq(into_array(drop_lt_7, [1, 3, 5]), [])


def describe_drop_repeats_with():
    @pytest.fixture
    def objs():
        return [{"i": 1}, {"i": 2}, {"i": 3}, {"i": 4}, {"i": 5}, {"i": 3}]

    @pytest.fixture
    def objs2():
        return[
            {"i": 1}, {"i": 1}, {"i": 1}, {"i": 2}, {"i": 3},
            {"i": 3}, {"i": 4}, {"i": 4}, {"i": 5}, {"i": 3}]

    @pytest.fixture
    def eq_i():
        return lambda x, y: x["i"] == y["i"]  # FIXME: R.eqProps("i")

    def it_removes_repeated_elements_based_on_predicate(objs, objs2, eq_i):
        eq(R.drop_repeats_with(eq_i, objs2), objs)
        eq(R.drop_repeats_with(eq_i, objs), objs)

    def it_keeps_elements_from_the_left(eq_i):
        eq(
            R.drop_repeats_with(
                eq_i,
                [{"i": 1, "n": 1}, {"i": 1, "n": 2}, {"i": 1, "n": 3},
                 {"i": 4, "n": 1}, {"i": 4, "n": 2}]),
            [{"i": 1, "n": 1}, {"i": 4, "n": 1}])

    def it_returns_an_empty_array_for_an_empty_array(eq_i):
        eq(R.drop_repeats_with(eq_i, []), [])

    def it_is_curried(objs, objs2, eq_i):
        eq(inspect.isfunction(R.drop_repeats_with(eq_i)), True)
        eq(R.drop_repeats_with(eq_i)(objs), objs)
        eq(R.drop_repeats_with(eq_i)(objs2), objs)

    def it_can_act_as_a_transducer(eq_i, objs, objs2):
        eq(R.into([], R.drop_repeats_with(eq_i), objs2), objs)


def describe_drop_repeats():
    @pytest.fixture
    def objs():
        return [1, 2, 3, 4, 5, 3, 2]

    @pytest.fixture
    def objs2():
        return [1, 2, 2, 2, 3, 4, 4, 5, 5, 3, 2, 2]

    def it_removes_repeated_elements(objs, objs2):
        eq(R.drop_repeats(objs2), objs)
        eq(R.drop_repeats(objs), objs)

    def it_returns_an_empty_array_for_an_empty_array():
        eq(R.drop_repeats([]), [])

    def it_can_act_as_a_transducer(objs2, objs):
        eq(R.into([], R.drop_repeats, objs2), objs)

    def it_has_equals_semantics(just):
        # eq(get_arity(R.drop_repeats([0, -0])), 2)
        # eq(get_arity(R.drop_repeats([-0, 0])), 2)
        eq(len(R.drop_repeats([float("nan"), float("nan")])), 1)
        eq(len(R.drop_repeats([just([42]), just([42])])), 1)


def describe_drop_while():
    def it_skips_elements_while_the_function_reports_true():
        eq(R.drop_while(lambda x: x < 5, [1, 3, 5, 7, 9]), [5, 7, 9])

    def it_returns_an_empty_list_for_an_empty_list():
        eq(R.drop_while(lambda _: True, []), [])
        eq(R.drop_while(lambda _: True, []), [])

    def it_starts_at_the_right_arg_and_acknowledges_none():
        sublist = R.drop_while(lambda x: x is not None, [1, 3, None, 5, 7])
        eq(len(sublist), 3)
        eq(sublist[0], None)
        eq(sublist[1], 5)
        eq(sublist[2], 7)

    def it_is_curried():
        drop_lt_7 = R.drop_while(lambda x: x < 7)
        eq(drop_lt_7([1, 3, 5, 7, 9]), [7, 9])
        eq(drop_lt_7([2, 4, 6, 8, 10]), [8, 10])

    def it_can_act_as_a_transducer(into_array):
        eq(into_array(R.drop_while(lambda x: x < 7), [1, 3, 5, 7, 9]), [7, 9])


def describe_ends_with():
    def it_should_return_true_when_a_string_ends_with_the_provided_value():
        eq(R.ends_with("c", "abc"), True)

    def it_should_return_true_when_a_long_string_ends_with_the_provided_value():
        eq(R.ends_with("ology", "astrology"), True)

    def it_should_return_false_when_a_string_does_not_end_with_the_provided_value():
        eq(R.ends_with("b", "abc"), False)

    def it_should_return_false_when_a_long_string_does_not_end_with_the_provided_value():
        eq(R.ends_with("olog", "astrology"), False)

    def it_should_return_true_when_an_array_ends_with_the_provided_value():
        eq(R.ends_with(["c"], ["a", "b", "c"]), True)

    def it_should_return_true_when_an_array_ends_with_the_provided_values():
        eq(R.ends_with(["b", "c"], ["a", "b", "c"]), True)

    def it_should_return_false_when_an_array_does_not_end_with_the_provided_value():
        eq(R.ends_with(["b"], ["a", "b", "c"]), False)

    def it_should_return_false_when_an_array_does_not_end_with_the_provided_values():
        eq(R.ends_with(["a", "b"], ["a", "b", "c"]), False)


def describe_find():
    obj1 = {"x": 100}
    obj2 = {"x": 200}
    a = [11, 10, 9, "cow", obj1, 8, 7, 100, 200, 300, obj2, 4, 3, 2, 1, 0]

    def it_returns_the_first_element_that_satisfies_the_predicate(
            even, is_str, gt100, x_gt100):
        eq(R.find(even, a), 10)
        eq(R.find(gt100, a), 200)
        eq(R.find(is_str, a), "cow")
        eq(R.find(x_gt100, a), obj2)

    def it_transduces_the_first_element_that_satisfies_the_predicate_into_an_array(
            into_array, even, gt100, is_str, x_gt100):
        eq(into_array(R.find(even), a), [10])
        eq(into_array(R.find(gt100), a), [200])
        eq(into_array(R.find(is_str), a), ["cow"])
        eq(into_array(R.find(x_gt100), a), [obj2])

    def it_returns_none_when_no_element_satisfies_the_predicate(even):
        eq(R.find(even, ["zing"]), None)

    def it_returns_none_in_array_when_no_element_satisfies_the_predicate_into_an_array(
            into_array, even):
        eq(into_array(R.find(even), ["zing"]), [None])

    def it_returns_none_when_given_an_empty_list(even):
        eq(R.find(even, []), None)

    def it_returns_none_into_an_array_when_given_an_empty_list(into_array, even):
        eq(into_array(R.find(even), []), [None])

    def it_is_curried(even):
        eq(inspect.isfunction(R.find(even)), True)
        eq(R.find(even)(a), 10)


def describe_find_index():
    obj1 = {"x": 100}
    obj2 = {"x": 200}
    a = [11, 10, 9, "cow", obj1, 8, 7, 100, 200, 300, obj2, 4, 3, 2, 1, 0]

    def it_returns_the_index_of_the_first_element_that_satisfies_the_predicate(
            even, is_str, gt100, x_gt100):
        eq(R.find_index(even, a), 1)
        eq(R.find_index(gt100, a), 8)
        eq(R.find_index(is_str, a), 3)
        eq(R.find_index(x_gt100, a), 10)

    def it_returns_the_index_of_the_first_element_that_satisfies_the_predicate_into_an_array(
            into_array, even, gt100, is_str, x_gt100):
        eq(into_array(R.find_index(even), a), [1])
        eq(into_array(R.find_index(gt100), a), [8])
        eq(into_array(R.find_index(is_str), a), [3])
        eq(into_array(R.find_index(x_gt100), a), [10])

    def it_returns_minus_1_when_no_element_satisfies_the_predicate(even):
        eq(R.find_index(even, ["zing"]), -1)
        eq(R.find_index(even, []), -1)

    def it_returns_minus_1_in_array_when_no_element_satisfies_the_predicate_into_an_array(
            into_array, even):
        eq(into_array(R.find_index(even), ["zing"]), [-1])

    def it_is_curried(even):
        eq(inspect.isfunction(R.find_index(even)), True)
        eq(R.find_index(even)(a), 1)


def describe_find_last():
    obj1 = {"x": 100}
    obj2 = {"x": 200}
    a = [11, 10, 9, "cow", obj1, 8, 7, 100, 200, 300, obj2, 4, 3, 2, 1, 0]

    def it_returns_the_index_of_the_last_element_that_satisfies_the_predicate(
            even, is_str, gt100, x_gt100):
        eq(R.find_last(even, a), 0)
        eq(R.find_last(gt100, a), 300)
        eq(R.find_last(is_str, a), "cow")
        eq(R.find_last(x_gt100, a), obj2)

    def it_returns_the_last_element_that_satisfies_the_predicate_into_an_array(
            into_array, even, gt100, is_str, x_gt100):
        eq(into_array(R.find_last(even), a), [0])
        eq(into_array(R.find_last(gt100), a), [300])
        eq(into_array(R.find_last(is_str), a), ["cow"])
        eq(into_array(R.find_last(x_gt100), a), [obj2])

    def it_returns_none_when_no_element_satisfies_the_predicate(
            even):
        eq(R.find_last(even, ["zing"]), None)

    def it_returns_none_into_an_array_when_no_element_satisfies_the_predicate(
            into_array, even):
        eq(into_array(R.find_last(even), ["zing"]), [None])

    def it_works_when_the_first_element_matches(even):
        eq(R.find_last(even, [2, 3, 5]), 2)

    def it_does_not_go_into_an_infinite_loop_on_an_empty_array():
        eq(R.find_last(even, []), None)

    def it_is_curried(even):
        eq(inspect.isfunction(R.find_last(even)), True)
        eq(R.find_last(even)(a), 0)


def describe_find_last_index():
    obj1 = {"x": 100}
    obj2 = {"x": 200}
    a = [11, 10, 9, "cow", obj1, 8, 7, 100, 200, 300, obj2, 4, 3, 2, 1, 0]

    def it_returns_the_index_of_the_last_element_that_satisfies_the_predicate(
            even, is_str, gt100, x_gt100):
        eq(R.find_last_index(even, a), 15)
        eq(R.find_last_index(gt100, a), 9)
        eq(R.find_last_index(is_str, a), 3)
        eq(R.find_last_index(x_gt100, a), 10)

    def it_returns_minus_1_when_no_element_satisfies_the_predicate(
            even):
        eq(R.find_last_index(even, ["zing"]), -1)

    def it_returns_the_index_of_the_last_element_into_an_array_that_satisfies_the_predicate(
            into_array, even, gt100, is_str, x_gt100):
        eq(into_array(R.find_last_index(even), a), [15])
        eq(into_array(R.find_last_index(gt100), a), [9])
        eq(into_array(R.find_last_index(is_str), a), [3])
        eq(into_array(R.find_last_index(x_gt100), a), [10])

    def it_returns_minus_1_into_an_array_when_no_element_satisfies_the_predicate(
            into_array, even):
        eq(into_array(R.find_last_index(even), ["zing"]), [-1])

    def it_works_when_the_first_element_matches(
            even):
        eq(R.find_last_index(even, [2, 3, 5]), 0)

    def it_does_not_go_into_an_infinite_loop_on_an_empty_array(even):
        eq(R.find_last_index(even, []), -1)

    def it_is_curried(even):
        eq(inspect.isfunction(R.find_last_index(even)), True)
        eq(R.find_last_index(even)(a), 15)


def describe_nth():
    @pytest.fixture
    def xs():
        return ["foo", "bar", "baz", "quux"]

    def it_accepts_positive_offsets(xs):
        eq(R.nth(0, xs), "foo")
        eq(R.nth(1, xs), "bar")
        eq(R.nth(2, xs), "baz")
        eq(R.nth(3, xs), "quux")
        eq(R.nth(4, xs), None)

        eq(R.nth(0, "abc"), "a")
        eq(R.nth(1, "abc"), "b")
        eq(R.nth(2, "abc"), "c")
        eq(R.nth(3, "abc"), "")

    def it_accepts_negative_offsets(xs):
        eq(R.nth(-1, xs), "quux")
        eq(R.nth(-2, xs), "baz")
        eq(R.nth(-3, xs), "bar")
        eq(R.nth(-4, xs), "foo")
        eq(R.nth(-5, xs), None)

        eq(R.nth(-1, "abc"), "c")
        eq(R.nth(-2, "abc"), "b")
        eq(R.nth(-3, "abc"), "a")
        eq(R.nth(-4, "abc"), "")

    def it_throws_if_applied_to_none():
        with pytest.raises(TypeError):
            R.nth(0, None)


def describe_head():
    def it_returns_the_first_element_of_an_ordered_collection():
        eq(R.head([1, 2, 3]), 1)
        eq(R.head([2, 3]), 2)
        eq(R.head([3]), 3)
        eq(R.head([]), None)

        eq(R.head("abc"), "a")
        eq(R.head("bc"), "b")
        eq(R.head("c"), "c")
        eq(R.head(""), "")

    def it_throws_if_applied_to_none():
        with pytest.raises(TypeError):
            R.head(None)
