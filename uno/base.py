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

    #def __repr__(self):
    #    return self._render

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

    def _all_features(self):
        x = {}
        x += self._features_dict
        for feat in self._features:
            x += self._features_dict[feat]._all_features()
        return x




class Payload(UnoBaseFeature):

    def __init__(self, name, text, **kwargs):
        super(Payload, self).__init__(self, **kwargs)
        self.is_type    = ('payload',)
        self.name       = name
        self._text      = text


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
        self._postcss_tag = '>'
        self._closing_tag = '<' + self._tag + '/>'
        spc_tag = kwargs.pop('special_tag', False)
        if spc_tag:
            self._closing_tag = ''
            self._postcss_tag = '>'
        self_closing = kwargs.pop('self_closing', False)
        if self_closing:
            self._closing_tag = ''
            self._postcss_tag = '/>'
        super(BaseElement, self).__init__(self, name, **kwargs)
        self._name = name
        self._is_type = ('element',)
        self._precss_tag = '<' + self._tag

    def _render_group(self, is_type):
        text = ''
        first = True
        for name in self._features:
            obj = self._features_dict[name]
            if is_type in obj._is_type:
                if first and is_type in ['payload','element']:
                    first = False
                    text += ' '
                text += obj._render
        return text

    def _render_css(self):
        is_type = 'css'
        text    = ''
        first   = True
        for name in self._features:
            obj = self._features_dict[name]
            if is_type in obj._is_type:
                text += obj._render
        return text

    def _render_payload(self):
        x = self._render_group('payload')
        if x != '':
            x += '\n'
        return x 

    def _render_elements(self):
        x = self._render_group('element')
        return x

    @property
    def _render(self):
        r =  self._precss_tag
        #print 'precss: ', r
        e = self._render_css()
        #print 'css: ', e
        n = self._postcss_tag
        #print 'postcss: ', n
        d = self._render_payload()
        #print 'payload: ', d
        er = self._render_elements()
        #print 'elements: ', er
        pls = self._closing_tag
        #print 'closing tag: ', pls
        self.__render = r+e+n+d+er+pls + '\n'
        return self.__render 
