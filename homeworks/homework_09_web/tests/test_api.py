import pytest
import sys
sys.path.append("..")
from app.server import app
from orm import Base

@pytest.fixture()
def test_client():

    app.config['DATABASE'] = app.config['TEST_DATABASE']
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture()
def init_database():
    engine = create_engine(app.config['DATABASE'])
    Base.metadata.create_all(engine)

    yield init_database
    Base.metadata.drop_all(engine)


def check_response(response, data=None, status_code=200):
    assert response.status_code == status_code
    if data:
        assert response.json == data


def test_create_flight(test_client, init_database):

    response = test_client.post(
        '/flights', json={
            "departure": "21:31",
            "arrival": "6:44",
            "travel_time": "9:13",
            "destination": "Mexico",
            "aircraft_type": "Airbus A320"
        })
    check_response(response, True, 201)


def test_get_flights(test_client, init_database):
    data = {
            "departure": "21:31",
            "arrival": "6:44",
            "travel_time": "9:13",
            "destination": "Mexico",
            "aircraft_type": "Airbus A320"
        }
    flight_test_client.post('/flights', json=data)
    response = test_client.get('/flights')
    check_response(response, data, 201)


def test_put_flight(test_client, init_database):
    response = test_client.put(
        "/flights/1", json={"aircraft_type": "Snoop-Dog Airbus A320 V2"})
    check_response(response, True, 202)


def test_delete_flight(test_client, init_database):
    response = test_client.delete("/flights/1")
    check_response(response, "1 is deleted.", 202)


def test_create_flight2(test_client, init_database):

    response = test_client.post(
        '/flights', json={
            "login": 'Morty',
            "password": 'password',
            "email": "testin@mail.ru"
        })
    check_response(response, "Error: wrong input", 400)


def test_put_flight2(test_client, init_database):
    response = test_client.put(
        "/flights/1", json={"aircraft_type1": "Snoop-Dog Airbus A320 V2"})
    check_response(response, "Error: wrong input", 400)


def test_delete_flight2(test_client, init_database):
    response = test_client.delete("/flights/101")
    check_response(response, "101 not found.", 404)


def test_registration(test_client, init_database):

    response = test_client.post(
        '/login', json={
            "token": 'toekrrtgg234234-tkfdgmgkd543',
            "login": 'Morty',
            "password": 'password',
            "email": "testin@mail.ru"
        })
    check_response(response, {"registration": "user created"}, 200)
