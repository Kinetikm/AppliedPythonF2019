from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime
Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    test_data = [
        Urls('get', 'http://localhost:5000/flights', None, None, None),
        Urls('post', 'http://localhost:5000/flights', None, {
                'departure': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
                'arrival': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
                'time_in_flight': '7200',
                'airport': 'SVO',
                'aircraft_type': 'AN28'
            }, None),
        Urls('post', 'http://localhost:5000/flights', None, {
                'departure': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
                'arrival': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
                'time_in_flight': '3600',
                'airport': 'SVO',
                'aircraft_type': 'AN28'
            }, None),
        Urls('post', 'http://localhost:5000/flights', None, {
                'departure': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
                'arrival': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
                'time_in_flight': '7200',
                'airport': 'SVO',
                'aircraft_type': 'AN28'
            }, None),
        Urls('post', 'http://localhost:5000/flights', None, {
            'departure': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
            'time_in_flight': '7200',
            'airport': 'SV',
            'aircraft_type': 'AN28'
        }, None),
        Urls('post', 'http://localhost:5000/flights', None, {
            'departure': str(int(datetime.datetime(2019, 10, 24, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 24, 14, 25).timestamp())),
            'time_in_flight': '15900',
            'airport': 'DMD',
            'aircraft_type': 'SU100'
        }, None),
        Urls('get', 'http://localhost:5000/flights', None, None, None),
        Urls('put', 'http://localhost:5000/flights/2', None, {
            'departure': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
            'time_in_flight': '7200',
            'airport': 'DMD',
            'aircraft_type': 'AN28'
        }, None),
        Urls('put', 'http://localhost:5000/flights/0', None, {
            'departure': str(int(datetime.datetime(2019, 10, 23, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 23, 12, 00).timestamp())),
            'time_in_flight': '7200',
            'airport': 'DMD',
            'aircraft_type': 'AN28'
        }, None),
        Urls('put', 'http://localhost:5000/flights/1', None, {
            'departure': str(int(datetime.datetime(2019, 10, 24, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 24, 14, 25).timestamp())),
            'time_in_flight': '15900',
            'airport': 'SVO',
            'aircraft_type': 'SU104'
        }, None),
        Urls('delete', 'http://localhost:5000/flights/2', None, None, None),
        Urls('post', 'http://localhost:5000/flights', None, {
            'departure': str(int(datetime.datetime(2019, 10, 25, 10, 00).timestamp())),
            'arrival': str(int(datetime.datetime(2019, 10, 25, 13, 00).timestamp())),
            'time_in_flight': '10800',
            'airport': 'DIA',
            'aircraft_type': 'A320'
        }, None),
        Urls('get', 'http://localhost:5000/flights/DMD', None, None, None),
        Urls('get', 'http://localhost:5000/flights/sort', None, None, None),
        Urls('delete', 'http://localhost:5000/flights/2', None, None, None),
        Urls('get', 'http://localhost:5000/flights', None, None, None),
    ]
    for index, url in enumerate(test_data):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
