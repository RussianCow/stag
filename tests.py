from __future__ import unicode_literals

import pytest

from stag import render, render_html
from stag.tags import *


def test_basic():
    assert render_basic(div({'id': 'main'}, p("Hello"))) == '<div id="main"><p>Hello</p></div>'
    assert render_basic(div(p("Hello"), id='main')) == '<div id="main"><p>Hello</p></div>'


def test_render():
    """
    Tests the `render()` function.
    """
    assert render_html(div(), doctype='') == render_basic(div())
    assert render_html(div()) == '<!DOCTYPE html>\n<div></div>'


def test_attributes():
    """
    Tests attributes being correctly rendered on elements.
    """
    # We have to test against both because we can't guarantee the order of the attributes
    outputs = ['<div id="main" style="display:none"></div>', '<div style="display:none" id="main"></div>']
    assert render_basic(div({'id': 'main', 'style': 'display:none'})) in outputs
    assert render_basic(div(id='main', style='display:none')) in outputs


def test_classes():
    """
    Tests the `classes` helper attribute on elements.
    """
    assert render_basic(div({'class': 'main'})) == render_basic(div(class_='main')) == '<div class="main"></div>'
    assert render_basic(div(classes=['content', 'wide'])) == '<div class="content wide"></div>'


def test_self_closing():
    """
    Tests to make sure self-closing tags properly raise a ValueError when children are inserted.
    """
    assert render_basic(img(class_='main')) == '<img class="main" />'
    with pytest.raises(ValueError):
        img(p())


def test_integration():
    assert render_html(html(head(), body())) == '<!DOCTYPE html>\n<html><head></head><body></body></html>'


def render_basic(tag):
    return render(tag)
