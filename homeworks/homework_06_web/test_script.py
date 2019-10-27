from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                 'dep_time': str(datetime.datetime(2018, 4, 1, 4, 30)),
                 'arr_time': str(datetime.datetime(2018, 4, 1, 9, 20)),
                 'dur_time': '4:50',
                 'arr_locate': 'luna',
                 'aircraft_type': 'mars'
             }, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                 'dep_time': str(datetime.datetime(2018, 4, 2, 18, 20)),
                 'arr_time': str(datetime.datetime(2018, 4, 2, 19, 35)),
                 'dur_time': '1:15',
                 'arr_locate': 'hzotkudo',
                 'aircraft_type': 'hzkuda'
             }, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                 'dep_time': str(datetime.datetime(2018, 4, 2, 7, 30)),
                 'arr_time': str(datetime.datetime(2018, 4, 2, 18, 35)),
                 'dur_time': '11:05',
                 'arr_locate': 'kachkanar',
                 'aircraft_type': 'indionapolis'
             }, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('put', 'http://localhost:5000/api/flights/0', None,
             {
                 'dep_time': str(datetime.datetime(2018, 4, 6, 17, 30)),
                 'arr_time': str(datetime.datetime(2018, 4, 6, 18, 50)),
                 'dur_time': '1:20',
                 'arr_locate': 'rick',
                 'aircraft_type': 'morty'
             }, None),
        Urls('delete', 'http://localhost:5000/api/flights/1', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('post', 'http://localhost:5000/api/flights', None,
             {
                 'dep_time': str(datetime.datetime(2018, 4, 2, 14, 20)),
                 'arr_time': str(datetime.datetime(2018, 4, 2, 17, 20)),
                 'dur_time': '03:00',
                 'arr_locate': 'darth',
                 'aircraft_type': 'vader'
             }, None),
        Urls('get', 'http://localhost:5000/api/flights', None, None, None),
        Urls('get', 'http://localhost:5000/api/flights/dep_time_sort', None, None, None),
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
