
#not used
class NonStat(object):
    def __init__(self, string):
        self.string = string

    def __call__(self, val):
        return {self.string: val}


class NonStatics(object):

    def _setup(self, name, val):
        setattr(self, name, NonStat(val))

    def _setup_many(self, iterable):
        for obj in iterable:
            self._setup(obj[0], obj[1])

                  ('ngm',  'ng-model'),
                  ('eq',   'equal-to'),
                  ('name', 'name'),
                  ('type',  'type'),
                  ('klass', 'class'),]

iod = NonStatics()
iod._setup_many(non_static_css)