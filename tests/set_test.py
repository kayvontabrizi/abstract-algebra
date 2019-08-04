# imports
import pytest

# local imports
from algebra import *

# create a test class
class TestClass(object):
    # test trivial set functionality
    def test_basics(self):
        # compare automatic and manual set constructions
        assert Set(range(3)) == Set({0, 1, 2, 1})
        assert Set(range(3)) == Set([0, 1, 2, 1])
        assert Set(range(2)) == Set(frozenset({0, 1, 0}))

        # check trivial equality
        s = Set(range(10))
        assert s == Set(range(10))

    # test set multiplication/exponentiation functionality
    def test_products(self):
        # try various sizes
        for n in range(10):
            # check multiplication
            s = Set(range(n))
            s * s == Set((x, y) for x in range(n) for y in range(n))

            # check exponentiation
            s == s ** 1
            s * s == s ** 2

        # check exponentiation error
        with pytest.raises(ValueError) as error:
            # cause error
            print(s ** 0)

        # verify correct error message was raised
        assert "must be at least" in str(error.value)

        # check Cartesian product with empty set
        Set(range(10)) * Set([]) == Set([])
