from flask import Flask, Blueprint, request, abort, jsonify, make_response, g
from flask import request
import app.firstmodule.validation as validation
import time
import logging
import app.firstmodule.orm_queries as orm_queries


module = Blueprint('', __name__)
controllers_logger = logging.getLogger('app.controllers')

@module.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@module.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@module.errorhandler(401)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid login or password'}),
                                 401)


@module.errorhandler(409)
def already_exist(error):
    return make_response(jsonify({'error': 'User already exist'}), 409)


@module.route('/registration', methods=['POST'])
def registration():
    try:
        validation.RegistrtationSchema().load(request.json)
        validation.validate_passwd(request.json)
    except validation.ValidationError:
        abort(400)
    user_add = orm_queries.registrate_user(request.json)
    if user_add == 1:
        abort(409)
    return jsonify({'result': 'New user was created'}), 201


@module.route('/login', methods=['POST'])
def login():
    jwt_token = orm_queries.auth(request.json)
    if not jwt_token:
        abort(401)
    return jsonify({'jwt_token': jwt_token}), 200
