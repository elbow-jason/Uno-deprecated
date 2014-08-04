# -*- coding: utf-8 -*-

from uno.base import Element, Css, Payload

class RegForm(Element):

    div_0 = Element('element_0', 'div')
    div_0.class_1 = Css('CLASS','form-group')
    div_0.input_4 = Element('element_4', 'input')
    div_0.input_4.ng_model_5 = Css('ng-model','regusername')
    div_0.input_4.type_6 = Css('TYPE','text')
    div_0.input_4.id_7 = Css('id','username')
    div_0.input_4.name_8 = Css('name','username')
    div_0.input_4.class_9 = Css('CLASS','form-control ng-pristine ng-invalid ng-invalid-required')
    div_0.input_4.placeholder_10 = Css('placeholder','Enter Username')
    div_0.input_4.value_11 = Css('value','')
    div_0.input_4.required_12 = Css('required','')
    div_0.input_4.autofocus_13 = Css('autofocus','')