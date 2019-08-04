# imports
import pytest
from math import factorial

# local imports
from algebra import *

# create a test class
class TestClass(object):
    # test trivial Group functionality
    def test_group_basics(self):
        # construct the multiplicative group of integers modulo 5
        g = Set(range(1, 5))
        func = lambda x: (x[0] * x[1]) % 5
        f = Function(g**2, g, func)
        G = Group(g, f)

        # check trivial equality
        assert G == G

        # generate Cayley table via printing
        print(G)

        # manually check its binary operation, elements, set, identity, and order
        assert G.bin_op == f
        assert G.elements == g
        assert G.set == Set(Element(a, G) for a in g)
        assert G.e == Element(1, G)
        assert G.order == None

        # check for TypeErrors upon Group creation
        with pytest.raises(TypeError):
            Group(range(5), f)
        with pytest.raises(TypeError):
            Group(g, func)

        # check for ValueErrors upon Group creation
        with pytest.raises(ValueError) as error:
            Group(g, Function(g**2, Set(range(6)), func))
        assert "elements as its codomain" in str(error.value)
        with pytest.raises(ValueError) as error:
            Group(Set(range(6)), Function(g**2, Set(range(6)), func))
        assert "element pairs as its domain" in str(error.value)

        # check for associativity ValueError
        with pytest.raises(ValueError) as error:
            Group(g, Function(g**2, g, lambda x: 1 + (x[0] * x[1]) % 4))
        assert "is not associative" in str(error.value)

        # check for multiple identities ValueError
        with pytest.raises(ValueError) as error:
            g_plus = Set(g|{6})
            Group(g_plus, Function(g_plus**2, g_plus, func))
        assert "must be one identity" in str(error.value)

        # check for inverse ValueError if 0 included in multiplicative group
        with pytest.raises(ValueError) as error:
            g_zero = Set(range(5))
            Group(g_zero, Function(g_zero**2, g_zero, func))
        assert "missing inverses" in str(error.value)

        # check for ordered/unordered mismatch ValueError
        with pytest.raises(ValueError) as error:
            Group(g, f, ordered=[1, 2])
        assert "ordered and unordered" in str(error.value)

    # test Group methods
    def test_group_methods(self):
        # construct the multiplicative group of integers modulo 5
        g = Set(range(1, 5))
        func = lambda x: (x[0] * x[1]) % 5
        f = Function(g**2, g, func)
        G = Group(g, f)
        h = Function(g**2, g, lambda y: 1 * (y[0] * y[1]) % 5)
        H = Group(Set([1, 2, 3, 4]), h)

        # check iteration
        assert list(G) == [Element(elem, G) for elem in g]

        # check inclusion
        assert Element(3, G) in G
        assert 'element' not in G

        # check equality and hashes
        assert G == H
        assert hash(G) == hash(H)

        # check Group length
        assert len(G) == len(g)

        # test string representation
        print(G)

        # check is_abelian method
        assert G.is_abelian()

        # check get_elements method
        assert G.get_elements() == {elem: Element(elem, G) for elem in g}

        # check element inversion
        assert G.invert(G.e) == G.e
        assert G.invert(Element(2, G)) == Element(3, G)

    # test Zn Group creation
    def test_Zn(self):
        # try various sizes
        for n in range(1, 10):
            # construct group
            Z = Zn(n)

            # check Group by printing
            print(Z)

            # check various group properties
            assert Z.e == Element(0, Z)
            assert len(Z) == n
            assert all(
                a * b == Element((a.elem + b.elem) % n, Z)
                for a in Z for b in Z
            )
            assert all(Z.invert(a) == Element((n - a.elem) % n, Z) for a in Z)
            assert Z.is_abelian()
            # assert Z <= Z
            # assert Z.is_normal_subgroup(Z)
            # assert len(Z/Z), 1
            # if n <= 5: assert len(Z * Z) == n * n
            # assert Z.generate(Z) == Z

    # test Sn Group creation
    def test_Sn(self):
        # try various sizes
        for n in range(1, 5):
            # construct group
            S = Sn(n)

            # check Group by printing
            print(S)

            # check various group properties
            assert S.e == Element(''.join(map(str, range(n))), S)
            assert len(S) == factorial(n)
            assert all(
                S.invert(a) == Element(
                    ''.join(dict(
                        (a.elem[int(j)], j) for j in a.elem
                    )[str(i)] for i in range(n)),
                S) for a in S
            )
            if n < 3: assert S.is_abelian()
            else: assert not S.is_abelian()
            # assert S <= S
            # assert S.is_normal_subgroup(S)
            # assert len(S/S), 1
            # if n < 4: assert len(S * S) == factorial(n)**2
            # assert S.generate(S) == S

    # test Dn Group creation
    def test_Dn(self):
        # try various sizes
        for n in range(1, 10):
            # construct group
            D = Dn(n)

            # check Group by printing
            print(D)

            # check various group properties
            assert D.e == Element('r0', D)
            assert len(D) == 2*n
            assert all(
                D.invert(a) == Element((
                    str(a) if 's' in str(a) else \
                    f'r{(n-int(str(a)[1:]))%n}'
                ), D) for a in D
            )
            if n < 3: assert D.is_abelian()
            else: assert not D.is_abelian()
            # assert D <= D
            # assert D.is_normal_subgroup(D)
            # assert len(D/D), 1
            # if n < 4: assert len(D * D) == factorial(n)**2
            # assert D.generate(D) == D

    # def test_subgroups(self):
    #     G = Zn(9)
    #     sgs = G.subgroups()
    #     self.assertEquals(len(sgs), 3)
    #     for H in sgs:
    #         if H.is_normal_subgroup(G):
    #             self.assertEquals(len(G / H) * len(H), len(G))

    #     G = Zn(2) * Zn(2)
    #     sgs = G.subgroups()
    #     self.assertEquals(len(sgs), 5)
    #     for H in sgs:
    #         if H.is_normal_subgroup(G):
    #             self.assertEquals(len(G / H) * len(H), len(G))

    #     G = Sn(3)
    #     sgs = G.subgroups()
    #     self.assertEquals(len(G.subgroups()), 6)
    #     for H in sgs:
    #         if H.is_normal_subgroup(G):
    #             self.assertEquals(len(G / H) * len(H), len(G))

    # def test_group_elem(self):
    #     V = Zn(2) * Zn(2)
    #     e, a, b, c = tuple(g for g in V)
    #     self.assertEquals(a + b + c, e)
    #     self.assertEquals(a + b, c)
    #     self.assertEquals(b + c, a)
    #     self.assertEquals(a + c, b)
    #     for g in V:
    #         self.assertTrue(g in V)
    #         self.assertEquals(g, g)
    #         self.assertEquals(e * g, g)
    #         self.assertEquals(g * e, g)
    #         self.assertEquals(e + g, g)
    #         self.assertEquals(g + e, g)
    #         self.assertEquals(g * g, e)
    #         self.assertEquals(g + g, e)
    #         self.assertEquals(g ** -1, g)
    #         self.assertEquals(-g, g)
    #         self.assertEquals(-g, g ** -1)
    #         self.assertEquals(g ** 209325, g)
    #         self.assertEquals(g ** -23234, e)
    #         for n in range(-10, 10):
    #             self.assertEquals(g * n, g ** n)
    #             self.assertEquals(n * g, g ** n)
    #             self.assertEquals(n * g, g * n)
    #     for g in [a, b, c]:
    #         self.assertTrue(e != g)

    #     G = Sn(3)
    #     for g in G:
    #         with self.assertRaises(TypeError):
    #             g + g
    #         with self.assertRaises(TypeError):
    #             g * 2
    #         with self.assertRaises(TypeError):
    #             2 * g
    #         with self.assertRaises(TypeError):
    #             -g
    #     for H in G.subgroups():
    #         for g in G:
    #             self.assertEquals(g ** 5, g * g * g * g * g)
    #             for h in H:
    #                 self.assertEquals(h ** 2, h * h)
    #                 self.assertEquals(h * g, GroupElem(h.elem, G) * g)
    #                 self.assertEquals(g * h, g * GroupElem(h.elem, G))

    # def test_generators(self):
    #     for G in [Zn(1), Zn(2), Zn(5), Zn(8), Sn(1), Sn(2), Sn(3), \
    #               Dn(1), Dn(2), Dn(3), Dn(4)]:
    #         self.assertEquals(G, G.generate(G.generators()))
    #         self.assertEquals(G, G.generate(g.elem for g in G.generators()))

    # def test_find_isomorphism(self):
    #     f = Dn(2).find_isomorphism(Zn(2) * Zn(2))
    #     self.assertTrue(f is not None)
    #     self.assertTrue(f.is_isomorphism())
    #     self.assertEquals(f.kernel(), Dn(2).generate([Dn(2).e]))
    #     self.assertEquals(f.image(), Zn(2) * Zn(2))

    #     self.assertFalse(Dn(12).is_isomorphic(Sn(4)))
    #     self.assertFalse(Sn(3).is_isomorphic(Zn(6)))
    #     self.assertFalse(Sn(3).is_isomorphic(Zn(4)))

    #     for G in [Zn(1), Zn(2), Zn(5), Sn(1), Sn(3), Dn(1), Dn(4)]:
    #         self.assertTrue(G.is_isomorphic(G))
    #         f = G.find_isomorphism(G)
    #         self.assertTrue(f is not None)
    #         self.assertTrue(f.is_isomorphism())
    #         self.assertEquals(f.kernel(), G.generate([G.e]))
    #         self.assertEquals(f.image(), G)

    #     self.assertTrue(Zn(1).is_isomorphic(Sn(1)))
    #     self.assertTrue(Zn(2).is_isomorphic(Sn(2)))
    #     self.assertTrue(Zn(2).is_isomorphic(Dn(1)))

    # # test identification of cyclic groups
    # def test_cyclic(self):
    #     # try various sized additive groups
    #     for n in range(1, 10):
    #         assert Zn(n).is_cyclic()

    #     # try various size symmetry groups
    #     assert Sn(1).is_cyclic()
    #     assert Sn(2).is_cyclic()
    #     assert Sn(3).is_cyclic()

    #     # try various size dihedral groups
    #     assert Dn(1).is_cyclic()
    #     assert Dn(2).is_cyclic()
    #     assert Dn(3).is_cyclic()
