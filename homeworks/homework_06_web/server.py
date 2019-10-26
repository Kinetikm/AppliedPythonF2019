from flask import Flask, request
from flask_restful import Api, Resource
from db import *
from validator import *
import logging as log
import time

app = Flask(__name__)
api = Api(app)
open('logger.log', 'w').close()
log.basicConfig(filename='logger.log', level=log.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = log.getLogger()

def makeFlight(data):
    flight = {
            "departure": data["departure"],
            "arrival": data["arrival"],
            "travel_time": data["travel_time"],
            "destination": data["destination"],
            "aircraft_type": data["aircraft_type"],
        }
    return flight


class FlightsWI(Resource):
    def get(self):
        logger.info("GET request for all flights completed")
        return flights

    def post(self):
        t = time.time()
        try:
            schema = FlightSchema()
            data = schema.load(request.get_json())
        except ValidationError:
            logger.error("POST request failed: WRONG INPUT or EMPTY FIELDS")
            return "Error: wrong input", 400

        global last_id
        last_id += 1
        id_ = last_id
        flight = makeFlight(data)
        flights[id_] = flight
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

        for fid, flight in flights.items():
            if(id_ == fid):
                for key in data:
                    flight[key] = data[key]
                logger.info(f"PUT request comleted | id = {id_} | Timing: {(time.time()-t)}")
                return flight, 202

        logger.info(f"PUT request failed | id = {id_} not exist")
        return "id {} not exists".format(id_), 404

    def delete(self, id_):
        global flights
        try:
            del flights[id_]
            logger.info(f"DELETE request completed | id = {id_}")
            return "{} is deleted.".format(id_), 202
        except KeyError:
            logger.info(f"DELETE request failed | id = {id_} not exist")
            return "{} not found.".format(id_), 404

api.add_resource(FlightsWI, "/flights")
api.add_resource(FlightsI, "/flights/<int:id_>")
app.run(debug=True)
