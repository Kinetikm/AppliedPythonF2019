import collections
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = collections.namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('get', 'http://localhost:8000/api/flight/all', None, None, None),
        Urls('post', 'http://localhost:8000/api/flight/create/', None, {
            'departure_time': '2019-02-12T22:14:00.000000Z',
            'arrival_time': '2019-02-12T22:18:50.000000Z',
            'airport': 'hzgde',
            'aircraft': 'hzkuda'
        }, None),
        Urls('get', 'http://localhost:8000/api/flight/all', None, None, None),
        Urls('put', 'http://localhost:8000/api/flight/1/', None, {
            'departure_time': '2019-02-12T22:20:00.000000Z',
            'arrival_time': '2019-02-12T22:23:10.000000Z',
            'airport': 'rip',
            'aircraft': u'zont'
        }, None),
        Urls('get', 'http://localhost:8000/api/flight/all/dep_sort/', None, None, None),
        Urls('get', 'http://localhost:8000/api/flight/all/air_sort/', None, None, None),
        Urls('delete', 'http://localhost:8000/api/flight/8/', None, None, None),
        Urls('get', 'http://localhost:8000/api/flight/all', None, None, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)