try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from inspect import isgenerator


class Element(object):
    tag = ''
    self_closing = False

    def __init__(self, *children, **attrs):
        if children and isinstance(children[0], dict):
            self.attrs = children[0]
            children = children[1:]
        else:
            self.attrs = attrs

        # Some helpers for the `class` attribute
        if 'classes' in attrs:
            attrs['class'] = ' '.join(c for c in attrs.pop('classes') if c)
        elif 'class_' in attrs:
            attrs['class'] = attrs.pop('class_')

        self.children = []
        self.add_children(children)

    def __call__(self, *children):
        self.add_children(children)
        return self

    def __repr__(self):
        attr_string = ''.join(' {}="{}"'.format(key, val) for key, val in self.attrs.items() if val)
        return '<{}{}>'.format(self.tag, attr_string)

    def add_children(self, children):
        if self.self_closing and children:
            raise ValueError("Self-closing tags can't have children.")
        if children and isgenerator(children[0]):
            children = children[0]
        for child in children:
            if child is not None:
                if isinstance(child, list):
                    self.add_children(child)
                else:
                    self.children.append(child)
