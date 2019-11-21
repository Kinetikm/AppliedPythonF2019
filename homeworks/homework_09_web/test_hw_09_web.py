#!/usr/bin/env python
# coding: utf-8

import wsgiref.simple_server
import threading
import zipapp
import json
import data_processing as dp
import auth
import manage
import os
import pytest
from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)

server_params = []


class Server(threading.Thread):
    def run(self):
        manage.prepare()
        self.httpd = wsgiref.simple_server.make_server(
            'localhost', 5000, manage.app)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


class Auth(threading.Thread):
    def run(self):
        auth.prepare()
        self.httpd = wsgiref.simple_server.make_server(
            'localhost', 5001, auth.app)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


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


def test_server():
    dp.clear_base()
    Urls = namedtuple(
        'Urls', [
            'method', 'url', 'headers', 'json', 'params', 'result_status_code'])

    server = Server()
    server.start()

    auth_server = Auth()
    auth_server.start()

    params = {
        "sort_by": "arrival_time",
        "filter_field": "destination_airport",
        "filter_value": "Sheremetievo"}

    cook = {}
    with open('expected_results.txt', 'r') as f:
        exp_json = json.load(f)
    cnt = -1
    res = []
    for index, url in enumerate([
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_first"], None, 200),
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_two"], None, 200),
        Urls('post', 'http://localhost:5001/registration', None, jsons["registration_bad"], None, 400),
        Urls('post', 'http://localhost:5001/login', None, jsons["login_first"], None, 200),
        Urls('get', 'http://localhost:5000/show_flights', None, None, None, 200),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["first insert"], None, 200),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["second insert"], None, 200),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["bad insert"], None, 400),
        Urls('get', 'http://localhost:5000/show_flights', None, None, None, 200),
        Urls('get', 'http://localhost:5000/show_flight/1', None, None, None, 200),
        Urls('get', 'http://localhost:5000/show_flight/33', None, None, None, 400),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["update"], None, 200),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["bad update"], None, 400),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["delete"], None, 200),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["bad delete"], None, 400),
        Urls('get', 'http://localhost:5000/show_flights', None, None, None, 200),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["third insert"], None, 200),
        Urls('post', 'http://localhost:5000/new_flight', None, jsons["forth insert"], None, 200),
        Urls('get', 'http://localhost:5000/show_flights', None, None, params, 200),
        Urls('get', 'http://localhost:5000/statistic', None, None, None, 200),
        Urls('get', 'http://localhost:5000/statistic_metrics', None, None, None, 200),
        Urls('post', 'http://localhost:5001/logout', None, None, None, 200),
        Urls('post', 'http://localhost:5001/login', None, jsons["login_second"], None, 200),
        Urls('put', 'http://localhost:5000/update_flight', None, jsons["no access update"], None, 403),
        Urls('delete', 'http://localhost:5000/delete_flight', None, jsons["no access delete"], None, 403),
    ]):
        resp = requests.request(
            method=url.method,
            url=url.url,
            headers=url.headers,
            json=url.json,
            params=url.params,
            cookies=cook)

        assert url.result_status_code == resp.status_code
        if resp._content is not None and resp._content != b'' and resp.status_code == 200:
            result_json = json.loads(resp._content)
            cnt += 1
            if url.url == 'http://localhost:5000/statistic_metrics':
                continue
            if url.url == "http://localhost:5000/statistic":
                for num, res in enumerate(result_json['result']):
                    assert exp_json[cnt]['result'][num][1:5] == res[1:5]
            else:
                assert exp_json[cnt] == result_json
        if dict(resp.cookies) != {}:
            cook = dict(resp.cookies)
        if url[1] == 'http://localhost:5001/logout':
            cook = {}

    server.stop()
    auth_server.stop()
