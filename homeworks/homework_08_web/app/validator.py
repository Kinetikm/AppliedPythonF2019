from marshmallow import Schema, fields, ValidationError


class FlightSchema(Schema):
    departure = fields.Str(required=True)
    arrival = fields.Str(required=True)
    travel_time = fields.Str(required=True)
    destination = fields.Str(required=True)
    aircraft_type = fields.Str(required=True)


class UserSchema(Schema):
    token = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    age = fields.Int()


class AuthSchema(Schema):
    token = fields.Str(required=True)
