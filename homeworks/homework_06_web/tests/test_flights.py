import logging
import pytest
from sqlalchemy import create_engine
import json

from flights.application import app, routes
from models.model import Base

logging.disable(logging.CRITICAL)


@pytest.fixture()
def flight_test_client():
    app.config['DATABASE'] = app.config['TEST_DATABASE']
    app.config['DEBUG'] = True
    testing_client = app.test_client(use_cookies=True)
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


def test_post_flight(flight_test_client, init_database, requests_mock):
    requests_mock.get("http://auth:8000/about_me", json={
        'id': '1',
        'username': 'user1',
        'email': 'example@email.com',
    })
    resp = flight_test_client.post('/flights',
                                   data=json.dumps({"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
                                                    "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
                                                    "dest_airport": "London"}),
                                   content_type='application/json')
    assert resp.status_code == 200


def test_get_flights(flight_test_client, init_database, requests_mock):
    user_id = 1
    requests_mock.get("http://auth:8000/about_me", json={
        'id': user_id,
        'username': 'user1',
        'email': 'example@email.com',
    })
    data = {"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
            "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
            "dest_airport": "London"}
    flight_test_client.post('/flights',
                            data=json.dumps(data),
                            content_type='application/json')
    resp = flight_test_client.get('/flights')
    resp_data = json.loads(resp.data)
    assert resp_data[0]['user_id'] == user_id
    assert resp_data[0]['airplane'] == data['airplane']
    assert resp_data[0]['arr_time'] == data['arr_time']
    assert resp_data[0]['dep_time'] == data['dep_time']
    assert resp_data[0]['airport'] == data['dest_airport']


def test_get_flight(flight_test_client, init_database, requests_mock):
    user_id = 1
    requests_mock.get("http://auth:8000/about_me", json={
        'id': user_id,
        'username': 'user1',
        'email': 'example@email.com',
    })
    data = {"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
            "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
            "dest_airport": "London"}
    flight_test_client.post('/flights',
                            data=json.dumps(data),
                            content_type='application/json')
    resp = flight_test_client.get('/flights/1/')
    resp_data = json.loads(resp.data)
    assert resp_data['user_id'] == user_id
    assert resp_data['airplane'] == data['airplane']
    assert resp_data['arr_time'] == data['arr_time']
    assert resp_data['dep_time'] == data['dep_time']
    assert resp_data['airport'] == data['dest_airport']


def test_delete_flight(flight_test_client, init_database, requests_mock):
    requests_mock.get("http://auth:8000/about_me", json={
        'id': 1,
        'username': 'user1',
        'email': 'example@email.com',
    })
    resp = flight_test_client.delete('/flights/1/')
    assert resp.status_code == 404
    flight_test_client.post('/flights',
                            data=json.dumps({"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
                                             "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
                                             "dest_airport": "London"}),
                            content_type='application/json')
    resp = flight_test_client.delete('/flights/1/')
    assert resp.status_code == 200


def test_put_flight(flight_test_client, init_database, requests_mock):
    requests_mock.get("http://auth:8000/about_me", json={
        'id': 1,
        'username': 'user1',
        'email': 'example@email.com',
    })
    flight_test_client.post('/flights',
                            data=json.dumps({"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
                                             "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
                                             "dest_airport": "London"}),
                            content_type='application/json')
    resp = flight_test_client.put('/flights/1/',
                                  data=json.dumps({"airplane": "A320", "arr_time": "Thu, 15 Nov 2018 04:15:52 GMT",
                                                   "dep_time": "Thu, 15 Nov 2018 01:16:22 GMT",
                                                   "dest_airport": "Moscow"}),
                                  content_type='application/json')
    assert resp.status_code == 200
    resp = flight_test_client.get('/flights')
    resp_data = json.loads(resp.data)
    assert resp_data[0]['airport'] == "Moscow"
