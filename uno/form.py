form.py


from uno.base import UnoBaseFeature


class UnoBaseForm(UnoBaseFeature):

    def __init__(self):
        super(Payload, self).__init__(self, **kwargs)
        self._is_type = ('form', 'base')
        self._fields = []

    @property
    def _fields(self):
        self._update_fields()
        return self.__fields
    @_fields.setter
    def _fields(self, value):
        self.__fields = value
    

    def _update_fields(self):
        for attr in self._features.keys():
            if 'field' in self._features[attr]._is_type:
                self._fields.append(self._features[attr])


    def _populate_obj(self, obj):
        for field in self._fields:



