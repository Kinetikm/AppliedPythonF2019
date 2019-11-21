import uuid
import json
import sys
import datetime
from os import path
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import create_engine, select, and_
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy import Column, Integer, SmallInteger, String, Boolean, Float, Time, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import sys
import os
import psycopg2
engine = create_engine(
    'postgresql+psycopg2://student:student@localhost:5432/flights')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
conn = engine.connect()

def conv_time(i):
    return (
        i[0], str(
            i[1].strftime('%H:%M')), str(
            i[2].strftime('%H:%M')), str(
                i[3].strftime('%H:%M')), i[4], i[5])


def is_valid(entry):
    schema = Flight()
    try:
        schema.load(entry)
        return True
    except ValidationError:
        return False


class destination_airport(Base):
    __tablename__ = 'destination_airport'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    airport = Column(String(50), unique=True, nullable=False)
    airport_flight = relationship('flight', back_populates='flight_airport')

    def __init__(self, airport):
        self.airport = airport

    def __repr__(self):
        return "<destination_airport('%s')>" % (self.airport)


class type_aircraft(Base):
    __tablename__ = 'type_aircraft'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    aircraft = Column(String(50), unique=True, nullable=False)
    aircraft_flight = relationship('flight', back_populates='flight_aircraft')

    def __init__(self, aircraft):
        self.aircraft = aircraft

    def __repr__(self):
        return "<type_aircraft('%s')>" % (self.aircraft)


class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(30), unique=True, nullable=False)
    login = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    users_flight = relationship(
        'flight',
        back_populates='flight_users')
    users_sessions = relationship(
        'sessions',
        back_populates='sessions_users')

    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password


class flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_da = Column(
        SmallInteger,
        ForeignKey('destination_airport.id'),
        nullable=False)
    id_ta = Column(
        SmallInteger,
        ForeignKey('type_aircraft.id'),
        nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time, nullable=False)
    travel_time = Column(Time, nullable=False)
    id_creator = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False)
    flight_airport = relationship(
        'destination_airport',
        back_populates='airport_flight')
    flight_aircraft = relationship(
        'type_aircraft',
        back_populates='aircraft_flight')
    flight_users = relationship(
        'users',
        back_populates='users_flight')

    def __init__(
            self,
            id_da,
            id_ta,
            departure_time,
            arrival_time,
            travel_time,
            id_creator):
        self.id_da = id_da
        self.id_ta = id_ta
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.travel_time = travel_time
        self.id_creator = id_creator

    def __repr__(self):
        return "<flight('%s','%s', '%s, %s, %s, %s)>" % (
            self.id_da,
            self.id_ta,
            self.departure_time,
            self.arrival_time,
            self.travel_time,
            self.id_creator)


class log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    url = Column(String(100), nullable=False)
    method = Column(String(6), nullable=False)
    action = Column(String(20), nullable=False)
    body = Column(String(500))
    response = Column(String(1000))
    http_status = Column(Integer, nullable=False)
    arrival_time = Column(Time, nullable=False)
    duration = Column(Float, nullable=False)

    def __init__(
            self,
            url,
            method,
            action,
            body,
            http_status,
            arrival_time,
            duration,
            resp):
        self.arrival_time = arrival_time
        self.url = url
        self.method = method
        self.action = action
        self.body = body
        self.http_status = http_status
        self.duration = duration
        self.response = resp


class sessions(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, nullable=False)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False,)
    token = Column(String(36), unique=True, nullable=False)
    sessions_users = relationship('users', back_populates='users_sessions')

    def __init__(self, id_user, token):
        self.id_user = id_user
        self.token = token

def clear_base():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def select_all(sort_by, filter_field, filter_value):
    query = session.query(flight, destination_airport, type_aircraft).\
        with_entities(flight.id,
                      flight.departure_time,
                      flight.arrival_time,
                      flight.travel_time,
                      destination_airport.airport,
                      type_aircraft.aircraft).\
        join(destination_airport, destination_airport.id == flight.id_da).\
        join(type_aircraft, type_aircraft.id == flight.id_ta)
    if filter_value is not None:
        if filter_field == 'arrival_time':
            query = query.filter(flight.arrival_time == filter_value)
        if filter_field == "destination_airport":
            query = query.filter(destination_airport.airport == filter_value)
    if sort_by == 'arrival_time':
        query = query.order_by(flight.arrival_time)
    if sort_by == "destination_airport":
        query = query.order_by(destination_airport.airport)
    query = query.all()
    query = [conv_time(i) for i in query]
    return True, query


def select_id(id_flight):
    query = session.query(flight, destination_airport, type_aircraft).\
        with_entities(flight.id,
                      flight.departure_time,
                      flight.arrival_time,
                      flight.travel_time,
                      destination_airport.airport,
                      type_aircraft.aircraft).\
        join(destination_airport, destination_airport.id == flight.id_da).\
        join(type_aircraft, type_aircraft.id == flight.id_ta).\
        filter(flight.id == id_flight).all()
    if len(query) == 0:
        return False, "id doesnt exist"
    return True, conv_time(query[0])


def insert(entry):
    id_da, id_ta, id_creator = None, None, None
    q = session.query(destination_airport).filter(
        destination_airport.airport == entry["destination_airport"]).first()
    if q is not None:
        id_da = q.id
    else:
        da = destination_airport(entry["destination_airport"])
        session.add(da)
        session.flush()
        id_da = da.id
    q = session.query(type_aircraft).filter(
        type_aircraft.aircraft == entry["type_aircraft"]).first()
    if q is not None:
        id_ta = q.id
    else:
        ta = type_aircraft(entry["type_aircraft"])
        session.add(ta)
        session.flush()
        id_ta = ta.id
    session.commit()

    q = session.query(users).filter(
        users.login == entry["login"]).first()
    if q is not None:
        id_creator = q.id
    else:
        return False, ""
    try:
        f = flight(
            id_da,
            id_ta,
            entry['departure_time'],
            entry['arrival_time'],
            entry['travel_time'],
            id_creator
        )
        session.add(f)
        session.flush()
    except BaseException:
        session.rollback()
        return False, 'bad entry, insert canceled'
    res = f.id
    session.refresh(f)
    session.commit()
    return True, res


def update(id_flight, flight_upd, login):
    query = session.query(flight, destination_airport, type_aircraft, users).\
        join(destination_airport, destination_airport.id == flight.id_da).\
        join(type_aircraft, type_aircraft.id == flight.id_ta).\
        join(users, users.id == flight.id_creator).\
        filter(flight.id == id_flight).first()
    if query is not None:
        if query[3].login != login:
            return 403, ""
        try:
            new_da = query[1].id
            if query[1].airport != flight_upd['destination_airport']:
                new_da = session.query(destination_airport). filter(
                    destination_airport.airport == flight_upd['destination_airport']).first()
                if new_da is None:
                    new_da = destination_airport(
                        flight_upd["destination_airport"])
                    session.add(new_da)
                    session.flush()
                new_da = new_da.id
            new_ta = query[2].id
            if query[2].aircraft != flight_upd['type_aircraft']:
                new_ta = session.query(type_aircraft). filter(
                    type_aircraft.aircraft == flight_upd['type_aircraft']).first()
                if new_ta is None:
                    new_ta = type_aircraft(flight_upd["type_aircraft"])
                    session.add(new_ta)
                    session.flush()
                new_ta = new_ta.id

            query = session.query(flight).\
                filter(flight.id == id_flight).\
                update({"departure_time": flight_upd['departure_time'],
                        "arrival_time": flight_upd['arrival_time'],
                        'travel_time': flight_upd['travel_time'],
                        'id_da': new_da,
                        'id_ta': new_ta})
            session.commit()
            return 200, "success"
        except BaseException:
            session.rollback()
    return 400, '''id_flight not exist or flight format not valid'''


def delete(entry, login):
    status, message = 400, "id_flight not exist"
    res = session.query(
        flight,
        users).join(
        users,
        users.id == flight.id_creator).filter(
            flight.id == entry["id_flight"]).first()
    if res is not None:
        if res[1].login != login:
            return 403, "abort: user is not creator of flight"
        status = 200
        message = "success"
        session.delete(res[0])
        session.commit()
    return status, message


def statistic():
    res = [[
        i.arrival_time.strftime('%H:%M:%S'),
        i.url,
        i.method,
        i.action,
        i.body,
        i.response,
        i.http_status,
        i.duration
    ] for i in session.query(log).all()]
    return res


def statistic_metrics():
    q = select([
        log.action,
        func.avg(log.duration).label("avg"),
        func.min(log.duration).label("min"),
        func.count(log.id).label("count"),
        func.percentile_disc(0.9).within_group(log.duration.asc())
    ]).group_by(log.action)
    res = [{
        "action": i[0],
        "avg": i[1],
        "min": i[2],
        "count": i[3],
        "percentile_disc(0.9)": i[4],
    } for i in conn.execute(q)]
    return res


def set_statistic(
        arrival_time,
        url,
        method,
        action,
        body,
        status_code,
        dur,
        resp):
    new_log = log(
        url,
        method,
        action,
        body,
        status_code,
        arrival_time,
        dur,
        resp)
    session.add(new_log)
    session.commit()


def insert_user(data):
    try:
        f = users(data["email"], data["login"], data["password"])
        session.add(f)
        session.commit()
    except BaseException:
        session.rollback()
        return False, 'bad registration'
    return True, "success"


def get_user(login, password):
    return session.query(users).\
        filter(users.login == login and users.password == password).first()


def finish_session(token):
    res = session.query(sessions).filter(sessions.token == token).first()
    success = res is not None
    if success:
        session.delete(res)
        session.commit()
    return success


def new_session(data):
    user = get_user(data['login'], data['password'])
    if user is None:
        return None
    nt = new_token()
    session.add(sessions(user.id, nt))
    session.commit()
    return nt


def new_token():
    return str(uuid.uuid4())


def check_session(token):
    res = session.query(users).join(
        sessions, users.id == sessions.id_user).filter(
        sessions.token == token).first()
    return res.login if res is not None else None

