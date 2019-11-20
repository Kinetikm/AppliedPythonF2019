import pytest
from flask import Flask
from app.firstmodule.models import Plane, Airport, Flight
from app.firstmodule.validation import validate_duration
from marshmallow import ValidationError
from app import create_app
import datetime


def test_duration_check():
    json = {
            'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
            'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
            'duration': '1:10'
           }
    try:
        validate_duration(json)
        return True
    except ValidationError:
        return False
    json_1 = {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:9'
              }
    try:
        validate_duration(json)
        return False
    except ValidationError:
        return True
