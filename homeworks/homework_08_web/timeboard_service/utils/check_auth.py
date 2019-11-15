from flask import request
from functools import wraps
from requests import get
from timeboard_service.models import FlightTable
from timeboard_service.utils.exception import ApiException


def check_permission(foo):
    @wraps(foo)
    def wrap(_id):
        cookie = request.cookies.get("session_cookie")
        if cookie is None:
            raise ApiException(403, "Bad access", "Couldnt find your cookie")

        resp = get("http://127.0.0.1:8080/about_me", cookies={"session_cookie": cookie})

        flight = FlightTable.query.filter_by(id=_id).first()
        if flight is None:
            raise ApiException(404, "Index out of range", "Flight with such ID doesnt exist")

        if flight.creator != resp.json()["login"]:
            raise ApiException(403, "Bad access", "You have not rule to access")

        return foo(_id)

    return wrap


def check_auth(foo):
    @wraps(foo)
    def wrap():
        cookie = request.cookies.get("session_cookie")
        if cookie is None:
            raise ApiException(403, "Bad access", "Couldnt find your cookie")
        resp = get("http://127.0.0.1:8080/about_me", cookies={"session_cookie": cookie})

        if "login" not in resp.json().keys():
            raise ApiException(403, "Bad access", "Bad cookie")

        return foo(resp.json()["login"])

    return wrap
