from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json'])

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
        "id_flight": "2",
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
    }
}

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('get', 'http://localhost:5000/show_flights', None, None),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["first insert"]),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["second insert"]),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["bad insert"]),
        Urls('get', 'http://localhost:5000/show_flights', None, None),
        Urls('get', 'http://localhost:5000/show_flight/1', None, None),
        Urls('get', 'http://localhost:5000/show_flight/33', None, None),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["update"]),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["bad update"]),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["delete"]),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["bad delete"]),
        Urls('get', 'http://localhost:5000/show_flights', None, None),
    ]):
        resp = requests.request(
            method=url.method,
            url=url.url,
            headers=url.headers,
            json=url.json)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
