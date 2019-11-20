import pytest
from flask_sqlalchemy import SQLAlchemy
from app.firstmodule.orm_queries import registrate_user
from app import create_app
import os


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


def test_registration(test_client, init_database):
    resp = test_client.post('/registration', json={
                                                   'login': 'test30',
                                                   'email': 'sm@ya.ru',
                                                   'passwd': '123',
                                                   'confirm_passwd': '123'
                                                   })
    assert resp.json == {'error': 'User already exist'}
    resp = test_client.post('/login', json={
                                            'login': 'test30',
                                            'passwd': '123',
                                            })
    assert resp.status_code == 200
    assert resp.headers.getlist('Set-Cookie')
    resp = test_client.get('/logout')
    assert resp.json == {'logout': True}
