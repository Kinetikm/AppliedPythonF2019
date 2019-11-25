import pytest
import sys
from homeworks.homework_09_web.app.server import app
from homeworks.homework_09_web.orm import Base
from sqlalchemy import create_engine


@pytest.fixture()
def test_client():

    app.config['DATABASE'] = 'sqlite:///test.db'
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
