# -*- coding: utf-8 -*-

import os

class Path(object):

    @property
    def html(self):
        return self._html
    @html.setter
    def html(self, value):
        self._html = value
        try:
            self.parent.load_html_files()
        except:
            pass

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, value):
        self._source = value
        try:
            self.parent.load_source_files()
        except:
            pass

    def __init__(self, parent, **kwargs):
        self.parent         = parent
        self.path           = kwargs.get('path', os.getcwd())
        self.html_rel       = kwargs.get('html', '/examples/raw_html/')
        self.source_rel     = kwargs.get('source','/examples/raw_source/')
        self.html           = self.path  + self.html_rel
        self.source         = self.path  + self.source_rel


    def get_path(self):
        return self.path

    def get_html_dir(self):
        return self.rel_html_dir

    def get_source_dir(self):
        return self.rel_source_dir

    def update(self, **kwargs):
        self.html   = kwargs.get('html', self.html)
        self.source = kwargs.get('source', self.source)

