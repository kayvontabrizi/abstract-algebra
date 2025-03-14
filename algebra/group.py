"""Group Implementation"""

# local imports
from . import Set, Function, Element
from . import bin_op, utils

# imports
import itertools        

# define Group class
class Group(object):
    """Implementation of a finite group"""

    # initialization
    def __init__(self, elements, bin_op, display_order=None, skip_checks=False):
        """Initialize a group and check group axioms."""

        # initialize super
        super().__init__()

        # check that elements is a Set
        if not isinstance(elements, Set):
            raise TypeError("The elements must be a Set!")

        # check that bin_op is a Function
        if not isinstance(bin_op, Function):
            raise TypeError("The bin_op must be a Function!")

        # We have to be careful about the storage order here. Element.__init__ requires
        # that group.elements be defined. Since we're passing self to Element's __init__,
        # it's important to store self.elements first. We can then take advatange
        # Element's syntactic simplicity in checking our group axioms.
        #
        # record the binary operation, element representations, and set of Elements
        #
        self.bin_op = bin_op
        self.elements = elements
        self.set = Set(Element(elem, self) for elem in elements)

        # verify bin_op domain includes the element pairs
        if not elements**2 <= bin_op.domain:
            raise ValueError("The binary operation must have all element pairs in its domain.")

        # verify group closure
        if not Set(bin_op(e) for e in elements**2) <= elements:
            raise ValueError("The elements must be closed under the binary operation.")

        # verify that a single identity element is present and set it as the group identity
        identities = [e for e in self.set if all(e * a == a and a * e == a for a in self.set)]
        if len(identities) == 0:
            raise ValueError("The group must have an identity element.")
        elif len(identities) > 1:
            raise RuntimeError("REPORT THIS ERROR: There are multiple identity elements.")
        self.e = identities[0]

        # if requested, skip associativity check, which can be expensive for large groups
        if not skip_checks:
            # verify associativity for all element triplets
            if not all(a * (b * c) == (a * b) * c for a, b, c in utils.combos(self.set, 3)):
                raise ValueError("The binary operation is not associative.")

        # verify that inverses exist for each element
        inverses = Set([a for a in self.set if any(a * b == self.e for b in self.set)])
        if len(inverses) != len(elements):
            raise ValueError("Some elements are missing inverses!")

        # determine if the Group is Abelian and record
        self.abelian = all(a * b == b * a for a, b in utils.combos(self.set, 2))

        # set element display_order, if display_order provided
        self.display_order = None
        if display_order is not None:
            # verify that the sets of ordered and unordered elements are identical
            if Set(display_order) != elements:
                raise ValueError("The sets of ordered and unordered elements do not match.")

            # determine display_order indicies
            self.display_order = [list(self.set).index(Element(a, self)) for a in display_order]

    # iterate through Group elements
    def __iter__(self):
        """
        Iterates over elements in the Group, starting with the identity.

        The iteration order can be ovewritten with self.display_order.
        """

        # check if an order is available
        if self.display_order is not None:
            # iterate and yield according to order
            for i in self.display_order:
                yield list(self.set)[i]
        # otherwise
        else:
            # return the identity element
            yield self.e

            # return non-identity elements
            for a in self.set:
                if a != self.e: yield a

    # check whether an element is in the Group
    def __contains__(self, item):
        """Checks whether or not an element is in the Group."""
        return item in self.set

    # generte a hash from the elements and binary operation
    def __hash__(self):
        """Returns a unique hash of the Group."""
        return hash(self.bin_op) ^ hash(self.set)

    # check equality of two Groups
    def __eq__(self, other_group):
        """
        Returns true if input Groups share an id, or if they share elements
        and a binary operation.
        """

        # return false if other_group is not a Group
        if not isinstance(other_group, Group):
            return False

        # return true if Groups are equivalent
        return id(self) == id(other_group) or ( \
               self.bin_op == other_group.bin_op and \
               self.set == other_group.set)

    # check inequality
    def __ne__(self, other):
        return not self == other

    # return the number of Group elements
    def __len__(self):
        return len(self.set)

    # # return a string representation of the Group
    # def __repr__(self):
    #     """Returns a string representation of the Group's elements and function."""

    #     # construct return string and return
    #     return str(self.set)+'\n'+str(self.bin_op)

    # return a pretty string representation of the Group
    def __str__(self):
        """Returns the Cayley table, if possible."""

        # initialize a return string
        ret_str = ""

        # identify longest element string
        max_len = max(len(str(elem)) for elem in self)

        # symbolize elements, if necessary
        if max_len > 3:
            # enumerate available symbols, beginning with 'e' for the identity
            symbols = "eabcdfghijklmnopqrstuvwxyz"

            # reset max_len
            max_len = 1

            # return warning if Group is too large to print
            if len(self) > len(symbols):
                return "This Group is too large to represent as a Cayley table!"

            # map symbols to elements
            to_symbol = dict(zip(self, symbols[:len(self)]))

            # add symbol mapping to return string
            ret_str += '\n'.join(f"{s}: {e}" for e, s in to_symbol.items())+"\n\n"

        # otherwise, use padded strings as symbols
        else: to_symbol = {elem: str(elem).ljust(max_len) for elem in self}

        # add a table to the return string
        hori, vert, plus = '─', '│', '•'
        col_sep, int_sep = f' {vert} ', f' {plus} '
        row_sep = '\n'+int_sep.join([hori*max_len for a in self])+'\n'
        ret_str += row_sep.join([
            col_sep.join([
                to_symbol[a * b] for b in self
            ]) for a in self
        ])

        # return return string
        return ret_str

    # return whether the Group is Abelian
    def is_abelian(self):
        """Checks if the Group is Abelian."""
        return self.abelian

    # return a dictionary of Group Elements
    def get_elements(self):
        """Returns a dictionary of the Group's Elements."""

        # construct and return the dictionary
        return {elem: Element(elem, self) for elem in self.elements}

    # return the inverse of an element
    def invert(self, element):
        """Returns the inverse of the given element."""

        # check that the element if in the group
        if not element in self.set:
            raise ValueError("The element is not in the Group.")

        # search for the element's inverse and return if found
        for a in self:
            if element * a == self.e:
                return a

        # throw an error if no inverse is found
        raise RuntimeError("Something's wrong--this element has no inverse!")

    # returns whether the Group is a subgroup of another Group
    def __lt__(self, other_group):
        """Evaluates whether this Group is a subgroup of another Group."""

        # check that other_group is a Group
        if not isinstance(other_group, Group):
            raise TypeError("The other group must be a Group!")

        # check that self's set is a subset of other_group's, return early if not
        is_subset = self.set < other_group.set

        # return early if self's set is not a is_subset
        if not is_subset: return False

        # verify the binary operations are equivalent by brute force
        same_bin_op = all(~(a*b) == other_group.bin_op(~a, ~b) for a, b in self.set**2)

        # return true if both conditions are met (is_subset must be true by now)
        return same_bin_op

    # generate a subgroup from the specified elements
    def generate(self, elements):
        """
        Returns the subgroup generated by the specified elements.

        This function will attempt to convert all input elements to
        Elements of this group.
        """

        # complain if elements is empty
        if not hasattr(elements, '__len__') or len(elements) == 0:
            print(elements)
            raise ValueError("Elements must be a non-empty iterable.")

        # attempt to convert all elements to Elements of this Group
        elements = Set(Element(
            e if not isinstance(e, Element) else ~e, self
        ) for e in elements)

        # compile Element products into a Set until the Set stops changing
        old_set, new_set = elements, Set()
        while old_set != new_set:
            old_set = old_set | new_set
            new_set = old_set | Set(a*b for a, b in utils.combos(old_set, 2))

        # return subgroup with Set of compiled Elements
        return Group(Set(~elem for elem in new_set), self.bin_op)

    # check whether this group is cyclic
    def is_cyclic(self):
        """Checks whether or not this Group is cyclic."""
        return any(e.order() == len(self) for e in self)

    # return a Set of this group's subgroups
    def subgroups(self):
        """Returns a Set of this Group's subgroups."""

        # compile subgroups into a Set until the Set stops changing
        old_set, new_set = Set([self.generate([self.e])]), Set()
        while old_set != new_set:
            old_set = old_set | new_set
            new_set = old_set | Set(
                self.generate(grp.set|{elem}) for grp in old_set
                for elem in self if elem not in grp
            )

        # return the Set of compiled subgroups
        return new_set

    # # TODO
    # def generators(self):
    #     """
    #     Returns a list of Elements that generate self, with length
    #     at most log_2(len(self)) + 1
    #     """

    #     result = [self.e.elem]
    #     H = self.generate(result)

    #     while len(H) < len(self):
    #         result.append((self.set - H.set).pick())
    #         H = self.generate(result)

    #     # The identity is always a redundant generator in nontrivial Groups
    #     if len(self) != 1:
    #         result = result[1:]

    #     return [Element(g, self) for g in result]

    # # TODO
    # def find_isomorphism(self, other):
    #     """
    #     Returns an isomorphic GroupHomomorphism between self and other,
    #     or None if self and other are not isomorphic

    #     Uses Tarjan's algorithm, running in O(n^(log n + O(1))) time, but
    #     runs a lot faster than that if the group has a small generating set.
    #     """
    #     if not isinstance(other, Group):
    #         raise TypeError("other must be a Group")

    #     if len(self) != len(other) or self.is_abelian() != other.is_abelian():
    #         return None

    #     # Try to match the generators of self with some subset of other
    #     A = self.generators()
    #     for B in itertools.permutations(other, len(A)):

    #         func = dict(itertools.izip(A, B)) # the mapping
    #         counterexample = False
    #         while not counterexample:

    #             # Loop through the mapped elements so far, trying to extend the
    #             # mapping or else find a counterexample
    #             noobs = {}
    #             for g, h in itertools.product(func, func):
    #                 if g * h in func:
    #                     if func[g] * func[h] != func[g * h]:
    #                         counterexample = True
    #                         break
    #                 else: 
    #                     noobs[g * h] = func[g] * func[h]

    #             # If we've mapped all the elements of self, then it's a
    #             # homomorphism provided we haven't seen any counterexamples.
    #             if len(func) == len(self): 
    #                 break

    #             # Make sure there aren't any collisions before updating
    #             imagelen = len(set(noobs.values()) | set(func.values()))
    #             if imagelen != len(noobs) + len(func):
    #                 counterexample = True
    #             func.update(noobs)

    #         if not counterexample:
    #             return GroupHomomorphism(self, other, lambda x: func[x])

    #     return None

    # # TODO
    # def is_isomorphic(self, other):
    #     """Checks if self and other are isomorphic"""
    #     return bool(self.find_isomorphism(other))

    # # TODO
    # def __div__(self, other):
    #     """ Returns the quotient Group self / other """
    #     if not other.is_normal_subgroup(self):
    #         raise ValueError("other must be a normal subgroup of self")
    #     G = Set(Set(self.bin_op((g, h)) for h in other.set) for g in self.set)

    #     def multiply_cosets(x):
    #         h = x[0].pick()
    #         return Set(self.bin_op((h, g)) for g in x[1])

    #     return Group(G, Function(G * G, G, multiply_cosets))

    # # TODO
    # def __mul__(self, other):
    #     """Returns the cartesian product of the two groups"""
    #     if not isinstance(other, Group):
    #         raise TypeError("other must be a group")
    #     bin_op = Function((self.set * other.set) * (self.set * other.set), \
    #                          (self.set * other.set), \
    #                          lambda x: (self.bin_op((x[0][0], x[1][0])), \
    #                                     other.bin_op((x[0][1], x[1][1]))))

    #     return Group(self.set * other.set, bin_op)

    # # TODO
    # def is_normal_subgroup(self, other):
    #     """Evaluates whether this Group is a normal subgroup of another Group."""
    #     return self <= other and \
    #            all(Set(g * h for h in self) == Set(h * g for h in self) \
    #                for g in other)

# shorthand to construct a group from a set and a two-argument function
def group(input_set, func):
    # return a group whose elements are input_set and whose operation is func
    return Group(input_set, bin_op(input_set, func))

# construct the additive group of integers modulo n
def Zn(n):
    """
    Returns the additive group of integers modulo n.

    This is the archetype of a cyclic group of order n.
    """

    # construct elements and binary operation, then return a Group
    elems = Set(range(n))
    bin_op = Function(elems**2, elems, lambda x: (x[0] + x[1]) % n)
    return Group(elems, bin_op)

# construct the multiplicative group of integers modulo n
def ZnX(n):
    """
    Returns the multiplicative group of integers modulo n.

    This group is only well-defined for prime values of n > 1.
    """

    # complain if n is not a prime integer greater than 1
    if n < 2 or not utils.is_prime(n):
        raise ValueError("The group is only well-defined for prime values of n > 1.")

    # construct elements and binary operation, then return a Group
    elems = Set(range(1, n))
    bin_op = Function(elems**2, elems, lambda x: x[0] * x[1] % n)
    return Group(elems, bin_op)

# construct the group of n integer permutations
def Sn(n):
    """
    Returns the group of n integer pertmutations.

    This is the archetype of a symmetric group of order n.
    """

    # if n > 5, warn about construction speeds
    if n > 5:
        print(
"""
Warning: Constructing S_n for n > 5 may be extremely slow,
as it requires repeated pairwise operations on n! elements.
"""
        )

    # if n > 7, refuse to construct the Group
    if n > 7:
        from math import factorial as f
        raise ValueError(
            f"The estimated wait time for S_{n} is {round(8*(f(n)/f(8))**2)} hours."
        )

    # if n > 10, represent elements as tuples
    if n > 10:
        # construct elements and binary operation, then return a Group
        ordered_elems = list(itertools.permutations(range(n)))
        elems = Set(ordered_elems)
        bin_op = Function(elems**2, elems, lambda x: tuple(x[0][i] for i in x[1]))
        return Group(elems, bin_op, ordered_elems, skip_checks=True)
    # otherwise, represent elements as strings
    else:
        # construct elements and binary operation, then return a Group
        ordered_elems = [''.join(map(str, perm)) for perm in itertools.permutations(range(n))]
        elems = Set(ordered_elems)
        bin_op = Function(elems**2, elems, lambda x: ''.join(str(x[0][int(i)]) for i in x[1]))
        return Group(elems, bin_op, ordered_elems, skip_checks=True)

# construct the dihedral group of order 2n
def Dn(n):
    """
    Returns the dihedral group of order 2n.
    
    Note, as a matter of convention, the group multiplication treats the
    element on the right as the first operation. This is consistent with
    "r2s" referring to a flip followed by two rotations. Thus, one should
    expect that in D5, for example, r1 * r2s = r3s, and r1s * r2 = r4s.
    """

    # construct elements
    ordered_elems = [elem%r for elem in ("r%s", "r%ss") for r in range(n)]
    elems = Set(ordered_elems)

    # define the binary operation for rotations and flips
    def multiply_rots_and_flips(x):
        # identify the operation type for each element
        s1, s2 = map(lambda y: int(y[-1] == 's'), x)

        # identify the rotational magnitude
        r1, r2 = map(lambda y: int(y[1]), x)

        # if the first operation is a flip
        if s2:
            # if the second operation is a flip
            if s1:
                # both rotations and flips cancel
                return f"r{(r1 - r2) % n}"
            # otherwise
            else:
                # the rotations sum
                return f"r{(r1 + r2) % n}s"
        # otherwise
        else:
            # if the second operation is a flip
            if s1:
                # the rotations cancel
                return f"r{(r1 - r2) % n}s"
            # otherwise
            else:
                # the rotations sum, but flips cancel
                return f"r{(r1 + r2) % n}"

    # return a group
    return Group(elems, Function(elems**2, elems, multiply_rots_and_flips), ordered_elems)
