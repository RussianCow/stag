def render(template, doctype='<!DOCTYPE html>'):
    if type(u'') == str:
        # Python 3
        output = str(template)
    else:
        output = unicode(template)
    return doctype + output
