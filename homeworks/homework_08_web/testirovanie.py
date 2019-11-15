from collections import namedtuple
import requests
from requests_toolbelt.utils.dump import dump_all
from datetime import datetime, timedelta

Urls = namedtuple('Urls', ['method', 'url', 'headers', 'json', 'data'])
t = datetime.now()

cookie = None

with open('request_dumps.txt', 'w') as f:
    for index, url in enumerate([
        # 0. good user
        Urls('post', 'http://localhost:8080/signup', None, {
            "email": "cron@mail.ru", "login": "kuznec", "password": "12345", "re_password": "12345"
        }, None),

        # 1. bad login
        Urls('post', 'http://localhost:8080/signup', None, {
            "email": "cron@mail.ru", "login": "kuznec", "password": "12345", "re_password": "12345"
        }, None),

        # 2. bad re_password
        Urls('post', 'http://localhost:8080/signup', None, {
            "email": "zhara@yandex.ru", "login": "stebel", "password": "12345", "re_password": "7373735"
        }, None),

        # 3. bad email
        Urls('post', 'http://localhost:8080/signup', None, {
            "email": "MAIL@", "login": "utug", "password": "12345", "re_password": "12345"
        }, None),

        # 4. good user
        Urls('post', 'http://localhost:8080/signup', None, {
            "email": "zhara@yandex.ru", "login": "utug", "password": "12345", "re_password": "12345"
        }, None),

        # 5. Login, get cookie
        Urls('post', 'http://localhost:8080/login', None, {
            "login": "utug", "password": "12345"
        }, None),

        # 6. Good add
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t+timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "2H00M", "dst_airport": "VOL", "aircraft": "Boeing"
            }, None),

        # 7. Login, get cookie
        Urls('post', 'http://localhost:8080/login', None, {
            "login": "kuznec", "password": "12345"
        }, None),

        # 8. Good add
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=20)).strftime("%H:%M") + "+1",
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Airbus"
            }, None),

        # 9. Bad airport
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=3)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "QQQ", "aircraft": "Airbus"
        }, None),

        # 10. Bad aircraft
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Stul"
        }, None),

        # 11. Seems good
        Urls('post', 'http://localhost:5000/service/rows', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t - timedelta(hours=2)).strftime("%H:%M"),
            "travel_time": "12H00M", "dst_airport": "CAN", "aircraft": "Airbus"
        }, None),

        # 12. Get all
        Urls('get', 'http://localhost:5000/service/rows', None, {}, None),

        # 13. Login, get cookie
        Urls('post', 'http://localhost:8080/login', None, {
            "login": "utug", "password": "12345"
        }, None),

        # 14. Good update
        Urls('put', 'http://localhost:5000/service/rows/4', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=1)).strftime("%H:%M"),
            "travel_time": "13H00M", "dst_airport": "CAN", "aircraft": "Airbus", "id": 4
            }, None),

        # 15. Login, get cookie
        Urls('post', 'http://localhost:8080/login', None, {
            "login": "kuznec", "password": "12345"
        }, None),

        # 16. Bad update
        Urls('put', 'http://localhost:5000/service/rows/4', None, {
            "dep_time": t.strftime("%H:%M"), "arr_time": (t + timedelta(hours=1)).strftime("%H:%M"),
            "travel_time": "13H00M", "dst_airport": "CAN", "aircraft": "Airbus", "id": 4
        }, None),

        # 17. Get 4
        Urls('get', 'http://localhost:5000/service/rows/4', None, {}, None),

        # 18. Login, get cookie
        Urls('post', 'http://localhost:8080/login', None, {
            "login": "utug", "password": "12345"
        }, None),

        # 19. Del 4
        Urls('delete', 'http://localhost:5000/service/rows/4', None, {}, None),

        Urls('get', 'http://localhost:5000/service/rows', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/min/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/average/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/count/2', None, {}, None),

        Urls('get', 'http://localhost:5000/statistic/percentile/2', None, {}, None)

    ]):
        if cookie:
            resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data, cookies=cookie)
        else:
            resp = requests.request(method=url.method, url=url.url, json=url.json, data=url.data)
        cookie = resp.cookies
        print(index, url, resp.status_code, resp.ok, file=f)
        print(dump_all(resp).decode('utf-8'), file=f)
