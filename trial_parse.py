from uno.base import Element, Css, Payload


div = Element('element_1', 'div')
element_1.id = Css('id','some_css')
element_1.payload_1 = Payload('payload_1', "Look! It's a payload.")
input = Element('element_3', 'input')
element_3.CLASS = Css('CLASS','form-control btn col-lg-6')