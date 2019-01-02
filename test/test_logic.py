import ramda as R
from ramda.shared import eq
from .common import get_arity
import pytest


def if_else():
    @pytest.fixture
    def t():
        return lambda a: a + 1

    @pytest.fixture
    def identity():
        return lambda a: a

    @pytest.fixture
    def is_list():
        return lambda a: isinstance(a, list)

    def it_calls_the_truth_case_function_if_validator_returns_truthy(
            identity, t):
        def v(a):
            return isinstance(a, int)

        eq(R.if_else(v, t, identity), 11)

    def it_calls_the_false_case_function_if_validator_returns_falsy(
            identity, t):
        def v(a):
            return isinstance(a, int)

        eq(R.if_else(v, t, identity)("hello"), "hello")

    def it_calls_the_case_on_list_items(
            is_list, identity):
        l = [[1, 2, 3, 4, 5], 10, [0, 1], 15]
        list_to_len = R.map(R.if_else(is_list, len, identity))
        eq(list_to_len(l), [5, 10, 2, 15])

    def it_passes_the_argument_to_the_true_case_function(identity):
        def v(*_):
            return True

        def on_true(a, b):
            eq(a, 123)
            eq(b, "abc")

        R.if_else(v, on_true, identity)(123, "abc")

    def it_returns_a_function_whose_arity_equals_the_max_arity():
        def a0():
            return 0

        def a1(x):
            return x

        def a2(x, y):
            return x + y

        eq(get_arity(R.if_else(a0, a1, a2)), 2)
        eq(get_arity(R.if_else(a0, a2, a1)), 2)
        eq(get_arity(R.if_else(a1, a0, a2)), 2)
        eq(get_arity(R.if_else(a1, a2, a0)), 2)
        eq(get_arity(R.if_else(a2, a0, a1)), 2)
        eq(get_arity(R.if_else(a2, a1, a0)), 2)

    def it_returns_a_curried_function(t, identity):
        def v(a):
            return isinstance(a, int)

        is_number = R.if_else(v)
        eq(is_number(t, identity)(15), 16)
        eq(is_number(t, identity)("hello"), "hello")

        fn = R.if_else(R.gt, R.substract, R.add)
        eq(fn(2)(7), 9)
        eq(fn(2, 7), 9)
        eq(fn(7)(2), 5)
        eq(fn(7, 2), 5)


def describe_and_():
    @pytest.fixture
    def half_truth():
        return R.and_(True)

    def it_compares_two_values():
        eq(R.and_(True, True), True)
        eq(R.and_(True, False), False)
        eq(R.and_(False, True), False)
        eq(R.and_(False, False), False)

    def it_is_curried(half_truth):
        eq(half_truth(False), False)
        eq(half_truth(True), True)


def describe_or_():
    def it_compares_two_values():
        eq(R.or_(True, True), True)
        eq(R.or_(True, False), True)
        eq(R.or_(False, True), True)
        eq(R.or_(False, False), False)

    def it_is_curried():
        eq(R.or_(False)(False), False)
        eq(R.or_(False)(True), True)


def describe_not_():
    def it_reverses_argument():
        eq(R.not_(False), True)
        eq(R.not_(1), False)
        eq(R.not_(""), True)


def describe_is_empty():

    def it_returnns_false_for_none():
        eq(R.is_empty(None), False)

    def it_returns_true_for_empty_string():
        eq(R.is_empty(""), True)

    def it_returns_true_for_empty_list():
        eq(R.is_empty([]), True)
        eq(R.is_empty([[]]), False)

    def it_returns_true_for_empty_dict():
        eq(R.is_empty({}), True)
        eq(R.is_empty({"a": 1}), False)
