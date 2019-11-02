from flask import Flask, jsonify, request, g
import data_processing as dp
from os import path
import json
import logging
import time

app = Flask(__name__)


@app.route("/show_flights", methods=["GET"])
def show_flights():
    sort_by = request.args.get("sort_by")
    filter_field = request.args.get("filter_field", default=None)
    filter_value = request.args.get("filter_value", default=None)
    resp = jsonify(
        success=True,
        result=dp.select_all(
            sort_by,
            filter_field,
            filter_value))
    return resp


@app.route("/show_flight/<int:id_flight>", methods=["GET"])
def show_flight(id_flight):
    exist, flight = dp.select(id_flight)
    if exist:
        resp = jsonify(success=True, flight=flight)
        resp.status_code = 200
    else:
        resp = jsonify(success=False)
        resp.status_code = 400
    return resp


@app.route("/new_flight", methods=["POST"])
def new_flight():
    res = dp.insert(request.json)
    if res is not None:
        resp = jsonify(success=True, id_flight=res)
        resp.status_code = 200
    else:
        resp = jsonify(success=False)
        resp.status_code = 400
    return resp


@app.route("/update_flight", methods=["PUT"])
def update_flight():
    body = request.json
    if "id_flight" not in body or "flight" not in body:
        return False, '''"id_flight" of "flight not scecified in request'''
    result, message = dp.update(body["id_flight"], body["flight"])
    if result:
        resp = jsonify(success=True)
        resp.status_code = 200
    else:
        resp = jsonify(success=False, message=message)
        resp.status_code = 400
    return resp


@app.route("/delete_flight", methods=["DELETE"])
def delete_flights():
    body = request.json
    if "id_flight" not in body:
        return False, '''"id_flight" not scecified in request'''
    res, message = dp.delete(body["id_flight"])
    if res:
        resp = jsonify(success=True)
        resp.status_code = 200
    else:
        resp = jsonify(success=False, message=message)
        resp.status_code = 400
    return resp


def start_server():
    if not path.isfile("data.json"):
        with open("data.json", "w", encoding='utf-8') as file:
            json.dump(dict(), file, ensure_ascii=False, indent=4)

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
            "response": resp,
            "http_status": resp.status_code
        })
        return resp
    app.run()
