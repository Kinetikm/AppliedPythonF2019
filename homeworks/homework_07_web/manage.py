from flask import Flask, jsonify, request, g
import data_processing as dp
from os import path
import json
import logging
import time
import datetime

app = Flask(__name__)


@app.route("/show_flights", methods=["GET"])
def show_flights():
    sort_by = request.args.get("sort_by")
    filter_field = request.args.get("filter_field", default=None)
    filter_value = request.args.get("filter_value", default=None)
    flag, res = dp.select_all(sort_by, filter_field, filter_value)
    resp = jsonify(success=flag, result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/show_flight/<int:id_flight>", methods=["GET"])
def show_flight(id_flight):
    flag, res = dp.select_id(id_flight)
    resp = jsonify(success=True, result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/new_flight", methods=["POST"])
def new_flight():
    flag, res = dp.insert(request.json)
    resp = jsonify(success=flag, result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/update_flight", methods=["PUT"])
def update_flight():
    body = request.json
    if "id_flight" not in body or "flight" not in body:
        return False, '''"id_flight" of "flight not scecified in request'''
    flag, res = dp.update(body["id_flight"], body["flight"])
    resp = jsonify(success=flag, result=res)
    resp.status_code = 200 if flag else 400
    return resp


@app.route("/delete_flight", methods=["DELETE"])
def delete_flights():
    body = request.json
    if "id_flight" not in body:
        return False, '''"id_flight" not scecified in request'''
    flag, res = dp.delete(body["id_flight"])
    resp = jsonify(success=flag, result=res)
    resp.status_code = 200 if flag else 400
    return resp


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


def start_server():
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
            "http_status": resp.status_code
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
    app.run()
