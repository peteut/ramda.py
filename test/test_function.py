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
