
# -*- coding: utf-8 -*-


from uno.base_elements import base_ele
import uno.css_constants as c

from uno import UnoBaseElement, UnoBaseGroup

DEF_CLASS = c.FORM_CTRL
FIELD_DICT = {c.CLASS: c.FORM_CTRL}

def INPUT(type_of_input):
    return base_ele.Input(css_dict={c.TYPE:type_of_input}).add_css(FIELD_DICT)

def input_text():
    return INPUT('text')

def select():
    return base_ele.Select(css_dict=FIELD_DICT)

def ng_text_input(ng_model_name):
    x = input_text()
    x.add_css({c.NGM: ng_model_name})
    return x

def button():
    x = base_ele.Button()
    x.add_css={c.TYPE:c.BUTTON, c.CLASS: c.BTN}
    return x 

def btn_outline():
    btn = button()
    btn.add_css({c.CLASS: c.BTN_OUTLINE})
    return btn

def btn_out_info():
    x = btn_outline()
    x.add_css({})

    return btn_outline().append_css('class', c.BTN_INFO)

def btn_out_success():
    return btn_outline().append_css('class', c.BTN_SUCCESS)

def option(payload):
    return base_ele.Option(payload=payload)




