# -*- coding: utf-8 -*-

from uno import markup, helpers

class InheritableMethodsClass(object):
    _not_inherited = helpers.PlaceHolder.__dict__.keys()
    
    @classmethod
    def _get_methods(cls):
        return helpers.get_all_parent_methods(cls)
    
    @classmethod
    def _ez_not_css(cls):
        return helpers.startswith_underscore(cls.__dict__)

    @classmethod
    def _parent_dicts(cls):
        return helpers.remove_double_underscores(cls._get_methods())

    @classmethod
    def _add_not_css(cls, new_items):
        cls._not_css = cls._not_css + new_items

    def __init__(self):
        self._not_css = self._ez_not_css()
        #self.__dict__ = helpers.remove_list_items_from_dict(self._not_inherited, self._parent_dicts())


class Base(InheritableMethodsClass):
    pass

class BaseElement(Base):
    _tag  = 'div'
    _payload = ''

    def _method_name_fixer(self, key):
        if key in ['_class', 'class_', 'class']:
            return 'class'
        elif key in ['_type', 'type_']:
            return 'type'
        else:
            return key

    def _set_name(self, name):
        self.name = name

    def _css_attrs(self):
        css_dict = {}
        for key, value in self.__dict__:
            if not key in self._not_css:
                key = self._method_name_fixer(key)
                css_dict[key] = value
        return css_dict

    def _render(self, *args, **kwargs):
        helpers.set_args_blank(self, args)
        helpers.set_kwargs(self, kwargs)
        return getattr(markup, self._tag).__call__(self._payload, **self._css_attrs())


class BaseDiv(BaseElement):
    pass

class BaseInput(BaseElement):
    _tag = 'input'
    value = ""


class BaseTextInput(BaseInput):
    _type = 'text'





