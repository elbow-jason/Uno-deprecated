# -*- coding: utf-8 -*-


import os

from .path          import Path

class FileManip(object):

    def __init__(self, parent):
        self.permitted  = []
        self.parent     = parent
        self.path       = Path(self)
        self.path.update()
        self.load_html_files()
        self.load_source_files()

    def find_files(self, extension, directory):
        return [ f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory,f))
            and f.endswith(extension)]

    def load_html_files(self):
        self.html_list = self.find_files('.html', self.path.html)
        for file_ in self.html_list:
            shortname = file_[:-5]
            print 'loaded:', file_
            print 'in html_files as', shortname
            self.parent.htmls[shortname] = self.open(self.path.html + file_)

    def load_source_files(self):
        self.source_list = self.find_files('.py', self.path.source)

    def check_for_overwriting(self):
        print "Checking for potential overwrites..."
        if self.source_files == []:
            print "Source destination folder is empty. \nSkipping checks..."
            return 0
        acceptable = ['y','Y','n','N','all', 'ALL', 'cancel', 'CANCEL']
        self.permitted = self.html_list
        html_names = [f[:-5] for f in self.html_files]
        for source_name in self.source_list:
            print "checking '{}'...".format(source_name),
            if source_name[:-3] in html_names:
                print "found."
                confirm_overwrite = 'unacceptable'
                while not confirm_overwrite in acceptable:
                    confirm_overwrite = raw_input("The file '{}' will be\
                            overwritten by this action. OK? (\
                            y/n/yes_all/cancel ): ".format(source_name))
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

    def save_source(self, name, data):
        filename = self.path.source + name + '.py'
        self.save(filename, data)

    def save(self, filename, data):
        with open(filename, 'w+') as file_:
            print 'saving:', filename
            file_.write(data)

    def open(self, filename):
        with open(filename, 'r') as file_:
            return file_.read()

