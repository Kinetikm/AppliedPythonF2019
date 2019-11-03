from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from timeboard_service.utils.exception import ApiException


class FlightSchema(Schema):
    id = fields.Int()
    dep_time = fields.Str(required=True)
    arr_time = fields.Str(required=True)
    travel_time = fields.Str(required=True, validate=validate.Regexp(r'\d{1,2}H\d{2}M'))
    dst_airport = fields.Str(required=True, validate=validate.Regexp("[A-Z]{3}"))
    aircraft = fields.Str(required=True, validate=validate.Length(max=10))

    @validates_schema
    def validate_time(self, data, **kwargs):
        if int(data["dep_time"].split(":")[0]) >= int(data["arr_time"][:2]):
            if "+1" not in data["arr_time"]:
                raise ApiException(400, "Data incorrect", "Departure time should be smaller than arrival")

    def handle_error(self, exc, data, **kwargs):
        raise ApiException(400, "Data incorrect", exc.messages)