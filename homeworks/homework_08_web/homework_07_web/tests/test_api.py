import pytest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
import os
import datetime


@pytest.fixture(scope='module')
def test_client():
    test_app = create_app()
    test_app.config['DATABASE'] = 'postgresql:///testdb'
    test_app.config['JWT_SECRET_KEY'] = 'super-secret'
    test_app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    test_app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    testing_client = test_app.test_client(use_cookies=True)
    ctx = test_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture()
def init_database():
    db = SQLAlchemy()
    db.create_all()
    yield init_database
    db.drop_all()


def test_post_flight(test_client, init_database):
    json = {
            'departure_time': str(datetime.datetime(2017, 3, 5, 12, 30)),
            'arrival_time': str(datetime.datetime(2017, 3, 5, 13, 40)),
            'duration': '1:10',
            'arrive_location': 'dmd',
            'aircraft_type': 'plane_1'
            }
    resp = test_client.post('/flights', json=json)
    assert resp.status_code == 401
