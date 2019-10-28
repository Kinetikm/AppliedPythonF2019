import logging
import time
from flask import jsonify, request, abort, Blueprint, g
from app.module.model import flights
from app.module.validation import isvalid

module = Blueprint('', __name__)
controllers_logger = logging.getLogger('app.api')
fields = ['Departure(GMT)', 'Arrival(GMT)', 'Travel time', 'Destination', 'Aircraft type']


@module.before_request
def before_request():
    g.start = time.time()


@module.after_request
def after_request(response):
    diff = time.time() - g.start
    if str(response.status_code)[0] == '2':
        controllers_logger.info(f'Have done the {request.url} with ' + f'{request.method} method for ' +
                                f'{"%.5f" % diff}')
    return response


@module.route('/todo/api/flights', methods=['GET'])
def get_flights():
    return jsonify(flights), 200


@module.route('/todo/api/flights/<int:flight_id>', methods=['PUT'])
def change_flight(flight_id):
    try:
        flight = list(filter(lambda f: f['id'] == flight_id, flights))[0]
        if not request.json:
            abort(400)
        for field in fields:
            if field in request.json and isvalid(field, request.json[field]):
                flight[field] = request.json[field]
            else:
                abort(400)
        return jsonify(flight), 200
    except IndexError:
        abort(404)


@module.route('/todo/api/flights', methods=['POST'])
def create_flight():
    if not request.json:
        abort(400)
    flight = {'id': flights[-1]['id'] + 1} if flights else {'id': 1}
    for field in fields:
        if field in request.json and isvalid(field, request.json[field]):
            flight[field] = request.json[field]
        else:
            abort(400)
    flights.append(flight)
    return jsonify(flight), 201


@module.route('/todo/api/flights/<int:flight_id>', methods=['DELETE'])
def del_flight(flight_id):
    try:
        flight = list(filter(lambda f: f['id'] == flight_id, flights))[0]
        flights.remove(flight)
        return 'Deleted', 204
    except IndexError:
        abort(404)
