from flask import Flask, request, Blueprint, g
from flask import jsonify
import app.firstmodule.forms as forms
import app.firstmodule.models as models
from time import time
import logging

module = Blueprint('', __name__)
logger = logging.getLogger('app.controllers')


@module.before_request
def before_request():
    g.start = time()


@module.after_request
def after_request(response):
    processing_time = time() - g.start
    if int(response.status_code / 100) == 2:
        logger.info(f'{request.method} {request.url}.Time: {processing_time}')
    return response


@module.route('/flights/', methods=['GET'])
def get_all_flights():
    return jsonify(models.Flights.select_all_flights()), 200


@module.route('/flights', methods=['POST'])
def create_new_flight():
    form = forms.NewFlight()
    if not form.validate():
        return form.errors, 400
    flight = models.Flights({
        'departure_time': form.departure_time.data,
        'arrival_time': form.arrival_time.data,
        'flight_time': form.flight_time.data,
        'destination_airport': form.destination_airport.data,
    })
    if (not flight.insert()):
        return jsonify({'error': f'Server error, try later'}), 500
    return jsonify(flight.convert_to_dict()), 201


@module.route('/flights/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = models.Flights.select_by_id(flight_id)
    if not flight:
        return jsonify({'error': f'Fligh with id: {flight_id} not found'}), 404
    flight.delete()
    return ('Deleted', 204)


@module.route('/flights/<int:flight_id>', methods=['PUT'])
def edit_flight(flight_id):
    flight = models.Flights.select_by_id(flight_id)
    if not flight:
        return jsonify({'error': f'Fligh with id: {flight_id} not found'}), 404
    form = forms.EditFlight()
    if (not form.validate()):
        return form.errors, 400
    if form.departure_time.data:
        flight.departure_time(form.departure_time.data)
    if form.arrival_time.data:
        flight.arrival_time(form.arrival_time.data)
    if form.flight_time.data:
        flight.flight_time(form.flight_time.data)
    if form.destination_airport.data:
        flight.destination_airport(form.destination_airport.data)
    if (not flight.update()):
        return jsonify({'error': f'Server error, try later'}), 500
    return jsonify(flight.convert_to_dict()), 200
