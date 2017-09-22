import ramda as R
from ramda.shared import eq


def describe_clamp():
    def it_clamps_to_the_lower_bound():
        eq(R.clamp(1, 10, 0), 1)
        eq(R.clamp(3, 12, 1), 3)
        eq(R.clamp(-15, 3, -100), -15)

    def it_clamps_to_the_upper_bound():
        eq(R.clamp(1, 10, 20), 10)
        eq(R.clamp(3, 12, 23), 12)
        eq(R.clamp(-15, 3, 16), 3)

    def it_leaves_it_alone_when_within_the_bound():
        eq(R.clamp(1, 10, 4), 4)
        eq(R.clamp(3, 12, 6), 6)
        eq(R.clamp(-15, 3, 0), 0)

    def it_works_with_letters_as_well():
        eq(R.clamp("d", "n", "f"), "f")
        eq(R.clamp("d", "n", "a"), "d")
        eq(R.clamp("d", "n", "q"), "n")


def describe_equals():
    a = []
    b = a

    def it_tests_for_deep_equality_of_its_operands():
        eq(R.equals(100, 100), True)
        eq(R.equals(100, "100"), False)
        eq(R.equals([], []), True)
        eq(R.equals(a, b), True)

    def it_considers_equal_boolean_primitives_equal():
        eq(R.equals(True, True), True)
        eq(R.equals(False, False), True)
        eq(R.equals(True, False), False)
        eq(R.equals(False, True), False)

    def it_considers_equal_number_primitives_equal():
        eq(R.equals(0, 0), True)
        eq(R.equals(0, 1), False)
        eq(R.equals(1, 0), False)

    def it_considers_equal_string_primitives_equal():
        eq(R.equals("", ""), True)
        eq(R.equals("", "x"), False)
        eq(R.equals("x", ""), False)
        eq(R.equals("foo", "foo"), True)
        eq(R.equals("foo", "bar"), False)
        eq(R.equals("bar", "foo"), False)

    def it_handles_objects():
        eq(R.equals({}, {}), True)
        eq(R.equals({"a": 1, "b": 2}, {"a": 1, "b": 2}), True)
        eq(R.equals({"a": 2, "b": 3}, {"b": 3, "a": 2}), True)
        eq(R.equals({"a": 2, "b": 3}, {"a": 3, "b": 3}), False)
        eq(R.equals({"a": 2, "b": 3, "c": 1}, {"a": 2, "b": 3}), False)

    def it_handles_lists():
        list_a = [1, 2, 3]
        list_b = [1, 3, 2]
        eq(R.equals([], {}), False)
        eq(R.equals(list_a, list_b), False)

    def it_handles_recursive_data_structures():
        c = {}
        c["v"] = c
        d = {}
        d["v"] = d
        e = []
        e.append(e)
        f = []
        f.append(f)
        nest_a = {"a": [1, 2, {"c": 1}], "b": 1}
        nest_b = {"a": [1, 2, {"c": 1}], "b": 1}
        nest_c = {"a": [1, 2, {"c": 2}], "b": 1}
        eq(R.equals(c, d), True)
        eq(R.equals(e, f), True)
        eq(R.equals(nest_a, nest_b), True)
        eq(R.equals(nest_a, nest_c), False)

    def it_dispatches_to_equals_method_recursively():
        class Left:
            def __init__(self, x):
                self.value = x

            def equals(self, x):
                return isinstance(x, Left) and R.equals(x.value, self.value)

        class Right:
            def __init__(self, x):
                self.value = x

            def equals(self, x):
                return isinstance(x, Right) and R.equals(self.value, x.value)

        eq(R.equals(Left([42]), Left([42])), True)
        eq(R.equals(Left([42]), Left([43])), False)
        eq(R.equals(Left(42), {"value": 42}), False)
        eq(R.equals({"value": 42}, Left(42)), False)
        eq(R.equals(Left(42), Right(42)), False)
        eq(R.equals(Right(42), Left(42)), False)

        eq(R.equals([Left(42)], [Left(42)]), True)
        eq(R.equals([Left(42)], [Right(42)]), False)
        eq(R.equals([Right(42)], [Left(42)]), False)
        eq(R.equals([Right(42)], [Right(42)]), True)

    def it_is_commutative():
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def equals(self, point):
                return isinstance(point, Point) and self.x == point.x and self.y == point.y

        class ColorPoint(Point):
            def __init__(self, x, y, color):
                super().__init__(x, y)
                self.color = color

            def equals(self, point):
                return isinstance(point, ColorPoint) and super().equals(point) \
                    and self.color == point.color

        eq(R.equals(Point(2, 2), ColorPoint(2, 2, "red")), False)
        eq(R.equals(ColorPoint(2, 2, "red"), Point(2, 2)), False)

    def it_is_curried():
        is_a = R.equals(a)
        eq(is_a([]), True)


def describe_identical():
    a = []
    b = a

    def it_has_object_is_semantics():
        eq(R.identical(100, 100), True)
        eq(R.identical(100, "100"), False)
        eq(R.identical("string", "string"), True)
        eq(R.identical([], []), False)
        eq(R.identical(a, b), True)
        eq(R.identical(None, None), True)
        # eq(R.identical(null, undefined), False)

        # eq(R.identical(-0, 0), False)
        # eq(R.identical(0, -0), False)
        eq(R.identical(float("nan"), float("nan")), True)

        eq(R.identical(float("nan"), 42), False)
        eq(R.identical(42, float("nan")), False)

        # eq(R.identical(0, int(0)), False)
        # eq(R.identical(int(0), 0), False)
        # eq(R.identical(int(0), int(0)), False)

    def it_is_curried():
        is_a = R.identical(a)

        eq(is_a([]), False)
