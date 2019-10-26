from marshmallow import Schema, fields, ValidationError

class FlightSchema(Schema):
    departure = fields.Str(required=True)
    arrival = fields.Str(required=True)
    travel_time = fields.Str(required=True)
    destination = fields.Str(required=True)
    aircraft_type = fields.Str(required=True)