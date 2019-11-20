from app.database import db
import app.firstmodule.models as models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import jsonify


def registrate_user(json_data):
    try:
        query = db.session.query(models.User).filter(models.User.login ==
                                                     json_data['login']).all()
        query = query[0]
    except IndexError:
        query = models.User(email=json_data['email'], login=json_data['login'],
                            passwd_hash=generate_password_hash(
                            json_data['passwd']))
        db.session.add(query)
        db.session.commit()
        return
    return 1


def auth(json_data):
    try:
        query = (db.session.query(models.User)
                 .filter(models.User.login == json_data['login'])
                 .all())
        query = query[0]
        if not check_password_hash(query.passwd_hash, json_data['passwd']):
            raise IndexError
    except IndexError:
        return
    token = create_access_token(identity=query.login)
    resp = jsonify({'login': True})
    set_access_cookies(resp, token)
    add_session = models.Session(login=query.login, jwt_token=token)
    db.session.add(add_session)
    db.session.commit()
    return resp


def delete_session(login):
    models.Session.query.filter(models.Session.login == login).delete()
    db.session.commit()
