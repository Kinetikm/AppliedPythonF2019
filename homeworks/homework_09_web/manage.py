import datetime
import time
import logging
import json
from os import path
import data_processing as dp
from flask import Flask, jsonify, request, g, abort
import requests
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)

app = Flask(__name__)


@app.route("/show_flights", methods=["GET"])
def show_flights():
    sort_by = request.args.get("sort_by")
    filter_field = request.args.get("filter_field", default=None)
    filter_value = request.args.get("filter_value", default=None)
    flag, res = dp.select_all(sort_by, filter_field, filter_value)
    resp = jsonify(result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/show_flight/<int:id_flight>", methods=["GET"])
def show_flight(id_flight):
    flag, res = dp.select_id(id_flight)
    resp = jsonify(result=res)
    resp.status_code = 200 if flag else 400
    return resp


def get_login(cooky):
    resp = requests.request(
        method="POST",
        url="http://localhost:5001/check",
        json=cooky)
    if not resp:
        return None
    return resp.json().get('login', None)


@app.route("/new_flight", methods=["POST"])
def new_flight():
    data = request.json
    login = get_login(request.cookies)
    if login is None:
        abort(403)
    data['login'] = login
    flag, res = dp.insert(data)
    resp = jsonify(result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/update_flight", methods=["PUT"])
def update_flight():
    body = request.json
    if "id_flight" not in body or "flight" not in body:
        abort(400)
    login = get_login(request.cookies)
    if login is None:
        abort(403)
    status, res = dp.update(body["id_flight"], body["flight"], login)
    if status != 200:
        abort(status)
    return jsonify(result=res)


@app.route("/delete_flight", methods=["DELETE"])
def delete_flights():
    body = request.json
    if "id_flight" not in body:
        abort(400)
    login = get_login(request.cookies)
    if login is None:
        abort(403)
    status, res = dp.delete(body, login)
    if status != 200:
        abort(status)
    return jsonify(result=res)


@app.route("/statistic_metrics", methods=["GET"])
def statistic_metrics():
    resp = jsonify(result=dp.statistic_metrics())
    resp.status_code = 200
    return resp


@app.route("/statistic", methods=["GET"])
def statistics():
    resp = jsonify(result=dp.statistic())
    resp.status_code = 200
    return resp


def prepare():
    logging.basicConfig(
        filename="flight_service.logging",
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @app.before_request
    def timer_on():
        g.start_handlefunc = time.time()

    @app.after_request
    def log_request(resp):
        dur = round(time.time() - g.start_handlefunc, 4)
        app.logger.info({
            "url": request.url,
            "args": dict(request.args),
            "body": request.json,
            "req_method": request.method,
            "duration": dur,
            "response": resp.data,
            "http_status": resp.status_code,
            "cookies": request.cookies
        })
        body = json.dumps(request.json)
        url = request.url
        response = str(resp.data)
        response = response if len(
            response) < 1000 else "{}...".format(response[:996])
        dp.set_statistic(
            time.strftime("%H:%M:%S", time.localtime(g.start_handlefunc)),
            url if len(url) < 101 else "{}...".format(url[:97]),
            request.method,
            request.url.split("/")[3].split("?")[0],
            body if body is not None and len(body) < 101 else "{}...".format(body[:497]),
            resp.status_code,
            dur,
            response
        )
        return resp


def start_server():
    prepare()
    app.run()


if __name__ == "__main__":
    start_server()
