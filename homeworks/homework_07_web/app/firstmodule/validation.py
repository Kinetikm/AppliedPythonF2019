from marshmallow import Schema, fields, ValidationError
import datetime


class FlightSchema(Schema):
    departure_time = fields.DateTime(required=True)
    arrival_time = fields.DateTime(required=True)
    duration = fields.Time(required=True)
    arrive_location = fields.Str(required=True)
    aircraft_type = fields.Str(required=True)

    class Meta:
        strict = True


def validate_duration(json_request):
    departure_time = datetime.datetime.strptime(json_request['departure_time'],
                                                '%Y-%m-%d %H:%M:%S')
    arrival_time = datetime.datetime.strptime(json_request['arrival_time'],
                                              '%Y-%m-%d %H:%M:%S')
    delta = arrival_time - departure_time
    correct_seconds = delta.total_seconds()
    duration = datetime.datetime.strptime(json_request['duration'], '%H:%M')
    duration_in_seconds = duration.hour * 3600 + duration.minute * 60
    if correct_seconds != duration_in_seconds or correct_seconds < 0:
        raise ValidationError('Incorrect duartion of flight')
