from flask import Flask, request
from flask_restful import Api, Resource
from flask_login import (
    LoginManager, UserMixin, login_required,
    current_user, login_user, logout_user
)
from app.db import *
from app.validator import *
import orm
import logging as log
import time

app = Flask(__name__)
api = Api(app)
open('logger.log', 'w').close()
log.basicConfig(filename='logger.log', level=log.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = log.getLogger()
login_manager = LoginManager()
login_manager.init_app(app)


def makeFlight(data):
    flight = {
            "departure": None,
            "arrival": None,
            "travel_time": None,
            "destination": None,
            "aircraft_type": None,
        }
    for key in data:
            flight[key] = data[key]
    return flight


class User(UserMixin):

    def __init__(self, token, username, password, email):
        self.id = token
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def get(cls, token):
        user = orm.get_user(token)
        if not user:
            return
        return cls(token, *user)

    @classmethod
    def set(cls, token, data):
        orm.set_user(token, data)
        # cls.user_database[token] = data


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

    try:
        data = UserSchema(strict=True).load(request.json).data
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error.messages)

    User.set(data['token'], {"login": data['login'], "password": data['password'], "email": data['email']})
    return jsonify({'token': data['token']})


@app.route("/login", methods=['POST'])
def login():
    if not request.json:
        abort(400)

    try:
        data = AuthSchema(strict=True).load(request.json).data
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error.messages)

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
    return jsonify({
        'username': current_user.username,
        'age': current_user.age,
        'cookie': request.cookies,
    })


class FlightsWI(Resource):
    def get(self):
        logger.info(f"GET request for all flights completed")
        return orm.select_all(), 200

    @login_required
    def post(self):
        t = time.time()
        try:
            schema = FlightSchema()
            data = schema.load(request.get_json())
        except ValidationError:
            logger.error(f"POST request failed: WRONG INPUT or EMPTY FIELDS")
            return f"Error: wrong input", 400

        flight = makeFlight(data)
        orm.insert(flight)
        logger.info(f"POST request comleted | Timing: {(time.time()-t)}")
        return flight, 201


class FlightsI(Resource):
    def put(self, id_):
        t = time.time()
        try:
            schema = FlightSchema()
            data = schema.load(request.get_json(), partial=True)
        except ValidationError:
            logger.error("PUT request failed: WRONG INPUT")
            return "Error: wrong input", 400

        flight = makeFlight(data)
        result = orm.update(id_, flight)
        print(f"ROWS UPDATED: {result}")
        logger.info(f"PUT request comleted | id = {id_} | Timing: {(time.time()-t)}")
        return flight, 202

    def delete(self, id_):
        result = orm.delete(id_)
        if result:
            logger.info(f"DELETE request completed | id = {id_}")
            return "{} is deleted.".format(id_), 202
        else:
            logger.info(f"DELETE request failed | id = {id_} not exist")
            return "{} not found.".format(id_), 404

api.add_resource(FlightsWI, "/flights")
api.add_resource(FlightsI, "/flights/<int:id_>")
