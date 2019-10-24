from flask import Flask
from flask_restful import Api, Resource, reqparse
from db import *
import logging as log
import time


app = Flask(__name__)
api = Api(app)
open('logger.log', 'w').close()
log.basicConfig(filename='logger.log', level=log.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = log.getLogger()

class FlightsWI(Resource):
    def get(self):
        logger.info("GET request for all flights completed")
        return flights

    def post(self):
        t = time.time()
        parser = reqparse.RequestParser()
        parser.add_argument("departure")
        parser.add_argument("arrival")
        parser.add_argument("travel_time")
        parser.add_argument("destination")
        parser.add_argument("aircraft_type")
        args = parser.parse_args()

        global last_id
        last_id += 1
        id_ = last_id
        flight = {
            "departure": args["departure"],
            "arrival": args["arrival"],
            "travel_time": args["travel_time"],
            "destination": args["destination"],
            "aircraft_type": args["aircraft_type"],
        }
        flights[id_] = flight
        logger.info("POST request comleted | id = %d | Timing: %f" % (id_, (time.time()-t)))
        return flight, 201


class FlightsI(Resource):
    def put(self,id_):
        t = time.time()
        parser = reqparse.RequestParser()
        parser.add_argument("departure", required=False)
        parser.add_argument("arrival", required=False)
        parser.add_argument("travel_time", required=False)
        parser.add_argument("destination", required=False)
        parser.add_argument("aircraft_type", required=False)
        args = parser.parse_args()

        for fid, flight in flights.items():
            if(id_ == fid):
                flight["departure"] = args["departure"]
                flight["arrival"] = args["arrival"]
                flight["travel_time"] = args["travel_time"]
                flight["destination"] = args["destination"]
                flight["aircraft_type"] = args["aircraft_type"]
                logger.info("PUT request comleted | id = %d | Timing: %f" % (id_, (time.time()-t)))
                return flight, 202
        logger.info("PUT request failed | id = %d not exist" % id_)
        return "id {} not exists".format(id_), 404


    def delete(self,id_):
        global flights
        try:
            del flights[id_]
            logger.info("DELETE request completed | id = %d" % id_)
            return "{} is deleted.".format(id_), 202
        except KeyError:
            logger.info("DELETE request failed | id = %d not exist" % id_)
            return "{} not found.".format(id_), 404
        
        

api.add_resource(FlightsWI, "/flights")
api.add_resource(FlightsI, "/flights/<int:id_>")

app.run(debug=True)
