# -*- coding: utf-8 -*-

from uno.constants import RESERVED_WORDS_LOWER
from IPython.core.debugger import Tracer

class SourceCoder(object):

    def __init__(self, parent):
        self.parent           = parent
        self.payload_template = "\n    {stack} = Payload('{varname}', \"{data}\")"
        self.css_template     = "\n    {stack} = Css('{key}','{value}')"
        self.element_template = "\n    {stack} = Element('{varname}', '{data}')"
        self.imports_line     = 'from uno.base import Element, Css, Payload\n\n'
        self.python_class_template = 'class {}(Element):\n'
        self.utf8             = "# -*- coding: utf-8 -*-\n\n"
        self.source_funcs = {}
        self.source_funcs['Payload']  = self.payload
        self.source_funcs['Css']      = self.css
        self.source_funcs['Element']  = self.element

    def payload(self, **kwargs):
        kwargs['data'] = self.cleanup_payload(kwargs['data'])
        if kwargs['data'] == '':
            return ''
        return self.payload_template.format(**kwargs)

    def css(self, **kwargs):
        text = ''
        stack = self.pretty_css_stack_name(kwargs)
        print 'KWARGS IS:', kwargs
        #Tracer()() # look at kwargs
        css = kwargs['data']
        for key in css:
            value = css[key]
            key = self.reserved_word_checker(key)
            text += self.css_template.format(stack=stack,
                                             key=key, 
                                             value=value)
        return text

    def pretty_css_stack_name(self, kwargs):
        stack = kwargs.pop('stack', 'unk_ele_name')
        stack = stack.replace('-','_')
        return stack

    def element(self, **kwargs):
        return self.element_template.format(**kwargs)

    def reserved_word_checker(self, attr_name):
        if attr_name in RESERVED_WORDS_LOWER:
            return attr_name.upper()
        else:
            return attr_name

    def add_imports(self):
        return self.imports_line

    def add_classname(self, filename):
        return filename.replace('.html', '').replace('.py', '')\
                .replace('_', ' ').title().replace(' ', '')
    def add_utf8(self):
        return self.utf8

    def add_python_class(self, filename):
        return self.python_class_template.format(self.add_classname(filename))

    def add_headers(self, name):
        text = self.add_utf8()
        text += self.add_imports()
        text += self.add_python_class(name)
        return text

    def cleanup_payload(self, payload):
        """
        Basically, turns payload that looks like '   \\n  ' to ''. In the 
        calling function, if this function returns '' no object is added 
        for that payload.
        """
        p = payload.replace('\n', '')
        p = p.rstrip()
        p = p.lstrip()
        return p

    def process_data(self, name):
        text = ''
        file_ = self.parent.datas[name]
        for item in file_.keys(): #file_ is an entire file's data. iter it.
            data = file_[item]
            #Tracer()() #look at data. 
            text += self.source_funcs[data['feature']](**data)
        return text

    def generate(self, name):
        text = self.add_headers(name)
        counter = 0
        text += self.process_data(name)
        return text


