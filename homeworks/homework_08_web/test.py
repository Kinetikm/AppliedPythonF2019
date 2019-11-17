from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'data'])

body = [
    {
        "id": 2,
        "name": "RE340",
        "dept_time": "10:00",
        "arr_time": "15:00",
        "travel_time": "5:00",
        "airport": "moscow",
        "type": "pass"
    },
    None,
    None,
    {
        "name": "RE340",
        "dept_time": "11:00",
        "arr_time": "15:00",
        "travel_time": "4:00",
        "airport": "moscow",
        "type": "pass"
    },
    None,
    None,
    None]

reqs = [Urls('post', 'http://localhost:5000/flights', None, None),
        Urls('get', 'http://localhost:5000/flights/2', None, None),
        Urls('get', 'http://localhost:5000/flights/3', None, None),
        Urls('put', 'http://localhost:5000/flights/2', None, None),
        Urls('get', 'http://localhost:5000/flights/2', None, None),
        Urls('delete', 'http://localhost:5000/flights/2', None, None),
        Urls('get', 'http://localhost:5000/flights', None, None)]

with open('request_dumps.txt', 'w') as f:
    for index, data in enumerate(zip(reqs, body)):
        url, url_body = data
        resp = requests.request(method=url.method, url=url.url, json=url_body, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
