# -*- coding: utf-8 -*-

from collections import Iterable

from uno import markup, helpers, Markup, constants

from uno.constants import (PAYLOAD, CSS, STATIC_TAGS, NORMAL_TAGS, 
                           ABNORMAL_TAGS, SELF_CLOSING_TAGS,)

PAYLOAD_TAGS = helpers.minus(NORMAL_TAGS, ABNORMAL_TAGS)

from uno.quickadder import ElementQuickAdder, GroupQuickAdder

import copy

from itertools import chain



class UnoBase(object):

#    def __repr__(self):
#        return self._render

    def __str__(self):
        return self._render

    def __call__(self):
        return self._render

    def __unicode__(self):
        return unicode(self._render)

    def __html__(self):
        return self._render

    def __add__(self, other):
        x = self._render
        try:
            y = other._render
        except:
            y = str(other)
        return x + ' ' + y

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if isinstance(value, UnoBase):
                self._features.append(name)
                self._features_dict[name] = value
        object.__setattr__(self, name, value)


class UnoBaseFeature(UnoBase):
    members = []

    def _render_features(self):
        text = ''
        for feat in self._features:
            text += self._features_dict[feat]._render
        return text

    @property
    def _render(self):
        self._render = self._text + self._render_features()
        return self.__render

    @_render.setter
    def _render(self, value):
        self.__render = value

    def __init__(self, *args, **kwargs):
        self._features      = []
        self._features_dict = {}
        self._is_type       = ('feature', 'base')
        self._text          = ''
        self._payload       = ''
        self.__class__.members.append(self)


    def _register(self, obj):
        self._parent = obj

    def _add_feature(self, feature):
        self._features.append(feature._name)
        self._features_dict[feature._name] = feature


class Payload(UnoBaseFeature):

    def __init__(self, name, **kwargs):
        super(Payload, self).__init__(self, **kwargs)
        self.name       = name
        self.is_type    = ('payload',)
        self._text      = ''


class Css(UnoBaseFeature):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        print 'new css', self.attr, 'value:', value
        self._value = value
    
    @property
    def attr(self):
        return self._attr
    @attr.setter
    def attr(self, value):
        print 'new css attr:', value
        self._attr = value


    def __init__(self, attr, value, **kwargs):
        super(Css, self).__init__(self, **kwargs)
        self.attr       = attr 
        self.value      = value
        self._is_type   = ('css',)
        self._text      = ' ' + attr + '="{}"'.format(value)


    def _extend(self, value):
        self.value += ' ' + value

    @property
    def _render(self):
        self._render = self._text + self._render_features()
        return self.__render
    @_render.setter
    def _render(self, value):
        self.__render = value
    


class BaseElement(UnoBaseFeature):

    def __init__(self, name, tag, *args, **kwargs):
        self._tag = tag
        self_closing = kwargs.pop('self_closing', False)
        if self_closing:
            self._closing_tag = ''
            self._postcss_tag = '/>'
        else:
            self._postcss_tag = '>'
            self._closing_tag = '<' + self._tag + '/>'
        super(BaseElement, self).__init__(self, name, **kwargs)
        self._name = name
        self._is_type = ('element',)
        self._precss_tag = '<' + self._tag

    def _render_group(self, is_type):
        text = ''
        for name in self._features:
            obj = self._features_dict[name]
            if is_type in obj._is_type:
                print is_type, ' IN ', obj._is_type
                text += obj._render
        return text + ' '

    def _render_css(self):
        x = self._render_group('css')
        return x

    def _render_payload(self):
        x = self._render_group('payload')
        return x

    def _render_elements(self):
        x = self._render_group('element')
        return x

    @property
    def _render(self):
        r =  self._precss_tag
        print 'precss: ', r
        e = self._render_css()
        print 'css: ', e
        n = self._postcss_tag
        print 'postcss: ', n
        d = self._render_payload()
        print 'payload: ', d
        er = self._render_elements()
        print 'elements: ', er
        pls = self._closing_tag
        print 'closing tag: ', pls
        self.__render = r+e+n+d+er+pls
        return self.__render

"""
class Useless(object):
    @property
    def _render(self):
        x = ''
        all_payload = self.payload + self._render_features() 
        x += self.pretext
        x += self.text.format(PAYLOAD=all_payload, CSS=' ' + self._css._render)
        x += self.posttext
        self.__render = Markup(x)
        return self.__render

    @_render.setter
    def _render(self, value):
        self.__render = value

    def _render_features(self):
        kids    = ''
        indent  = '    '
        newline = '\n'
        if self._features != []:
            for feature in self._features:
                kids += newline
                kids += indent
                kids += feature
            kids += newline
        return kids



class UnoGroup(object):

    def __init__(self, name):
        super(Css, self).__init__(self, name)
        self._is_type = ('format', 'CSS', 'css')
        self._text = CSS




class UnoBaseElement(object):

    members = {}

    def copy(self):
        return copy.copy(self)


    def __init__(self, tag=None, text=None, elements=[], payload='', posttext='',
                 pretext='', pre_payload='', post_payload='', data=None,
                 css_dict={}, meta_html_type='', name=None):

        if tag == None:
            self.tag = self.__class__._accessible_tag
        else:
            self.tag = tag

        if name != None:
            self.name = name
        else:
            self.name = self.__class__.__name__.lower()

        self.data         = data 
        self.elements     = elements
        self.payload      = payload
        self.css_dict     = css_dict
        self.posttext     = posttext
        self.pretext      = pretext
        self.pre_payload  = pre_payload
        self.post_payload = post_payload
        self.css_memory_text = helpers.ele.kwargs_to_css(self.css_dict)
        self.add_css     = ElementQuickAdder(self)

    @property
    def css_text(self):
        updated = helpers.ele.kwargs_to_css(self.css_dict)
        if updated != self.css_memory_text or self.css_memory_text == 'brand_new':
            self.css_text = updated
        return self._css_text


    @css_text.setter
    def css_text(self, value):
        print 'new css -> ' + value
        self._css_text = value
        self.css_memory_text = value


    @property
    def css_dict(self):
        return self._css_dict

    @css_dict.setter
    def css_dict(self, value):
        self._css_dict = value
        self.css_text


    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if not isinstance(value, (basestring)):
            raise Exception('UnoElement tag must be a basestring. {} was not acceptable.'.format(value))
        print "New TAG: ", value
        self._tag = value
        self.reset_text_html()

    @classmethod
    def new(cls, name, tag='div', text=None, elements=None, payload=None, posttext=None,
                 pretext=None, pre_payload=None, post_payload=None, data=None,
                 css_dict=None):
        class newClass(UnoBaseElement):
            _accessible_tag = ''
            pass

        def set_new_attrs(new_class, this_cls, attr_name, local_var, attr_default):
            if local_var:
                setattr(new_class, attr_name, local_var)
            try:
                cls_attr = getattr(this_cls, attr_name)
                if cls_attr != None:
                    setattr(new_class, attr_name, cls_attr)
                else:
                    setattr(new_class, attr_name, attr_default)
            except:
                setattr(new_class, attr_name, attr_default)

        attrs_to_set = [ ('tag', tag),
                         ('_accessible_tag', tag),
                         ('elements', list()), 
                         ('payload',  str()),
                         ('posttext', str()),
                         ('pretext',  str()),
                         ('pre_payload',  str()),
                         ('post_payload', str()),
                         ('data', None),
                         ('css_dict',  dict()),
                         ('_accessible_css_text', str()),
                         ('css_memory_text', 'brand_new')]


        
        for attr in attrs_to_set:
            try:
                locales = locals()[attr[0]]
            except:
                locales = None
            set_new_attrs(newClass, cls, attr[0], locales, attr[1] )

        newClass.__name__ = name.title()
        cls.members[name] = dict(name=name,class_obj=newClass)
        return newClass

    @property
    def render(self):
        x = str()
        all_payload = self.pre_payload + self.payload + self.post_payload + self.render_children() 
        x += self.pretext
        x += self.text.format(PAYLOAD=all_payload, CSS=' ' + self.css_text)
        x += self.posttext
        self._render = Markup(x)
        return self._render

    @render.setter
    def render(self, value):
        self._render = value

    def render_children(self):
        kids    = ''
        indent  = '    '
        newline = '\n'
        if self.elements != []:
            for child in self.elements:
                kids += newline
                kids += indent
                kids += child.render
            kids += newline
        return kids



    def add_css(self, keywarg):
        self.css_dict = helpers.combine_dicts(self.css_dict, keywarg)

    def append_css(self, name, val):
        self.css_dict[name] += (' '+ val)


    def reset_text_html(self):
        self.text = helpers.ele.setup_text_by_tag(self.tag)


    def __repr__(self):
        return self.render

    def __str__(self):
        return self.render

    def __call__(self):
        return self.render

    def __unicode__(self):
        return unicode(self.render)

    def __html__(self):
        return self.render


class UnoBaseGroup(UnoBase):
    An ordered collection of UnoElements. Each element has a group (maybe an
    empty list)


    def set_attr_on_element(self, name, ele_index, value):
        setattr(self.elements[index], name, value)

    def set_attr_on_all_elements(self, name, values, iterate_values=True):
        if isinstance(values, Iterable): 
            if iterate_values:
                if not len(values) == len(self.elements):
                    raise Exception('The passed iterable was not the correct length')
                for i in xrange(len(values)):
                    if not values[i] == False: # eq to 'if value:' but more clear
                        setattr(self.elements[i], name, values[i])
            else: 
                for ele in self.elements:
                    setattr(self, name, values)

    def set_attr_by_element_name(self, ele_name, attr_name, value):
        for element in self.elements:
            if element.name == ele_name:
                setattr(element, attr_name, value)

    def retrieve_elements_properties(self, name):
        attrs = []
        search_for = name[:-1]
        for element in self.elements:
            attrs.append(getattr(element, search_for))
            setattr(self, name, attrs)
        return attrs

    def add_elements_property(self, name, value):
        # create local fget and fset functions
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        # add property to self
        setattr(self.__class__, name, property(fget, fset))
        # add corresponding local variable
        setattr(self, '_' + name, value)

    def _set_property(self, name, value):
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        self.retrieve_elements_properties(name)
        return getattr(self, '_' + name)

    def set_all_group_properties(self):
        self.add_elements_property('pretexts', [])
        self.add_elements_property('posttexts', [])
        self.add_elements_property('payloads', [])
        self.add_elements_property('pre_payloads', [])
        self.add_elements_property('post_payloads', [])
        self.add_elements_property('tags', [])
        self.add_elements_property('css_dicts', [])
        self.add_elements_property('css_texts', [])
        self.add_elements_property('texts', [])

    def add_element(self, ele):
        self.elements.append(ele)

    def insert_element(self, ele, idx):
        self.elements.insert(idx, ele)

    @property
    def render(self):
        html =  ''
        html += self.pretext
        for child in self.elements:
            html += child.render
            html += '\n'
        html += self.posttext
        self.render = html
        return self._render

    @render.setter
    def render(self, value):
        self._render = value

    def __init__(self, elements=[]):
        self.name     = ''
        self.pretext  = ''
        self.posttext = ''
        self.elements = elements
        #elements and features of group
        self.set_all_group_properties()
        self.feature  = GroupQuickAdder(self)
"""