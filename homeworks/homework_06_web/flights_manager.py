from flight_entity import Flight, abort
from collections import OrderedDict


class FlightManager():
    def __init__(self):
        self.dict_of_flights = OrderedDict()
        self.max_id = 0

    def create_flight(self, input_value):
        temp = Flight(input_value)
        if len(temp.get_flight_info()) == 5:
            self.dict_of_flights[self.max_id] = temp
            self.max_id += 1
        else:
            abort(400)

    def delete_flight(self, flight_number):
        if flight_number in self.dict_of_flights:
            del self.dict_of_flights[flight_number]
        else:
            abort(404)

    def flight_by_airport(self, airport):
        return [flight.get_flight_info() for flight in self.dict_of_flights.values() if flight.get_flight_info()[
            'airport'] == airport]

    def get_all_flights(self):
        return [flight.get_flight_info() for flight in self.dict_of_flights.values()]

    def sort_by_flight_duration(self):
        temp = self.dict_of_flights
        self.value = OrderedDict(sorted(temp.items(), key=lambda x: x[1]['time_in_flight']))

    def __len__(self):
        return len(self.dict_of_flights)

    def __getitem__(self, key):
        if key not in self.dict_of_flights:
            abort(404)
        return self.dict_of_flights[key]
