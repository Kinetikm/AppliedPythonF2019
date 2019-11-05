#!/usr/bin/python
import collections
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = collections.namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:8000/api/flights/flight/create/', None, {
            'departure': '2222-02-12T22:22:00.000000Z',
            'arrival': '2222-02-12T22:22:50.000000Z',
            'destination': 'VKO',
            'aircraft': 'boeing'
        }, None),
        Urls('get', 'http://localhost:8000/api/flights/all', None, None, None),
        Urls('put', 'http://localhost:8000/api/flights/flight/6/', None, {
            'departure': '2222-02-12T22:22:00.000000Z',
            'arrival': '2222-02-12T22:22:10.000000Z',
            'destination': 'DME',
            'aircraft': u'airbus'
        }, None),
        Urls('get', 'http://localhost:8000/api/flights/all/dep_sort/', None, None, None),
        Urls('get', 'http://localhost:8000/api/flights/all/air_sort/', None, None, None),
        Urls('delete', 'http://localhost:8000/api/flights/flight/8/', None, None, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
