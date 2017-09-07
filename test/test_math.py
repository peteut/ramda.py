import pytest
import ramda as R
from ramda.shared import eq


def describe_add():

    def adds_together_two_numbers():
        eq(R.add(3, 7), 10)

    def it_coerces_its_arguments_to_numbers():
        eq(R.add('1', '2'), 3)
        eq(R.add(1, '2'), 3)
        eq(R.add(True, False), 1)
        # eq(R.add(null, null), 0)
        eq(R.identical(R.add(None, None), float('nan')), True)
        # eq(R.add(new Date(1), new Date(2)), 3)

    def it_is_curried():
        incr = R.add(1)
        eq(incr(42), 43)


def describe_add_properties():

    @pytest.mark.randomize()
    def commutative(a: float, b: float):
        assert R.add(a, b) == R.add(b, a)

    @pytest.mark.randomize()
    def associative(a: float, b: float, c: float):
        assert R.add(a, R.add(b, c)) == pytest.approx(R.add(R.add(a, b), c))

    @pytest.mark.randomize()
    def identity(a: float):
        assert R.add(a, 0) == a and R.add(0, a) == a


def describe_dec():

    def it_decrements_its_argument():
        eq(R.dec(-1), -2)
        eq(R.dec(0), -1)
        eq(R.dec(1), 0)
        eq(R.dec(12.34), 11.34)
        eq(R.dec(float('-inf')), float('-inf'))
        eq(R.dec(float('inf')), float('inf'))


def describe_divide():

    def it_divides_two_numbers():
        eq(R.divide(28, 7), 4)

    def it_is_curried():
        into28 = R.divide(28)
        eq(into28(7), 4)

    def it_behaves_right_curried_when_passed_a_placeholder_for_its_first_argument():
        half = R.divide(R.__, 2)
        eq(half(40), 20)


def describe_inc():

    def it_increments_its_argument():
        eq(R.inc(-1), 0)
        eq(R.inc(0), 1)
        eq(R.inc(1), 2)
        eq(R.inc(12.34), 13.34)
        eq(R.inc(float('-inf')), float('-inf'))
        eq(R.inc(float('inf')), float('inf'))


def describe_math_mod():

    def it_requires_integer_arguments():
        assert R.math_mod('s', 3) == R.math_mod('s', 3) is None
        assert R.math_mod(3, 's') == R.math_mod(3, 's') is None

    def it_computes_the_true_modulo_function():
        eq(R.math_mod(-17, 5), 3)
        eq(R.identical(None, R.math_mod(17, -5)), True)
        eq(R.identical(None, R.math_mod(17, 0)), True)
        eq(R.identical(None, R.math_mod(17.2, 5)), True)
        eq(R.identical(None, R.math_mod(17, 5.5)), True)

    def it_is_curried():
        f = R.math_mod(29)
        eq(f(6), 5)

    def it_behaves_right_curried_when_passed_a_placeholder_for_its_first_argument():
        mod5 = R.math_mod(R.__, 5)
        eq(mod5(12), 2)
        eq(mod5(8), 3)


def describe_mean():

    def it_returns_mean_of_a_nonempty_list():
        eq(R.mean([2]), 2)
        eq(R.mean([2, 7]), 4.5)
        eq(R.mean([2, 7, 9]), 6)
        eq(R.mean([2, 7, 9, 10]), 7)

    def it_returns_None_for_an_empty_list():
        eq(R.identical(float('nan'), R.mean([])), True)


def describe_multiply():

    def it_multiplies_together_two_numbers():
        eq(R.multiply(6, 7), 42)

    def it_is_curried():
        dbl = R.multiply(2)
        eq(dbl(15), 30)


def describe_negate():

    def it_negates_its_argument():
        eq(R.negate(float('-inf')), float('inf'))
        eq(R.negate(-1), 1)
        eq(R.negate(-0), 0)
        eq(R.negate(0), -0)
        eq(R.negate(1), -1)
        eq(R.negate(float('inf')), float('-inf'))


def describe_product():

    def it_multiplies_together_the_array_of_numbers_supplied():
        eq(R.product([1, 2, 3, 4]), 24)


def describe_subtract():

    def it_subtracts_two_numbers():
        eq(R.subtract(22, 7), 15)

    def it_coerces_its_arguments_to_numbers():
        eq(R.subtract('1', '2'), -1)
        eq(R.subtract(1, '2'), -1)
        eq(R.subtract(True, False), 1)
        # eq(R.subtract(null, null), 0)
        eq(R.identical(R.subtract(None, None), float('nan')), True)
        # eq(R.subtract(new Date(1), new Date(2)), -1)

    def it_is_curried():
        nines_compl = R.subtract(9)
        eq(nines_compl(6), 3)

    def it_behaves_right_curried_when_passed_a_placeholder_for_its_first_argument():
        minus5 = R.subtract(R.__, 5)
        eq(minus5(17), 12)


def describe_sum():

    def it_adds_together_the_array_of_numbers_supplied():
        eq(R.sum([1, 2, 3, 4]), 10)

    def it_does_not_save_the_state_of_the_accumulator():
        eq(R.sum([1, 2, 3, 4]), 10)
        eq(R.sum([1]), 1)
        eq(R.sum([5, 5, 5, 5, 5]), 25)
