"""Element Implementation"""

# local imports
from algebra import Group

# # define Element class
# class Element:
#     """
#     Implementation of a group element
    
#     This is mainly syntactic sugar, so you can write stuff like g * h
#     instead of group.bin_op(g, h), or group(g, h).
#     """

#     # initialization
#     def __init__(self, elem, group):
#         """Initialize an element as part of a group."""

#         # check that group is a Group
#         if not isinstance(group, Group):
#             print(type(group), type(Group), isinstance(group, Group))
#             raise TypeError("group is not a Group")

#         # check that the element is in the group
#         if not elem in group.elements:
#             raise ValueError("elem is not an element of group")

#         # record element and group
#         self.elem = elem
#         self.group = group

#     def __str__(self):
#         return str(self.elem)

#     def __eq__(self, other):
#         """
#         Two Elements are equal if they represent the same element,
#         regardless of the Groups they belong to
#         """

#         if not isinstance(other, Element):
#             raise TypeError("other is not a Element")
#         return self.elem == other.elem

#     def __ne__(self, other):
#         return not self == other

#     def __hash__(self):
#         return hash(self.elem)

#     def __mul__(self, other):
#         """
#         If other is a group element, returns self * other.
#         If other = n is an int, and self is in an abelian group, returns self**n
#         """
#         if self.group.is_abelian() and isinstance(other, (int, long)):
#             return self ** other

#         if not isinstance(other, Element):
#             raise TypeError("other must be a Element, or an int " \
#                             "(if self's group is abelian)")
#         try:
#             return Element(self.group.bin_op((self.elem, other.elem)), \
#                              self.group)
#         # This can return a TypeError in Funcion.__call__ if self and other
#         # belong to different Groups. So we see if we can make sense of this
#         # operation the other way around.
#         except TypeError:
#             return other.__rmul__(self)

#     def __rmul__(self, other):
#         """
#         If other is a group element, returns other * self.
#         If other = n is an int, and self is in an abelian group, returns self**n
#         """
#         if self.group.is_abelian() and isinstance(other, (int, long)):
#             return self ** other

#         if not isinstance(other, Element):
#             raise TypeError("other must be a Element, or an int " \
#                             "(if self's group is abelian)")

#         return Element(self.group.bin_op((other.elem, self.elem)), self.group)

#     def __add__(self, other):
#         """Returns self + other for Abelian groups"""
#         if self.group.is_abelian():
#             return self * other
#         raise TypeError("not an element of an abelian group")
        
#     def __pow__(self, n, modulo=None):
#         """
#         Returns self**n
        
#         modulo is included as an argument to comply with the API, and ignored
#         """
#         if not isinstance(n, (int, long)):
#             raise TypeError("n must be an int or a long")

#         if n == 0:
#             return self.group.e
#         elif n < 0:
#             return self.group.inverse(self) ** -n
#         elif n % 2 == 1:
#             return self * (self ** (n - 1))
#         else:
#             return (self * self) ** (n / 2)

#     def __neg__(self):
#         """Returns self ** -1 if self is in an abelian group"""
#         if not self.group.is_abelian():
#             raise TypeError("self must be in an abelian group")
#         return self ** (-1)

#     def __sub__(self, other):
#         """Returns self * (other ** -1) if self is in an abelian group"""
#         if not self.group.is_abelian():
#             raise TypeError("self must be in an abelian group")
#         return self * (other ** -1)

#     def order(self):
#         """Returns the order of self in the Group"""
#         return len(self.group.generate([self]))
