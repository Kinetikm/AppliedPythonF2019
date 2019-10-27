import logging
import time
import uuid

from flask import Flask, request, g


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


def create_app():
    app = Flask(__name__)

    logging_setup(app)
    logging.info('...::: Flask timeboard_service setup starts :::...')

    app.config.from_mapping(
        DATABASE='/Users/danil/Documents/Technoatom/AppliedPythonF2019/homeworks' +
                 '/homework_06_web/timeboard_service/storage.dump',
    )

    logging.info('...::: Storage initializing :::...')
    from timeboard_service import storage

    app.teardown_appcontext(storage.close_fd)
    storage.init_fd(app)

    logging.info('...::: Storage initialized :::...')

    from timeboard_service import routing
    app.register_blueprint(routing.bp)

    logging.info('...::: Flask timeboard_service setup ends :::...')
    return app
