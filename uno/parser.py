

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class HTML(object):
    name = ''
    def __init__(self, name):
        self.name

def remove_newlines(string):
    return string.replace('\n', '')




html = HTML('html')
class UnoParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print "Start tag: ", tag
        html.start_tag = HTML('start_tag')
        for attr in attrs:
            print "Attr: ", attr
            setattr(html.start_tag, 'attrs', attr)

    def handle_endtag(self, tag):
        print "End tag  :", tag
        html.end_tag = tag

    def handle_data(self, data):
        print "Data     :", data
        html.data = data

    def handle_comment(self, data):
        print "Comment  :", data
        html.comment = data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
        html.named_ent = c

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


class UnoParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "     attr:", attr
    def handle_endtag(self, tag):
        print "End tag  :", tag
    def handle_data(self, data):
        print "Data     :", data
    def handle_comment(self, data):
        print "Comment  :", data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data

uno_parser  = UnoParser()
parser      = MyHTMLParser()

import markup

mydiv = markup.div('this here', **dict(id='some_css'))

mydiv = remove_newlines(mydiv)

parser.feed(mydiv)
