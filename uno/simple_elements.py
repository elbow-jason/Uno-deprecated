# -*- coding: utf-8 -*-

from collections import Iterable

from uno import markup, helpers, Markup, constants

from uno.constants import (PAYLOAD, CSS, STATIC_TAGS, NORMAL_TAGS, 
                           ABNORMAL_TAGS, SELF_CLOSING_TAGS,)

PAYLOAD_TAGS = helpers.minus(NORMAL_TAGS, ABNORMAL_TAGS)

class UnoBase(object):
    pass

class UnoGroup(UnoBase):
    """
    An ordered collection of UnoElements. Each element has a group (maybe an
    empty list)
    """

    def set_attr_on_element(self, name, ele_index, value):
        setattr(self.elements[index], name, value)

    def set_attr_on_all_elements(self, name, values, iterate_values=True):
        if isinstance(values, Iterable): 
            if iterate_values:
                if not len(values) == len(self.elements):
                    raise Exception('The passed iterable was not the correct length')
                for i in xrange(len(values)):
                    if not values[i] == False: # eq to 'if value:' but more clear
                        setattr(self.elements[i], name, values[i])
            else: 
                for ele in self.elements:
                    setattr(self, name, values)

    def set_attr_by_element_name(self, ele_name, attr_name, value):
        for element in self.elements:
            if element.name == ele_name:
                setattr(element, attr_name, value)

    def retrieve_elements_properties(self, name):
        attrs = []
        search_for = name[:-1]
        for element in self.elements:
            attrs.append(getattr(element, search_for))
            setattr(self, name, attrs)
        return attrs

    def add_elements_property(self, name, value):
        # create local fget and fset functions
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        # add property to self
        setattr(self.__class__, name, property(fget, fset))
        # add corresponding local variable
        setattr(self, '_' + name, value)

    def _set_property(self, name, value):
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        self.retrieve_elements_properties(name)
        return getattr(self, '_' + name)

    def set_all_group_properties(self):
        self.add_elements_property('pretexts', [])
        self.add_elements_property('posttexts', [])
        self.add_elements_property('payloads', [])
        self.add_elements_property('pre_payloads', [])
        self.add_elements_property('post_payloads', [])


    @property
    def render(self):
        html =  ''
        html += self.pretext
        for child in self.elements:
            html += child.render
        html += self.posttext
        return self._render

    @render.setter
    def render(self, value):
        self._render = value

    def __init__(self, elements=[]):
        self.elements       = elements
        self.pretext  = ''
        self.posttext = ''


class UnoElement(object):

    members = {}

    @property
    def css_dict(self):
        return self._css_dict
    @css_dict.setter
    def css_dict(self, value):
        self.reset_css_text()
        self._css_dict = value

    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, value):
        self._tag = value
        self.reset_text_html()


    @classmethod
    def new(cls, name, tag='div', text=None, elements=None, payload=None, posttext=None,
                 pretext=None, pre_payload=None, post_payload=None, data=None,
                 css_dict=None):
        class newClass(UnoElement):

            @classmethod
            def add_cls_attr(cls, attname, val):
                setattr(cls, attname, val)

        def set_new_attrs(new_class, class_cls, attr_name, local_var, attr_default):
            if local_var:
                new_class.add_cls_attr(attr_name, local_var)
            try:
                cls_attr = getattr(class_cls, attr_name)
                if cls_attr != None:
                    new_class.add_cls_attr(attr_name, cls_attr)
                else:
                    new_class.add_cls_attr(attr_name, attr_default)
            except:
                new_class.add_cls_attr(attr_name, attr_default)


        attrs_to_set = [ ('tag', tag),
                         ('elements', list()), 
                         ('payload',  str()),
                         ('posttext', str()),
                         ('pretext',  str()),
                         ('pre_payload',  str()),
                         ('post_payload', str()),
                         ('data', None),
                         ('css_dict',  dict()),]

        for attr in attrs_to_set:
            set_new_attrs(newClass, cls, attr[0], locals()[attr[0]], attr[1] )
  
        newClass.__name__ = name.title()
        cls.members[name] = dict(name=name,class_obj=newClass)
        return newClass

    @property
    def render(self):
        x = str()
        all_payload = self.pre_payload + self.payload + self.post_payload + self.render_children() 
        x += self.pretext
        x += self.text.format(PAYLOAD=all_payload, CSS=self.css_text)
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
        if self.elements != []:
            for child in self.elements:
                kids += newline
                kids += indent
                kids += child.render
            kids += newline
        return kids

    def reset_css_text(self):
        self.css_text   = helpers.ele.kwargs_to_css(self.css_dict)

    def add_css(self, keywarg):
        self.css_dict = helpers.combine_dicts(self.css_dict, keywarg)


    def reset_text_html(self):
        self.text = helpers.ele.setup_text_by_tag(self.tag)


    def __init__(self, tag='div', text=None, elements=[], payload='', posttext='',
                 pretext='', pre_payload='', post_payload='', data=None,
                 css={}, meta_html_type=''):

        self.tag        = tag
        self.data       = data 
        self.elements   = elements
        self.payload    = payload
        self.css_dict   = css
        self.reset_css_text()
        self.posttext   = posttext
        self.pretext    = pretext
        self.pre_payload  = pre_payload
        self.post_payload = post_payload

    def __repr__(self):
        return self.render

    def __str__(self):
        return self.render

    def __call__(self):
        return self.render

    def __unicode__(self):
        return unicode(self.render)

    def __html__(self):
        return self.render



class UnoElementFactory(object):

    def set_all(self):
        for tag in PAYLOAD_TAGS:
            self.set_new(tag.title(), UnoElement.new(tag, tag, text=self.gen(tag)))
        for tag in SELF_CLOSING_TAGS:
            self.set_new(tag.title(), UnoElement.new(tag, tag, text='<'+ tag +' '+ CSS + ' />'))
        for tag in STATIC_TAGS:
            self.set_new(tag[0].title(), UnoElement.new(tag[0], tag[0], text=tag[1]))

    def set_new(self, tag, element_obj):
        setattr(self, tag, element_obj)

    def from_markup(self, tag):
        return getattr(markup, tag).__call__(PAYLOAD, **dict(replace_me=CSS))

    def gen(self, tag):
        try:
            base_element = self.from_markup(tag)
        except:
            base_element = self.from_markup('div')
            base_element = base_element.replace('div', tag)
        return base_element.replace('replace_me=', '').replace('"', '').replace(' ','')

    def kwargify_element(self, ele):
        idx = ele.find('>')
        return ele[:idx] + " " +  CSS + ele[idx:]

    def pre_payloadify_element(self, ele):
        first_idx = ele.find('<')
        idx = ele.find('<', first_idx)
        return ele[:idx] + " " +  PAYLOAD + ele[idx:]

    #def __init__(self):
    #    self.set_all()

ele = UnoElementFactory()
ele.set_all()
