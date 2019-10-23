from marshmallow import Schema, fields, validates_schema, ValidationError


class FlightSchema(Schema):

    airplane = fields.Str(required=True)
    dest_airport = fields.Str(required=True)
    dep_time = fields.DateTime(required=True, format='rfc')
    arr_time = fields.DateTime(required=True, format='rfc')

    @validates_schema
    def arr_is_later_dep(self, data, **kwargs):
        if data['dep_time'] >= data['arr_time']:
            raise ValidationError("arr_time must be later then dep_time")
