import pytest
import ramda as R
from ramda.shared import eq
from .common import list_xf


def describe_adjuxt():

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

    def it_returns_true_if_all_elements_satisfy_the_predicate(even, is_false):
        eq(R.all(even, [2, 4, 6, 8, 10, 12]), True)
        eq(R.all(is_false, [False, False, False]), True)

    def it_returns_false_if_any_element_fails_to_satisfy_the_predicate(even):
        eq(R.all(even, [2, 4, 6, 8, 9, 10]), False)

    def it_returns_true_for_an_empty_list(T):
        eq(R.all(T, []), True)

    def it_works_with_more_complex_objects():
        xs = [{"x": 'abc'}, {"x": 'ade'}, {"x": 'fghiajk'}]
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
