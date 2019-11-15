from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from auth_service.utils.validation_schema import SignupSchema, AuthSchema
from auth_service.models import UsersTable, CookiesTable
from auth_service.utils.exception import ApiException
from auth_service import db
import uuid
import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    if not request.json:
        raise ApiException(403, 'Bad data', 'Body without data')

    data = SignupSchema(strict=True).load(request.json).data

    email = data['email']
    login = data['login']
    password = data['password']

    user = UsersTable.query.filter_by(login=login).first()

    if user:
        raise ApiException(403, 'Bad login', 'Login already exists')

    new_user = UsersTable(login=login, email=email, password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return "Register success"


@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.json:
        raise ApiException(403, 'Bad data', 'Body without data')

    data = AuthSchema(strict=True).load(request.json).data

    login = data['login']
    password = data['password']

    user = UsersTable.query.filter_by(login=login).first()

    if not user or not check_password_hash(user.password_hash, password):
        raise ApiException(403, 'Bad data', 'Invalid username or password')

    saved_cookie = CookiesTable.query.filter_by(login_id=user.id).first()
    if saved_cookie:
        db.session.delete(saved_cookie)

    token = str(uuid.uuid4())
    max_age = datetime.timedelta(seconds=30)

    cook = CookiesTable(
        token=token,
        expire=str(datetime.datetime.now() + max_age)
    )
    cook.login_id = user.id
    db.session.add(cook)
    db.session.commit()

    resp = make_response("Login success")
    resp.set_cookie("session_cookie", token, max_age=max_age)
    return resp


def login_required(foo):
    @wraps(foo)
    def wrap():
        cookie = request.cookies.get("session_cookie")
        saved_cookie = CookiesTable.query.filter_by(token=cookie).first()
        if saved_cookie is None:
            raise ApiException(403, "Bad access", "Couldnt find your cookie")

        if datetime.datetime.strptime(saved_cookie.expire, '%Y-%m-%d %H:%M:%S.%f') < datetime.datetime.now():
            db.session.delete(saved_cookie)
            db.session.commit()
            raise ApiException(403, "Bad access", "End of time")

        return foo()

    return wrap


@auth_bp.route('/about_me', methods=['GET'])
@login_required
def about_me():
    cookie = request.cookies.get("session_cookie")
    saved_cookie = CookiesTable.query.filter_by(token=cookie).first()

    return jsonify({
        'login': saved_cookie.user.login
    })


@auth_bp.route('/logout')
@login_required
def logout():
    cookie = request.cookies.get("session_cookie")
    saved_cookie = CookiesTable.query.filter_by(token=cookie).first()
    db.session.delete(saved_cookie)
    db.session.commit()
    return "Logout success"
