import pytest

from stag import render
from stag.tags import *


def test_basic():
    assert str(div({'id': 'main'}, p("Hello"))) == u'<div id="main"><p>Hello</p></div>'
    assert str(div(p("Hello"), id='main')) == u'<div id="main"><p>Hello</p></div>'


def test_render():
    """
    Tests the `render()` function.
    """
    assert render(div(), doctype='') == str(div())
    assert render(div()) == u'<!DOCTYPE html><div></div>'


def test_attributes():
    """
    Tests attributes being correctly rendered on elements.
    """
    # We have to test against both because we can't guarantee the order of the attributes
    outputs = [u'<div id="main" style="display:none"></div>', u'<div style="display:none" id="main"></div>']
    assert str(div({'id': 'main', 'style': 'display:none'})) in outputs
    assert str(div(id='main', style='display:none')) in outputs


def test_classes():
    """
    Tests the `classes` helper attribute on elements.
    """
    assert str(div({'class': 'main'})) == str(div(class_='main')) == u'<div class="main"></div>'
    assert str(div(classes=['content', 'wide'])) == u'<div class="content wide"></div>'


def test_self_closing():
    """
    Tests to make sure self-closing tags properly raise a ValueError when children are inserted.
    """
    assert str(img(class_='main')) == u'<img class="main">'
    with pytest.raises(ValueError):
        img(p())
