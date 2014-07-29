# -*- coding: utf-8 -*-

import copy
import uno.css_constants as c




class ElementQuickAdder(object):

    def __init__(self, parent_obj):
        self.element = parent_obj

    def ng_model(self, info):
        self.element.add_css({c.NGM: info})

    def name(self, info):
        self.element.add_css({c.NAME: info})




class GroupQuickAdder(object):

    def verifier(self, ele_name):
        for ele_obj in self.group.elements:
            if ele.name == ele_name:
                ver = copy.copy(ele_obj)
                ver.add_css({c.NAME : self.ele_obj.css_dict[c.NAME] + c._CONFIRM })
                ver.add_css({c.EQ : ele_obj.css_dict[c.NGM]})
                ele_obj.add_css({c.EQ : ver.css_dict[c.NAME]})


    def __init__(self, parent_obj):
        self.group = parent_obj



