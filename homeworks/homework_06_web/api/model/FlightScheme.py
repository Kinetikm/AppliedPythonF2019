from marshmallow import Schema, fields, ValidationError
import datetime


class FlightPlan(Schema):
    dep_time = fields.DateTime(required=True)
    arr_time = fields.DateTime(required=True)
    dur_time = fields.Time(required=True)
    arr_locate = fields.Str(required=True)
    aircraft_type = fields.Str(required=True)


def validates_time(json_request):
    dep_time = datetime.datetime.strptime(json_request['dep_time'], '%Y-%m-%d %H:%M:%S')
    arr_time = datetime.datetime.strptime(json_request['arr_time'], '%Y-%m-%d %H:%M:%S')
    dur_time = datetime.datetime.strptime(json_request['dur_time'], '%H:%M')
    if (arr_time - dep_time).total_seconds() < 0:
        raise ValidationError('Departure time must be less than arrival time')
    elif (arr_time - dep_time).total_seconds() != (dur_time.hour * 3600 + dur_time.minute * 60):
        raise ValidationError('Incorrect flight duration')
