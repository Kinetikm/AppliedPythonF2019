from app import app
from flask import jsonify, abort, request, g
from marshmallow.exceptions import ValidationError
import validation
import time
from logger_config import LOGGING_CONFIG
import logging.config
from model import Airports, Airplanes, Flights
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

flights_engine = create_engine('sqlite:///flights.db')
flight_schema = validation.FlightSchema()
args_schema = validation.ArgsSchema()
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('RequestLogger')
logger.info('App running')
Session = sessionmaker(bind=flights_engine)


@app.route('/flights', methods=['GET'])
def get_flights():
    args = args_schema.load(request.args)
    session = g.session
    result = session.query(Flights)
    if args['filter_by_airport'] is not None:
        result = session.query(Flights).join(Flights.airport).filter(Airports.airport == args['filter_by_airport'])
    if args['filter_by_plane'] is not None:
        result = session.query(Flights).join(Flights.airplane).filter(Airplanes.airplane == args['filter_by_plane'])
    if args['filter_by_time'] is not None:
        result = session.query(Flights).filter(Flights.dep_time == args['filter_by_time'])
    if args['sort_by'] is not None:
        result = result.order_by(args['sort_by'])
    data = [i.serialize for i in result.all()]
    return jsonify(data)


@app.route('/flights', methods=['POST'])
def post_flight():
    try:
        data = flight_schema.load(request.get_json())
        session = g.session
        airport = session.query(Airports).filter(Airports.airport == data['dest_airport']).first()
        if airport is None:
            airport = Airports(airport=data['dest_airport'])
            session.flush(airport)
        airport_id = airport.id
        airplane = session.query(Airplanes).filter(Airplanes.airplane == data['airplane']).first()
        if airplane is None:
            airplane = Airplanes(airport=data['airplane'])
            session.flush(airplane)
        airplane_id = airplane.id
        h = (data['arr_time'] - data['dep_time']).seconds // 3600
        m = (data['arr_time'] - data['dep_time']).seconds // 60 % 60
        row = Flights(dep_time=data['dep_time'], arr_time=data['arr_time'], airport_id=airport_id,
                      plane_id=airplane_id, flight_time=f'{h}:{m}')
        session.add(row)
        session.commit()
        return 'OK'
    except ValidationError as e:
        abort(400, str(e))


@app.route('/flights/<int:flight_id>/', methods=['GET'])
def get_flight(flight_id):
    session = g.session
    data = session.query(Flights).get(flight_id)
    if data is not None:
        data = data.serialize
    return jsonify(data)


@app.route('/flights/<int:flight_id>/', methods=['DELETE'])
def delete_flight(flight_id):
    session = g.session
    obj = session.query(Flights).get(flight_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    return 'OK'


@app.route('/flights/<int:flight_id>/', methods=['PUT'])
def put_flight(flight_id):
    try:
        data = flight_schema.load(request.get_json())
        session = g.session
        airport = session.query(Airports).filter(Airports.airport == data['dest_airport']).first()
        if airport is None:
            airport = Airports(airport=data['dest_airport'])
            session.flush(airport)
        airport_id = airport.id
        airplane = session.query(Airplanes).filter(Airplanes.airplane == data['airplane']).first()
        if airplane is None:
            airplane = Airplanes(airport=data['airplane'])
            session.flush(airplane)
        airplane_id = airplane.id
        h = (data['arr_time'] - data['dep_time']).seconds // 3600
        m = (data['arr_time'] - data['dep_time']).seconds // 60 % 60
        obj = session.query(Flights).get(flight_id)
        if obj is None:
            row = Airports(dep_time=data['dep_time'], arr_time=data['arr_time'], airport_id=airport_id,
                           plane_id=airplane_id, flight_time=f'{h}:{m}')
            session.add(row)
            session.commit()
        else:
            obj.dep_time = data['dep_time']
            obj.arr_time = data['arr_time']
            obj.airport_id = airport_id
            obj.plane_id = airplane_id
            obj.flight_time = f'{h}:{m}'
            session.commit()
        return 'OK'
    except ValidationError as e:
        abort(400, str(e))


@app.before_request
def before_request():
    g.start = time.time()
    g.session = Session()


@app.after_request
def after_request(response):
    resp_time = (time.time() - g.start) * 1000  # время ответа сервера в миллисекндах
    if 400 <= response.status_code < 500:
        logger.info('%s %s %s %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                    request.json, response.status, response.data, resp_time)
    logger.info('%s %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                response.status, resp_time)
    g.session.close()
    return response
