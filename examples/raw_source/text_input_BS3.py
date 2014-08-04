# -*- coding: utf-8 -*-

from uno.base import Element, Css, Payload

class TextInputBs3(Element):

    div_17 = Element('element_17', 'div')
    div_17.class_18 = Css('CLASS','form-group')
    div_17.label_21 = Element('element_21', 'label')
    div_17.label_21.payload_23 = Payload('payload_23', "Text Input with Placeholder")
    div_17.input_25 = Element('element_25', 'input')
    div_17.input_25.class_26 = Css('CLASS','form-control')
    div_17.input_25.placeholder_27 = Css('placeholder','Enter text')