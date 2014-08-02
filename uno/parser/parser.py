# -*- coding: utf-8 -*-

from .base_parser   import UnoHTMLParser
from .config        import ParserConfig
from .file_manip    import FileManip
from .source_coder  import SourceCoder

from uno.helpers import combine_dicts

"""
class ParsedObj(object):
    def __init__(self, filename):
        self.filename = filename
        self.source_code = ''
        self.html = ''
        self.parsed_data = {}
"""


class UnoParser(object):

    def __init__(self):
        self.parsed_obj = {}
        self.silent     = False
        self.cleanup    = True
        self.coder      = SourceCoder(self)
        self.files      = FileManip(self)
        self.config     = ParserConfig(self.files)
        self.files.config = self.config
        self.config.update()

    def run(self, **kwargs):
        self.cleanup = kwargs.get('cleanup', True)
        self.silent  = kwargs.get('silent', False)
        self.yell("HTML to Uno Source Code Conversion Running...")
        self.html_to_source()
        self.save_all_sources()


    def add_parser(self, shortname):
        self.parsed_obj[shortname] = UnoHTMLParser(shortname)


    def html_to_source(self):
        if self.check_html_files():
            self.files.check_for_overwriting()
        for file_ in self.files.permitted:
            shortname = self.shortname(file_)
            self.add_parser(shortname)
            self.html_to_data(self.parsed_obj[shortname])
            self.data_to_source(self.parsed_obj[shortname])

    def save_all_sources(self):
        for name in self.parsed_obj.keys():
            code = self.parsed_obj[name].source
            filename = name + '.py'
            self.files.save_source(filename, code)



    def prepare_obj(self, shortname):
        self.parsed_obj[shortname].source_code += self.code.add_utf8()
        self.parsed_obj[shortname].source_code += self.code.add_imports()
        self.parsed_obj[shortname].source_code += self.code.add_python_class(shortname)

    def html_to_data(self, obj):
        obj.parse(self.files.open(self.config.html_folder + obj.html_file))
        obj.data = combine_dicts({},obj.data)

    def data_to_source(self, obj):
        self.yell('Generating source from data...')
        self.coder.generate(obj)
        print self.source_code

    def check_html_files(self):
        self.yell("Searching for *.html files in " + self.config.html_folder)
        if self.files.html_files:
            self.yell("Found html files:", )
            self.yell(self.files.html_files)
            return True
        else:
            self.yell("No html files found for conversion in ", )
            self.yell(self.config.html_folder,)
            self.yell(". Check the config.")
            return False

    def shortname(self, file_):
        return file_[:-5]

    def yell(self, *args):
        if not self.silent:
            for arg in args:
                print arg,


