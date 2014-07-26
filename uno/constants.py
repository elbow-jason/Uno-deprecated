


PAYLOAD = '{PAYLOAD}'
CSS     = '{CSS}'

#Html tag classification attributed to htmldog.com. It's pretty nice. 

FORM_TAGS = ('input', 'form', 'textarea', 'select', 'option', 'optgroup', 
            'button', 'label', 'fieldset', 'legend',)

STRUCTURE_TAGS = ('html', 'head', 'body', 'div', 'span',)

META_TAGS = ('DOCTYPE', 'title', 'link', 'meta', 'style',)

TEXT_TAGS = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 
            'abbr', 'acronym', 'address', 'bdo', 'blockquote', 'cite', 
            'q', 'code', 'ins', 'del', 'dfn', 'kbd', 'pre', 'samp', 'var',
            'br',)

LINK_TAGS = ('a', 'base',)

IMAGE_AND_OBJECTS_TAGS = ('img', 'area', 'map', 'object', 'param',)







SPECIAL_PAYLOAD_TAGS = [('comment', '<!-- {PAYLOAD} -->')]

STATIC_TAGS = [('DOCTYPE', '<!DOCTYPE>')]





SELF_CLOSING_TAGS = ('area', 'base', 'br', 'col', 'command', 'embed', 'hr',
        'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 
        'track', 'wbr')

PAYLOAD_TAGS = ['div', 'p', 'nav', 'html', 'head',
                'label', 'form', 'button', 'textarea', 'select', 'option', 
                'optgroup', 'ul', 'ol', 'li', ] + FORM_TAGS[1:]
