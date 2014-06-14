Stag: HTML templates with pure Python
=====================================

Stag is a Python library that allows you to output HTML by creating a sort of tree in pure Python. Instead of generating HTML with a text-based templating solution like Jinja, we use simple Python objects. A quick example:

```python
def navigation():
    links = [
        ('Home', '/'),
        ('Blog', '/blog')
    ]
    return ul(
        {'id': 'navigation'},
        [
            li(
                a({'href': link[1]}, link[0])
            ) for link in links
        ]
    )
```

Stag has no dependencies (except py.test for testing), and works with Python 2.7+ and 3.3+. It is not considered production-ready yet.


Motivation
----------

(In other words, why would someone be crazy enough to do this?)

Instead of running a preprocessor through a bunch of text files in order to generate our HTML output, Stag uses Python functions as templates. This has several advantages, which I will explain in detail below. What it boils down to, though, is that Stag templates are just regular Python functions that return regular Python objects, which makes them much easier to reason about. There is less magic, it's easier to test, and you have much more flexibility with composition.


Usage
-----

To install:

```python
python setup.py install
```

(It's not on PyPI yet, so no `pip install` unfortunately.)

To use Stag, first import the tags you need:

```python
from stag.tags import a, div, li, ul  # Or you can import * for all tags
```

Each tag is represented by a class that inherits from `stag.base.Element`. Elements can be initialized with child elements in two different ways:

```python
# As arguments to the constructor
div(
    h2("Information"),
    p("Informational text...")
)

# Or as a list of elements
div([
    h2("Information"),
    p("Informational text...")
])
```

The former is preferred, but the latter is useful if you generate the list of children dynamically with a list comprehension:

```python
ul([
    li("Item %s" % i) for i in range(10)
])
```

Stag also supports initializing elements with attributes in two ways:

```python
# As a dictionary passed as the first argument
div(
    {'id': 'content', 'class': 'wide'},
    h2("Information"),
    p("Informational text...")
)

# Or as keyword arguments
div(
    h2("Information"),
    p("Informational text..."),
    id='content',
    class_='wide'
)
```

(Since `class` is a keyword in Python, we use the `class_` keyword argument.)

Either way is fine, but it's important to stay consistent within your application. I personally prefer using a dictionary.

For convenience, Stag supports an attribute called `classes` that allows you to pass in a list of class names instead of a string:

```python
div(classes=['inner', 'wide']) # <div class="inner wide"></div>
```

To turn your template into a string for output, use Stag's helper `render` function:

```python
from stag import render
return render(my_template())
```

Or you can just call `str` on it:

```python
return str(my_template())
```

`render` includes a doctype by default. This can be overridden with a keyword argument:

```python
return render(my_template(), doctype='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
```

To see how all this fits into a web app, see `examples/webapp.py` (must have Flask installed).


Testability
-----------

Because Stag templates are just Python objects, testing them is a piece of cake. Example:

```python
def post(title, text):
    return div(
        {'class': 'post'},
        h2(title),
        p(text)
    )

def test_post():
    assert post("My Test Post", "This is a test post.") == div(
        {'class': 'post'},
        h2("My Test Post"),
        p("This is a test post.")
    )
```

This way, we don't have to write weird workarounds using string checks and other approximations--we can test the output directly! You can see how testing complex functions can be so much easier than testing complex Jinja/Django templates.


Composition
-----------

Since templates are just functions, it's not much easier (and encouraged!) to break your templates down into little pieces. For instance, your general `template` function might look like this:

```python
def template(content):
    return render(
        html(
            head(
                title("My composition example"),
                script(src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js")
            ),
            body(
                navigation(),
                heading(),
                div(
                    {'id': 'content'},
                    content
                ),
                footer()
            )
        )
    )
```

...where `navigation`, `heading`, and `footer` are also functions that return partial templates. And since everything is just a function, you can pass things around as arguments to dynamically generate these partials, without relying on global template variables like Jinja makes you do.
