from flask import Flask, jsonify, request, g, abort, make_response
import data_processing as dp
from os import path
import json
import logging
import time
import datetime
import uuid


app = Flask(__name__)


sessions = {}


@app.route("/registration", methods=["POST"])
def registration():
    flag, res = False, {}
    body = request.json
    pas, pas_confirm = body.get(
        "password", None), body.get(
        "password_confirm", None)
    if pas is not None and pas == pas_confirm:
        flag, res = dp.insert_user(body)
        res = ""
    resp = jsonify(success=flag, result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/login", methods=["POST"])
def login():
    token = dp.new_session(request.json)
    if token:
        resp = make_response()
        resp.set_cookie('token', token)
        return resp
    abort(401)


@app.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token", None)
    if token is not None and dp.finish_session(token):
        res = make_response("Cookie Removed")
        res.set_cookie('token', '', max_age=0)
        return res
    abort(401)


@app.route("/check", methods=["POST"])
def check():
    login = dp.check_session(request.json.get("token", None))
    if login:
        return jsonify(login=login)
    abort(401)


def start_auth_server():
    logging.basicConfig(
        filename="auth.logging",
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @app.after_request
    def log_request(resp):
        app.logger.info({
            "url": request.url,
            "body": request.json,
            "req_method": request.method,
            "response": resp.data,
            "http_status": resp.status_code
        })
        return resp
    app.run(port=5001)


if __name__ == "__main__":
    start_auth_server()
