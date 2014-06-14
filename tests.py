
from stag import render
from stag.tags import *


def test_basic():
    assert str(div({'id': 'main'}, p("Hello"))) == u'<div id="main"><p>Hello</p></div>'
    assert str(div(p("Hello"), id='main')) == u'<div id="main"><p>Hello</p></div>'


def test_render():
    assert render('') == u'<!DOCTYPE html>'


def test_attributes():
    # We have to test against both because we can't guarantee the order of the attributes
    outputs = [u'<div id="main" style="display:none"></div>', u'<div style="display:none" id="main"></div>']
    assert str(div({'id': 'main', 'style': 'display:none'})) in outputs
    assert str(div(id='main', style='display:none')) in outputs


def test_classes():
    assert str(div({'class': 'main'})) == str(div(class_='main')) == u'<div class="main"></div>'
    assert str(div(classes=['content', 'wide'])) == u'<div class="content wide"></div>'
