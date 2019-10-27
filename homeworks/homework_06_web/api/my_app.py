from flask import Flask, request, abort, jsonify, g
import api.model.FlightScheme as scheme
import api.model.FlightRecords as records
import time
import logging

app = Flask(__name__)
app_log = logging.getLogger("api.my_app")


@app.before_request
def before_req():
    g.start_req = time.time()


@app.after_request
def after_req(responce):
    delta = time.time() - g.start_req
    if str(responce.status_code)[0] == '2':
        app_log.info(f'{request.url} done using {request.method} for {delta}')
    return responce


@app.route('/api/flights', methods=['GET'])
def get_flights():
    all_flights_temp = []
    for flight in records.all_flights:
        all_flights_temp.append(flight.converted())
    return jsonify({'flights': all_flights_temp})


@app.route('/api/flights/dep_time_sort', methods=['GET'])
def sort_by_dep_time():
    all_flights_sort = sorted(records.all_flights, key=lambda rec: rec.dep_time)
    all_flights_sort = [flight.converted() for flight in all_flights_sort]
    return jsonify({'flights': all_flights_sort})


@app.route('/api/flights', methods=['POST'])
def create_record():
    try:
        scheme.FlightPlan().load(request.json)
        scheme.validates_time(request.json)
    except scheme.ValidationError:
        abort(400)
    new_record = {
        'dep_time': request.json['dep_time'],
        'arr_time': request.json['arr_time'],
        'dur_time': request.json['dur_time'],
        'arr_locate': request.json['arr_locate'],
        'aircraft_type': request.json['aircraft_type']
    }
    records.all_flights.append(records.Flight(new_record))
    return jsonify({'flight': new_record}), 201


@app.route('/api/flights/<int:flight_id>', methods=['PUT'])
def change_flight(flight_id):
    flight = list(filter(lambda f: f.id == flight_id, records.all_flights))
    if not flight:
        abort(404)
    try:
        scheme.FlightPlan().load(request.json)
        scheme.validates_time(request.json)
    except scheme.ValidationError:
        abort(404)
    flight = flight[0]
    flight.dep_time = request.json['dep_time']
    flight.arr_time = request.json['arr_time']
    flight.dur_time = request.json['dur_time']
    flight.arr_locate = request.json['arr_locate']
    flight.aircraft_type = request.json['aircraft_type']
    return jsonify({'flights': flight.converted()})


@app.route('/api/flights/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = list(filter(lambda f: f.id == flight_id, records.all_flights))
    if not flight:
        abort(404)
    flight = flight[0]
    records.all_flights.remove(flight)
    return jsonify({'result': 'Successfull delete'})


if __name__ == '__main__':
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('api.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("Start Program")
    app.run()
