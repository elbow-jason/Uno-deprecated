# -*- coding: utf-8 -*-

from HTMLParser     import HTMLParser
from htmlentitydefs import name2codepoint
from collections    import OrderedDict

from uno.constants import SELF_CLOSING_TAGS
from uno.helpers   import join_under

from .nested_counter    import NestedCounter
from .varstacklist      import VarStackList


class NewStyleClassObject(object, HTMLParser):
    pass

class HTMLExtractor(NewStyleClassObject):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tracker    = NestedCounter()
        self.varstack   = VarStackList()
        self.data       = OrderedDict()

    @property
    def last_tag(self):
        return self._last_tag
    @last_tag.setter
    def last_tag(self, value):
        self._last_tag = value


    def parse(self, raw_html):
        self.data = OrderedDict()
        self.feed(raw_html)
        return self.data


    def handle_starttag(self, tag, attrs):
        current_ele = tag + '_' + self.tracker.g_id
        self.varstack.add(current_ele)
        self.construct_element(tag)
        self.last_tag = tag

        #css parse
        self.tracker.new_level
        for attr in attrs:
            keyval_pair = dict()
            #add css feature to stack
            self.varstack.add(attr[0] + '_' + self.tracker.g_id)
            keyval_pair[attr[0]] = attr[1]
            #assign stack as 'stack'
            css_tag = join_under([tag, self.tracker.g_id])
            self.construct_css(css_tag, keyval_pair)
            self.tracker.next
            #remove css feature from stack
            self.varstack.pop
        if tag in SELF_CLOSING_TAGS:
            self.tracker.end_level
            self.varstack.pop
        self.tracker.next


    def handle_endtag(self, tag):
        print "End tag  :", tag
        #html['end_tag_' + self.tracker.ct()] = tag +'_' + 'tag_' + self.tracker.ct()
        self.varstack.pop
        self.tracker.end_level

    def handle_data(self, data):
        print "Payload(", data, ')'
        self.varstack.add('payload_' + self.tracker.g_id)
        self.construct_payload(self.last_tag, data)
        self.varstack.pop
        self.tracker.next

    def construct_element(self, tag):
        self.construct(tag, tag,'element')

    def construct_css(self, tag, data):
        self.construct(tag, data,'css')

    def construct_payload(self, tag, data):
        self.construct(tag, data,'payload')

    def construct(self, tag, data,  typer):
        self.data[tag +'_' + typer + '_'  + str(self.tracker.g_id)] =\
                {'feature': typer.title(), 
                'data': data, 
                'position': self.tracker.position,
                'chart': [x for x in self.tracker.chart],
                'depth': len(self.tracker.chart),
                'g_id': self.tracker.g_id,
                'stack': self.varstack.string,
                'varname': typer + '_' + str(self.tracker.g_id)}


