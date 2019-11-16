#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models import Users, Sessions
from flask import Flask, request, jsonify, make_response, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

auth_app = Flask(__name__)


@auth_app.route("/registration", methods=["POST"])
def registration():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    password_confirm = request.json.get("password_confirm")
    if password != password_confirm:
        return jsonify({"user": "passwords must match"}), 400
    session = Session()
    if session.query(Users).filter_by(name=name).first():
        return jsonify({"user": "login is already in use"}), 400
    user = Users(name=name,
                 email=email,
                 password=generate_password_hash(password, method='sha256'))
    session.add(user)
    session.commit()
    return jsonify({"user": "user created"}), 200


@auth_app.route("/login", methods=["POST"])
def login():
    name = request.json.get("name")
    password = request.json.get("password")
    session = Session()
    user = session.query(Users).filter_by(name=name).first()
    if user:
        if check_password_hash(user.password, password):
            cookie = str(generate_password_hash(password, method='sha256'))
            session.add(Sessions(username=name, cookie=cookie))
            session.commit()
            r = make_response("setting a cookie")
            r.set_cookie("cookie", cookie)
            return r, 200
        return jsonify({"user": "wrong password"}), 400
    return jsonify({"user": "user does not exist"}), 401


@auth_app.route("/logout", methods=["GET"])
def logout():
    cookie = request.cookies.get("cookie")
    session = Session()
    ck = session.query(Sessions).filter(Sessions.cookie == cookie).first()
    if cookie:
        session.delete(ck)
        session.commit()
        r = make_response("cookie removed")
        r.set_cookie("cookie", "", max_age=0)
        return r, 200
    abort(401)


if __name__ == "__main__":
    auth_app.run(debug=True, port=8000)
