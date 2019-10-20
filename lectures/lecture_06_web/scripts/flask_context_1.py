#!/usr/bin/env python
# coding: utf-8

from flask import Flask, g
app = Flask(__name__)

f = open("tmp.txt", "w")


@app.route("/")
def increment():
    f.write("request_1\n")
    return "OK"


@app.teardown_appcontext
def teardown_file(exception):
    f.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8081")
