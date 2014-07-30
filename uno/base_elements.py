# -*- coding: utf-8 -*-

from uno.constants import NORMAL_TAGS, ABNORMAL_TAGS, SELF_CLOSING_TAGS, STATIC_TAGS, PAYLOAD, CSS
from uno import helpers

PAYLOAD_TAGS = helpers.minus(NORMAL_TAGS, ABNORMAL_TAGS)

from uno.base import UnoBaseElement
import markup



class UnoElementFactory(object):
    def set_all(self):
        for tag in PAYLOAD_TAGS:
            self.set_new(tag.title(), UnoBaseElement.new(tag, tag=tag, text=self.gen(tag)))
        for tag in SELF_CLOSING_TAGS:
            self.set_new(tag.title(), UnoBaseElement.new(tag, tag=tag, text='<'+ tag +' '+ CSS + ' />'))
        for tag in STATIC_TAGS:
            self.set_new(tag[0].title(), UnoBaseElement.new(tag[0], tag=tag[0], text=tag[1]))

    def set_new(self, tag, element_obj):
        setattr(self, tag, element_obj)

    def from_markup(self, tag):
        return getattr(markup, tag).__call__(PAYLOAD, **dict(replace_me=CSS))

    def gen(self, tag):
        try:
            base_element = self.from_markup(tag)
        except:
            base_element = self.from_markup('div')
            base_element = base_element.replace('div', tag)
        return base_element.replace('replace_me=', '').replace('"', '')#.replace(' ','')

    def kwargify_element(self, ele):
        idx = ele.find('>')
        return ele[:idx] + " " +  CSS + ele[idx:]

    def pre_payloadify_element(self, ele):
        first_idx = ele.find('<')
        idx = ele.find('<', first_idx)
        return ele[:idx] + " " +  PAYLOAD + ele[idx:]

    #def __init__(self):
    #    self.set_all()

base_ele = UnoElementFactory()
base_ele.set_all()
