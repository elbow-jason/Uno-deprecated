# -*- coding: utf-8 -*-

from uno.base import Element, Css, Payload

class TextInputBs3(Element):

    div_0 = Element('element_0', 'div')
    div_0.class_1 = Css('CLASS','form-group')
    div_0.label_4 = Element('element_4', 'label')
    div_0.label_4.payload_6 = Payload('payload_6', "Text Input with Placeholder")
    div_0.input_8 = Element('element_8', 'input')
    div_0.input_8.class_9 = Css('CLASS','form-control')
    div_0.input_8.placeholder_10 = Css('placeholder','Enter text')