import pytest
import ramda as R
from ramda.shared import eq


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
