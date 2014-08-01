# -*- coding: utf-8 -*-


import os

from config import ParserConfig

class FileManip(object):

    def __init__(self):
        self.permitted = []
        self.not_configured = True

    def configured_check(self):
        if self.not_configured:
            raise Exception("Parser must be confiured. Try uno_parser.configure()")


    def find_files(self, extension, directory):
        return [ f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory,f)) and f.endswith(extension)]

    def update_html_files(self):
        self.configured_check()
        self.html_files = self.find_files('.html', self.config.html_folder)

    def update_source_files(self):
        self.configured_check()
        self.source_files = self.find_files('.py', self.config.source_folder)

    def check_for_overwriting(self):
        print "Checking for potential overwrites..."
        if self.source_files == []:
            print "Source destination folder is empty. \nSkipping checks..."
            return 0
        acceptable = ['y','Y','n','N','all', 'ALL', 'cancel', 'CANCEL']
        self.permitted = self.html_files
        html_names = [f[:-5] for f in self.html_files]
        for source_name in self.source_files:
            print "checking '{}'...".format(source_name),
            if source_name[:-3] in html_names:
                print "found."
                confirm_overwrite = 'unacceptable'
                while not confirm_overwrite in acceptable:
                    confirm_overwrite = raw_input("The file '{}' will be overwritten by this action. OK? ( y/n/yes_all/cancel ): ".format(source_name))
                    if confirm_overwrite in ['n', 'N']:
                        print "The file '{}' will not be overwritten.".format(source_name)
                        self.permitted.pop(self.permitted.index(source_name[:-3]+'.html'))
                    elif confirm_overwrite in ['yes_all', 'YES_ALL']:
                        self.permitted = self.html_files
                        return 0
                    elif confirm_overwrite in ['cancel', 'CANCEL']:
                        self.permitted = []
                        return 0
                    elif confirm_overwrite in ['y', 'Y']:
                        print "The file '{}' will be overwritten.".format(source_name)
                    else:
                        print "Response not understood. Try again."
            else:
                print "not found."

    def save_source(self, filename, data):
        filename = self.config.source_folder + filename
        self.save(filename, data)

    def save(self, filename, data):
        with open(filename, 'w+') as file_:
            file_.write(data)

    def open(self, filename):
        with open(filename, 'r') as file_:
            return file_.read()

