

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

def joiner(sep, listthing):
    return sep.join([str(x) for x in listthing])

def join_under(listthing):
    return joiner('_', listthing)

def join_dot(listthing):
    return joiner('.', listthing)

#html = HTML('html')

class VarStackList(object):

    stack = []
    ele_stack = []
    sub_stack = stack

    def add_both(self, var):
        self.add_ele(var)
        self.add_sub(var)

    def drop_both(self):
        self.drop
        self.ele_drop

    def add_ele(self, var):
        self.ele_stack.append(var)

    def add(self, var):
        self.stack.append(var)
    
    @property
    def pop(self):
        self.stack.pop(-1)

    @property
    def drop_ele(self):
        self.ele_stack.pop(-1)

    @property
    def ele_str(self):
        return '.'.join(self.ele_stack)

    @property
    def string(self):
        return '.'.join(self.stack)

    sub_add = add
    sub_pop = pop
    sub_string = string

class NestedCounter(object):

    def __init__(self):
        self.count = 0
        self.chart = [0]
        self.total = 0
        self.serial_events = ['init']

    @property
    def g_id(self):
        return str(self.total)

    @property
    def position(self):
        self.print_chart
        y = [str(x) for x in self.chart]
        return '_'.join(y)

    @property
    def up_total(self):
        self.total += 1

    @property
    def print_chart(self):
        print 'chart:', str(self.chart)

    @property
    def pos(self):
        self.pos = str(self.chart[-1])
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def new_level(self):
        self.count = 0
        self.chart.append(0)
        self.print_chart
        self.up_total
        ser_string = 'new level: {}'
        ser_string.format(str(len(self.chart)))
        self.serial_events.append(ser_string)

    @property
    def end_level(self):
        self.chart.pop(-1)
        self.counter = self.chart[-1]
        self.print_chart
        ser_string = 'end level: {}, current item: {}'
        ser_string.format(str(len(self.chart) + 1), str(self.counter))
        self.serial_events.append(ser_string)

    @property
    def next(self):
        self.count += 1
        self.chart[-1] = self.count
        self.print_chart
        self.up_total
        ser_string = 'new feature on level: {}, item: {}'
        ser_string.format(str(len(self.chart)),  str(self.count))
        self.serial_events.append(ser_string)

    def __repr__(self):
        return str(self.chart)

    def uplevel(self, varname):
        self.new_level



class ParsedToCode(object):

    def __init__(self, parent_obj):
        self.parent = parent_obj

    def reserved_word_checker(self, attr_name):
        if attr_name in RESERVED_WORDS_LOWER:
            return attr_name.upper()
        else:
            return attr_name

    def cleanup_payload(self, payload):
        p = payload.replace('\n', '')
        p = p.rstrip()
        p = p.lstrip()
        return p

    def parse(self, raw_html):
        #self.start()
        return self.parent.feed(raw_html)

    def prep_css(self, info):
        if info['feature'] == 'Css':
            info['data']['stack'] = info['stack']
            return self.code_css(**info['data'])
        return ''

    def code_css(self, **kwargs):
        text = ''
        #print "css kwargs: ", kwargs
        stack = kwargs.pop('stack', 'unk_ele_name')
        #print "css kwargs: ", kwargs
        for key in kwargs:
            value = kwargs[key]
            key = self.reserved_word_checker(key)
            template = "\n{stack} = Css('{key}','{value}')"
            text += template.format(stack=stack, key=key, value=value)
        return text

    def prep_element(self, info):
        if info['feature'] == 'Element':
            return self.code_element(**dict(stack=info['stack'],
                    varname=info['data']+'_'+str(info['g_id']),
                    tag=info['data']))
        return ''

    def code_element(self, **kwargs):
        print "element kwargs: ", kwargs
        return "\n{stack} = Element('{varname}', '{tag}')".format(**kwargs)


    def prep_payload(self, info):
        if info['feature'] == 'Payload':
            payload = self.cleanup_payload(info['data'])
            if payload == "":
                return ''
            k_wargs =  dict(stack=info['stack'],
                            pname='payload_' + str(info['g_id']), 
                            payload=payload)
            return self.code_payload(**k_wargs)
        return ''

    def code_payload(self, **kwargs):
        print 'payload kwargs:', kwargs
        return "\n{stack} = Payload('{pname}', \"{payload}\")".format(**kwargs)

    def output(self, parsed_data):
        text = ''
        for item_name in parsed_data:
            info = parsed_data[item_name]
            text += self.prep_element(info)
            text += self.prep_css(info)
            text += self.prep_payload(info)
        return text

    def save(self, filename, data):
        with open(filename, 'w+') as file_:
            file_.write(data)

    def add_imports(self):
        return 'from uno.base import Element, Css, Payload\n\n'

    def save_with_imports(self, filename, data):
        new_data = self.add_imports() + data
        self.save(filename, new_data)


class UnoBaseParser(HTMLParser):

    def __cfg__(self):
        self.tracker = NestedCounter()
        self.code = ParsedToCode(self)
        self.html = coll.OrderedDict()
        self.varstack = VarStackList()

    __call__ = __cfg__

    @property
    def last_tag(self):
        return self._last_tag
    @last_tag.setter
    def last_tag(self, value):
        self._last_tag = value
    

    def construct_element(self, tag):
        self.constructor(tag, tag,'element')

    def construct_css(self, tag, data):
        self.constructor(tag, data,'css')

    def construct_payload(self, tag, data):
        self.constructor(tag, data,'payload')

    def constructor(self, tag, data,  typer):
        self.html[tag +'_' + typer + '_'  + str(self.tracker.g_id)] =\
                {'feature': typer.title(), 
                'data':data, 
                'position': self.tracker.position,
                'chart': [x for x in self.tracker.chart],
                'depth': len(self.tracker.chart),
                'g_id': self.tracker.g_id,
                'stack': self.varstack.string }

    def handle_starttag(self, tag, attrs):
        current_ele = tag + '_' + self.tracker.g_id
        self.varstack.add(current_ele)
        self.construct_element(tag)
        self.last_tag = tag

        #css parse
        self.tracker.new_level
        keyval_pair = dict()
        for attr in attrs:
            #add css feature to stack
            self.varstack.add(attr[0] + '_' + self.tracker.g_id)
            keyval_pair[attr[0]] = attr[1]
            #assign stack as 'stack'
            css_tag = join_under([tag, self.tracker.g_id])
            self.construct_css(tag, keyval_pair)
            self.tracker.next
            #remove css feature from stack
            self.varstack.pop
        if tag in SELF_CLOSING_TAGS:
            self.tracker.end_level
            self.stack.pop
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
