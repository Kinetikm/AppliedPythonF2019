flights = []


class Flight:

    temp_id = 0

    def __init__(self, data):
        self.id = Flight.temp_id
        Flight.temp_id += 1
        self.departure_time = data['departure_time']
        self.arrival_time = data['arrival_time']
        self.duration = data['duration']
        self.arrive_location = data['arrive_location']
        self.aircraft_type = data['aircraft_type']

    def convert_to_dict(self):
        return {
            'id': self.id,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'duration': self.duration,
            'arrive_location': self.arrive_location,
            'aircraft_type': self.aircraft_type
            }
