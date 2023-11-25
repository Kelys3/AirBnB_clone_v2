#!/usr/bin/python3
"""Starts a Flask web app and displays n is even|odd inside the H1 tag BODY"""
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


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
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """displays 'n is a number' only if n is an integer."""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """displays an HTML page only if <n> is an integer."""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """displays an HTML page only if <n> is an integer.
    States whether <n> is odd or even in the body.
    """
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
