from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
from datetime import datetime, timedelta

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

t = datetime.now()

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t+timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "2H00M", "airport": "ABS", "aircraft": "BUS"
            }, None),
        Urls('post', 'http://localhost:5000/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=12)).strftime("%H:%M"),
            "travel_time": "12H00M", "airport": "DSA", "aircraft": "Airbus"
            }, None),
        Urls('put', 'http://localhost:5000/rows/3', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=1)).strftime("%H:%M"),
            "travel_time": "1H00M", "airport": "NEW", "aircraft": "Airbus"
            }, None),
        Urls('delete', 'http://localhost:5000/rows/1', None, {}, None),
        Urls('delete', 'http://localhost:5000/rows/2', None, {}, None)
    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
