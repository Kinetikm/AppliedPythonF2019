#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, g
from schema import valid
from flight import Flight
from initial_data import flights
import logging
import time


app = Flask(__name__)

logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)
file = logging.FileHandler("logger")
file.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s - %(message)s"))
logger.addHandler(file)


@app.before_request
def before():
    g.start = time.time()


@app.after_request
def after(response):
    duration = time.time() - g.start
    logger.info((f"URL: {request.url}, ") +
                (f"method: {request.method}, ") +
                (f"status code: {response.status_code}, ") +
                (f'duration: {"%.4f" % duration} sec'))
    return response


@app.route("/flights", methods=["GET"])
def get_flights():
    return jsonify({"flights": flights}), 200


@app.route("/flights/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    for flight in flights:
        if flight["id"] == flight_id:
            return jsonify({"flight": flight}), 200
    abort(404)


@app.errorhandler(404)
def flight_not_found(error):
    return make_response(jsonify({"error": "flight not found"}), 404)


@app.errorhandler(400)
def valid_error(error):
    return make_response(jsonify({"error": "bad request"}), 400)


@app.route("/flights", methods=["POST"])
def add_flight():
    if not valid.validate(request.json):
        abort(400)
    flight = {"id": flights[-1]["id"] + 1 if flights else 1}
    info_path = Flight(request.json)
    flight.update(vars(info_path))
    flights.append(flight)
    return jsonify({"flight": flight}), 201


@app.route("/flights/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    for flight in flights:
        if flight["id"] == flight_id:
            flights.remove(flight)
            return jsonify({"result": "flight deleted"}), 200
    abort(404)


@app.route("/flights/<int:flight_id>", methods=["PUT"])
def update_flight(flight_id):
    if not valid.validate(request.json):
        abort(400)
    for flight in flights:
        if flight["id"] == flight_id:
            flight["departure_time"] = request.json.get("departure_time", flight["departure_time"])
            flight["arrival_time"] = request.json.get("arrival_time", flight["arrival_time"])
            flight["travel_time"] = request.json.get("travel_time", flight["travel_time"])
            flight["destination_airport"] = request.json.get("destination_airport", flight["destination_airport"])
            flight["type_of_aircraft"] = request.json.get("type_of_aircraft", flight["type_of_aircraft"])
            return jsonify({"flight": flight}), 200


@app.route("/flights/sort_by_departure_time", methods=["GET"])
def sort_by_departure_time():
    return jsonify({"flights": sorted(flights, key=lambda x: x["departure_time"])}), 200


@app.route("/flights/sort_by_arrival_time", methods=["GET"])
def sort_by_arrival_time():
    return jsonify({"flights": sorted(flights, key=lambda x: x["arrival_time"])}), 200


@app.route("/flights/filter_airport:<string:destination_airport>", methods=["GET"])
def filter_by_airport(destination_airport):
    filter_flights = []
    for flight in flights:
        if flight["destination_airport"] == destination_airport:
            filter_flights.append(flight)
    if filter_flights:
        return jsonify({"flights": filter_flights}), 200
    abort(404)


@app.route("/flights/filter_aircraft:<string:type_of_aircraft>", methods=["GET"])
def filter_by_aircraft(type_of_aircraft):
    filter_flights = []
    for flight in flights:
        if flight["type_of_aircraft"] == type_of_aircraft:
            filter_flights.append(flight)
    if filter_flights:
        return jsonify({"flights": filter_flights}), 200
    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
