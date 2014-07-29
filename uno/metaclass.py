# -*- coding: utf-8 -*-

from uno import helpers, Markup, markup

class UnoElementMetaClass(type):

    data       = None 
    elements   = []
    payload    = ''
    css_dict   = dict()
    posttext   = ''
    pretext    = ''
    pre_payload  = ''
    post_payload = ''
    

    """
        if tag == None:
            self.tag = self.parent_tag_or_div()
        else:
            self.tag    = tag

        self.data       = data 
        self.elements   = elements
        self.payload    = payload
        self.css_dict   = css_dict
        self.posttext   = posttext
        self.pretext    = pretext
        self.pre_payload  = pre_payload
        self.post_payload = post_payload
    """

    #    return super(UnoElement, meta).__new__(meta, name, bases, dct)
    @property
    def css_dict(cls):
        return cls._css_dict

    @css_dict.setter
    def css_dict(cls, value):
        cls._css_dict = value
        cls.css_text

    @property
    def tag(cls):
        return cls._tag

    @tag.setter
    def tag(cls, value, name='_accessible_tag'):
        if not isinstance(value, (basestring)):
            raise Exception('UnoElement tag must be a basestring. {} was not acceptable.'.format(value))
        print "New TAG: ", value
        cls._tag = value
        cls.reset_text_html(cls())

    @property
    def css_text(cls):
        cls._css_text = helpers.ele.kwargs_to_css(cls.css_dict)
        return cls._css_text

    @css_text.setter
    def css_text(cls, value):
        cls._accessible_css_text = value
        cls._css_text = value

    @property
    def render(cls):
        x = str()
        all_payload = cls.pre_payload + cls.payload + cls.post_payload + cls.render_children(cls) 
        x += cls.pretext
        x += cls.text.format(PAYLOAD=all_payload, CSS=cls.css_text)
        x += cls.posttext
        cls._render = Markup(x)
        return cls._render

    @render.setter
    def render(cls, value):
        cls._render = value

    def render_children():
        kids    = ''
        indent  = '    '
        newline = '\n'
        if cls.elements != []:
            for child in cls.elements:
                kids += newline
                kids += indent
                kids += child.render
            kids += newline
        return kids

    def add_css(cls, keywarg):
        cls.css_dict = helpers.combine_dicts(cls.css_dict, keywarg)

    def reset_text_html(cls):
        cls.text = helpers.ele.setup_text_by_tag(cls.tag)

    def parent_tag_or_div(cls):
        return 'div'



    def __repr__(cls):
        return cls.render

    def __str__(cls):
        return cls.render

    def __call__(cls):
        return cls.render

    def __unicode__(cls):
        return unicode(cls.render)

    def __html__(cls):
        return cls.render

    def __init__(cls, tag=None, text=None, elements=[], payload='', posttext='',
                 pretext='', pre_payload='', post_payload='', data=None,
                 css_dict={}, meta_html_type=''):

        cls._accessible_tag = ''
        if tag == None:
            cls.tag = cls.parent_tag_or_div()
        else:
            cls.tag    = tag

        cls.data       = data 
        cls.elements   = elements
        cls.payload    = payload
        cls.css_dict   = css_dict
        cls.posttext   = posttext
        cls.pretext    = pretext
        cls.pre_payload  = pre_payload
        cls.post_payload = post_payload
