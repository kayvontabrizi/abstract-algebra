"""Set Implementation"""

# local imports
from . import utils

# cast inherited set operators as Set
@utils.castInheritedMethods(f'__{x}__' for x in 'and or sub xor'.split())

# define Set class
class Set(frozenset):
    """
    Implementation of a set
    
    It's important that Set be a subclass of frozenset (not set) because:
    1) it makes Set immutable
    2) it allows Set to contains Sets
    """

    # define set product
    def __mul__(self, other_set):
        """Returns Cartesian product."""

        # check that the other_set object is a Set
        if not isinstance(other_set, Set):
            raise TypeError("One of these objects is not a Set!")

        # return set product
        return Set((x, y) for x in self for y in other_set)

    # define set exponentiation
    def __pow__(self, exponent, modulo=None):
        """
        Syntactic sugar for repeated Cartesian product.

        `modulo` is included as an argument to comply with the API, but
        is otherwise ignored.
        """

        # check that the exponent is an integer
        if not isinstance(exponent, int):
            raise TypeError("The exponent must be an integer!")

        # complain if exponent is less than 1
        if exponent < 1:
            raise ValueError("The exponent must be at least 1.")

        # calculate and return set products
        set_prod = self
        for i in range(exponent-1):
            set_prod *= self
        return Set(set_prod)
