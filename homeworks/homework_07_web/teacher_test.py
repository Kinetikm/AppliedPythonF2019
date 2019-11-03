from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
from datetime import datetime, timedelta

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

t = datetime.now()

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t+timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "2H00M", "dst_airport": "VOL", "aircraft": "Boeing"
            }, None),

        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=20)).strftime("%H:%M") + "+1",
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Airbus"
            }, None),

        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=3)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "QQQ", "aircraft": "Airbus"
        }, None),

        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Stul"
        }, None),

        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t - timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Airbus"
        }, None),

        Urls('get', 'http://localhost:5000/service/rows', None, {}, None),

        Urls('put', 'http://localhost:5000/service/rows/3', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=1)).strftime("%H:%M"),
            "travel_time": "13H00M", "dst_airport": "CAN", "aircraft": "Airbus", "id": 3
            }, None),

        Urls('get', 'http://localhost:5000/service/rows/3', None, {}, None),

        Urls('delete', 'http://localhost:5000/service/rows/4', None, {}, None),

        Urls('get', 'http://localhost:5000/service/rows', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/min/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/average/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/count/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/percentile/2', None, {}, None)

    ]):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
