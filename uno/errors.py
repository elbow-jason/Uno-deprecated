
        class ErrorObj(object):
            pass

        error = ErrorObj()
        error.safe = """
UnoForm base cannot override base attributes while unoformsafe is True.
\tPlease:
\t\tChange the key '{}' to something else.
\tor
\t\tPass 'unoformsafe=False' during class instantiaion to be allowed to override object methods."""
