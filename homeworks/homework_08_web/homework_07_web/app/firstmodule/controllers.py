from flask import Flask, Blueprint, request, abort, jsonify, make_response, g
from flask import request
import app.firstmodule.validation as validation
import time
import logging
import app.firstmodule.orm_queries as orm_queries
from flask_jwt_extended import jwt_required, get_jwt_identity


module = Blueprint('', __name__)
controllers_logger = logging.getLogger('app.controllers')


@module.before_request
def before_request():
    g.start = time.time()


@module.after_request
def teardown_request(response):
    diff = time.time() - g.start
    controllers_logger.info((f'Query to {request.url}.') +
                            (f'{request.method} method. Answer code is:') +
                            (f'{response.status_code}') +
                            (f'Answer is: {response.json}'))
    orm_queries.add_metric(request, g.start, diff, response.status_code)
    return response


@module.route('/flights', methods=['POST'])
@jwt_required
def create_flight():
    with open('req.txt', 'w') as f:
        f.write(str(request.headers))
    try:
        validation.FlightSchema().load(request.json)
        validation.validate_duration(request.json)
    except validation.ValidationError:
        abort(400)
    current_user = get_jwt_identity()
    orm_queries.add_flight(request, current_user)
    return jsonify({'flight': request.json}), 201


@module.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    try:
        res = orm_queries.get_flight_by_id(flight_id)
    except IndexError:
        abort(404)
    return jsonify({'flight': res})


@module.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@module.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@module.errorhandler(403)
def page_not_found(error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@module.route('/flights', methods=['GET'])
def get_flights():
    res = orm_queries.get_all_flights(request.json)
    return jsonify({'flights': res})


@module.route('/flights/<int:flight_id>', methods=['PUT'])
@jwt_required
def change_flight(flight_id):
    if not request.json:
        abort(400)
    try:
        validation.FlightSchema().load(request.json)
        validation.validate_duration(request.json)
    except validation.ValidationError:
        abort(400)
    flight = orm_queries.get_flight_object(flight_id)
    try:
        flight = flight[0]
    except IndexError:
        abort(404)
    current_user = get_jwt_identity()
    if flight.creator != current_user:
        abort(403)
    try:
        orm_queries.modify_flight(request, flight_id, flight)
    except IndexError:
        abort(400)
    return jsonify({'result': 'Successfully changed'})


@module.route('/flights/<int:flight_id>', methods=['DELETE'])
@jwt_required
def delete_flight(flight_id):
    flight = orm_queries.get_flight_object(flight_id)
    try:
        flight = flight[0]
    except IndexError:
        abort(404)
    current_user = get_jwt_identity()
    if flight.creator != current_user:
        abort(403)
    orm_queries.delete_flight(flight_id)
    return jsonify({'result': 'Successfully delete'})


@module.route('/flights/metrix', methods=['GET'])
def get_metrix():
    metrix = orm_queries.get_metrix(request.json)
    return jsonify({'metrix': metrix})
