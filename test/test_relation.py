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


def describe_identical():
    a = []
    b = a

    def it_has_Object_is_semantics():
        eq(R.identical(100, 100), True)
        eq(R.identical(100, '100'), False)
        eq(R.identical('string', 'string'), True)
        eq(R.identical([], []), False)
        eq(R.identical(a, b), True)
        eq(R.identical(None, None), True)
        # eq(R.identical(null, undefined), False)

        # eq(R.identical(-0, 0), False)
        # eq(R.identical(0, -0), False)
        eq(R.identical(float('nan'), float('nan')), True)

        eq(R.identical(float('nan'), 42), False)
        eq(R.identical(42, float('nan')), False)

        # eq(R.identical(0, int(0)), False)
        # eq(R.identical(int(0), 0), False)
        # eq(R.identical(int(0), int(0)), False)

    def it_is_curried():
        is_a = R.identical(a)

        eq(is_a([]), False)
