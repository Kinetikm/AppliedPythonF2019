from flask import Flask

app = Flask(__name__)

from app import flight_data
from app import validation

data_storage = flight_data.FlightsStorage()
flight_schema = validation.FlightSchema()
