from flights_manager import FlightManager
from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = sqlite3.connect('test.db')
c = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Journal(db.Model):
    __tablename__ = 'Journal'
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow, primary_key=True)
    request_url = db.Column(db.String, index=True)
    request_method = db.Column(db.String, index=True)
    status_code = db.Column(db.String)
    execution_time_in_ms = db.Column(db.Float)


class Aircrafts(db.Model):
    __tablename__ = 'Aircrafts'
    name = db.Column(db.String(30), primary_key=True)
    names = db.relationship('Flights')


class Airports(db.Model):
    __tablename__ = 'Airports'
    name = db.Column(db.String(3), primary_key=True)
    names = db.relationship('Flights')


class Flights(db.Model):
    __tablename__ = 'Flights'
    id_ = db.Column(db.Integer, primary_key=True)
    arrival = db.Column(db.String(10))
    departure = db.Column(db.String(10))
    time_in_flight = db.Column(db.String(10))
    username = db.Column(db.String())
    airport = db.Column(db.String(3), db.ForeignKey('Airports.name'))
    aircraft_type = db.Column(db.String(30), db.ForeignKey('Aircrafts.name'))

db.drop_all()
db.create_all()
aircraft = Aircrafts(name='AN28')
db.session.add(aircraft)
aircraft = Aircrafts(name='SU100')
db.session.add(aircraft)
aircraft = Aircrafts(name='SU104')
db.session.add(aircraft)
aircraft = Aircrafts(name='A320')
db.session.add(aircraft)
airport = Airports(name='SVO')
db.session.add(airport)
airport = Airports(name='DMD')
db.session.add(airport)
airport = Airports(name='DIA')
db.session.add(airport)
db.session.commit()

FM = FlightManager(db)
data_true1 = {
            'departure': str(datetime.datetime(2019, 10, 23, 10, 00)),
            'arrival': str(datetime.datetime(2019, 10, 23, 12, 00)),
            'time_in_flight': '2:00',
            'airport': 'SVO',
            'aircraft_type': 'AN28'
        }
data_true2 = {
            'departure': str(datetime.datetime(2019, 10, 23, 10, 00)),
            'arrival': str(datetime.datetime(2019, 10, 23, 12, 00)),
            'time_in_flight': '2:00',
            'airport': 'DMD',
            'aircraft_type': 'SU100'
        }
data_false = {
            'departure': str(datetime.datetime(2019, 10, 23, 10, 00)),
            'arrival': str(datetime.datetime(2019, 10, 23, 12, 00)),
            'time_in_flight': '1:00',
            'airport': 'SVO',
            'aircraft_type': 'AN28'
        }


def test_create_flight():
    assert FM.create_flight(data_false, '{}') == ('You are not logged in', 401)
    assert FM.create_flight(data_false, 'zakhar343') == ('Invalid Input Data', 400)
    assert FM.create_flight(data_true1.copy(), 'zakhar343') == ('OK', 201)


def test_edit_flight():
    assert FM.edit_flight(2, data_false, '{}') == ('You are not logged in', 401)
    assert FM.edit_flight(2, data_false, 'zakhar') == ('No Such Flight', 404)
    assert FM.edit_flight(1, data_false, 'zakhar') == ('Not enough rights to edit this flight', 403)
    assert FM.edit_flight(1, data_false, 'zakhar343') == ('Invalid Input Data', 400)
    assert FM.edit_flight(1, data_true2.copy(), 'zakhar343') == ('OK', 200)


def test_delete_flight():
    assert FM.delete_flight(2, '{}') == ('You are not logged in', 401)
    assert FM.delete_flight(2, 'zakhar') == ('No Such Flight', 404)
    assert FM.delete_flight(1, 'zakhar') == ('Not enough rights to delete this flight', 403)
    assert FM.delete_flight(1, 'zakhar343') == ('OK', 204)


def test_get_flights():
    print(data_true1)
    FM.create_flight(data_true1.copy(), 'zakhar343')
    FM.create_flight(data_true2.copy(), 'zakhar')
    with app.app_context():
        temp = FM.get_flights({})
        assert (temp[0].json, temp[1]) == ([{
            'aircraft_type': 'AN28',
            'airport': 'SVO', 'arrival': '2019-10-23 09:00:00',
            'departure': '2019-10-23 07:00:00',
            'id_': 1, 'time_in_flight': '02:00:00',
            'username': 'zakhar343'
        }, {
            'aircraft_type': 'SU100',
            'airport': 'DMD',
            'arrival': '2019-10-23 09:00:00',
            'departure': '2019-10-23 07:00:00',
            'id_': 2,
            'time_in_flight': '02:00:00',
            'username': 'zakhar'
        }], 200)
        temp = FM.get_flights({'filter_by_airport': 'SVO'})
        assert (temp[0].json, temp[1]) == ([{
            'aircraft_type': 'AN28',
            'airport': 'SVO',
            'arrival': '2019-10-23 09:00:00',
            'departure': '2019-10-23 07:00:00',
            'id_': 1,
            'time_in_flight': '02:00:00',
            'username': 'zakhar343'
        }], 200)
        temp = FM.get_flights({'sort_by': 'time_in_flight'})
        assert (temp[0].json, temp[1]) == ([{
            'aircraft_type': 'AN28',
            'airport': 'SVO',
            'arrival': '2019-10-23 09:00:00',
            'departure': '2019-10-23 07:00:00',
            'id_': 1,
            'time_in_flight': '02:00:00',
            'username': 'zakhar343'
        }, {
            'aircraft_type': 'SU100',
            'airport': 'DMD',
            'arrival': '2019-10-23 09:00:00',
            'departure': '2019-10-23 07:00:00',
            'id_': 2,
            'time_in_flight': '02:00:00',
            'username': 'zakhar'
        }], 200)
        assert FM.get_flights({'new_method': 'exit'}) == ('No Such Method', 405)
