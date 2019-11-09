import uuid

import marshmallow as ma

from flask import Flask, abort, jsonify, request
from flask_login import (
    LoginManager, UserMixin, login_required,
    current_user, login_user, logout_user
)

# python3.7 server.py
app = Flask(__name__)
app.config["SECRET_KEY"] = "123SECRET_KEY123"
app.config['REMEMBER_COOKIE_NAME'] = 'technoatom'

login_manager = LoginManager()
login_manager.init_app(app)


class UserSchema(ma.Schema):
    token = ma.fields.Str(dump_only=True)
    username = ma.fields.Str(required=True)
    age = ma.fields.Int()

    @ma.pre_load
    def process_input(self, data):
        data['username'] = data['username'].lower().strip()
        return data

    @ma.post_load
    def make_object(self, data):
        data['token'] = str(uuid.uuid4())
        data['age'] = data.get('age', 0)
        return data


class AuthSchema(ma.Schema):
    token = ma.fields.Str(required=True)


class User(UserMixin):
    # proxy for a database of users
    user_database = {
        'bd8caa3d-51c9-4add-bb13-a4fbbe12a777': ('Test', '123')
    }

    def __init__(self, token, username, age):
        self.id = token
        self.username = username
        self.age = age

    @classmethod
    def get(cls, token):
        user = cls.user_database.get(token)
        if not user:
            return
        return cls(token, *user)

    @classmethod
    def set(cls, token, data):
        cls.user_database[token] = data


@login_manager.header_loader
def load_header_user(token):
    return User.get(token)


@login_manager.user_loader
def load_request_user(token):
    return User.get(token)


@app.route('/registration', methods=['POST'])
def registration():
    if not request.json:
        abort(400)

    # Валидация данных
    try:
        data = UserSchema(strict=True).load(request.json).data
    except ma.exceptions.ValidationError as e:
        return jsonify(e.messages)

    # Установка данных
    User.set(data['token'], (data['username'], data['age']))
    return jsonify({'token': data['token']})


@app.route("/login", methods=['POST'])
def login():
    if not request.json:
        abort(400)

    try:
        data = AuthSchema(strict=True).load(request.json).data
    except ma.exceptions.ValidationError as e:
        return jsonify(e.messages)

    user = User.get(data['token'])
    if not user:
        abort(401)

    login_user(user, remember=True)
    return '', 204


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return '', 204


@app.route('/about_me')
@login_required
def about_me():
    # import ipdb; ipdb.set_trace()
    return jsonify({
        'username': current_user.username,
        'age': current_user.age,
        'coockie': request.cookies,
    })


if __name__ == '__main__':
    app.run(debug=True)
