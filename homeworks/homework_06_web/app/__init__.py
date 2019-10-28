from flask import Flask


def create_app():
    app = Flask(__name__)
    import app.module.api as module
    app.register_blueprint(module.module)
    return app
