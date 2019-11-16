#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
    test = [Urls('post', 'http://localhost:8000/registration', None, {"name": "Anton",
                                                                      "email": "A@mail.ru",
                                                                      "password": "123456",
                                                                      "password_confirm": "123456"}, None),
            Urls('post', 'http://localhost:8000/registration', None, {"name": "Kate",
                                                                      "email": "K@mail.ru",
                                                                      "password": "123456",
                                                                      "password_confirm": "123456"}, None),
            Urls('post', 'http://localhost:5000/flights', None, {"departure_time": "2019-10-09 19:50",
                                                                 "arrival_time": "2019-10-09 21:05",
                                                                 "travel_time": "04:15",
                                                                 "destination_airport": "London",
                                                                 "type_of_aircraft": "Airflot"}, None),
            Urls('post', 'http://localhost:8000/login', None, {"name": "Kate",
                                                               "password": "123456"}, None),
            Urls('post', 'http://localhost:5000/flights', None, {"departure_time": "2019-10-09 19:50",
                                                                 "arrival_time": "2019-10-09 21:05",
                                                                 "travel_time": "04:15",
                                                                 "destination_airport": "London",
                                                                 "type_of_aircraft": "Airflot"}, None),
            Urls('get', 'http://localhost:5000/flights', None, None, None),
            Urls('post', 'http://localhost:8000/login', None, {"name": "Anton",
                                                               "password": "123456"}, None),
            Urls('post', 'http://localhost:5000/flights', None, {"departure_time": "2019-12-10 04:20",
                                                                 "arrival_time": "2019-12-11 01:05",
                                                                 "travel_time": "19:45",
                                                                 "destination_airport": "Dubai",
                                                                 "type_of_aircraft": "A300"}, None),
            Urls('delete', 'http://localhost:5000/flights/3', None, None, None),
            Urls('get', 'http://localhost:5000/flights/4', None, None, None),
            Urls('get', 'http://localhost:5000/flights/15', None, None, None),
            Urls('get', 'http://localhost:5000/flights/filter_airport:London', None, None, None),
            Urls('get', 'http://localhost:5000/flights/filter_aircraft:Airflot', None, None, None),
            Urls('post', 'http://localhost:5000/flights', None, {"departure_time": "2019-01 21:40",
                                                                 "arrival_time": "2019-01-05 08",
                                                                 "travel_time": "05:45",
                                                                 "destination_airport": "Irkutsk",
                                                                 "type_of_aircraft": "Airflot"}, None),
            Urls('get', 'http://localhost:5000/flights/sort_by_arrival_time', None, None, None),
            Urls('get', 'http://localhost:5000/flights/sort_by_departure_time', None, None, None),
            Urls('put', 'http://localhost:5000/flights/4', None, {"departure_time": "2019-10-20 19:50",
                                                                  "arrival_time": "2019-10-20 21:05",
                                                                  "travel_time": "04:15",
                                                                  "destination_airport": "Moscow",
                                                                  "type_of_aircraft": "Airflot"}, None),
            Urls('get', 'http://localhost:5000/flights/metric', None, None, None)
            ]
    for index, url in enumerate(test):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
