from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'params'])

jsons = {
    "registration_first":
    {
        "email": "email1@example.com",
        "login": "user1",
        "password": "pswd1",
        "password_confirm": "pswd1"
    },
    "registration_two":
    {
        "email": "email2@example.com",
        "login": "user2",
        "password": "pswd2",
        "password_confirm": "pswd2"
    },
    "registration_bad":
    {
        "email": "email_bad@example.com",
        "login": "user_bad",
        "password": "pswd_bad_1",
        "password_confirm": "pswd_bad_2"
    },
    "login_first":
    {
        "login": "user1",
        "password": "pswd1",
    },
    "login_second":
    {
        "login": "user2",
        "password": "pswd2",
    },
    "first insert":
    {
        "departure_time": "10:00",
        "arrival_time": "13:00",
        "travel_time": "03:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU",
        "login": "user1"
    },
    "second insert":
    {
        "departure_time": "11:00",
        "arrival_time": "12:00",
        "travel_time": "01:00",
        "destination_airport": "Sheremetievo",
        "type_aircraft": "TU",
        "login": "user1"
    },
    "bad insert":
    {
        "departure_time": "12:00",
        "arrival_time": "25:00",
        "travel_time": "02:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU",
        "login": "user1"
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
    "no access update":
    {
        "id_flight": "3",
        "flight":
        {
            "departure_time": "16:00",
            "arrival_time": "17:00",
            "travel_time": "01:00",
            "destination_airport": "Vnukovo",
            "type_aircraft": "TU"
        }
    },
    "delete":
    {
        "id_flight": "1",
        "login": "user1"
    },
    "bad delete":
    {
        "id_flight": "4",
        "login": "user1"
    },
    "no access delete":
    {
        "id_flight": "2",
        "login": "user2"
    },
    "third insert":
    {
        "departure_time": "06:00",
        "arrival_time": "08:00",
        "travel_time": "02:00",
        "destination_airport": "Sheremetievo",
        "type_aircraft": "TU",
        "login": "user1"
    },
    "forth insert":
    {
        "departure_time": "10:00",
        "arrival_time": "11:00",
        "travel_time": "01:00",
        "destination_airport": "Vnukovo",
        "type_aircraft": "TU",
        "login": "user1"
    },
}

params = {
    "sort_by": "arrival_time",
    "filter_field": "destination_airport",
    "filter_value": "Sheremetievo"}

cook = {}

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_first"], None),
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_two"], None),
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_bad"], None),
        Urls('post', 'http://localhost:5001/login', None, jsons["login_first"], None),
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
        Urls('post', 'http://localhost:5001/logout', None, None, None),
        Urls('post', 'http://localhost:5001/login', None, jsons["login_second"], None),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["no access update"], None),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["no access delete"], None),
    ]):
        resp = requests.request(
            method=url.method,
            url=url.url,
            headers=url.headers,
            json=url.json,
            params=url.params,
            cookies=cook)
        print(
            index,
            url,
            resp.status_code,
            resp.ok,
            dict(
                resp.cookies),
            file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
        if dict(resp.cookies) != {}:
            cook = dict(resp.cookies)
        if url[1] == 'http://localhost:5001/logout':
            cook = {}
