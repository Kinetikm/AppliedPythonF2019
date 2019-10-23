from flask import Flask, request
from flask import jsonify
from my_model import Flights
from my_forms import NewFlight, EditFlight

app = Flask(__name__)


@app.route('/flights/', methods=['GET'])
def get_all_flights():
    return jsonify(Flights.select_all_flights()), 200


@app.route('/flight', methods=['PUT'])
def create_new_flight():
    form = NewFlight()
    if not form.validate():
        return form.errors, 400
    flight = Flights({
        'departure_time': form.departure_time.data,
        'arrival_time': form.arrival_time.data,
        'flight_time': form.flight_time.data,
        'destination_airport': form.destination_airport.data,
    })
    if (not flight.insert()):
        return jsonify({'error': f'Server error, try later'}), 500
    return jsonify(flight.convert_to_dict()), 201


@app.route('/flight/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = Flights.select_by_id(flight_id)
    if not flight:
        return jsonify({'error': f'Fligh with id: {flight_id} not found'}), 404
    flight.delete()
    return ('Deleted', 204)


@app.route('/flight/<int:flight_id>', methods=['POST'])
def edit_flight(flight_id):
    flight = Flights.select_by_id(flight_id)
    if not flight:
        return jsonify({'error': f'Fligh with id: {flight_id} not found'}), 404
    form = EditFlight()
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
    return jsonify(flight.convert_to_dict()), 200

app.run(host='0.0.0.0')
