# imports
import pytest

# local imports
from algebra import *

# create a test class
class TestClass(object):
    # test trivial function functionality
    def test_basics(self):
        # create a function
        s = Set([0, 1, 2, 3])
        t = Set([1, 2, 3, 4])
        f = Function(s, t, lambda x: x + 1)

        # check trivial equality
        assert f == f

        # generate its image via printing
        print(f)

        # manually check its output
        for x in range(4):
            assert f(x) == x + 1

        # check for TypeErrors upon Function creation
        with pytest.raises(TypeError):
            Function([0, 1, 2, 3], t, lambda x: x + 1)
        with pytest.raises(TypeError):
            Function(s, [1, 2, 3, 4], lambda x: x + 1)

        # check for codomain ValueError
        with pytest.raises(ValueError) as error:
            Function(s, t, lambda x: x + 2)
        assert "value outside of codomain" in str(error.value)

    # test identity function
    def test_identity(self):
        # construct identity function
        s = Set(["las", 3, "ksjfdlka"])
        ID = identity_func(s)

        # generate its image via printing
        print(ID)

        # manually check its output
        for item in s:
            assert ID(item) == item

    # test dict function
    def test_dict(self):
        # construct dict function
        dictionary = {'a': 1, 'b': 2, 'c': 3}
        ID = dict_func(dictionary)

        # generate its image via printing
        print(ID)

        # manually check its output
        for key, value in dictionary.items():
            assert ID(key) == value

    # test calling & unpacking funcationality
    def test_call(self):
        # prepare function
        domain = Set([1,2])*Set([2,3])
        codomain = Set([2, 3, 4, 6])
        f = Function(domain, codomain, lambda x: x[0]*x[1])

        # generate its image via printing
        print(f)

        # check for outside-of-domain ValueError
        with pytest.raises(ValueError) as error:
            print(f(1))
        assert "called on elements of the domain" in str(error.value)

        # manually check argument packing
        assert f(1, 3) == 3

        # prepare 1-ple function
        domain = Set([(1, ), (2, )])
        codomain = Set([3, 5])
        g = Function(domain, codomain, lambda x: x[0]*2 + 1)

        # generate its image via printing
        print(g)

        # check for outside-of-domain ValueError
        with pytest.raises(ValueError) as error:
            print(g(1))
        assert "called on elements of the domain" in str(error.value)

    # test Function methods
    def test_methods(self):
        # construct surjectivity/injectivity/bijectivity test set
        s = Set([0, 1, 2, 3])
        t = Set([1, 2, 3, 4])
        u = Set([0, 1, 2, 3, 4, 5])
        f = Function(s, t, lambda x: x + 1)
        g = Function(t, u, lambda x: x + 1)
        h = g.compose(f)
        i = Function(Set([-1, 0, 1]), Set([0, 1]), lambda x: abs(x))

        # verify that f is bijective
        assert f.is_surjective()
        assert f.is_injective()
        assert f.is_bijective()

        # manually check its image, generate via printing
        assert f.image() == t
        print(f)

        # verify that g is only injective
        assert not g.is_surjective()
        assert g.is_injective()
        assert not g.is_bijective()

        # manually check its image, generate via printing
        assert g.image() == Set([2, 3, 4, 5])
        print(g)

        # verify that h = g(f) is only injective
        assert not h.is_surjective()
        assert h.is_injective()
        assert not h.is_bijective()

        # manually check its image, generate via printing
        assert h.image() == Set([2, 3, 4, 5])
        print(h)

        # verify that i is only surjective
        assert i.is_surjective()
        assert not i.is_injective()
        assert not i.is_bijective()

        # manually check its image, generate via printing
        assert i.image() == Set([0, 1])
        print(i)

        # check for domain-mismatch ValueErrors upon composition
        with pytest.raises(ValueError) as error:
            i.compose(f)
        assert "must match the domain" in str(error.value)
        with pytest.raises(ValueError) as error:
            f.compose(i)
        assert "must match the domain" in str(error.value)

        # check hash generation
        assert hash(dict_func({'a': 1})) != hash(dict_func({1: 'a'}))
