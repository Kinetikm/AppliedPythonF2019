from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)

flights = {
    0: { 
        "departure": "22:31",
        "arrival": "6:44",
        "travel_time": "8:13",
        "destination": "Tokyo",
        "aircraft_type": "Syknoi SuperJet"
    },
    1: {
        "departure": "20:31",
        "arrival": "5:44",
        "travel_time": "9:13",
        "destination": "Jamaica",
        "aircraft_type": "Snoop-Dog Airbus A320"
    },
    2: {
        "departure": "7:31",
        "arrival": "13:44",
        "travel_time": "6:13",
        "destination": "Riyadh",
        "aircraft_type": "Snoop-Dog Airbus A320"
    }
}
last_id = 2


class FlightsWI(Resource):
    def get(self):
        print(flights)
        return flights

    def post(self):
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
        print(flights)
        return flight, 201


class FlightsI(Resource):
    def put(self,id_):
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
                print(flights)
                return flight, 200
        print(flights)
        return "id {} not exists".format(id_), 400


    def delete(self,id_):
        global flights
        try:
            del flights[id_]
            print(flights)
            return "{} is deleted.".format(id_), 200
        except KeyError:
            print(flights)
            return "{} not found.".format(id_), 400
        
        

api.add_resource(FlightsWI, "/flights")
api.add_resource(FlightsI, "/flights/<int:id_>")

app.run(debug=True)
