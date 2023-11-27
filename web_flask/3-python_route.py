#!/usr/bin/python3
"""Starts a Flask web app and displays "Python" followed by text"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def welcome():
    """display Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def console():
    """display HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """display “C ” followed by the value of the text variable
    (replace underscore _ symbols with a space )"""

    new_text = text.replace('_', ' ')
    return ("C {}".format(new_text))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """ display “Python ”, followed by the value of the text variable
    (replace underscore _ symbols with a space )"""

    p_text = text.replace("_", " ")
    return "Python {}".format(p_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
