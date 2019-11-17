import time
from flight import db
from flight.models import *
from flask import abort


def get_one_flight(id):
    return Flight.query.get(id)


def get_all_flights():
    return [flight.in_dict() for flight in Flight.query.all()]


def add_flight(user_id, body):
    aircraft = Aircraft.query.filter_by(name=body["aircraft"]).first_or_404(
        description='There is no data with {}'.format(body["aircraft"]))
    airport = Airport.query.filter_by(name=body['airport']).first_or_404(
        description='There is no data with {}'.format(body["airport"]))

    flight = Flight.query.filter_by(airport_id=airport.id, aircraft_id=aircraft.id, dept_time=body["dept_time"]).first()
    if flight:
        return flight.in_dict()

    flight = Flight(
        dept_time=body["dept_time"],
        arr_time=body["arr_time"],
        travel_time=body["travel_time"],
        owner=user_id,
        airport_id=airport.id_airport,
        aircraft_id=aircraft.id_aircraft
    )

    db.session.add(flight)
    db.session.commit()


def change_flight(id, user_id, body):
    flight = Flight.query.get(id)

    if not flight:
        abort(404)
    if not flight.check_user(user_id):
        abort(403)

    aircraft = Aircraft.query.filter_by(name=body["aircraft"]).first_or_404(
        description='There is no data with {}'.format(body["aircraft"]))
    airport = Airport.query.filter_by(name=body['airport']).first_or_404(
        description='There is no data with {}'.format(body["airport"]))

    flight.dept_time = body["dept_time"],
    flight.arr_time = body["arr_time"],
    flight.travel_time = body["travel_time"],
    flight.aiport = airport.id,
    flight.aircraft = aircraft.id

    db.session.commit()


def delete_flight(id, user_id):
    flight = Flight.query.get(id)

    if not flight:
        abort(404)
    if not flight.check_user(user_id):
        abort(403)

    flight.delete()


def get_all_airports():
    return [airport.name for airport in Airport.query.all()]


def get_all_aircrafts():
    return [aircraft.name for aircraft in Aircraft.query.all()]


def write_duration(g):
    duration = round(time.time() - g.get_time, 4)
    type = g.pop("type", None)
    if type is None:
        return

    row = Statistic(type=type, time=duration)
    db.session.add(row)
    db.session.commit()


def get_all_queries():
    return [{'Type': query.type, 'Time': float(query.time)} for query in Statistic.query.all()]


def get_stat(f):
    min_0 = db.session.query(f(Statistic.time)).filter(Statistic.type == 0).first()[0]
    min_1 = db.session.query(f(Statistic.time)).filter(Statistic.type == 1).first()[0]
    min_2 = db.session.query(f(Statistic.time)).filter(Statistic.type == 2).first()[0]
    min_3 = db.session.query(f(Statistic.time)).filter(Statistic.type == 3).first()[0]
    return {'GET': float(min_0) if min_0 else 0, 'POST': float(min_1) if min_1 else 0,
            'PUT': float(min_2) if min_2 else 0, 'DELETE': float(min_3) if min_3 else 0}
