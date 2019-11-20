import pytest
from flask import Flask
from app.firstmodule.models import User
from app.firstmodule.validation import validate_passwd
from marshmallow import ValidationError
from app import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User(email='ex@ya.ru', login='user', passwd_hash='gjdtr')
    return user


def test_new_user(new_user):
    user = User(email='ex@ya.ru', login='user', passwd_hash='gjdtr')
    assert new_user.email == 'ex@ya.ru'
    assert new_user.login == 'user'
    assert new_user.passwd_hash == 'gjdtr'
    assert str(new_user) == '<user:ex@ya.ru>'


def test_passwd_check():
    json = {
        'passwd': '123',
        'confirm_passwd': '123'
    }
    json_1 = {
        'passwd': '123',
        'confirm_passwd': 'qwe'
    }
    res = validate_passwd(json)
    assert res is None
    try:
        res_1 = validate_passwd(json_1)
    except ValidationError:
        return True
    else:
        return False
