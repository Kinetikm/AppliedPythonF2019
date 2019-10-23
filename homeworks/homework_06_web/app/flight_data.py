import datetime
import random


def generate_data(n=5, start_date=datetime.datetime(2018, 1, 1), end_date=datetime.datetime(2019, 1, 1),
                  max_flight_time=10):
    data = []
    airports = ['Moscow', 'Chelyabinsk', 'Ekaterinburg', 'London', 'Berlin', 'Minsk']
    planes = ['A320', 'B777', 'B737', 'A319', 'A380']
    for i in range(n):
        # генерируем случайное время отправления и прибытия
        delta = end_date - start_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        t1 = start_date + datetime.timedelta(seconds=random_second)
        t2 = t1 + datetime.timedelta(hours=random.randrange(max_flight_time)+1)
        h = (t2 - t1).seconds // 3600
        m = (t2 - t1).seconds // 60 % 60
        d = {'dep_time': t1, 'arr_time': t2, 'dest_airport': random.choice(airports), 'airplane': random.choice(planes),
             'flight_time': '{h}:{m}'.format(h=h, m=m)}
        data.append(d)
    return data


class FlightsStorage:

    def __init__(self):
        self._data = generate_data()

    def get_flight(self, pos):
        if pos >= len(self._data):
            return None
        result = self._data[pos]
        return result

    def get_flights(self):
        return self._data

    def add_flight(self, dep_time: datetime.datetime, arr_time: datetime.datetime,
                   dest_airp, airplane):
        h = (arr_time - dep_time).seconds // 3600
        m = (arr_time - dep_time).seconds // 60 % 60
        d = {'dep_time': dep_time, 'arr_time': arr_time, 'dest_airport': dest_airp,
             'airplane': airplane, 'flight_time': '{h}:{m}'.format(h=h, m=m)}
        self._data.append(d)

    def change_flight(self, pos, dep_time: datetime.datetime, arr_time: datetime.datetime,
                      dest_airp, airplane):

        if pos >= len(self._data):
            return None
        h = (arr_time - dep_time).seconds // 3600
        m = (arr_time - dep_time).seconds // 60 % 60
        d = {'dep_time': dep_time, 'arr_time': arr_time, 'dest_airport': dest_airp,
             'airplane': airplane, 'flight_time': '{h}:{m}'.format(h=h, m=m)}
        self._data[pos] = d
        return True

    def delete_flight(self, pos):
        if pos >= len(self._data):
            return None
        del self._data[pos]
        return True
