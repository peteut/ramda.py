import collections
import ramda as R
from ramda.shared import eq
from .common import get_arity
import pytest


@pytest.fixture
def odd():
    return lambda n: n % 2 != 0


@pytest.fixture
def gt20():
    return lambda n: n > 20


@pytest.fixture
def lt5():
    return lambda n: n < 5


@pytest.fixture
def plus_eq():
    return lambda w, x, y, z: w + x == y + z


def all_pass():
    def it_reports_wheter_all_preds_are_satified(odd, lt20, gt5):
        ok = R.all_pass([odd, lt20, gt5])
        eq(ok(7), True)
        eq(ok(9), True)
        eq(ok(10), False)
        eq(ok(3), False)
        eq(ok(21), False)

    def it_returns_true_on_empty_predicate_list():
        eq(R.all_pass([])(3), True)

    def it_returns_a_curried_function_whose_arity_matches(odd, gt5, plus_eq):
        eq(get_arity(R.all_pass([odd, gt5, plus_eq])), 4)
        eq(R.all_pass([odd, gt5, plus_eq])(9, 9, 9, 9), True)
        eq(R.all_pass([odd, gt5, plus_eq])(9)(9)(9)(9), True)


def any_pass():
    def it_report_wheter_any_preds_are_satisfied(odd, gt20, lt5):
        ok = R.any_pass([odd, gt20, lt5])
        eq(ok(7), True)
        eq(ok(9), True)
        eq(ok(10), False)
        eq(ok(18), False)
        eq(ok(3), True)
        eq(ok(22), True)

    def it_returns_false_for_an_empty_pred_list():
        eq(R.any_pass([])(3), False)

    def it_returns_a_curried_function_whose_arity_matches(odd, lt5, plus_eq):
        eq(get_arity(R.any_pass([odd, lt5, plus_eq])), 4)
        eq(R.any_pass([odd, lt5, plus_eq])(6, 7, 8, 9), False)
        eq(R.any_pass([odd, lt5, plus_eq])(6)(7)(8)(9), False)


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


def describe_cond():
    def it_returns_a_function():
        eq(isinstance(R.cond([]), collections.Callable), True)

    def it_returns_a_conditional_function():
        fn = R.cond([
            [R.equals(0), R.always("water freezes at 0°C")],
            [R.equals(100), R.always("water boils at 100°C")],
            [lambda _: True,
             lambda temp: "nothing special happens at {}'°C".format(temp)]
        ])
        eq(fn(0), "water freezes at 0°C")
        eq(fn(50), "nothing special happens at 50°C")
        eq(fn(100), "water boils at 100°C")

    def it_returns_a_function_which_returns_none_if_none_of_the_preds_matches():
        fn = R.cond([
            [R.equals("foo"), R.always(1)],
            [R.equals("bar"), R.always(2)]
        ])
        eq(fn("quux"), None)

    def it_predicates_are_tested_order():
        fn = R.cond([
            [lambda _: True, R.always("foo")],
            [lambda _: True, R.always("bar")],
            [lambda _: True, R.always("baz")]
        ])
        eq(fn(), "foo")

    def it_forwards_all_args_to_preds_and_to_transformers():
        fn = R.cond([
            [lambda _, x: x == 42, lambda *args: len(args)]
        ])
        eq(fn(21, 42), 2)

    def it_retains_highest_predicate_arity():
        fn = R.cond([
            [R.n_ary(2, lambda *_: True), lambda _: True],
            [R.n_ary(3, lambda *_: True), lambda _: True],
            [R.n_ary(1, lambda *_: True), lambda _: True]
        ])
        eq(get_arity(fn), 3)


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


def describe_until():
    def it_applies_fn_until_pred_is_satisfied():
        eq(R.until(R.gt(R.__, 100), R.multiply(2), 1), 128)

    def it_ignores_fn_if_predicate_is_always_true():
        eq(R.until(lambda _: True, lambda _: True, False), False)


def describe_when():
    def it_calls_the_when_true_fn_if_pred_returns_a_truthy_value():
        eq(R.when(R.is_(int), R.add(1))(10), 11)

    def it_returns_the_arg_if_pred_returns_a_falsy_value():
        eq(R.when(R.is_(int), R.add(1))("hello"), "hello")

    def it_return_a_curried_function():
        if_is_number = R.when(R.is_(int))
        eq(if_is_number(R.add(1))(15), 16)
        eq(if_is_number(R.add(1))("hello"), "hello")
