import pytest
import ramda as R
from ramda.shared import eq


@pytest.fixture
def T():
    return lambda *_: True


@pytest.fixture
def not_equal():
    return lambda a, b: id(a) is not id(b)


def describe_pick_by():
    @pytest.fixture
    def obj():
        return {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6}

    def it_creates_a_copy_of_the_object(obj, not_equal):
        eq(not_equal(R.pick_by(R.always(True), obj), obj), True)

    def it_when_returning_truthy_keeps_the_key(T, obj):
        eq(R.pick_by(T, obj), obj)
        eq(R.pick_by(R.always({}), obj), obj)
        eq(R.pick_by(R.always(1), obj), obj)

    def it_is_called_with_val_key_obj(obj):
        eq(R.pick_by(lambda val, key, _: key == "d" and val == 4, obj), {"d": 4})

    def it_is_curried(T, obj):
        copier = R.pick_by(T)
        eq(copier(obj), obj)


def describe_path():
    @pytest.fixture
    def deep_object():
        return {"a": {"b": {"c": "c"}}}

    def it_takes_a_path_and_an_obj_and_returns_the_value_at_the_path_or_none():
        obj = {
            "a": {
                "b": {
                    "c": 100,
                    "d": 200
                },
                "e": {
                    "f": [100, 101, 102],
                    "g": "G"
                },
                "h": "H"
            },
            "i": "I",
            "j": ["J"]
        }
        eq(R.path(["a", "b", "c"], obj), 100)
        eq(R.path([], obj), obj)
        eq(R.path(["a", "e", "f", 1], obj), 101)
        eq(R.path(["j", 0], obj), "J")
        eq(R.path(["j", 1], obj), None)
