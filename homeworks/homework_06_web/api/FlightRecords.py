all_flights = []


class Flight:
    temp = 0

    def __init__(self, data):
        self.id = Flight.temp
        Flight.temp += 1
        self.dep_time = data['dep_time']
        self.arr_time = data['arr_time']
        self.dur_time = data['dur_time']
        self.arr_locate = data['arr_locate']
        self.aircraft_type = data['aircraft_type']

    def converted(self):
        return {
            'id': self.id,
            'dep_time': self.dep_time,
            'arr_time': self.arr_time,
            'dur_time': self.dur_time,
            'arr_locate': self.arr_locate,
            'aircraft_type': self.aircraft_type
        }