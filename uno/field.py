

from uno.base import UnoBaseFeature, 


class UnoBaseField(UnoBaseFeature):

    def __init__(self, name, **kwargs):
        super(UnoBaseField, self).__init__(self, **kwargs)
        self._is_type = ('field', 'base')
        self._data = ''
        self._name = 




# standard bs3 field follows...


