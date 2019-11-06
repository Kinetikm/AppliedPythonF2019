import time
from app import app
from sqlalchemy import func
from app.db_func import get_all_flights, get_one_flight, add_flight, change_flight, delete_flight, get_all_airports, \
    get_all_aircrafts, write_duration, get_all_queries, get_stat
from app.models import Statistic
from flask import request, abort, jsonify, g
from marshmallow import Schema, fields, validates_schema, ValidationError


class FlightSchema(Schema):
    dept_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M%z')
    arr_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M%z')
    travel_time = fields.Str(required=True)
    airport = fields.Str(required=True)
    aircraft = fields.Str(required=True)

    @validates_schema
    def validate_time(self, flight, **kwargs):
        if flight["dept_time"] > flight["arr_time"]:
            raise ValidationError("Departure time can`t be greater than arrival time")


@app.route('/flights', methods=['GET'])
def get_flights():
    g.type = 0
    records = get_all_flights()
    return jsonify(records)


@app.route('/flights', methods=['POST'])
def index():
    g.type = 1
    schema = FlightSchema()
    data = request.json
    try:
        format_data = schema.load(data)
        add_flight(format_data)
        return "Successfully append"

    except ValidationError as err:
        abort(400, err.messages)


@app.route('/flights/<int:id>', methods=['GET'])
def get_flight(id):
    g.type = 0
    flight = get_one_flight(id)
    if not flight:
        return abort(404)
    return jsonify(flight.in_dict())


@app.route('/flights/<int:id>', methods=['PUT'])
def put_flight(id):
    g.type = 2
    try:
        schema = FlightSchema()
        data = schema.load(request.json)
        change_flight(id, data)
        return "Record changed"
    except ValidationError as err:
        abort(400, err.messages)


@app.route('/flights/<int:id>', methods=['DELETE'])
def del_flight(id):
    g.type = 3
    delete_flight(id)
    return "Record delete"


@app.route('/airports', methods=['GET'])
def get_airports():
    g.type = 0
    records = get_all_airports()
    return jsonify(records)


@app.route('/aircrafts', methods=['GET'])
def get_aircrafts():
    g.type = 0
    records = get_all_aircrafts()
    return jsonify(records)


@app.before_request
def get_req():
    g.get_time = time.time()


@app.after_request
def send_req(resp):
    write_duration(g)
    return resp


@app.route('/queries', methods=['GET'])
def get_query():
    return jsonify(get_all_queries())


@app.route('/min', methods=['GET'])
def min():
    return jsonify(get_stat(func.min))


@app.route('/avg', methods=['GET'])
def avg():
    return jsonify(get_stat(func.avg))


@app.route('/count', methods=['GET'])
def get_count():
    return jsonify(get_stat(func.count))
