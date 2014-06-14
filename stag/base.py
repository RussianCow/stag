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

    def __unicode__(self):
        body = StringIO()
        if self.attrs:
            attr_string = u' '.join(u'%s="%s"' % (key, val) for key, val in self.attrs.items() if val)
            body.write(u'<%s %s>' % (self.tag, attr_string))
        else:
            body.write(u'<%s>' % self.tag)

        if not self.self_closing:
            # If it's a self-closing tag (<img>, <hr>, etc) there can't be any children anyway
            for child in self.children:
                body.write(str(child))
            body.write(u'</%s>' % self.tag)
        return body.getvalue()

    def __str__(self):
        return self.__unicode__()

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
