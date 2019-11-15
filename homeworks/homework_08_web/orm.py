from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
import datetime
from os import path
from sqlalchemy import create_engine, select, and_
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
import sys
import os

engine = create_engine('sqlite:///database.db')
session = Session(bind=engine)
Base = declarative_base()


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure = Column(String)
    arrival = Column(String)
    travel_time = Column(String)
    airport_id = Column(Integer, ForeignKey('dest_airports.id'))
    aircraft_id = Column(Integer, ForeignKey('aircraft_types.id'))
    airport = relationship("Dest_airports", backref='flights')
    aircraft = relationship("Aircraft_types", backref='flights')

    def deserializ(self):
        result = {
                "departure": self.departure,
                "arrival": self.arrival,
                "travel_time": self.travel_time,
                "destination": self.airport.airport,
                "aircraft_type": self.aircraft.aircraft
                }
        return result


class Dest_airports(Base):
    __tablename__ = 'dest_airports'
    id = Column(Integer, primary_key=True)
    airport = Column(String(70), unique=True, nullable=True)


class Aircraft_types(Base):
    __tablename__ = 'aircraft_types'
    id = Column(Integer, primary_key=True)
    aircraft = Column(String(100), unique=True, nullable=True)


def select_all():
    query = session.query(Flights).all()
    result = []
    for flight in query:
        result.append(flight.deserializ())
    return result, True


def select_by_id(id_):
    query = session.query(Flights).filter(Flights.id == id_).first()
    if flight:
        return query.deserializ(), True
    else:
        None, False


def insert(flight_):
    airport_ = session.query(Dest_airports).filter(Dest_airports.airport == flight_["destination"]).first()
    if not airport_:
        airport_ = Dest_airports(airport=flight_["destination"])
        session.add(airport_)
        session.commit()
    aircraft_ = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight_["aircraft_type"]).first()
    if not aircraft_:
        aircraft_ = Aircraft_types(aircraft=flight_["aircraft_type"])
        session.add(aircraft_)
        session.commit()

    flightdb = Flights(
                    departure=flight_["departure"],
                    arrival=flight_["arrival"],
                    travel_time=flight_["travel_time"],
                    airport_id=airport_.id,
                    aircraft_id=aircraft_.id)
    session.add(flightdb)
    session.commit()
    return True


def delete(id_):
    flightdb = session.query(Flights).filter(Flights.id == id_).first()
    if flightdb:
        session.delete(flightdb)
        session.commit()
        return True
    else:
        return False


def update(id_, flight_):
    airport_ = session.query(Dest_airports).filter(Dest_airports.airport == flight_["destination"]).first()
    if not airport_:
        airport_ = Dest_airports(airport=flight_["departure"])
        session.add(airport_)
        session.commit()
    aircraft_ = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight_["aircraft_type"]).first()
    if not aircraft_:
        aircraft_ = Aircraft_types(aircraft=flight_["aircraft_type"])
        session.add(aircraft_)
        session.commit()

    session.query(Flights).filter(Flights.id == id_).\
        update({Flights.departure: flight_["departure"],
                Flights.arrival: flight_["arrival"],
                Flights.travel_time: flight_["travel_time"],
                Flights.airport_id: aircraft_.id,
                Flights.aircraft_id: aircraft_.id})
    session.commit()
    return True
