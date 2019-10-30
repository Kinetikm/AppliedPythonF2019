from flask import Flask, Blueprint, request, abort, jsonify, make_response, g
from flask import request
import app.firstmodule.entities as entities
import app.firstmodule.validation as validation
import time
import logging


module = Blueprint('', __name__)
controllers_logger = logging.getLogger('app.controllers')


@module.before_request
def before_request():
    g.start = time.time()


@module.after_request
def teardown_request(response):
    diff = time.time() - g.start
    if str(response.status_code)[0] == '2':
        controllers_logger.info((f'Have done the {request.url} with ') +
                                (f'{request.method} method for ') +
                                (f'{"%.5f" % diff}'))
    return response


@module.route('/flights', methods=['POST'])
def create_flight():
    try:
        validation.FlightSchema().load(request.json)
        validation.validate_duration(request.json)
    except validation.ValidationError:
        abort(400)
    new_flight = {
        'departure_time': request.json['departure_time'],
        'arrival_time': request.json['arrival_time'],
        'duration': request.json['duration'],
        'arrive_location': request.json['arrive_location'],
        'aircraft_type': request.json['aircraft_type']
    }
    entities.flights.append(entities.Flight(new_flight))
    return jsonify({'flight': new_flight}), 201


@module.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    flight = list(filter(lambda f: f.id == flight_id, entities.flights))
    if len(flight) == 0:
        abort(404)
    return jsonify({'flight': flight[0].convert_to_dict()})


@module.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@module.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@module.route('/flights', methods=['GET'])
def get_flights():
    all_flights = []
    for flight in entities.flights:
        all_flights.append(flight.convert_to_dict())
    return jsonify({'flights': all_flights})


@module.route('/flights/<int:flight_id>', methods=['PUT'])
def change_flight(flight_id):
    flight = list(filter(lambda f: f.id == flight_id, entities.flights))
    if len(flight) == 0:
        abort(404)
    try:
        validation.FlightSchema().load(request.json)
        validation.validate_duration(request.json)
    except validation.ValidationError:
        abort(400)
    flight = flight[0]
    flight.departure_time = request.json['departure_time']
    flight.arrival_time = request.json['arrival_time']
    flight.duration = request.json['duration']
    flight.arrive_location = request.json['arrive_location']
    flight.aircraft_type = request.json['aircraft_type']
    return jsonify({'flight': flight.convert_to_dict()})


@module.route('/flights/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = list(filter(lambda f: f.id == flight_id, entities.flights))
    if len(flight) == 0:
        abort(404)
    flight = flight[0]
    entities.flights.remove(flight)
    return jsonify({'result': 'Successfully delete'})


@module.route('/flights/duration_sorted', methods=['GET'])
def sort_flights_by_duration():
    sorted_flights = sorted(entities.flights, key=lambda flight:
                            flight.duration, reverse=True)
    all_flights = []
    for flight in sorted_flights:
        all_flights.append(flight.convert_to_dict())
    return jsonify({'flights': all_flights})


@module.route('/flights/<string:arrive_location>', methods=['GET'])
def get_dmd_arrival_flights(arrive_location):
    accord_flights = list(filter(lambda flight: flight.arrive_location ==
                                 arrive_location, entities.flights))
    if len(accord_flights) == 0:
        abort(400)
    all_flights = []
    for flight in accord_flights:
        all_flights.append(flight.convert_to_dict())
    return jsonify({'flights': all_flights})
