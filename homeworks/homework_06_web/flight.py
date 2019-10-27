class Flight:
    def __init__(self, info):
        self.departure_time = info["departure_time"]
        self.arrival_time = info["arrival_time"]
        self.travel_time = info["travel_time"]
        self.destination_airport = info["destination_airport"]
        self.type_of_aircraft = info["type_of_aircraft"]
