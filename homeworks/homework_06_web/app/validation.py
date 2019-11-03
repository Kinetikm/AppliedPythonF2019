from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class FlightSchema(Schema):

    airplane = fields.Str(required=True)
    dest_airport = fields.Str(required=True)
    dep_time = fields.DateTime(required=True, format='rfc')
    arr_time = fields.DateTime(required=True, format='rfc')

    @validates_schema
    def arr_is_later_dep(self, data, **kwargs):
        if data['dep_time'] >= data['arr_time']:
            raise ValidationError("arr_time must be later then dep_time")


class ArgsSchema(Schema):

    PERMISSIBLE_VALUE = ['airplane', 'airport', 'dep_time', 'arr_time', 'flight_time']
    sort_by = fields.Str(missing=None)
    filter_by_plane = fields.Str(missing=None)
    filter_by_airport = fields.Str(missing=None)
    filter_by_time = fields.DateTime(missing=None, format='rfc')

    @validates('sort_by')
    def validate_sort_by(self, value):
        if (value is not None) and (value not in self.PERMISSIBLE_VALUE):
            raise ValidationError('Incorrect value of sort_by parameter')


class MetricsParamsSchema(Schema):

    PERMISSIBLE_VALUE = ['GET', 'POST', 'PUT', 'DELETE']
    method_type = fields.Str(required=True)

    @validates('method_type')
    def validate_sort_by(self, value):
        if (value is not None) and (value not in self.PERMISSIBLE_VALUE):
            raise ValidationError('Incorrect value of sort_by parameter')
