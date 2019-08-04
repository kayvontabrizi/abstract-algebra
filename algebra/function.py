"""Function Implementation"""

# local imports
from . import Set

# define Function class
class Function(object):
    """Implementation of a finite function"""

    # initialization
    def __init__(self, domain, codomain, function):
        """
        Initialize the function and check that it is well-formed.

        This method can be overwritten by subclasses of Function, so that for
        example GroupHomomorphisms can be between Groups, rather than Sets.
        """

        # initialize super
        super().__init__()

        # check that domain is a Set
        if not isinstance(domain, Set):
            raise TypeError("The domain must be a Set!")

        # check that codomain is a Set
        if not isinstance(codomain, Set):
            raise TypeError("The codomain must be a Set!")

        # verify codomain contains image of domain
        if not all(function(elem) in codomain for elem in domain):
            raise ValueError("Function returns a value outside of codomain.")

        # record domain, codomain, and function
        self.domain = domain
        self.codomain = codomain
        self.function = function

    # invoke function on element
    def __call__(self, *elem):
        """Evaluates the function on packed arguments."""

        # The call packs multiple arguments for convenience, and leaves single
        # arguments unpacked. As a result, function elements cannot be a 1-ple.

        # undo list contraction if elem is 1-ple
        if len(elem) == 1: elem = elem[0]

        # verify the input element is in the domain
        if elem not in self.domain:
            raise ValueError("Function must be called on elements of the domain.")

        # return the output function
        return self.function(elem)

    # generate a hash from the domain and codomain
    def __hash__(self):
        """Returns a unique hash of the Function."""

        # Naftali Harris:
        #
        # Need to be a little careful, since self.domain and self.codomain are
        # often the same, and we don't want to cancel out their hashes by xoring
        # them against each other.
        # 
        # Also, functions we consider equal, like lambda x: x + 1, and 
        # def jim(x): return x + 1, have different hashes, so we can't include 
        # the hash of self.function.
        #
        # Finally, we should make the combination of hashes non-commutative,
        # so that switching the domain and codomain results in a new hash.

        # return hash
        return hash(self.domain) + 2 * hash(self.codomain)

    # check equality of two Functions
    def __eq__(self, other_func):
        """
        Returns true if input Functions share an id, or if they share domains,
        codomains, and domain images.
        """

        # return false if other_func is not a Function
        if not isinstance(other_func, Function):
            return False

        # return true if Functions are equivalent
        return id(self) == id(other_func) or ( \
               self.domain == other_func.domain and \
               self.codomain == other_func.codomain and \
               all(self(elem) == other_func(elem) for elem in self.domain) )

    # check inequality
    def __ne__(self, other_func):
        return not self == other_func

    # return the image of the domain as a Set
    def _image(self):
        """Returns the image of the function domain."""
        return Set(self(elem) for elem in self.domain)

    # return the image of the domain
    def image(self):
        """
        Returns the API image of the function; can change depending on the subclass.

        For example, GroupHomomorphisms return the image as a Group, not a Set.
        """
        return self._image()

    # return a string representation of the Function
    def __repr__(self):
        """Returns a string representation of the Function's domain and image."""

        # return a list of the input/output pairs
        return str([(x, self(x)) for x in self.domain])

    # return a pretty string representation of the Function
    def __str__(self):
        """Returns a pretty string representation of a Function."""

        # construct return string and return
        ret_str  = "Domain & Image:"
        ret_str += ''.join(f"\n{x} -> {self(x)}" for x in self.domain)
        ret_str += "\nRemaining Codomain:"
        ret_str += ''.join(f"\n -> {x}" for x in self.codomain - self._image())
        return ret_str

    # check that the function is surjective
    def is_surjective(self):
        """Check that the image of the domain is the codomain."""

        # cast self.domain as a Set, since it might not be in subclasses of Function
        return self._image() == Set(self.codomain)

    # check that the function is injective
    def is_injective(self):
        """Check that every element of the domain maps to a unique element in the codomain."""

        # check that the domain and its image are equal length
        return len(self.domain) == len(self._image())

    # check that the function is bijective
    def is_bijective(self):
        """Check bijectivity by requiring surjectivity and injectivity."""

        # check that the function is both surjective and injective
        return self.is_surjective() and self.is_injective()

    # return a composition function
    def compose(self, inner_func):
        """Returns: x -> self(inner_func(x))."""

        # check that the inner_func object is a Function
        if not isinstance(inner_func, Function):
            raise TypeError("The inner function is not a Function!")

        # verify that the inner function's codomain is the outer function's domain
        if not self.domain == inner_func.codomain:
            raise ValueError("The codomain of the inner function must match the domain of the outer.")

        # return the composition function
        return Function(inner_func.domain, self.codomain, lambda x: self(inner_func(x)))

# return an identity function on a set
def identity_func(input_set):
    """Returns the identity function on the input set."""

    # verify input is a Set
    if not isinstance(input_set, Set):
        raise TypeError("Input must be a Set!")

    # return identity Function
    return Function(input_set, input_set, lambda x: x)

# return a function given a dictionary mapping
def dict_func(input_dict):
    """Returns the corresponding to the mapping specified by input_dict."""

    # verify input is a dictionary
    if not isinstance(input_dict, dict):
        raise TypeError("Input must be a dictionary!")

    # return Function represented by the dictionary mapping
    return Function(Set(input_dict.keys()), Set(input_dict.values()), lambda x: input_dict[x])
