from flight_entity import Flight
from numpy import percentile
from sqlalchemy import update, func
from sqlalchemy.sql import text
from create_db import db, app, Flights, Airports, Aircrafts, Journal, jsonify


class FlightManager():
    def __init__(self):
        pass

    def create_flight(self, input_value, user):
        if user[0] == '{':
            return 'You are not logged in', 401
        try:
            temp = Flight(input_value)
        except ValueError:
            return 'Invalid Input Data', 400
        else:
            res = temp.get_flight_info()
            flight = Flights(**res, username=user)
            db.session.add(flight)
            db.session.commit()
            return 'OK', 201

    def delete_flight(self, flight_number, user):
        if user[0] == '{':
            return 'You are not logged in', 401
        rows = db.session.query(Flights).filter(Flights.id_ == flight_number).count()
        if rows == 0:
            return 'No Such Flight', 404
        rows = db.session.query(Flights).filter(Flights.id_ == flight_number).filter(Flights.username == user).count()
        if rows == 0:
            return 'Not enough rights to delete this flight', 403
        temp = Flights.query.filter_by(id_=flight_number).delete()
        db.session.commit()
        return 'OK', 204

    def edit_flight(self, flight_number, input_value, user):
        if user[0] == '{':
            return 'You are not logged in', 401
        rows = db.session.query(Flights).filter(Flights.id_ == flight_number).count()
        if rows == 0:
            return 'No Such Flight', 404
        rows = db.session.query(Flights).filter(Flights.id_ == flight_number).filter(Flights.username == user).count()
        if rows == 0:
            return 'Not enough rights to edit this flight', 403
        try:
            temp = Flight(input_value)
        except ValueError:
            return 'Invalid Input Data', 400
        else:
            res = temp.get_flight_info()
            db.session.execute(update(Flights).where(Flights.id_ == flight_number).values(**res))
            db.session.commit()
            return 'OK', 200

    def get_flights(self, params):
        lst = []
        if 'sort_by' in params:
            temp = params['sort_by']
            for u in db.session.query(Flights).order_by(text(f'Flights.{temp}')).all():
                a = u.__dict__
                del a['_sa_instance_state']
                lst.append(a)
            return jsonify(lst), 200
        elif 'filter_by_airport' in params:
            temp = params['filter_by_airport']
            for u in db.session.query(Flights).filter(Flights.airport == temp).all():
                a = u.__dict__
                del a['_sa_instance_state']
                lst.append(a)
            return jsonify(lst), 200
        elif len(params) == 0:
            for u in db.session.query(Flights).all():
                a = u.__dict__
                del a['_sa_instance_state']
                lst.append(a)
            return jsonify(lst), 200
        elif 1:
            return 'No Such Method', 405

    def show_performance(self):
        main_dict = {}
        for i in ('GET', 'PUT', 'DELETE', 'POST'):
            temp_dict = {}
            main_dict[i] = temp_dict
            u = db.session.query(
                func.avg(Journal.execution_time_in_ms)).filter(Journal.request_method == i).scalar()
            temp_dict['average_time'] = u
            u = db.session.query(
                func.min(Journal.execution_time_in_ms)).filter(Journal.request_method == i).scalar()
            temp_dict['minimal_time'] = u
            u = db.session.query(
                Journal.execution_time_in_ms).filter(Journal.request_method == i).count()
            temp_dict['number_of_requests'] = u
            lst = [u[0] for u in db.session.query(
                Journal.execution_time_in_ms).filter(Journal.request_method == i).all()]
            temp_dict['percentile'] = percentile(lst, 90)
        return jsonify(main_dict), 200
