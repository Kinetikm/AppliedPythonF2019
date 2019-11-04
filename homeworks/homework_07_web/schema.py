#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cerberus import Validator
from datetime import datetime


def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def to_time(s):
    return datetime.strptime(s, "%H:%M")


schema = {
            "departure_time": {"type": "datetime", "coerce": to_date},
            "arrival_time": {"type": "datetime", "coerce": to_date},
            "travel_time": {"type": "datetime", "coerce": to_time},
            "destination_airport": {"type": "string"},
            "type_of_aircraft": {"type": "string"}
}
valid = Validator(schema)
