from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data', 'params'])

with open('request_dumps.txt', 'w') as f:
    test_reqts = [  # Urls('get', 'http://localhost:5000/flights', None, None, None, None),  # получаем все рейсы
        # сортируем по времени отправления
        # Urls('get', 'http://localhost:5000/flights', None, None, None, {'sort_by': 'dep_time'}),
        # Urls('get', 'http://localhost:5000/flights/2/', None, None, None, None),  # получаем рейс 2
        # Urls('get', 'http://localhost:5000/flights/100/', None, None, None, None),  # несушествующий рейс


        # Urls('delete', 'http://localhost:5000/flights/3/', None, None, None, None),  # удаляем рейс
        # Urls('post', 'http://localhost:5000/flights', None,  # добавляем
        #     {"airplane": "A380", "arr_time": "Thu, 15 Nov 2018 03:12:52 GMT",
        #      "dep_time": "Thu, 15 Nov 2018 02:12:52 GMT", "dest_airport": "Moscow"}, None, None),
        # Urls('post', 'http://localhost:5000/flights', None,  # невалидные данные
        #     {"airplane": "A380", "arr_time": "Thu, 15 Nov 2018 03:12:52 GMT",
        #      "dep_time": "Thu, 15 Nov 2018 02:12:52 GMT"}, None, None),
        # Urls('put', 'http://localhost:5000/flights/1/', None,  # изменяем рейс
        #     {"airplane": "A320", "arr_time": "Thu, 27 Sep 2018 23:21:43 GMT",
        #      "dep_time": "Thu, 27 Sep 2018 22:21:43 GMT", "dest_airport": "Moscow"}, None, None),
        # фильтруем по аэропорту
        # Urls('get', 'http://localhost:5000/flights', None, None, None, {'sort_by': 'dep_time',
        #                                                                'filter_by_airport': 'Moscow'}),
        # метрики для get-запросов
        # Urls('get', 'http://localhost:5000/metrics', None, None, None, {'method_type': 'GET'}),
        Urls('post', 'http://localhost:8080/registration', None,
             {'login': 'user1', 'email': 'user2@example.com', 'password': '123'}, None, None),
        Urls('post', 'http://localhost:8080/login', None,
             {'login': 'user1', 'password': '123'}, None, None),
    ]
    for index, url in enumerate(test_reqts):
        resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data, params=url.params)
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
