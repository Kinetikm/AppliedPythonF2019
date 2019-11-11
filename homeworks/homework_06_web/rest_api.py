#!flask/bin/python
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import jsonify, request, abort, Flask
from flask import make_response

""""Это просто гениальная статейка https://habr.com/ru/post/246699/ работал по ней"""

app = Flask(__name__)
fields = ['Departure(GMT)', 'Arrival(GMT)', 'Travel time', 'Destination', 'Aircraft type']
flights = {
    'flights': [
        {
            'id': 1,
            'Departure(GMT)': 1424,
            'Arrival(GMT)': 612,
            'Travel time': 812,
            'Destination': u'SVO',
            'Aircraft type': u'AA'
        },
        {
            'id': 2,
            'Departure(GMT)': 2000,
            'Arrival(GMT)': 1000,
            'Travel time': 1000,
            'Destination': u'SPV',
            'Aircraft type': u'Boing'
        }
    ]
}  # хранилище полётов


@app.route('/api/flights', methods=['GET'])
def get_flights():
    return jsonify({'flights': flights}), 200


@app.route('/api/flights/<int:flight_id>', methods=['GET'])
def get_flight(flight_id: int):
    marker = False
    for elem in flights['flights']:
        if elem['id'] == flight_id:
            marker = True
            return jsonify({'flight': elem})
    if marker is False:
        abort(404)


@app.route('/api/flights/<int:flight_id>', methods=['PUT'])
def change_flight(flight_id):
    flight_tmp = list(filter(lambda f: f['id'] == flight_id, flights['flights']))[0]
    if len(flight_tmp) == 0:
        abort(404)
    if not request.json:
        abort(400)

    for field in flight_tmp:
        if field in request.json:
            flight_tmp[field] = request.json[field]
    return jsonify({'task': flight_tmp}, {'flights': flights})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/flights', methods=['POST'])
def create_flight():
    if not request.json:
        abort(400)
    print(request.data)
    print(request.json)
    flight_tmp = {'id': flights['flights'][-1]['id'] + 1} if flights['flights'] else {'id': 1}

    for field in fields:
        if field in request.json:
            flight_tmp[field] = request.json[field]
        else:
            abort(400)
    flights['flights'].append(flight_tmp)
    return jsonify(flights['flights']), 201


@app.route('/api/flights/<int:flight_id>', methods=['DELETE'])
def del_flight(flight_id):
    try:
        for index, elem in enumerate(flights['flights']):
            if elem['id'] == flight_id:
                flights['flights'].pop(index)
                return jsonify(flights['flights']), 204

    except IndexError:
        print("IndexError")
        abort(404)


if __name__ == '__main__':
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/logs.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('START')
    app.debug = True
    app.run(host='0.0.0.0')
