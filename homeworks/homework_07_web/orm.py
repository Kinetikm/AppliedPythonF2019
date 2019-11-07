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

engine = create_engine('sqlite:///:memory:')
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


class Dest_airports(Base):
    __tablename__ = 'dest_airports'
    id = Column(Integer, primary_key=True)
    airport = Column(String(70), unique=True, nullable=True)


class Aircraft_types(Base):
    __tablename__ = 'aircraft_types'
    id = Column(Integer, primary_key=True)
    aircraft = Column(String(100), unique=True, nullable=True)


def select_all(self):
    query = session.query(Flights).all()
    return query, True


def select_by_id(id_):
    query = session.query(Flights).filter(Flights.id == id_).first()
    if flight:
        return query, True
    else:
        None, False


def insert(flight_):
    airport = session.query(Dest_airports).filter(Dest_airports.airport == flight_["destination"]).first()
    if not airport:
        airport = Dest_airports(airport=airport_name)
        session.add(airport)
        session.commit()
    aircraft = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight_["aircraft_type"]).first()
    if not aircraft:
        aircraft = Aircraft_types(aircraft=aircraft_name)
        session.add(aircraft)
        session.commit()

    flightdb = Flights(
                    departure=flight_["departure"],
                    arrival=flight_["arrival"],
                    travel_time=flight_["travel_time"],
                    airport=flight_["destination"],
                    aircraft=flight_["aircraft_type"])
    session.add(flight_)
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
    airport = session.query(Dest_airports).filter(Dest_airports.airport == flight_["destination"]).first()
    if not airport:
        airport = Airports(airport=flight_["departure"])
        session.add(airport)
        session.commit()
    aircraft = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight_["aircraft_type"]).first()
    if not aircraft:
        aircraft = Aircrafts(aircraft=flight_["aircraft_type"])
        session.add(aircraft)
        session.commit()

    session.query(Flights).filter(Flights.id == id_).\
        update({Flights.departure: flight_["departure"],
                Flights.arrival: flight_["arrival"],
                Flights.travel_time: flight_["travel_time"],
                Flights.airport: flight_["destination"],
                Flights.aircraft: flight_["aircraft_type"]})
    session.commit()
    return True
