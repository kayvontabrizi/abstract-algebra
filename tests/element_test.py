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
        assert "element is not in" in str(error.value)

    # test Element methods
    def test_element_methods(self):
        # construct two dihedral groups and grab a few elements
        D3, D5 = Dn(3), Dn(5)
        r1s_D3, r2_D3 = Element('r1s', D3), Element('r2', D3)
        r1s_D5, r4_D5 = Element('r1s', D5), Element('r4', D5)

        # check representation
        assert str(r1s_D3) == 'r1s'
        assert str(r4_D5)  ==  'r4'

        # check equality and hashes
        assert r1s_D3 == r1s_D5
        assert hash(r1s_D3) == hash(r1s_D5)

        # check exponentiation
        assert r1s_D3**-1 == r1s_D3
        assert r1s_D3** 0 == D3.e
        assert r1s_D3** 1 == r1s_D3
        assert r1s_D3** 2 == D3.e
        assert r1s_D3** 3 == r1s_D3
        assert  r4_D5**-2 == r2_D3

        # check multiplication
        assert r2_D3*r1s_D3 == Element('r0s', D3)
        assert r2_D3*r1s_D5 == Element('r0s', D3)
        assert r1s_D5*r2_D3 == Element('r4s', D5)
        assert  r2_D3*r4_D5 == Element( 'r1', D3)

        # construct two Abelian groups and grab a few elements
        Z3, Z5 = Zn(3), Zn(5)
        Z3_1, Z3_2 = Element(1, Z3), Element(2, Z3)
        Z5_1, Z5_4 = Element(1, Z5), Element(4, Z5)

        # check Abelian multiplication (exponentiation)
        assert -Z3_1   == Z3_2
        assert  Z3_1*0 == Z3.e
        assert  Z3_1*1 == Z3_1
        assert  Z3_1*2 == Z3_2
        assert Z3_1*-2 == Z3_1
        assert -2*Z3_1 == Z3_1

        # check Abelian addition (multiplication)
        assert Z3_1+Z3_2 == Z3.e
        assert Z3_1-Z3_1 == Z3.e
        assert Z5_1+Z3_2 == Element(3, Z5)
        assert Z3_2+Z5_1 == Z3.e
        assert Z3_1+Z5_4 == Z3.e

        # check for TypeErrors upon Element multiplication
        with pytest.raises(TypeError):
            Z3_1 * 'test'

        # check for ValueErrors upon non-Abelian Element multiplication
        with pytest.raises(ValueError) as error:
            r2_D3 * 5
        assert "self-multiply Elements of non-Abelian" in str(error.value)
        with pytest.raises(ValueError) as error:
            5 * r2_D3
        assert "self-multiply Elements of non-Abelian" in str(error.value)
        with pytest.raises(ValueError) as error:
            r1s_D3 + r2_D3
        assert "Elements must belong to Abelian" in str(error.value)
        with pytest.raises(ValueError) as error:
            r1s_D3 - r2_D3
        assert "Elements must belong to Abelian" in str(error.value)
        with pytest.raises(ValueError) as error:
            -r1s_D5
        assert "Element must belong to an Abelian" in str(error.value)
