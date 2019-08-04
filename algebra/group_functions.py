"""Group Function Implementations"""

# local imports
from . import Set, Function, Group

# # TODO
# class GroupHomomorphism(Function):
#     """
#     The definition of a Group Homomorphism
    
#     A GroupHomomorphism is a Function between Groups that obeys the group
#     homomorphism axioms.
#     """

#     def __init__(self, domain, codomain, function):
#         """Check types and the homomorphism axioms; records the two groups"""

#         if not isinstance(domain, Group):
#             raise TypeError("domain must be a Group")
#         if not isinstance(codomain, Group):
#             raise TypeError("codomain must be a Group")
#         if not all(function(elem) in codomain for elem in domain):
#             raise TypeError("Function returns some value outside of codomain")

#         if not all(function(a * b) == function(a) * function(b) \
#                    for a in domain for b in domain):
#             raise ValueError("function doesn't satisfy the homomorphism axioms")

#         self.domain = domain
#         self.codomain = codomain
#         self.function = function

#     def kernel(self):
#         """Returns the kernel of the homomorphism as a Group object"""
#         G = Set(g.elem for g in self.domain if self(g) == self.codomain.e)
#         return Group(G, Function(G * G, G, self.domain.bin_op.function))

#     def image(self):
#         """Returns the image of the homomorphism as a Group object"""
#         G = Set(g.elem for g in self._image())
#         return Group(G, Function(G * G, G, self.codomain.bin_op.function))

#     def is_isomorphism(self):
#         return self.is_bijective()
