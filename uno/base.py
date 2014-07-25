# -*- coding: utf-8 -*-

import markup
from markupsafe import Markup

try:
    from .errors import error
    
    print "SUPER"
except:
    raise Exception('One of the imports failed. Shame on the you.')


class UnoFormatString(object):

    def __init__(self, name):
        __name = name
        self.format_tag = '{' + name + '}'

    def __call__(self):
        return self.format_tag


class UnoBaseStrings(object):
    base        = UnoFormatString('')
    element     = UnoFormatString('element')
    nested      = UnoFormatString('nested')
    label       = UnoFormatString('label')


class UnoBaseInfo(object):
    safe = True


class UnoBase(object):
    _info        = UnoBaseInfo()
    _string      = UnoMetaInfo()
    _is_rendered = False

    def _unosafe_assign(self, kwargs, safe=True):
        for key, val in kwargs:
            if safe:
                if key not in self.__dict__.keys():
                    self.__add_attr__(key, val)
            else:
                raise Exception(error.safe.format(key))
        else:
            self.__add_attr__(key, val)

    def __html__(self):
        return self()

    def __call__(self, **kwargs):
        return self.__render__(self, **kwargs)

    def finish(self, arg=''):
        self.__render__()
        self._rendered = self._rendered.replace(self.substring, '')

    @property
    def _rendered(self):
        if not self._is_rendered:
            self.__render__()
        return self.__rendered
    @_rendered.setter
    def _rendered(self, value):
        self.__rendered = value

    def __render__(self, **kwargs):
        self._is_rendered = True
        if kwargs:
            self._rendered =  Markup(str(kwargs))
        else:
            self._rendered = Markup("<div> NOTHING RENDERED; NO KWARGS PASSED <div>")
        return self.__rendered


class UnoBaseForm(UnoBase):
    _has_title = False

    def __init__(self, name, fields=[], **kwargs):
        self._info.name = name
        self.fields     = fields

    def _extract_fields_from_kwargs(self, kwargs):
        if kwargs.has_key('fields'):
            if self._is_field(kwargs['fields']):
                return [kwargs['fields']]
            if isinstance(kwargs['fields'], list, tuple):
                if not False in [self._is_field(x) for x in kwargs['fields']]:
                    return list(kwargs['fields'])
                else:
                    raise Exception("At least one of the indexes of the passed kwarg\'s 'elements' list was not a UnoBaseElement child")
            else:
                raise Exception("Kwargs invalid for elements assignment. Make sure kwargs['']" )

    def _is_field(self, thing):
        return isinstance(thing, UnoBaseField)

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._has_title = True
        self._title = value


class UnoBaseElement(UnoBase):
    """
    The base class for an Uno element object.
    """

    def __init__(self, name, tag_type, safe=True, **kwargs):
        self._info.name      = name
        self._info.attrs     = kwargs
        self._info.payload   = self.base_string
        self._info.tag       = tag
        self._info.safe      = safe
        self._unosafe_assign(kwargs, safe=safe)
        self._rendered = False

    def __add_nested__(self, thing):
        self.__insert_nested__(len(self._info.nested), thing)

    def __insert_nested__(self, idx, thing): # idx for index
        if isinstance(thing, UnoBaseElement):
            self._info.nested.insert(idx, thing)
        else:
            raise Exception("Could not nest {}. Not a UnoBaseElement.".format(str(thing)))

    def __add_attr__(self, name, value):
        if not isinstance(name, basestring):
            raise Exception('UnoHTMLTag attribute name was not a basestring (str type or unicode type)')
        if not isinstance(value, basestring):
            raise Exception('UnoHTMLTag attribute value was not a basestring (str type or unicode type)')
        self._info.attrs = dict(self._info.attrs.items() + dict(name=value).items())
        setattr(self, name, value)

    def __iter__(self, func):
        return [func(x[0], x[1]) for x in self._info.attrs.items()]

    def __unicode__(self):
        return self()

    def __html__(self):
        return self()

    def __call__(self, **kwargs):
        return self.__render__(self, **kwargs)

    def __stringify_kwarg__(self, kwarg_tuple):
        return "{}={}".format(kwarg_tuple[0], kwarg_tuple[1])

    def __markup_safe__(self, html_string):
        return Markup(html_string)

    def __render__(self, this_obj, **kwargs):
        new_kwargs = dict(this_obj._info._attrs.items() + kwargs.items())
        try:
            this_obj.__payload__ += __rendernested__()
            element = markup.__getattribute__(this_obj.tag)(this_obj.__payload__, **new_kwargs)
        except AttributeError, e:
            if str(e).starts_with("'module' object has no attribute"):
                raise Exception("markup module has no html tag type '{}'".format(this_obj._info.tag))
            else:
                raise e
        except TypeError, e:
            if str(e).starts_with('<lambda>() argument after ** must be a mapping, not'):
                raise Exception('invalid kwargs for rendering check the .attributes of {}'.format(this_obj._info.name))
            else:
                raise e

        self._rendered = self.__markup_safe__(element)
        return self._rendered

    def __rendernested__(self):
        nest = ''
        for element in self._info.nested:
            nest += element()
        self._nest = nest
        return nest


class UnoBaseField(UnoBase):

    def __init__(self, name, field_type, elements=[], **kwargs):
        self._info.name = name
        self._info.type = field_type
        self.elements = elements
        self._has_label = False

    def _init_elements(self, kwargs):
        self.elements = self._extract_elements(kwargs)

    def _extract_elements_from_kwargs(self, kwargs):
        if kwargs.has_key('elements'):
            if self._is_element(kwargs['elements']):
                return [kwargs['elements']]
            if isinstance(kwargs['elements'], list, tuple):
                if not False in [self._is_element(x) for x in kwargs['elements']]:
                    return kwargs['elements']
                else:
                    raise Exception("At least one of the indexes of the passed kwarg\'s 'elements' list was not a UnoBaseElement child")
            else:
                raise Exception("Kwargs invalid for elements assignment. Make sure kwargs['']" )

    def _is_element(self, thing):
        return isinstance(thing, UnoBaseElement)

    def finish(self, arg=''):
        self.raw_html.format(arg)
        self.raw_html = self.raw_html.replace(self.substring, '')

    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, value):
        if self._is_element(value):
            self._has_label = True
            self._label = value
        else:
            raise Exception('The label must be an UnoBaseElement')

    def __render__(self):
        output = ''
        if self._has_label:
            self.elements.insert(0, self.label)
        for element in self.elements:
            output += element()
            output += '\n'
        self._rendered = output
        return output
