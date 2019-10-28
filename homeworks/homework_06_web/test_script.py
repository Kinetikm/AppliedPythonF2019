from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])

with open('request_dumps.txt', 'w') as f:
	for index, url in enumerate([
    	Urls('post', "http://127.0.0.1:5000/flights", None,
	         {'id': 3,
          'departure':'Tue, 12 Jun 2012 14:03:19 GMT',
            'arrival':'Tue, 12 Jun 2012 14:03:11 GMT',
        'flight_time':'14:34 GMT',
            'airport':'AMD',
              'plane':'Airbus'}
		    , None),
    	Urls('get', "http://127.0.0.1:5000/flights", None, None, None),
		Urls('put', "http://127.0.0.1:5000/flights/1"),
		Urls('delete', "http://127.0.0.1:5000/flights/1")
	]):
    	resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
    	print(index, url, resp.status_code, resp.ok, file=f)
    	print(dump_all(resp).decode('utf-8'), file=f)
