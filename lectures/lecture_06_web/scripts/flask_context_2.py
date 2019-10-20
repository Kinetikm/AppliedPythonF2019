#!/usr/bin/env python
# coding: utf-8

from flask import Flask, g
app = Flask(__name__)


def get_descr():
    f = getattr(g, '_descr', None)
    if f is None:
        f = g._descr = open("tmp.txt", "w")
    return f


@app.route("/")
def increment():
    f = get_descr()
    f.write("request_1\n")
    return "OK"


@app.teardown_appcontext
def teardown_file(exception):
    f = getattr(g, '_database', None)
    if f is not None:
        f.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8081")
