import sqlite3
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
conn = sqlite3.connect('database.db')
c = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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
