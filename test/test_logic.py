import ramda as R
from ramda.shared import eq


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
