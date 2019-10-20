#!/usr/bin/env python
# coding: utf-8

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


# TODO Добавить рутинги /goodbye


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8081")
