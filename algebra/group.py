"""Group Implementation"""

# local imports
from . import Set, Function, Element

# imports
import itertools        

# define Group class
class Group(object):
    """Implementation of a finite group"""

    # initialization
    def __init__(self, elements, bin_op, ordered=None):
        """Initialize a group and check group axioms."""

        # initialize super
        super().__init__()

        # check that elements is a Set
        if not isinstance(elements, Set):
            raise TypeError("The elements must be a Set!")

        # check that bin_op is a Function
        if not isinstance(bin_op, Function):
            raise TypeError("The bin_op must be a Function")

        # verify bin_op codomain is equal to the elements
        if bin_op.codomain != elements:
            raise ValueError("The binary operation must have the elements as its codomain.")

        # verify bin_op domain is equal to the element pairs
        if bin_op.domain != elements * elements:
            raise ValueError("The binary operation must have all element pairs as its domain.")

        # record the binary operation, element representations, and set of Elements
        #
        # We have to be careful about the storage order here. Since we're passing self to
        # to Element's __init__, it's important to store bin_op and elements first. We can
        # now take advatange Element's syntactic simplicity.
        #
        self.bin_op = bin_op
        self.elements = elements
        self.set = Set(Element(elem, self) for elem in elements)

        # verify associativity for all element triplets
        triplets = list(itertools.combinations(self.set, 3))
        if not all(a * (b * c) == (a * b) * c for a, b, c in triplets):
            raise ValueError("The binary operation is not associative.")

        # verify that a single identity element is present and set that identity element
        identities = [e for e in self.set if all(e * a == a for a in self.set)]
        if len(identities) != 1:
            raise ValueError("There must be one identity element.")
        self.e = identities[0]

        # verify that inverses exist for each element
        inverses = Set([a for a in self.set if any(a * b == self.e for b in self.set)])
        if len(inverses) != len(elements):
            raise ValueError("Some elements are missing inverses!")

        # determine if the Group is Abelian and record
        pairs = list(itertools.combinations(self.set, 2))
        self.abelian = all(a * b == b * a for a, b in pairs)

        # set element order, if ordered provided
        self.order = None
        if ordered is not None:
            # verify that ordered elements matches unordered elements
            if Set(ordered) != elements:
                raise ValueError("The ordered and unordered elements do not match.")

            # determine ordered indicies
            self.order = [list(self.set).index(Element(elem, self)) for elem in ordered]

    # iterate through Group elements
    def __iter__(self):
        """
        Iterates over elements in the Group, starting with the identity.

        The iteration order can be ovewritten with self.order.
        """

        # check if an order is available
        if self.order is not None:
            # iterate and yield according to order
            for i in self.order:
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
                to_symbol[self.bin_op(a, b)] for a in self
            ]) for b in self
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
        """Returns the inverse of the given elemenet."""

        # check that the element if in the group
        if not element in self.set:
            raise ValueError("The element is not in the Group.")

        # search for the element's inverse and return if found
        for a in self:
            if element * a == self.e:
                return a

        # throw an error if no inverse is found
        raise RuntimeError("Something's wrong--this element has no inverse!")

    # # TODO
    # # return whether the Group is a subgroup of another
    # def __le__(self, other_group):
    #     """Checks if this group is a subgroup of other_group."""

    #     # check that other_group is a Group
    #     if not isinstance(other_group, Group):
    #         raise TypeError("The other group must be a Group!")

    #     return self.set <= other_group.set and \
    #            all(self.bin_op((a, b)) == other_group.bin_op((a, b)) \
    #                for a in self.set for b in self.set)

    # # TODO
    # def is_normal_subgroup(self, other):
    #     """Checks if self is a normal subgroup of other"""
    #     return self <= other and \
    #            all(Set(g * h for h in self) == Set(h * g for h in self) \
    #                for g in other)

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
    # def generate(self, elems):
    #     """
    #     Returns the subgroup of self generated by Elements elems

    #     If any of the items aren't already Elements, we will try to convert
    #     them to Elements before continuing.
        
    #     elems must be iterable
    #     """

    #     elems = Set(g if isinstance(g, Element) else Element(g, self) \
    #                 for g in elems)

    #     if not elems <= self.set:
    #         raise ValueError("elems must be a subset of self.set")
    #     if len(elems) == 0:
    #         raise ValueError("elems must have at least one element")

    #     oldG = elems
    #     while True:
    #         newG = oldG | Set(a * b for a in oldG for b in oldG)
    #         if oldG == newG: break
    #         else: oldG = newG
    #     oldG = Set(g.elem for g in oldG)

    #     return Group(oldG, Function(oldG * oldG, oldG, self.bin_op.function))

    # # TODO
    # def is_cyclic(self):
    #     """Checks if self is a cyclic Group"""
    #     return any(g.order() == len(self) for g in self)

    # # TODO
    # def subgroups(self):
    #     """Returns the Set of self's subgroups"""

    #     old_sgs = Set([self.generate([self.e])])
    #     while True:
    #         new_sgs = old_sgs | Set(self.generate(list(sg.set) + [g]) \
    #                                  for sg in old_sgs for g in self \
    #                                  if g not in sg.set)
    #         if new_sgs == old_sgs: break
    #         else: old_sgs = new_sgs

    #     return old_sgs

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

# construct the group of n integer permutations
def Sn(n):
    """
    Returns the group of n integer pertmutations.

    This is the archetype of a symmetric group of order n.
    """

    # if n > 10, represent elements as tuples
    if n > 10:
        # construct elements and binary operation, then return a Group
        ordered_elems = list(itertools.permutations(range(n)))
        elems = Set(ordered_elems)
        bin_op = Function(elems**2, elems, lambda x: tuple(x[0][i] for i in x[1]))
        return Group(elems, bin_op, ordered_elems)
    # otherwise, represent elements as strings
    else:
        # construct elements and binary operation, then return a Group
        ordered_elems = [''.join(map(str, perm)) for perm in itertools.permutations(range(n))]
        elems = Set(ordered_elems)
        bin_op = Function(elems**2, elems, lambda x: ''.join(str(x[0][int(i)]) for i in x[1]))
        return Group(elems, bin_op, ordered_elems)

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
