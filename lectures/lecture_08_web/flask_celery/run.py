import os

from flask import Flask, Blueprint, jsonify
from celery import Celery


folder_files = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

bp = Blueprint("all", __name__)


@bp.route("/")
def index():
    return "Hello!"


@bp.route("/<string:fname>/<string:content>")
def makefile(fname, content):
    fpath = os.path.join(folder_files, fname)
    make_file.delay(fpath, content)
    return jsonify({'result': True})


@bp.route("/files")
def list_files():
    files = os.listdir(folder_files)
    return jsonify({'files': files})


def create_app(app_name):
    app = Flask(app_name)
    app.register_blueprint(bp)
    return app


def make_celery(app_name=__name__):
    backend = "redis://localhost:6379/0"
    broker = backend.replace("0", "1")
    return Celery(app_name, backend=backend, broker=broker)


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


celery = make_celery()


@celery.task(name="make_file")
def make_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)


app = create_app(app_name=PKG_NAME)
init_celery(celery, app)

if __name__ == "__main__":
    app.run()
