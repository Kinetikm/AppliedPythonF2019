#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Airports(Base):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True)
    airport = Column(String, unique=True)


class Aircrafts(Base):
    __tablename__ = 'aircrafts'

    id = Column(Integer, primary_key=True)
    aircraft = Column(String, unique=True)


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure_time = Column(String)
    arrival_time = Column(String)
    travel_time = Column(String)
    destination_airport_id = Column(Integer, ForeignKey('airports.id'))
    type_of_aircraft_id = Column(Integer, ForeignKey('aircrafts.id'))
    airport = relationship("Airports", backref='flights')
    aircraft = relationship("Aircrafts", backref='flights')

    def get_data(self):
        data = {"departure_time": self.departure_time,
                "arrival_time": self.arrival_time,
                "travel_time": self.travel_time,
                "destination_airport": self.airport.airport,
                "type_of_aircraft": self.aircraft.aircraft}
        return data


class LogTable(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    method = Column(String)
    status_code = Column(String)
    duration = Column(Float)
