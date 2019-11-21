from marshmallow import Schema, fields, ValidationError


class FlightSchema(Schema):
    departure = fields.Str(required=True)
    arrival = fields.Str(required=True)
    travel_time = fields.Str(required=True)
    destination = fields.Str(required=True)
    aircraft_type = fields.Str(required=True)


class UserSchema(Schema):
    token = fields.Str(dump_only=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)

class AuthSchema(Schema):
    token = fields.Str(required=True)
