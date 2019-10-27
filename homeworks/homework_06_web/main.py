from flask import Flask, request, jsonify, g
import time
from flights_manager import FlightManager
from logger_conf import create_logger

app = Flask(__name__)
manager = FlightManager()
logger = create_logger()


@app.route('/flights', methods=['POST'])
def create_new_flight():
    manager.create_flight(request.json)
    return jsonify(manager.get_all_flights()), 201


@app.route('/flights/<int:flight_number>', methods=['PUT'])
def edit_flight(flight_number):
    manager[flight_number].edit_flight(request.json)
    return jsonify(manager.get_all_flights()), 200


@app.route('/flights', methods=['GET'])
def get_flights():
    return jsonify(manager.get_all_flights()), 200


@app.route('/flights/sort', methods=['GET'])
def sort_flights():
    manager.sort_by_flight_duration()
    return jsonify(manager.get_all_flights()), 200


@app.route('/flights/<string:airport>', methods=['GET'])
def get_flights_airport(airport):
    return jsonify(manager.flight_by_airport(airport)), 200


@app.route('/flights/<int:flight_number>', methods=['DELETE'])
def delete_flight(flight_number):
    manager.delete_flight(flight_number)
    return jsonify(manager.get_all_flights()), 200


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = time.time() - g.start
    logger.info(
        f'Request by URL {request.url} using method {request.method}' +
        f' executed with return code {response.status_code} in {diff} seconds')
    return response


if __name__ == '__main__':
    logger.info("Program started")
    app.run(host='0.0.0.0')
    logger.info("Program terminated")
