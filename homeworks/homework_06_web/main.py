from flask import request, g
from flights_manager import FlightManager, app, Journal, db, Flights
import time

manager = FlightManager()


@app.route('/flights', methods=['POST'])
def create_new_flight():
    return manager.create_flight(request.json)


@app.route('/flights/<int:flight_number>', methods=['PUT'])
def edit_flight(flight_number):
    return manager.edit_flight(flight_number, request.json)


@app.route('/flights', methods=['GET'])
def get_flights():
    return manager.get_flights(request.args)


@app.route('/flights/<int:flight_number>', methods=['DELETE'])
def delete_flight(flight_number):
    return manager.delete_flight(flight_number)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = (time.time() - g.start) * 1000
    if response.status_code // 100 == 2:
        answer = str(response.status_code) + " OK"
    else:
        answer = str(response.status_code) + " " + response.data.decode("utf-8")
    temp = {
        'request_url': request.url,
        'request_method': request.method,
        'status_code': answer,
        'execution_time_in_ms': diff
    }
    log = Journal(**temp)
    db.session.add(log)
    db.session.commit()
    return response


if __name__ == '__main__':
    start = Journal(request_url='', request_method='Program Started', status_code='', execution_time_in_ms=0)
    db.session.add(start)
    db.session.commit()
    app.run(host='0.0.0.0')
    stop = Journal(request_url='', request_method='Program Stopped', status_code='', execution_time_in_ms=0)
    db.session.add(stop)
    db.session.commit()
