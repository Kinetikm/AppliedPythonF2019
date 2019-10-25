import json
from flask import Flask, request, abort
from database import *
from marshmallow import Schema, fields, validates_schema, ValidationError

app = Flask(__name__)


@app.route('/flights', methods=['GET'])
def get_flights():
    records = get_all_flight()
    return json.dumps(records)


class FlightSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    dept_time = fields.Time(required=True)
    arr_time = fields.Time(required=True)
    travel_time = fields.Time(required=True)
    airport = fields.Str(required=True)
    type = fields.Str(required=True)

    @validates_schema
    def validate_time(self, flight, **kwargs):
        if flight["dept_time"] > flight["arr_time"]:
            raise ValidationError("Departure time can`t be greater than arrival time")


@app.route('/flights', methods=['POST'])
def index():
    schema = FlightSchema()
    data = request.json
    try:
        format_data = schema.load(data)
        if 'id' not in format_data:
            raise ValidationError("{'id': ['Missing data for required field.']}")
        return add_flight(format_data)

    except ValidationError as err:
        abort(400, err.messages)


@app.route('/flights/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_flight(id):
    flight = get_one_flight(id)
    if not flight:
        return abort(404)

    if request.method == 'GET':
        return flight
    elif request.method == 'PUT':
        try:
            schema = FlightSchema()
            data = schema.load(request.json)
            change_flight(id, data)
            return "Record changed"
        except ValidationError as err:
            abort(400, err.messages)
    else:
        delete_flight(id)
        return "Record delete"
