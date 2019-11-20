from flask import request, g, redirect
from flask_jwt_extended import set_access_cookies
from flights_manager import FlightManager, app, Journal, db, Flights, jsonify
import time
import requests

manager = FlightManager()

app.config['JWT_TOKEN_LOCATION'] = ['cookies']

app.config['JWT_ACCESS_COOKIE_PATH'] = '/'

app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret'


@app.errorhandler(405)
def page_not_found(error):
    return 'Method not allowed', 405


@app.route('/registration', methods=['POST'])
def register():
    resp = requests.request(
        method=request.method,
        url='http://localhost:8000/registration',
        headers=request.headers,
        json=request.json
        )
    return (resp.text, resp.status_code, resp.headers.items())


@app.route('/check', methods=['GET'])
def check():
    resp = requests.request(
        method=request.method,
        url='http://localhost:8000/check',
        headers=request.headers,
        json=request.json
        )
    return (resp.text, resp.status_code, resp.headers.items())


@app.route('/login', methods=['POST'])
def login():
    resp = requests.request(
        method=request.method,
        url='http://localhost:8000/login',
        headers=request.headers,
        json=request.json
        )
    return (resp.text, resp.status_code, resp.headers.items())


@app.route('/logout', methods=['GET'])
def logout():
    resp = requests.request(
        method=request.method,
        url='http://localhost:8000/logout',
        headers=request.headers,
        json=request.json
        )
    return (resp.text, resp.status_code, resp.headers.items())


@app.route('/flights', methods=['POST'])
def create_new_flight():
    resp = requests.request(
        method='GET',
        url='http://localhost:8000/check',
        headers=request.headers,
        json=request.json
        )
    return manager.create_flight(request.json, resp.text)


@app.route('/flights/<int:flight_number>', methods=['PUT'])
def edit_flight(flight_number):
    resp = requests.request(
        method='GET',
        url='http://localhost:8000/check',
        headers=request.headers,
        json=request.json
        )
    return manager.edit_flight(flight_number, request.json, resp.text)


@app.route('/flights', methods=['GET'])
def get_flights():
    return manager.get_flights(request.args)


@app.route('/show_performance', methods=['GET'])
def show_performance():
    return manager.show_performance()


@app.route('/flights/<int:flight_number>', methods=['DELETE'])
def delete_flight(flight_number):
    resp = requests.request(
        method='GET',
        url='http://localhost:8000/check',
        headers=request.headers,
        json=request.json
        )
    return manager.delete_flight(flight_number, resp.text)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = (time.time() - g.start) * 1000
    if response.status_code // 100 == 2:
        answer = str(response.status_code) + " OK"
    else:
        if response.data.decode("utf-8")[0] == '"':
            data = response.data.decode("utf-8")[1:-2]
        else:
            data = response.data.decode("utf-8")
        answer = str(response.status_code) + " " + data
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
