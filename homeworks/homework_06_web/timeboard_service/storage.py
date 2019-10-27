from flask import current_app
from flask import g
import json
from datetime import datetime, timedelta


def get_fd():
    if "fd" not in g:
        g.fd = open(current_app.config["DATABASE"], 'r+')
    return g.fd


def close_fd(e=None):
    fd = g.pop("fd", None)

    if fd is not None:
        fd.close()


def init_fd(app):
    with open(app.config["DATABASE"], 'w+') as fd:
        t = datetime(2019, 3, 5, 12, 30)

        data = [
            {
                "id": 1,
                "dep_time": t.strftime("%H:%M"),
                "arr_time": (t + timedelta(hours=3)).strftime("%H:%M"),
                "travel_time": "2H00M",
                "airport": "QQQ",
                "aircraft": "Airbus"
            },
            {
                "id": 2,
                "dep_time": (t - timedelta(hours=2)).strftime("%H:%M"),
                "arr_time": (t + timedelta(hours=3)).strftime("%H:%M"),
                "travel_time": "8H46M",
                "airport": "AWE",
                "aircraft": "Boeing"
            },
            {
                "id": 3,
                "dep_time": t.strftime("%H:%M"),
                "arr_time": (t + timedelta(hours=6)).strftime("%H:%M"),
                "travel_time": "1H51M",
                "airport": "ZAS",
                "aircraft": "Superjet"
            }
        ]

        json.dump(data, fd)
