from marshmallow import Schema, fields, ValidationError, validates_schema


class FlightPlan(Schema):
    dep_time = fields.DateTime(required=True, format="rfc")
    arr_time = fields.DateTime(required=True, format="rfc")
    dur_time = fields.Time(required=True)
    dest = fields.Str(required=True)
    aircraft = fields.Str(required=True)


    @validates_schema
    def validates_time(self, data, **kwargs):
        if data['arr_time'] <= data['dep_time']:
            raise ValidationError('Departure time longer than arrival time')