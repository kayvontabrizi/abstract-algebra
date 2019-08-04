# imports
import pytest

# local imports
from algebra import *

# create a test class
class TestClass(object):
    # test trivial Element functionality
    def test_element_basics(self):
        # construct the multiplicative group of integers modulo 5
        g = Set(range(1, 5))
        func = lambda x: (x[0] * x[1]) % 5
        f = Function(g**2, g, func)
        G = Group(g, f)

        # make an Element
        a = Element(3, G)

        # manually check the underlying Element and Group
        assert a.elem == 3
        assert a.group == G

        # check for TypeErrors upon Element creation
        with pytest.raises(TypeError):
            Element(3, (g, f))

        # check for ValueErrors upon Element creation
        with pytest.raises(ValueError) as error:
            Element(8, G)
        assert "elements is not in" in str(error.value)

    # test Element methods
    def test_element_methods(self):
        pass
