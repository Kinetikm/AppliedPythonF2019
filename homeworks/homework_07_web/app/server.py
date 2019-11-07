from flask import Flask, request
from flask_restful import Api, Resource
from app.db import *
from app.validator import *
import orm
import logging as log
import time

app = Flask(__name__)
api = Api(app)
open('logger.log', 'w').close()
log.basicConfig(filename='logger.log', level=log.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = log.getLogger()


def makeFlight(data):
    flight = {
            "departure": None,
            "arrival": None,
            "travel_time": None,
            "destination": None,
            "aircraft_type": None,
        }
    for key in data:
            flight[key] = data[key]
    return flight


class FlightsWI(Resource):
    def get(self):
        logger.info(f"GET request for all flights completed")
        return orm.select_all()

    def post(self):
        t = time.time()
        try:
            schema = FlightSchema()
            data = schema.load(request.get_json())
        except ValidationError:
            logger.error(f"POST request failed: WRONG INPUT or EMPTY FIELDS")
            return f"Error: wrong input", 400

        flight = makeFlight(data)
        orm.insert(flight)
        logger.info(f"POST request comleted | id = {id_} | Timing: {(time.time()-t)}")
        return flight, 201


class FlightsI(Resource):
    def put(self, id_):
        t = time.time()
        try:
            schema = FlightSchema()
            data = schema.load(request.get_json(), partial=True)
        except ValidationError:
            logger.error("PUT request failed: WRONG INPUT")
            return "Error: wrong input", 400

        flight = makeFlight(data)
        result = orm.update(flight, id_)
        print(f"ROWS UPDATED: {result}")
        logger.info(f"PUT request comleted | id = {id_} | Timing: {(time.time()-t)}")
        return flight, 202

    def delete(self, id_):
        result = orm.delete(id_)
        if result:
            logger.info(f"DELETE request completed | id = {id_}")
            return "{} is deleted.".format(id_), 202
        else:
            logger.info(f"DELETE request failed | id = {id_} not exist")
            return "{} not found.".format(id_), 404

api.add_resource(FlightsWI, "/flights")
api.add_resource(FlightsI, "/flights/<int:id_>")
