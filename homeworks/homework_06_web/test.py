
from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])


urls_for_enum = [Urls('post', 'http://localhost:5000/flights', None, {
    "departure_time": 4535435,
    "arrival_time": 543534,
    "flight_time": 456465,
    "destination_airport": "dmd",
    }, None)]
urls_for_enum.append(Urls('get', 'http://localhost:5000/flights/', None, None, None))
urls_for_enum.append(Urls('put', 'http://localhost:5000/flights/1', None, {
    "destination_airport": "svo",
    "arrival_time": 1,
    }, None))
urls_for_enum.append(Urls('delete', 'http://localhost:5000/flights/1', None, None, None))

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate(urls_for_enum):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
