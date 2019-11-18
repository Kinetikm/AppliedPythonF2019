from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data', 'params'])

with open('request_dumps.txt', 'w') as f:
    test_reqts = [
        Urls('post', 'http://localhost:8080/registration', None,
             {'login': 'user1', 'email': 'user2@example.com', 'password': '123'}, None, None),
        Urls('post', 'http://localhost:8080/registration', None,
             {'login': 'user2', 'email': 'user1@example.com', 'password': '123'}, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user1', 'password': '123'}, None, None),
        Urls('get', 'http://localhost:8080/about_me', None, None, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user1', 'password': '123'}, None, None),
        Urls('post', 'http://localhost:8080/flights', None,
             {"airplane": "A380", "arr_time": "Thu, 15 Nov 2018 03:12:52 GMT",
              "dep_time": "Thu, 15 Nov 2018 02:12:52 GMT", "dest_airport": "Moscow"}, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user2', 'password': '123'}, None, None),
        Urls('post', 'http://localhost:8080/flights', None,
             {"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
              "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT", "dest_airport": "London"}, None, None),
        Urls('get', 'http://localhost:8080/flights', None, None, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user2', 'password': '123'}, None, None),
        Urls('delete', 'http://localhost:8080/flights/1/', None, None, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user1', 'password': '123'}, None, None),
        Urls('delete', 'http://localhost:8080/flights/1/', None, None, None, None),
        Urls('get', 'http://localhost:8080/flights', None, None, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user2', 'password': '123'}, None, None),
        Urls('put', 'http://localhost:8080/flights/2/', None,
             {"airplane": "A320", "arr_time": "Thu, 27 Sep 2018 23:21:43 GMT",
              "dep_time": "Thu, 27 Sep 2018 22:21:43 GMT", "dest_airport": "Moscow"}, None, None),
        Urls('get', 'http://localhost:8080/flights', None, None, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user1', 'password': '123'}, None, None),
        Urls('put', 'http://localhost:8080/flights/2/', None,  # изменяем рейс
             {"airplane": "A320", "arr_time": "Thu, 27 Sep 2018 23:21:43 GMT",
              "dep_time": "Thu, 27 Sep 2018 22:21:43 GMT", "dest_airport": "Berlin"}, None, None),
    ]
    cookies = None
    for index, url in enumerate(test_reqts):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data, params=url.params,
                                cookies=cookies)
        cookies = resp.cookies
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
