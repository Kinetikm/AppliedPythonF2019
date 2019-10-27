

# Сохраняем {id: obj(Flights)} тутава, в оперативе
FLIGHTS = {}

# Дэнжероус
current_max_id = 0


class Flights:
    def __init__(self, params):
        self._departure_time = params['departure_time']
        self._arrival_time = params['arrival_time']
        self._flight_time = params['flight_time']
        self._destination_airport = params['destination_airport']
        global current_max_id
        current_max_id += 1
        self._id = current_max_id
        FLIGHTS[self._id] = self

    def insert(self):
        # В БД пока не ходим, поэтому так
        if (self._id):
            return self._id
        else:
            return None

    def update(self):
        # В БД пока не ходим, поэтому так
        if (self._id):
            return self._id
        else:
            return None

    def delete(self):
        del FLIGHTS[self._id]

    @staticmethod
    def select_by_id(flight_id):
        global current_max_id
        if (flight_id < current_max_id or flight_id <= 0):
            return None
        return FLIGHTS[flight_id]

    @staticmethod
    def select_all_flights():
        # Cчитерим и вернем сразу массив диктов:
        global current_max_id
        if (current_max_id == 0):
            return []
        data = []
        for flight in FLIGHTS.values():
            data.append(flight.convert_to_dict())
        return data

    def convert_to_dict(self):
        return {
            'id': self._id,
            'departure_time': self._departure_time,
            'arrival_time': self._arrival_time,
            'flight_time': self._flight_time,
            'destination_airport': self._destination_airport,
        }

    def departure_time(self, value=None):
        if (value and value > 0):
            self._departure_time = value
        return self._departure_time

    def arrival_time(self, value=None):
        if (value and value > 0):
            self._arrival_time = value
        return self._departure_time

    def flight_time(self, value=None):
        if (value and value > 0):
            self._flight_time = value
        return self._flight_time

    def destination_airport(self, value=None):
        if (value):
            self._destination_airport = value
        return self._destination_airport
