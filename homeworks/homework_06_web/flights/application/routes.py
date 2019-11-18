from application import app
from flask import jsonify, abort, request, g
from marshmallow.exceptions import ValidationError
from application import validation
import time
from application.logger_config import LOGGING_CONFIG
import logging.config
from models.model import Airports, Airplanes, Flights, Log, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

flights_engine = create_engine('sqlite:///../flights.db')
Base.metadata.create_all(flights_engine)
log_engine = create_engine('sqlite:///log.db')
flight_schema = validation.FlightSchema()
args_schema = validation.ArgsSchema()
metrics_schema = validation.MetricsParamsSchema()
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('RequestLogger')
Session = sessionmaker(bind=flights_engine)
LogSession = sessionmaker(bind=log_engine)


def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db


@app.route('/flights', methods=['GET'])
def get_flights():
    args = args_schema.load(request.args)
    session = get_db()
    if args['filter_by_airport'] is not None:
        result = session.query(Flights).join(Flights.airport).filter(Airports.airport == args['filter_by_airport'])
    elif args['filter_by_plane'] is not None:
        result = session.query(Flights).join(Flights.airplane).filter(Airplanes.airplane == args['filter_by_plane'])
    elif args['filter_by_time'] is not None:
        result = session.query(Flights).filter(Flights.dep_time == args['filter_by_time'])
    else:
        result = session.query(Flights)
    if args['sort_by'] is not None:
        result = result.order_by(args['sort_by'])
    data = [i.serialize for i in result.all()]
    return jsonify(data)


@app.route('/flights', methods=['POST'])
def post_flight():
    try:
        data = flight_schema.load(request.get_json())
        session = get_db()
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
    session = get_db()
    data = session.query(Flights).get(flight_id)
    if data is not None:
        data = data.serialize
    return jsonify(data)


@app.route('/flights/<int:flight_id>/', methods=['DELETE'])
def delete_flight(flight_id):
    session = get_db()
    obj = session.query(Flights).get(flight_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    return 'OK'


@app.route('/flights/<int:flight_id>/', methods=['PUT'])
def put_flight(flight_id):
    try:
        data = flight_schema.load(request.get_json())
        session = get_db()
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


@app.route('/log', methods=['GET'])
def get_log():
    session = LogSession()
    result = session.query(Log).all()
    data = [i.serialize for i in result]
    session.close()
    print(data)
    return jsonify(data)


@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        args = metrics_schema.load(request.args)
        method_type = args['method_type']
        session = LogSession()
        # sqlite не поддерживает percentile_count, поэтому обходимся без него
        req_numb = session.query(func.count(Log.time)).filter(Log.method == method_type).first()[0]
        ofs = req_numb * 0.9 - 1
        data = {'max_time': session.query(func.max(Log.resp_time)).filter(Log.method == method_type).first()[0],
                'min_time': session.query(func.min(Log.resp_time)).filter(Log.method == method_type).first()[0],
                'req_numb': req_numb,
                'avg_time': session.query(func.avg(Log.resp_time)).filter(Log.method == method_type).first()[0],
                'percentiles': session.query(Log.resp_time).order_by(Log.resp_time).filter(
                    Log.method == method_type).limit(1).offset(ofs).first()[0]}
        session.close()
        return jsonify(data)
    except ValidationError as e:
        abort(400, str(e))


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    resp_time = (time.time() - g.start) * 1000  # время ответа сервера в миллисекндах
    d = dict(remote_addr=request.remote_addr, method=request.method, scheme=request.scheme,
             full_path=request.full_path, json=request.json, status=response.status,
             resp_time=resp_time)
    logger.info(msg='', extra=d)
    return response


@app.teardown_appcontext
def teardown_db(args):
    db = g.pop('db', None)

    if db is not None:
        db.close()
