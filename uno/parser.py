

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from constants import SELF_CLOSING_TAGS, RESERVED_WORDS_LOWER
import collections as coll

class HTML(object):
    name = ''
    def __init__(self, name):
        self.name


def remove_newlines(string):
    return string.replace('\n', '')


#html = HTML('html')
html = coll.OrderedDict()

class Tracker(object):

    def __init__(self):
        self.ctr = 0
        self.tracker = []

    def ct(self):
        if self.tracker == []:
            self.tracker.append(self.ctr)
        x = [str(t) for t in self.tracker]
        return '_'.join(x)

    def get_tracker(self):
        return self.tracker[-1]

    def append_tracker(self):
        self.tracker.append(self.ctr)

    def tick(self):
        self.append_tracker()
        self.ctr += 1

    def pop_tracker(self):
        self.tracker.pop(-1)


class UnoBaseParser(HTMLParser):

    def start(self):
        self.tracker = Tracker()

    def handle_starttag(self, tag, attrs):
        self.tracker.tick()
        print "Start tag:", tag
        html[tag +'_' + 'tag_' + self.tracker.ct()] = {'feature':'Element','tag':tag,'id': self.tracker.get_tracker() }
        holder = dict()
        for attr in attrs:
            holder[attr[0]] = attr[1]
            print " Css: " + self.tracker.ct() + str(attr)
        html[tag + '_' + 'attrs_'+ self.tracker.ct()] = {'feature':'Css','attrs': holder ,'id': self.tracker.get_tracker() }

    def handle_endtag(self, tag):
        print "End tag  :", tag
        #html['end_tag_' + self.tracker.ct()] = tag +'_' + 'tag_' + self.tracker.ct()
        self.tracker.pop_tracker()

    def handle_data(self, data):
        print "Payload(", data, ')'
        html['payload_' + self.tracker.ct()] = {'feature':'Payload', 'payload':data, 'id': self.tracker.get_tracker() }
        self.tracker.tick()

    def handle_comment(self, data):
        print "Comment  :", data
        html['comment_' + self.tracker.ct()] = data
        self.tracker.tick()

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
        html['named_ent'+ self.tracker.ct()] = c
        self.tracker.tick()

    def parse(self, raw_html):
        self.start()
        return self.feed(raw_html)

    def add_parsed_element(self, **kwargs):
        print "element kwargs: ", kwargs
        return "\n{varname} = Element('{varname}', '{tag}')".format(**kwargs)
        

    def add_parsed_css(self, **kwargs):
        text = ''
        print "css kwargs: ", kwargs
        varname = kwargs.pop('varname', 'unk_ele_name')
        print "css kwargs: ", kwargs
        for key in kwargs:
            value = kwargs[key]
            key = self.reserved_word_checker(key)
            template = "\n{varname}.{key} = Css('{key}','{value}')"
            text += template.format(varname=varname, key=key, value=value)
        return text

    def reserved_word_checker(self, attr_name):
        if attr_name in RESERVED_WORDS_LOWER:
            return attr_name.upper()
        else:
            return attr_name

    def add_parsed_payload(self, **kwargs):
        print 'payload kwargs:', kwargs
        return "\n{varname}.{pname} = Payload('{pname}', '{payload}')".format(**kwargs)
        x = "\n{varname}.{pname} = Payload('{pname}', '{payload}')"
        x = x.format(**kwargs)
        return x

    def parsed_to_code(self, parsed_data):
        text = ''
        for item_name in parsed_data:
            print "item_name:", item_name
            info = parsed_data[item_name]
            print "info:", info
            print type(info)
            varname = 'element_' + str(info['id'])
            if info['feature'] == 'Element':
                k_wargs = dict(varname=varname, tag=info['tag'])
                text += self.add_parsed_element(**k_wargs)
            if info['feature'] == 'Css':
                info['attrs']['varname'] = varname
                text += self.add_parsed_css(**info['attrs'])
            if info['feature'] == 'Payload':
                k_wargs = dict(varname=varname, 
                                pname=item_name, 
                                payload=info['payload'])
                text += self.add_parsed_payload(**k_wargs)
        return text




uno_parser  = UnoBaseParser()

import markup

div = markup.div("Look! It's a payload." + markup.input(**{'class':'form-control btn col-lg-6'}), **dict(id='some_css'))

div = remove_newlines(div)













"""
def handle_charref(self, name):
    if name.startswith('x'):
        c = unichr(int(name[1:], 16))
    else:
        c = unichr(int(name))
    print "Num ent  :", c
    html.startswith_x = c
def handle_decl(self, data):
    print "Decl     :", data
    html.decl = data
"""
