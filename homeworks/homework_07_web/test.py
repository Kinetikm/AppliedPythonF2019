from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:

    test_requests = [
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:10',
              'arrive_location': 'dmd',
              'aircraft_type': 'plane'
             }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time':  str(datetime.datetime(2017, 3, 5, 14, 15)),
              'arrival_time':  str(datetime.datetime(2017, 3, 5, 18, 30)),
              'duration': '4:15',
              'arrive_location': 'vko',
              'aircraft_type': 'jedi_starflight'
              }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time':  str(datetime.datetime(2017, 3, 5, 9, 40)),
              'arrival_time':  str(datetime.datetime(2017, 3, 5, 19, 30)),
              'duration': '9:50',
              'arrive_location': 'svo',
              'aircraft_type': 'broom'
              }, None),
        Urls('get', 'http://localhost:5000/flights', None, {'sorted': True,
             'filter': False}, None),
        Urls('put', 'http://localhost:5000/flights/1', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:10',
              'arrive_location': 'dmd',
              'aircraft_type': 'jedi_starflight'
             }, None),
        Urls('put', 'http://localhost:5000/flights/5', None, None, None),
        Urls('get', 'http://localhost:5000/flights/5', None, None, None),
        Urls('get', 'http://localhost:5000/flights/1', None, None, None),
        Urls('delete', 'http://localhost:5000/flights/1', None, None, None),
        Urls('get', 'http://localhost:5000/flights', None, {'sorted':
             False, 'filter': 'svo'}, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
                'departure_time': str(datetime.datetime(2017, 3, 5, 5, 0)),
                'arrival_time': str(datetime.datetime(2017, 3, 5, 10, 23)),
                'duration': '5:23',
                'arrive_location': 'dmd',
                'aircraft_type': 'plane'
              }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
                'departure_time': str(2),
                'arrival_time': str(3),
                'duration': 323,
                'arrive_location': 'dmd',
                'aircraft_type': 'broom'
              }, None),
        Urls('get', 'http://localhost:5000/flights', None, {'sorted': True,
             'filter': False}, None),
        Urls('get', 'http://localhost:5000/flights/metrix', None,
             {
                'method': 'GET',
                'url': 'http://localhost:5000/flights'
              }, None),
        Urls('get', 'http://localhost:5000/flights/metrix', None,
             {
                'method': 'DELETE',
             }, None),
        Urls('get', 'http://localhost:5000/flights/metrix', None,
             {
                'method': 'PUT',
             }, None),
        Urls('get', 'http://localhost:5000/flights/metrix', None,
             {
                'method': 'POST',
             }, None)
        ]
    for index, url in enumerate(test_requests):
        resp = requests.request(method=url.method, url=url.url,
                                json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
