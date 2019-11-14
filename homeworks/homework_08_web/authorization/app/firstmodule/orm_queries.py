from app.database import db
import app.firstmodule.models as models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


def registrate_user(json_data):
    try:
        query = db.session.query(models.User).filter(models.User.login ==
                                                 json_data['login']).all()
        query = query[0]
    except IndexError:
        query = models.User(email=json_data['email'], login=json_data['login'],
                            passwd_hash=generate_password_hash(json_data['passwd']))
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
    token = create_access_token(identity=query.user_id)
    add_session = models.Session(user_id=query.user_id, jwt_token=token)
    db.session.add(add_session)
    db.session.commit()
    return token


