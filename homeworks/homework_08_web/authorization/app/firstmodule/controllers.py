from flask import Flask, Blueprint, request, abort, jsonify, make_response, g
from flask import request
import app.firstmodule.validation as validation
import time
import logging
import app.firstmodule.orm_queries as orm_queries
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                unset_jwt_cookies)
import logging


module = Blueprint('', __name__)
controllers_logger = logging.getLogger('app.controllers')


@module.before_request
def before_request():
    g.start = time.time()


@module.after_request
def teardown_request(response):
    diff = time.time() - g.start
    controllers_logger.info((f'Query to {request.url}.') +
                            (f'{request.method} method. Answer code is: ') +
                            (f'{response.status_code}. ') +
                            (f'Answer is: {response.json}'))
    return response


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
    return jwt_token, 200


@module.route('/logout', methods=['GET'])
@jwt_required
def logout():
    login = get_jwt_identity()
    orm_queries.delete_session(login)
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
