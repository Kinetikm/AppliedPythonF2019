import time
from datetime import datetime


class Flight():
    def check_time(self, string):
        return string.isnumeric()

    def check_airport(self, string):
        return string.isalpha() and len(string) == 3

    def check_aircraft(self, string):
        return True

    def check_flight_time(self, string):
        if string.isnumeric():
            return int(string) == (int(self.value['arrival']) - int(self.value['departure'])) and string <= '86400'
        else:
            return False

    def __init__(self, input_value):
        self.params = {
            'arrival': self.check_time,
            'departure': self.check_time,
            'time_in_flight': self.check_flight_time,
            'airport': self.check_airport,
            'aircraft_type': self.check_aircraft}
        self.transfer = ['arrival', 'departure']
        self.value = dict()
        for val in self.transfer:
            if val in input_value:
                input_value[val] = str(int(datetime.strptime(input_value[val], '%Y-%m-%d %H:%M:%S').timestamp()))
        h, m = input_value['time_in_flight'].split(':')
        input_value['time_in_flight'] = str(int(h)*3600 + int(m)*60)
        for val in self.params:
            if val in input_value and self.params[val](input_value[val]):
                self.value[val] = input_value[val]
            else:
                self.value.clear()
                raise ValueError

    def get_flight_info(self):
        temp = self.value.copy()
        temp['arrival'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(temp['arrival'])))
        temp['departure'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(temp['departure'])))
        temp['time_in_flight'] = time.strftime("%H:%M:%S", time.gmtime(int(temp['time_in_flight'])))
        return temp
