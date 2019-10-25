#!flask/bin/python
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import jsonify, request, abort, Flask
from model import flights
from validation import isvalid

app = Flask(__name__)
fields = ['Departure(GMT)', 'Arrival(GMT)', 'Travel time', 'Destination', 'Aircraft type']


@app.route('/todo/api/flights', methods=['GET'])
def get_flights():
    return jsonify(flights), 200


@app.route('/todo/api/flights/<int:flight_id>', methods=['PUT'])
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


@app.route('/todo/api/flights', methods=['POST'])
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


@app.route('/todo/api/flights/<int:flight_id>', methods=['DELETE'])
def del_flight(flight_id):
    try:
        flight = list(filter(lambda f: f['id'] == flight_id, flights))[0]
        flights.remove(flight)
        return 'Deleted', 204
    except IndexError:
        abort(404)


if __name__ == '__main__':
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)  # Маленький логгер, который фиксирует старт сервера =)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
    app.debug = True
    app.run(host='0.0.0.0')
