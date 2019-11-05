
from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

urls_for_enum = [Urls('post', 'http://localhost:8000/api/flights/', None, {
    "departure_time": "2019-11-01T20:41:57Z",
    "arrival_time": "2019-11-01T20:41:57Z",
    "flight_time": 456465,
    "destination_airport": "dmd",
    "aircraft_type": "boing",
    }, None)]
urls_for_enum.append(Urls('get', 'http://localhost:8000/api/flights/', None, None, None))
urls_for_enum.append(Urls('put', 'http://localhost:8000/api/flights/6', None, {
    "destination_airport": "svo",
    }, None))
urls_for_enum.append(Urls('delete', 'http://localhost:8000/api/flights/6', None, None, None))

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate(urls_for_enum):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
