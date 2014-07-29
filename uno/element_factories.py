"""
# -*- coding: utf-8 -*-

from uno import markup
from uno import helpers
from uno.simple_elements import ele, UnoElement, UnoGroup




class InfoHolder(object):

    def combine(self, a, b):
        return helpers.combine_dicts(a, b)

    def _prop_hidden_(self, name):
        return '_' + name

    def _uni_setter(self, name, value):
        setattr(self, self._prop_hidden_(name), value)

    def _uni_getter(self, name):
        return getattr(self, self._prop_hidden_(name))

    def _use_adder(self, adder, iterable):
        for obj in iterable:
            adder(obj[0], obj[1])

    def _adder_(self, attr, val):
        setattr(self, attr, property(self._uni_getter, self._uni_setter))
        setattr(self, attr, val)

    def _addmany_(self, iterable):
        self._use_adder(self._adder_, iterable)

    def _adder_non_static(self, attr):
        setattr(self, attr, property(self._dictify_getter, self._dictify_setter))

    def _addmany_non_static(self, iterable):
        self._use_adder(self._adder_non_static, iterable)

    def _dictify_getter(self, name, val):
        p_name = self._prop_hidden_(name)
        x = getattr(self, p_name)
        return { x[0] : x[1].format(val) }

    def _dictify_setter(self, name, val):
        p_name = self._prop_hidden_(name)
        bi_tup = (val, '{}')
        setattr(self, p_name, bi_tup)


s = InfoHolder()
s._addmany_(css_strings)



css_dicts = [(s.input, iod.klass(s.form_crtl)),
             (s.typ,   iod.typ(s.text)),
            ]

d = InfoHolder()
d._addmany_(css_dicts)


class Templates(object):

    def text_input(self):
        inp = ele.Input()
        inp.add_css(d.input)
        inp.add_css(iod.typ(s.text))
        return inp



new = Templates()
"""