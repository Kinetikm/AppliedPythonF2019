from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:

    test_requests = [
        Urls('post', 'http://localhost:4000/login', None,
             {
              'login': 'test1',
              'passwd': 'qwe',
             }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:10',
              'arrive_location': 'dmd',
              'aircraft_type': 'plane'
             }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time':  str(datetime.datetime(2017, 3, 5, 14, 15)),
              'arrival_time':  str(datetime.datetime(2017, 3, 5, 18, 30)),
              'duration': '4:15',
              'arrive_location': 'vko',
              'aircraft_type': 'jedi_starflight'
              }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time':  str(datetime.datetime(2017, 3, 5, 9, 40)),
              'arrival_time':  str(datetime.datetime(2017, 3, 5, 19, 30)),
              'duration': '9:50',
              'arrive_location': 'svo',
              'aircraft_type': 'broom'
              }, None),
        Urls('get', 'http://localhost:4000/logout', None, None, None),
        Urls('get', 'http://localhost:5000/flights', None, {'sorted': True,
             'filter': False}, None),
        Urls('put', 'http://localhost:5000/flights/1', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:10',
              'arrive_location': 'dmd',
              'aircraft_type': 'jedi_starflight'
             }, None),
        Urls('delete', 'http://localhost:5000/flights/1', None, None, None)]
    session = requests.session()
    resp0 = requests.request(method='post',
                             url='http://localhost:4000/registration',
                             json={
                                   'email': 'ya@ru',
                                   'login': 'test1',
                                   'passwd': 'qwe',
                                   'confirm_passwd': 'qwe'})
    print('0', 'http://localhost:4000/registration', resp0.status_code,
          resp0.ok, file=f)
    print(dump_all(resp0).decode('utf-8'), file=f)
    for index, url in enumerate(test_requests):
        resp = session.request(method=url.method, url=url.url,
                               json=url.json, data=url.data)
        print(index+1, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
    resp1 = requests.request(method='post',
                             url='http://localhost:4000/registration',
                             json={
                                   'email': 'go@ru',
                                   'login': 'test2',
                                   'passwd': '123',
                                   'confirm_passwd': '123'})
    test_requests = [
        Urls('post', 'http://localhost:4000/login', None,
             {
              'login': 'test2',
              'passwd': '12',
             }, None),
        Urls('post', 'http://localhost:4000/login', None,
             {
              'login': 'test2',
              'passwd': '123',
             }, None),
        Urls('post', 'http://localhost:5000/flights', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 5, 0)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 10, 23)),
              'duration': '5:23',
              'arrive_location': 'dmd',
              'aircraft_type': 'plane'
             }, None),
        Urls('delete', 'http://localhost:5000/flights/3', None, None, None),
        Urls('get', 'http://localhost:4000/logout', None, None, None),
        Urls('post', 'http://localhost:4000/login', None,
             {
              'login': 'test1',
              'passwd': 'qwe',
             }, None),
        Urls('delete', 'http://localhost:5000/flights/1', None, None, None),
        Urls('put', 'http://localhost:5000/flights/2', None,
             {
              'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
              'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
              'duration': '1:10',
              'arrive_location': 'dmd',
              'aircraft_type': 'jedi_starflight'
             }, None)]
    session = requests.session()
    for index, url in enumerate(test_requests):
        resp = session.request(method=url.method, url=url.url,
                               json=url.json, data=url.data)
        print(index+8, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
