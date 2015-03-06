from __future__ import unicode_literals

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def render_html(root, doctype='<!DOCTYPE html>', indent=0):
    doctype_text = doctype + '\n' if doctype else ''
    return doctype_text + render(root, indent=indent)


def render(template, indent=0):
    printer = ElementRenderer(template, indent)
    return printer.render()


class ElementRenderer(object):
    def __init__(self, root, indent=0):
        self.root = root
        self.indent_spaces = indent
        self.indent_level = 0

    def render(self):
        body = StringIO()
        stack = []
        tree = [[self.root]]

        while tree:
            siblings = tree[-1]
            if siblings:
                el = siblings.pop(0)
                stack.append(el)

                if is_string(el):
                    body.write(el)
                else:
                    body.write('<{}'.format(el.tag))
                    if el.attrs:
                        attr_string = ''.join(' {}="{}"'.format(key, val) for key, val in el.attrs.items() if val)
                        body.write(attr_string)

                    if el.self_closing:
                        body.write(' />')
                    else:
                        body.write('>')
                        if el.children:
                            tree.append(el.children)
            else:
                tree.pop()
                el = stack.pop()
                if not is_string(el) and not el.self_closing:
                    body.write('</{}>'.format(el.tag))

        return body.getvalue()


def is_string(val):
    if type('') == str:
        # Python 3
        base = str
    else:
        base = basestring
    return isinstance(val, base)
