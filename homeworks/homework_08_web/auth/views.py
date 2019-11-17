from auth.models import User
from auth import db, app_auth, login_manager
from flask import Flask, abort, jsonify, request
from marshmallow import Schema, fields, validates_schema, ValidationError
from flask_login import (login_required, current_user, login_user, logout_user)


class UserSchema(Schema):
    email = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)
    password_ver = fields.Str(required=True)

    @validates_schema
    def validate_time(self, user, **kwargs):
        if user['password'] != user['password_ver']:
            raise ValidationError("Passwords don`t match")


class AuthSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


@login_manager.header_loader
def load_user(login):
    return User.get(login)


@login_manager.user_loader
def load_user(login):
    return User.get(login)


def add_user(data):
    user = User(
        email=data['email'],
        login=data['login']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()


@app_auth.route('/registration', methods=['POST'])
def registration():
    if not request.json:
        abort(400)

    try:
        data = UserSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages)

    user = User.get(data['login'])
    if user:
        abort(400, "User with that username already create")

    add_user(data)
    return "Success"


@app_auth.route("/login", methods=['POST'])
def login():
    if not request.json:
        abort(400)

    try:
        data = AuthSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages)

    user = User.get(data['login'])
    if not user:
        abort(401)

    if not user.check_password(data['password']):
        return abort(400, "Wrong password")

    login_user(user, remember=True)
    user.cookie = request.cookies["remember_token"]
    db.session.commit()
    return '', 204


@app_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return '', 204


@app_auth.route('/user_login', methods=['GET'])
@login_required
def get_login():
    return jsonify({'id': current_user.id_user,
                    'login': current_user.login})
