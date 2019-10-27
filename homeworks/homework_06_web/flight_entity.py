import time
from flask import abort


class Flight():
    def check_time(self, string):
        return string.isnumeric()

    def check_airport(self, string):
        return string.isalpha() and len(string) == 3

    def check_aircraft(self, string):
        return True

    def check_flight_time(self, string):
        if string.isnumeric():
            return int(string) == (int(self.value['arrival']) - int(self.value['departure'])) and int(string) <= 86400
        else:
            return False

    def __init__(self, input_value):
        self.params = {
            'arrival': self.check_time,
            'departure': self.check_time,
            'time_in_flight': self.check_flight_time,
            'airport': self.check_airport,
            'aircraft_type': self.check_aircraft}
        self.value = dict()
        for val in self.params:
            if val in input_value and self.params[val](input_value[val]):
                self.value[val] = input_value[val]
            else:
                self.value.clear()
                abort(400)

    def __getitem__(self, key):
        if key not in self.value:
            abort(404)
        return self.value[key]

    def edit_flight(self, input_value):
        for val in self.params:
            if val in input_value and self.params[val](input_value[val]):
                self.value[val] = input_value[val]
            else:
                abort(400)

    def get_flight_info(self):
        temp = self.value.copy()
        temp['arrival'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(temp['arrival'])))
        temp['departure'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(temp['departure'])))
        temp['time_in_flight'] = time.strftime("%H:%M:%S", time.gmtime(int(temp['time_in_flight'])))
        return temp
