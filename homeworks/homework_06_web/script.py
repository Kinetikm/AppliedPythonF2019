from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'params'])

jsons = {
    "first insert":
    {
        "departure_time": "10:00",
        "arrival_time": "13:00",
        "travel_time": "03:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU"
    },
    "second insert":
    {
        "departure_time": "11:00",
        "arrival_time": "12:00",
        "travel_time": "01:00",
        "destination_airport": "Sheremetievo",
        "type_aircraft": "TU"
    },
    "bad insert":
    {
        "departure_time": "12:00",
        "arrival_time": "25:00",
        "travel_time": "02:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU"
    },
    "update":
    {
        "id_flight": "1",
        "flight":
        {
            "departure_time": "16:00",
            "arrival_time": "17:00",
            "travel_time": "01:00",
            "destination_airport": "Vnukovo",
            "type_aircraft": "TU"
        }
    },
    "bad update":
    {
        "id_flight": "3",
        "flight":
        {
            "departure_time": 1600,
            "arrival_time": "17:00",
            "travel_time": "01:00",
            "destination_airport": "Vnukovo",
            "type_aircraft": "TU"
        }
    },
    "delete":
    {
        "id_flight": "1",
    },
    "bad delete":
    {
        "id_flight": "4",
    },
    "third insert":
    {
        "departure_time": "06:00",
        "arrival_time": "08:00",
        "travel_time": "02:00",
        "destination_airport": "Sheremetievo",
        "type_aircraft": "TU"
    },
    "forth insert":
    {
        "departure_time": "10:00",
        "arrival_time": "11:00",
        "travel_time": "01:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU"
    },
}
params = {
    "sort_by": "arrival_time",
    "filter_field": "destination_airport",
    "filter_value": "Sheremetievo"}

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('get', 'http://localhost:5000/show_flights', None, None, None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["first insert"], None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["second insert"], None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["bad insert"], None),
        Urls('get', 'http://localhost:5000/show_flights', None, None, None),
        Urls('get', 'http://localhost:5000/show_flight/1', None, None, None),
        Urls('get', 'http://localhost:5000/show_flight/33', None, None, None),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["update"], None),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["bad update"], None),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["delete"], None),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["bad delete"], None),
        Urls('get', 'http://localhost:5000/show_flights', None, None, None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["third insert"], None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["forth insert"], None),
        Urls('get', 'http://localhost:5000/show_flights', None, None, params),
        Urls('get', 'http://localhost:5000/statistic', None, None, None),
        Urls('get', 'http://localhost:5000/statistic_metrics', None, None, None),
    ]):
        resp = requests.request(
            method=url.method,
            url=url.url,
            headers=url.headers,
            json=url.json,
            params=url.params)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
