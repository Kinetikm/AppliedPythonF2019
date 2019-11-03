import logging
import time
import uuid
import traceback
import json

from flask import Flask, request, g, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from timeboard_service.database import init_db
from timeboard_service.utils.exception import ApiException


def logging_setup(app):
    logging.basicConfig(format='%(asctime)s timeboard_service %(levelname)s:  %(message)s',
                        level=logging.INFO,
                        filename='./mylog.txt')
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    @app.before_request
    def start_timer():
        g.request_start = time.time()
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def log_request(response):
        now = time.time()
        duration = round(now - g.request_start, 3)

        from timeboard_service.models import StatisticTable
        req_type = g.pop("req_type", None)
        if req_type:
            stat = StatisticTable(
                req_type=req_type,
                time=duration
            )
            db.session.add(stat)
            db.session.commit()

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host
        args = dict(request.args)
        request_body = None
        try:
            request_body = request.json
        except Exception as e:
            pass

        log_dict = {
            'id': g.request_id,
            'type': 'http',
            'method': request.method,
            'path': request.path,
            'args': args,
            'body': request_body,
            'status_code': response.status_code,
            'response': response.data[0:100],
            'duration': duration,
            'host': host,
            'ip': ip
        }
        app.logger.info(log_dict)

        return response


def error_handler_setup(app):
    @app.errorhandler(Exception)
    def error_handler(error):
        if not isinstance(error, ApiException) and not current_app.testing:
            logging.exception('Got exception on main handler')
            traceback.print_exc()

        if isinstance(error, IntegrityError):
            response = {
                'code': 400,
                'name': type(error.orig).__name__,
                'description': error.orig.pgerror
            }
        else:
            description = error.description if hasattr(error, 'description') else ';'.join(error.args)

            response = {
                'code': error.code if hasattr(error, 'code') else 500,
                'name': error.name if hasattr(error, 'name') else error.__class__.__name__,
                'description': description
            }

        return json.dumps(response), response['code']


def teardown_appcontext_setup(app):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()


def initialize_bd(app):
    db.init_app(app)
    with app.app_context():
        import timeboard_service.models
        db.drop_all()
        db.create_all()
        init_db(db)


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    logging_setup(app)
    logging.info('...::: Flask timeboard_service setup starts :::...')

    app.config.from_mapping(
        DATABASE='timeboard_service/storage.db',
        SQLALCHEMY_DATABASE_URI='sqlite:///storage.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    teardown_appcontext_setup(app)
    error_handler_setup(app)

    logging.info('...::: Storage initializing :::...')

    initialize_bd(app)

    logging.info('...::: Storage initialized :::...')

    from timeboard_service.route import service_route, statistic_route
    app.register_blueprint(service_route.bp)
    app.register_blueprint(statistic_route.bp)

    logging.info('...::: Flask timeboard_service setup ends :::...')
    return app
