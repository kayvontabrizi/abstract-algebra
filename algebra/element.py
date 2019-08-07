"""Element Implementation"""

# define Element class
class Element(object):
    """
    Implementation of a group element
    
    This is mainly syntactic sugar, so you can write
    things like g * h instead of group.bin_op(g, h).
    """

    # initialization
    def __init__(self, elem, group):
        """Initialize an element as part of a group."""

        # initialize super
        super().__init__()

        # delay group import to avoid circular import issues
        from .group import Group

        # check that group is a Group
        if not isinstance(group, Group):
            raise TypeError("The group must be a Group object!")

        # check that the element is in the group
        if not elem in group.elements:
            raise ValueError("The element is not in the group.")

        # record element and group
        self.elem = elem
        self.group = group

    # return string representation of element
    def __repr__(self):
        return str(self.elem)

    # check element equality
    def __eq__(self, other_elem):
        """
        Two Elements are equal if they represent the same element,
        regardless of the Groups they belong to.
        """

        # check that other element is an Element
        if not isinstance(other_elem, Element):
            raise TypeError("The other_elem must be an Element!")

        # return equality of the underlying elements
        return self.elem == other_elem.elem

    # check inequality
    def __ne__(self, other):
        return not self == other

    # generate a hash of the underlying element
    def __hash__(self):
        return hash(self.elem)

    # return the underlying element
    def __invert__(self):
        return self.elem

    # define element exponentiation
    def __pow__(self, exponent, modulo=None):
        """
        Returns the element raised to the exponent.
        
        The element exponentiation is implemented recursively as a
        combination of element products.

        `modulo` is included as an argument to comply with the API, but
        is otherwise ignored.
        """

        # check that the exponent is an integer
        if not isinstance(exponent, int):
            raise TypeError("The exponent must be an integer!")

        # if exponent is 0, return the group identity
        if exponent == 0:
            return self.group.e
        # if the exponent is negative, return the exponentiated inverse
        elif exponent < 0:
            return self.group.invert(self) ** -exponent
        # if the exponent is odd, decompose into even + 1
        elif exponent % 2 == 1:
            return self * (self ** (exponent - 1))
        # if the exponent is even, decompose into a product
        else:
            return (self * self) ** (exponent // 2)

    # define element left-multiplication
    def __mul__(self, elem):
        """
        If elem is a group element, returns self * elem.
        If elem is an int, and self is in an Abelian group, returns self**elem.

        This product assumes that both elements are in self.group. If this
        assumption fails, the equivalent product is attempted with elem.group.
        """

        # check if elem is an integer
        if isinstance(elem, int):
            # if the group is Abelian, return self-multiplication product
            if self.group.is_abelian():
                return self ** elem
            # otherwise, complain that the element is not from an Abelian group
            raise ValueError("Cannot self-multiply Elements of non-Abelian groups!")
        # otherwise, check that elem is an Element
        elif not isinstance(elem, Element):
            raise TypeError("The other elem must be a Element or an integer.")

        # attempt to return the element product
        try:
            return Element(self.group.bin_op(self.elem, elem.elem), self.group)
        # This can return a ValueError in Funcion.__call__ if self and elem
        # belong to different Groups. In this case, we'll try the equivalent product
        # with the other element's group, with a warning.
        except ValueError:
            print("WARNING: These elements come from different groups, "\
                  "the results may be unexpected.")
            return elem.__rmul__(self)

    # define element right-multiplication
    def __rmul__(self, elem):
        """
        If elem is a group element, returns elem * self.
        If elem is an int, and self is in an Abelian group, returns self**elem

        As an element product, this should only be triggered if a left multiply
        fails, in which case the product is re-attempted with what is now self.group.
        """

        # check if elem is an integer
        if isinstance(elem, int):
            # if the group is Abelian, return self-multiplication product
            if self.group.is_abelian():
                return self ** elem
            # otherwise, complain that the element is not from an Abelian group
            raise ValueError("Cannot self-multiply Elements of non-Abelian groups!")
        # otherwise, check that elem is an Element
        elif not isinstance(elem, Element):
            raise TypeError("The other elem must be a Element or an integer.")

        # return the element product with a warning
        return Element(self.group.bin_op(elem.elem, self.elem), self.group)

    # returns element product for Abelian groups
    def __add__(self, elem):
        """Returns self + elem for Abelian groups."""

        # return product if both elements belong to Abelian groups
        if self.group.is_abelian() and elem.group.is_abelian():
            return self * elem
        # otherwise, complain
        else:
            raise ValueError("Both Elements must belong to Abelian groups.")

    # returns element inverse for Abelian groups
    def __neg__(self):
        """Returns element inverse for an Abelian group."""

        # return inverse if element belongs to an Abelian group
        if self.group.is_abelian():
            return self ** -1
        # otherwise, complain
        else:
            raise ValueError("Element must belong to an Abelian group.")

    # returns the product of this element with another's inverse
    def __sub__(self, elem):
        """Returns self * (elem ** -1) for Abelian groups."""

        # return product if both elements belong to Abelian groups
        if self.group.is_abelian() and elem.group.is_abelian():
            return self * (elem ** -1)
        # otherwise, complain
        else:
            raise ValueError("Both Elements must belong to Abelian groups.")

    # TODO
    # def order(self):
    #     """Returns the order of self in the Group"""
    #     return len(self.group.generate([self]))