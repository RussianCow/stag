from stag import render
from stag.tags import *


def test_basic():
    assert str(div({'id': 'main'}, p("Hello"))) == u'<div id="main"><p>Hello</p></div>'
    assert str(div(p("Hello"), id='main')) == u'<div id="main"><p>Hello</p></div>'


def test_render():
    assert render('') == u'<!DOCTYPE html>'
