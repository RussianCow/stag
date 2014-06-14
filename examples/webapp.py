from flask import Flask

from stag import render
from stag.tags import *

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def home():
    return template(
        p("This is an example Flask web app.")
    )


def template(content):
    return render(
        html(
            head(
                title("Test web app"),
                script(src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js")
            ),
            body(
                navigation(),
                h1("Greetings, comrade!"),
                div({'id': 'content'}, content)
            )
        )
    )


def navigation():
    links = [
        ('Home', ''),
        ('Blog', ''),
    ]
    return ul(
        {'id': 'navigation'},
        [
            li(
                a({'href': link[1]}, link[0])
            ) for link in links
        ]
    )


if __name__ == '__main__':
    app.run(port=4441)
