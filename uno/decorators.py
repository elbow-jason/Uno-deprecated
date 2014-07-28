

from functools import wraps

def setify(i):
        """
        Iterable to set.
        """
        return set(i)

def change_return_type(f):
    """
    Converts the returned value of wrapped function to the type of the
    first arg or to the type specified by a kwarg key return_type's value.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.has_key('return_type'):
            return_type = kwargs['return_type']
            kwargs.pop('return_type')
            return return_type(f(*args, **kwargs))
        elif len(args) > 0:
            return_type = type(args[0])
            return return_type(f(*args, **kwargs))
        else:
            return f(*args, **kwargs)
    return wrapper


def convert_args_to_sets(f):
    """
    Converts all args to 'set' type via self.setify function.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        args = (setify(x) for x in args)
        return f(*args, **kwargs)
    return wrapper







