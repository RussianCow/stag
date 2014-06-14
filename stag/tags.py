import sys

from .base import Element


class el(Element):
    def __init__(self, tag, *children, **attrs):
        self.tag = tag
        Element.__init__(self, *children, **attrs)


def define_simple_tag(tag_name):
    class new_tag(Element):
        tag=tag_name
    new_tag.__name__ = tag_name
    return new_tag


# Does not yet include tags used in Web Components
__all__ = [
    'el',
    'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio',
    'b', 'base', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button',
    'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
    'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'div', 'dl', 'dt',
    'em', 'embed',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html',
    'label', 'legend', 'li', 'link',
    'p', 'param', 'pre', 'progress',
    's', 'samp', 'script', 'section', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup',
    'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
    'u', 'ul',
]

for tag_name in __all__:
    this_module = sys.modules[__name__]
    if not hasattr(this_module, tag_name):
        setattr(sys.modules[__name__], tag_name, define_simple_tag(tag_name))
