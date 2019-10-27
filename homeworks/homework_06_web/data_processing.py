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

def select_all():
    with open("data.json", 'r', encoding='utf-8')as file:
        return file.read()

def select(id_flight):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    if id_flight in data:
        return True, json.dumps(data[id_flight])
    return False, ""

def insert(entry):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    if is_valid(entry):
        id_flight = c.new_id()
        data[id_flight] = entry
        with open("data.json", 'w', encoding='utf-8')as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return id_flight
    return None

def update(id_flight, flight):
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    id_flight = str(id_flight)
    if is_valid(flight) and id_flight in data:
        data[id_flight] = flight
        with open("data.json", 'w', encoding='utf-8')as file:
            json.dump(data, file, ensure_ascii=False, indent=4) 
        return True, ""
    return False, '''id_flight not exist or flight format not valid'''

def delete(id_flight):   
    with open("data.json", 'r', encoding='utf-8')as file:
        data = json.loads(file.read())
    result = id_flight in data
    message = "id_flight not exist"
    if result:
        message = ""
        del data[id_flight]
    with open("data.json", 'w', encoding='utf-8')as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return result, message