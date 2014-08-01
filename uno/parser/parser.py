# -*- coding: utf-8 -*-

from .base_parser import UnoBaseHTMLParser
from .config import ParserConfig
from uno.helpers import combine_dicts

class ParsedObj(object):
    def __init__(self, filename):
        self.filename = filename
        self.source_code = ''
        self.html = ''
        self.parsed_data = {}




class UnoParser(UnoBaseHTMLParser):

    def __init__(self):
        super(UnoParser, self).__init__()
        self.parsed_obj = {}
        self.silent = False
        self.cleanup = True

    def run(self, **kwargs):
        self.cleanup = kwargs.get('cleanup', True)
        self.silent  = kwargs.get('silent', False)
        self.yell("HTML to Uno Source Code Conversion Running...")
        self.html_to_source()
        self.save_all_sources()

    def html_to_source(self):
        if self.check_html_files():
            self.files.check_for_overwriting()
        for file_ in self.files.permitted:
            self.add_parsed_obj(file_)
            self.parse_from_file(file_)
            self.parsed_data_to_source(file_)

    def save_all_sources(self):
        for name in self.parsed_obj.keys():
            code = self.parsed_obj[name].source_code
            filename = name + '.py'
            self.files.save_source(filename, code)



    def prepare_obj(self, shortname):
        self.parsed_obj[shortname].source_code += self.code.add_utf8()
        self.parsed_obj[shortname].source_code += self.code.add_imports()
        self.parsed_obj[shortname].source_code += self.code.add_python_class(shortname)


    def parsed_data_to_source(self, file_):
        shortname = self.shortname(file_)
        self.yell('Generating source from data...')
        source_code = self.code.generate(self.parsed_data)
        self.parsed_obj[shortname].source_code += source_code
        print source_code

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

    def add_parsed_obj(self, file_):
        shortname = self.shortname(file_)
        self.parsed_obj[shortname] = ParsedObj(shortname)
        self.prepare_obj(shortname)

    def parse_from_file(self, file_):
        shortname = self.shortname(file_)
        self.parse(self.files.open(self.config.html_folder + file_))
        self.parsed_obj[shortname].parsed_data = combine_dicts({},self.parsed_data)


    def yell(self, *args):
        if not self.silent:
            for arg in args:
                print arg,


