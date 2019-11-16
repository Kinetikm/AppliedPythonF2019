#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models import Flights, Airports, Aircrafts, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///database.db')
if __name__ == "__main__":
    flights = [{
            "departure_time": "2019-10-10 23:00",
            "arrival_time": "2019-10-11 12:20",
            "travel_time": "09:20",
            "destination_airport": "Tomsk",
            "type_of_aircraft": "S7",
            "creator": "Ivan"
        },
        {
            "departure_time": "2019-10-11 23:50",
            "arrival_time": "2019-10-12 06:20",
            "travel_time": "09:30",
            "destination_airport": "London",
            "type_of_aircraft": "WizzAir",
            "creator": "Sergei"
    }]
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for flight in flights:
        ap = Airports(airport=flight["destination_airport"])
        ac = Aircrafts(aircraft=flight["type_of_aircraft"])
        session.add(ap)
        session.add(ac)
        session.commit()
        f = Flights(departure_time=flight["departure_time"],
                    arrival_time=flight["arrival_time"],
                    travel_time=flight["travel_time"],
                    creator=flight["creator"],
                    destination_airport_id=ap.id_,
                    type_of_aircraft_id=ac.id_)
        session.add(f)
        session.commit()
    session.close()
