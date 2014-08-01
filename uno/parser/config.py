# -*- coding: utf-8 -*-

import os

class ParserConfig(object):

    @property
    def html_folder(self):
        return self._html_folder
    @html_folder.setter
    def html_folder(self, value):
        self._html_folder = value
        self.parent.update_html_files()
    
    @property
    def source_folder(self):
        return self._source_folder
    @source_folder.setter
    def source_folder(self, value):
        self._source_folder = value
        self.parent.update_source_files()

    def __init__(self, parent, **kwargs):
        self.parent = parent
        #kwargs follow:
        self.path           = kwargs.get('path', os.getcwd())
        self.parent.path    = self.path
        self.rel_html_dir   = kwargs.get('rel_html_dir', '/examples/raw_html/')
        self.rel_source_dir = kwargs.get('rel_source_dir','/examples/raw_source/')



    def update(self, **kwargs):
        self.parent.not_configured = False
        self.html_folder = kwargs.get('html_folder', self.path + self.rel_html_dir )
        self.source_folder = kwargs.get('source_folder', self.path + self.rel_source_dir)

