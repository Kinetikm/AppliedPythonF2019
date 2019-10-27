from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/todo/api/flights', None, {
                'departure_time': str(datetime.datetime(2018, 4, 1, 4, 30)),
                'arrival_time': str(datetime.datetime(2018, 4, 1, 9, 20)),
                'duration': '4:50',
                'arrive_location': 'luna',
                'aircraft_type': 'mars'
              }, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                'departure_time':  str(datetime.datetime(2018, 4, 2, 18, 20)),
                'arrival_time':  str(datetime.datetime(2018, 4, 2, 19, 35)),
                'duration': '1:15',
                'arrive_location': 'hzotkudo',
                'aircraft_type': 'hzkuda'
              }, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                'departure_time':  str(datetime.datetime(2018, 4, 2, 7, 30)),
                'arrival_time':  str(datetime.datetime(2018, 4, 2, 18, 35)),
                'duration': '11:05',
                'arrive_location': 'kachkanar',
                'aircraft_type': 'indionapolis'
              }, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('put', 'http://localhost:5000/api/flights/0', None,
             {
                'departure_time': str(datetime.datetime(2018, 4, 6, 17, 30)),
                'arrival_time': str(datetime.datetime(2018, 4, 6, 18, 50)),
                'duration': '1:20',
                'arrive_location': 'rick',
                'aircraft_type': 'morty'
              }, None),
        Urls('put', 'http://localhost:5000/api/flights/5', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights/5', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights/0', None, None, None),
        Urls('delete', 'http://localhost:5000/api/flights/1', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                'departure_time': str(datetime.datetime(2018, 4, 2, 14, 20)),
                'arrival_time': str(datetime.datetime(2018, 4, 2, 17, 20)),
                'duration': '03:00',
                'arrive_location': 'darth',
                'aircraft_type': 'vader'
              }, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                'departure_time': "heh",
                'arrival_time': "lol",
                'duration': 323,
                'arrive_location': 'mama',
                'aircraft_type': 'criminal'
              }, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights/duration_sorted',
             None, None, None),
        Urls('get', 'http://localhost:5000/api/flights/dep_time_sort', None, None, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)