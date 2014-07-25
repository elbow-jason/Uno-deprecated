# -*- coding: utf-8 -*-

import markup
from markupsafe import Markup

from errors import error
print "SUPER"


class UnoFormatString(object):

    def __init__(self, name):
        __name = name
        self.format_tag = '{' + name + '}'
        self.text = self.format_tag
    def __call__(self):
        return self.format_tag

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        self._text = value
    


class UnoBaseStrings(object):
    base        = UnoFormatString('')
    element     = UnoFormatString('element')
    nested      = UnoFormatString('nested')
    label       = UnoFormatString('label')
    payload     = UnoFormatString('payload')


class UnoBaseInfo(object):
    safe = True
    attrs = {}
    nested = []


class UnoBase(object):
    _info        = UnoBaseInfo()
    _string      = UnoBaseStrings()
    _is_rendered = False

    def _unosafe_assign(self, kwargs, _safe=True):
        for key, val in kwargs:
            if _safe:
                if key not in self.__dict__.keys():
                    self.__add_attr__(key, val)
                else:
                    error.safe_is_true()
            else:
                self.__add_attr__(key, val)

    def __html__(self):
        return self()

    def __call__(self, **kwargs):
        return self.__render__(**kwargs)

    def _finish(self, arg=''):
        self.__render__()
        self._html = self._html.replace(self._string.base, '')

    def _render(self, **kwargs):
        self.__render__(**kwargs)

    @property
    def _html(self):
        if not self._is_rendered:
            self.__render__()
        return self.__html
    @_html.setter
    def _html(self, value):
        self._is_rendered = True
        self.__html = value
    

    def __render__(self, kwargs):
        self._is_rendered = True
        if kwargs:
            self._html =  Markup(str(kwargs))
        else:
            self._html = Markup("<div> NOTHING RENDERED; NO KWARGS PASSED <div>")
        return self._html

    def _merge_dicts(self, a, b):
        return dict(a.items() + b.items())

    def _add_element(self, orig_list, thing):
        orig_list._insert_element(len(orig_list), thing)
        return orig_list

    def _insert_element(self, orig_list, thing, idx): # idx for index
        if isinstance(thing, UnoBaseElement):
            orig_list.insert(idx, thing)
            return orig_list
        else:
            raise Exception('Inserted object was not an UnoBaseElement')


class UnoBaseForm(UnoBase):
    _has_title = False

    def __init__(self, name, fields=[], **kwargs):
        self.name       = name
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

    def __init__(self, name='', safe=True, attrs={}):
        self._info.tag       = 'div'
        self._info.name      = name
        self._info.attrs     = attrs
        self._info.payload   = ''
        self._info.safe      = safe

    def _update_info(self, attr_name, value):
        self._info.__dict__[attr_name] = value

    def _add_nested__(self, thing):
        self.__insert_nested__(len(self._info.nested), thing)

    def _insert_nested__(self, idx, thing): # idx for index
        if isinstance(thing, UnoBaseElement):
            self._info.nested.insert(idx, thing)
        else:
            raise Exception("Could not nest {}. Not a UnoBaseElement.".format(str(thing)))

    def _check_for_attr_named_class(self, name, value):
        if name == 'class' or name == '_class':
            return 'class_', value
        else:
            return name, value

    def _attr_named_class_prerender(self, attr_dict):
        if any(x in ['class', '_class', 'class_'] for x in attr_dict.keys()):
            try:
                x = attr_dict['class']
                return attr_dict
            except: pass 

            try:
                attr_dict['class'] = attr_dict['class_']
                del attr_dict['class_']
                return attr_dict
            except: pass

            try:
                attr_dict['class'] = attr_dict['_class']
                del attr_dict['_class']
                return attr_dict
            except: pass

    def _update_attrs(self, attrs):
        self._info.attrs = self._merge_dicts(self._info.attrs, attrs)

    def _add_attrs(self, attrs):
        for name, value in attrs.items():
            self._add_attr(name, value)

    def _add_attr(self, name, value):
        (name, value) = self._check_for_attr_named_class(name, value)
        if not isinstance(name, basestring):
            raise Exception('UnoHTMLTag attribute name was not a basestring (str type or unicode type)')
        if not isinstance(value, basestring):
            raise Exception('UnoHTMLTag attribute value was not a basestring (str type or unicode type)')
        self._update_attrs({name:value})
        setattr(self, name, value)

    def __iter__(self, func):
        return [func(x[0], x[1]) for x in self._info.attrs.items()]

    def __unicode__(self):
        return self()

    def __html__(self):
        return self()

    def __call__(self, **kwargs):
        return self.__render__(self, **kwargs)

    def _stringify_kwarg(self, kwarg_tuple):
        return "{}={}".format(kwarg_tuple[0], kwarg_tuple[1])

    def _markup_safe(self, html_string):
        return Markup(html_string)

    def _render(self, **kwargs):
        self.__render__(self, **kwargs)

    def __render__(self, this_obj, **kwargs):
        new_kwargs = this_obj._merge_dicts(this_obj._info.attrs, kwargs)
        new_kwargs = this_obj._attr_named_class_prerender(new_kwargs)
        try:
            this_obj._info.payload += this_obj._render_nested()
            element = markup.__getattribute__(this_obj._info.tag)(this_obj._info.payload, **new_kwargs)
        except AttributeError, e:
            if str(e).startswith("'module' object has no attribute"):
                raise Exception("markup module has no html tag type '{}'".format(this_obj._info.tag))
            else:
                raise e
        except TypeError, e:
            if str(e).startswith('<lambda>() argument after ** must be a mapping, not'):
                raise Exception("Invalid kwargs for rendering check the ._info._attrs of '{}' object.".format(this_obj._info.name))
            else:
                raise e
        this_obj._is_rendered = True
        this_obj._html    = this_obj._markup_safe(element)
        self = this_obj
        return self._html

    def _render_nested(self):
        nest = ''
        for element in self._info.nested:
            nest += element()
        self._nest = nest
        return nest


class UnoBaseField(UnoBase):

    @property
    def elements(self):
        return self._elements
    @elements.setter
    def elements(self, value):
        self._elements = self._check_elements(value)

    def __init__(self, name, elements=[], field_type='text'):
        self.name       = name
        self.elements   = elements
        self._has_label = False
        self.field_type = field_type


    def _check_elements(self, elements):
        if isinstance(elements, list):
            if self._are_elements(elements):
                return elements
        elif isinstance(elements, tuple):
            if self._are_elements(elements):
                return [x for x in elements]
        elif isinstance(elements, dict):
            try:
                x = self._extract_elements_from_kwargs(elements)
            except: pass
            try:
                if x:
                    if self._are_elements(x):
                            return x
            except: pass
            try:
                if self._are_elements(elements.values()):
                    return elements.values()
            except: pass
        elif self._is_element(elements):
            return list(elements)
        else:
            error.not_elements()


    def _add_elements(self, kwargs):
        self.elements.append(kwargs)

    def _reorder_element(self, name, new_idx):
        pass

    def _extract_elements_from_kwargs(self, kwargs):
        if kwargs.has_key('elements'):
            if self._is_element(kwargs['elements']):
                return [kwargs['elements']]
            elif isinstance(kwargs['elements'], list, tuple):
                self._are_elements(kwargs['elements'].values())
                return kwargs['elements']
            else:
                raise Exception("At least one of the indexes of the kwargs's 'elements' list was not a UnoBaseElement child")


    def _are_elements(self, thing_list):
        return not False in [self._is_element(x) for x in thing_list]

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
        self._html = output
        return output
