# -*- coding: utf-8 -*-

from uno.constants import RESERVED_WORDS_LOWER

class SourceCoder(object):

    def __init__(self, parent):
        self.parent = parent
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
        stack = kwargs.pop('stack', 'unk_ele_name')
        css = kwargs['data']
        for key in css:
            value = css[key]
            key = self.reserved_word_checker(key)
            text += self.css_template.format(stack=stack,
                                             key=key, 
                                             value=value)
        return text


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

    def generate(self, obj):
        text = ''
        for item_name in obj.data:
            text += self.source_funcs[obj.data[item_name]['feature']](**obj.data[item_name])
        self.parent.source_code = text


