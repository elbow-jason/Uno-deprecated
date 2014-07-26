# -*- coding: utf-8 -*-

from uno import markup
from uno import helpers
from uno import Markup




class UnoBase(object):
    self.children   = []
    self.posttext   = ''
    self.pretext    = ''


class UnoCollection(UnoBase):
    """
    An ordered collection of UnoElements.
    """
    @property
    def posttexts(self):
        x = (x for x in self.children.posttexts)
        self._posttexts = x
        return self._posttexts

    @posttexts.setter
    def posttexts(self, value):
        self._posttexts = value

    @property
    def render(self):
        html =  '\n'
        html += self.pretext
        for child in children:
            html += child.render
        html += self.posttext
        return self._render

    @render.setter
    def render(self, value):
        self._render = value
    
    @property
    def payloads(self):
        self._payloads = (x.payload for x in self.children)
        return self._payloads

    @payloads.setter
    def payloads(self, value):
        self._payloads = value

    def __init__(self, ):
        payloads = tuple()
        children = []
        pretext  = ''
        posttexts = tuple()



class UnoElement(object):
    self.text       = text
    self.children   = []
    self.payload    = ''
    self.css_kwargs = dict()
    self.css_text   = self.kwargs_to_css()
    self.posttext   = ''
    self.pretext    = ''

    @property
    def render(self):
        payload = self.payload  + self.render_children() 
        x += self.pretext
        x += self.text.format(PAYLOAD=payload, CSS=self.css_text)
        x += self.posttext
        self._render = Markup(x)
        return self._render

    @render.setter
    def render(self, value):
        self._render = value

    def render_children(self):
        kids    = ''
        indent  = '    '
        newline = '\n'
        for child in self.children:
            kids += newline
            kids += indent 
            kids += child.render
        kids += newline
        return kids


    def kwarg_to_css(self, kwarg_tuple):
        return " {}={}".format(kwarg_tuple[0], kwarg_tuple[1])

    def add_css_kwarg(self, keywarg):
        self.css_kwargs = helpers.combine_dicts(self.css_kwargs, keywarg)
        self.kwargs_to_css()

    def kwargs_to_css(self):
        attrs = ''
        for bi_tup in self.css_kwargs.items():
            new = stringify_kwarg(bi_tup)
            print 'new ' + new
            attrs += new
        return attrs

    def __init__(self, text, children=[], payload='', posttext='',
                 pretext='', **kwargs):

        self.text       = text
        self.children   = children
        self.payload    = payload
        self.css_kwargs = kwargs
        self.css_text   = self.kwargs_to_css()
        self.posttext   = posttext
        self.pretext    = pretext

    def __repr__(self):
        return self.render

    def __str__(self):
        return self.render

    def __call__(self):
        return self.render

    def __unicode__(self):
        return unicode(self.render)

    def __html__(self):
        self.__unicode__()


class ElementsFactory(object):
    payload_tags      = PAYLOAD_TAGS
    self_closing_tags = SELF_CLOSING_TAGS
    special_tags      = SPECIAL_TAGS

    def set_all(self):
        for tag in self.payload_tags:
            setattr(self, tag, Element(self.gen(tag)))
        for tag in self.self_closing_tags:
            setattr(self, tag, '<'+ tag +' '+ CSS + ' \>')
        for tag in self.special_tags:


    def from_markup(self, tag):
        return getattr(markup, tag).__call__(PAYLOAD, **dict(replace_me=CSS))

    def gen(self, tag):
        try:
            base_element = self.from_markup(tag)
        except:
            base_element = self.from_markup('div')
            base_element = base_element.replace('div', tag)
        return base_element.replace('replace_me=', '').replace("\"", '').replace(' ','')

    def kwargify_element(self, ele):
        idx = ele.find('>')
        return ele[:idx] + " " +  CSS + ele[idx:]

    def pre_payloadify_element(self, ele):
        first_idx = ele.find('<')
        idx = ele.find('<', first_idx)
        return ele[:idx] + " " +  PAYLOAD + ele[idx:]


ele = ElementsFactory()
ele.set_all()
