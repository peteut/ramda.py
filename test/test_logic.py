import ramda as R
from ramda.shared import eq
import pytest


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
