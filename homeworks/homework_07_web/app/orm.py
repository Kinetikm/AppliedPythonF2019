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

Base = declarative_base()
engine = create_engine('sqlite://')
session = Session(bind=engine)


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure = Column(Time)
    arrival = Column(Time)
    travel_time = Column(Time)
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


class ORM():
    def select_all(self):
        query = session.query(Flights).all()
        return query, True

    def select_by_id(self, id_):
        query = session.query(Flights).filter(Flights.id == id_).first()
        if flight:
            return query, True
        else:
            None, False

    def insert(self, flight):
        airport = session.query(Dest_airports).filter(Dest_airports.airport == flight["destination"]).first()
        if not airport:
            airport = Dest_airports(airport=airport_name)
            session.add(airport)
            session.commit()
        aircraft = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight["aircraft_type"]).first()
        if not aircraft:
            aircraft = Aircraft_types(aircraft=aircraft_name)
            session.add(aircraft)
            session.commit()

        flightdb = Flights(
                        departure=flight["departure"],
                        arrival=flight["arrival"],
                        travel_time=flight["travel_time"],
                        airport=flight["destination"],
                        aircraft=flight["aircraft_type"])
        session.add(flight)
        session.commit()
        return True

    def delete(self, id_):
        flightdb = session.query(Flights).filter(Flights.id == id_).first()
        if flight:
            session.delete(flightdb)
            session.commit()
            return True
        else:
            return False

    def update(self, id_, flight):
        airport = session.query(Dest_airports).filter(Dest_airports.airport == flight["destination"]).first()
        if not airport:
            airport = Airports(airport=flight["departure"])
            session.add(airport)
            session.commit()
        aircraft = session.query(Aircraft_types).filter(Aircraft_types.aircraft == flight["aircraft_type"]).first()
        if not aircraft:
            aircraft = Aircrafts(aircraft=flight["aircraft_type"])
            session.add(aircraft)
            session.commit()

        session.query(Flights).filter(Flights.id == id_).\
            update({Flights.departure: flight["departure"],
                    Flights.arrival: flight["arrival"],
                    Flights.travel_time: flight["travel_time"],
                    Flights.airport: flight["destination"],
                    Flights.aircraft: flight["aircraft_type"]})
        session.commit()
        return True

orm = ORM()
