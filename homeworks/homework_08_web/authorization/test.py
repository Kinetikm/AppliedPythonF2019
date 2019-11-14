from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
import datetime

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:

    test_requests = [
        Urls('post', 'http://localhost:5000/registration', None,
             {
              'email': 'ya@ru',
              'login': 'test4',
              'passwd': 'qwe',
              'confirm_passwd': 'qwe'
             }, None),
        Urls('post', 'http://localhost:5000/login', None,
             {
              'login': 'test4',
              'passwd': 'qwe',
             }, None)
        ]
    for url in test_requests:
        resp = requests.request(method=url.method, url=url.url,
                                json=url.json, data=url.data)
        f.write(str(resp.text))
