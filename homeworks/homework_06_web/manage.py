from flask import Flask, jsonify, request
import data_processing as dp
from os import path
import json
import logging

logging.basicConfig(filename="flight_service.logging", level=logging.INFO)

app = Flask(__name__)


@app.route("/show_flights", methods=["GET"])
def show_flights():
    logging.info("show_flights, output all flights")
    return dp.select_all()


@app.route("/show_flight/<int:id_flight>", methods=["GET"])
def show_flight(id_flight):
    exist, flight = dp.select(id_flight)
    logging.info(
        "show_flight, id_flight = {}: exists = {}".format(
            id_flight, exist))
    if exist:
        return flight
    resp = jsonify(success=False)
    resp.status_code = 400
    return resp


@app.route("/new_flight", methods=["POST"])
def new_flights():
    res = dp.insert(request.json)
    logging.info("new_flight: new id_flight = {}".format(res))
    resp = jsonify(success=res if res else False)
    resp.status_code = 200 if res else 400
    if res:
        resp.message = "id_flight = {}".format(res)
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
        resp = jsonify(success=False)
        resp.message = message
        resp.status_code = 400
    return resp


@app.route("/delete_flight", methods=["DELETE"])
def delete_flights():
    body = request.json
    if "id_flight" not in body:
        return False, '''"id_flight" not scecified in request'''
    res, message = dp.delete(body["id_flight"])
    logging.info(
        "delete_flight, id_flight = {}: result = {}".format(
            body["id_flight"], res))
    if res:
        resp = jsonify(success=True)
        resp.status_code = 200
    else:
        resp = jsonify(success=False)
        resp.message = message
        resp.status_code = 400
    return resp


def start_server():
    if not path.isfile("data.json"):
        with open("data.json", "w", encoding='utf-8') as file:
            json.dump(dict(), file, ensure_ascii=False, indent=4)
    app.run()
