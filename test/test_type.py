import collections
import ramda as R
from ramda.shared import eq


def describe_is():
    def it_works_with_builtin_types():
        eq(R.is_(list, []), True)
        eq(R.is_(bool, False), True)
        eq(R.is_(collections.Callable, lambda _: _), True)
        eq(R.is_(int, int(0)), True)
        eq(R.is_(object, {}), True)
        eq(R.is_(str, ""), True)

    def it_is_curried():
        is_list = R.is_(list)
        eq(is_list([]), True)
        eq(is_list({}), False)


def describe_is_nil():
    def it_tests_a_value_for_none():
        eq(R.is_nil(None), True)
        eq(R.is_nil([]), False)
        eq(R.is_nil({}), False)
        eq(R.is_nil(0), False)
        eq(R.is_nil(""), False)


def describe_prop_is():
    def it_returns_true_if_the_obj_property_is_of_the_given_type():
        eq(R.prop_is(int, "value", {"value": 1}), True)

    def it_returns_false_otherwise():
        eq(R.prop_is(str, "value", {"value": 1}), False)
        eq(R.prop_is(str, "value", {}), False)
