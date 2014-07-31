from uno.base import Element, Css, Payload

class WorkingPretty(Element):
    div_0 = Element('div_0', 'div')
    div_0.class_1 = Css('CLASS','panel panel-primary')
    div_0.div_4 = Element('div_4', 'div')
    div_0.div_4.class_5 = Css('CLASS','panel-heading')
    div_0.div_4.div_8 = Element('div_8', 'div')
    div_0.div_4.div_8.class_9 = Css('CLASS','row')
    div_0.div_4.div_8.payload_11 = Payload('payload_11', "THIS IS SOME PAYLOAD")
    div_0.a_14 = Element('a_14', 'a')
    div_0.a_14.href_15 = Css('href','#')