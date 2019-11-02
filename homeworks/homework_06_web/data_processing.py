import json
import sys
from os import path
from marshmallow import Schema, fields, ValidationError


class Cnt:
    def __init__(self):
        self.cnt = 0
        if path.isfile("data.json"):
            with open("data.json", 'r', encoding='utf-8')as file:
                data = json.loads(file.read())
                if len(data) > 0:
                    self.cnt = max(data.keys())

    def new_id(self):
        self.cnt += 1
        return str(self.cnt)


c = Cnt()


class Flight(Schema):
    departure_time = fields.Time(required=True)
    arrival_time = fields.Time(required=True)
    travel_time = fields.Time(required=True)
    destination_airport = fields.Str(required=True)
    type_aircraft = fields.Str(required=True)


def is_valid(entry):
    schema = Flight()
    try:
        schema.load(entry)
        return True
    except ValidationError:
        return False


def select_all(sort_by, filter_field, filter_value):
    with open("data.json", 'r', encoding='utf-8')as file:
        res = json.loads(file.read())
        if len(res) == 0:
            res = []
        else:
            res = [{"id_flight": i, "flight": res[i]} for i in res]
    if filter_field is not None and filter_value is not None and len(res) > 0:
        try:
            res = [i for i in res if i["flight"][filter_field] == filter_value]
        except BaseException:
            return None
    if sort_by is not None and len(res) > 0:
        try:
            res.sort(key=lambda a: a["flight"][sort_by])
        except BaseException:
            return None
    return res


def select(id_flight):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    try:
        return True, data[str(id_flight)]
    except BaseException:
        return False, ""


def insert(entry):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    if is_valid(entry):
        key = c.new_id()
        data[key] = entry
        with open("data.json", 'w', encoding='utf-8')as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return key
    return None


def update(id_flight, flight):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    if is_valid(flight):
        try:
            data[str(id_flight)] = flight
            with open("data.json", 'w', encoding='utf-8')as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True, ""
        except BaseException:
            pass
    return False, '''id_flight not exist or flight format not valid'''


def delete(id_flight):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    try:
        del data[str(id_flight)]
        with open("data.json", 'w', encoding='utf-8')as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True, ""
    except BaseException:
        return False, "id_flight not exist"
