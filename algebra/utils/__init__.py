# import everything to utils namespace

## some convenience functions

# decorator to cast return values of inherited methods as decorated class
def castInheritedMethods(method_strings):
    # returns class-casted method
    def castMethod(cls, method):
        return lambda *args: cls(method(*args))

    # actual decorator
    def decorator(cls):
        # loop through method strings
        for method_string in method_strings:
            # extract method
            method = getattr(cls, method_string)

            # create casted method
            casted = castMethod(cls, method)

            # replace original with casted method
            setattr(cls, method_string, casted)

        # return modified class
        return cls

    # return decorating function
    return decorator
