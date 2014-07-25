# -*- coding: utf-8 -*-

class ErrorObj(object):
    def not_elements(self):
        raise Exception('Not valid elements')

    def safe_is_true(self, key):
        raise Exception("""
UnoForm base cannot override base attributes while unoformsafe is True.
\tPlease:
\t\tChange the key '{}' to something else.
\tor
\t\tPass 'unoformsafe=False' during class instantiaion to be allowed to override object methods.""".format(key))



error = ErrorObj()