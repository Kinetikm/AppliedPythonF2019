from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class FlightSchema(Schema):
    id = fields.Int()
    dep_time = fields.Str(required=True)
    arr_time = fields.Str(required=True)
    travel_time = fields.Str(required=True, validate=validate.Regexp(r'\d{1,2}H\d{2}M'))
    airport = fields.Str(required=True, validate=validate.Regexp("[A-Z]{3}"))
    aircraft = fields.Str(required=True, validate=validate.Length(max=10))

    @validates_schema
    def validate_time(self, data, **kwargs):
        if data["dep_time"] < data["arr_time"]:
            raise ValidationError("Departure time should be smaller than arrival")


def show_all(data, offset, count, dep_time):
    offset = int(offset) if offset is not None else None
    count = int(count) if count is not None else None

    if offset is not None:
        if offset > len(data) or offset < 0:
            return None
    if count is not None:
        if count > len(data) or count < 1:
            return None

    answer = data[offset:count]

    if dep_time is not None:
        answer2 = []
        for val in answer:
            if val["dep_time"] == dep_time:
                answer2.append(val)
        return answer2

    return answer


def show_flight(data, id):
    for val in data:
        if val["id"] == id:
            return val
    return None


def add_flight(body, data):
    new_flight = FlightSchema().load(body)
    new_flight[0]["id"] = data[-1]["id"] + 1
    data.append(new_flight[0])
    return data


def update_flight(body, data, id):
    upd_flight = FlightSchema().load(body)
    upd_flight[0]["id"] = id
    for i, flight in enumerate(data):
        if flight["id"] == id:
            data[i] = upd_flight[0]
            return data
    return None


def del_flight(data, id):
    for i in range(len(data)):
        if data[i]["id"] == id:
            del data[i]
            return data
    return None
