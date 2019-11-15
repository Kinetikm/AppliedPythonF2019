from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/flights', None, {
            "departure": "21:31",
            "arrival": "6:44",
            "travel_time": "9:13",
            "destination": "Mexico",
            "aircraft_type": "Airbus A320"
        }, None),
        Urls('get', 'http://localhost:5000/flights', None, None, None),
        Urls('put', 'http://localhost:5000/flights/2', None, {"aircraft_type": "Snoop-Dog Airbus A320 V2"}, None),
        Urls('delete', 'http://localhost:5000/flights/1', None, None, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
