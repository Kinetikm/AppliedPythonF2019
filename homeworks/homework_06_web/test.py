from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/todo/api/flights', None, {
            'Departure(GMT)': 2130,
            'Arrival(GMT)': 600,
            'Travel time': 830,
            'Destination': u'VNU',
            'Aircraft type': u'IL-56'
        }, None),
        Urls('get', 'http://localhost:5000/todo/api/flights', None, None, None),
        Urls('put', 'http://localhost:5000/todo/api/flights/1', None, {
            'Departure(GMT)': 2031,
            'Arrival(GMT)': 1000,
            'Travel time': 1031,
            'Destination': u'Bashni blizneci',
            'Aircraft type': u'airbus'
        }, None),
        Urls('delete', 'http://localhost:5000/todo/api/flights/2', None, None, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
